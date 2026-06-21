"""
Project — a student's portfolio project entry, used by the Career
Readiness Score and as the basis for project recommendations.
"""
from datetime import datetime, timezone
from app.extensions import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False
    )
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    tech_stack = db.Column(db.String(255), nullable=True)  # comma-separated
    project_url = db.Column(db.String(255), nullable=True)
    github_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "tech_stack": [t.strip() for t in self.tech_stack.split(",")] if self.tech_stack else [],
            "project_url": self.project_url,
            "github_url": self.github_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
