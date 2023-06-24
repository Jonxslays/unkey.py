from __future__ import annotations

import typing as t

from unkey import models
from unkey import result
from unkey import routes

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
        payload = self._generate_map(
            meta=meta,
            apiId=api_id,
            prefix=prefix,
            ownerId=owner_id,
            byteLength=byte_length,
            expires=self._expires_in(milliseconds=expires or 0),
            ratelimit=None
            if not ratelimit
            else self._generate_map(
                limit=ratelimit.limit,
                type=ratelimit.type.value,
                refillRate=ratelimit.refill_rate,
                refillInterval=ratelimit.refill_interval,
            ),
        )

        data = await self._http.fetch(route, payload=payload)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.to_api_key(data))

    async def verify_key(self, key: str) -> ResultT[models.ApiKeyVerification]:
        route = routes.VERIFY_KEY.compile()
        payload = self._generate_map(key=key)
        data = await self._http.fetch(route, payload=payload)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.to_api_key_verification(data))

    async def revoke_key(self, key_id: str) -> ResultT[None]:
        route = routes.REVOKE_KEY.compile(key_id)
        data = await self._http.fetch(route)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(None)
