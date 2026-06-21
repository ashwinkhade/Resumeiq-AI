"""
PlacementPrediction — stores the output of the Random Forest
placement prediction model each time it's run for a student, so
the history is auditable and the latest result can be fetched fast.
"""
from datetime import datetime, timezone
from app.extensions import db


class PlacementPrediction(db.Model):
    __tablename__ = "placement_predictions"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False
    )

    placement_probability = db.Column(db.Float, nullable=False)  # 0-1
    strengths = db.Column(db.Text, nullable=True)  # JSON-encoded list
    weaknesses = db.Column(db.Text, nullable=True)  # JSON-encoded list
    suggestions = db.Column(db.Text, nullable=True)  # JSON-encoded list

    model_version = db.Column(db.String(40), nullable=False, default="rf_v1")
    predicted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        import json
        return {
            "id": self.id,
            "placement_probability": round(self.placement_probability, 4),
            "placement_percent": round(self.placement_probability * 100, 1),
            "strengths": json.loads(self.strengths) if self.strengths else [],
            "weaknesses": json.loads(self.weaknesses) if self.weaknesses else [],
            "suggestions": json.loads(self.suggestions) if self.suggestions else [],
            "model_version": self.model_version,
            "predicted_at": self.predicted_at.isoformat() if self.predicted_at else None,
        }
