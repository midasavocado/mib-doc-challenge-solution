"""Validated runtime feature switches for the evidence-only pipeline."""

from __future__ import annotations

import os


_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off"}


def _read_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default

    normalized = value.strip().casefold()
    if normalized in _TRUE:
        return True
    if normalized in _FALSE:
        return False
    raise ValueError(
        f"{name} must be one of {sorted(_TRUE | _FALSE)}, got {value!r}"
    )


def enabled(name: str, default: bool = True) -> bool:
    """Return a validated boolean feature flag."""

    return _read_bool(name, default)


def runtime_mode() -> str:
    """Return the only supported adjudication mode."""

    return "evidence-only"
