from __future__ import annotations

import platform
from pathlib import Path

from unkey import __git_sha__
from unkey import __version__


def _main() -> None:
    """Prints package/system info and exits."""
    path = Path(__file__).parent.absolute()
    py_impl = platform.python_implementation()
    py_ver = platform.python_version()
    py_c = platform.python_compiler()
    p = platform.uname()

    print(f"unkey.py v{__version__} from {__git_sha__}")
    print(f"@ {path}")
    print(f"{py_impl} {py_ver} {py_c}")
    print(f"{p.system} {p.node} {p.release} {p.machine}")
    print(p.version)


if __name__ == "__main__":
    _main()
