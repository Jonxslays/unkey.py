from __future__ import annotations

import typing as t

import attrs

from .base import BaseModel
from .keys import ApiKeyMeta

__all__ = ("Api", "ApiKeyList")


@attrs.define(init=False, weakref_slot=False)
class Api(BaseModel):
    """Data representing a particular ratelimit."""

    id: str
    """The id for this api."""

    name: str
    """The name of the api."""

    workspace_id: str
    """The id for the workspace this api belongs to."""


@attrs.define(init=False, weakref_slot=False)
class ApiKeyList(BaseModel):
    """Data representing keys for an api."""

    keys: t.List[ApiKeyMeta]
    """A list of keys associated with the api."""

    total: int
    """The total number of keys associated with the api."""
