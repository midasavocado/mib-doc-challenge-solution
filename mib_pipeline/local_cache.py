"""Small, fail-open local cache for expensive PDF-derived evidence."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import threading
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any


_STATS: Counter[str] = Counter()
_STATS_LOCK = threading.Lock()


@lru_cache(maxsize=1)
def _cache_root() -> Path | None:
    if os.environ.get("MIB_LOCAL_CACHE", "1") != "1":
        return None
    configured = os.environ.get("MIB_LOCAL_CACHE_DIR")
    if configured:
        root = Path(configured).expanduser()
    elif sys.platform == "darwin":
        root = Path.home() / "Library" / "Caches" / "mib-doc-challenge"
    else:
        root = (
            Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
            / "mib-doc-challenge"
        )
    try:
        root.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    return root


@lru_cache(maxsize=8192)
def _pdf_digest(path: str, size: int, mtime_ns: int) -> str:
    del size, mtime_ns
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _entry_path(pdf: Path, namespace: str, schema: str) -> Path | None:
    root = _cache_root()
    if root is None:
        return None
    try:
        stat = pdf.stat()
        pdf_hash = _pdf_digest(
            str(pdf.resolve()),
            stat.st_size,
            stat.st_mtime_ns,
        )
    except OSError:
        return None
    key = hashlib.sha256(
        f"{namespace}\0{schema}\0{pdf_hash}".encode("utf-8")
    ).hexdigest()
    safe_namespace = re.sub(r"[^a-zA-Z0-9_.-]+", "-", namespace)
    return root / safe_namespace / key[:2] / f"{key}.json"


def _record(namespace: str, outcome: str) -> None:
    with _STATS_LOCK:
        _STATS[f"{namespace}_{outcome}"] += 1


def load_json(pdf: Path, namespace: str, schema: str) -> Any | None:
    """Return a valid cached payload, or None on any miss or cache failure."""
    path = _entry_path(pdf, namespace, schema)
    if path is None:
        _record(namespace, "miss")
        return None
    try:
        envelope = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        _record(namespace, "miss")
        return None
    if (
        not isinstance(envelope, dict)
        or envelope.get("schema") != schema
        or "payload" not in envelope
    ):
        _record(namespace, "miss")
        return None
    _record(namespace, "hit")
    return envelope["payload"]


def store_json(
    pdf: Path,
    namespace: str,
    schema: str,
    payload: Any,
) -> None:
    """Atomically cache one JSON payload; silently continue if unavailable."""
    path = _entry_path(pdf, namespace, schema)
    if path is None:
        return
    temporary: Path | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.stem}-",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(
                {"schema": schema, "payload": payload},
                handle,
                ensure_ascii=False,
                separators=(",", ":"),
            )
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        _record(namespace, "write")
    except (OSError, TypeError, ValueError):
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass


def cache_stats() -> dict[str, int]:
    with _STATS_LOCK:
        return dict(_STATS)
