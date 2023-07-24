from __future__ import annotations

from datetime import datetime
from unittest import mock

import pytest

from unkey import UNDEFINED
from unkey import BaseService


@pytest.fixture()
def service() -> BaseService:
    return BaseService(mock.Mock(), mock.Mock())


def test_generate_map(service: BaseService) -> None:
    result = service._generate_map(one=1, two=2)  # type: ignore

    assert result == {"one": 1, "two": 2}


def test_generate_map_with_undefined(service: BaseService) -> None:
    result = service._generate_map(one=1, two=UNDEFINED)  # type: ignore

    assert result == {"one": 1}


def test_generate_map_with_none(service: BaseService) -> None:
    result = service._generate_map(one=1, two=None)  # type: ignore

    assert result == {"one": 1, "two": None}


def test_expires_in_returns_undefined(service: BaseService) -> None:
    result = service._expires_in()  # type: ignore

    assert result is UNDEFINED


@mock.patch("unkey.services.base.datetime", wraps=datetime)
def test_expires_in_milliseconds(dt: mock.Mock, service: BaseService) -> None:
    dt.now = mock.Mock(return_value=datetime(2000, 1, 1, 1, 1, 1))

    result = service._expires_in(milliseconds=5000)  # type: ignore

    assert result
    assert datetime.fromtimestamp(result // 1000) == datetime(2000, 1, 1, 1, 1, 6)


@mock.patch("unkey.services.base.datetime", wraps=datetime)
def test_expires_in_seconds(dt: mock.Mock, service: BaseService) -> None:
    dt.now = mock.Mock(return_value=datetime(2000, 1, 1, 1, 1, 1))

    result = service._expires_in(seconds=3)  # type: ignore

    assert result
    assert datetime.fromtimestamp(result // 1000) == datetime(2000, 1, 1, 1, 1, 4)


@mock.patch("unkey.services.base.datetime", wraps=datetime)
def test_expires_in_minutes(dt: mock.Mock, service: BaseService) -> None:
    dt.now = mock.Mock(return_value=datetime(2000, 1, 1, 1, 1, 1))

    result = service._expires_in(minutes=2)  # type: ignore

    assert result
    assert datetime.fromtimestamp(result // 1000) == datetime(2000, 1, 1, 1, 3, 1)


@mock.patch("unkey.services.base.datetime", wraps=datetime)
def test_expires_in_days(dt: mock.Mock, service: BaseService) -> None:
    dt.now = mock.Mock(return_value=datetime(2000, 1, 1, 1, 1, 1))

    result = service._expires_in(days=6)  # type: ignore

    assert result
    assert datetime.fromtimestamp(result // 1000) == datetime(2000, 1, 7, 1, 1, 1)
