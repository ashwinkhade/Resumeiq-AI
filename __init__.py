"""
Importing every model here ensures SQLAlchemy's metadata is fully
populated before db.create_all() / Flask-Migrate runs — and lets
other modules do `from app.models import User, StudentProfile, ...`.
"""
from app.models.user import User
from app.models.profile import StudentProfile
from app.models.skill import StudentSkill
from app.models.industry_skill import IndustrySkill
from app.models.project import Project
from app.models.certification import Certification
from app.models.internship import Internship
from app.models.career_score import CareerScore
from app.models.roadmap import Roadmap, RoadmapMilestone
from app.models.job_posting import JobPosting
from app.models.prediction import PlacementPrediction
from app.models.resume import ResumeAnalysis
from app.models.recommended_project import RecommendedProject
from app.models.github_stats import GitHubStats
from app.models.activity_log import ActivityLog

__all__ = [
    "User",
    "StudentProfile",
    "StudentSkill",
    "IndustrySkill",
    "Project",
    "Certification",
    "Internship",
    "CareerScore",
    "Roadmap",
    "RoadmapMilestone",
    "JobPosting",
    "PlacementPrediction",
    "ResumeAnalysis",
    "RecommendedProject",
    "GitHubStats",
    "ActivityLog",
]
