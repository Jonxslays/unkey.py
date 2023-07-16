from __future__ import annotations

import pytest

from unkey import CompiledRoute
from unkey import Route


@pytest.fixture()
def mock_route() -> Route:
    return Route("GET", "/69420")


@pytest.fixture()
def mock_route_w_uri() -> Route:
    return Route("POST", "/69420/{}/hi/{}")


def test_route_instantiation(mock_route: Route) -> None:
    assert mock_route.method == "GET"
    assert mock_route.uri == "/69420"


def test_route_compiles(mock_route: Route) -> None:
    compiled = mock_route.compile()
    assert isinstance(compiled, CompiledRoute)
    assert compiled.route == mock_route
    assert compiled.uri == "/69420"
    assert compiled.method == "GET"
    assert not compiled.params


def test_route_compiles_w_uri(mock_route_w_uri: Route) -> None:
    compiled = mock_route_w_uri.compile(1, 2)
    assert isinstance(compiled, CompiledRoute)
    assert compiled.route == mock_route_w_uri
    assert compiled.uri == "/69420/1/hi/2"
    assert compiled.method == "POST"
    assert not compiled.params


def test_route_compiles_w_params(mock_route: Route) -> None:
    compiled = mock_route.compile().with_params({"test": 1})
    assert isinstance(compiled, CompiledRoute)
    assert compiled.route == mock_route
    assert compiled.uri == "/69420"
    assert compiled.method == "GET"
    assert len(compiled.params) == 1
    assert compiled.params["test"] == 1
