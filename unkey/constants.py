from __future__ import annotations

from typing import Final

import unkey

__all__ = ()

API_BASE_URL: Final[str] = "https://api.unkey.dev"
USER_AGENT: Final[str] = f"unkey.py v{unkey.__version__}"

GET: Final[str] = "GET"
PUT: Final[str] = "PUT"
POST: Final[str] = "POST"
PATCH: Final[str] = "PATCH"
DELETE: Final[str] = "DELETE"
