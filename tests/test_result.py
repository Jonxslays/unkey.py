from __future__ import annotations

import pytest

from unkey import Err
from unkey import Ok
from unkey import Result
from unkey import UnwrapError


@pytest.fixture()
def mock_ok() -> Ok[str, int]:
    return Ok("OK!")


@pytest.fixture()
def mock_err() -> Err[int, str]:
    return Err("ERR!")


def test_abstract_result_fails_to_instantiate() -> None:
    with pytest.raises(TypeError) as e:
        _ = Result()  # type: ignore

    assert "Can't instantiate abstract class Result" in e.exconly()


def test_repr(mock_ok: Ok[str, int]) -> None:
    assert repr(mock_ok) == "Ok(OK!)"


def test_ok_is_ok(mock_ok: Ok[str, int]) -> None:
    assert mock_ok.is_ok == True
    assert mock_ok.unwrap() == "OK!"


def test_ok_is_err(mock_ok: Ok[str, int]) -> None:
    assert mock_ok.is_err == False
    assert mock_ok.unwrap() == "OK!"


def test_unwrap_err_fails_for_ok(mock_ok: Ok[str, int]) -> None:
    with pytest.raises(UnwrapError) as e:
        mock_ok.unwrap_err()

    assert "Called unwrap error on a non error value of type 'str'" in e.exconly()


def test_err_is_err(mock_err: Err[int, str]) -> None:
    assert mock_err.is_err == True
    assert mock_err.unwrap_err() == "ERR!"


def test_err_is_ok(mock_err: Err[int, str]) -> None:
    assert mock_err.is_ok == False
    assert mock_err.unwrap_err() == "ERR!"


def test_unwrap_fails_for_err(mock_err: Err[int, str]) -> None:
    with pytest.raises(UnwrapError) as e:
        mock_err.unwrap()

    assert "Called unwrap on an error value - ERR!" in e.exconly()
