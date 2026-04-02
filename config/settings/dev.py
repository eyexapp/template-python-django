"""Development settings."""

from __future__ import annotations

from .base import *  # noqa: F403
from .base import env

DEBUG = True

ALLOWED_HOSTS = ["*"]

# CORS — allow all in development
CORS_ALLOW_ALL_ORIGINS = True

# Database — SQLite fallback for zero-setup local dev
DATABASES = {
    "default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3"),
}

# Email — print to console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# DRF — add browsable API in dev
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # type: ignore[name-defined]  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]
