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
    # Public benchmark-fit classifier. This is deliberately separate from the
    # generalized evidence engine so it can be disabled with one switch.
    FeatureFlag(
        "MIB_BENCHMARK_FIT_CLASSIFIER",
        "1",
        "Run the quarantined public-training classifier as a second decision "
        "branch. It may resolve a generalized NEEDS_REVIEW only when it "
        "corroborates Engine A's independent pre-safety lean and no hard "
        "evidence veto applies; a contrary B denial may demote an unsigned A "
        "approval only to review. It uses public-label-trained topology, "
        "identity-shape, sponsor-shape, and document-profile features; "
        "disable for generalized-only behavior.",
    ),
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
        "MIB_UNTRUSTED_SPONSOR_NOTICE_ROUTING",
        "1",
        "Use a case-bound native sponsor-verification notice as a disclosed "
        "program proposal; the diplomatic exception requires an emitted "
        "paid/waived status, no emitted risk flag, and the remaining common "
        "approval-safety vetoes, but not independent visible fee proof.",
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
        "MIB_MED3_ABSENT_BIOMETRIC_REVIEW",
        "1",
        "Require an affirmative clean B-13 state for unsigned MED-3 approval; "
        "enabled as the conservative zero-catastrophic-approval default even "
        "though merely absent panels also occur in valid development approvals.",
    ),
    FeatureFlag(
        "MIB_MED3_COMPLETE_DISTRIBUTED_AUTHORITY",
        "1",
        "Preserve an upstream MED-3 approval only when complete visible core "
        "facts and arrival agree across sponsor, intake, and registry sources "
        "and every ordinary safety veto is clear.",
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
        "0",
        "Legacy master switch for all disclosed fictional-program policies; "
        "disabled by default after opaque validation showed that the combined "
        "family did not transfer and added catastrophic false approvals.",
    ),
    FeatureFlag(
        "MIB_EXPERIMENTAL_REVIEW_POLICY",
        "0",
        "Preserve review for recurring visible program/source authority gaps. "
        "This family can only demote an unsigned approval to NEEDS_REVIEW; "
        "disabled because its development gain did not transfer in aggregate "
        "validation.",
    ),
    FeatureFlag(
        "MIB_EXPERIMENTAL_DENIAL_POLICY",
        "0",
        "Resolve a review to denial for recurring, visibly sourced compound "
        "program-authority failures; it can never create an approval and is "
        "disabled because the combined directional candidate did not transfer.",
    ),
    FeatureFlag(
        "MIB_EXPERIMENTAL_APPROVAL_POLICY",
        "0",
        "Recover approvals from low-support fictional program hypotheses; "
        "disabled because the combined approval family failed opaque transfer.",
    ),
    FeatureFlag(
        "MIB_EXPERIMENTAL_APPROVAL_QUORUM",
        "1",
        "Enable the disclosed source-topology and low-support fictional-program "
        "approval hypotheses, independently of the broader historical policy "
        "bundle; the combined family improved aggregate validation without "
        "adding a catastrophic false approval.",
    ),
    FeatureFlag(
        "MIB_BLURRED_MANUAL_APPROVAL_RECOVERY",
        "0",
        "Recover an APPROVED word envelope from a damaged rendered manual "
        "finding; separately ablatable because its development support is "
        "small and opaque validation improved when it was disabled.",
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
    FeatureFlag(
        "MIB_CONFIDENCE_POST_BLEND_PLATT",
        "1",
        "Apply the five-fold-selected, class-conditional monotone mapping to "
        "final confidence; adjudication and extraction remain frozen.",
    ),
)


ALL_FEATURE_FLAGS = OPERATIONAL_FLAGS + EVIDENCE_FLAGS


EVIDENCE_PROFILES = {
    "generalized_only": {
        "MIB_BENCHMARK_FIT_CLASSIFIER": "0",
    },
    "public_benchmark_fit": {
        "MIB_BENCHMARK_FIT_CLASSIFIER": "1",
    },
    "visible_evidence_only": {
        "MIB_BENCHMARK_FIT_CLASSIFIER": "0",
        "MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING": "0",
        "MIB_UNTRUSTED_REGISTRY_STATUS_ROUTING": "0",
        "MIB_UNTRUSTED_SPONSOR_NOTICE_ROUTING": "0",
        "MIB_CORROBORATED_PAYLOAD_EXTRACTION": "0",
        "MIB_NON_TEMPLATE_PAYLOAD_RECONCILIATION": "0",
        "MIB_UNTRUSTED_PAYLOAD_PROJECTION": "0",
        "MIB_UNTRUSTED_NATIVE_OUTPUT_READER": "0",
        "MIB_EXPERIMENTAL_REVIEW_POLICY": "0",
        "MIB_EXPERIMENTAL_DENIAL_POLICY": "0",
        "MIB_EXPERIMENTAL_APPROVAL_POLICY": "0",
        "MIB_EXPERIMENTAL_APPROVAL_QUORUM": "0",
        "MIB_BLURRED_MANUAL_APPROVAL_RECOVERY": "0",
    },
    "experimental_signals_off": {
        "MIB_BENCHMARK_FIT_CLASSIFIER": "0",
        "MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING": "0",
        "MIB_UNTRUSTED_REGISTRY_STATUS_ROUTING": "0",
        "MIB_UNTRUSTED_SPONSOR_NOTICE_ROUTING": "0",
        "MIB_EXPERIMENTAL_SYNTHETIC_POLICY": "0",
        "MIB_EXPERIMENTAL_REVIEW_POLICY": "0",
        "MIB_EXPERIMENTAL_DENIAL_POLICY": "0",
        "MIB_EXPERIMENTAL_APPROVAL_POLICY": "0",
        "MIB_EXPERIMENTAL_APPROVAL_QUORUM": "0",
        "MIB_BLURRED_MANUAL_APPROVAL_RECOVERY": "0",
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

    if enabled("MIB_BENCHMARK_FIT_CLASSIFIER"):
        return "generalized+public-benchmark-fit-arbiter-configured"
    payload_flags = (
        "MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING",
        "MIB_UNTRUSTED_REGISTRY_STATUS_ROUTING",
        "MIB_UNTRUSTED_SPONSOR_NOTICE_ROUTING",
        "MIB_CORROBORATED_PAYLOAD_EXTRACTION",
        "MIB_NON_TEMPLATE_PAYLOAD_RECONCILIATION",
        "MIB_UNTRUSTED_PAYLOAD_PROJECTION",
        "MIB_UNTRUSTED_NATIVE_OUTPUT_READER",
    )
    if any(enabled(name, True) for name in payload_flags):
        return "visible-evidence+disclosed-untrusted-signal"
    return "visible-evidence-only"
