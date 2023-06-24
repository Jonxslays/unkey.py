from __future__ import annotations

import typing as t

from unkey import models
from unkey import result
from unkey import routes

from . import BaseService

__all__ = ("KeyService",)

T = t.TypeVar("T")
ResultT = result.Result[T, models.HttpResponse]


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
        ratelimit: t.Optional[models.Ratelimit] = None,
    ) -> ResultT[models.ApiKey]:
        """Creates a new api key.

        Args:
            api_id: The id of the api this key is for.

            owner_id: The owner id to use for this key. Represents the
                user who will use this key.

            prefix: The prefix to place at the beginning of the key.

        Keyword Args:
            byte_length: The optional desired length of they in bytes.
                Defaults to 16.

            meta: An optional dynamic mapping of information used to
                provide context around this keys user.

            expires: The optional number of milliseconds into the future
                when this key should expire.

            ratelimit: The optional Ratelimit to set on this key.

        Returns:
            A result containing the requested information or an error.
        """
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

        if isinstance(data, models.HttpResponse):
            return result.Err(data)

        return result.Ok(self._serializer.to_api_key(data))

    async def verify_key(self, key: str) -> ResultT[models.ApiKeyVerification]:
        """Verifies a key is valid and within ratelimit.

        Args:
            key: The key to verify.

        Returns:
            A result containing the api key verification or an error.
        """
        route = routes.VERIFY_KEY.compile()
        payload = self._generate_map(key=key)
        data = await self._http.fetch(route, payload=payload)

        if isinstance(data, models.HttpResponse):
            return result.Err(data)

        return result.Ok(self._serializer.to_api_key_verification(data))

    async def revoke_key(self, key_id: str) -> ResultT[models.HttpResponse]:
        """Revokes a keys validity.

        Args:
            key_id: The id of the key to revoke.

        Returns:
            A result containing the http response or an error.
        """
        route = routes.REVOKE_KEY.compile(key_id)
        data: str | models.HttpResponse = await self._http.fetch(route)  # type: ignore

        if isinstance(data, models.HttpResponse):
            return result.Err(data)

        return result.Ok(models.HttpResponse(202, data))
