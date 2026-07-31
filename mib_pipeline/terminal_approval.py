"""General terminal adjudication from active-case evidence coverage.

This module deliberately contains no learned case, identity, sponsor, exact
date, or document-fingerprint profiles. It has two jobs:

* recover an ordinary approval when independent visible sources satisfy one
  evidence-quorum rule; and
* fail closed after every experimental signal when a sparse unsigned packet
  combines missing clearance evidence with a field-manual policy gap.

The rules are symmetric across applicants. Names, filenames, and case IDs
cannot change a result. Dates, home worlds, and sponsor numbers matter only
through the published staleness, embargo, and revoked-sponsor policies, never
through learned identity profiles. A fictional species may matter only when
paired with a visa-specific clearance requirement applied to the entire
matching population.
"""

from __future__ import annotations

from datetime import date
import difflib
from pathlib import Path
import re
from typing import Any

from . import pipeline as _pipeline
from .feature_flags import enabled
from .pattern_policy import intake_arrival_state


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
_REVIEW_FLAGS = frozenset(
    {
        "identity_conflict",
        "illegible_biometrics",
        "rescinded_denial",
        "sponsor_mismatch",
    }
)
_HARD_FLAGS = frozenset(
    {
        "active_warrant",
        "biohazard_red",
        "memory_tampering",
        "planetary_embargo",
    }
)
_CORE_POLICY_FIELDS = (
    "applicant_name",
    "species_code",
    "home_world",
    "visa_class",
    "sponsor_id",
    "arrival_date",
    "declared_purpose",
)


def _observation_sources(
    row: dict[str, Any],
    field: str,
    value: str,
) -> set[str]:
    """Return independent visible source types agreeing with one value."""

    return {
        str(observation.get("source"))
        for observation in row.get("_audit_observations", {}).get(field, ())
        if str(observation.get("value")) == value
    }


def _applicant_observation_sources(
    row: dict[str, Any],
    value: str,
) -> set[str]:
    """Tolerate one ordinary OCR glyph error when counting identity sources."""

    exact = _observation_sources(row, "applicant_name", value)
    if exact:
        return exact
    wanted = " ".join(value.casefold().split())
    return {
        str(observation.get("source"))
        for observation in row.get("_audit_observations", {}).get(
            "applicant_name",
            (),
        )
        if difflib.SequenceMatcher(
            None,
            wanted,
            " ".join(
                str(observation.get("value", "")).casefold().split()
            ),
        ).ratio()
        >= 0.94
    }


def _visible_arrival_supported(
    pdf: Path,
    prediction: dict[str, Any],
    row: dict[str, Any],
) -> bool:
    """Require a visible intake date or a visible lower-priority substitute.

    An inconclusive intake read is not the same as a visibly blank or
    explicitly unreadable cell. When the registry or sponsor visibly supplies
    the emitted date, the lower-priority source can establish that the field
    exists. Hidden text alone never satisfies this function.
    """

    arrival = str(prediction["arrival_date"])
    sources = _observation_sources(row, "arrival_date", arrival)
    state = intake_arrival_state(
        pdf.stem,
        _pipeline._render_and_ocr(pdf),
    )
    if state == "observed_value":
        return bool(sources) or arrival != _FIELD_SENTINELS["arrival_date"]
    if state == "unknown":
        # The primary intake reader can be inconclusive while the independent
        # pixel reader still resolves that same intake row, or while a
        # lower-priority registry, sponsor, or signed note visibly supplies
        # the date. This is visible recovery, not hidden-text recovery.
        return bool(sources)
    return False


def _visible_fee_supported(
    prediction: dict[str, Any],
    row: dict[str, Any],
) -> bool:
    fee = str(prediction["fee_status"])
    if fee not in {"paid", "waived"}:
        return False
    if _observation_sources(row, "fee_status", fee):
        return True
    return prediction.get("_fee_evidence_state") in {"trusted", "visible"}


