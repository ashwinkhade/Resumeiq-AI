"""
StudentProfile — the core dashboard data for each user.
One-to-one with User. Skills/Projects/Certifications/Internships
are separate tables (one-to-many) so they can be added, edited,
and queried independently.
"""
from datetime import datetime, timezone
from app.extensions import db


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    full_name = db.Column(db.String(150), nullable=False)
    branch = db.Column(db.String(100), nullable=True)
    academic_year = db.Column(db.String(20), nullable=True)  # e.g. "3rd Year"
    cgpa = db.Column(db.Float, nullable=True)  # 0.0 - 10.0

    linkedin_url = db.Column(db.String(255), nullable=True)
    github_username = db.Column(db.String(100), nullable=True)
    leetcode_username = db.Column(db.String(100), nullable=True)
    codeforces_username = db.Column(db.String(100), nullable=True)
    hackerrank_username = db.Column(db.String(100), nullable=True)

    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    skills = db.relationship(
        "StudentSkill", backref="profile", cascade="all, delete-orphan", passive_deletes=True
    )
    projects = db.relationship(
        "Project", backref="profile", cascade="all, delete-orphan", passive_deletes=True
    )
    certifications = db.relationship(
        "Certification", backref="profile", cascade="all, delete-orphan", passive_deletes=True
    )
    internships = db.relationship(
        "Internship", backref="profile", cascade="all, delete-orphan", passive_deletes=True
    )

    def to_dict(self, include_children: bool = True) -> dict:
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "branch": self.branch,
            "academic_year": self.academic_year,
            "cgpa": self.cgpa,
            "linkedin_url": self.linkedin_url,
            "github_username": self.github_username,
            "leetcode_username": self.leetcode_username,
            "codeforces_username": self.codeforces_username,
            "hackerrank_username": self.hackerrank_username,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_children:
            data["skills"] = [s.to_dict() for s in self.skills]
            data["projects"] = [p.to_dict() for p in self.projects]
            data["certifications"] = [c.to_dict() for c in self.certifications]
            data["internships"] = [i.to_dict() for i in self.internships]
        return data
