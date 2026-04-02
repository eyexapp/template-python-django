"""Custom User model — email-based authentication."""

from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """User model with email as the unique identifier instead of username."""

    username = None  # type: ignore[assignment,misc]
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = ["first_name", "last_name"]

    objects = None  # type: ignore[assignment]  # Set by managers.py import

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return self.email


# Attach the manager — avoids circular import issues
from apps.users.managers import CustomUserManager  # noqa: E402

CustomUser.objects = CustomUserManager()  # type: ignore[assignment,misc]
CustomUser.objects.auto_created = True
CustomUser.objects.model = CustomUser
