from __future__ import annotations

import typing as t

import aiohttp

from unkey import constants
from unkey import models
from unkey import routes

__all__ = ("HttpService",)

T = t.TypeVar("T")


class HttpService:
    """The HTTP service used to make requests to the WOM API.

    Args:
        api_key: The api key to use.

        api_base_url: The optional api base url to use.
    """

    __slots__ = ("_base_url", "_headers", "_method_mapping", "_session")

    def __init__(
        self,
        api_key: str,
        api_base_url: t.Optional[str],
    ) -> None:
        self._headers = {
            "x-user-agent": constants.USER_AGENT,
            "Authorization": f"Bearer {api_key}",
        }

        self._base_url = api_base_url or constants.API_BASE_URL

    async def _try_get_json(self, response: aiohttp.ClientResponse) -> t.Any:
        try:
            return await response.json()
        except Exception:
            return models.HttpError(
                response.status, "Unable to deserialize response, the api is likely down."
            )

    async def _request(
        self, req: t.Callable[..., t.Awaitable[t.Any]], url: str, **kwargs: t.Any
    ) -> t.Any:
        response = await req(url, **kwargs)
        data = await self._try_get_json(response)

        if isinstance(data, models.HttpError):
            return data

        if not response.ok:
            return models.HttpError(
                response.status,
                # TODO: Check what property error messages are returned in
                data.get("message", "An unexpected error occurred while making the request."),
            )

        return data

    def _get_request_func(self, method: str) -> t.Callable[..., t.Awaitable[t.Any]]:
        if not hasattr(self, "_method_mapping"):
            raise RuntimeError("HttpService.start was never called, aborting...")

        return self._method_mapping[method]  # type: ignore

    async def _init_session(self) -> None:
        self._session = aiohttp.ClientSession()
        self._method_mapping = {
            constants.GET: self._session.get,
            constants.PUT: self._session.put,
            constants.POST: self._session.post,
            constants.PATCH: self._session.patch,
            constants.DELETE: self._session.delete,
        }

    def set_api_key(self, api_key: str) -> None:
        """Sets the api key used by the http service.

        Args:
            api_key: The new api key to use.
        """
        self._headers["x-api-key"] = api_key

    def unset_api_key(self) -> None:
        """Un-sets the current api key so it isn't sent with requests."""
        if "x-api-key" in self._headers:
            del self._headers["x-api-key"]

    def set_base_url(self, base_url: str) -> None:
        """Sets the api base url used by the http service.

        Args:
            base_url: The new base url to use.
        """
        self._base_url = base_url

    async def start(self) -> None:
        """Starts the client session to be used by the http service."""
        if not hasattr(self, "_session"):
            await self._init_session()

    async def close(self) -> None:
        """Closes the existing client session, if it's still open."""
        if hasattr(self, "_session") and not self._session.closed:
            await self._session.close()

    async def fetch(
        self,
        route: routes.CompiledRoute,
        _: t.Type[T],
        *,
        payload: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> T | models.HttpError:
        """Fetches the given route.

        Args:
            route: The route to make the request to.

            _: The type expected to be returned.

            payload: The optional payload to send in the request body.

        Returns:
            The requested json data or the error response.
        """
        return await self._request(  # type: ignore[no-any-return]
            self._get_request_func(route.method),
            self._base_url + route.uri,
            headers=self._headers,
            params=route.params,
            json=payload or None,
        )