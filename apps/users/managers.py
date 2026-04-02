"""Custom user manager — email as the unique identifier."""

from __future__ import annotations

from typing import Any

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager["CustomUser"]):
    """Manager for CustomUser where email is the USERNAME_FIELD."""

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> CustomUser:
        if not email:
            msg = "Email is required"
            raise ValueError(msg)
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> CustomUser:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# Avoid circular import — type used only in type hints above
from apps.users.models import CustomUser  # noqa: E402
