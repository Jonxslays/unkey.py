from __future__ import annotations

import abc
import typing as t

from unkey import errors

__all__ = ("Err", "Ok", "Result")

T = t.TypeVar("T")
E = t.TypeVar("E")


class Result(t.Generic[T, E], abc.ABC):
    """Represents a potential `Ok` or `Err` result.

    Note:
        This class can not be instantiated, only its variants can.
    """

    __slots__ = ("_error", "_value")

    def __repr__(self) -> str:
        inner = self._value if self.is_ok else self._error  # type: ignore [attr-defined]
        return f"{self.__class__.__name__}({inner})"

    @property
    @abc.abstractmethod
    def is_ok(self) -> bool:
        """`True` if this result is the `Ok` variant."""

    @property
    @abc.abstractmethod
    def is_err(self) -> bool:
        """`True` if this result is the `Err` variant."""

    @abc.abstractmethod
    def unwrap(self) -> T:
        """Unwraps the result to produce the value.

        Returns:
            The unwrapped value.

        Raises:
            UnwrapError: If the result was an `Err` and not `Ok`.
        """

    @abc.abstractmethod
    def unwrap_err(self) -> E:
        """Unwraps the result to produce the error.

        Returns:
            The unwrapped error.

        Raises:
            UnwrapError: If the result was `Ok` and not an `Err`.
        """


@t.final
class Ok(Result[T, E]):
    __slots__ = ()

    def __init__(self, value: T) -> None:
        self._value = value

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_err(self) -> E:
        actual = self._value.__class__.__name__
        raise errors.UnwrapError(f"Called unwrap error on a non error value of type {actual!r}")


@t.final
class Err(Result[T, E]):
    __slots__ = ()

    def __init__(self, error: E) -> None:
        self._error = error

    @property
    def is_ok(self) -> bool:
        return False

    @property
    def is_err(self) -> bool:
        return True

    def unwrap(self) -> T:
        raise errors.UnwrapError(f"Called unwrap on an error value - {self._error}")

    def unwrap_err(self) -> E:
        return self._error
