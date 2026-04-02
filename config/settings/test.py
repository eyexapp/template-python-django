"""Test settings — optimized for speed."""

from __future__ import annotations

from .base import *  # noqa: F403

DEBUG = False

# Fast password hashing for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# In-memory SQLite for speed
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

# Disable logging noise during tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "level": "CRITICAL",
        "handlers": ["null"],
    },
}

# Email — in-memory
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Celery — always eager in tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
