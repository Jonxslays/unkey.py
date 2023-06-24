from __future__ import annotations

import typing as t

import attrs

from .base import BaseEnum
from .base import BaseModel

__all__ = ("ApiKey", "ApiKeyVerification", "RateLimit", "RateLimitType")


class RateLimitType(BaseEnum):
    Fast = "fast"
    Consistent = "consistent"


@attrs.define(weakref_slot=False)
class RateLimit(BaseModel):
    """Data representing a particular ratelimit."""

    type: RateLimitType
    """The type of ratelimiting to implement."""

    limit: int
    """The total amount of burstable requests."""

    refill_rate: int
    """How many tokens to refill during each refill interval."""

    refill_interval: int
    """The speed at which tokens are refilled."""


@attrs.define(init=False, weakref_slot=False)
class ApiKey(BaseModel):
    """Minimal representation of an api key."""

    key_id: str
    """The id of this key stored at unkey."""

    key: str
    """The api key itself."""


@attrs.define(init=False, weakref_slot=False)
class ApiKeyVerification(BaseModel):
    """Data about whether this api key is valid."""

    valid: bool
    """Whether or not this key is valid and passes ratelimit."""

    owner_id: t.Optional[str]
    """The id of the owner for this key, if the key was found."""

    meta: t.Optional[t.Dict[str, t.Any]]
    """Dynamic mapping of data used during key creation, if the
    key was found.
    """

    error: t.Optional[str]
    """The error message if the key was invalid."""
