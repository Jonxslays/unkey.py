from __future__ import annotations

import pytest

from unkey import models


def test_from_str() -> None:
    ratelimit = models.RatelimitType.from_str("fast")
    assert ratelimit is models.RatelimitType.Fast
    assert ratelimit.value == "fast"


def test_from_str_none() -> None:
    with pytest.raises(ValueError) as e:
        _ = models.ErrorCode.from_str(None)  # type: ignore

    assert e.exconly().startswith("ValueError: None is not a valid ErrorCode variant.")


def test_from_str_invalid() -> None:
    with pytest.raises(ValueError) as e:
        _ = models.ErrorCode.from_str("fake")  # type: ignore

    assert e.exconly().startswith("ValueError: 'fake' is not a valid ErrorCode variant.")


def test_from_str_maybe() -> None:
    code = models.ErrorCode.from_str_maybe("UNAUTHORIZED")
    assert code is models.ErrorCode.Unauthorized
    assert code.value == "UNAUTHORIZED"


def test_from_str_maybe_invalid() -> None:
    period = models.RatelimitType.from_str_maybe("lol")
    assert period is None


def test_from_str_maybe_none() -> None:
    period = models.RatelimitType.from_str_maybe(None)  # type: ignore
    assert period is None


def test_str() -> None:
    period = models.RatelimitType.Consistent
    assert str(period) == "consistent"
