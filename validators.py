"""
Shared input validation helpers. Kept dependency-free (no marshmallow
schemas) so they're easy to read and reuse across every route module.
"""
import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    return bool(email) and bool(EMAIL_REGEX.match(email.strip()))


def is_valid_password(password: str) -> tuple[bool, str]:
    """Returns (is_valid, error_message)."""
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    return True, ""


def is_valid_cgpa(cgpa) -> bool:
    try:
        value = float(cgpa)
    except (TypeError, ValueError):
        return False
    return 0.0 <= value <= 10.0


def require_fields(data: dict, fields: list[str]) -> list[str]:
    """Returns a list of missing/empty required field names."""
    missing = []
    for field in fields:
        value = data.get(field) if isinstance(data, dict) else None
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)
    return missing
