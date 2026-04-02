"""Root URL configuration."""

from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request: Request) -> Response:
    """Health check endpoint — returns 200 OK."""
    return Response({"status": "ok"})


urlpatterns = [
    path("api/health/", health_check, name="health_check"),
    path("api/v1/", include("apps.users.urls")),
    path("admin/", admin.site.urls),
]
