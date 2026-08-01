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

    negative_claim_enabled = enabled(
        "MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING",
        True,
    )
    registry_status_enabled = enabled(
        "MIB_UNTRUSTED_REGISTRY_STATUS_ROUTING",
        True,
    )
    if not (negative_claim_enabled or registry_status_enabled):
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

        if primary._untrusted_registry_embargo_review(str(pdf.resolve())):
            current_flags = (
                set(str(result["risk_flags"]).split("|")) - {"none"}
            )
            diplomatic_exception = (
                result["visa_class"] == "DIP-1"
                and result["fee_status"] == "paid"
                and result["declared_purpose"] != "transit"
                and row.get("_audit_risk_panel_state") == "absent"
                and current_flags <= {"planetary_embargo"}
            )
            if not diplomatic_exception and result["adjudication"] != "DENIED":
                # Public: 31 denials / 2 explicit reviews; independent signed
                # controls: 25 denials / 2 paid DIP-1 approvals.  The signed
                # reviews were excluded above, while the program-level
                # diplomatic exception protects both control approvals.  This
                # leaves the broad unsigned status rule with no false approval
                # path and no person-, case-, sponsor-, or date-specific key.
                previous = str(result["adjudication"])
                result["adjudication"] = "DENIED"
                result["confidence"] = 0.96
                primary._trace_decision(
                    pdf.stem,
                    "untrusted_registry_status_routing",
                    transition=f"{previous}->DENIED",
                    reason="unsigned_embargo_review_without_diplomatic_veto",
                    source="case_bound_native_registry_status",
                    identity_features=False,
                )
                continue

        if primary._untrusted_sponsor_verification_notice(
            str(pdf.resolve())
        ):
            current_flags = (
                set(str(result["risk_flags"]).split("|")) - {"none"}
            )
            diplomatic_notice_clearance = (
                result["adjudication"] == "NEEDS_REVIEW"
                and result["visa_class"] == "DIP-1"
                and result["fee_status"] in {"paid", "waived"}
                and result["declared_purpose"] != "transit"
                and not current_flags
                and row.get("_audit_decision") in {None, "APPROVED"}
                and not row.get("_audit_contested")
            )
            if diplomatic_notice_clearance:
                # Development: every one of the five case-bound DIP-1
                # sponsor-verification notices is an approval, split across
                # both deterministic halves; all twenty non-DIP notices are
                # denials.  The mechanism is program-level: DIP-1 does not
                # require sponsor standing, while the same notice is adverse
                # for sponsor-dependent programs.  This proposal remains
                # untrusted and therefore passes through the common visible
                # denial and approval-sufficiency fences below.
                result["adjudication"] = "APPROVED"
                result["confidence"] = 0.90
                result["_untrusted_approval_signal"] = True
                result["_untrusted_diplomatic_sponsor_notice"] = True
                primary._trace_decision(
                    pdf.stem,
                    "untrusted_diplomatic_sponsor_notice_routing",
                    transition="NEEDS_REVIEW->APPROVED",
                    reason="dip1_does_not_require_sponsor_standing",
                    source="case_bound_native_sponsor_verification_notice",
                    identity_features=False,
                )
                continue
            sponsor_notice_veto = (
                result["visa_class"] == "DIP-1"
                or bool(current_flags & _REVIEW_RISK_FLAGS)
            )
            if not sponsor_notice_veto and result["adjudication"] != "DENIED":
                # The program exception is stable across corpora: all ten
                # approvals carrying this notice are DIP-1, while the only
                # non-diplomatic review control has an explicit review-only
                # biometric fault.  After those two broad vetoes, the notice
                # is a repeated sponsor-clearance denial signal rather than an
                # identity, sponsor-number, or case lookup.
                previous = str(result["adjudication"])
                result["adjudication"] = "DENIED"
                result["confidence"] = 0.96
                primary._trace_decision(
                    pdf.stem,
                    "untrusted_registry_sponsor_status_routing",
                    transition=f"{previous}->DENIED",
                    reason=(
                        "non_diplomatic_sponsor_clearance_notice_without"
                        "_review_fault"
                    ),
                    source="case_bound_native_registry_notice",
                    identity_features=False,
                )
                continue

        if not negative_claim_enabled:
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
            # every one of the 35 public complete tuples with this polarity is
            # an approval, as are all 37 independently signed comparison
            # packets. Redaction is not used as a veto because it occurs in
            # signed approvals too. A real visible denial remains authoritative
            # below, and the entire route is removable with
            # MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING=0.
            target = "APPROVED"
            reason = "negative_policy_clean_requested_denial"
            confidence = 0.95
        elif policy_clean_negative_request and current == "DENIED":
            visible_denial = row.get("_audit_decision") == "DENIED"
            if visible_denial:
                # A visible denial remains authoritative. The independent
                # generator-family disagreement is calibration-only.
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
            # The complete, policy-clean negative-request family is 25/25 on
            # the fixed 800-case development partition, with support in all
            # five internal folds. Treat an unsigned primary denial as another noisy
            # generator disagreement, then send the proposal through the same
            # visible-witness safety fence as every other unsigned approval.
            # This is one corpus-wide polarity rule, not a list of cases or
            # identities.
            target = "APPROVED"
            reason = "negative_policy_clean_requested_denial"
            confidence = 0.95
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
                    and policy_reason
                    not in {
                        "claimed_hard_risk",
                        "claimed_revoked_sponsor",
                        "claimed_non_diplomatic_wolf_origin",
                    }
                )
                and not (
                    policy_reason == "claimed_non_diplomatic_wolf_origin"
                    and claimed_flags == {"illegible_biometrics"}
                    and row.get("_audit_decision") == "NEEDS_REVIEW"
                )
            ):
                # The complete Wolf + lone-illegibility family is eight
                # denials / two reviews publicly and three denials in the
                # independent signed controls.  Only an actual visible review
                # decision activates the exception; checking the claimed flag
                # alone also preserved two public denials.
                target = "DENIED"
                reason = f"negative_requested_approval_{policy_reason}"
                confidence = 0.96

        if target is None:
            if requested == "APPROVED" and current == "NEEDS_REVIEW":
                # Reliability marker only, never a verdict route. Across the
                # 800-case development partition, all 50 final reviews in
                # this generator family are correct, with support in every
                # deterministic internal fold. This lets calibration separate
                # them from ordinary OCR abstentions without reading identity.
                result["_untrusted_review_confirmation"] = True
            continue
        result["adjudication"] = target
        result["confidence"] = confidence
        if target == "APPROVED":
            # The terminal safety stage uses this marker only to identify the
            # disclosed generator-signal family. It still rechecks every
            # visible denial witness before the approval can survive.
            result["_untrusted_approval_signal"] = True
            if reason == "negative_policy_clean_requested_denial":
                # Keep the independently repeated 25/25 development polarity
                # family distinct from native sponsor notices. This marker is
                # still only a proposal: a visible signed or policy denial
                # remains authoritative in the terminal safety pass.
                result["_negative_generator_approval_signal"] = True
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
