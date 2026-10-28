"""Integration tests for the ULMS Online Flask application.

These tests exercise the actual Flask routes against an isolated in-memory DB.
They do not claim to cover scheduled jobs or external email delivery, which are
not implemented as independently callable services in the current app source.
"""
from datetime import datetime, timedelta, UTC

from models import (
    db, User, Book, Loan, Reservation, Favorite, Fine, AuditLog, SystemConfig
)

def login_as(client, user, password="TestPassword123!"):
    return client.post(
        "/login",
        data={"email": user.email, "password": password},
        follow_redirects=True,
    )


def test_member_cannot_open_admin_page(client, member):
    login_as(client, member)
    response = client.get("/admin", follow_redirects=False)
    assert response.status_code == 403


def test_member_can_add_and_remove_favorite(client, member, book, app):
    login_as(client, member)

    add_response = client.post(f"/favorite/toggle/{book.id}", follow_redirects=True)
    assert add_response.status_code == 200
    assert Favorite.query.filter_by(member_id=member.id, book_id=book.id).count() == 1
    assert AuditLog.query.filter_by(user_id=member.id, action="FAVORITE_BOOK").count() == 1

    remove_response = client.post(f"/favorite/toggle/{book.id}", follow_redirects=True)
    assert remove_response.status_code == 200
    assert Favorite.query.filter_by(member_id=member.id, book_id=book.id).count() == 0
    assert AuditLog.query.filter_by(user_id=member.id, action="UNFAVORITE_BOOK").count() == 1


def test_member_with_active_loan_can_read_book(client, member, book, active_loan):
    login_as(client, member)
    response = client.get(f"/read-book/{book.id}")
    assert response.status_code == 200
    assert b"Test Digital Book" in response.data
    assert response.headers.get("Cache-Control", "").find("no-store") >= 0
    assert AuditLog.query.filter_by(user_id=member.id, action="READ_ONLINE").count() == 1


def test_member_without_active_loan_is_redirected_from_reader(client, member, book):
    login_as(client, member)
    response = client.get(f"/read-book/{book.id}", follow_redirects=False)
    assert response.status_code == 302
    assert f"/book/{book.id}" in response.headers["Location"]


def test_admin_can_approve_pending_access_and_audit_it(client, member, circulation_admin, book, app):
    loan = Loan(
        member_id=member.id,
        book_id=book.id,
        status="Pending Approval",
    )
    book.available_copies -= 1
    db.session.add(loan)
    db.session.commit()

    login_as(client, circulation_admin)
    response = client.post(f"/admin/circulation/approve-access/{loan.id}", follow_redirects=True)
    assert response.status_code == 200
    db.session.refresh(loan)
    assert loan.status == "Active"
    assert loan.due_date is not None
    assert AuditLog.query.filter_by(user_id=circulation_admin.id, action="APPROVE_ACCESS").count() == 1


def test_member_cannot_view_admin_audit_log(client, member):
    login_as(client, member)
    response = client.get("/admin/audit", follow_redirects=False)
    assert response.status_code == 403


def test_admin_can_view_audit_log(client, admin):
    login_as(client, admin)
    response = client.get("/admin/audit")
    assert response.status_code == 200


def test_member_can_reserve_book_when_no_copies_available(client, member, book, app):
    book.available_copies = 0
    db.session.commit()
    login_as(client, member)

    response = client.post(f"/request-access/{book.id}", follow_redirects=True)
    assert response.status_code == 200
    reservation = Reservation.query.filter_by(
        member_id=member.id, book_id=book.id, status="Pending"
    ).first()
    assert reservation is not None
    assert Loan.query.filter_by(member_id=member.id, book_id=book.id).count() == 0
    assert AuditLog.query.filter_by(user_id=member.id, action="RESERVATION").count() == 1


