from __future__ import annotations

import attrs

from .base import BaseModel

__all__ = ("HttpResponse",)


@attrs.define(weakref_slot=False)
class HttpResponse(BaseModel):
    """Directly represents a response from the api.

    Could indicate either success or failure.
    """

    status: int
    """The HTTP status code."""

    message: str
    """The error or success message."""
