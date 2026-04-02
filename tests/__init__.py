"""Shared test fixtures."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture()
def api_client() -> APIClient:
    """Unauthenticated DRF test client."""
    return APIClient()


@pytest.fixture()
def user(db: None) -> object:
    """Create a regular test user."""
    return User.objects.create_user(  # type: ignore[union-attr]
        email="test@example.com",
        password="TestPass123!",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture()
def authenticated_client(api_client: APIClient, user: object) -> APIClient:
    """DRF client authenticated via JWT."""
    response = api_client.post(
        "/api/v1/auth/token/",
        {"email": "test@example.com", "password": "TestPass123!"},
        format="json",
    )
    token = response.data["access"]  # type: ignore[index]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client