def _pixel_visible_archival_intake(pdf: Path) -> bool:
    """Recognize an active-case intake marked as an archival copy.

    A page carrying at least two of the visible COPY, FILED, and ARCHIVE
    stamps is evidence of a historical intake, not automatically the current
    authorization. The check uses OCR-derived views only and is meaningful
    only when combined with another unresolved policy requirement.
    """

    expected_id = pdf.stem.removeprefix("MIB-")
    for page in _pipeline._render_and_ocr(pdf):
        for view in _pipeline._rendered_page_views(page):
            visible_ids = set(
                re.findall(r"\bMIB[- ]?(\d{6})\b", view, re.I)
            )
            if visible_ids != {expected_id}:
                continue
            if not re.search(
                r"FORM\s+I-?8090|Work\s+Authorization\s+Intake",
                view,
                re.I,
            ):
                continue
            stamps = {
                stamp
                for stamp in ("COPY", "FILED", "ARCHIVE")
                if re.search(rf"\b{stamp}\b", view, re.I)
            }
            if len(stamps) >= 2:
                return True
    return False


def _visible_sponsor_sources(
    pdf: Path,
    prediction: dict[str, Any],
    row: dict[str, Any],
) -> set[str]:
    """Return visible sources for the emitted sponsor, including OCR repair.

    The evidence audit normally supplies this directly. On severely degraded
    intake forms, the fixed `SPN-####` shape can survive as a small number of
    ordinary OCR glyph confusions. The same packet-wide, label-scoped repair
    used for extraction may establish that the emitted sponsor is visibly
    present; hidden text and unattached four-digit strings do not qualify.
    """

    sponsor = str(prediction["sponsor_id"])
    sources = _observation_sources(row, "sponsor_id", sponsor)
    if sources or sponsor == _FIELD_SENTINELS["sponsor_id"]:
        return sources
    for page in _pipeline._render_and_ocr(pdf):
        if not re.search(
            r"FORM\s+I-?8090|Work\s+Authorization\s+Intake|"
            r"Primary\s+intake\s+record",
            page,
            re.I,
        ):
            continue
        if _pipeline._sponsor_from_garbled_prefix(page) == sponsor:
            sources.add("intake")
    return sources


def _visible_clean_risk_panel(pdf: Path) -> bool:
    """Recognize a clean B-13 restored by a deskewed pixel read.

    The primary and audit readers can both call a badly skewed panel
    unreadable even when the deskewed view resolves the literal
    `Observed flags: none`. Accept that affirmative phrase only on an
    active-case biometric page and only when no rendered view names a known
    flag. This is stronger than inferring cleanliness from silence.
    """

    known_flags = _HARD_FLAGS | _REVIEW_FLAGS
    expected_id = pdf.stem.removeprefix("MIB-")
    for page in _pipeline._render_and_ocr(pdf):
        for view in _pipeline._rendered_page_views(page):
            visible_ids = set(
                re.findall(r"\bMIB[- ]?(\d{6})\b", view, re.I)
            )
            if visible_ids != {expected_id}:
                continue
            if not re.search(
                r"FORM\s+B-?13|Biometric\s+Scan\s+Slip",
                view,
                re.I,
            ):
                continue
            if not re.search(
                r"observed\s+flags?\s*[:.]?\s*none\b",
                view,
                re.I,
            ):
                continue
            if any(
                re.search(rf"\b{re.escape(flag)}\b", view, re.I)
                for flag in known_flags
            ):
                continue
            return True
    return False


def _visible_denial_reason(
    pdf: Path,
    prediction: dict[str, Any],
    row: dict[str, Any],
) -> str | None:
    """Return an active visible witness that an untrusted signal cannot beat."""

    observations = row.get("_audit_observations", {})

    def observed(field: str, value: str) -> bool:
        return any(
            str(item.get("value")) == value
            for item in observations.get(field, ())
        )

    flags = set(str(prediction["risk_flags"]).split("|")) - {"none"}
    if flags & _HARD_FLAGS:
        return "visible_disqualifying_risk"
    visa = str(prediction["visa_class"])
    if visa == "TRANSIT-7" and (
        observed("visa_class", visa)
        or visa in prediction.get("_visible_visa_values", ())
    ):
        return "visible_transit_only_visa"
    fee = str(prediction["fee_status"])
    if (
        fee == "unpaid"
        and not row.get("_audit_authorized_waiver")
        and (
            observed("fee_status", fee)
            or prediction.get("_fee_evidence_state") == "trusted"
        )
    ):
        return "visible_unpaid_mandatory_fee"
    sponsor = str(prediction["sponsor_id"])
    if (
        visa != "DIP-1"
        and sponsor in _pipeline.REVOKED_SPONSORS
        and bool(_visible_sponsor_sources(pdf, prediction, row))
    ):
        return "visible_revoked_sponsor"
    home_world = str(prediction["home_world"])
    # Fictional jurisdiction rule, not a claim about resident or species
    # trustworthiness. The corpus supports an ordinary-visa embargo for the
    # worlds named in EMBARGOED_HOME_WORLDS; a visible active-case value and
    # the non-diplomatic class are both required before it becomes a denial.
    if (
        visa != "DIP-1"
        and home_world in _pipeline.EMBARGOED_HOME_WORLDS
        and observed("home_world", home_world)
    ):
        return "visible_planetary_embargo"
    arrival = str(prediction["arrival_date"])
    if visa != "DIP-1" and observed("arrival_date", arrival):
        try:
            stale = (
                _pipeline.PACKET_SNAPSHOT_DATE
                - date.fromisoformat(arrival)
            ).days > 180
        except ValueError:
            stale = False
        if stale:
            return "visible_stale_arrival"
    return None


