from datetime import datetime, UTC, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="member")  # member | admin
    is_active = db.Column(db.Boolean, default=True)          # False = khoa dang nhap
    can_borrow = db.Column(db.Boolean, default=True)         # False = ngat quyen muon/doc
    ban_reason = db.Column(db.String(255), nullable=True)
    ban_until = db.Column(db.DateTime, nullable=True)        # None = ban vinh vien khi is_active=False
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    loans = db.relationship("Loan", backref="member", lazy="dynamic")
    reservations = db.relationship("Reservation", backref="member", lazy="dynamic")
    fines = db.relationship("Fine", backref="member", lazy="dynamic")
    favorites = db.relationship("Favorite", backref="member", lazy="dynamic", cascade="all, delete-orphan")
    violations = db.relationship("Violation", backref="member", lazy="dynamic", foreign_keys="Violation.user_id")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, *roles):
        return self.role in roles

    @property
    def account_status(self):
        if not self.is_active:
            if self.ban_until and self.ban_until > datetime.now(UTC):
                return "Banned tạm thời"
            return "Banned / Vô hiệu hóa"
        if not self.can_borrow:
            return "Ngắt quyền mượn"
        return "Bình thường"

    def is_currently_banned(self):
        if not self.is_active:
            if self.ban_until is None:
                return True
            if self.ban_until > datetime.now(UTC):
                return True
            # Het han ban tam -> tu mo
            self.is_active = True
            self.ban_reason = None
            self.ban_until = None
            db.session.commit()
            return False
        return False


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(120))
    year = db.Column(db.Integer)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    loan_days = db.Column(db.Integer, default=14)            # thoi han muon theo loai sach
    status = db.Column(db.String(30), default="Available")   # Available | Hidden | NoCopyright | Archived
    has_digital_file = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    loans = db.relationship("Loan", backref="book", lazy="dynamic")
    reservations = db.relationship("Reservation", backref="book", lazy="dynamic")
    favorites = db.relationship("Favorite", backref="book", lazy="dynamic", cascade="all, delete-orphan")

    @property
    def display_status(self):
        if self.status == "NoCopyright":
            return "Hết bản quyền"
        if self.status == "Hidden":
            return "Ẩn"
        if self.status == "Archived":
            return "Lưu trữ"
        if self.available_copies > 0:
            return "Available"
        return "On Loan"


class Loan(db.Model):
    """Quyen doc so (digital access). Status: Pending Approval | Active | Returned | Revoked | Cancelled"""
    __tablename__ = "loans"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    pickup_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(30), default="Pending Approval")
    renew_count = db.Column(db.Integer, default=0)
    max_renewals = db.Column(db.Integer, default=2)
    revoked_reason = db.Column(db.String(255), nullable=True)

    def is_overdue(self):
        if self.status != "Active" or not self.due_date:
            return False

        due_date = self.due_date

        # SQLite có thể trả về datetime không có múi giờ.
        # Nếu có múi giờ, chuyển về dạng naive để so sánh nhất quán.
        if due_date.tzinfo is not None:
            due_date = due_date.replace(tzinfo=None)

        return datetime.now() > due_date

    def days_overdue(self):
        if not self.is_overdue():
            return 0

        due_date = self.due_date

        if due_date.tzinfo is not None:
            due_date = due_date.replace(tzinfo=None)

        return max(0, (datetime.now() - due_date).days)

    def can_renew(self):
        if self.status != "Active":
            return False
        if self.is_overdue():
            return False
        if self.renew_count >= self.max_renewals:
            return False
        pending_res = Reservation.query.filter_by(book_id=self.book_id, status="Pending").first()
        if pending_res:
            return False
        return True


class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("member_id", "book_id", name="_user_book_fav_uc"),)


class Reservation(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default="Pending")
    notified_at = db.Column(db.DateTime, nullable=True)


