from __future__ import annotations

import typing as t

from unkey import models
from unkey import result
from unkey import routes
from unkey.undefined import UNDEFINED
from unkey.undefined import UndefinedOr

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
        params = self._generate_map(apiId=api_id)
        route = routes.GET_API.compile().with_params(params)
        data = await self._http.fetch(route)

        if isinstance(data, models.HttpResponse):
            return result.Err(data)

        if "error" in data:
            return result.Err(
                models.HttpResponse(
                    404,
                    data["error"].get("message", "Unknown error"),
                    models.ErrorCode.from_str_maybe(data["error"].get("code", "UNKNOWN")),
                )
            )

        return result.Ok(self._serializer.to_api(data))

    async def list_keys(
        self,
        api_id: str,
        *,
        owner_id: UndefinedOr[str] = UNDEFINED,
        limit: UndefinedOr[int] = UNDEFINED,
        cursor: UndefinedOr[str] = UNDEFINED,
    ) -> ResultT[models.ApiKeyList]:
        """Gets a paginated list of keys for the given api.

        Args:
            api_id: The id of the api.

        Keyword Args:
            owner_id: The optional owner id to list the keys for.

            limit: The optional max number of keys to include in this page.

            cursor: Optional key used to determine pagination offset.

        Returns:
            A result containing api key list or an error.
        """
        params = self._generate_map(apiId=api_id, ownerId=owner_id, limit=limit, cursor=cursor)
        route = routes.GET_KEYS.compile().with_params(params)
        data = await self._http.fetch(route)

        if isinstance(data, models.HttpResponse):
            return result.Err(data)

        if "error" in data:
            return result.Err(
                models.HttpResponse(
                    404,
                    data["error"].get("message", "Unknown error"),
                    models.ErrorCode.from_str_maybe(data["error"].get("code", "UNKNOWN")),
                )
            )

        return result.Ok(self._serializer.to_api_key_list(data))
