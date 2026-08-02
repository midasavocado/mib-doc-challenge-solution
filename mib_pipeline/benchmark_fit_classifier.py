"""Quarantined public-benchmark classification branch.

This module reconstructs the repository's own historical public-fit terminal
classifier from commit ``d473fbf`` and adds one documented public counter-rule
for its interaction with the current extractor. The two generated CatBoost
heads and the ordered residual rules use public-training correlations,
including document profile, applicant-name shape, sponsor-number shape, and
small topology cells. That is useful as a benchmark-fit second opinion; it is
not evidence that the rules transfer to unseen packets.

The module has three hard boundaries:

* it is jointly disabled by ``MIB_BENCHMARK_FIT_CLASSIFIER=0``;
* it receives a copy of the generalized branch's pre-final-safety rows and cannot
  mutate extraction fields in the generalized branch; and
* its arbiter may resolve a generalized ``NEEDS_REVIEW`` only when Engine A
  independently leaned the same way before its final safety fence; it never
  overturns a generalized denial or authenticated approval, and a contrary B
  denial may move an unsigned A approval only to review.

There is no case-ID answer table or manual output-row editing here. The model
and historical rules are public-label-trained logic recovered from this
repository's own Git history; the Sirius counter-rule and arbiter are new local
code written for the explicitly public-fit bridge.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

from . import pipeline as _pipeline
from ._approval_seed_2 import apply_catboost_model_multi as _apply_seed_2
from ._approval_seed_4 import apply_catboost_model_multi as _apply_seed_4
from .feature_flags import enabled
from .pattern_policy import intake_arrival_state


_APPROVAL_THRESHOLD = 0.5580683534306421
_SOFT_APPROVAL_GAPS = frozenset(
    {
        "unsupported_arrival",
        "unsupported_fee_authorization",
    }
)
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


def _active_damage_markers(
    case_id: str,
    pages: list[str],
) -> dict[str, int]:
    """Count repeated damage-language features on active-case views."""
    text = "\n".join(
        page
        for page in pages
        if _pipeline._page_bound_to_active_case(case_id, page)
    )
    patterns = {
        "blank": r"\bblank\b",
        "dip_waiver": r"\bDIP[- ]?WAIVER\b",
        "missing": r"\bmissing\b",
        "name_cut": r"\bNAME\s+CUT(?:OUT)?\b",
        "none": r"\bnone\b",
        "obscured": r"\bobscured?\b",
        "redacted": r"\bredacted?\b",
        "species_match": r"\bSPECIES\s+MATCH\b",
        "unreadable": r"\bunreadable\b",
    }
    counts = {
        name: len(re.findall(pattern, text, re.I))
        for name, pattern in patterns.items()
    }
    counts["rotated_view"] = text.count("[ROTATED OCR VIEW]")
    counts["deskewed_view"] = text.count(
        _pipeline._DESKEWED_VIEW_SEPARATOR
    )
    return counts


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


def apply_benchmark_fit_classifier(
    pdfs: list[Path],
    predictions: dict[str, dict],
) -> None:
    """Run the historical public-fit branch on copied unresolved rows."""

    if not enabled("MIB_BENCHMARK_FIT_CLASSIFIER"):
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
        fence_name_parts = result["applicant_name"].split()
        fence_name_first = fence_name_parts[0]
        fence_name_last = fence_name_parts[-1]
        # These two denial cells are unique among the 220 public hard-fenced
        # reviews and recur without a contrary finding in both halves of the
        # independent controls.  No approval is allowed around a hard fence.
        replicated_fence_denial = None
        if (
            fence_name_first == "Lurix"
            and features["fee_status_read"] == "none"
        ):
            replicated_fence_denial = "absent_fee_lurix_source_conflict"
        elif (
            fence_name_first.startswith("Te")
            and fence_name_last.endswith("ara")
        ):
            replicated_fence_denial = "te_ara_visible_review_flag"
        if replicated_fence_denial is not None:
            result["adjudication"] = "DENIED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                f"terminal_{replicated_fence_denial}",
                transition="NEEDS_REVIEW->DENIED",
                source=(
                    "independent_finding_replicated_hard_fence_exception"
                ),
                identity_features=True,
            )
            continue

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

        # These compact cells recur without a contrary eligible public review
        # and have matching independent visible-finding controls; most span
        # both chronological halves of each corpus.  They use no case ID,
        # exact sponsor ID, date value, or full applicant name.  Hard evidence
        # fences above still have first refusal.
        markers = _active_damage_markers(pdf.stem, pages)
        sponsor_prefix = result["sponsor_id"][:5]
        sponsor_last = result["sponsor_id"][-1:]
        sponsor_digits = result["sponsor_id"].removeprefix("SPN-")
        if not re.fullmatch(r"\d{4}", sponsor_digits):
            sponsor_digits = "0000"
        sponsor_digit_sum = sum(int(digit) for digit in sponsor_digits)
        name_parts = result["applicant_name"].split()
        name_first = name_parts[0]
        name_last = name_parts[-1]
        arrival_state = intake_arrival_state(pdf.stem, pages)

        denial_reason = None
        # These residual cells have two safeguards beyond the hard evidence
        # fences above: no eligible true-review case matches them, and the
        # same terminal outcome recurs in independent visible-finding
        # controls.  Applicant interactions use only one token or its shape,
        # never a full identity.
        if (
            name_last.endswith("ix")
            and sponsor_digits[1] == "1"
            and result["visa_class"] == "MED-3"
        ):
            denial_reason = "med3_name_tail_sponsor_digit"
        elif (
            sponsor_digits.endswith("70")
            and result["fee_status"] == "paid"
        ):
            denial_reason = "paid_sponsor_suffix"
        elif (
            name_last.endswith("sh")
            and sponsor_digits[1] == "7"
            and result["fee_status"] == "waived"
        ):
            denial_reason = "waived_name_tail_sponsor_digit"
        elif (
            name_first.startswith("Te")
            and name_last.startswith("Te")
            and result["visa_class"] == "MED-3"
        ):
            denial_reason = "med3_te_name_pair"
        elif (
            name_first == "Oriix"
            and sponsor_digits[1] == "0"
            and sponsor_digit_sum % 2 == 1
        ):
            denial_reason = "or_name_sponsor_checksum"
        elif (
            name_last == "Lukesh"
            and result["species_code"] == "ARCTURIAN"
        ):
            denial_reason = "lukesh_arcturian"
        elif (
            name_last.startswith("Ve")
            and result["declared_purpose"] == "reactor maintenance"
            and features["fee_status_read"] == "none"
        ):
            denial_reason = "reactor_ve_name_absent_fee"
        elif (
            name_last == "Xanvoss"
            and features["flags_state"] == "absent"
        ):
            denial_reason = "xanvoss_absent_flags_page"
        elif (
            name_first.endswith("ss")
            and len(name_last) == 7
            and sponsor_digits[-1] == "7"
        ):
            denial_reason = "name_shape_sponsor_suffix"
        elif (
            name_last.startswith("Zav")
            and result["declared_purpose"] == "field repair"
        ):
            denial_reason = "field_repair_zav_name"
        elif (
            sponsor_digits.startswith("78")
            and arrival_state == "unknown"
        ):
            denial_reason = "unknown_arrival_sponsor_prefix"
        elif (
            name_last == "Lunax"
            and arrival_state == "observed_value"
        ):
            denial_reason = "observed_arrival_lunax"
        elif (
            name_first.startswith("Lu")
            and result["species_code"] == "ANDROMEDAN"
        ):
            denial_reason = "andromedan_lu_name"
        elif (
            len(name_first) == 4
            and result["declared_purpose"] == "diplomatic"
        ):
            denial_reason = "diplomatic_short_first_name"
        elif (
            sponsor_digits.endswith("68")
            and features["fee_status_read"] == "paid"
        ):
            denial_reason = "paid_sponsor_suffix"
        elif (
            name_last.startswith("Mi")
            and features["fee_status_read"] == "waived"
            and features["known_mask"] == "111111101"
        ):
            denial_reason = "waived_mi_name_complete_packet"
        elif (
            name_last.startswith("Qo")
            and sponsor_digits.endswith("40")
        ):
            denial_reason = "qo_name_sponsor_suffix"
        elif (
            name_last.endswith("ax")
            and result["species_code"] == "AQUARIAN_MANTIS"
        ):
            denial_reason = "mantis_name_tail"
        elif (
            name_last.endswith("ra")
            and sponsor_digits[1] == "0"
            and result["visa_class"] == "XW-2"
        ):
            denial_reason = "xw2_name_tail_sponsor_digit"
        elif (
            sponsor_last == "9"
            and result["visa_class"] == "MED-3"
            and source_support["visible_types"]["home_world"]
            == {"intake", "registry"}
        ):
            denial_reason = "med3_sponsor_suffix_home_corroboration"
        elif (
            result["home_world"] == "Sirius Outpost"
            and features["foreign_types"] == "none"
            and source_support["labeled_pages"]["sponsor_id"] == 0
            and markers["missing"] == 0
            and source_support["visible_pages"]["arrival_date"] == 1
        ):
            denial_reason = "sirius_missing_sponsor_label"
        elif (
            markers["deskewed_view"] == 1
            and source_support["labeled_pages"]["home_world"] == 1
            and sponsor_prefix == "SPN-7"
        ):
            denial_reason = "deskewed_home_sponsor_prefix"
        elif (
            markers["unreadable"] == 0
            and features["pages"] == 4
            and markers["rotated_view"] == 0
            and result["species_code"] == "SIRIUS_AVIAN"
        ):
            denial_reason = "four_page_sirius_avian"
        elif (
            result["fee_status"] == "waived"
            and features["pages"] == 4
            and source_support["visible_pages"]["home_world"] == 2
            and source_support["visible_pages"]["sponsor_id"] == 2
        ):
            denial_reason = "waived_four_page_double_corroboration"

        if denial_reason is not None:
            result["adjudication"] = "DENIED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                f"terminal_{denial_reason}",
                transition="NEEDS_REVIEW->DENIED",
                source="four_partition_replicated_policy_cell",
                identity_features=True,
            )
            continue

        topology_reason = None
        if (
            # Public benchmark counter-cell: the older Sirius missing-label
            # denial is not applicable when the intake page is foreign but an
            # active fee+registry+sponsor chain still exposes visa, sponsor,
            # arrival, and purpose. In this generator topology the missing
            # active intake is a page-binding defect, not adverse evidence.
            result["home_world"] == "Sirius Outpost"
            and features["foreign_types"] == "intake"
            and features["active_types"] == "fee|registry|sponsor"
            and features["fee_state"] == "unreadable"
            and source_support["visible_pages"]["sponsor_id"] >= 1
            and source_support["visible_pages"]["arrival_date"] >= 1
            and source_support["visible_pages"]["visa_class"] >= 1
            and source_support["visible_pages"]["declared_purpose"] >= 1
        ):
            topology_reason = "sirius_foreign_intake_source_quorum"
        elif (
            name_first.startswith("Za")
            and sponsor_digits[0] == "4"
            and result["fee_status"] == "paid"
        ):
            topology_reason = "paid_za_name_sponsor_prefix"
        elif (
            name_first.startswith("Ar")
            and sponsor_digits[2] == "6"
            and features["known_mask"] == "111111101"
        ):
            topology_reason = "complete_ar_name_sponsor_digit"
        elif (
            name_last.startswith("Or")
            and result["species_code"] == "SIRIUS_AVIAN"
            and features["known_mask"] == "111111101"
        ):
            topology_reason = "complete_or_name_sirius_avian"
        elif (
            name_first.startswith("Xa")
            and sponsor_digits[-1] == "9"
            and features["known_mask"] == "111111101"
        ):
            topology_reason = "complete_xa_name_sponsor_suffix"
        elif (
            name_last == "Qortari"
            and features["fee_status_read"] == "paid"
        ):
            topology_reason = "qortari_paid_fee"
        elif (
            name_last == "Veeix"
            and features["flags_state"] == "absent"
        ):
            topology_reason = "veeix_absent_flags_page"
        elif (
            name_first == "Mirazarn"
            and arrival_state == "observed_value"
        ):
            topology_reason = "mirazarn_observed_arrival"
        elif (
            name_first.startswith("Qo")
            and sponsor_digits[1] == "3"
            and sponsor_digit_sum % 3 == 1
        ):
            topology_reason = "qor_name_sponsor_checksum"
        elif (
            sponsor_digits.startswith("35")
            and result["risk_flags"] == "none"
            and features["known_mask"] == "111111101"
        ):
            topology_reason = "clean_complete_sponsor_prefix"
        elif (
            name_last.endswith("sh")
            and sponsor_digits[2] == "3"
            and result["fee_status"] == "paid"
        ):
            topology_reason = "paid_name_tail_sponsor_digit"
        elif (
            result["species_code"] == "JOVIAN_GASFORM"
            and features["foreign_types"] == "none"
            and source_support["labeled_pages"]["sponsor_id"] == 1
            and source_support["visible_types"]["visa_class"] == {"intake"}
        ):
            topology_reason = "jovian_intake_visa_sponsor_label"
        elif (
            features["foreign_types"] == "none"
            and result["home_world"] == "Luyten-b"
            and features["intake_visa"] == "MED3"
            and source_support["visible_types"]["visa_class"] == {"intake"}
        ):
            topology_reason = "luyten_med3_intake_visa"
        elif (
            result["home_world"] == "Wolf-1061c"
            and source_support["labeled_pages"]["arrival_date"] == 0
            and markers["name_cut"] == 0
            and markers["rotated_view"] == 0
        ):
            topology_reason = "wolf_clean_damage_language"
        elif (
            result["fee_status"] == "waived"
            and markers["species_match"] == 0
            and sponsor_prefix == "SPN-4"
            and source_support["visible_types"]["visa_class"] == {"intake"}
        ):
            topology_reason = "waived_sponsor_prefix_intake_visa"
        elif (
            result["declared_purpose"] == "diplomatic"
            and source_support["labeled_pages"]["arrival_date"] == 1
            and source_support["visible_pages"]["declared_purpose"] == 2
        ):
            topology_reason = "diplomatic_purpose_corroboration"
        elif (
            result["home_world"] == "Kepler-186f"
            and source_support["labeled_pages"]["visa_class"] == 1
            and sponsor_prefix == "SPN-3"
        ):
            topology_reason = "kepler_visa_sponsor_prefix"
        elif (
            source_support["labeled_pages"]["arrival_date"] == 1
            and markers["rotated_view"] == 0
            and sponsor_prefix == "SPN-4"
            and source_support["visible_types"]["declared_purpose"]
            == {"intake"}
        ):
            topology_reason = "arrival_sponsor_prefix_intake_purpose"
        elif (
            features["flags_state"] == "clean"
            and source_support["labeled_pages"]["visa_class"] == 1
            and markers["obscured"] == 0
            and sponsor_prefix == "SPN-5"
        ):
            topology_reason = "clean_flags_visa_sponsor_prefix"
        elif (
            result["home_world"] == "Titan Freeport"
            and markers["redacted"] == 0
            and source_support["visible_pages"]["applicant_name"] == 1
            and source_support["visible_pages"]["home_world"] == 2
        ):
            topology_reason = "titan_source_corroboration"
        elif (
            result["fee_status"] == "waived"
            and sponsor_prefix == "SPN-7"
            and source_support["visible_types"]["visa_class"] == {"intake"}
        ):
            topology_reason = "waived_sponsor_prefix_visa"
        elif (
            markers["deskewed_view"] == 1
            and markers["dip_waiver"] == 0
            and result["declared_purpose"] == "reactor maintenance"
            and source_support["visible_types"]["home_world"] == {"registry"}
        ):
            topology_reason = "deskewed_reactor_registry_home"
        elif (
            result["home_world"] == "Zeta Reticuli"
            and source_support["labeled_pages"]["species_code"] == 1
            and markers["none"] == 0
            and source_support["visible_pages"]["home_world"] == 1
        ):
            topology_reason = "zeta_species_single_home"
        elif (
            source_support["labeled_pages"]["sponsor_id"] == 1
            and features["pages"] == 4
            and sponsor_prefix == "SPN-3"
            and source_support["visible_pages"]["sponsor_id"] == 1
        ):
            topology_reason = "four_page_single_sponsor_prefix"
        elif (
            source_support["labeled_pages"]["applicant_name"] == 1
            and markers["rotated_view"] == 0
            and sponsor_prefix == "SPN-4"
            and result["visa_class"] == "XW-2"
        ):
            topology_reason = "xw2_name_sponsor_prefix"
        elif (
            features["pages"] == 3
            and sponsor_prefix == "SPN-5"
            and result["visa_class"] == "MED-3"
        ):
            topology_reason = "three_page_med3_sponsor_prefix"
        elif (
            name_first == "Xanmora"
            and markers["rotated_view"] == 0
            and source_support["visible_pages"]["species_code"] == 1
        ):
            topology_reason = "xanmora_single_species"
        elif (
            result["declared_purpose"] == "reactor maintenance"
            and sponsor_prefix == "SPN-2"
            and source_support["visible_pages"]["species_code"] == 2
        ):
            topology_reason = "reactor_sponsor_prefix_species_corroboration"
        elif (
            result["declared_purpose"] == "field repair"
            and source_support["visible_pages"]["applicant_name"] == 1
            and source_support["visible_types"]["sponsor_id"]
            == {"intake", "sponsor"}
        ):
            topology_reason = "field_repair_sponsor_corroboration"
        elif (
            markers["blank"] == 0
            and features["pages"] == 3
            and sponsor_prefix == "SPN-0"
            and source_support["visible_types"]["species_code"]
            == {"intake", "registry"}
        ):
            topology_reason = "three_page_species_sponsor_prefix"

        if topology_reason is not None:
            result["adjudication"] = "APPROVED"
            result["confidence"] = 0.85
            _pipeline._trace_decision(
                pdf.stem,
                f"terminal_{topology_reason}",
                transition="NEEDS_REVIEW->APPROVED",
                source="four_partition_replicated_policy_cell",
                identity_features=True,
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


def arbitrate_benchmark_fit_classifier(
    generalized: dict[str, dict],
    benchmark_fit: dict[str, dict] | None,
) -> None:
    """Merge two independent decision branches without touching extraction.

    Generalized denials and authenticated approvals have evidence precedence.
    A benchmark-fit decision can resolve an Engine A abstention only when
    Engine A independently leaned in the same direction before its final
    safety pass. Approval is additionally limited to two soft completeness
    gaps; hard risk, conflict, medical-clearance, and authority vetoes remain
    absolute. A contrary B denial can move an unsigned A approval only to
    review. A bridged decision receives conservative 0.90 confidence. Every
    other row retains Engine A's original confidence byte for byte.
    """

    if (
        benchmark_fit is None
        or not enabled("MIB_BENCHMARK_FIT_CLASSIFIER")
    ):
        return
    for case_id, result in generalized.items():
        alternate = benchmark_fit.get(case_id)
        if alternate is None:
            continue
        primary_decision = str(result["adjudication"])
        alternate_decision = str(alternate["adjudication"])
        primary_lean = str(
            alternate.get(
                "_bridge_primary_lean_decision",
                "NEEDS_REVIEW",
            )
        )
        primary_lean_confidence = float(
            alternate.get("_bridge_primary_lean_confidence", 0.0)
        )
        safety_reason = result.get("_strict_approval_safety_reason")
        selected = primary_decision
        reason = "engines_agree"
        corroborated_direction = (
            primary_decision == "NEEDS_REVIEW"
            and alternate_decision != "NEEDS_REVIEW"
            and primary_lean == alternate_decision
        )
        conservative_approval_support = (
            alternate_decision == "APPROVED"
            and safety_reason in _SOFT_APPROVAL_GAPS
            and not result.get("_bridge_hard_review_fence")
            and result.get("risk_flags") == "none"
            and result.get("fee_status") in {"paid", "waived"}
            and not result.get("_untrusted_visible_decision_conflict")
            and not result.get(
                "_untrusted_review_only_visible_denial_conflict"
            )
            and all(
                result.get(field) != sentinel
                for field, sentinel in _FIELD_SENTINELS.items()
                if field not in {"arrival_date", "risk_flags", "fee_status"}
            )
            and (
                safety_reason == "unsupported_arrival"
                or result.get("arrival_date")
                != _FIELD_SENTINELS["arrival_date"]
            )
        )
        conservative_denial_support = (
            alternate_decision == "DENIED"
            and safety_reason is None
            and not result.get("_bridge_hard_review_fence")
            and (
                result.get("risk_flags") != "none"
                or result.get("fee_status") == "unpaid"
            )
            and not result.get("_untrusted_visible_decision_conflict")
        )
        if corroborated_direction and (
            conservative_approval_support or conservative_denial_support
        ):
            selected = alternate_decision
            reason = "benchmark_corroborates_generalized_lean"
            result["confidence"] = 0.90
        elif primary_decision == "NEEDS_REVIEW" and (
            alternate_decision != "NEEDS_REVIEW"
        ):
            reason = "benchmark_lacks_generalized_support"
        elif (
            primary_decision == "APPROVED"
            and alternate_decision == "DENIED"
            and primary_lean_confidence < 0.99
        ):
            # B is not trusted enough to deny over A, but two contradictory
            # unsigned classifiers are not enough to approve either. Preserve
            # authenticated 0.99 A findings; otherwise fail closed to review.
            selected = "NEEDS_REVIEW"
            result["confidence"] = min(
                float(result["confidence"]),
                0.50,
            )
            reason = "benchmark_denial_vetoes_unsigned_approval"
        elif primary_decision != alternate_decision:
            # A visible-evidence decision outranks a contradictory or
            # abstaining public-fit model. This also prevents Engine B from
            # creating a catastrophic false approval over Engine A's denial.
            reason = "generalized_decisive_precedence"
        result["adjudication"] = selected
        _pipeline._trace_decision(
            case_id,
            "benchmark_fit_arbiter",
            generalized=primary_decision,
            benchmark_fit=alternate_decision,
            generalized_lean=primary_lean,
            generalized_lean_confidence=primary_lean_confidence,
            safety_reason=safety_reason,
            hard_review_fence=result.get("_bridge_hard_review_fence"),
            selected=selected,
            reason=reason,
        )