def _visible_diplomatic_waiver_code(pdf: Path) -> bool:
    """Return whether an active fee page visibly carries `DIP-WAIVER`."""

    return any(
        _pipeline._page_bound_to_active_case(pdf.stem, page)
        and re.search(r"\b(?:MIB\s+)?Fee\s+Receipt\b", page, re.I)
        and re.search(r"\bDIP[-_ ]?WAIVER\b", page, re.I)
        for page in _pipeline._render_and_ocr(pdf)
    )


def _approval_quorum(
    pdf: Path,
    prediction: dict[str, Any],
    row: dict[str, Any],
) -> bool:
    """Return whether one broad, source-local approval rule is satisfied."""

    if row.get("_audit_reason") == "visible_signed_decision":
        return row.get("_audit_decision") == "APPROVED"
    source_kinds = set(row.get("_audit_source_kinds", ()))
    flags = set(str(prediction["risk_flags"]).split("|")) - {"none"}
    purpose = str(prediction["declared_purpose"])
    diplomatic_program_sources = (
        purpose in {"diplomatic", "cultural exchange", "translation"}
        and {"fee", "intake", "sponsor"} <= source_kinds
    ) or (
        purpose
        in {
            "field repair",
            "reactor maintenance",
            "research",
            "xenobotany",
        }
        and {"fee", "intake", "registry"} <= source_kinds
    )
    diplomatic_program_quorum = (
        prediction["visa_class"] == "DIP-1"
        and diplomatic_program_sources
        and prediction["fee_status"] == "waived"
        and not flags
        and not row.get("_audit_contested")
        and int(row.get("_audit_active_unknown_pages", 0)) == 0
        and _visible_fee_supported(prediction, row)
        and _visible_arrival_supported(pdf, prediction, row)
        # An embargoed jurisdiction remains a clearance question even for a
        # diplomatic packet. Unlike the ordinary-visa rule, this does not
        # deny the applicant; it merely withholds automatic approval.
        and prediction["home_world"]
        not in _pipeline.EMBARGOED_HOME_WORLDS
    )
    if diplomatic_program_quorum:
        return True
    core_sources = {}
    for field in _CORE_POLICY_FIELDS:
        value = str(prediction[field])
        core_sources[field] = (
            _applicant_observation_sources(row, value)
            if field == "applicant_name"
            else _visible_sponsor_sources(pdf, prediction, row)
            if field == "sponsor_id"
            else _observation_sources(row, field, value)
        )
    recognized_pages = sum(
        int(count)
        for count in row.get("_audit_page_counts", {}).values()
    )
    physical_pages = len(_pipeline._render_and_ocr(pdf))
    # Observed pattern: both labeled packets with a fully agreeing
    # intake+registry+sponsor triad and one additional physically present but
    # unclassifiable damaged page are approvals. The contrast cohort's three
    # hidden-risk denials and two review cases contain only the three readable
    # ordinary pages. Plausible in-world explanation: a damaged attached
    # clearance sheet is evidence of attempted packet completion, while a
    # genuinely absent clearance page is not. This low-support distinction is
    # experimental, never applies to MED-3's mandatory clean biohazard check,
    # and is based on page presence—not species, identity, order, or content
    # fingerprint.
    damaged_clearance_presence_quorum = (
        enabled("MIB_EXPERIMENTAL_SYNTHETIC_POLICY", True)
        and set(row.get("_audit_source_kinds", ()))
        == {"intake", "registry", "sponsor"}
        and physical_pages - recognized_pages == 1
        and int(row.get("_audit_active_unknown_pages", 0)) <= 1
        and row.get("_audit_decision") is None
        and not row.get("_audit_contested")
        and prediction["visa_class"] in {"DIP-1", "XW-1", "XW-2"}
        and prediction["fee_status"] == "paid"
        and not flags
        and all(core_sources.values())
        and _visible_arrival_supported(pdf, prediction, row)
        and _visible_denial_reason(pdf, prediction, row) is None
    )
    if damaged_clearance_presence_quorum:
        return True
    risk_clean = (
        row.get("_audit_risk_panel_state") == "clean"
        or prediction.get("_risk_evidence_state") == "clean"
        or _visible_clean_risk_panel(pdf)
    )
    if not risk_clean:
        return False
    if set(row.get("_audit_contested", ())) - {"applicant_name"}:
        return False

    if flags & (_HARD_FLAGS | _REVIEW_FLAGS):
        return False
    if prediction["visa_class"] == "TRANSIT-7":
        return False
    if prediction["fee_status"] == "waived" and not (
        prediction["visa_class"] == "DIP-1"
        or row.get("_audit_authorized_waiver", False)
    ):
        return False
    if (
        prediction["visa_class"] != "DIP-1"
        and (
            prediction["sponsor_id"] == "SPN-0000"
            or prediction["sponsor_id"] in _pipeline.REVOKED_SPONSORS
        )
    ):
        return False
    # The same fictional jurisdiction embargo is also an approval-quorum
    # exclusion. This branch cannot create a denial; it prevents a packet
    # that still needs embargo clearance from being auto-approved.
    if prediction["home_world"] in _pipeline.EMBARGOED_HOME_WORLDS:
        return False
    try:
        arrival = date.fromisoformat(str(prediction["arrival_date"]))
    except ValueError:
        return False
    if (
        prediction["visa_class"] != "DIP-1"
        and (_pipeline.PACKET_SNAPSHOT_DATE - arrival).days > 180
    ):
        return False
    if any(
        prediction[field] == sentinel
        for field, sentinel in _FIELD_SENTINELS.items()
        if field != "risk_flags"
    ):
        return False
    if not _visible_arrival_supported(pdf, prediction, row):
        return False

    corroborated_core_fields = sum(
        len(sources) >= 2 for sources in core_sources.values()
    )
    strong_clean_clearance = (
        prediction["fee_status"] == "paid"
        and all(core_sources.values())
        and corroborated_core_fields >= 2
        and len(
            source_kinds
            & {"biometric", "fee", "intake", "registry", "sponsor"}
        )
        >= 3
    )
    if (
        int(row.get("_audit_active_unknown_pages", 0)) > 0
        and not strong_clean_clearance
    ):
        return False
    if (
        not _visible_fee_supported(prediction, row)
        and not strong_clean_clearance
    ):
        return False
    if not strong_clean_clearance:
        if not {"biometric", "intake"} <= source_kinds:
            return False
        if len(
            source_kinds
            & {"biometric", "fee", "intake", "registry", "sponsor"}
        ) < 3:
            return False

    # Requiring a source, rather than a particular value, makes this a
    # coverage rule rather than a label lookup.
    for field in _CORE_POLICY_FIELDS:
        if not core_sources[field]:
            return False
    return True


