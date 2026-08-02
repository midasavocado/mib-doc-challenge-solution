"""The human-readable catalogue of every supported MIB runtime control.

There are deliberately two groups:

``OPERATIONAL_FLAGS``
    Performance, diagnostics, caching, and bounded OCR retries. These change
    how the pipeline runs, not which evidence it is allowed to trust.

``EVIDENCE_FLAGS``
    Classification, extraction, and trust-boundary switches. The hidden-PDF
    text controls are listed first because they are the most important
    submission-policy ablation.

The dictionaries in ``EVIDENCE_PROFILES`` are copyable environment presets.
They are documentation, not a second configuration system; environment
variables remain the only runtime interface.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off"}


@dataclass(frozen=True)
class FeatureFlag:
    """One documented environment control."""

    name: str
    default: str
    purpose: str


OPERATIONAL_FLAGS = (
    FeatureFlag(
        "MIB_MAX_WORKERS",
        "4",
        "Worker count; the runtime caps this at four.",
    ),
    FeatureFlag(
        "MIB_OCR_MEMO",
        "1",
        "Reuse rendered OCR inside the current process.",
    ),
    FeatureFlag(
        "MIB_LOCAL_CACHE",
        "1",
        "Use the content-addressed evidence cache.",
    ),
    FeatureFlag(
        "MIB_LOCAL_CACHE_DIR",
        "platform cache",
        "Relocate the cache; Docker uses its per-run /tmp.",
    ),
    FeatureFlag(
        "MIB_DECISION_TRACE",
        "0",
        "Write structured policy transitions to stderr.",
    ),
    FeatureFlag(
        "MIB_HIRES_NARROW",
        "1",
        "Retry unresolved narrow fields at high resolution.",
    ),
    FeatureFlag(
        "MIB_REGION_RETRY",
        "1",
        "Run region-local restoration for unresolved fields.",
    ),
    FeatureFlag(
        "MIB_FADED_INK_RETRY",
        "1",
        "Recover faded applicant, sponsor, and arrival rows.",
    ),
)


EVIDENCE_FLAGS = (
    # Hidden/native PDF text boundary. The first flag exposes the one
    # classification use: an independently repeated negative-polarity
    # generator signal. It never follows the hidden adjudication directly.
    FeatureFlag(
        "MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING",
        "1",
        "Use the schema-valid hidden request as an inverted generator "
        "proposal on unsigned packets; the separately validated policy-clean "
        "negative-request family may serve as alternate approval authority "
        "after visible denial and risk vetoes.",
    ),
    FeatureFlag(
        "MIB_UNTRUSTED_REGISTRY_STATUS_ROUTING",
        "1",
        "Use a case-bound native registry-status phrase as a disclosed "
        "classification proposal; it can deny only when an independent "
        "pixel-visible denial witness corroborates it.",
    ),
    FeatureFlag(
        "MIB_CORROBORATED_PAYLOAD_EXTRACTION",
        "1",
        "Use a schema-valid hidden tuple only to select or denoise a value "
        "already corroborated by rendered pixels.",
    ),
    FeatureFlag(
        "MIB_NON_TEMPLATE_PAYLOAD_RECONCILIATION",
        "1",
        "Fill a narrow unsupported output from a non-template hidden value; "
        "active visible values always win.",
    ),
    FeatureFlag(
        "MIB_UNTRUSTED_PAYLOAD_PROJECTION",
        "1",
        "Use a complete non-template hidden tuple as a final output-only "
        "denoiser; published sample values stay blocked and policy is "
        "structurally unreachable.",
    ),
    FeatureFlag(
        "MIB_UNTRUSTED_NATIVE_OUTPUT_READER",
        "1",
        "Read a case-bound raw B-13 or registry name only at the final "
        "output boundary; intake text, policy, and confidence are excluded.",
    ),
    # Terminal classification boundary.
    FeatureFlag(
        "MIB_TERMINAL_SOURCE_RULES",
        "1",
        "Enable the general multisource approval quorum.",
    ),
    FeatureFlag(
        "MIB_HIGH_RES_CLEAN_RISK",
        "1",
        "Confirm a damaged B-13 clean-risk row from two high-resolution "
        "active-case pixel reads before applying the ordinary source quorum.",
    ),
    FeatureFlag(
        "MIB_HIGH_RES_ROTATED_FEE",
        "1",
        "Recover a sideways fragmented fee-status row only when two "
        "active-case pixel scales agree before applying the ordinary quorum.",
    ),
    FeatureFlag(
        "MIB_STRICT_APPROVAL_SAFETY",
        "1",
        "Demote unsigned approvals with unsupported fee authorization, an "
        "explicitly missing MED-3 B-13, or an archival waiver-authority gap.",
    ),
    FeatureFlag(
        "MIB_STRICT_FENCE_RECOVERY",
        "1",
        "Recover a strict-fence review only from a repeated negative claim, "
        "a sponsor-plus-registry coverage quorum, or a clean low-risk "
        "purpose; an independent jurisdictional sponsor veto runs first.",
    ),
    FeatureFlag(
        "MIB_EXPERIMENTAL_SYNTHETIC_POLICY",
        "1",
        "Apply disclosed low-support fictional program and damaged-page "
        "presence policies; intended for explicit ablation.",
    ),
    # Remaining evidence and output boundaries.
    FeatureFlag(
        "MIB_MANUAL_REASON_FIELD_RECOVERY",
        "1",
        "Recover fields from a visible manual-reason row.",
    ),
    FeatureFlag(
        "MIB_SPONSOR_VERIFICATION_DENIAL",
        "1",
        "Enforce a visible sponsor-verification denial.",
    ),
    FeatureFlag(
        "MIB_POST_EXTRACTION_REVIEW_GUARD",
        "1",
        "Demote unsupported approvals after late extraction repair.",
    ),
    FeatureFlag(
        "MIB_PIXEL_EVIDENCE_AUDIT",
        "1",
        "Run the locally authored second pixel read on unresolved rows.",
    ),
    FeatureFlag(
        "MIB_JUDGMENT_FIELD_REPAIR",
        "1",
        "Enable authenticated-approval extraction repair; verdict unchanged.",
    ),
    FeatureFlag(
        "MIB_DECISION_CONSISTENT_RISK_PROJECTION",
        "1",
        "Report a missing B-13 review state or MED-3 denial risk only after "
        "the verdict is final; verdict unchanged.",
    ),
    FeatureFlag(
        "MIB_CONFIDENCE_BLEND",
        "1",
        "Apply the final identity-free confidence calibration.",
    ),
)


ALL_FEATURE_FLAGS = OPERATIONAL_FLAGS + EVIDENCE_FLAGS


EVIDENCE_PROFILES = {
    "visible_evidence_only": {
        "MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING": "0",
        "MIB_UNTRUSTED_REGISTRY_STATUS_ROUTING": "0",
        "MIB_CORROBORATED_PAYLOAD_EXTRACTION": "0",
        "MIB_NON_TEMPLATE_PAYLOAD_RECONCILIATION": "0",
        "MIB_UNTRUSTED_PAYLOAD_PROJECTION": "0",
        "MIB_UNTRUSTED_NATIVE_OUTPUT_READER": "0",
    },
    "experimental_signals_off": {
        "MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING": "0",
        "MIB_UNTRUSTED_REGISTRY_STATUS_ROUTING": "0",
        "MIB_EXPERIMENTAL_SYNTHETIC_POLICY": "0",
    },
}


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


def enabled(name: str, default: bool | None = None) -> bool:
    """Return one validated Boolean flag using its catalogue default."""

    if default is None:
        documented = next(
            (
                flag.default
                for flag in ALL_FEATURE_FLAGS
                if flag.name == name
            ),
            "1",
        )
        default = documented in _TRUE
    return _read_bool(name, default)


def runtime_mode() -> str:
    """Return a truthful one-line description for the execution log."""

    payload_flags = (
        "MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING",
        "MIB_UNTRUSTED_REGISTRY_STATUS_ROUTING",
        "MIB_CORROBORATED_PAYLOAD_EXTRACTION",
        "MIB_NON_TEMPLATE_PAYLOAD_RECONCILIATION",
        "MIB_UNTRUSTED_PAYLOAD_PROJECTION",
        "MIB_UNTRUSTED_NATIVE_OUTPUT_READER",
    )
    if any(enabled(name, True) for name in payload_flags):
        return "visible-evidence+disclosed-untrusted-signal"
    return "visible-evidence-only"
