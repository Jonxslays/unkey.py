from __future__ import annotations

import typing as t

from unkey import models
from unkey import result
from unkey import routes
from unkey import undefined

from . import BaseService

__all__ = ("ApiService",)

T = t.TypeVar("T")
ResultT = result.Result[T, models.HttpResponse]


class ApiService(BaseService):
    """Handles api related requests."""

    __slots__ = ()

    async def get_api(self, api_id: str) -> ResultT[models.Api]:
        """Gets information about an api.

        Args:
            api_id: The id of the api.

        Returns:
            A result containing the requested information or an error.
        """
        route = routes.GET_API.compile(api_id)
        data = await self._http.fetch(route)

        if isinstance(data, models.HttpResponse):
            return result.Err(data)

        if "error" in data:
            return result.Err(
                models.HttpResponse(
                    404,
                    data["error"],
                    models.ErrorCode.from_str_maybe(data.get("code", "unknown")),
                )
            )

        return result.Ok(self._serializer.to_api(data))

    async def list_keys(
        self,
        api_id: str,
        *,
        owner_id: undefined.UndefinedOr[str] = undefined.UNDEFINED,
        limit: int = 100,
        offset: int = 0,
    ) -> ResultT[models.ApiKeyList]:
        """Gets a paginated list of keys for the given api.

        Args:
            api_id: The id of the api.

        Keyword Args:
            owner_id: The optional owner id to list the keys for.

            limit: The max number of keys to include in this page.
                Defaults to 100.

            offset: How many keys to offset by, for pagination.

        Returns:
            A result containing api key list or an error.
        """
        params = self._generate_map(ownerId=owner_id, limit=limit, offset=offset)
        route = routes.GET_KEYS.compile(api_id).with_params(params)
        data = await self._http.fetch(route)

        if isinstance(data, models.HttpResponse):
            return result.Err(data)

        if "error" in data:
            return result.Err(
                models.HttpResponse(
                    404,
                    data["error"],
                    models.ErrorCode.from_str_maybe(data.get("code", "unknown")),
                )
            )

        return result.Ok(self._serializer.to_api_key_list(data))
