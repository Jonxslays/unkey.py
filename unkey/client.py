from __future__ import annotations

import typing as t

from unkey import serializer
from unkey import services

__all__ = ("Client",)

ServiceT = t.TypeVar("ServiceT")


class Client:
    """An asynchronous client used for interacting with the API."""

    __slots__ = (
        "_http",
        "_keys",
        "_serializer",
    )

    def __init__(
        self,
        api_key: str,
        *,
        api_version: t.Optional[int] = None,
        api_base_url: t.Optional[str] = None,
    ) -> None:
        self._serializer = serializer.Serializer()
        self._http = services.HttpService(api_key, api_version, api_base_url)
        self.__init_core_services()

    def __init_core_services(self) -> None:
        self._keys = self.__init_service(services.KeyService)

    def __init_service(self, service: t.Type[ServiceT]) -> ServiceT:
        if not issubclass(service, services.BaseService):
            raise TypeError(f"{service.__name__!r} can not be initialized as a service.")

        return service(self._http, self._serializer)  # type: ignore[return-value]

    @property
    def keys(self) -> services.KeyService:
        """The key service used to make key related requests."""
        return self._keys

    def set_api_key(self, api_key: str) -> None:
        """Sets the api key used by the http service."""
        self._http.set_api_key(api_key)

    def set_api_base_url(self, base_url: str) -> None:
        """Sets the api base url used by the http service."""
        self._http.set_base_url(base_url)

    async def start(self) -> None:
        """Starts the client session to be used for http requests."""
        await self._http.start()

    async def close(self) -> None:
        """Closes the existing client session, if it's still open."""
        await self._http.close()
