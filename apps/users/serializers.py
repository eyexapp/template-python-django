"""User serializers for DRF."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    """Serialize registration data — email + password + name."""

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

    def create(self, validated_data: dict) -> object:  # type: ignore[type-arg]
        from apps.users.services import UserService

        return UserService.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    """Serialize user profile — read/update."""

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "date_joined")
        read_only_fields = ("id", "email", "date_joined")


class ChangePasswordSerializer(serializers.Serializer):
    """Serialize password change request."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
    )
