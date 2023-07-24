from __future__ import annotations

import copy

import pytest

from unkey import undefined


def test_undefined_is_falsy() -> None:
    assert not undefined.UNDEFINED


def test_any_undefined_false() -> None:
    values = {1, 2, 3}

    assert not undefined.any_undefined(*values)


def test_any_undefined_true() -> None:
    values = {1, 2, undefined.UNDEFINED}

    assert undefined.any_undefined(*values)


def test_all_undefined_false() -> None:
    values = {1, 2, undefined.UNDEFINED}

    assert not undefined.all_undefined(*values)


def test_all_undefined_true() -> None:
    values = {undefined.UNDEFINED, undefined.UNDEFINED, undefined.UNDEFINED}

    assert undefined.all_undefined(*values)


def test_instantiating_undefined_fails() -> None:
    with pytest.raises(TypeError) as e:
        _ = undefined.Undefined()

    assert e.exconly() == "TypeError: Cannot instantiate singleton class UNDEFINED."


def test_undefined_is_singleton() -> None:
    clone = copy.deepcopy(undefined.UNDEFINED)

    assert clone is undefined.UNDEFINED
