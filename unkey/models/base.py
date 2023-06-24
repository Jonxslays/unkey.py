from __future__ import annotations

import typing as t
from enum import Enum

import attrs

__all__ = ("BaseEnum", "BaseModel")

T = t.TypeVar("T", bound="BaseEnum")


@attrs.define(weakref_slot=False)
class BaseModel:
    """The base model all library models inherit from."""

    def to_dict(self) -> t.Dict[str, t.Any]:
        """Converts this class into a dictionary.

        Returns:
            The requested dictionary.
        """
        return attrs.asdict(self)


class BaseEnum(Enum):
    """The base enum all library enums inherit from."""

    __slots__ = ()

    value: str  # pyright: ignore

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls: t.Type[T], value: str) -> T:
        """Generate this enum from the given value.

        Args:
            value: The value to generate from.

        Returns:
            The generated enum.
        """
        try:
            return cls(value)
        except ValueError as e:
            raise ValueError(
                f"{e} variant. Please report this issue on github at "
                "https://github.com/Jonxslays/unkey.py/issues/new"
            ) from None

    @classmethod
    def from_str_maybe(cls: t.Type[T], value: str) -> t.Optional[T]:
        """Attempt to generate this enum from the given value.

        Args:
            value: The value to generate from.

        Returns:
            The generated enum or `None` if the value was not a valid
                enum variant.
        """
        try:
            return cls(value)
        except ValueError:
            return None
