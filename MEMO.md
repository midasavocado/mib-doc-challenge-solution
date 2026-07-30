# MIB Pipeline Final Handoff

## Outcome

The final generalized pipeline passed the organizer's exact 1,000-document
Docker run and schema validator.

| Section | Final score |
|---|---:|
| Extraction | 45.465556 / 50 |
| Classification | 71.70 / 80 |
| Calibration | 17.639628 / 20 |
| Total | 134.805184 / 150 |

Extraction raw is 40,919/45,000 and classification raw is 7,170/8,000.
Mean confidence Brier is 0.0590093. The confusion matrix is:

- 200 approved as approved;
- one approved as denied;
- 88 approved as review;
- 382 denied as denied;
- 49 denied as review;
- all 280 reviews preserved.

There are **zero catastrophic false approvals**.

The requested 79/80 classification and 50/50 extraction targets were not
reached after benchmark-specific and mixed-transfer rules were removed. The
lower score is the honest submission-safe result. The full experiment history,
including failed paths and historical higher public scores, is preserved in
[`MEMO original.md`](MEMO%20original.md).

## What ships

The pipeline is offline and CPU-only. It renders every page, performs
multi-view OCR, binds evidence to the active case, resolves fields by source
precedence, applies visible policy rules, and reconciles an independent
provenance pass.

Classification uses:

- authenticated visible decisions and corrections;
- case-bound fee, sponsor, embargo, visa, biometric, and conflict evidence;
- source-corroborated terminal rules behind hard review fences;
- ten feature-flagged low-cardinality profiles using ordinary policy fields
  and active document topology.

Extraction uses:

- case-bound source precedence and multi-view OCR;
- bounded rotation, deskew, region, faded-ink, and high-resolution retries;
- one-glyph sponsor alternatives only when labels and absence evidence agree;
- prefix-only and batch-vocabulary applicant-name repair;
- a narrow arrival-year repair;
- a post-extraction review safeguard.

For unresolved closed-vocabulary fields, the provenance serializer may use a
disclosed global training mode for species, home world, visa, purpose, or fee.
This output-only fallback never re-enters adjudication or confidence and is
disabled with `MIB_OUTPUT_PRIOR_FALLBACKS=0`.

## Anti-overfitting audit

The final runtime contains no:

- case-number routing or per-case answer table;
- applicant identity, name token, or name-shape decision feature;
- arbitrary sponsor value, sponsor digit, or sponsor-fragment decision feature;
- exact date, file size, text length, or document-fingerprint route;
- hidden answer-key instruction or hidden-payload reconciliation;
- verdict-conditioned per-case extraction guess;
- public-selected residual tree or categorical model.

Exact sponsor IDs appear only in the documented revoked-sponsor policy list.

Two generated approval seed tables and the public-perfect name/sponsor
conjunctions were deleted. The frozen CatBoost approval model was deleted after
its non-fingerprint categorical features failed rotating and chronological
controls. The default-off perfect-field policy bridge was also removed from the
runtime because it failed on actual noisy extracted fields.

The final acceptance audit removed two additional broad-looking shortcuts
wholesale:

1. Two species reads plus either home-world or arrival corroboration recovered
   four public approvals but falsely approved one denial. Requiring both still
   produced four approvals, three denials, and two reviews on independent
   controls.
2. Diplomatic purpose seen twice plus one arrival source still included two
   terminal-eligible denials in the independent controls.

Neither family was narrowed around individual cases; both now abstain.

The retained topology rules have either direct policy semantics or clean
independent support. Examples include four independent approvals for complete
biometric/intake/registry packets, three each for the two damaged
registry/sponsor families, three for the damaged three-page biometric family,
two for the visible DIP-waiver family, and two for XW-2 intake/sponsor
agreement.

## Independent controls

The separate 5,000-document corpus contains 840 packets with independently
readable visible findings: 242 approved, 340 denied, and 258 review. The
current visible-finding path classifies all 840 correctly.

Those controls were also used to reject:

- additional sponsor-identity rules;
- sponsor-digit and text n-gram models;
- low-cardinality logistic and random-forest residual classifiers;
- the blue-slash visual detector;
- portrait-to-species inference;
- neighboring-case and generator-phase probes.

Models trained on the 840 controls did not transfer to the public
missing-evidence residual. No such model is shipped.

## Docker acceptance

Organizer commit:
`38ce8883dea9f87c27a8a95f134e54fe8b673064`

The two organizer maintenance PRs were inspected and are merged. They clarify
README and Docker wording but do not add a scoring path.

The final run used:

- no network;
- four CPUs and 8 GiB RAM;
- read-only root and input filesystems;
- a 2 GiB nonpersistent `/tmp`;
- 512 PIDs and `no-new-privileges`.

Primary processing took 1,615.3 seconds. The provenance pass took 1,591.1
seconds. Container start through schema-valid output took 3,317.152 seconds,
or **3.317152 seconds/PDF**, below the requested five-second target and the
organizer's six-second cap.

The per-run cache began empty and logged 1,000 rendered-OCR writes, 327
same-run OCR hits, 891 provenance writes, and 109 authenticated-finding
provenance skips.

The validator accepted exactly 1,000 records with zero missing, extra,
duplicate, invalid-adjudication, invalid-confidence, or invalid-fee rows.

## Reproducibility

- Image:
  `sha256:8b8bb4bb409fa966f550f03435a4962bb7f0d642fee3e5d6f011556d49436747`
- Predictions:
  `6c2a9f2d1186dfa7c1541287923464a6020f8c83d82b6b8ccad6b84beb4dd067`
- Evaluation:
  `14eb7a86ff0dec25f2358cfa98d2e4b2843141cacc00ec33ada7da495d43d5b2`

The exact organizer commands and all feature flags are documented in
[`README.md`](README.md).
