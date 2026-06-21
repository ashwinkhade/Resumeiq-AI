"""
ResumeAnalysis — stores the result of parsing an uploaded resume
(PDF/DOCX), including extracted skills/education/projects/certs
and a comparison against the industry skill list.
"""
from datetime import datetime, timezone
from app.extensions import db


class ResumeAnalysis(db.Model):
    __tablename__ = "resume_analyses"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False
    )

    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # pdf | docx

    extracted_skills = db.Column(db.Text, nullable=True)  # JSON list
    extracted_education = db.Column(db.Text, nullable=True)  # JSON list
    extracted_projects = db.Column(db.Text, nullable=True)  # JSON list
    extracted_certifications = db.Column(db.Text, nullable=True)  # JSON list
    matched_industry_skills = db.Column(db.Text, nullable=True)  # JSON list
    missing_industry_skills = db.Column(db.Text, nullable=True)  # JSON list
    match_score = db.Column(db.Float, nullable=True)  # 0-100

    raw_text_excerpt = db.Column(db.Text, nullable=True)  # first ~2000 chars, for debugging
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        import json
        return {
            "id": self.id,
            "original_filename": self.original_filename,
            "file_type": self.file_type,
            "extracted_skills": json.loads(self.extracted_skills) if self.extracted_skills else [],
            "extracted_education": json.loads(self.extracted_education) if self.extracted_education else [],
            "extracted_projects": json.loads(self.extracted_projects) if self.extracted_projects else [],
            "extracted_certifications": json.loads(self.extracted_certifications) if self.extracted_certifications else [],
            "matched_industry_skills": json.loads(self.matched_industry_skills) if self.matched_industry_skills else [],
            "missing_industry_skills": json.loads(self.missing_industry_skills) if self.missing_industry_skills else [],
            "match_score": self.match_score,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
        }
