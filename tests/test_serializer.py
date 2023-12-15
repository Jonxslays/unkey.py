from __future__ import annotations

import typing as t
from datetime import datetime
from unittest import mock

import pytest

from unkey import Serializer
from unkey import models

DictT = t.Dict[str, t.Any]

serializer = Serializer()


@pytest.fixture()
def blank_class() -> t.Any:
    class BlankClass:
        ...

    return BlankClass


def test_dt_from_iso() -> None:
    iso_string = "2023-03-17T17:56:31.436179"

    expected = datetime(2023, 3, 17, 17, 56, 31, 436179)
    result = serializer._dt_from_iso(iso_string)  # type: ignore
    assert expected == result


def test_dt_from_iso_with_z() -> None:
    iso_string = "2023-03-17T17:56:31.436179Z"

    expected = datetime(2023, 3, 17, 17, 56, 31, 436179)
    result = serializer._dt_from_iso(iso_string)  # type: ignore
    assert expected == result


def test_dt_from_iso_maybe() -> None:
    iso_string = "2023-03-17T17:56:31.436179"

    expected = datetime(2023, 3, 17, 17, 56, 31, 436179)
    result = serializer._dt_from_iso_maybe(iso_string)  # type: ignore
    assert result == expected


def test_dt_from_iso_maybe_with_z() -> None:
    iso_string = "2023-03-17T17:56:31.436179Z"

    expected = datetime(2023, 3, 17, 17, 56, 31, 436179)
    result = serializer._dt_from_iso_maybe(iso_string)  # type: ignore
    assert result == expected


def test_dt_from_iso_maybe_none() -> None:
    result = serializer._dt_from_iso_maybe(None)  # type: ignore
    assert result == None


def test_to_camel_case() -> None:
    result = serializer.to_camel_case("test")  # type: ignore
    assert result == "test"


def test_to_camel_case_with_casing() -> None:
    result = serializer.to_camel_case("test_what_im_doing")  # type: ignore
    assert result == "testWhatImDoing"


def test_set_attrs() -> None:
    model: t.Any = mock.Mock()
    data = {"one": 1, "two": 2}

    serializer._set_attrs(model, data, "one", "two")  # type: ignore

    assert model.one == 1
    assert model.two == 2


def test_set_attrs_with_camel_case() -> None:
    model: t.Any = mock.Mock()
    data = {"one": 1, "twoThree": 2}

    serializer._set_attrs(model, data, "one", "two_three", camel_case=True)  # type: ignore

    assert model.one == 1
    assert model.two_three == 2


def test_set_attrs_maybe_transform_fails() -> None:
    with pytest.raises(RuntimeError) as e:
        serializer._set_attrs(  # type: ignore
            mock.Mock(), mock.Mock(), maybe=True, transform=lambda: None  # type: ignore
        )

    assert e.exconly() == "RuntimeError: Only one of 'maybe' and 'transform' may be used."


def test_set_attrs_with_transform() -> None:
    model: t.Any = mock.Mock()
    data = {"one": 1, "two": 2}

    serializer._set_attrs(model, data, "one", "two", transform=lambda i: i * 2)  # type: ignore

    assert model.one == 2
    assert model.two == 4


@mock.patch("unkey.serializer.Serializer._set_attrs")
def test_set_attrs_cased(set_attrs: mock.Mock) -> None:
    model = object()
    data = {}
    attrs = {"one", "two"}
    transform = lambda: None
    maybe = False

    serializer._set_attrs_cased(  # type: ignore
        model, data, *attrs, transform=transform, maybe=maybe  # type: ignore
    )

    set_attrs.assert_called_once_with(
        model, data, *attrs, transform=transform, camel_case=True, maybe=maybe
    )


########
# to_api
########


def _raw_api() -> DictT:
    return {"id": "api_123", "name": "Amazing API", "workspaceId": "ws_777"}


@pytest.fixture()
def raw_api() -> DictT:
    return _raw_api()


def _full_api() -> models.Api:
    model = models.Api()
    model.id = "api_123"
    model.name = "Amazing API"
    model.workspace_id = "ws_777"
    return model


@pytest.fixture()
def full_api() -> models.Api:
    return _full_api()


def test_to_api(
    raw_api: DictT,
    full_api: models.ApiKeyVerification,
) -> None:
    result = serializer.to_api(raw_api)

    assert result == full_api


############
# to_api_key
############


def _raw_api_key() -> DictT:
    return {"key": "prefix_lolol", "keyId": "key_master"}


@pytest.fixture()
def raw_api_key() -> DictT:
    return _raw_api_key()


def _full_api_key() -> models.ApiKey:
    model = models.ApiKey()
    model.key = "prefix_lolol"
    model.key_id = "key_master"
    return model


@pytest.fixture()
def full_api_key() -> models.ApiKey:
    return _full_api_key()


def test_to_api_key(
    raw_api_key: DictT,
    full_api_key: models.ApiKey,
) -> None:
    result = serializer.to_api_key(raw_api_key)

    assert result == full_api_key


####################
# to_ratelimit_state
####################


