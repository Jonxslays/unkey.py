from __future__ import annotations

import typing as t

from unkey import models
from unkey import result
from unkey import routes

from . import BaseService

__all__ = ("ApiService",)

T = t.TypeVar("T")
ResultT = result.Result[T, models.HttpErrorResponse]


class ApiService(BaseService):
    """Handles api related requests."""

    __slots__ = ()

    async def get_api(self, api_id: str) -> ResultT[models.Api]:
        route = routes.GET_API.compile(api_id)
        data = await self._http.fetch(route)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.to_api(data))

    async def get_keys(
        self, api_id: str, *, limit: int = 100, offset: int = 0
    ) -> ResultT[models.ApiKeyList]:
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.GET_KEYS.compile(api_id).with_params(params)
        data = await self._http.fetch(route)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.to_api_key_list(data))
