# Copyright (c) 2020 Nekokatt
# Copyright (c) 2021-present davfsa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

import typing as t

__all__ = ("UndefinedNoneOr", "UndefinedOr", "UNDEFINED")

# This code is almost line for line from https://github.com/hikari-py/hikari
# Thanks to the amazing developers on that project <3


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
