"""CustomUser model tests."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db()
class TestCustomUser:
    def test_create_user(self) -> None:
        user = User.objects.create_user(  # type: ignore[union-attr]
            email="user@example.com",
            password="StrongPass123!",
            first_name="John",
            last_name="Doe",
        )
        assert user.email == "user@example.com"
        assert user.first_name == "John"
        assert user.check_password("StrongPass123!")
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_superuser(self) -> None:
        admin = User.objects.create_superuser(  # type: ignore[union-attr]
            email="admin@example.com",
            password="AdminPass123!",
        )
        assert admin.is_staff
        assert admin.is_superuser

    def test_email_normalization(self) -> None:
        user = User.objects.create_user(  # type: ignore[union-attr]
            email="User@EXAMPLE.com",
            password="TestPass123!",
        )
        assert user.email == "User@example.com"

    def test_str_representation(self) -> None:
        user = User.objects.create_user(  # type: ignore[union-attr]
            email="str@example.com",
            password="TestPass123!",
        )
        assert str(user) == "str@example.com"

    def test_create_user_without_email_raises(self) -> None:
        with pytest.raises(ValueError, match="Email is required"):
            User.objects.create_user(email="", password="TestPass123!")  # type: ignore[union-attr]
