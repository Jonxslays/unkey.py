from __future__ import annotations

from unittest import mock

import pytest

from unkey import BaseService
from unkey import UNDEFINED


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
