from __future__ import annotations

import attrs

from .base import BaseModel

__all__ = ("HttpError",)


@attrs.define(weakref_slot=False)
class HttpError(BaseModel):
    """Indicates something went wrong during the request."""

    status: int
    """The HTTP status code."""

    message: str
    """The error message."""


# Not sure if we're gonna use this yet
# @attrs.define(weakref_slot=False)
# class HttpSuccess(BaseModel):
#     """Indicates a successful HTTP response."""

#     status: int
#     """The HTTP status code."""

#     message: str
#     """The success message."""
