from __future__ import annotations

import typing as t

import attrs

__all__ = ("BaseModel",)


@attrs.define(weakref_slot=False)
class BaseModel:
    """The base model all library models inherit from."""

    def to_dict(self) -> t.Dict[str, t.Any]:
        """Converts this class into a dictionary.

        Returns:
            The requested dictionary.
        """
        return attrs.asdict(self)
