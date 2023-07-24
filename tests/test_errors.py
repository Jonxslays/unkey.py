from __future__ import annotations

from unkey import errors


def test_base_error() -> None:
    e = errors.BaseError("test")
    assert isinstance(e, Exception)
    assert str(e) == "test"


def test_unwrap_error() -> None:
    e = errors.UnwrapError("test")
    assert isinstance(e, errors.BaseError)
    assert str(e) == "Unwrap failed: test"


def test_missing_required_argument() -> None:
    e = errors.MissingRequiredArgument("test")
    assert isinstance(e, errors.BaseError)
    assert str(e) == "Missing required argument: test"
