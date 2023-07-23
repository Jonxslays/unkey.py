from __future__ import annotations

import typing as t

from unkey import errors
from unkey import models
from unkey import result
from unkey import routes
from unkey import undefined

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
        name: undefined.UndefinedOr[str] = undefined.UNDEFINED,
        byte_length: undefined.UndefinedOr[int] = undefined.UNDEFINED,
        meta: undefined.UndefinedOr[t.Dict[str, t.Any]] = undefined.UNDEFINED,
        expires: undefined.UndefinedOr[int] = undefined.UNDEFINED,
        remaining: undefined.UndefinedOr[int] = undefined.UNDEFINED,
        ratelimit: undefined.UndefinedOr[models.Ratelimit] = undefined.UNDEFINED,
    ) -> ResultT[models.ApiKey]:
        """Creates a new api key.

        Args:
            name: The name to use for this key.

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

            remaining: The optional max number of times this key can be
                used. Useful for creating long lived keys but with a
                limit on total uses.

            ratelimit: The optional Ratelimit to set on this key.

        Returns:
            A result containing the requested information or an error.
        """
        route = routes.CREATE_KEY.compile()
        payload = self._generate_map(
            meta=meta,
            name=name,
            apiId=api_id,
            prefix=prefix,
            ownerId=owner_id,
            remaining=remaining,
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

        return result.Ok(models.HttpResponse(200, "OK"))

    async def update_key(
        self,
        key_id: str,
        *,
        name: undefined.UndefinedNoneOr[str] = undefined.UNDEFINED,
        owner_id: undefined.UndefinedNoneOr[str] = undefined.UNDEFINED,
        meta: undefined.UndefinedNoneOr[t.Dict[str, t.Any]] = undefined.UNDEFINED,
        expires: undefined.UndefinedNoneOr[int] = undefined.UNDEFINED,
        remaining: undefined.UndefinedNoneOr[int] = undefined.UNDEFINED,
        ratelimit: undefined.UndefinedNoneOr[models.Ratelimit] = undefined.UNDEFINED,
    ) -> ResultT[models.HttpResponse]:
        """Updates an existing api key. To delete a key set its value
        to `None`.

        Args:
            key_id: The id of the key to update.

        Keyword Args:
            name: The new name to use for this key.

            owner_id: The new owner id to use for this key.

            meta: The new dynamic mapping of information used
                to provide context around this keys user.

            expires: The new number of milliseconds into the future
                when this key should expire.

            remaining: The new max number of times this key can be
                used.

            ratelimit: The new Ratelimit to set on this key.

        Returns:
            A result containing the OK response or an error.
        """
        if undefined.all_undefined(name, owner_id, meta, expires, remaining, ratelimit):
            raise errors.MissingRequiredArgument("At least one value is required to be updated.")

        route = routes.UPDATE_KEY.compile(key_id)
        payload = self._generate_map(
            name=name,
            meta=meta,
            keyId=key_id,
            ownerId=owner_id,
            remaining=remaining,
            ratelimit=ratelimit,
            expires=self._expires_in(milliseconds=expires or 0)
            if expires is not None
            else expires,
        )

        data = await self._http.fetch(route, payload=payload)

        if isinstance(data, models.HttpResponse):
            return result.Err(data)

        return result.Ok(models.HttpResponse(200, "OK"))
