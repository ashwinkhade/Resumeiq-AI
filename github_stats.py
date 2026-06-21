"""
GitHubStats — cached snapshot of a student's GitHub analytics, so
we don't hit the GitHub API on every dashboard load. Refreshed on
demand via the GitHub Analytics endpoint.
"""
from datetime import datetime, timezone
from app.extensions import db


class GitHubStats(db.Model):
    __tablename__ = "github_stats"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    username = db.Column(db.String(100), nullable=False)
    public_repos = db.Column(db.Integer, default=0)
    total_stars = db.Column(db.Integer, default=0)
    total_forks = db.Column(db.Integer, default=0)
    followers = db.Column(db.Integer, default=0)
    top_languages = db.Column(db.Text, nullable=True)  # JSON dict {lang: byte_count}
    contribution_streak_estimate = db.Column(db.Integer, default=0)  # repos updated in last 90 days
    recent_repos = db.Column(db.Text, nullable=True)  # JSON list of {name, stars, language, updated_at}

    fetched_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        import json
        return {
            "username": self.username,
            "public_repos": self.public_repos,
            "total_stars": self.total_stars,
            "total_forks": self.total_forks,
            "followers": self.followers,
            "top_languages": json.loads(self.top_languages) if self.top_languages else {},
            "contribution_streak_estimate": self.contribution_streak_estimate,
            "recent_repos": json.loads(self.recent_repos) if self.recent_repos else [],
            "fetched_at": self.fetched_at.isoformat() if self.fetched_at else None,
        }
