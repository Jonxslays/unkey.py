from __future__ import annotations

from unittest import mock

import pytest

from unkey import Client
from unkey import services


async def test_all_services_exist() -> None:
    client = Client("api_key_123")
    assert isinstance(client.keys, services.KeyService)
    assert isinstance(client.apis, services.ApiService)
    await client.close()


@mock.patch("unkey.client.serializer.Serializer")
@mock.patch("unkey.client.services.HttpService")
async def test_basic_init(http: mock.MagicMock, serializer: mock.MagicMock) -> None:
    _ = Client("abc123")
    http.assert_called_once_with("abc123", None, None)
    serializer.assert_called_once()


@mock.patch("unkey.client.serializer.Serializer")
@mock.patch("unkey.client.services.HttpService")
async def test_full_init(http: mock.MagicMock, serializer: mock.MagicMock) -> None:
    _ = Client("abc", api_version=69, api_base_url="fake")
    http.assert_called_once_with("abc", 69, "fake")
    serializer.assert_called_once()


def test_empty_api_key_fails() -> None:
    with pytest.raises(ValueError) as e:
        Client("")

    assert e.exconly() == "ValueError: Api key must be provided."


@mock.patch("unkey.client.services.HttpService.set_api_key")
async def test_set_api_key(set_api_key: mock.MagicMock) -> None:
    client = Client("fake")
    client.set_api_key("hello")
    set_api_key.assert_called_once_with("hello")


@mock.patch("unkey.client.services.HttpService.set_base_url")
async def test_set_api_base_url(set_base_url: mock.MagicMock) -> None:
    client = Client("abc")
    client.set_api_base_url("https://localhost:6969")
    set_base_url.assert_called_once_with("https://localhost:6969")


@mock.patch("unkey.client.services.HttpService.start")
async def test_start(start: mock.MagicMock) -> None:
    client = Client("abc123")
    await client.start()
    start.assert_called_once()


@mock.patch("unkey.client.services.HttpService.close")
async def test_close(close: mock.MagicMock) -> None:
    client = Client("abc123")
    await client.close()
    close.assert_called_once()


@mock.patch("unkey.client.Client._Client__init_service")
async def test_init_services(init_service: mock.MagicMock) -> None:
    _ = Client("abc")
    init_service.assert_has_calls(
        (
            mock.call(services.ApiService),
            mock.call(services.KeyService),
        )
    )


async def test_init_service_fails() -> None:
    client = Client("abc")

    with pytest.raises(TypeError) as e:
        client._Client__init_service(int)  # type: ignore

    assert e.exconly() == "TypeError: 'int' can not be initialized as a service."
    await client.close()
