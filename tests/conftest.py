"""Shared fixtures for ULMS Online application tests.

These tests use a fresh in-memory SQLite database and never touch instance/ulms.db.
"""
from datetime import datetime, timedelta, UTC, UTC

import pytest

from app import app as flask_app
from models import db, User, Book, Loan, SystemConfig


@pytest.fixture()
def app():
    flask_app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key",
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False,
    )

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        SystemConfig.set("max_loans_per_user", "5", "test")
        SystemConfig.set("default_loan_days", "14", "test")
        SystemConfig.set("require_admin_approval", "1", "test")
        SystemConfig.set("fine_per_day", "5000", "test")
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def member(app):
    user = User(
        university_id="TEST-MEMBER-001",
        email="member@test.edu.vn",
        full_name="Test Member",
        role="member",
        is_active=True,
        can_borrow=True,
    )
    user.set_password("TestPassword123!")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def circulation_admin(app):
    user = User(
        university_id="TEST-CIRCULATION-ADMIN-001",
        email="circulation-admin@test.edu.vn",
        full_name="Test Circulation Admin",
        role="admin",
        is_active=True,
        can_borrow=True,
    )
    user.set_password("TestPassword123!")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def admin(app):
    user = User(
        university_id="TEST-ADMIN-001",
        email="admin@test.edu.vn",
        full_name="Test Admin",
        role="admin",
        is_active=True,
        can_borrow=True,
    )
    user.set_password("TestPassword123!")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def book(app):
    item = Book(
        isbn="9780000000001",
        title="Test Digital Book",
        author="Test Author",
        subject="Testing",
        year=2025,
        total_copies=2,
        available_copies=2,
        loan_days=14,
        status="Available",
        has_digital_file=True,
    )
    db.session.add(item)
    db.session.commit()
    return item


def login_as(client, user, password="TestPassword123!"):
    """Log in through the real login form and return its response."""
    return client.post(
        "/login",
        data={"email": user.email, "password": password},
        follow_redirects=True,
    )


@pytest.fixture()
def login_helper():
    return login_as


@pytest.fixture()
def active_loan(app, member, book):
    from models import Loan

    loan = Loan(
        member_id=member.id,
        book_id=book.id,
        status="Active",
        pickup_date=datetime.now(UTC) - timedelta(days=3),
        due_date=datetime.now(UTC)
         + timedelta(days=7),
    )
    book.available_copies -= 1
    db.session.add(loan)
    db.session.commit()
    return loan
