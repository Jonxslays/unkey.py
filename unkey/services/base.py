from __future__ import annotations

import abc
import typing as t

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
        return {k: v for k, v in kwargs.items() if v is not None}
