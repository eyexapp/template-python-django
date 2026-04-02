"""Config package — ensures Celery app is loaded on Django startup."""

from __future__ import annotations

from config.celery import app as celery_app

__all__ = ["celery_app"]