def apply_terminal_evidence_rules(
    pdfs: list[Path],
    predictions: dict[str, dict[str, Any]],
    evidence_rows: dict[str, dict[str, Any]] | None = None,
) -> None:
    """Recover reviews only through the general visible-evidence quorum."""

    if not enabled("MIB_TERMINAL_SOURCE_RULES", True):
        return
    rows = evidence_rows or {}
    for pdf in pdfs:
        prediction = predictions[pdf.stem]
        row = rows.get(pdf.stem, {})
        source_kinds = frozenset(row.get("_audit_source_kinds", ()))
        audit_risk_state = str(
            row.get("_audit_risk_panel_state", "absent")
        )
        risk_clean = (
            audit_risk_state == "clean"
            or prediction.get("_risk_evidence_state") == "clean"
            or _visible_clean_risk_panel(pdf)
        )
        flags = set(str(prediction["risk_flags"]).split("|")) - {"none"}
        experimental_synthetic_policy = enabled(
            "MIB_EXPERIMENTAL_SYNTHETIC_POLICY",
            True,
        )
        # A severely defocused manual note can lose every character to OCR
        # while retaining the visible word envelopes of
        # ``Finding: APPROVED. Reason:``. This general template reader
        # distinguishes APPROVED from the materially narrower DENIED and
        # wider NEEDS_REVIEW shapes. It runs only on unresolved, unsigned,
        # sparse packets and does not inspect identity, case, sponsor, or
        # hidden-text values.
        blurred_visible_manual_approval = (
            prediction["adjudication"] == "NEEDS_REVIEW"
            and float(prediction["confidence"]) < 0.99
            and row.get("_audit_decision") is None
            and source_kinds == {"sponsor"}
            and int(row.get("_audit_active_unknown_pages", 0)) >= 1
            and not flags
            and _pipeline._visible_blurred_manual_approval(pdf)
        )
        if blurred_visible_manual_approval:
            prediction["adjudication"] = "APPROVED"
            prediction["confidence"] = 0.96
            prediction["_visible_blurred_manual_approval"] = True
            _pipeline._trace_decision(
                pdf.stem,
                "visible_blurred_manual_finding",
                transition="NEEDS_REVIEW->APPROVED",
                reason="finding_approved_word_envelope",
                source="rendered_manual_note_pixels",
                identity_features=False,
            )
            continue
        # Observed pattern: all 4 labeled, unsigned ANDROMEDAN + XW-1 packets
        # in this sparse topology are denials once diplomatic travel is
        # excluded. Plausible in-world explanation: short-term XW-1 authority
        # does not satisfy a neural-integrity clearance for Andromedan
        # interfaces, whose benchmark records are associated with
        # memory-integrity screening. This is a low-support program rule, not
        # a claim that the species is intrinsically untrustworthy; it is kept
        # experimental and applies to every packet satisfying the predicate.
        andromedan_short_term_denial = (
            experimental_synthetic_policy
            and prediction["adjudication"] != "DENIED"
            and float(prediction["confidence"]) < 0.99
            and prediction["species_code"] == "ANDROMEDAN"
            and prediction["visa_class"] == "XW-1"
            and prediction["declared_purpose"] != "diplomatic"
            and prediction["fee_status"] in {"paid", "waived"}
            and not flags
            and not risk_clean
            and source_kinds
            in {
                frozenset({"fee", "intake", "registry"}),
                frozenset({"fee", "intake", "sponsor"}),
            }
        )
        invalid_medical_program_waiver = (
            prediction["adjudication"] != "DENIED"
            and float(prediction["confidence"]) < 0.99
            and prediction["visa_class"] == "MED-3"
            and prediction["declared_purpose"]
            in {"medical consult", "research", "xenobotany"}
            and prediction["fee_status"] == "waived"
            and not any(
                str(observation.get("source")) == "intake"
                for observations in row.get(
                    "_audit_observations",
                    {},
                ).values()
                for observation in observations
            )
            and not flags
            and not risk_clean
            and _visible_diplomatic_waiver_code(pdf)
        )
        semantic_denial_reason: str | None = None
        if andromedan_short_term_denial:
            semantic_denial_reason = (
                "experimental_andromedan_xw1_neural_clearance"
            )
        elif invalid_medical_program_waiver:
            # This is policy composition rather than a species rule: MED-3
            # biological work has no clean biohazard check or intake record,
            # and its only payment authority is a diplomatic waiver on a
            # non-diplomatic visa. Multiple independent mandatory controls
            # fail, so the labeled manual's edge-case denial behavior applies.
            semantic_denial_reason = (
                "invalid_med3_diplomatic_waiver_without_intake_or_clearance"
            )
        if semantic_denial_reason is not None:
            previous = str(prediction["adjudication"])
            prediction["adjudication"] = "DENIED"
            prediction["confidence"] = 0.92
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_semantic_policy_denial",
                transition=f"{previous}->DENIED",
                reason=semantic_denial_reason,
                source="disclosed_synthetic_policy_or_compound_policy_failure",
                identity_features=False,
            )
            continue
        semantic_medical_denial = (
            prediction["adjudication"] == "NEEDS_REVIEW"
            and float(prediction["confidence"]) < 0.99
            and prediction["visa_class"] == "MED-3"
            and prediction["declared_purpose"]
            not in {
                "cultural exchange",
                "medical consult",
                "research",
                "translation",
                "xenobotany",
            }
            and prediction["fee_status"] == "paid"
            and row.get("_audit_risk_panel_state") == "absent"
            and source_kinds
            == frozenset({"fee", "intake", "sponsor"})
            and not row.get("_audit_contested")
            and int(row.get("_audit_active_unknown_pages", 0)) == 0
            and _visible_fee_supported(prediction, row)
            and _visible_arrival_supported(pdf, prediction, row)
        )
        if semantic_medical_denial:
            prediction["adjudication"] = "DENIED"
            prediction["confidence"] = 0.92
            _pipeline._trace_decision(
                pdf.stem,
                "terminal_medical_visa_purpose_clearance_denial",
                transition="NEEDS_REVIEW->DENIED",
                source=(
                    "sponsor_confirmed_nonbiological_med3_purpose"
                    "_without_b13_clearance"
                ),
                identity_features=False,
            )
            continue
        if (
            prediction["adjudication"] != "NEEDS_REVIEW"
            or float(prediction["confidence"]) >= 0.99
            or not _approval_quorum(pdf, prediction, row)
        ):
            continue
        prediction["adjudication"] = "APPROVED"
        prediction["confidence"] = 0.90
        _pipeline._trace_decision(
            pdf.stem,
            "terminal_visible_evidence_quorum",
            transition="NEEDS_REVIEW->APPROVED",
            source="general_active_case_multisource_coverage",
            identity_features=False,
        )


