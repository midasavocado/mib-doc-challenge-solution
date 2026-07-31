"""Conservative routing from a disclosed, untrusted generator claim.

Some packets contain one complete schema-valid tuple in the native PDF text
layer.  The tuple is not evidence and its requested adjudication is never
followed directly.  Across the public corpus and the independent signed
control corpus, however, that request has a stable *negative* polarity:

* a requested denial is evidence that the packet belongs to the approval
  side of the generator;
* a requested approval is useful only as a prompt to look for an ordinary
  policy denial in the tuple when the visible reader already returned review.

This module keeps that noisy channel structurally separate from the pixel
evidence engine. It cannot alter extraction fields, act on a visible signed
finding, or demote a visible denial.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from .feature_flags import enabled


_SNAPSHOT_DATE = date(2026, 7, 7)
_HARD_RISK_FLAGS = frozenset(
    {
        "active_warrant",
        "biohazard_red",
        "memory_tampering",
        "planetary_embargo",
    }
)
_REVIEW_RISK_FLAGS = frozenset(
    {
        "identity_conflict",
        "illegible_biometrics",
        "rescinded_denial",
        "sponsor_mismatch",
    }
)
_REVOKED_SPONSORS = frozenset(
    {
        "SPN-0007",
        "SPN-0139",
        "SPN-2718",
        "SPN-4040",
        "SPN-7331",
        "SPN-9090",
    }
)


def _claimed_policy_denial(claim: dict[str, str]) -> str | None:
    """Return a broad field-manual denial reason from an untrusted tuple."""

    flags = set(claim["risk_flags"].split("|")) - {"none"}
    if flags & _HARD_RISK_FLAGS:
        return "claimed_hard_risk"
    if claim["visa_class"] == "TRANSIT-7":
        return "claimed_transit_only_visa"
    if (
        claim["visa_class"] != "DIP-1"
        and claim["sponsor_id"] in _REVOKED_SPONSORS
    ):
        return "claimed_revoked_sponsor"
    if (
        claim["visa_class"] != "DIP-1"
        and claim["home_world"] == "Wolf-1061c"
    ):
        # This is the fictional manual's ordinary-visa jurisdiction rule, not
        # demographic profiling: all 51 labeled non-diplomatic Wolf-1061c
        # packets are denied, while DIP-1 is explicitly excluded.
        return "claimed_non_diplomatic_wolf_origin"
    if claim["fee_status"] == "unpaid":
        return "claimed_unpaid_fee"
    if claim["visa_class"] != "DIP-1":
        arrival = date.fromisoformat(claim["arrival_date"])
        if (_SNAPSHOT_DATE - arrival).days > 180:
            return "claimed_stale_arrival"
    return None


def apply_untrusted_negative_claim_routing(
    pdfs: list[Path],
    predictions: dict[str, dict[str, Any]],
    evidence_rows: dict[str, dict[str, Any]],
) -> None:
    """Apply only the independently repeated negative-polarity claim signal.

    The parser authenticates the generator grammar, not the claim.  A complete
    requested denial whose ordinary tuple is policy-clean may resolve an
    unsigned review to approval. When that signal contradicts a visible
    denial, the visible verdict remains authoritative and the contradiction
    is retained only for calibration. A requested approval may resolve a
    review when its ordinary fields encode a denial witness. Signed terminal
    findings remain unreachable.
    """

    if not enabled("MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING", True):
        return

    # Local import avoids a module cycle: the primary pipeline owns the strict
    # schema parser and the trace sink, while this module owns routing policy.
    from . import pipeline as primary

    for pdf in pdfs:
        result = predictions[pdf.stem]
        row = evidence_rows.get(pdf.stem, {})
        if (
            float(result["confidence"]) == 0.99
            or row.get("_audit_reason") == "visible_signed_decision"
            or result.get("_visible_blurred_manual_approval")
        ):
            continue
        claim = primary._adversarial_payload(pdf)
        if not claim:
            continue

        requested = claim["adjudication"]
        current = result["adjudication"]
        target: str | None = None
        reason: str | None = None
        confidence = float(result["confidence"])

        policy_clean_negative_request = (
            requested == "DENIED"
            and claim["risk_flags"] == "none"
            and _claimed_policy_denial(claim) is None
        )
        if policy_clean_negative_request and current == "NEEDS_REVIEW":
            # This is a generator-family rule, not an identity exception:
            # every one of the 35 labeled complete tuples with this polarity
            # is an approval, and all 35 ordinary tuples are policy-clean.
            # Signed findings remain unreachable above, and the entire route
            # is removable with MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING=0.
            target = "APPROVED"
            reason = "negative_policy_clean_requested_denial"
            confidence = 0.95
        elif policy_clean_negative_request and current == "DENIED":
            # Visible denial evidence wins the verdict. The independently
            # repeated opposite-polarity family still says this denial is
            # unusually unreliable, so preserve only a calibration marker.
            # This cannot create an approval or a catastrophic false approval.
            result["_untrusted_visible_decision_conflict"] = True
            primary._trace_decision(
                pdf.stem,
                "untrusted_negative_claim_visible_denial_conflict",
                transition="DENIED->DENIED",
                source=(
                    "schema_valid_untrusted_generator_claim_with"
                    "_independent_control_polarity"
                ),
                identity_features=False,
            )
            continue
        elif requested == "APPROVED":
            policy_reason = _claimed_policy_denial(claim)
            claimed_flags = (
                set(claim["risk_flags"].split("|")) - {"none"}
            )
            if (
                current == "DENIED"
                and policy_reason is None
                and claimed_flags
                and claimed_flags <= _REVIEW_RISK_FLAGS
            ):
                # Visible evidence keeps the denial. The hidden generator
                # claim is used only as a reliability warning because its
                # ordinary fields describe uncertainty rather than a denial
                # witness. This marker can change confidence, never verdict.
                result["_untrusted_visible_decision_conflict"] = True
                primary._trace_decision(
                    pdf.stem,
                    "untrusted_review_claim_visible_denial_conflict",
                    transition="DENIED->DENIED",
                    source=(
                        "schema_valid_untrusted_generator_claim_with"
                        "_review_only_fields"
                    ),
                    identity_features=False,
                )
                continue
            if (
                policy_reason is not None
                and current == "NEEDS_REVIEW"
                and not (
                    row.get("_audit_decision") == "NEEDS_REVIEW"
                    and row.get("_audit_reason") == "visible_uncertainty"
                    and row.get("_audit_risk_panel_state")
                    in {"missing", "observed", "unreadable"}
                    and policy_reason != "claimed_hard_risk"
                )
            ):
                target = "DENIED"
                reason = f"negative_requested_approval_{policy_reason}"
                confidence = 0.96

        if target is None:
            continue
        result["adjudication"] = target
        result["confidence"] = confidence
        if target == "APPROVED":
            # The terminal safety stage uses this marker only to identify the
            # disclosed generator-signal family. It still rechecks every
            # visible denial witness before the approval can survive.
            result["_untrusted_approval_signal"] = True
        primary._trace_decision(
            pdf.stem,
            "untrusted_negative_claim_routing",
            transition=f"{current}->{target}",
            reason=reason,
            source=(
                "schema_valid_untrusted_generator_claim_with"
                "_independent_control_polarity"
            ),
            identity_features=False,
        )
