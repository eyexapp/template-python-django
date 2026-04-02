"""User business logic — service layer."""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model

User = get_user_model()


class UserService:
    """Encapsulates user-related business logic.

    Views should delegate to this service instead of calling ORM directly.
    """

    @staticmethod
    def create_user(
        email: str,
        password: str,
        **extra_fields: Any,
    ) -> Any:
        """Create a new user and trigger post-creation tasks."""
        user = User.objects.create_user(
            email=email,
            password=password,
            **extra_fields,
        )
        # Trigger async welcome email
        from apps.users.tasks import send_welcome_email

        send_welcome_email.delay(user.pk)
        return user

    @staticmethod
    def update_profile(user: Any, **data: Any) -> Any:
        """Update user profile fields."""
        for field, value in data.items():
            setattr(user, field, value)
        user.save(update_fields=list(data.keys()))
        return user
