"""
Standard JSON response helpers, so every endpoint returns the same
envelope shape: { "success": bool, "data": ..., "message": ... }.
Makes the frontend's API client simple and predictable.
"""
from flask import jsonify


def success_response(data=None, message: str = "", status_code: int = 200):
    payload = {"success": True, "message": message, "data": data}
    return jsonify(payload), status_code


def error_response(message: str, status_code: int = 400, errors=None):
    payload = {"success": False, "message": message}
    if errors is not None:
        payload["errors"] = errors
    return jsonify(payload), status_code
