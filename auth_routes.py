"""
Authentication routes.

POST /api/auth/register   - create a user account (+ empty profile)
POST /api/auth/login      - verify credentials, issue JWT access+refresh tokens
POST /api/auth/refresh    - exchange a valid refresh token for a new access token
POST /api/auth/logout     - client-side token discard endpoint (logged server-side)
GET  /api/auth/me         - return the current authenticated user + profile
PUT  /api/auth/password   - change password (requires current password)
"""
from datetime import datetime, timezone

from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from app.extensions import db, limiter
from app.models.user import User
from app.models.profile import StudentProfile
from app.utils.validators import is_valid_email, is_valid_password, require_fields
from app.utils.responses import success_response, error_response
from app.utils.activity import log_activity

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("20 per hour")
def register():
    data = request.get_json(silent=True) or {}

    missing = require_fields(data, ["email", "password", "full_name"])
    if missing:
        return error_response(f"Missing required fields: {', '.join(missing)}", 422)

    email = data["email"].strip().lower()
    password = data["password"]
    full_name = data["full_name"].strip()

    if not is_valid_email(email):
        return error_response("Please provide a valid email address.", 422)

    valid_pw, pw_error = is_valid_password(password)
    if not valid_pw:
        return error_response(pw_error, 422)

    if User.query.filter_by(email=email).first():
        return error_response("An account with this email already exists.", 409)

    user = User(email=email, role="student")
    user.set_password(password)
    db.session.add(user)
    db.session.flush()  # get user.id before commit

    profile = StudentProfile(user_id=user.id, full_name=full_name)
    db.session.add(profile)
    db.session.commit()

    log_activity(user.id, "register", f"New account: {email}")

    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims={"role": user.role})

    return success_response(
        data={
            "user": user.to_dict(include_profile=True),
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        message="Account created successfully.",
        status_code=201,
    )


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("30 per hour")
def login():
    data = request.get_json(silent=True) or {}

    missing = require_fields(data, ["email", "password"])
    if missing:
        return error_response(f"Missing required fields: {', '.join(missing)}", 422)

    email = data["email"].strip().lower()
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return error_response("Invalid email or password.", 401)

    if not user.is_active:
        return error_response("This account has been deactivated.", 403)

    user.last_login_at = datetime.now(timezone.utc)
    db.session.commit()

    log_activity(user.id, "login", f"User logged in: {email}")

    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims={"role": user.role})

    return success_response(
        data={
            "user": user.to_dict(include_profile=True),
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        message="Login successful.",
    )


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    claims = get_jwt()
    new_access_token = create_access_token(
        identity=identity, additional_claims={"role": claims.get("role", "student")}
    )
    return success_response(data={"access_token": new_access_token}, message="Token refreshed.")


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    log_activity(user_id, "logout", "User logged out")
    # Stateless JWT: actual invalidation happens client-side by discarding
    # the tokens. A token-blocklist (e.g. Redis) can be added here later
    # for true server-side revocation if needed.
    return success_response(message="Logged out successfully.")


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if not user:
        return error_response("User not found.", 404)
    return success_response(data=user.to_dict(include_profile=True))


@auth_bp.route("/password", methods=["PUT"])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if not user:
        return error_response("User not found.", 404)

    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["current_password", "new_password"])
    if missing:
        return error_response(f"Missing required fields: {', '.join(missing)}", 422)

    if not user.check_password(data["current_password"]):
        return error_response("Current password is incorrect.", 401)

    valid_pw, pw_error = is_valid_password(data["new_password"])
    if not valid_pw:
        return error_response(pw_error, 422)

    user.set_password(data["new_password"])
    db.session.commit()
    log_activity(user.id, "password_change", "Password updated")

    return success_response(message="Password updated successfully.")
