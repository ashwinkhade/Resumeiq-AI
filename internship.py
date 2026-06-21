"""
Internship — work experience entries used in the Career Readiness
Score and Placement Prediction modules.
"""
from datetime import datetime, timezone
from app.extensions import db


class Internship(db.Model):
    __tablename__ = "internships"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False
    )
    company_name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), nullable=True)
    duration_months = db.Column(db.Integer, nullable=False, default=1)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "company_name": self.company_name,
            "role": self.role,
            "duration_months": self.duration_months,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "description": self.description,
        }
