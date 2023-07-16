from __future__ import annotations

import typing as t

import attrs

from .base import BaseEnum
from .base import BaseModel

__all__ = ("ErrorCode", "HttpResponse")


class ErrorCode(BaseEnum):
    NotFound = "NOT_FOUND"
    BadRequest = "BAD_REQUEST"
    Unauthorized = "UNAUTHORIZED"
    InternalServerError = "INTERNAL_SERVER_ERROR"
    Ratelimited = "RATELIMITED"
    Forbidden = "FORBIDDEN"
    UsageExceeded = "USAGE_EXCEEDED"
    Unknown = "UNKNOWN"


@attrs.define(weakref_slot=False)
class HttpResponse(BaseModel):
    """Directly represents a response from the api.

    Could indicate either success or failure.
    """

    status: int
    """The HTTP status code."""

    message: str
    """The error or success message."""

    code: t.Optional[ErrorCode] = None
    """The optional error code returned by the unkey api."""
