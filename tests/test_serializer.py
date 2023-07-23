from __future__ import annotations

import typing as t
from datetime import datetime

import pytest

from unkey import Serializer
from unkey import models

# from unittest import mock


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


#########################
# to_api_key_verification
#########################


def _raw_api_key_verification() -> DictT:
    return {
        "valid": False,
        "owner_id": None,
        "meta": None,
        "remaining": None,
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
    return {"total": 1, "keys": [_raw_api_key_meta()]}


@pytest.fixture()
def raw_api_key_list() -> DictT:
    return _raw_api_key_list()


def _full_api_key_list() -> models.ApiKeyList:
    model = models.ApiKeyList()
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
