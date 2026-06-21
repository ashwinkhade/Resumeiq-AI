"""
JobPosting — rows from the job market dataset used to power the
Job Market Analytics module (trending skills, salary distribution,
role distribution, experience requirements). Loaded from a CSV seed
file but also manageable via the Admin Dashboard.
"""
from datetime import datetime, timezone
from app.extensions import db


class JobPosting(db.Model):
    __tablename__ = "job_postings"

    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(150), nullable=False, index=True)
    company = db.Column(db.String(150), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    role_category = db.Column(db.String(80), nullable=False, index=True)
    # e.g. Data Scientist, ML Engineer, Data Analyst, Software Engineer, AI Engineer

    required_skills = db.Column(db.Text, nullable=False)  # comma-separated
    min_experience_years = db.Column(db.Float, nullable=False, default=0)
    max_experience_years = db.Column(db.Float, nullable=False, default=0)

    min_salary_lpa = db.Column(db.Float, nullable=True)  # lakhs per annum
    max_salary_lpa = db.Column(db.Float, nullable=True)

    posted_date = db.Column(db.Date, nullable=True)
    source = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def skills_list(self):
        return [s.strip() for s in self.required_skills.split(",") if s.strip()]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "job_title": self.job_title,
            "company": self.company,
            "location": self.location,
            "role_category": self.role_category,
            "required_skills": self.skills_list(),
            "min_experience_years": self.min_experience_years,
            "max_experience_years": self.max_experience_years,
            "min_salary_lpa": self.min_salary_lpa,
            "max_salary_lpa": self.max_salary_lpa,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "source": self.source,
        }
