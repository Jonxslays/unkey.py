from __future__ import annotations

import attrs

from .base import BaseEnum
from .base import BaseModel

__all__ = ("ApiKey", "RateLimit", "RateLimitType")


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

    key: str
    """The api key itself."""

    id: str
    """The id of this key stored at unkey."""
