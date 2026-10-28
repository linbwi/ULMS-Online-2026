"""
Application configuration for ULMS Online.
"""

import os
from datetime import timedelta


class Config:
    """Base configuration for the ULMS Flask application."""

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "ulms-demo-secret-key-2026-change-in-production",
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///ulms.db",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PERMANENT_SESSION_LIFETIME = timedelta(
        minutes=int(
            os.environ.get("SESSION_TIMEOUT_MINUTES", "30")
        )
    )

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = os.environ.get(
        "SESSION_COOKIE_SECURE", "false"
    ).lower() in {"1", "true", "yes"}


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}