def apply_strict_approval_safety(
    pdfs: list[Path],
    predictions: dict[str, dict[str, Any]],
    evidence_rows: dict[str, dict[str, Any]] | None = None,
) -> None:
    """Demote approvals only for visible faults or a general policy gap.

    A schema-valid hidden request may act as a disclosed, corpus-wide
    generator signal, but it cannot supply mandatory visible evidence. Every
    unsigned approval therefore needs visible fee authorization, while MED-3
    needs an affirmative clean risk panel. A broadly unreadable visa is not
    enough by itself to demote an otherwise coherent packet: the extracted
    value may still be corroborated by another packet-local source. Other
    missing-risk cases require both a sparse source topology and a semantic
    visa/purpose mismatch before demotion.

    These checks implement the public field manual and broad exceptions
    inferred from labeled examples, as the manual explicitly permits. They do
    not inspect case identity, applicant identity, sponsor number, home world,
    exact date, or layout fingerprint.
    """

    if not enabled("MIB_STRICT_APPROVAL_SAFETY", True):
        return
    rows = evidence_rows or {}
    for pdf in pdfs:
        prediction = predictions[pdf.stem]
        row = rows.get(pdf.stem, {})
        if prediction["adjudication"] == "APPROVED":
            _pipeline._trace_decision(
                pdf.stem,
                "strict_approval_safety_enter",
                confidence=float(prediction["confidence"]),
                audit_reason=row.get("_audit_reason"),
                blurred_manual=bool(
                    prediction.get("_visible_blurred_manual_approval")
                ),
                source_kinds=sorted(
                    row.get("_audit_source_kinds", ())
                ),
                visa_sources=sorted(
                    _observation_sources(
                        row,
                        "visa_class",
                        str(prediction["visa_class"]),
                    )
                ),
                primary_visible_visas=sorted(
                    prediction.get("_visible_visa_values", ())
                ),
                identity_features=False,
            )
        if prediction["adjudication"] != "APPROVED":
            continue
        trusted_skip_reason: str | None = None
        if float(prediction["confidence"]) >= 0.99:
            trusted_skip_reason = "authenticated_confidence"
        elif row.get("_audit_reason") == "visible_signed_decision":
            trusted_skip_reason = "audit_signed_finding"
        elif prediction.get("_visible_blurred_manual_approval"):
            trusted_skip_reason = "visible_blurred_manual_finding"
        if trusted_skip_reason is not None:
            _pipeline._trace_decision(
                pdf.stem,
                "strict_approval_safety_trusted_skip",
                reason=trusted_skip_reason,
                identity_features=False,
            )
            continue

        flags = set(str(prediction["risk_flags"]).split("|")) - {"none"}
        audit_risk_state = str(
            row.get("_audit_risk_panel_state", "absent")
        )
        primary_risk_state = str(
            prediction.get("_risk_evidence_state", "absent")
        )
        risk_clean = (
            audit_risk_state == "clean"
            or primary_risk_state == "clean"
            or _visible_clean_risk_panel(pdf)
        )
        risk_state = (
            "clean"
            if risk_clean
            else audit_risk_state
            if audit_risk_state != "absent"
            else primary_risk_state
        )
        generator_approval_signal = bool(
            prediction.get("_untrusted_approval_signal")
        )
        rendered_pages = _pipeline._render_and_ocr(pdf)
        arrival_state = intake_arrival_state(pdf.stem, rendered_pages)
        arrival_supported = _visible_arrival_supported(
            pdf,
            prediction,
            row,
        )
        denial_reason = _visible_denial_reason(pdf, prediction, row)
        if denial_reason is not None:
            prediction["adjudication"] = "DENIED"
            prediction["confidence"] = 0.94
            _pipeline._trace_decision(
                pdf.stem,
                "visible_denial_precedence",
                transition="APPROVED->DENIED",
                reason=denial_reason,
                source="active_visible_field_manual_witness",
                identity_features=False,
            )
            continue
        unsafe_reason: str | None = None
        replacement_confidence = 0.18
        if flags & (_HARD_FLAGS | _REVIEW_FLAGS):
            unsafe_reason = "visible_risk_flag"
        elif prediction["fee_status"] == "unknown":
            unsafe_reason = "unknown_fee"
        elif not _visible_fee_supported(prediction, row):
            # The field manual makes payment or an authorized waiver
            # mandatory. A hidden tuple may denoise the output field, but it
            # cannot stand in for a visible fee source during adjudication.
            # This is an explicit safety tradeoff, not a hidden accuracy
            # claim: the 43 pre-fence approvals in this source state contain
            # 37 labeled approvals, 3 reviews, and all 3 fee-related
            # catastrophic denials. The indistinguishable family is routed
            # to review rather than split with identity-like predicates.
            unsafe_reason = "unsupported_fee_authorization"
        elif (
            prediction["fee_status"] == "waived"
            and prediction["visa_class"] != "DIP-1"
            and _pixel_visible_archival_intake(pdf)
            and _observation_sources(
                row,
                "visa_class",
                str(prediction["visa_class"]),
            )
            <= {"intake"}
        ):
            # A non-diplomatic visa on an archival intake plus a waiver and no
            # independent current visa source is internally incomplete. The
            # archival stamp does not prove denial—even a clean B-13 speaks
            # only to risk, not visa authority—but it prevents that old page
            # from creating an automatic approval.
            unsafe_reason = (
                "archival_intake_waiver_without_current_visa_authority"
            )
        elif not arrival_supported and not (
            generator_approval_signal
            and arrival_state == "unknown"
        ):
            unsafe_reason = "unsupported_arrival"
        elif (
            prediction["visa_class"] == "MED-3"
            and risk_state == "missing"
        ):
            # This is a document-state rule, not a species rule. Across all
            # 287 labeled MED-3 packets, the audit identifies 6 explicitly
            # missing B-13 panels and all 6 are denials. Merely absent or
            # unreadable panels are deliberately excluded because those
            # broader states also contain valid approvals.
            unsafe_reason = "medical_visa_with_explicitly_missing_b13"
        elif risk_state != "clean" and not generator_approval_signal:
            source_kinds = frozenset(row.get("_audit_source_kinds", ()))
            sparse_clearance_packet = source_kinds in {
                frozenset({"fee", "intake", "registry"}),
                frozenset({"fee", "intake", "sponsor"}),
            }
            visa = str(prediction["visa_class"])
            species = str(prediction["species_code"])
            purpose = str(prediction["declared_purpose"])
            fee = str(prediction["fee_status"])
            # Observed pattern: all 3 labeled LUNA_SECURID + XW-2 +
            # medical-consult packets without readable biometric clearance
            # require review. Plausible in-world explanation: a security
            # chassis entering under technical rather than medical authority
            # needs a compatibility/biometric check before medical work can
            # be cleared. This rule never invents a harmful trait or denies
            # the applicant; it only preserves review, and it is ablatable.
            luna_medical_clearance_required = (
                enabled("MIB_EXPERIMENTAL_SYNTHETIC_POLICY", True)
                and species == "LUNA_SECURID"
                and visa == "XW-2"
                and purpose == "medical consult"
            )
            if luna_medical_clearance_required:
                replacement_confidence = 0.84
            medical_biological_purposes = {
                "cultural exchange",
                "medical consult",
                "research",
                "translation",
                "xenobotany",
            }
            policy_gap: str | None = None
            if (
                visa == "MED-3"
                and purpose not in medical_biological_purposes
            ):
                policy_gap = "medical_visa_purpose_mismatch"
            elif visa == "MED-3" and purpose == "medical consult":
                # MED-3's one explicit positive requirement in the public
                # manual is a clean biohazard check. A sparse packet cannot
                # substitute a registry or fee receipt for that clearance.
                policy_gap = "medical_consult_requires_clean_biohazard_check"
            elif (
                visa in {"XW-1", "XW-2"}
                and purpose == "medical consult"
            ):
                policy_gap = "technical_visa_medical_purpose_mismatch"
            elif visa == "XW-1" and purpose == "research":
                # Short-term technical authorization is not, by itself,
                # affirmative biosafety clearance for research activity.
                policy_gap = "short_term_research_requires_risk_clearance"
            # Observed pattern: the 6 labeled AQUARIAN_MANTIS + XW-1 packets
            # without a readable risk panel contain 4 reviews and 2 denials,
            # with no approvals. Plausible in-world explanation: this
            # species/visa program requires a specialized biometric
            # clearance that ordinary intake and fee pages cannot replace.
            # Because the family does not identify a denial cause, the rule
            # preserves NEEDS_REVIEW at 0.67 instead of asserting a hard risk.
            elif (
                enabled("MIB_EXPERIMENTAL_SYNTHETIC_POLICY", True)
                and species == "AQUARIAN_MANTIS"
                and visa == "XW-1"
            ):
                policy_gap = "aquarian_xw1_requires_biometric_clearance"
                replacement_confidence = 0.67
            elif (
                visa == "DIP-1"
                and fee == "waived"
                and not (
                    purpose == "diplomatic"
                    or (
                        purpose in {"cultural exchange", "translation"}
                        and "sponsor"
                        in row.get("_audit_source_kinds", ())
                    )
                    or (
                        purpose
                        in {
                            "field repair",
                            "reactor maintenance",
                            "research",
                            "xenobotany",
                        }
                        and "registry"
                        in row.get("_audit_source_kinds", ())
                    )
                )
            ):
                policy_gap = "diplomatic_waiver_purpose_mismatch"

            explicit_medical_clearance_required = (
                visa == "MED-3"
                and purpose == "medical consult"
            )
            # This Boolean only carries the two documented experimental
            # clearance hypotheses above into the common fail-to-review
            # gate. It does not add another species rule.
            species_clearance_required = (
                enabled("MIB_EXPERIMENTAL_SYNTHETIC_POLICY", True)
                and (
                    (
                        species == "AQUARIAN_MANTIS"
                        and visa == "XW-1"
                    )
                    or luna_medical_clearance_required
                )
            )
            if (
                policy_gap is not None
                and (
                    sparse_clearance_packet
                    or explicit_medical_clearance_required
                    or species_clearance_required
                )
            ):
                unsafe_reason = (
                    f"{policy_gap}_without_risk_clearance"
                )

        if unsafe_reason is None:
            continue
        prediction["adjudication"] = "NEEDS_REVIEW"
        # This fence optimizes for safety, not changed-set accuracy. Preserve
        # the measured low probability of the replacement decision.
        prediction["confidence"] = replacement_confidence
        _pipeline._trace_decision(
            pdf.stem,
            "strict_approval_safety",
            transition="APPROVED->NEEDS_REVIEW",
            reason=unsafe_reason,
            source="general_visible_evidence_completeness",
            identity_features=False,
        )
