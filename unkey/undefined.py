from __future__ import annotations

import typing as t

__all__ = ("UndefinedNoneOr", "UndefinedOr", "UNDEFINED")


class Undefined:
    """Represents an undefined value - without being None."""

    __slots__ = ()

    def __bool__(self) -> t.Literal[False]:
        return False

    def __copy__(self) -> Undefined:
        return self

    def __deepcopy__(self, memo: t.MutableMapping[int, t.Any]) -> Undefined:
        memo[id(self)] = self
        return self

    def __getstate__(self) -> t.Any:
        return False

    def __repr__(self) -> str:
        return "UNDEFINED"

    def __reduce__(self) -> str:
        return "UNDEFINED"

    def __str__(self) -> str:
        return "UNDEFINED"


def __singleton_new(cls: t.Any) -> t.NoReturn:
    raise TypeError("Cannot instantiate singleton class UNDEFINED.")


UNDEFINED = Undefined()
"""A value that does not exist."""

Undefined.__new__ = __singleton_new  # type: ignore

T = t.TypeVar("T", covariant=True)

UndefinedOr = t.Union[T, Undefined]
"""A value that is undefined or T"""

UndefinedNoneOr = UndefinedOr[t.Optional[T]]
"""A value that is undefined, none, or T"""


def all_undefined(*values: t.Any) -> bool:
    """Whether or not all values are undefined.

    Arguments:
        *values: The values to check.

    Returns:
        `True` if all values were undefined.
    """
    return all(v is UNDEFINED for v in values)


def any_undefined(*values: t.Any) -> bool:
    """Whether or not any values are undefined.

    Arguments:
        *values: The values to check.

    Returns:
        `True` if any values were undefined.
    """
    return any(v is UNDEFINED for v in values)