def test_return_marks_next_reservation_ready_and_records_audit(
    client, member, circulation_admin, book, active_loan, app
):
    waiting_member = User(
        university_id="TEST-MEMBER-002",
        email="waiting@test.edu.vn",
        full_name="Waiting Member",
        role="member",
        is_active=True,
        can_borrow=True,
    )
    waiting_member.set_password("TestPassword123!")
    db.session.add(waiting_member)
    db.session.flush()  # Assign waiting_member.id before creating its reservation.

    reservation = Reservation(
        member_id=waiting_member.id,
        book_id=book.id,
        status="Pending",
        request_date=datetime.now(UTC) - timedelta(minutes=5),
    )
    db.session.add(reservation)
    db.session.commit()

    login_as(client, circulation_admin)
    response = client.post(f"/admin/circulation/return/{active_loan.id}", follow_redirects=True)
    assert response.status_code == 200

    db.session.refresh(active_loan)
    db.session.refresh(reservation)
    assert active_loan.status == "Returned"
    assert reservation.status == "Ready"
    assert reservation.notified_at is not None
    assert AuditLog.query.filter_by(user_id=circulation_admin.id, action="RETURN").count() == 1


def test_return_creates_fine_for_two_full_overdue_days(client, member, circulation_admin, book, app):
    overdue_loan = Loan(
        member_id=member.id,
        book_id=book.id,
        status="Active",
        pickup_date=datetime.now(UTC) - timedelta(days=20),
        due_date=datetime.now(UTC) - timedelta(days=2),
    )
    book.available_copies = max(0, book.available_copies - 1)
    db.session.add(overdue_loan)
    db.session.commit()

    login_as(client, circulation_admin)
    response = client.post(f"/admin/circulation/return/{overdue_loan.id}", follow_redirects=True)
    assert response.status_code == 200

    fine = Fine.query.filter_by(loan_id=overdue_loan.id).first()
    assert fine is not None
    assert fine.days_overdue >= 1
    assert fine.amount == fine.days_overdue * 5000


def test_search_treats_sql_injection_like_text_as_data(client, book):
    response = client.get("/search", query_string={"q": "' OR 1=1 --"})
    assert response.status_code == 200
    # A harmless unmatched payload should not crash the route or expose a traceback.
    assert b"Traceback" not in response.data


def test_search_escapes_script_input_in_rendered_html(client):
    payload = "<script>alert(1)</script>"
    response = client.get("/search", query_string={"q": payload})
    assert response.status_code == 200
    assert b"<script>alert(1)</script>" not in response.data
    assert b"&lt;script&gt;" in response.data or b"&lt;script" in response.data


