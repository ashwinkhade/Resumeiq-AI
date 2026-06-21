"""
RecommendedProject — master catalog of project ideas, tagged by the
skills they exercise and a difficulty level, used by the Project
Recommendation Engine to suggest projects matching a student's
current skill set (and nudging toward adjacent skills).
"""
from app.extensions import db

DIFFICULTY_LEVELS = ("beginner", "intermediate", "advanced")


class RecommendedProject(db.Model):
    __tablename__ = "recommended_projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.String(255), nullable=False)  # comma-separated
    difficulty = db.Column(db.String(20), nullable=False, default="beginner")
    estimated_hours = db.Column(db.Integer, nullable=True)
    category = db.Column(db.String(60), nullable=True)  # e.g. "Machine Learning", "Data Viz"

    def skills_list(self):
        return [s.strip().lower() for s in self.required_skills.split(",") if s.strip()]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "required_skills": [s.strip() for s in self.required_skills.split(",")],
            "difficulty": self.difficulty,
            "estimated_hours": self.estimated_hours,
            "category": self.category,
        }
