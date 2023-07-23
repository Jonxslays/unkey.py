from __future__ import annotations

import typing as t

__all__ = ("UndefinedNoneOr", "UndefinedOr", "UNDEFINED")


class Undefined:
    """Represents an undefined value - without being None."""

    __slots__ = ()

    def __bool__(self) -> t.Literal[False]:
        return False

    def __str__(self) -> str:
        return "UNDEFINED"


UNDEFINED = Undefined()
"""A value that does not exist."""

T = t.TypeVar("T", covariant=True)

UndefinedOr = t.Union[T, Undefined]
"""A value that is undefined or T"""

UndefinedNoneOr = t.Union[UndefinedOr[T], None]
"""A value that is undefined, none, or T"""


def all_undefined(*values: t.Any) -> bool:
    """Whether or not all values are undefined.

    Returns:
        bool: `True` if all values were undefined.
    """
    return all(v is UNDEFINED for v in values)


def any_undefined(*values: t.Any) -> bool:
    """Whether or not any values are undefined.

    Returns:
        bool: `True` if any values were undefined.
    """
    return any(v is UNDEFINED for v in values)
