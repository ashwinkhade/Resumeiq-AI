"""
StudentSkill — join-style table linking a student to a skill name
with a proficiency level. Kept as free-text skill names (normalized
to lowercase for matching) rather than a strict FK to a master skill
table, so students can log skills outside the curated industry list
while skill-gap analysis still matches against the curated list.
"""
from datetime import datetime, timezone
from app.extensions import db

PROFICIENCY_LEVELS = ("beginner", "intermediate", "advanced")


class StudentSkill(db.Model):
    __tablename__ = "student_skills"
    __table_args__ = (
        db.UniqueConstraint("profile_id", "skill_name", name="uq_profile_skill"),
    )

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False
    )
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency = db.Column(db.String(20), nullable=False, default="beginner")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "skill_name": self.skill_name,
            "proficiency": self.proficiency,
        }
