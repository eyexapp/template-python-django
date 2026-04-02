"""User API views."""

from __future__ import annotations

from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.serializers import (
    ChangePasswordSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterView(generics.CreateAPIView):
    """Register a new user — POST /api/v1/auth/register/."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """User profile CRUD.

    - ``GET /api/v1/users/me/`` — retrieve own profile
    - ``PATCH /api/v1/users/me/`` — update own profile
    - ``POST /api/v1/users/me/change-password/`` — change password
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> object:
        return self.request.user

    @action(detail=False, methods=["get", "patch"], url_path="me")
    def me(self, request: Request) -> Response:
        if request.method == "PATCH":
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="me/change-password")
    def change_password(self, request: Request) -> Response:
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"error": {"code": "invalid_password", "message": "Wrong password."}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"message": "Password updated."})
