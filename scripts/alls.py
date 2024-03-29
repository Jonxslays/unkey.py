import sys
import typing as t

import unkey


_IGNORE = ("annotations", "protected")


def should_include_module(module: str) -> bool:
    if module in _IGNORE:
        return False

    if (char := module[0]) == "_":
        return False

    if char.upper() == char:
        return False

    return True


def get_modules() -> t.List[str]:
    return [m for m in unkey.__dict__ if should_include_module(m)]


def get_alls() -> t.Tuple[t.Set[str], t.Set[str]]:
    modules = get_modules()
    return (
        set(item for module in modules for item in unkey.__dict__[module].__all__),
        set(i for i in unkey.__all__ if i not in modules),
    )


def validate_alls() -> None:
    modules, lib = get_alls()
    err = None

    if missing := modules - lib:
        err = "Missing exported items at top level:\n" + "\n".join(f" - {m}" for m in missing)
        print(err, file=sys.stderr)

    if missing := lib - modules:
        err = "Missing exported items at module level:\n" + "\n".join(f" - {m}" for m in missing)
        print(err, file=sys.stderr)

    if err:
        sys.exit(1)


if __name__ == "__main__":
    validate_alls()
