from __future__ import annotations

import typing as t

import attrs

from unkey import constants as c

__all__ = ("CompiledRoute", "Route")


@attrs.define(weakref_slot=False)
class CompiledRoute:
    """A route that has been compiled to include uri variables.

    Args:
        route: The route itself.
        uri: The endpoint for this route.
    """

    route: Route
    """The route itself."""

    uri: str
    """The routes uri endpoint."""

    params: t.Dict[str, t.Union[str, int]] = attrs.field(init=False)
    """The query params for the route."""

    def __init__(self, route: Route, uri: str) -> None:
        self.route = route
        self.uri = uri
        self.params = {}

    @property
    def method(self) -> str:
        """The routes method, i.e. GET, POST..."""
        return self.route.method

    def with_params(self, params: t.Dict[str, t.Any]) -> CompiledRoute:
        """Adds additional query params to this compiled route.

        Args:
            params: The query params to compile.

        Returns:
            The compiled route for chained calls.
        """
        if params:
            self.params.update(params)

        return self


@attrs.define(weakref_slot=False)
class Route:
    """A route that has not been compiled yet."""

    method: str
    """The request method to use."""

    uri: str
    """The request uri."""

    def compile(self, *args: t.Union[str, int]) -> CompiledRoute:
        """Turn this route into a compiled route.

        Args:
            *args: The arguments to insert into the uri.

        Returns:
            The compiled route.
        """
        compiled = CompiledRoute(self, self.uri)

        for arg in args:
            compiled.uri = compiled.uri.replace(r"{}", str(arg), 1)

        return compiled


# Keys
CREATE_KEY: t.Final[Route] = Route(c.POST, "/keys")
VERIFY_KEY: t.Final[Route] = Route(c.POST, "/keys/verify")
REVOKE_KEY: t.Final[Route] = Route(c.DELETE, "/keys/{}")
UPDATE_KEY: t.Final[Route] = Route(c.PUT, "/keys/{}")

# Apis
GET_API: t.Final[Route] = Route(c.GET, "/apis/{}")
GET_KEYS: t.Final[Route] = Route(c.GET, "/apis/{}/keys")
