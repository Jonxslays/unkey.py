from __future__ import annotations

import abc
import typing as t
from datetime import datetime
from datetime import timedelta

from unkey import undefined

if t.TYPE_CHECKING:
    from unkey import serializer

    from . import HttpService

__all__ = ("BaseService",)


class BaseService(abc.ABC):
    """The base service all API services inherit from.

    Args:
        http_service: The http service to use for requests.

        serializer: The serializer to use for handling incoming
            JSON data from the API.
    """

    __slots__ = ("_http", "_serializer")

    def __init__(self, http_service: HttpService, serializer: serializer.Serializer) -> None:
        self._http = http_service
        self._serializer = serializer

    def _generate_map(self, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        return {k: v for k, v in kwargs.items() if v is not undefined.UNDEFINED}

    def _expires_in(
        self, *, milliseconds: int = 0, seconds: int = 0, minutes: int = 0, days: int = 0
    ) -> undefined.UndefinedOr[int]:
        if not any({milliseconds, seconds, minutes, days}):
            return undefined.UNDEFINED

        delta = timedelta(days=days, minutes=minutes, seconds=seconds, milliseconds=milliseconds)
        return int((datetime.now() + delta).timestamp()) * 1000
