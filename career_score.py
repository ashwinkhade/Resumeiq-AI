"""
CareerScore — a stored snapshot of a computed Career Readiness Score.
Each time the score is recalculated, a new row is written, so the
dashboard can show progress over time as well as the current value.
"""
from datetime import datetime, timezone
from app.extensions import db


class CareerScore(db.Model):
    __tablename__ = "career_scores"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False
    )

    total_score = db.Column(db.Float, nullable=False)  # 0-100
    skills_score = db.Column(db.Float, nullable=False)
    projects_score = db.Column(db.Float, nullable=False)
    certifications_score = db.Column(db.Float, nullable=False)
    internships_score = db.Column(db.Float, nullable=False)
    cgpa_score = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(30), nullable=False)  # Beginner | Intermediate | Placement Ready
    computed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "total_score": round(self.total_score, 2),
            "breakdown": {
                "skills": round(self.skills_score, 2),
                "projects": round(self.projects_score, 2),
                "certifications": round(self.certifications_score, 2),
                "internships": round(self.internships_score, 2),
                "cgpa": round(self.cgpa_score, 2),
            },
            "status": self.status,
            "computed_at": self.computed_at.isoformat() if self.computed_at else None,
        }
