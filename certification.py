"""
Certification — tracks a student's certifications with a status
(completed / ongoing / pending) for the Certification Tracker module.
"""
from datetime import datetime, timezone, date
from app.extensions import db

CERT_STATUSES = ("completed", "ongoing", "pending")


class Certification(db.Model):
    __tablename__ = "certifications"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False
    )
    name = db.Column(db.String(150), nullable=False)
    issuer = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="pending")
    progress_percent = db.Column(db.Integer, nullable=False, default=0)  # 0-100
    issue_date = db.Column(db.Date, nullable=True)
    credential_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "issuer": self.issuer,
            "status": self.status,
            "progress_percent": self.progress_percent,
            "issue_date": self.issue_date.isoformat() if self.issue_date else None,
            "credential_url": self.credential_url,
        }
