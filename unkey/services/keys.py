from __future__ import annotations

import typing as t

from unkey import models
from unkey import routes
from unkey import result

from . import BaseService

__all__ = ("KeyService",)

T = t.TypeVar("T")
ResultT = result.Result[T, models.HttpErrorResponse]


class KeyService(BaseService):
    """Handles api key related requests."""

    __slots__ = ()

    async def create_key(
        self,
        api_id: str,
        owner_id: str,
        prefix: str,
        *,
        byte_length: int = 16,
        meta: t.Dict[str, t.Any] = {},
        expires: t.Optional[int] = None,
        ratelimit: t.Optional[models.RateLimit] = None,
    ) -> ResultT[models.ApiKey]:
        route = routes.CREATE_KEY.compile()
        ratelimit_data = None

        if ratelimit:
            ratelimit_data = self._generate_map(
                type=ratelimit.type,
                limit=ratelimit.limit,
                refillRate=ratelimit.refill_rate,
                refillInterval=ratelimit.refill_interval,
            )

        payload = self._generate_map(
            meta=meta,
            prefix=prefix,
            apiId=api_id,
            expires=expires,
            owner_id=owner_id,
            byteLength=byte_length,
            ratelimit=ratelimit_data,
        )

        data = await self._http.fetch(route, payload=payload)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.to_api_key(data))