class Fine(db.Model):
    __tablename__ = "fines"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # A fine may relate to a loan (legacy overdue records) or a copyright violation.
    loan_id = db.Column(db.Integer, db.ForeignKey("loans.id"), nullable=True)
    violation_id = db.Column(db.Integer, db.ForeignKey("violations.id"), nullable=True, index=True)
    fine_type = db.Column(db.String(30), nullable=False, default="Copyright")
    description = db.Column(db.Text, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    days_overdue = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="Unpaid")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)

    loan = db.relationship("Loan", backref="fines")
    violation = db.relationship("Violation", backref=db.backref("fines", lazy="dynamic"))


class PaymentTransaction(db.Model):
    """Recorded simulated payments; this does not represent a real money transfer."""
    __tablename__ = "payment_transactions"
    id = db.Column(db.Integer, primary_key=True)
    transaction_code = db.Column(db.String(40), unique=True, nullable=False, index=True)
    fine_id = db.Column(db.Integer, db.ForeignKey("fines.id"), nullable=False, index=True)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(30), nullable=False, default="Simulation")
    status = db.Column(db.String(20), nullable=False, default="Completed")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    fine = db.relationship("Fine", backref=db.backref("payment_transactions", lazy="dynamic"))
    member = db.relationship("User", backref=db.backref("payment_transactions", lazy="dynamic"))


class Violation(db.Model):
    """Lich su vi pham ban quyen / quy dinh (so do 2.4 + 3.3 + 4)"""
    __tablename__ = "violations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    violation_type = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.Integer, nullable=True, default=None)
    status = db.Column(db.String(30), default="Open")
    action_taken = db.Column(db.String(255), nullable=True)
    handled_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    handled_at = db.Column(db.DateTime, nullable=True)

    handled_by = db.relationship("User", foreign_keys=[handled_by_id])


class SystemConfig(db.Model):
    """Cau hinh he thong (so do 3.2)"""
    __tablename__ = "system_config"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))

    @staticmethod
    def get(key, default=None):
        row = SystemConfig.query.filter_by(key=key).first()
        return row.value if row else default

    @staticmethod
    def get_int(key, default=0):
        try:
            return int(SystemConfig.get(key, default))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def set(key, value, description=None):
        row = SystemConfig.query.filter_by(key=key).first()
        if row:
            row.value = str(value)
            if description:
                row.description = description
        else:
            row = SystemConfig(key=key, value=str(value), description=description)
            db.session.add(row)
        db.session.commit()


class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="audit_logs")


def log_action(user_id, action, details="", ip=""):
    entry = AuditLog(user_id=user_id, action=action, details=details, ip_address=ip)
    db.session.add(entry)
    db.session.commit()


class SoftwareRequirement(db.Model):
    """Requirements-engineering records; separate from library book records."""
    __tablename__ = "software_requirements"

    id = db.Column(db.Integer, primary_key=True)
    req_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False, default="")
    statement = db.Column(db.Text, nullable=False, default="")
    req_type = db.Column(db.String(50), nullable=True)
    priority = db.Column(db.String(30), nullable=True)
    status = db.Column(db.String(30), nullable=True)
    source = db.Column(db.String(255), nullable=True)
    rationale = db.Column(db.Text, nullable=True)
    owner = db.Column(db.String(120), nullable=True)
    release = db.Column(db.String(80), nullable=True)
    acceptance_criteria = db.Column(db.Text, nullable=True)
    verification_method = db.Column(db.String(120), nullable=True)
    complexity = db.Column(db.String(50), nullable=True)
    dependencies = db.Column(db.Text, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    source_data = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        import json
        data = {
            "id": self.req_id, "title": self.title, "statement": self.statement,
            "type": self.req_type, "priority": self.priority, "status": self.status,
            "source": self.source, "rationale": self.rationale, "owner": self.owner,
            "release": self.release, "acceptance_criteria": self.acceptance_criteria,
            "verification_method": self.verification_method, "complexity": self.complexity,
            "dependencies": self.dependencies, "tags": self.tags,
        }
        if self.source_data:
            try:
                extra = json.loads(self.source_data)
                if isinstance(extra, dict):
                    data.update({k: v for k, v in extra.items() if k not in data})
            except (ValueError, TypeError):
                pass
        return data
