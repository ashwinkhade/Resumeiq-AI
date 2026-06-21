"""
Roadmap / RoadmapMilestone — a generated 6-month learning plan built
from a student's missing skills. A Roadmap has many ordered
RoadmapMilestones, each trackable as not_started/in_progress/done.
"""
from datetime import datetime, timezone
from app.extensions import db

MILESTONE_STATUSES = ("not_started", "in_progress", "completed")


class Roadmap(db.Model):
    __tablename__ = "roadmaps"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False
    )
    title = db.Column(db.String(150), nullable=False, default="6-Month Learning Roadmap")
    generated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    milestones = db.relationship(
        "RoadmapMilestone",
        backref="roadmap",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="RoadmapMilestone.month_number, RoadmapMilestone.order_index",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "is_active": self.is_active,
            "milestones": [m.to_dict() for m in self.milestones],
            "progress_percent": self._progress_percent(),
        }

    def _progress_percent(self) -> int:
        if not self.milestones:
            return 0
        done = sum(1 for m in self.milestones if m.status == "completed")
        return round((done / len(self.milestones)) * 100)


class RoadmapMilestone(db.Model):
    __tablename__ = "roadmap_milestones"

    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(
        db.Integer, db.ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False
    )
    month_number = db.Column(db.Integer, nullable=False)  # 1-6
    order_index = db.Column(db.Integer, nullable=False, default=0)
    skill_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    resource_links = db.Column(db.Text, nullable=True)  # comma-separated URLs
    status = db.Column(db.String(20), nullable=False, default="not_started")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "month_number": self.month_number,
            "skill_name": self.skill_name,
            "title": self.title,
            "description": self.description,
            "resource_links": [l.strip() for l in self.resource_links.split(",")] if self.resource_links else [],
            "status": self.status,
        }
