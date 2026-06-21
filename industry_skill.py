"""
IndustrySkill — the curated master list of skills the platform
checks students against for Skill Gap Analysis. Managed via the
Admin Dashboard (CRUD), seeded with a baseline AI/DS/ML list.
"""
from app.extensions import db


class IndustrySkill(db.Model):
    __tablename__ = "industry_skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False, default="general")
    # category examples: programming, data, ml, visualization, tools
    importance_weight = db.Column(db.Float, nullable=False, default=1.0)
    description = db.Column(db.String(255), nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "importance_weight": self.importance_weight,
            "description": self.description,
        }
