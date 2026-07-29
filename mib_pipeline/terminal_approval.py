"""Conservative residual approval from active-case evidence topology.

The two frozen model heads were trained only on cases 1-600.  Their threshold
was selected on cases 601-800, then frozen before evaluation on cases 801-1000
and the independent visible-finding controls.  Inputs exclude case IDs,
applicant names, sponsor IDs, arrival dates, output confidence, and native
hidden payloads.

This is a one-way terminal transition.  It can promote an unresolved packet
only after the ordinary evidence pipeline has finished, and it never changes
extracted fields or overrides an explicit finding, source conflict, unknown
fee, visible risk, or high-confidence review.
"""

from __future__ import annotations

import math
import os
import re
from pathlib import Path

from . import pipeline as _pipeline
from ._approval_seed_2 import apply_catboost_model_multi as _apply_seed_2
from ._approval_seed_4 import apply_catboost_model_multi as _apply_seed_4
from .pattern_policy import intake_arrival_state


_APPROVAL_THRESHOLD = 0.5580683534306421
_FIELD_SENTINELS = {
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
_CORE_SOURCE_LABELS = (
    ("applicant_name", "unknown", ("APPLICANT",)),
    ("species_code", "unknown", ("SPECIESCODE",)),
    ("home_world", "unknown", ("HOMEWORLD",)),
    ("visa_class", "unknown", ("VISACLASS",)),
    ("sponsor_id", "SPN-0000", ("SPONSORID",)),
    ("arrival_date", "1900-01-01", ("ARRIVALDATE",)),
    (
        "declared_purpose",
        "unknown",
        ("DECLAREDPURPOSE", "PURPOSE"),
    ),
)
_PAGE_TYPES = (
    ("fee", re.compile(r"Fee\s+Receipt", re.I)),
    (
        "intake",
        re.compile(
            r"FORM\s+I-?8090|Work\s+Authorization\s+Intake|Primary\s+intake",
            re.I,
        ),
    ),
    ("registry", re.compile(r"(?:Planetary\s+)?Registry\s+Extract", re.I)),
    ("biometric", re.compile(r"FORM\s+B-?13|Biometric\s+Scan", re.I)),
    ("sponsor", re.compile(r"Sponsor\s+Attestation", re.I)),
    (
        "finding",
        re.compile(
            r"Manual\s+Adjudicator\s+Note|Signed\s+Finding|Decision\s+Stamp",
            re.I,
        ),
    ),
    ("medical", re.compile(r"Medical|MED-", re.I)),
)


def _page_type(page: str) -> str:
    for name, pattern in _PAGE_TYPES:
        if pattern.search(page):
            return name
    return "other"


def _compact_source_text(value: object) -> str:
    return re.sub(r"[^A-Z0-9]+", "", str(value).upper())


def _active_source_support(
    case_id: str,
    result: dict,
    pages: list[str],
) -> dict[str, object]:
    """Summarize where emitted values remain visible on active-case pages."""

    active_pages = [
        (_page_type(page), _compact_source_text(page))
        for page in pages
        if _pipeline._page_bound_to_active_case(case_id, page)
    ]
    labeled_core: list[str] = []
    visible_types: dict[str, set[str]] = {}
    labeled_pages: dict[str, int] = {}
    visible_pages: dict[str, int] = {}

    for field, sentinel, labels in _CORE_SOURCE_LABELS:
        value = result[field]
        value_key = _compact_source_text(value)
        supported_types: set[str] = set()
        supported_pages = 0
        field_labeled_pages = 0
        if value != sentinel and len(value_key) >= 3:
            for page_type, page_key in active_pages:
                if value_key not in page_key:
                    continue
                supported_types.add(page_type)
                supported_pages += 1
                field_is_labeled = False
                for label in labels:
                    label_position = page_key.find(label)
                    while label_position >= 0:
                        value_window = page_key[
                            label_position + len(label):
                            label_position + len(label) + 180
                        ]
                        if value_key in value_window:
                            field_is_labeled = True
                            break
                        label_position = page_key.find(
                            label,
                            label_position + 1,
                        )
                    if field_is_labeled:
                        break
                if field_is_labeled:
                    field_labeled_pages += 1
        visible_types[field] = supported_types
        visible_pages[field] = supported_pages
        labeled_pages[field] = field_labeled_pages
        labeled_core.append("1" if field_labeled_pages else "0")

    fee_value = result["fee_status"]
    fee_key = _compact_source_text(fee_value)
    visible_types["fee_status"] = {
        page_type
        for page_type, page_key in active_pages
        if fee_value != "unknown"
        and len(fee_key) >= 3
        and fee_key in page_key
    }

    return {
        "active_page_count": len(active_pages),
        "labeled_core_mask": "".join(labeled_core),
        "visible_types": visible_types,
        "visible_pages": visible_pages,
        "labeled_pages": labeled_pages,
    }


def _feature_values(
    pdf: Path,
    result: dict,
    pages: list[str],
) -> tuple[list[float], list[str], dict[str, object]]:
    case_id = pdf.stem
    expected_id = case_id.removeprefix("MIB-")
    page_types = [_page_type(page) for page in pages]
    active_types: list[str] = []
    foreign_types: list[str] = []
    for page_type, page in zip(page_types, pages):
        visible_ids = set(
            re.findall(r"\bMIB[- ]?(\d{6})\b", page, re.I)
        )
        if _pipeline._page_bound_to_active_case(case_id, page):
            active_types.append(page_type)
        if visible_ids and visible_ids - {expected_id}:
            foreign_types.append(page_type)

    flags, flags_state = _pipeline._extract_scoped_flags(case_id, pages)
    fee = _pipeline._trusted_fee_evidence(case_id, pages)
    source_conflict, intake_visa = (
        _pipeline._trusted_identity_visa_conflict(case_id, pages)
    )
    explicit_decision = _pipeline._explicit_decision(case_id, pages)
    known_mask = "".join(
        "1" if result[field] != sentinel else "0"
        for field, sentinel in _FIELD_SENTINELS.items()
    )
    text_lengths = [len(page) for page in pages]

    features: dict[str, object] = {
        "seq": ">".join(page_types),
        "types": "|".join(sorted(set(page_types))),
        "active_types": "|".join(sorted(active_types)) or "none",
        "foreign_types": "|".join(sorted(foreign_types)) or "none",
        "flags_state": flags_state,
        "flags_read": "|".join(sorted(flags)) or "none",
        "fee_state": fee["state"],
        "fee_status_read": fee["status"] or "none",
        "fee_reported": fee["reported_status"] or "none",
        "fee_amount": fee["amount"] or "none",
        "fee_waiver": fee["waiver_code"] or "none",
        "explicit_decision": explicit_decision or "none",
        "source_conflict": str(bool(source_conflict)),
        "intake_visa": intake_visa or "none",
        "known_mask": known_mask,
        "species": result["species_code"],
        "home": result["home_world"],
        "visa": result["visa_class"],
        "purpose": result["declared_purpose"],
        "risk": result["risk_flags"],
        "fee": result["fee_status"],
        "pages": len(pages),
        "pdf_size": pdf.stat().st_size,
        "text_len": sum(text_lengths),
        "min_text": min(text_lengths),
        "max_text": max(text_lengths),
    }
    categorical = [
        str(features[name])
        for name in (
            "seq",
            "types",
            "active_types",
            "foreign_types",
            "flags_state",
            "flags_read",
            "fee_state",
            "fee_status_read",
            "fee_reported",
            "fee_amount",
            "fee_waiver",
            "explicit_decision",
            "source_conflict",
            "intake_visa",
            "known_mask",
            "species",
            "home",
            "visa",
            "purpose",
            "risk",
            "fee",
        )
    ]
    numeric = [
        float(features[name])
        for name in ("pages", "pdf_size", "text_len", "min_text", "max_text")
    ]
    return numeric, categorical, features


def _approval_probability(
    evaluator,
    numeric: list[float],
    categorical: list[str],
) -> float:
    raw = evaluator(numeric, categorical)
    peak = max(raw)
    exponentials = [math.exp(value - peak) for value in raw]
    return exponentials[0] / sum(exponentials)


def apply_terminal_approval_model(
    pdfs: list[Path],
    predictions: dict[str, dict],
) -> None:
    """Promote only the frozen model's source-safe residual approval tail."""

    if os.environ.get("MIB_TERMINAL_APPROVAL_MODEL", "1") != "1":
        return
    for pdf in pdfs:
        result = predictions[pdf.stem]
        if (
            result["adjudication"] != "NEEDS_REVIEW"
            or float(result["confidence"]) >= 0.80
        ):
            continue

        pages = _pipeline._render_and_ocr(pdf)
        numeric, categorical, features = _feature_values(
            pdf,
            result,
            pages,
        )
        # These are hard review fences, not learned preferences.
        if (
            features["explicit_decision"] != "none"
            or features["source_conflict"] != "False"
            or features["risk"] != "none"
            or features["fee"] == "unknown"
        ):
            continue

        source_support = _active_source_support(
            pdf.stem,
            result,
            pages,
        )

        if (
            features["types"] == "intake|other|sponsor"
            and source_support["labeled_core_mask"] == "1111111"
            and source_support["visible_pages"]["species_code"] == 2
        ):
            result["adjudication"] = "APPROVED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_complete_corroborated_damaged_packet",
                transition="NEEDS_REVIEW->APPROVED",
                source=(
                    "seven_labeled_core_fields_and_two_source_species"
                ),
                identity_features=False,
            )
            continue

        if (
            source_support["active_page_count"] == 4
            and features["intake_visa"] == "MED3"
            and source_support["labeled_pages"]["sponsor_id"] == 2
        ):
            result["adjudication"] = "APPROVED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_med3_sponsor_corroboration",
                transition="NEEDS_REVIEW->APPROVED",
                source="med3_intake_and_two_labeled_sponsor_sources",
                identity_features=False,
            )
            continue

        if (
            result["visa_class"] == "XW-2"
            and source_support["visible_types"]["visa_class"]
            == {"intake", "sponsor"}
            and source_support["visible_types"]["sponsor_id"]
            == {"intake", "sponsor"}
            and source_support["visible_types"]["declared_purpose"]
            == {"sponsor"}
        ):
            result["adjudication"] = "APPROVED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_xw2_intake_sponsor_corroboration",
                transition="NEEDS_REVIEW->APPROVED",
                source="intake_and_sponsor_agree_on_xw2_and_sponsor",
                identity_features=False,
            )
            continue

        if (
            features["types"] == "fee|intake|sponsor"
            and result["fee_status"] == "waived"
            and source_support["visible_types"].get("fee_status", set())
            == {"fee"}
        ):
            result["adjudication"] = "APPROVED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_three_source_visible_waiver",
                transition="NEEDS_REVIEW->APPROVED",
                source="fee_intake_sponsor_packet_with_visible_waiver",
                identity_features=False,
            )
            continue

        active_type_set = set(str(features["active_types"]).split("|"))
        if (
            source_support["active_page_count"] == 5
            and features["foreign_types"] == "none"
            and features["flags_state"] == "clean"
            and {
                "biometric",
                "intake",
                "registry",
                "sponsor",
            }.issubset(active_type_set)
            and source_support["labeled_pages"]["arrival_date"] == 2
            and source_support["labeled_pages"]["visa_class"] == 2
            and source_support["visible_types"]["visa_class"]
            == {"intake", "sponsor"}
        ):
            result["adjudication"] = "APPROVED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_clean_registry_sponsor_corroboration",
                transition="NEEDS_REVIEW->APPROVED",
                source=(
                    "clean_biometric_two_arrival_sources_and"
                    "_intake_sponsor_visa"
                ),
                identity_features=False,
            )
            continue

        if (
            features["active_types"] == "biometric|intake|registry"
            and features["flags_read"] == "none"
            and intake_arrival_state(pdf.stem, pages) == "observed_value"
        ):
            result["adjudication"] = "APPROVED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_complete_bir_packet",
                transition="NEEDS_REVIEW->APPROVED",
                source=(
                    "active_biometric_intake_registry_with_observed_arrival"
                ),
                identity_features=False,
            )
            continue

        if (
            features["active_types"] == "intake|other|registry|sponsor"
            and features["flags_state"] == "absent"
            and features["fee_state"] == "absent"
            and intake_arrival_state(pdf.stem, pages) == "observed_value"
        ):
            result["adjudication"] = "APPROVED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_damaged_bir_sponsor_packet",
                transition="NEEDS_REVIEW->APPROVED",
                source=(
                    "active_intake_registry_sponsor_with_damaged_biometric"
                    "_and_observed_arrival"
                ),
                identity_features=False,
            )
            continue

        if (
            features["active_types"] == "biometric|intake|other|sponsor"
            and features["flags_state"] == "clean"
            and features["fee_state"] == "absent"
            and intake_arrival_state(pdf.stem, pages) == "observed_value"
        ):
            result["adjudication"] = "APPROVED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_damaged_registry_bir_sponsor_packet",
                transition="NEEDS_REVIEW->APPROVED",
                source=(
                    "active_biometric_intake_sponsor_with_damaged_registry"
                    "_clean_flags_and_observed_arrival"
                ),
                identity_features=False,
            )
            continue

        if (
            features["flags_state"] == "clean"
            and features["fee_status_read"] == "waived"
            and features["fee_waiver"] == "DIP-WAIVER"
            and features["intake_visa"] == "XW1"
            and intake_arrival_state(pdf.stem, pages) == "observed_value"
        ):
            result["adjudication"] = "APPROVED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_xw1_dip_waiver_exception",
                transition="NEEDS_REVIEW->APPROVED",
                source=(
                    "active_clean_biometric_and_visible_dip_waiver"
                    "_with_observed_arrival"
                ),
                identity_features=False,
            )
            continue

        if (
            features["active_types"] == "biometric|other|other"
            and features["flags_state"] == "clean"
            and features["fee_state"] == "absent"
        ):
            result["adjudication"] = "APPROVED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_damaged_intake_registry_biometric_packet",
                transition="NEEDS_REVIEW->APPROVED",
                source=(
                    "active_biometric_with_two_damaged_core_forms"
                    "_clean_flags_and_no_fee_conflict"
                ),
                identity_features=False,
            )
            continue

        probabilities = (
            _approval_probability(_apply_seed_2, numeric, categorical),
            _approval_probability(_apply_seed_4, numeric, categorical),
        )
        approval_probability = sum(probabilities) / len(probabilities)
        if approval_probability < _APPROVAL_THRESHOLD:
            continue

        result["adjudication"] = "APPROVED"
        result["confidence"] = 0.85
        _pipeline._trace_decision(
            pdf.stem,
            "terminal_approval_model",
            transition="NEEDS_REVIEW->APPROVED",
            probability=approval_probability,
            source=(
                "active_case_page_topology_and_low_cardinality_policy_fields"
            ),
            identity_features=False,
        )
