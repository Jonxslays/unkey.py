from __future__ import annotations

from typing import Final

__packagename__: Final[str] = "unkey.py"
__version__: Final[str] = "0.2.0"
__author__: Final[str] = "Jonxslays"
__copyright__: Final[str] = "2023-present Jonxslays"
__description__: Final[str] = "An asynchronous Python SDK for unkey.dev."
__url__: Final[str] = "https://github.com/Jonxslays/unkey.py"
# __docs__: Final[str] = "https://jonxslays.github.io/unkey.py"
__repository__: Final[str] = __url__
__license__: Final[str] = "GPL-3.0"
__git_sha__: Final[str] = "[HEAD]"

from . import client
from . import constants
from . import errors
from . import models
from . import result
from . import routes
from . import serializer
from . import services
from .client import *
from .errors import *
from .models import *
from .result import *
from .routes import *
from .serializer import *
from .services import *

__all__ = (
    "client",
    "constants",
    "errors",
    "models",
    "result",
    "routes",
    "serializer",
    "services",
    "ApiKey",
    "BaseEnum",
    "BaseError",
    "BaseModel",
    "BaseService",
    "Client",
    "CompiledRoute",
    "Err",
    "HttpErrorResponse",
    "HttpService",
    "KeyService",
    "Ok",
    "RateLimit",
    "RateLimitType",
    "Result",
    "Route",
    "Serializer",
    "UnwrapError",
)
