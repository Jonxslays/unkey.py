from __future__ import annotations

import typing as t

import attrs

from .base import BaseEnum
from .base import BaseModel
from .http import ErrorCode

__all__ = (
    "ApiKey",
    "ApiKeyMeta",
    "ApiKeyVerification",
    "Ratelimit",
    "RatelimitState",
    "RatelimitType",
    "Refill",
    "RefillInterval",
    "UpdateOp",
)


class RatelimitType(BaseEnum):
    Fast = "fast"
    Consistent = "consistent"


class RefillInterval(BaseEnum):
    Daily = "daily"
    Monthly = "monthly"


class UpdateOp(BaseEnum):
    Increment = "increment"
    Decrement = "decrement"
    Set = "set"


@attrs.define(weakref_slot=False)
class Ratelimit(BaseModel):
    """Data representing a particular ratelimit."""

    type: RatelimitType
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
class ApiKeyMeta(BaseModel):
    """Metadata about an api key."""

    id: str
    """The id of this key."""

    api_id: str
    """The id of the api this key belongs to."""

    workspace_id: str
    """The id of the workspace this key belongs to."""

    start: str
    """The prefix and beginning 3 letters of the key."""

    created_at: int
    """The unix epoch representing when this key was created in
    milliseconds."""

    owner_id: t.Optional[str]
    """The owner of this api key if one was specified."""

    expires: t.Optional[int]
    """The optional unix epoch representing when this key expires in
    milliseconds."""

    ratelimit: t.Optional[Ratelimit]
    """The optional ratelimit associated with this key."""

    meta: t.Optional[t.Dict[str, t.Any]]
    """The dynamic mapping of data used during key creation, if
    the key was found.
    """

    remaining: t.Optional[int]
    """The remaining verifications before this key is invalidated.
    If `None`, this field was not used in the keys creation and can
    be ignored.
    """

    refill: t.Optional[Refill]
    """The keys refill state, if any."""


@attrs.define(init=False, weakref_slot=False)
class ApiKeyVerification(BaseModel):
    """Data about whether this api key and its validity."""

    id: t.Optional[str]
    """The id of this key."""

    valid: bool
    """Whether or not this key is valid and passes ratelimit."""

    owner_id: t.Optional[str]
    """The id of the owner for this key, if the key was found."""

    meta: t.Optional[t.Dict[str, t.Any]]
    """Dynamic mapping of data used during key creation, if the
    key was found.
    """

    remaining: t.Optional[int]
    """The remaining verifications before this key is invalidated.
    If `None`, this field was not used in the keys creation and can
    be ignored.
    """

    expires: t.Optional[int]
    """The unix epoch in milliseconds indicating when this key expires,
    if it does."""

    ratelimit: t.Optional[RatelimitState]
    """The state of the ratelimit set on this key, if any."""

    refill: t.Optional[Refill]
    """The keys refill state, if any."""

    code: t.Optional[ErrorCode]
    """The optional error code returned by the unkey api."""

    error: t.Optional[str]
    """The error message if the key was invalid."""

    @staticmethod
    def __internal_serialize(_: type, __: t.Any, value: t.Any) -> t.Any:
        if isinstance(value, ErrorCode):
            # Automatically convert ErrorCodes to strings for to_dict()
            return str(value)

        return value

    def to_dict(self) -> t.Dict[str, t.Any]:
        """Converts this class into a dictionary.

        Returns:
            The requested dictionary.
        """
        return attrs.asdict(self, value_serializer=self.__internal_serialize)


@attrs.define(init=False, weakref_slot=False)
class RatelimitState(BaseModel):
    """The state of the ratelimit for a given key."""

    limit: int
    """The number of burstable requests allowed."""

    remaining: int
    """The remaining requests in this burst window."""

    reset: int
    """The unix timestamp in milliseconds until the next window."""


@attrs.define(weakref_slot=False)
class Refill(BaseModel):
    """Data regarding how a key's verifications should be refilled."""

    amount: int
    """The number of verifications to refill."""

    interval: RefillInterval
    """The interval at which to refill the verifications."""

    last_refilled_at: t.Optional[int] = None
    """The UNIX timestamp in milliseconds indicating when the key was
    las refilled, if it has been.
    """
