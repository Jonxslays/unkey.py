from __future__ import annotations

import typing as t

import attrs

from .base import BaseEnum
from .base import BaseModel

__all__ = ("ApiKey", "ApiKeyCreationMeta", "RateLimit", "RateLimitType")


class RateLimitType(BaseEnum):
    Fast = "fast"
    Consistent = "consistent"


@attrs.define(init=False, weakref_slot=False)
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

    key: str
    """The api key itself."""

    id: str
    """The id of this key stored at unkey."""


@attrs.define(weakref_slot=False)
class ApiKeyCreationMeta(BaseModel):
    """Data representing all metadata about a new key that is being
    created.
    """

    api_id: str
    """The id for the api this key will be used to access."""

    prefix: str
    """The prefix to use for the key."""

    owner_id: str
    """The id of the owner who will use this key."""

    byte_length: int = 16
    """The length to use for the key in bytes (defaults to 16)."""

    meta: t.Dict[str, t.Any] = attrs.field(factory=dict)
    """Optional dynamic metadata that you feel is useful."""

    expires: t.Optional[int] = None
    """The optional unix epoch timestamp when this key should expire."""

    ratelimit: t.Optional[RateLimit] = None
    """The optional ratelimit to place on this key."""


