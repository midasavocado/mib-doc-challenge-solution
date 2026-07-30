# MIB Document Pipeline

![MIB document pipeline](docs/assets/mib-pipeline-hero.svg)

An offline, CPU-only submission for the
[8090 MIB Document Challenge](https://github.com/8090-inc/mib-doc-challenge).
It renders every page, extracts case-bound evidence, resolves conflicts by
document precedence, and emits one schema-valid JSONL record per PDF.

The guiding rule is simple: visible evidence may change a decision; a hidden
instruction, identity coincidence, or public-label lookup may not. Any
serialization-only field guess is isolated from policy and disclosed below.

## How it works

![Architecture and evidence guardrails](docs/assets/mib-architecture.svg)

The pipeline has four substantive stages:

1. **Render and OCR.** Poppler rasterizes the PDF before Tesseract reads it.
   Bounded rotation, deskew, high-resolution, faded-ink, and region retries run
   only when the ordinary read is unresolved.
2. **Bind evidence to the active case.** Pages with foreign case IDs cannot
   silently fill the active packet. Multiple OCR views corroborate a source;
   disagreement remains explicit.
3. **Resolve fields and policy.** Document precedence, visible corrections,
   fee and sponsor evidence, risk flags, visa rules, and source conflicts feed
   a deterministic policy engine.
4. **Conservative terminal recovery.** Source-corroborated rules and two
   separately flagged low-cardinality profile families may recover a narrow
   approval tail after hard review fences. The profile features are ordinary
   policy values such as species, home world, visa, purpose, and visible fee
   evidence. They exclude case IDs, applicant identities and name shapes,
   sponsor values, dates, file size, text length, hidden text, and output
   confidence.

`NEEDS_REVIEW` is intentional when the packet does not contain affirmative
evidence for a terminal result. Clean layout, missing forms, or high OCR
confidence alone are not approval or denial witnesses.

At serialization only, the independent extractor may fill unresolved
closed-vocabulary fields with global public-training modes. These output
priors never re-enter policy, change a decision, or use a case identity; they
are disclosed guesses for a scorer that requires every field. Disable them
with `MIB_OUTPUT_PRIOR_FALLBACKS=0` for strictly evidence-only field output.

## Anti-overfitting contract

The submitted path does **not** use:

- case-number routing or per-case answer tables;
- applicant-name tokens, name shapes, sponsor digits, or exact sponsor IDs as
  terminal features;
- hidden “answer key” text, barcode instructions, or native-text directives;
- case-specific verdict-conditioned field guesses;
- exact-document metadata such as PDF bytes or rendered-text length;
- public-selected identity or document-fingerprint residual cells.

Exact sponsor IDs are consulted only by the documented semantic policy list of
revoked sponsors. That is a policy fact, not an identity proxy.

A historical public-only experiment reached perfect public classification by
adding highly specific name/sponsor conjunctions. Those rules and the analogous
extraction table were removed from the runtime rather than presented as
generalization. A later frozen approval model was also removed: its categorical-
only cross-fit failed, showing that its apparent gain depended on PDF/text-size
features.

Two tempting visual shortcuts were rejected too. The legacy blue-slash detector
matched one public true review and one independent true approval, but no denial;
its fee-text veto merely hid the public error. Passport portraits are also
reused across species, so portrait-to-species inference performs near chance.

A repeated-source shortcut was removed during final acceptance as well.
Requiring two labeled species reads plus either home-world or arrival
corroboration recovered four public approvals, but also created one false
approval of a denied packet. The stricter “both home and arrival” variant was
still mixed on the independent controls (four approvals, three denials, and two
reviews), so the family now abstains instead of encoding a public residual.
The same audit removed a diplomatic-purpose corroboration shortcut: after
ordinary hard fences, its independent matches still included two denials.

The remaining demographic/cohort profiles are disclosed associational
exceptions inferred from labeled examples, as the field manual permits. They
are feature-flagged, contain no identities, and were retained only when the
same terminal-eligible pattern recurred without a contrary result in the
separate visible-finding controls. Disable them for a source-rules-only
ablation.

| Flagged profile | Public support | Independent support |
|---|---:|---:|
| Paid XW-1 field repair | 7 approved | 4 approved |
| VENUSIAN_MYCELIAL from Zeta Reticuli | 3 approved | 3 approved |
| Gliese-581g translation with visible arrival | 3 approved | 3 approved |
| TRIANGULAN XW-1 with visible fee/intake support | 3 approved | 3 approved among terminal-eligible controls |
| JOVIAN DIP-1 with visible arrival | 5 approved | 5 approved |
| Intake-visible DIP-1 field repair | 4 approved | 3 approved |
| KAIJU cultural exchange with no flag claim | 4 approved | 3 approved |
| TRIANGULAN DIP-1 with visible arrival | 3 approved | 6 approved |
| Barnard-c MED-3 with intake-visible visa and arrival | 2 approved | 4 approved |
| Three-page sponsor-backed JOVIAN, safe visa | 2 approved | 2 approved |

These counts are selection evidence, not a promise of private accuracy. The
JOVIAN profile is separated because its sample is smaller; the cohort and
demographic flags permit independent rollback.

## Run

Build and run the same offline entrypoint used by the organizer:

```bash
docker build -t mib-doc-solution .
mkdir -p output
docker run --rm --network none \
  --cpus 4 \
  --memory 8g \
  --pids-limit 512 \
  --read-only \
  --tmpfs /tmp:rw,size=2g \
  -v "$PWD/input:/input:ro" \
  -v "$PWD/output:/output" \
  mib-doc-solution /input /output/predictions.jsonl
```

The entrypoint accepts exactly:

```text
<input_pdf_dir> <output_predictions_path>
```

The image is CPU-only. Building it fetches the pinned system and Python
packages; running the completed image requires no network.

## Feature flags

All flags are optional. Defaults are the production settings.

| Flag | Default | Purpose |
|---|---:|---|
| `MIB_MAX_WORKERS` | `4` | Worker count, capped at four |
| `MIB_TERMINAL_SOURCE_RULES` | `1` | Source-corroborated terminal families |
| `MIB_TERMINAL_DEMOGRAPHIC_PROFILE` | `1` | Sponsor-corroborated JOVIAN/page-topology cohort with a non-transit visa safety gate |
| `MIB_TERMINAL_COHORT_PROFILES` | `1` | Cross-corpus low-cardinality policy cohorts; no identities or document fingerprints |
| `MIB_HIRES_NARROW` | `1` | Targeted high-resolution unresolved-field OCR |
| `MIB_REGION_RETRY` | `1` | Region-local restoration for unresolved fields |
| `MIB_FADED_INK_RETRY` | `1` | Faded applicant/sponsor/date recovery |
| `MIB_MANUAL_REASON_FIELD_RECOVERY` | `1` | Parse visible manual-reason fields |
| `MIB_SPONSOR_VERIFICATION_DENIAL` | `1` | Enforce visible sponsor-verification denial |
| `MIB_POST_EXTRACTION_REVIEW_GUARD` | `1` | Demote inferred approvals on late B-13 review flags or a blank active intake arrival |
| `MIB_JUDGMENT_FIELD_REPAIR` | `1` | Extraction-only repair when an authenticated approval is paired with a two-view foreign unpaid receipt |
| `MIB_OUTPUT_PRIOR_FALLBACKS` | `1` | Serialization-only global modes for unresolved closed-vocabulary fields; cannot affect adjudication |
| `MIB_CONFIDENCE_BLEND` | `1` | Identity-free confidence calibration only |
| `MIB_OCR_MEMO` | `1` | Reuse OCR calls within one process |
| `MIB_LOCAL_CACHE` | `1` | Reuse content-addressed host evidence |
| `MIB_LOCAL_CACHE_DIR` | platform cache | Relocate the cache; Docker uses its per-run `/tmp` tmpfs |
| `MIB_DECISION_TRACE` | `0` | Emit structured policy transitions to stderr |

For a source-rules-only classification ablation:

```bash
MIB_TERMINAL_DEMOGRAPHIC_PROFILE=0 \
MIB_TERMINAL_COHORT_PROFILES=0 \
docker run ...
```

Cache keys include the PDF digest and extractor schema; malformed, unavailable,
or stale entries fail open to ordinary processing. The organizer container
starts with an empty cache in its nonpersistent `/tmp` tmpfs, which only avoids
duplicating OCR between stages of that one run. Read-only input remains
untouched.

## Organizer contract audit

The final audit used organizer commit
`38ce8883dea9f87c27a8a95f134e54fe8b673064`. The two merged maintenance PRs
([#1](https://github.com/8090-inc/mib-doc-challenge/pull/1) and
[#2](https://github.com/8090-inc/mib-doc-challenge/pull/2)) clarify README and
Docker-submission wording; they do not add a new scoring path. The enforced
contract remains offline CPU execution with 4 vCPUs, 8 GiB RAM, read-only
input/root filesystems, a 2 GiB `/tmp`, 512 PIDs, and a six-second average
budget per PDF.

## Verified result

The final generalized image was evaluated on all 1,000 public packets through
the organizer's unchanged Docker runner:

| Section | Score |
|---|---:|
| Extraction | 45.465556 / 50 |
| Classification | 71.70 / 80 |
| Calibration | 17.639628 / 20 |
| Total | 134.805184 / 150 |

The confusion matrix is 200 approved-as-approved, one approved-as-denied, 88
approved-as-review, 382 denied-as-denied, 49 denied-as-review, and all 280
reviews preserved. There are **zero catastrophic false approvals**.

Primary processing took 1,615.3 seconds and the independent provenance pass
took 1,591.1 seconds. Container start through schema-valid output took 3,317.2
seconds, or **3.317 seconds/PDF**, under both the requested five-second target
and organizer cap. The run used image
`sha256:8b8bb4bb409fa966f550f03435a4962bb7f0d642fee3e5d6f011556d49436747`;
the prediction SHA-256 is
`6c2a9f2d1186dfa7c1541287923464a6020f8c83d82b6b8ccad6b84beb4dd067`.

The requested 79/80 classification and 50/50 extraction targets were not met
after identity, fingerprint, hidden-payload, and mixed-transfer rules were
removed. The lower number is the submission-safe result, not a claim that the
old public-perfect residual table generalized.

## Verification

Acceptance is run through the organizer’s own Docker runner and validator:

```bash
python3 scripts/run_docker_submission.py \
  --repo /path/to/solution \
  --input-dir data/train \
  --output /tmp/mib-acceptance/predictions.jsonl \
  --manifest data/train_labels.csv \
  --image-tag mib-doc-solution:acceptance \
  --timeout-seconds 5000 \
  --cpus 4 \
  --memory 8g \
  --require-complete

python3 scripts/validate_submission.py \
  --submission /tmp/mib-acceptance/predictions.jsonl \
  --manifest data/train_labels.csv \
  --require-complete

python3 scripts/evaluate.py \
  --truth data/train_labels.csv \
  --submission /tmp/mib-acceptance/predictions.jsonl \
  --output-json /tmp/mib-acceptance/evaluation.json
```

The final verified score, confusion matrix, runtime, hashes, transfer audit,
and rejected experiments are recorded in [`MEMO.md`](MEMO.md). The concise memo
is the handoff document; `MEMO original.md` preserves the full research log.

## Repository map

```text
solution.py                         challenge entrypoint
mib_pipeline/
  pipeline.py                      OCR, extraction, and evidence policy
  hybrid.py                        independent provenance reconciliation
  local_cache.py                   content-addressed development cache
  pattern_policy.py                active-intake evidence-state helpers
  terminal_approval.py             source rules and flagged broad profiles
provenance_engine/                  independent extraction/provenance pass
docs/assets/                        README diagrams
run.sh                              container entrypoint
Dockerfile                          offline runtime image
```

## Provenance and licensing

This repository began from the organizer’s MIT-licensed offline baseline and
was developed against the official public challenge kit and training PDFs.
It contains no copied participant implementation. Third-party notices for
vendored/exported components are in [`third_party_licenses`](third_party_licenses).