def _raw_ratelimit_state() -> DictT:
    return {
        "limit": 100,
        "remaining": 90,
        "reset": 123,
    }


@pytest.fixture()
def raw_ratelimit_state() -> DictT:
    return _raw_ratelimit_state()


def _full_ratelimit_state() -> models.RatelimitState:
    model = models.RatelimitState()
    model.limit = 100
    model.remaining = 90
    model.reset = 123
    return model


@pytest.fixture()
def full_ratelimit_state() -> models.RatelimitState:
    return _full_ratelimit_state()


def test_to_ratelimit_state(
    raw_ratelimit_state: DictT,
    full_ratelimit_state: models.RatelimitState,
) -> None:
    result = serializer.to_ratelimit_state(raw_ratelimit_state)

    assert result == full_ratelimit_state


#########################
# to_api_key_verification
#########################


def _raw_api_key_verification() -> DictT:
    return {
        "valid": False,
        "owner_id": None,
        "meta": None,
        "remaining": None,
        "ratelimit": _raw_ratelimit_state(),
        "expires": 12345,
        "error": "some error",
        "code": "NOT_FOUND",
    }


@pytest.fixture()
def raw_api_key_verification() -> DictT:
    return _raw_api_key_verification()


def _full_api_key_verification() -> models.ApiKeyVerification:
    model = models.ApiKeyVerification()
    model.valid = False
    model.owner_id = None
    model.meta = None
    model.remaining = None
    model.ratelimit = _full_ratelimit_state()
    model.expires = 12345
    model.error = "some error"
    model.code = models.ErrorCode.NotFound
    return model


@pytest.fixture()
def full_api_key_verification() -> models.ApiKeyVerification:
    return _full_api_key_verification()


def test_to_api_key_verification(
    raw_api_key_verification: DictT,
    full_api_key_verification: models.ApiKeyVerification,
) -> None:
    result = serializer.to_api_key_verification(raw_api_key_verification)

    assert result == full_api_key_verification


##############
# to_ratelimit
##############


def _raw_ratelimit() -> DictT:
    return {
        "limit": 1,
        "refillRate": 2,
        "refillInterval": 3000,
        "type": "consistent",
    }


@pytest.fixture()
def raw_ratelimit() -> DictT:
    return _raw_ratelimit()


def _full_ratelimit() -> models.Ratelimit:
    return models.Ratelimit(
        limit=1,
        refill_rate=2,
        refill_interval=3000,
        type=models.RatelimitType.Consistent,
    )


@pytest.fixture()
def full_ratelimit() -> models.Ratelimit:
    return _full_ratelimit()


def test_to_ratelimit(
    raw_ratelimit: DictT,
    full_ratelimit: models.ApiKeyVerification,
) -> None:
    result = serializer.to_ratelimit(raw_ratelimit)

    assert result == full_ratelimit


#################
# to_api_key_meta
#################


def _raw_api_key_meta() -> DictT:
    return {
        "id": "fxc_DDD",
        "meta": {"test": 1},
        "start": "fxc",
        "apiId": "api_FFF",
        "expires": 123,
        "remaining": 12,
        "ownerId": "jonxslays",
        "createdAt": 456,
        "workspaceId": "ws_GGG",
        "ratelimit": {
            "type": "fast",
            "limit": 1,
            "refillRate": 2,
            "refillInterval": 3,
        },
    }


@pytest.fixture()
def raw_api_key_meta() -> DictT:
    return _raw_api_key_meta()


def _full_api_key_meta() -> models.ApiKeyMeta:
    model = models.ApiKeyMeta()
    model.id = "fxc_DDD"
    model.meta = {"test": 1}
    model.start = "fxc"
    model.api_id = "api_FFF"
    model.expires = 123
    model.remaining = 12
    model.owner_id = "jonxslays"
    model.created_at = 456
    model.workspace_id = "ws_GGG"
    model.ratelimit = models.Ratelimit(
        models.RatelimitType.Fast,
        limit=1,
        refill_rate=2,
        refill_interval=3,
    )

    return model


@pytest.fixture()
def full_api_key_meta() -> models.ApiKeyMeta:
    return _full_api_key_meta()


def test_to_api_key_meta(
    raw_api_key_meta: DictT,
    full_api_key_meta: models.ApiKeyMeta,
) -> None:
    result = serializer.to_api_key_meta(raw_api_key_meta)

    assert result == full_api_key_meta


#################
# to_api_key_list
#################


def _raw_api_key_list() -> DictT:
    return {"cursor": None, "total": 1, "keys": [_raw_api_key_meta()]}


@pytest.fixture()
def raw_api_key_list() -> DictT:
    return _raw_api_key_list()


def _full_api_key_list() -> models.ApiKeyList:
    model = models.ApiKeyList()
    model.cursor = None
    model.total = 1
    model.keys = [_full_api_key_meta()]
    return model


@pytest.fixture()
def full_api_key_list() -> models.ApiKeyList:
    return _full_api_key_list()


def test_to_api_key_list(
    raw_api_key_list: DictT,
    full_api_key_list: models.ApiKeyList,
) -> None:
    result = serializer.to_api_key_list(raw_api_key_list)

    assert result == full_api_key_list
