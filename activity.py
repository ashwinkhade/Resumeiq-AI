"""
Helper to write an ActivityLog row without every route needing to
import the model and handle commit/rollback boilerplate itself.
"""
from flask import request
from app.extensions import db
from app.models.activity_log import ActivityLog


def log_activity(user_id, action: str, details: str = None) -> None:
    try:
        entry = ActivityLog(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=request.remote_addr if request else None,
        )
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()
