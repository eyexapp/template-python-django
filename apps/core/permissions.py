"""Custom DRF permissions."""

from __future__ import annotations

from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwner(BasePermission):
    """Allow access only to the object's owner.

    Expects the object to have an ``owner`` attribute pointing to a User.
    """

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Any,
    ) -> bool:
        return bool(hasattr(obj, "owner") and obj.owner == request.user)
