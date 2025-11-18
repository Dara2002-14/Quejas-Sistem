from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="user", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # RELACIONES CORREGIDAS
    complaints = db.relationship(
        'Complaint',
        foreign_keys='Complaint.user_id',
        backref='owner',
        lazy=True
    )

    assigned_complaints = db.relationship(
        'Complaint',
        foreign_keys='Complaint.assigned_to',
        backref='assigned_user',
        lazy=True
    )

    actions = db.relationship(
        'ComplaintTracker',
        backref='actor',
        lazy=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat()
        }


class Complaint(db.Model):
    __tablename__ = "complaints"
    id = db.Column(db.Integer, primary_key=True)
    complaint_number = db.Column(db.String(32), unique=True, nullable=False, index=True)

    # DOS FOREIGN KEYS -> RELACIONES ESPECIFICADAS ARRIBA
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="pendiente", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tracker = db.relationship(
        'ComplaintTracker',
        backref='complaint',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def to_dict(self, include_tracker=True):
        data = {
            "id": self.id,
            "complaint_number": self.complaint_number,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at.isoformat(),
            "owner": self.owner.username if self.owner else None,
            "assigned_user": self.assigned_user.username if self.assigned_user else None,
        }
        if include_tracker:
            data["tracker"] = [t.to_dict() for t in self.tracker]
        return data


class ComplaintTracker(db.Model):
    __tablename__ = "complaint_tracker"
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "complaint_id": self.complaint_id,
            "actor_id": self.actor_id,
            "action": self.action,
            "note": self.note,
            "timestamp": self.timestamp.isoformat()
        }
