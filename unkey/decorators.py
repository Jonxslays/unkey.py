from __future__ import annotations

import functools
import inspect
from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

from unkey import client
from unkey import models

__all__ = ("protected",)

T = TypeVar("T")
CallableT = Callable[..., T]
CallbackT = CallableT[Any]
DecoratorT = CallableT[CallbackT]
VerificationResponseT = Union[T, Any]
ExtractorT = Callable[[Tuple[Any], Dict[str, Any]], Optional[str]]
"""The type of a callback used to extract the api key from the decorated
functions `*args` and `**kwargs`.
"""

InvalidKeyHandlerT = Optional[Callable[[Dict[str, Any], Optional[models.ApiKeyVerification]], Any]]
"""The type of a callback used to handle cases where the key was invalid."""

ExcHandlerT = Optional[Callable[[Exception], Any]]
"""The type of a callback used to handle exceptions during verification."""


def protected(
    api_id: str,
    key_extractor: ExtractorT,
    on_invalid_key: InvalidKeyHandlerT = None,
    on_exc: ExcHandlerT = None,
) -> DecoratorT:
    """A framework agnostic second order decorator that is used to protect
    api routes with Unkey key verification.

    !!! info

        An endpoint decorated with this decorator guarantees that once the
        decorated function body is reached that the api key was verified and
        is valid.

        A keyword argument `unkey_verification` will be injected into the
        function on a successful verification so you should make sure you
        accept that argument in the decorated function. From there feel
        free to inspect the returned `ApiKeyVerification` for any properties
        of interest.

    Args:
        api_id: The ID of the api to verify keys against.

        key_extractor: The callback function used to extract the api key
            from the `*args` and `**kwargs` of the decorated function. It
            should return the key stripped of the "Bearer " prefix or `None`.

        on_invalid_key: The callback function used to transform the output
            from an invalid key. This can mean the key could not be parsed, the
            key was not found, or the key was actually invalid. This function
            should accept a dictionary and an optional `ApiKeyVerification`.
            The verification will be provided in cases where we were able to
            successfully retrieve it from Unkey.

        on_exc: The callback function used to handle exceptions that get thrown
            at any point during verification.

    Raises:
        exc: If an exception is raised and no `on_exc` callback was supplied.

    Returns:
        A function that replaces the decorated function, and performs Unkey
            key verification prior to calling the decorated function.
            If the key could not be parsed or was invalid, a dictionary
            containing "code" and "message" keys will be returned, unless
            altered by `on_invalid_key` if it was passed. If verification
            succeeds the original functions return value is returned.
    """
    _client = client.Client()

    def _on_invalid_key(
        data: Dict[str, Any], verification: Optional[models.ApiKeyVerification] = None
    ) -> Any:
        if on_invalid_key:
            return on_invalid_key(data, verification)

        return data

    def _on_exc(exc: Exception) -> Any:
        if on_exc:
            return on_exc(exc)

        raise exc

    def wrapper(
        func: CallableT[T],
    ) -> CallableT[Coroutine[Any, Any, VerificationResponseT[T]]]:
        @functools.wraps(func)
        async def inner(*args: Any, **kwargs: Any) -> VerificationResponseT[T]:
            try:
                if not (key := key_extractor(*args, **kwargs)):
                    message = "Failed to extract API key"
                    return _on_invalid_key({"code": None, "message": message})

                await _client.start()
                result = await _client.keys.verify_key(key, api_id)
                await _client.close()

                if result.is_err:
                    err = result.unwrap_err()
                    code = (err.code or models.ErrorCode.Unknown).value
                    return _on_invalid_key({"code": code, "message": err.message})

                verification = result.unwrap()
                kwargs["unkey_verification"] = verification

                if not verification.valid:
                    code = (verification.code or models.ErrorCode.Unknown).value
                    return _on_invalid_key(
                        {"code": code, "message": verification.error}, verification
                    )

                if inspect.iscoroutinefunction(func):
                    value = await func(*args, **kwargs)
                else:
                    value = func(*args, **kwargs)

            except Exception as exc:
                return _on_exc(exc)

            return value

        return inner

    return wrapper
