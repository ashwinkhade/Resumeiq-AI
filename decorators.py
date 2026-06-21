"""
Role-based access decorators built on top of flask-jwt-extended.
`admin_required` is used to lock down the Admin Dashboard endpoints.
"""
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.utils.responses import error_response


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            return error_response("Admin access required.", 403)
        return fn(*args, **kwargs)
    return wrapper
