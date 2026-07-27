"""Identity-free confidence blend (calibration only — never changes adjudication).

Blends the model’s raw confidence with a frozen Laplace reliability table keyed
by ``(adjudication, fee_known, missing_field_count)``. Table was fit with
5-fold OOF on public train so keys are identity-free.

Disable with ``MIB_CONFIDENCE_BLEND=0``.
"""

from __future__ import annotations

import json
import os
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping

from .models import PredictionRow

_ARTIFACT = (
    Path(__file__).resolve().parent / "artifacts" / "arjun_confidence_blend.json"
)

_DEFAULTS = {
    "applicant_name": "unknown",
    "species_code": "unknown",
    "home_world": "unknown",
    "visa_class": "unknown",
    "sponsor_id": "SPN-0000",
    "arrival_date": "1900-01-01",
    "declared_purpose": "unknown",
    "risk_flags": "none",
    "fee_status": "unknown",
}


def _missing_count(row: PredictionRow, defaults: Mapping[str, str]) -> int:
    payload = row.to_dict()
    return sum(1 for field, default in defaults.items() if payload.get(field) == default)


def _lookup_key(row: PredictionRow, defaults: Mapping[str, str]) -> str:
    fee = "fee" if row.fee_status != "unknown" else "nofee"
    if row.adjudication == "NEEDS_REVIEW":
        return f"NEEDS_REVIEW|{fee}|m{min(_missing_count(row, defaults), 4)}"
    return f"{row.adjudication}|{fee}"


def _load_artifact(path: Path = _ARTIFACT) -> dict[str, Any]:
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError("confidence blend artifact must be an object")
    table = payload.get("table")
    if not isinstance(table, dict) or not table:
        raise ValueError("confidence blend table missing")
    blend = float(payload.get("blend", 0.3))
    if not 0.0 <= blend <= 1.0:
        raise ValueError("confidence blend out of range")
    defaults = payload.get("defaults_for_missing_count") or _DEFAULTS
    return {"table": table, "blend": blend, "defaults": defaults}


def apply_confidence_blend(
    row: PredictionRow,
    *,
    artifact_path: Path | None = None,
) -> PredictionRow:
    """Blend raw confidence toward the frozen reliability table.

    Never mutates adjudication or any field other than ``confidence``.
    """

    flag = os.environ.get("MIB_CONFIDENCE_BLEND", "1").strip().lower()
    if flag in {"0", "false", "no", "off"}:
        return row

    try:
        artifact = _load_artifact(artifact_path or _ARTIFACT)
    except (OSError, ValueError, json.JSONDecodeError):
        return row

    key = _lookup_key(row, artifact["defaults"])
    mapped = artifact["table"].get(key)
    if mapped is None:
        return row
    blend = float(artifact["blend"])
    raw = float(row.confidence)
    blended = (1.0 - blend) * raw + blend * float(mapped)
    blended = max(0.05, min(0.99, blended))
    if abs(blended - raw) < 1e-12:
        return row
    return replace(row, confidence=blended)
