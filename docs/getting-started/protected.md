# The `protected` decorator

The [`protected`](/unkey.py/reference/decorators/#unkey.decorators.protected)
decorator is web framework agnostic and can be used to apply automatic api key
verification to your endpoints.

Check out how easily you can protect your endpoints using
[`protected`](/unkey.py/reference/decorators/#unkey.decorators.protected)!

---

## FastAPI

### Dependencies

- [unkey.py](https://pypi.org/project/unkey.py/)
- [fastapi](https://pypi.org/project/fastapi/)
- [uvicorn](https://pypi.org/project/uvicorn/)

### Example

```py
import os
from typing import Any, Dict, Optional

import fastapi
import unkey
import uvicorn

app = fastapi.FastAPI()


def key_extractor(*args: Any, **kwargs: Any) -> Optional[str]:
    if isinstance(auth := kwargs.get("authorization"), str):
        return auth.split(" ")[-1]

    return None


@app.get("/protected")
@unkey.protected(os.environ["UNKEY_API_ID"], key_extractor)
async def protected_route(
    *,
    authorization: str = fastapi.Header(None),
    unkey_verification: Any = None,
) -> Dict[str, Optional[str]]:
    assert isinstance(unkey_verification, unkey.ApiKeyVerification)
    assert unkey_verification.valid
    print(unkey_verification.owner_id)
    return {"message": "protected!"}


if __name__ == "__main__":
    uvicorn.run(app)
```

---

## Flask

### Dependencies

- [unkey.py](https://pypi.org/project/unkey.py/)
- [flask](https://pypi.org/project/flask/)

### Example

```py
import os
from typing import Any, Optional

import flask
import unkey
from flask.typing import ResponseReturnValue

app = flask.Flask(__name__)


def key_extractor(*args: Any, **kwargs: Any) -> Optional[str]:
    auth = flask.request.headers.get("authorization")
    if isinstance(auth, str):
        return auth.split(" ")[-1]

    return None


@app.get("/protected")
@unkey.protected(os.environ["UNKEY_API_ID"], key_extractor)
async def protected_route(
    *, unkey_verification: unkey.ApiKeyVerification
) -> ResponseReturnValue:
    assert unkey_verification.valid
    print(unkey_verification.owner_id)
    return {"message": "protected!"}


if __name__ == "__main__":
    app.run(port=8000, debug=True)
```

---

## Quart

### Dependencies

- [unkey.py](https://pypi.org/project/unkey.py/)
- [quart](https://pypi.org/project/quart/)

### Example

```py
import os
from typing import Any, Optional

import quart
import unkey

app = quart.Quart(__name__)


def key_extractor(*args: Any, **kwargs: Any) -> Optional[str]:
    auth = quart.request.headers.get("authorization")
    if isinstance(auth, str):
        return auth.split(" ")[-1]

    return None


@app.get("/protected")
@unkey.protected(os.environ["UNKEY_API_ID"], key_extractor)
async def protected_route(
    *, unkey_verification: unkey.ApiKeyVerification
) -> quart.Response:
    assert unkey_verification.valid
    print(unkey_verification.owner_id)
    return quart.jsonify(message="protected!")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
```

---

## Django

### Dependencies

- [unkey.py](https://pypi.org/project/unkey.py/)
- [django](https://pypi.org/project/django/)

### Example

```py
import os
import sys
from typing import Any, Dict, Optional

import unkey
from django.conf import settings
from django.urls import path
from django.core.management import execute_from_command_line
from django.http import JsonResponse, HttpRequest

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=sys.modules[__name__],
)


def key_extractor(*args: Any, **kwargs: Any) -> Optional[str]:
    if args and (auth := args[0].headers.get("authorization")):
        if isinstance(auth, str):
            return auth.split(" ")[-1]

    return None


def on_invalid_key(
    data: Dict[str, Optional[str]], verification: Optional[ApiKeyVerification]
) -> JsonResponse:
    response = {"error": "Key is invalid", **data}

    if verification:
        response["verification"] = verification.to_dict()

    return JsonResponse(response)


def on_exc(exc: Exception) -> JsonResponse:
    print(exc, file=sys.stderr)
    return JsonResponse({"error": "An unexpected error occurred"})


@unkey.protected(
    os.environ["UNKEY_API_ID"], key_extractor, on_invalid_key, on_exc
)
def protected_route(
    request: HttpRequest, *, unkey_verification: unkey.ApiKeyVerification
) -> JsonResponse:
    assert unkey_verification.valid
    print(unkey_verification.owner_id)
    return JsonResponse({"message": "protected!"})


urlpatterns = [path("protected", protected_route)]


if __name__ == "__main__":
    execute_from_command_line(sys.argv)
```
