"""Custom middleware."""

from __future__ import annotations

import uuid
from typing import Any

from django.http import HttpRequest, HttpResponse


class RequestIDMiddleware:
    """Add ``X-Request-ID`` header to every request/response.

    If the incoming request already has the header (e.g., from a load
    balancer), it is preserved. Otherwise a new UUID is generated.
    """

    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.META["HTTP_X_REQUEST_ID"] = request_id

        response: HttpResponse = self.get_response(request)
        response["X-Request-ID"] = request_id
        return response
