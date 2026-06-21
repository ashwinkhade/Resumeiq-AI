"""
Configuration classes for the Career Tracker backend.

Uses environment variables where available, with sensible
development defaults. The SQLALCHEMY_DATABASE_URI is written so
that swapping SQLite for PostgreSQL only requires setting
DATABASE_URL — no code changes needed elsewhere.
"""
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_ERROR_MESSAGE_KEY = "message"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "resumes")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload
    ALLOWED_RESUME_EXTENSIONS = {"pdf", "docx"}

    CORS_ORIGINS = os.environ.get(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
    ).split(",")

    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_DEFAULT = "1000 per hour"

    GITHUB_API_BASE = "https://api.github.com"
    GITHUB_DEFAULT_TOKEN = os.environ.get("GITHUB_TOKEN", "")

    ML_MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "placement_model.joblib")
    ML_ENCODER_PATH = os.path.join(BASE_DIR, "ml_models", "skill_encoder.joblib")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'career_tracker.db')}"
    )


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'career_tracker.db')}"
    )
    # Render/Heroku-style URLs sometimes use the legacy postgres:// scheme.
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
