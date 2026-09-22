"""
University Library Management System (Online) - Digital / Ebook
Theo so do chuc nang Sach so + ISO/IEC/IEEE 29148:2018
Bo sung day du: giam sat TK, ngat quyen muon, ban, gioi han, DRM, quan ly kho, staff theo doi yeu cau.
"""
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Flask, render_template, redirect, url_for, flash, request,
    abort, jsonify, make_response
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)

from models import (
    db, User, Book, Loan, Reservation, Fine, Favorite, AuditLog,
    Violation, SystemConfig, log_action
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "ulms-demo-secret-key-2026-change-in-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ulms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Vui lòng đăng nhập để tiếp tục."
login_manager.login_message_category = "warning"

FINE_PER_DAY = 5000
DEFAULT_LOAN_DAYS = 14
DEFAULT_MAX_LOANS = 5


@app.context_processor
def inject_globals():
    if current_user.is_authenticated:
        fav_ids = [f.book_id for f in Favorite.query.filter_by(member_id=current_user.id).all()]
    else:
        fav_ids = []
    return dict(user_fav_ids=fav_ids, datetime_now=datetime.utcnow())


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("login"))
            if current_user.role not in roles:
                flash("Bạn không có quyền truy cập chức năng này.", "danger")
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator


def get_max_loans():
    return SystemConfig.get_int("max_loans_per_user", DEFAULT_MAX_LOANS)


def get_default_loan_days():
    return SystemConfig.get_int("default_loan_days", DEFAULT_LOAN_DAYS)


