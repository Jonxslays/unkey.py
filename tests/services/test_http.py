from __future__ import annotations

import pytest

from unkey import HttpService
from unkey import constants


def test_init() -> None:
    http = HttpService("abc123", None, None)

    assert http._ok_responses == {200, 202}  # type: ignore
    assert http._api_version == "/v1"  # type: ignore
    assert http._base_url == constants.API_BASE_URL  # type: ignore
    assert http._headers == {  # type: ignore
        "Unkey-SDK": constants.USER_AGENT,
        "User-Agent": constants.USER_AGENT,
        "x-user-agent": constants.USER_AGENT,
        "Authorization": "Bearer abc123",
    }


def test_init_fails_without_token() -> None:
    with pytest.raises(ValueError) as e:
        HttpService("", None, None)

    assert e.exconly() == "ValueError: Api key must be provided."


def test_full_init() -> None:
    http = HttpService("abc123", 4, "1234")

    assert http._ok_responses == {200, 202}  # type: ignore
    assert http._api_version == "/v4"  # type: ignore
    assert http._base_url == "1234"  # type: ignore
    assert http._headers == {  # type: ignore
        "Unkey-SDK": constants.USER_AGENT,
        "User-Agent": constants.USER_AGENT,
        "x-user-agent": constants.USER_AGENT,
        "Authorization": "Bearer abc123",
    }
