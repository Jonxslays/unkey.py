from __future__ import annotations

__all__ = ("UnwrapError", "BaseError")


class BaseError(Exception):
    """The base error all wom errors inherit from."""

    __slots__ = ()


class UnwrapError(BaseError):
    """Raised when calling unwrap or unwrap_err incorrectly.

    message: The error message.
    """

    __slots__ = ()

    def __init__(self, message: str) -> None:
        super().__init__(f"Unwrap failed: {message}")
