"""Custom DRF exception handler for consistent error responses."""

from __future__ import annotations

from typing import Any

from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(
    exc: Exception,
    context: dict[str, Any],
) -> Response | None:
    """Return errors in a consistent format.

    Response shape::

        {
            "error": {
                "code": "validation_error",
                "message": "Invalid input.",
                "details": { ... }
            }
        }
    """
    response = exception_handler(exc, context)
    if response is None:
        return None

    error_code = exc.__class__.__name__
    message: Any
    details: Any

    if isinstance(response.data, list):
        message = response.data[0] if response.data else str(exc)
        details = response.data
    elif isinstance(response.data, dict):
        message = response.data.get("detail", str(exc))
        details = {k: v for k, v in response.data.items() if k != "detail"}
    else:
        message = str(exc)
        details = None

    response.data = {
        "error": {
            "code": error_code,
            "message": str(message),
            "details": details or None,
        },
    }
    return response
