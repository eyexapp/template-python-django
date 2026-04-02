"""User API endpoint tests."""

from __future__ import annotations

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db()
class TestRegister:
    def test_register_success(self, api_client: APIClient) -> None:
        response = api_client.post(
            "/api/v1/auth/register/",
            {
                "email": "new@example.com",
                "password": "NewPass123!",
                "first_name": "New",
                "last_name": "User",
            },
            format="json",
        )
        assert response.status_code == 201
        assert response.data["email"] == "new@example.com"  # type: ignore[index]

    def test_register_duplicate_email(
        self, api_client: APIClient, user: object
    ) -> None:
        response = api_client.post(
            "/api/v1/auth/register/",
            {
                "email": "test@example.com",
                "password": "AnotherPass123!",
                "first_name": "Dup",
                "last_name": "User",
            },
            format="json",
        )
        assert response.status_code == 400


@pytest.mark.django_db()
class TestAuth:
    def test_obtain_token(self, api_client: APIClient, user: object) -> None:
        response = api_client.post(
            "/api/v1/auth/token/",
            {"email": "test@example.com", "password": "TestPass123!"},
            format="json",
        )
        assert response.status_code == 200
        assert "access" in response.data  # type: ignore[operator]
        assert "refresh" in response.data  # type: ignore[operator]

    def test_token_refresh(self, api_client: APIClient, user: object) -> None:
        token_response = api_client.post(
            "/api/v1/auth/token/",
            {"email": "test@example.com", "password": "TestPass123!"},
            format="json",
        )
        refresh_token = token_response.data["refresh"]  # type: ignore[index]
        response = api_client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": refresh_token},
            format="json",
        )
        assert response.status_code == 200
        assert "access" in response.data  # type: ignore[operator]

    def test_invalid_credentials(self, api_client: APIClient, user: object) -> None:
        response = api_client.post(
            "/api/v1/auth/token/",
            {"email": "test@example.com", "password": "WrongPass"},
            format="json",
        )
        assert response.status_code == 401


@pytest.mark.django_db()
class TestUserProfile:
    def test_get_profile(self, authenticated_client: APIClient) -> None:
        response = authenticated_client.get("/api/v1/users/me/")
        assert response.status_code == 200
        assert response.data["email"] == "test@example.com"  # type: ignore[index]

    def test_update_profile(self, authenticated_client: APIClient) -> None:
        response = authenticated_client.patch(
            "/api/v1/users/me/",
            {"first_name": "Updated"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["first_name"] == "Updated"  # type: ignore[index]

    def test_unauthenticated_profile(self, api_client: APIClient) -> None:
        response = api_client.get("/api/v1/users/me/")
        assert response.status_code == 401

    def test_change_password(self, authenticated_client: APIClient) -> None:
        response = authenticated_client.post(
            "/api/v1/users/me/change-password/",
            {"old_password": "TestPass123!", "new_password": "NewSecure456!"},
            format="json",
        )
        assert response.status_code == 200

    def test_change_password_wrong_old(self, authenticated_client: APIClient) -> None:
        response = authenticated_client.post(
            "/api/v1/users/me/change-password/",
            {"old_password": "WrongOld!", "new_password": "NewSecure456!"},
            format="json",
        )
        assert response.status_code == 400