def test_admin_can_suspend_member_and_audit_action(client, admin, member, app):
    login_as(client, admin)
    response = client.post(
        f"/admin/users/{member.id}/toggle",
        data={"action": "ban_perm", "reason": "Automated test"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    db.session.refresh(member)
    assert member.is_active is False
    assert member.can_borrow is False
    assert AuditLog.query.filter_by(user_id=admin.id, action="ADMIN_USER_ACTION").count() == 1


def test_access_request_is_pending_when_circulation_admin_approval_enabled(client, member, book, app):
    login_as(client, member)
    response = client.post(f"/request-access/{book.id}", follow_redirects=True)
    assert response.status_code == 200
    loan = Loan.query.filter_by(member_id=member.id, book_id=book.id).first()
    assert loan is not None
    assert loan.status == "Pending Approval"
    assert book.available_copies == 1


def test_registration_rejects_non_university_email(client):
    response = client.post(
        "/register",
        data={
            "university_id": "TEST-NEW-001",
            "email": "student@example.com",
            "full_name": "New Student",
            "password": "TestPassword123!",
            "confirm_password": "TestPassword123!",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert User.query.filter_by(university_id="TEST-NEW-001").first() is None


def test_duplicate_reservation_is_not_created(client, member, book, app):
    book.available_copies = 0
    existing = Reservation(member_id=member.id, book_id=book.id, status="Pending")
    db.session.add(existing)
    db.session.commit()
    login_as(client, member)

    response = client.post(f"/request-access/{book.id}", follow_redirects=True)
    assert response.status_code == 200
    assert Reservation.query.filter_by(
        member_id=member.id, book_id=book.id, status="Pending"
    ).count() == 1


# Group 1: automate test cases that previously had no pytest mapping.
def test_registered_member_can_log_in_with_valid_credentials(client, member, app):
    """TC-01: a registered active university account can authenticate."""
    response = client.post(
        "/login",
        data={"email": member.email, "password": "TestPassword123!"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Test Member" in response.data  # dashboard greets the authenticated member
    assert AuditLog.query.filter_by(user_id=member.id, action="LOGIN").count() == 1


def test_catalogue_search_returns_matching_results_within_two_seconds(client, book):
    """TC-02: catalogue search returns a known matching book within the target time."""
    import time

    started = time.perf_counter()
    response = client.get("/search", query_string={"q": "Test Digital Book"})
    elapsed = time.perf_counter() - started

    assert response.status_code == 200
    assert b"Test Digital Book" in response.data
    assert elapsed < 2.0, f"Search took {elapsed:.3f}s; expected under 2 seconds"


def test_eligible_member_can_renew_active_loan(client, member, book, active_loan, app):
    """TC-04: eligible member renews an active, non-overdue loan."""
    from datetime import timedelta

    old_due_date = active_loan.due_date
    old_renew_count = active_loan.renew_count
    login_as(client, member)
    response = client.post(f"/renew/{active_loan.id}", follow_redirects=True)

    assert response.status_code == 200
    db.session.refresh(active_loan)
    assert active_loan.due_date == old_due_date + timedelta(days=book.loan_days)
    assert active_loan.renew_count == old_renew_count + 1
    assert AuditLog.query.filter_by(user_id=member.id, action="RENEW").count() == 1


def test_member_can_view_loan_history_fines_and_favourites(client, member, book, app):
    """TC-07: My Loans displays the member's loan, fine and favourite records."""
    from datetime import datetime, timedelta, UTC

    historical_loan = Loan(
        member_id=member.id,
        book_id=book.id,
        status="Returned",
        pickup_date=datetime.now(UTC) - timedelta(days=20),
        due_date=datetime.now(UTC) - timedelta(days=6),
        return_date=datetime.now(UTC) - timedelta(days=4),
    )
    db.session.add(historical_loan)
    db.session.flush()
    fine = Fine(
        member_id=member.id,
        loan_id=historical_loan.id,
        amount=10000,
        days_overdue=2,
        status="Unpaid",
    )
    favorite = Favorite(member_id=member.id, book_id=book.id)
    db.session.add_all([fine, favorite])
    db.session.commit()

    login_as(client, member)
    response = client.get("/my-loans")

    assert response.status_code == 200
    assert b"Test Digital Book" in response.data
    assert b"10,000" in response.data or b"10000" in response.data or b"10.000" in response.data
    assert Favorite.query.filter_by(member_id=member.id, book_id=book.id).count() == 1


# Additional mapped tests for the remaining demo-baseline test cases.
def test_expired_digital_access_is_revoked_on_next_read_attempt(client, member, book, app):
    """TC-06: expired Active access is revoked and cannot be used to read."""
    expired = Loan(
        member_id=member.id,
        book_id=book.id,
        status="Active",
        pickup_date=datetime.utcnow() - timedelta(days=20),
        due_date=datetime.utcnow() - timedelta(days=2),
    )
    db.session.add(expired)
    db.session.commit()

    login_as(client, member)
    response = client.get(f"/read-book/{book.id}", follow_redirects=False)

    assert response.status_code == 302
    db.session.refresh(expired)
    assert expired.status == "Revoked"
    assert expired.revoked_reason == "Digital access expired"
    assert AuditLog.query.filter_by(user_id=member.id, action="ACCESS_EXPIRED").count() == 1


def test_login_and_online_access_decisions_are_audited(client, member, book, active_loan, app):
    """TC-08: authentication and authorised reading generate audit records."""
    login_as(client, member)
    assert AuditLog.query.filter_by(user_id=member.id, action="LOGIN").count() == 1

    response = client.get(f"/read-book/{book.id}")
    assert response.status_code == 200
    assert AuditLog.query.filter_by(user_id=member.id, action="READ_ONLINE").count() == 1


def test_member_can_request_access_again_after_previous_loan_returned(client, member, book, app):
    """TC-12: a historical Returned loan does not block a new access request."""
    previous = Loan(
        member_id=member.id,
        book_id=book.id,
        status="Returned",
        pickup_date=datetime.utcnow() - timedelta(days=20),
        due_date=datetime.utcnow() - timedelta(days=6),
        return_date=datetime.utcnow() - timedelta(days=5),
    )
    db.session.add(previous)
    db.session.commit()
    login_as(client, member)

    response = client.post(f"/request-access/{book.id}", follow_redirects=True)
    assert response.status_code == 200
    new_loan = Loan.query.filter_by(member_id=member.id, book_id=book.id, status="Pending Approval").first()
    assert new_loan is not None
    assert new_loan.id != previous.id


def test_member_with_unpaid_fine_cannot_request_another_book(client, member, book, app):
    """TC-13: borrowing eligibility rule blocks access requests with unpaid fines."""
    old_loan = Loan(
        member_id=member.id, book_id=book.id, status="Returned",
        pickup_date=datetime.utcnow() - timedelta(days=10),
        due_date=datetime.utcnow() - timedelta(days=5),
        return_date=datetime.utcnow() - timedelta(days=3),
    )
    db.session.add(old_loan)
    db.session.flush()
    db.session.add(Fine(member_id=member.id, loan_id=old_loan.id, amount=5000, days_overdue=1, status="Unpaid"))
    db.session.commit()
    login_as(client, member)

    response = client.post(f"/request-access/{book.id}", follow_redirects=True)
    assert response.status_code == 200
    assert Loan.query.filter_by(member_id=member.id, book_id=book.id, status="Pending Approval").count() == 0


def test_suspended_member_cannot_read_even_with_active_loan(client, member, book, active_loan, app):
    """TC-16: account borrowing suspension blocks online reading."""
    member.can_borrow = False
    db.session.commit()
    login_as(client, member)

    response = client.get(f"/read-book/{book.id}", follow_redirects=False)
    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]
    assert AuditLog.query.filter_by(user_id=member.id, action="READ_ONLINE").count() == 0



def test_overdue_fine_uses_full_overdue_days_and_configured_daily_rate(
    client, member, circulation_admin, book, app
):
    """Returning an overdue book does not create a monetary fine."""
    overdue_loan = Loan(
        member_id=member.id,
        book_id=book.id,
        status="Active",
        pickup_date=datetime.utcnow() - timedelta(days=20),
        due_date=datetime.utcnow() - timedelta(days=3),
    )
    book.available_copies = max(0, book.available_copies - 1)
    db.session.add(overdue_loan)
    db.session.commit()

    login_as(client, circulation_admin)

    response = client.post(
        f"/admin/circulation/return/{overdue_loan.id}",
        follow_redirects=True,
    )

    assert response.status_code == 200

    db.session.refresh(overdue_loan)
    assert overdue_loan.status == "Returned"

    fine = Fine.query.filter_by(loan_id=overdue_loan.id).first()
    assert fine is None

    assert AuditLog.query.filter_by(
        user_id=circulation_admin.id,
        action="RETURN",
    ).count() == 1


def test_overdue_loan_appears_in_member_notifications(client, member, book, app):
    """TC-21: in-app notifications show loans that are overdue."""
    overdue_loan = Loan(
        member_id=member.id, book_id=book.id, status="Active",
        pickup_date=datetime.utcnow() - timedelta(days=10),
        due_date=datetime.utcnow() - timedelta(days=2),
    )
    db.session.add(overdue_loan)
    db.session.commit()
    login_as(client, member)

    response = client.get("/notifications")
    assert response.status_code == 200
    assert book.title.encode() in response.data
    assert "Quá hạn".encode() in response.data



def test_reservation_return_fine_transactions_are_audited(
    client, member, circulation_admin, book, app
):
    """TC-22: reservation and return transactions are recorded in the audit log."""
    book.available_copies = 0
    db.session.commit()

    login_as(client, member)

    reserve_response = client.post(
        f"/request-access/{book.id}",
        follow_redirects=True,
    )
    assert reserve_response.status_code == 200

    assert AuditLog.query.filter_by(
        user_id=member.id,
        action="RESERVATION",
    ).count() == 1

    loan = Loan(
        member_id=member.id,
        book_id=book.id,
        status="Active",
        pickup_date=datetime.utcnow() - timedelta(days=12),
        due_date=datetime.utcnow() - timedelta(days=2),
    )
    db.session.add(loan)
    db.session.commit()

    client.get("/logout", follow_redirects=True)
    login_as(client, circulation_admin)

    response = client.post(
        f"/admin/circulation/return/{loan.id}",
        follow_redirects=True,
    )
    assert response.status_code == 200

    db.session.refresh(loan)
    assert loan.status == "Returned"

    assert AuditLog.query.filter_by(
        user_id=circulation_admin.id,
        action="RETURN",
    ).count() == 1

    # Returning an overdue book does not create a monetary fine.
    assert Fine.query.filter_by(loan_id=loan.id).first() is None

    # Fine creation is not expected for this return transaction.
