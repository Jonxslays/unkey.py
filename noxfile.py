from __future__ import annotations

import functools
from typing import Callable
from pathlib import Path

import nox
import toml

SessionT = Callable[[nox.Session], None]
InjectorT = Callable[[SessionT], SessionT]


def parse_dependencies() -> dict[str, str]:
    data = toml.load("pyproject.toml")["tool"]["poetry"]
    deps: dict[str, str | dict[str, str]] = {
        **data["dependencies"],
        **data["group"]["dev"]["dependencies"],
    }

    for k, v in deps.items():
        if isinstance(v, dict):
            deps[k] = v["version"]

    return {k.lower(): f"{k}{v}" for k, v in deps.items()}


DEPS = parse_dependencies()


def install(*packages: str) -> InjectorT:
    def inner(func: SessionT) -> SessionT:
        @functools.wraps(func)
        def wrapper(session: nox.Session) -> None:
            try:
                session.install("-U", *(DEPS[p] for p in packages))
            except KeyError as e:
                session.error(f"Invalid package install - {e}")
            return func(session)

        return wrapper

    return inner


@nox.session(reuse_venv=True)
@install("pytest", "pytest-asyncio", "pytest-testdox", "coverage", "aiohttp", "attrs")
def tests(session: nox.Session) -> None:
    session.run(
        "coverage",
        "run",
        "--omit",
        "tests/*",
        "-m",
        "pytest",
        "--testdox",
        "--log-level=INFO",
    )


@nox.session(reuse_venv=True)
@install("coverage")
def coverage(session: nox.Session) -> None:
    if not Path(".coverage").exists():
        session.skip("Skipping coverage")

    session.run("coverage", "report", "-m")


@nox.session(reuse_venv=True)
@install("pyright", "mypy", "aiohttp", "attrs")
def types(session: nox.Session) -> None:
    session.run("mypy")
    session.run("pyright")


@nox.session(reuse_venv=True)
@install("black", "len8")
def formatting(session: nox.Session) -> None:
    session.run("black", ".", "--check")
    session.run("len8")


@nox.session(reuse_venv=True)
@install("flake8", "isort")
def imports(session: nox.Session) -> None:
    session.run("isort", "unkey", "tests", "-cq", "-s", "__init__.py")
    session.run(
        "flake8",
        "unkey",
        "tests",
        "--select",
        "F4",
        "--extend-ignore",
        "E,F",
        "--extend-exclude",
        "__init__.py",
    )


@nox.session(reuse_venv=True)
def alls(session: nox.Session) -> None:
    session.install(".")
    session.run("python", "scripts/alls.py")
