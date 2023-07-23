from __future__ import annotations

__all__ = ("BaseError", "MissingRequiredArgument", "UnwrapError")


class BaseError(Exception):
    """The base error all unkey errors inherit from."""

    __slots__ = ()


class UnwrapError(BaseError):
    """Raised when calling unwrap or unwrap_err incorrectly."""

    __slots__ = ()

    def __init__(self, message: str) -> None:
        super().__init__(f"Unwrap failed: {message}")


class MissingRequiredArgument(BaseError):
    """Raised when a required argument is missing."""

    __slots__ = ()

    def __init__(self, message: str) -> None:
        super().__init__(f"Missing required argument: {message}")
