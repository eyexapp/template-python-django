"""Health check endpoint tests."""

from __future__ import annotations

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db()
class TestHealthCheck:
    def test_health_returns_200(self, api_client: APIClient) -> None:
        response = api_client.get("/api/health/")
        assert response.status_code == 200
        assert response.data == {"status": "ok"}  # type: ignore[union-attr]