# ===================== AUTH =====================

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        university_id = request.form.get("university_id", "").strip()
        email = request.form.get("email", "").strip().lower()
        full_name = request.form.get("full_name", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not all([university_id, email, full_name, password]):
            flash("Vui lòng điền đầy đủ thông tin.", "danger")
            return render_template("register.html")
        if password != confirm:
            flash("Mật khẩu xác nhận không khớp.", "danger")
            return render_template("register.html")
        if not email.endswith(".edu.vn"):
            flash("Chỉ chấp nhận email nội bộ có đuôi .edu.vn.", "danger")
            return render_template("register.html")
        if User.query.filter(
            (User.university_id == university_id) | (User.email == email)
        ).first():
            flash("Mã sinh viên/email đã được sử dụng.", "danger")
            return render_template("register.html")

        user = User(
            university_id=university_id,
            email=email,
            full_name=full_name,
            role="member",
            can_borrow=True,
            is_active=True,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        log_action(user.id, "REGISTER", f"New account: {university_id}", request.remote_addr)
        flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not email.endswith(".edu.vn"):
            flash("Chỉ chấp nhận email nội bộ có đuôi .edu.vn.", "danger")
            return render_template("login.html")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if user.is_currently_banned():
                reason = user.ban_reason or "Vi phạm quy định bảo mật DRM / bản quyền."
                until = ""
                if user.ban_until:
                    until = f" (đến {user.ban_until.strftime('%d/%m/%Y %H:%M')})"
                flash(f"Tài khoản của bạn đã bị KHÓA{until}. Lý do: {reason}", "danger")
                log_action(user.id, "BANNED_LOGIN_ATTEMPT", f"Banned login for {email}", request.remote_addr)
                return render_template("login.html")
            login_user(user, remember=False)
            log_action(user.id, "LOGIN", "Successful login", request.remote_addr)
            flash(f"Xin chào, {user.full_name}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))
        flash("Email hoặc mật khẩu không đúng.", "danger")
        log_action(None, "LOGIN_FAILED", f"Failed login for {email}", request.remote_addr)
    return render_template("login.html")


@app.route("/report-violation", methods=["POST"])
@login_required
def report_violation():
    """Client-side DRM phat hien vi pham -> ghi Violation + ban theo chinh sach"""
    reason = request.form.get(
        "reason",
        "Cố ý vi phạm quy định bảo mật DRM (tải về / chụp màn hình / trích xuất văn bản)."
    )
    vtype = request.form.get("type", "copy")
    # Dem so lan vi pham Open/Warned cua user
    prev_count = Violation.query.filter(
        Violation.user_id == current_user.id,
        Violation.status.in_(["Open", "Warned", "AccessRevoked", "Banned"])
    ).count()
    severity = min(prev_count + 1, 3)

    v = Violation(
        user_id=current_user.id,
        violation_type=vtype,
        description=reason,
        severity=severity,
        status="Open",
    )
    db.session.add(v)
    db.session.commit()
    log_action(current_user.id, "VIOLATION_REPORTED", f"type={vtype} severity={severity}", request.remote_addr)

    # Chinh sach vi pham (so do 4)
    action_msg = ""
    if severity == 1:
        v.status = "Warned"
        v.action_taken = "Cảnh báo email + ghi nhận (lần 1)"
        action_msg = "Cảnh báo: Đây là lần vi phạm thứ 1. Lần sau sẽ bị khóa quyền đọc 5 ngày."
    elif severity == 2:
        v.status = "AccessRevoked"
        v.action_taken = "Khóa quyền đọc 5 ngày (lần 2)"
        current_user.can_borrow = False
        # Thu hoi tat ca quyen Active
        for loan in Loan.query.filter_by(member_id=current_user.id, status="Active").all():
            loan.status = "Revoked"
            loan.revoked_reason = "Vi phạm bản quyền lần 2"
            loan.return_date = datetime.utcnow()
            if loan.book and loan.book.available_copies is not None:
                loan.book.available_copies = min(loan.book.total_copies, loan.book.available_copies + 1)
        action_msg = "Tài khoản bị NGẮT QUYỀN MƯỢN/ĐỌC trong 5 ngày do vi phạm lần 2."
        # Tu dong mo lai sau 5 ngay (demo: set ban_until de staff biet)
        current_user.ban_until = datetime.utcnow() + timedelta(days=5)
        current_user.ban_reason = "Vi phạm DRM lần 2 - ngắt quyền mượn 5 ngày"
    else:
        v.status = "Banned"
        v.action_taken = "Ban vĩnh viễn / khóa đăng nhập (lần 3+)"
        current_user.is_active = False
        current_user.can_borrow = False
        current_user.ban_reason = reason
        current_user.ban_until = None  # vinh vien
        for loan in Loan.query.filter_by(member_id=current_user.id, status="Active").all():
            loan.status = "Revoked"
            loan.revoked_reason = "Ban do vi phạm bản quyền"
            loan.return_date = datetime.utcnow()
        action_msg = "Tài khoản bị KHÓA VĨNH VIỄN do vi phạm bản quyền nhiều lần."
        logout_user()

    v.handled_at = datetime.utcnow()
    db.session.commit()
    flash(action_msg, "danger")
    return jsonify({"status": "handled", "severity": severity, "redirect": url_for("login") if severity >= 3 else url_for("dashboard")})


@app.route("/logout")
@login_required
def logout():
    log_action(current_user.id, "LOGOUT", "", request.remote_addr)
    logout_user()
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for("index"))


# ===================== PUBLIC / MEMBER =====================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "admin":
        return redirect(url_for("admin_dashboard"))
    if current_user.role == "staff":
        return redirect(url_for("staff_dashboard"))
    active_loans = Loan.query.filter_by(member_id=current_user.id, status="Active").all()
    pending = Loan.query.filter(
        Loan.member_id == current_user.id,
        Loan.status.in_(["Pending Approval", "Pending Pickup"])
    ).all()
    unpaid_fines = Fine.query.filter_by(member_id=current_user.id, status="Unpaid").all()
    fav_records = Favorite.query.filter_by(member_id=current_user.id).order_by(Favorite.created_at.desc()).all()
    favorite_books = [f.book for f in fav_records]
    return render_template(
        "dashboard.html",
        active_loans=active_loans,
        pending=pending,
        unpaid_fines=unpaid_fines,
        favorite_books=favorite_books,
        can_borrow=current_user.can_borrow,
        account_status=current_user.account_status,
    )


@app.route("/notifications")
@login_required
@role_required("member")
def notifications():
    active_loans = Loan.query.filter_by(member_id=current_user.id, status="Active").all()
    overdue = [l for l in active_loans if l.is_overdue()]
    due_soon = []
    now = datetime.utcnow()
    for l in active_loans:
        if l.due_date and not l.is_overdue():
            days_left = (l.due_date - now).days
            if days_left <= 1:
                due_soon.append(l)
    return render_template("notifications.html", overdue=overdue, due_soon=due_soon)


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    subject = request.args.get("subject", "").strip()
    year = request.args.get("year", "").strip()
    query = Book.query.filter(Book.status.in_(["Available", "Hidden"]))  # an NoCopyright khoi search cong khai
    # Hidden chi admin/staff thay; member chi Available
    if not (current_user.is_authenticated and current_user.role in ("staff", "admin")):
        query = Book.query.filter(Book.status == "Available")
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(
                Book.title.ilike(like),
                Book.author.ilike(like),
                Book.isbn.ilike(like),
                Book.subject.ilike(like),
            )
        )
    if subject:
        query = query.filter(Book.subject.ilike(f"%{subject}%"))
    if year:
        try:
            query = query.filter(Book.year == int(year))
        except ValueError:
            pass
    books = query.order_by(Book.title).limit(50).all()
    if current_user.is_authenticated:
        log_action(current_user.id, "SEARCH", f"q={q}", request.remote_addr)
    return render_template("search.html", books=books, q=q, subject=subject, year=year)


@app.route("/book/<int:book_id>")
def book_detail(book_id):
    book = db.session.get(Book, book_id) or abort(404)
    if book.status == "NoCopyright" and not (current_user.is_authenticated and current_user.role in ("staff", "admin")):
        abort(404)
    return render_template("book_detail.html", book=book, max_loans=get_max_loans())


@app.route("/read-book/<int:book_id>")
@login_required
def read_book(book_id):
    book = db.session.get(Book, book_id) or abort(404)
    # Chi cho doc neu co quyen Active
    loan = Loan.query.filter_by(
        member_id=current_user.id, book_id=book.id, status="Active"
    ).first()
    if not loan and current_user.role not in ("staff", "admin"):
        flash("Bạn chưa có quyền đọc cuốn sách này. Hãy yêu cầu truy cập trước.", "warning")
        return redirect(url_for("book_detail", book_id=book_id))
    if not current_user.can_borrow and current_user.role == "member":
        flash("Quyền mượn/đọc của bạn đang bị ngắt. Liên hệ thư viện.", "danger")
        return redirect(url_for("dashboard"))

    log_action(current_user.id, "READ_ONLINE", f"Book #{book.id} - {book.title}", request.remote_addr)

    chapters = [
        {
            "chapter": "Chuong 1: Gioi thieu tong quan & Khái niem co ban",
            "content": (
                f"Chao mung doc gia {current_user.full_name} (Ma SV: {current_user.university_id}) den voi giao dien doc truc tuyen thuoc Thu vien So ULMS.\n\n"
                f"Tac pham: «{book.title}» | Tac gia: {book.author} | Chu de: {book.subject or 'Tai lieu hoc tap'} | Nam XB: {book.year or 2026}.\n\n"
                "Tai lieu nay duoc bao ve boi He thong Quan ly Ban quyen Ky thuat so ULMS DRM. "
                "Tat ca hanh vi tai xuong, sao chep van ban, in an, chup man hinh hoac chia se ngoai he thong deu bi chan va ghi nhan."
            )
        },
        {
            "chapter": "Chuong 2: Noi dung ly thuyet chuyen sau",
            "content": (
                f"Phan nay cung cap cac nguyen ly va phuong phap luan chinh yeu trong cuon sach «{book.title}».\n\n"
                "1. Tong quan cac cong cu va mo hinh phan tich hien dai.\n"
                "2. Quy trinh ung dung thuc tien trong moi truong nghien cuu dai hoc.\n"
                "3. Phuong phap danh gia chi so hieu qua va do luong ket qua thuc nghiem.\n\n"
                "Sinh vien co the su dung thanh dieu chinh giao dien (font, theme) de co trai nghiem doc toi uu."
            )
        },
        {
            "chapter": "Chuong 3: Cau hoi thao luan & Huong dan tu hoc",
            "content": (
                f"Tom tat bai tap va tai lieu tham khao bo tro cho hoc phan {book.subject or 'Chuyen nganh'}.\n\n"
                "• Bai tap 1: Phan tich case study ap dung mo hinh duoc de cap trong Chuong 2.\n"
                "• Bai tap 2: Thao luan nhom ve cac thach thuc cong nghe va giai phap phat trien ben vung.\n\n"
                f"Nhat ky doc sach truc tuyen cua tai khoan {current_user.email} da duoc luu tru an toan."
            )
        }
    ]

    response = make_response(render_template("read_book.html", book=book, chapters=chapters, loan=loan))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.route("/favorite/toggle/<int:book_id>", methods=["POST"])
@login_required
def toggle_favorite(book_id):
    book = db.session.get(Book, book_id) or abort(404)
    existing = Favorite.query.filter_by(member_id=current_user.id, book_id=book.id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        log_action(current_user.id, "UNFAVORITE_BOOK", f"Book #{book.id}", request.remote_addr)
        flash(f"Đã xóa «{book.title}» khỏi danh sách yêu thích.", "info")
    else:
        fav = Favorite(member_id=current_user.id, book_id=book.id)
        db.session.add(fav)
        db.session.commit()
        log_action(current_user.id, "FAVORITE_BOOK", f"Book #{book.id}", request.remote_addr)
        flash(f"Đã thêm «{book.title}» vào danh sách yêu thích.", "success")
    return redirect(request.referrer or url_for("book_detail", book_id=book_id))


@app.route("/request-access/<int:book_id>", methods=["POST"])
@login_required
@role_required("member")
def request_access(book_id):
    """Yeu cau quyen doc so - co the can staff duyet (Pending Approval) hoac cap ngay neu con ban"""
    book = db.session.get(Book, book_id) or abort(404)
    if book.status != "Available":
        flash("Sách không khả dụng để mượn (hết bản quyền / ẩn / lưu trữ).", "danger")
        return redirect(url_for("book_detail", book_id=book_id))
    if not current_user.can_borrow:
        flash("Quyền mượn/đọc của bạn đang bị ngắt. Liên hệ thư viện.", "danger")
        return redirect(url_for("book_detail", book_id=book_id))

    unpaid = Fine.query.filter_by(member_id=current_user.id, status="Unpaid").count()
    if unpaid > 0:
        flash("Bạn còn phí phạt chưa thanh toán. Không thể yêu cầu truy cập mới.", "danger")
        return redirect(url_for("book_detail", book_id=book_id))

    active_loan = Loan.query.filter_by(member_id=current_user.id, book_id=book.id, status="Active").first()
    if active_loan:
        flash(f"Bạn đã có quyền truy cập. Hạn đọc: {active_loan.due_date.strftime('%d/%m/%Y')}.", "info")
        return redirect(url_for("read_book", book_id=book.id))

    # Gioi han so sach dang muon (cau hinh he thong)
    max_loans = get_max_loans()
    active_count = Loan.query.filter(
        Loan.member_id == current_user.id,
        Loan.status.in_(["Active", "Pending Approval", "Pending Pickup"]),
    ).count()
    if active_count >= max_loans:
        flash(f"Bạn đã đạt giới hạn {max_loans} cuốn đang mượn/chờ duyệt.", "danger")
        return redirect(url_for("book_detail", book_id=book_id))

    loan_days = book.loan_days or get_default_loan_days()

    if book.available_copies > 0:
        # Cap quyen ngay (demo) - van ghi Pending neu muon bat buoc staff duyet
        # Theo so do: co the can staff theo doi. De staff thay yeu cau, dung Pending Approval
        require_approval = SystemConfig.get("require_staff_approval", "0") == "1"
        if require_approval:
            loan = Loan(
                member_id=current_user.id,
                book_id=book.id,
                status="Pending Approval",
            )
            book.available_copies -= 1
            db.session.add(loan)
            db.session.commit()
            log_action(current_user.id, "ACCESS_REQUEST", f"Book {book.isbn} Loan #{loan.id} Pending", request.remote_addr)
            flash(f"Đã gửi yêu cầu truy cập «{book.title}». Chờ thủ thư duyệt.", "success")
        else:
            loan = Loan(
                member_id=current_user.id,
                book_id=book.id,
                status="Active",
                pickup_date=datetime.utcnow(),
                due_date=datetime.utcnow() + timedelta(days=loan_days),
            )
            book.available_copies -= 1
            db.session.add(loan)
            db.session.commit()
            log_action(current_user.id, "REQUEST_ACCESS", f"Book {book.isbn} Loan #{loan.id}", request.remote_addr)
            flash(f"Đã cấp quyền đọc «{book.title}» trong {loan_days} ngày.", "success")
            return redirect(url_for("read_book", book_id=book.id))
    else:
        # Dat giu
        existing = Reservation.query.filter_by(
            member_id=current_user.id, book_id=book.id, status="Pending"
        ).first()
        if existing:
            flash("Bạn đã đặt giữ cuốn này rồi.", "warning")
            return redirect(url_for("book_detail", book_id=book_id))
        res = Reservation(member_id=current_user.id, book_id=book.id, status="Pending")
        db.session.add(res)
        db.session.commit()
        log_action(current_user.id, "RESERVATION", f"Book {book.isbn}", request.remote_addr)
        flash(f"Đã đặt giữ «{book.title}». Bạn sẽ nhận thông báo khi sẵn sàng.", "success")
    return redirect(url_for("dashboard"))


@app.route("/renew/<int:loan_id>", methods=["POST"])
@login_required
@role_required("member")
def renew_loan(loan_id):
    loan = db.session.get(Loan, loan_id) or abort(404)
    if loan.member_id != current_user.id:
        abort(403)
    if not current_user.can_borrow:
        flash("Quyền mượn đang bị ngắt.", "danger")
        return redirect(url_for("my_loans"))
    if not loan.can_renew():
        flash("Không thể gia hạn: đã đạt số lần tối đa, quá hạn, hoặc sách đang có người đặt giữ.", "danger")
        return redirect(url_for("my_loans"))
    days = loan.book.loan_days if loan.book else get_default_loan_days()
    loan.due_date = loan.due_date + timedelta(days=days)
    loan.renew_count += 1
    db.session.commit()
    log_action(current_user.id, "RENEW", f"Loan #{loan.id} new due {loan.due_date.date()}", request.remote_addr)
    flash(f"Gia hạn thành công. Hạn mới: {loan.due_date.strftime('%d/%m/%Y')}", "success")
    return redirect(url_for("my_loans"))


@app.route("/my-loans")
@login_required
@role_required("member")
def my_loans():
    loans = Loan.query.filter_by(member_id=current_user.id).order_by(Loan.request_date.desc()).all()
    fines = Fine.query.filter_by(member_id=current_user.id).order_by(Fine.created_at.desc()).all()
    fav_records = Favorite.query.filter_by(member_id=current_user.id).all()
    favorite_books = [f.book for f in fav_records]
    return render_template(
        "my_loans.html", loans=loans, fines=fines, favorite_books=favorite_books
    )


# ===================== STAFF =====================

@app.route("/staff")
@login_required
@role_required("staff", "admin")
def staff_dashboard():
    pending_loans = Loan.query.filter(
        Loan.status.in_(["Pending Approval", "Pending Pickup"])
    ).order_by(Loan.request_date).all()
    active_loans = Loan.query.filter_by(status="Active").order_by(Loan.due_date).all()
    ready_res = Reservation.query.filter_by(status="Ready").all()
    open_violations = Violation.query.filter(Violation.status.in_(["Open", "Warned"])).order_by(Violation.created_at.desc()).limit(20).all()
    return render_template(
        "staff_dashboard.html",
        pending_loans=pending_loans,
        active_loans=active_loans,
        ready_res=ready_res,
        open_violations=open_violations,
    )


@app.route("/staff/approve-access/<int:loan_id>", methods=["POST"])
@login_required
@role_required("staff", "admin")
def approve_access(loan_id):
    """Staff duyet yeu cau quyen doc so"""
    loan = db.session.get(Loan, loan_id) or abort(404)
    if loan.status not in ("Pending Approval", "Pending Pickup"):
        flash("Yêu cầu không ở trạng thái chờ duyệt.", "warning")
        return redirect(url_for("staff_dashboard"))
    days = loan.book.loan_days if loan.book else get_default_loan_days()
    loan.status = "Active"
    loan.pickup_date = datetime.utcnow()
    loan.due_date = datetime.utcnow() + timedelta(days=days)
    db.session.commit()
    log_action(current_user.id, "APPROVE_ACCESS", f"Loan #{loan.id}", request.remote_addr)
    flash(f"Đã duyệt quyền đọc cho {loan.member.full_name}. Hạn: {loan.due_date.strftime('%d/%m/%Y')}", "success")
    return redirect(url_for("staff_dashboard"))


@app.route("/staff/reject-access/<int:loan_id>", methods=["POST"])
@login_required
@role_required("staff", "admin")
def reject_access(loan_id):
    loan = db.session.get(Loan, loan_id) or abort(404)
    if loan.status not in ("Pending Approval", "Pending Pickup"):
        flash("Yêu cầu không ở trạng thái chờ duyệt.", "warning")
        return redirect(url_for("staff_dashboard"))
    reason = request.form.get("reason", "Từ chối bởi thủ thư")
    loan.status = "Cancelled"
    loan.revoked_reason = reason
    if loan.book:
        loan.book.available_copies = min(loan.book.total_copies, loan.book.available_copies + 1)
    db.session.commit()
    log_action(current_user.id, "REJECT_ACCESS", f"Loan #{loan.id} reason={reason}", request.remote_addr)
    flash("Đã từ chối yêu cầu.", "info")
    return redirect(url_for("staff_dashboard"))


@app.route("/staff/revoke-access/<int:loan_id>", methods=["POST"])
@login_required
@role_required("staff", "admin")
def revoke_access(loan_id):
    """Ngat quyen doc cua 1 loan dang Active"""
    loan = db.session.get(Loan, loan_id) or abort(404)
    if loan.status != "Active":
        flash("Chỉ thu hồi quyền đang Active.", "warning")
        return redirect(url_for("staff_dashboard"))
    reason = request.form.get("reason", "Thu hồi bởi thủ thư")
    loan.status = "Revoked"
    loan.revoked_reason = reason
    loan.return_date = datetime.utcnow()
    if loan.book:
        loan.book.available_copies = min(loan.book.total_copies, loan.book.available_copies + 1)
    db.session.commit()
    log_action(current_user.id, "REVOKE_ACCESS", f"Loan #{loan.id} reason={reason}", request.remote_addr)
    flash(f"Đã thu hồi quyền đọc Loan #{loan.id}.", "success")
    return redirect(request.referrer or url_for("staff_dashboard"))


@app.route("/staff/confirm-pickup/<int:loan_id>", methods=["POST"])
@login_required
@role_required("staff", "admin")
def confirm_pickup(loan_id):
    return approve_access(loan_id)


@app.route("/staff/return/<int:loan_id>", methods=["POST"])
@login_required
@role_required("staff", "admin")
def process_return(loan_id):
    loan = db.session.get(Loan, loan_id) or abort(404)
    if loan.status != "Active":
        flash("Chỉ có thể trả sách đang Active.", "warning")
        return redirect(url_for("staff_dashboard"))

    days = loan.days_overdue()
    fine_amount = 0
    if days > 0:
        fine_amount = days * FINE_PER_DAY
        fine = Fine(
            member_id=loan.member_id,
            loan_id=loan.id,
            amount=fine_amount,
            days_overdue=days,
            status="Unpaid",
        )
        db.session.add(fine)

    loan.status = "Returned"
    loan.return_date = datetime.utcnow()
    book = loan.book
    if book:
        book.available_copies = min(book.total_copies, book.available_copies + 1)
        next_res = (
            Reservation.query.filter_by(book_id=book.id, status="Pending")
            .order_by(Reservation.request_date)
            .first()
        )
        if next_res:
            next_res.status = "Ready"
            next_res.notified_at = datetime.utcnow()
            book.available_copies -= 1

    db.session.commit()
    log_action(current_user.id, "RETURN", f"Loan #{loan.id}, fine={fine_amount}", request.remote_addr)
    msg = "Đã ghi nhận trả / kết thúc quyền đọc."
    if fine_amount:
        msg += f" Phạt quá hạn: {fine_amount:,.0f} VND ({days} ngày)."
    flash(msg, "success")
    return redirect(url_for("staff_dashboard"))


@app.route("/staff/waive-fine/<int:fine_id>", methods=["POST"])
@login_required
@role_required("staff", "admin")
def waive_fine(fine_id):
    fine = db.session.get(Fine, fine_id) or abort(404)
    reason = request.form.get("reason", "Staff adjustment")
    fine.status = "Waived"
    fine.paid_at = datetime.utcnow()
    db.session.commit()
    log_action(current_user.id, "WAIVE_FINE", f"Fine #{fine.id} reason={reason}", request.remote_addr)
    flash("Đã miễn phạt.", "success")
    return redirect(request.referrer or url_for("staff_dashboard"))


@app.route("/staff/fulfill-reservation/<int:res_id>", methods=["POST"])
@login_required
@role_required("staff", "admin")
def fulfill_reservation(res_id):
    res = db.session.get(Reservation, res_id) or abort(404)
    if res.status != "Ready":
        flash("Đặt giữ chưa ở trạng thái Ready.", "warning")
        return redirect(url_for("staff_dashboard"))
    days = res.book.loan_days if res.book else get_default_loan_days()
    res.status = "Fulfilled"
    loan = Loan(
        member_id=res.member_id,
        book_id=res.book_id,
        status="Active",
        pickup_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=days),
    )
    db.session.add(loan)
    db.session.commit()
    log_action(current_user.id, "FULFILL_RESERVATION", f"Res #{res.id} -> Loan #{loan.id}", request.remote_addr)
    flash(f"Đã giao quyền đọc cho {res.member.full_name}.", "success")
    return redirect(url_for("staff_dashboard"))


@app.route("/staff/user/<int:user_id>")
@login_required
@role_required("staff", "admin")
def staff_user_detail(user_id):
    """Giam sat tai khoan: ngay tao, lich su muon, lich su xu phat, trang thai"""
    user = db.session.get(User, user_id) or abort(404)
    loans = Loan.query.filter_by(member_id=user.id).order_by(Loan.request_date.desc()).all()
    violations = Violation.query.filter_by(user_id=user.id).order_by(Violation.created_at.desc()).all()
    fines = Fine.query.filter_by(member_id=user.id).order_by(Fine.created_at.desc()).all()
    audit = AuditLog.query.filter_by(user_id=user.id).order_by(AuditLog.created_at.desc()).limit(50).all()
    return render_template(
        "staff_user_detail.html",
        user=user,
        loans=loans,
        violations=violations,
        fines=fines,
        audit=audit,
    )


@app.route("/staff/violations")
@login_required
@role_required("staff", "admin")
def staff_violations():
    status_filter = request.args.get("status", "")
    q = Violation.query
    if status_filter:
        q = q.filter_by(status=status_filter)
    violations = q.order_by(Violation.created_at.desc()).limit(100).all()
    return render_template("staff_violations.html", violations=violations, status_filter=status_filter)


@app.route("/staff/handle-violation/<int:vid>", methods=["POST"])
@login_required
@role_required("staff", "admin")
def handle_violation(vid):
    v = db.session.get(Violation, vid) or abort(404)
    action = request.form.get("action", "warn")
    note = request.form.get("note", "")
    user = v.member

    if action == "warn":
        v.status = "Warned"
        v.action_taken = f"Canh bao. {note}"
    elif action == "revoke_borrow":
        v.status = "AccessRevoked"
        v.action_taken = f"Ngat quyen muon. {note}"
        user.can_borrow = False
        for loan in Loan.query.filter_by(member_id=user.id, status="Active").all():
            loan.status = "Revoked"
            loan.revoked_reason = "Xử lý vi phạm bản quyền"
            loan.return_date = datetime.utcnow()
            if loan.book:
                loan.book.available_copies = min(loan.book.total_copies, loan.book.available_copies + 1)
    elif action == "ban_temp":
        days = int(request.form.get("days", 5))
        v.status = "Banned"
        v.action_taken = f"Ban tạm {days} ngay. {note}"
        user.is_active = False
        user.can_borrow = False
        user.ban_reason = note or v.description
        user.ban_until = datetime.utcnow() + timedelta(days=days)
    elif action == "ban_perm":
        v.status = "Banned"
        v.action_taken = f"Ban vĩnh viễn. {note}"
        user.is_active = False
        user.can_borrow = False
        user.ban_reason = note or v.description
        user.ban_until = None
    elif action == "close":
        v.status = "Closed"
        v.action_taken = f"Dong ho so. {note}"

    v.handled_by_id = current_user.id
    v.handled_at = datetime.utcnow()
    db.session.commit()
    log_action(current_user.id, "HANDLE_VIOLATION", f"V#{v.id} action={action}", request.remote_addr)
    flash(f"Đã xử lý vi phạm #{v.id}.", "success")
    return redirect(request.referrer or url_for("staff_violations"))


# ===================== ADMIN =====================

@app.route("/admin")
@login_required
@role_required("admin")
def admin_dashboard():
    stats = {
        "users": User.query.count(),
        "books": Book.query.count(),
        "active_loans": Loan.query.filter_by(status="Active").count(),
        "pending": Loan.query.filter(Loan.status.in_(["Pending Approval", "Pending Pickup"])).count(),
        "unpaid_fines": Fine.query.filter_by(status="Unpaid").count(),
        "open_violations": Violation.query.filter(Violation.status.in_(["Open", "Warned"])).count(),
    }
    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(20).all()
    return render_template("admin_dashboard.html", stats=stats, recent_logs=recent_logs)


@app.route("/admin/books")
@login_required
@role_required("admin")
def admin_books():
    books = Book.query.order_by(Book.title).all()
    return render_template("admin_books.html", books=books)


@app.route("/admin/books/add", methods=["GET", "POST"])
@login_required
@role_required("admin")
def admin_add_book():
    if request.method == "POST":
        isbn = request.form.get("isbn", "").strip()
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        subject = request.form.get("subject", "").strip()
        year = request.form.get("year", type=int)
        copies = request.form.get("copies", type=int) or 1
        loan_days = request.form.get("loan_days", type=int) or get_default_loan_days()
        status = request.form.get("status", "Available")
        has_digital = request.form.get("has_digital_file") == "on"
        if not all([isbn, title, author]):
            flash("ISBN, tiêu đề và tác giả là bắt buộc.", "danger")
            return render_template("admin_add_book.html")
        if Book.query.filter_by(isbn=isbn).first():
            flash("ISBN đã tồn tại.", "danger")
            return render_template("admin_add_book.html")
        book = Book(
            isbn=isbn, title=title, author=author,
            subject=subject, year=year,
            total_copies=copies, available_copies=copies,
            loan_days=loan_days, status=status, has_digital_file=has_digital,
        )
        db.session.add(book)
        db.session.commit()
        log_action(current_user.id, "ADD_BOOK", f"{isbn} - {title}", request.remote_addr)
        flash("Đã thêm sách thành công.", "success")
        return redirect(url_for("admin_books"))
    return render_template("admin_add_book.html")


@app.route("/admin/books/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def admin_edit_book(book_id):
    book = db.session.get(Book, book_id) or abort(404)
    if request.method == "POST":
        isbn = request.form.get("isbn", "").strip()
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        subject = request.form.get("subject", "").strip()
        year = request.form.get("year", type=int)
        total = request.form.get("copies", type=int)
        loan_days = request.form.get("loan_days", type=int) or book.loan_days
        status = request.form.get("status", book.status)
        has_digital = request.form.get("has_digital_file") == "on"
        if not all([isbn, title, author]) or not total or total < 1:
            flash("Dữ liệu không hợp lệ.", "danger")
            return render_template("admin_edit_book.html", book=book)
        duplicate = Book.query.filter(Book.isbn == isbn, Book.id != book.id).first()
        if duplicate:
            flash("ISBN đã tồn tại ở sách khác.", "danger")
            return render_template("admin_edit_book.html", book=book)
        borrowed = book.total_copies - book.available_copies
        if total < borrowed:
            flash(f"Không thể giảm tổng số bản dưới số bản đang giữ/mượn ({borrowed}).", "danger")
            return render_template("admin_edit_book.html", book=book)
        book.isbn, book.title, book.author = isbn, title, author
        book.subject, book.year = subject, year
        book.total_copies = total
        book.available_copies = total - borrowed
        book.loan_days = loan_days
        book.status = status
        book.has_digital_file = has_digital
        db.session.commit()
        log_action(current_user.id, "EDIT_BOOK", f"Book #{book.id} status={status}", request.remote_addr)
        flash("Đã cập nhật sách.", "success")
        return redirect(url_for("admin_books"))
    return render_template("admin_edit_book.html", book=book)


@app.route("/admin/books/<int:book_id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def admin_delete_book(book_id):
    book = db.session.get(Book, book_id) or abort(404)
    active = Loan.query.filter(
        Loan.book_id == book.id,
        Loan.status.in_(["Pending Approval", "Pending Pickup", "Active"])
    ).count()
    pending_res = Reservation.query.filter_by(book_id=book.id, status="Pending").count()
    if active or pending_res:
        flash("Không thể xóa sách đang có giao dịch. Hãy đổi trạng thái NoCopyright/Archived thay vì xóa.", "danger")
        return redirect(url_for("admin_books"))
    # Cho phep xoa khi het ban quyen hoac khong con giao dich
    title = book.title
    db.session.delete(book)
    db.session.commit()
    log_action(current_user.id, "DELETE_BOOK", title, request.remote_addr)
    flash("Đã xóa sách khỏi catalogue.", "success")
    return redirect(url_for("admin_books"))


@app.route("/admin/users")
@login_required
@role_required("admin")
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin_users.html", users=users)


@app.route("/admin/users/<int:user_id>")
@login_required
@role_required("admin")
def admin_user_detail(user_id):
    user = db.session.get(User, user_id) or abort(404)
    loans = Loan.query.filter_by(member_id=user.id).order_by(Loan.request_date.desc()).all()
    violations = Violation.query.filter_by(user_id=user.id).order_by(Violation.created_at.desc()).all()
    fines = Fine.query.filter_by(member_id=user.id).order_by(Fine.created_at.desc()).all()
    audit = AuditLog.query.filter_by(user_id=user.id).order_by(AuditLog.created_at.desc()).limit(50).all()
    return render_template(
        "admin_user_detail.html",
        user=user,
        loans=loans,
        violations=violations,
        fines=fines,
        audit=audit,
    )


@app.route("/admin/users/<int:user_id>/toggle", methods=["POST"])
@login_required
@role_required("admin")
def admin_toggle_user(user_id):
    user = db.session.get(User, user_id) or abort(404)
    if user.id == current_user.id:
        flash("Không thể tự khóa tài khoản Admin đang đăng nhập.", "warning")
        return redirect(url_for("admin_users"))
    action = request.form.get("action", "toggle_active")
    if action == "toggle_active":
        user.is_active = not user.is_active
        if not user.is_active:
            user.ban_reason = request.form.get("reason", "Khóa bởi Quản trị viên.")
            user.ban_until = None
            user.can_borrow = False
        else:
            user.ban_reason = None
            user.ban_until = None
            user.can_borrow = True
    elif action == "toggle_borrow":
        user.can_borrow = not user.can_borrow
        if not user.can_borrow:
            for loan in Loan.query.filter_by(member_id=user.id, status="Active").all():
                loan.status = "Revoked"
                loan.revoked_reason = "Admin ngắt quyền mượn"
                loan.return_date = datetime.utcnow()
                if loan.book:
                    loan.book.available_copies = min(loan.book.total_copies, loan.book.available_copies + 1)
    elif action == "ban_temp":
        days = int(request.form.get("days", 5))
        user.is_active = False
        user.can_borrow = False
        user.ban_reason = request.form.get("reason", f"Ban tạm {days} ngay")
        user.ban_until = datetime.utcnow() + timedelta(days=days)
    elif action == "ban_perm":
        user.is_active = False
        user.can_borrow = False
        user.ban_reason = request.form.get("reason", "Ban vĩnh viễn")
        user.ban_until = None
    elif action == "unban":
        user.is_active = True
        user.can_borrow = True
        user.ban_reason = None
        user.ban_until = None

    db.session.commit()
    log_action(current_user.id, "ADMIN_USER_ACTION", f"User #{user.id} action={action}", request.remote_addr)
    flash(f"Đã cập nhật tài khoản {user.full_name} ({user.account_status}).", "success")
    return redirect(request.referrer or url_for("admin_users"))


@app.route("/admin/config", methods=["GET", "POST"])
@login_required
@role_required("admin")
def admin_config():
    """Cau hinh he thong: gioi han muon, thoi han mac dinh, bat buoc staff duyet..."""
    if request.method == "POST":
        SystemConfig.set("max_loans_per_user", request.form.get("max_loans", DEFAULT_MAX_LOANS), "Gioi han so sach/user")
        SystemConfig.set("default_loan_days", request.form.get("default_loan_days", DEFAULT_LOAN_DAYS), "Thoi han muon mac dinh (ngay)")
        SystemConfig.set("require_staff_approval", "1" if request.form.get("require_staff_approval") else "0", "Bat buoc staff duyet yeu cau doc")
        SystemConfig.set("fine_per_day", request.form.get("fine_per_day", FINE_PER_DAY), "Muc phat VND/ngay")
        flash("Đã lưu cấu hình hệ thống.", "success")
        log_action(current_user.id, "UPDATE_CONFIG", "", request.remote_addr)
        return redirect(url_for("admin_config"))
    cfg = {
        "max_loans": SystemConfig.get_int("max_loans_per_user", DEFAULT_MAX_LOANS),
        "default_loan_days": SystemConfig.get_int("default_loan_days", DEFAULT_LOAN_DAYS),
        "require_staff_approval": SystemConfig.get("require_staff_approval", "0") == "1",
        "fine_per_day": SystemConfig.get_int("fine_per_day", FINE_PER_DAY),
    }
    return render_template("admin_config.html", cfg=cfg)


@app.route("/admin/reports")
@login_required
@role_required("admin")
def admin_reports():
    stats = {
        "total_books": Book.query.count(),
        "total_copies": sum((b.total_copies or 0) for b in Book.query.all()),
        "available_copies": sum((b.available_copies or 0) for b in Book.query.all()),
        "active_loans": Loan.query.filter_by(status="Active").count(),
        "returned_loans": Loan.query.filter_by(status="Returned").count(),
        "revoked_loans": Loan.query.filter_by(status="Revoked").count(),
        "unpaid_fines": sum((f.amount or 0) for f in Fine.query.filter_by(status="Unpaid").all()),
        "reservations": Reservation.query.filter(Reservation.status.in_(["Pending", "Ready"])).count(),
        "violations_total": Violation.query.count(),
        "violations_open": Violation.query.filter(Violation.status.in_(["Open", "Warned"])).count(),
        "banned_users": User.query.filter_by(is_active=False).count(),
    }
    return render_template("admin_reports.html", stats=stats)


@app.route("/admin/audit")
@login_required
@role_required("admin")
def admin_audit():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return render_template("admin_audit.html", logs=logs)


# ===================== ERRORS =====================

@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html", code=403, message="Truy cập bị từ chối (RBAC)"), 403


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, message="Không tìm thấy trang"), 404


# ===================== SEED =====================

def seed_data():
    if User.query.first():
        return
    # Config mac dinh
    SystemConfig.set("max_loans_per_user", "5", "Gioi han so sach/user")
    SystemConfig.set("default_loan_days", "14", "Thoi han muon mac dinh")
    SystemConfig.set("require_staff_approval", "1", "Bat buoc staff duyet (de staff thay yeu cau)")
    SystemConfig.set("fine_per_day", "5000", "Phat VND/ngay")

    admin = User(
        university_id="ADMIN001",
        email="admin@lib.university.edu.vn",
        full_name="Library Administrator",
        role="admin",
        can_borrow=True,
    )
    admin.set_password("admin123")
    staff = User(
        university_id="STAFF001",
        email="lan@lib.university.edu.vn",
        full_name="Ms. Lan - Circulation",
        role="staff",
        can_borrow=True,
    )
    staff.set_password("staff123")
    member1 = User(
        university_id="SV2024001",
        email="an.nguyen@student.university.edu.vn",
        full_name="Nguyễn Văn An",
        role="member",
        can_borrow=True,
    )
    member1.set_password("student123")
    member2 = User(
        university_id="SV2024002",
        email="tuan@fit.university.edu.vn",
        full_name="Dr. Tuấn",
        role="member",
        can_borrow=True,
    )
    member2.set_password("student123")
    db.session.add_all([admin, staff, member1, member2])

    books_data = [
        ("9780134685991", "Effective Java", "Joshua Bloch", "Programming", 2018, 3, 14),
        ("9781492052203", "Designing Data-Intensive Applications", "Martin Kleppmann", "Software Engineering", 2017, 2, 14),
        ("9780132350884", "Clean Code", "Robert C. Martin", "Software Engineering", 2008, 4, 7),
        ("9780201633610", "Design Patterns", "Erich Gamma et al.", "Software Engineering", 1994, 2, 30),
        ("9780135957059", "The Pragmatic Programmer", "David Thomas, Andrew Hunt", "Programming", 2019, 3, 14),
        ("9780262033848", "Introduction to Algorithms", "Cormen et al.", "Algorithms", 2009, 2, 14),
        ("9781492032649", "Python for Data Analysis", "Wes McKinney", "Data Science", 2022, 2, 14),
        ("9780134685992", "Software Engineering (10th)", "Ian Sommerville", "Software Engineering", 2015, 3, 14),
        ("9780596007126", "Head First Design Patterns", "Eric Freeman", "Software Engineering", 2004, 1, 7),
        ("9780131103627", "The C Programming Language", "Kernighan & Ritchie", "Programming", 1988, 2, 30),
        ("9781491946008", "Fluent Python", "Luciano Ramalho", "Programming", 2022, 2, 14),
        ("9781617294945", "Grokking Algorithms", "Aditya Bhargava", "Algorithms", 2016, 3, 14),
    ]
    for isbn, title, author, subject, year, copies, loan_days in books_data:
        b = Book(
            isbn=isbn, title=title, author=author,
            subject=subject, year=year,
            total_copies=copies, available_copies=copies,
            loan_days=loan_days, status="Available", has_digital_file=True,
        )
        db.session.add(b)
    db.session.commit()
    print("Seed data created successfully.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True, host="0.0.0.0", port=5000)
