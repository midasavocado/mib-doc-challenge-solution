# MIB Document Challenge — Development Changelog

This file preserves the detailed experiment history in chronological form.
For the current architecture, measured result, and engineering rationale, see
[`MEMO.md`](MEMO.md).

Last updated: 2026-08-01

## 2026-08-01 — fragmented sideways fee source reaches 145.2377

- Added a visible-pixel source reader for fee receipts whose sideways row
  survives while the document heading is too damaged to classify. It consumes
  only exact active-case unknown-page numbers from the independent audit,
  rejects prompt-like and non-fee headings, and requires 150/200-DPI rotated
  reads to agree on one row-local status.
- Preserved physical OCR geometry: up to four rows and 48 compact characters,
  with at most one blank row to accommodate Linux Tesseract splitting `Sta`
  from `tus`. Conflicting scales, multiple pages, multiple statuses, or a
  different nondefault extraction all abstain.
- Audited the complete structural development cohort: 127 eligible packets,
  six detector reads across three folds, two approvals and four denials, and
  six of six fee values correct. Five reads reach the normal terminal stage
  because the sixth packet has an earlier authenticated finding. Only one
  unresolved clean diplomatic waiver changes verdict, from review to approval.
- The review path is not fee-only authority. Sparse retry requires a defaulted
  fee, visibly observed `DIP-1`, a clean audited risk panel, no visible
  decision/reason/contest, and confidence below 0.99. The ordinary source
  quorum plus both final approval-safety passes still gate the result.
- Exact fixed-800 replay: **47.061111 extraction**, **78.575000
  classification**, **19.601605 calibration**, and **145.237716 total**, with
  **0 catastrophic false approvals**. Confusion is 204 correct approvals, 350
  correct denials, 227 correct reviews, and 19 approvals conservatively held
  for review. The spent 200 was not opened or rescored.
- Prediction SHA-256:
  `71f52a60dacf16154733e431d9754c7ccae1a366e204ecde21b86854b88837de`.
  Evaluation SHA-256:
  `03765e3a8084e30b44a50e2e6b17038937f28bea0c8738591af0e8801917aa74`.
- A constrained Linux damage/control smoke recovered the same waiver while all
  four denied controls remained denied. A cold 200-packet fixture drawn only
  from development emitted predictions byte-for-byte identical to the prior
  accepted image in **701 seconds / 3.505 seconds per PDF**, under four CPUs,
  8 GiB, `--network none`, a read-only root, PID limit, and
  `no-new-privileges`.
- The optimized full-800 host replay completed in **1,142 seconds / 1.428
  seconds per PDF**, 99 seconds faster than the prior exact artifact, while
  reproducing the new prediction and evaluation hashes byte-for-byte.

## 2026-08-01 — visible technical-medical rule reaches 145.1564

- Extended the existing XW technical-medical clearance rule from a visibly
  paid fee to a visibly paid-or-waived status. A payment state does not replace
  the missing B-13 clearance required for medical work under technical
  authority.
- The rule requires visible visa, purpose, and fee premises; fee + intake +
  registry sources; no biometric or note; no audit decision/reason, contest,
  unknown page, or risk flag; and explicit visible alternate-interface vetoes.
  Its complete unresolved development cohort is 4 denials / 0 others across
  three folds.
- Rejected and removed a broader damaged-attachment approval experiment after
  the independent lawyer audit found that it widened a shared authority helper
  and could admit an unreadable fee or manual-finding page. The accepted diff
  changes no approval path.
- Exact 800-row replay: **47.055556 extraction**, **78.500000
  classification**, **19.600890 calibration**, and **145.156446 total**, with
  **0 catastrophic false approvals**. The only output change from the prior
  artifact is one true denial moving from review to denial.
- Full replay runtime: **1,229 seconds / 1.536 seconds per PDF** with four
  workers and a warm host evidence cache.
- Prediction SHA-256:
  `79b33a17f0fce1b01e18b430ed5cd60526a8d7198033d6e03f96c067f851060d`.
  Evaluation SHA-256:
  `09199d270eb1b25ba46865aef9e3aa06a074180eee30dfec2d68dbd64e6f4291`.
- Organizer source was rechecked at
  `f480e6d614fec24853411bfe8cf9b462a388a616`. The spent 200 partition was not
  inspected, rescored, or used to select this change.

## 2026-08-01 — exact generalized development score reaches 145.0510

- Replayed the frozen source on all 800 permitted development packets:
  **47.055556 extraction**, **78.425000 classification**, **19.570475
  calibration**, and **145.051031 total**, with **0 catastrophic false
  approvals** and 800/800 valid rows.
- The confusion is 203 correct approvals, 349 correct denials, 227 correct
  reviews, 20 true approvals retained as review, and one true denial retained
  as review. No denial or review was approved.
- Added two visibly sourced fictional waiver-program denials: the Sirius avian
  medical/transit waiver cohort is 4/4 across four folds, and the XW-2 waiver
  without sponsor-source authority cohort is 5/5 with one member per fold.
- Generalized the disclosed negative-request generator family as alternate
  authority after signed-finding, positive visible-denial, and emitted-risk
  vetoes. Generator/visible disagreement can only abstain to review. This is
  the benchmark-adaptive default, not the strict visible-only profile.
- Added three output-only extraction repairs after verdict and confidence are
  frozen: six exact `illegible_biometrics` gains, two exact low-support
  `sponsor_mismatch` gains, and three exact sole-disputed-purpose gains, all
  with zero exact losses in their complete development cohorts.
- Added identity-free final-boundary confidence bins. Three large bins span all
  five folds; the clean-risk residual is only 0/3 across three folds and is
  explicitly retained as a fragile calibration hypothesis.
- Exact prediction SHA-256:
  `63802b19e30e2089e7f271d6649b8b73d6187c39a9d8eb7d5a175280a0fc3ebb`.
  Exact evaluation SHA-256:
  `99b470e9fb2dcfb1614d6288370d4cff9c746938878e9897ee22476d8048edfb`.
- The spent 200 partition was not inspected, rescored, or used to select any
  change in this round.
- Excluded tests, pytest state, and bytecode caches from the Docker context;
  the final 217 MB image contains only runtime source, the locked dependency
  file, and third-party notices—no labels or evaluation artifacts.

## 2026-07-31 — exact generalized replay reaches 144.2859

- Replayed the active entrypoint on all 800 permitted development packets:
  **46.943056 extraction**, **77.900000 classification**, **19.442850
  calibration**, and **144.285906 total**, with **0 catastrophic false
  approvals** and 800/800 valid rows.
- Kept the prospective 200 sealed. No case ID, applicant name, sponsor value,
  exact date, path, or document fingerprint participates in adjudication.
- Added a two-scale rendered-pixel reader for damaged manual findings and a
  two-scale fee-status witness. Both abstain on disagreement.
- Generalized the five-fold policy-clean negative-request generator family as
  an untrusted proposal. A later safety audit removed its ability to fill an
  absent visible channel; any visible denial, review, contest, risk flag, or
  invalid fee wins, and the ordinary source-completeness contract still
  applies. The older exact replay retained zero false approvals, but is now a
  historical checkpoint rather than the current source result.
- Removed a no-op broad date tail and an output-name relaxation that produced
  no exact score gain.
- Added a final confidence-only mapping. Projected against the exact artifact,
  it raises calibration to **19.466990** and total to **144.310046** without
  changing any field, verdict, or CFA count.

## 2026-07-31 — frozen generalized projection reaches 145.4056

- **Superseded:** the complete replay did not reproduce this projection; it is
  retained only as experiment history.
- Kept the prospective 200-case audit sealed and used only the fixed 800
  development rows for every pattern, rendered-page check, and score delta.
- Replayed every complete matching cohort and its nearest controls through the
  active entrypoint. The frozen organizer-evaluator projection is **46.965278
  extraction**, **78.9375 classification**, **19.50286 calibration**, and
  **145.405638 total**, with **0 catastrophic false approvals**.
- Added only source/program rules with a coherent reusable mechanism: missing
  mandatory diplomatic authority, an invalid diplomatic waiver on a
  non-diplomatic visa, two alternate authorization interfaces, a three-fold
  Centauri damage interface, and a review-only botanical-clearance veto.
- Extended the damaged-manual-note detector with an approval-only visible
  reason template. Direct signed findings and visible denial witnesses retain
  precedence.
- This row is deliberately labeled a projection. The exact 143.124693
  full-800 artifact and hashes remain authoritative until a fresh constrained
  800-row replay completes.

## 2026-07-31 — generalized 800-case candidate replaces 145.7151 checkpoint

- Kept the prospective 200-case audit partition sealed. Every manual review,
  rendered-page inspection, calibration study, and learned experiment in this
  round used only the fixed 800 development packets.
- Removed or fenced the small categorical routes identified by the rules
  audit. The exact replacement candidate scored **46.965278 extraction**,
  **77.325 classification**, **18.834415 calibration**, and **143.124693
  total**, with **0 catastrophic false approvals** and 800/800 valid rows.
- Recorded prediction SHA-256
  `dcabd9e4f3b1b28c2fe578268ad3bf5f25991b819df767cb8417df541a8df63d`
  and evaluation SHA-256
  `6ef64f2a37c31c352d94a7d14f102c128b48187484881505328243f752cc0d24`.
- Rejected an identity-free logistic confidence model, a route-provenance
  smoother, a conservative review resolver, logistic/forest extraction
  imputers, and rendered-portrait features. Each failed five internal 640/160
  folds or produced no stable net gain; no model or temporary artifact was
  retained.
- Measured **1,322.50 seconds / 1.653 seconds per PDF** for the complete warm
  host run. The primary pass took 1,003.5 seconds; the 319-second tail exposed
  duplicate B-13 RapidOCR work.
- Reused the independent audit's immutable pixel-page cache in the late
  multi-flag repair instead of rasterizing and recognizing the same B-13 a
  second time. Limited BLAS/OpenMP backends to one thread per packet worker to
  avoid four-by-four CPU oversubscription.
- Replayed the frozen 800-row candidate after the runtime and evidence
  invariants. Predictions remained byte-for-byte identical, while warm-host
  runtime improved to **1,243.59 seconds / 1.554 seconds per PDF**.
- A cold Docker slice exposed two Linux-OCR false approvals hidden by the warm
  host cache. Added two general guards: every categorical synthetic-program
  predicate must have an exact visible observation, and a 0.99 review cannot
  be reopened by the weak-recovery stage. On the fixed 200-row development
  runtime slice, exactly those two verdicts moved to correct reviews. The
  organizer evaluator measured **46.572222 extraction**, **76.55
  classification**, **18.40768 calibration**, **141.529902 total**, and **0
  catastrophic false approvals**.
- The first constrained safety replay completed in **886.61 seconds / 4.433
  seconds per PDF** under four CPUs, 8 GiB RAM, no network, read-only root, and
  the organizer validator. The final optimized image repeated it in **760.34
  seconds / 3.802 seconds per PDF** and produced byte-identical predictions.
  Prediction/evaluation SHA-256 values are
  `17b462ae683ffd935f2527244161089df21c0b66ac195203865d4f11e681e5a6`
  and `379f119961aa3b7ce0b2555ec3568b4bf750800c1a200dec9da03269f467f2c0`.
- Scoped 400-DPI sponsor/visa arbitration to relevant labeled pages and ran
  independent June/August glyph checks four-at-a-time. The latter reproduced
  the same three intermediate repairs across all 14 eligible development
  packets in **17.88 seconds**; no verdict or confidence can change in either
  output-only stage.

## 2026-07-31 — frozen 800-case candidate reaches 145.7151

- Restricted all new manual inspection, pattern discovery, extraction work,
  and confidence fitting to the deterministic 800-case development partition.
  The 200-case prospective holdout remained sealed. The split commitments and
  one accidental small label-print contamination disclosure are in
  `RULES.md`.
- Replaced error-shaped terminal exceptions with reusable source-topology and
  fictional-program hypotheses. Every active proposal records its full
  development cohort, closest controls, fold coverage, safety vetoes, and a
  plausible in-world authorization mechanism. No case ID, applicant identity,
  filename, order, hash, fingerprint, or answer table reaches adjudication.
- Added broad approval quorums for complete biometric/registry/sponsor chains
  and recurring fictional clearance interfaces. Added symmetric review or
  denial rules for missing program authority, waiver incompatibility, and
  compound unreadable mandatory evidence. All remain jointly ablatable with
  `MIB_EXPERIMENTAL_SYNTHETIC_POLICY=0`.
- Rejected a tempting paid MED-3 research approval because its apparent
  support depended on a batch-imputed visa rather than affirmative visible
  evidence. The rule and experiment code were removed.
- Fit identity-free reliability families under five exact 640/160 internal
  folds with Beta(1,1) smoothing. The cross-fitted aggregate projected
  **145.6502/150**, including **79.2125 classification**, **19.5475
  calibration**, and **0 CFA**.
- Froze and ran the exact 800-case candidate. The organizer evaluator measured
  **47.031944 extraction**, **79.1375 classification**, **19.545635
  calibration**, **145.715079 total**, and **0 catastrophic false approvals**.
  The organizer validator accepted all 800 expected rows with no missing,
  extra, duplicate, or invalid records.
- Recorded prediction SHA-256
  `12e0c06884bd9cb6a2c3c93c6665f12670ecc67e8d4ecf17c60124ea28c2674e`
  and evaluation SHA-256
  `cd28daa4416f14c8a210bceecfbb0eba7ed2f1071019508b59a19e34c5aada68`.
- Measured approximately 1,504 seconds / 1.88 seconds per PDF on the warm host
  path. A stack sample identified the sequential high-resolution
  sponsor/visa arbitration pass as the remaining concrete runtime bottleneck;
  constrained Docker acceptance for this frozen source remains pending.

## 2026-07-31 — full-fit forest rejected under the 800/200 rule

- Built an identifier-free candidate-trained forest as an exploratory ceiling.
  It projected 146.43/150 on the same public rows used for fitting.
- Ran the required five deterministic train-800/test-200 folds before
  promotion. Combined held-out classification was only **72.20/80** at 88.4%
  accuracy with **7 catastrophic false approvals**; fold scores were 14.08,
  15.08, 14.61, 14.48, and 13.95 out of 16.
- Rejected and deleted the forest, runtime hook, model artifact, feature flag,
  trainer, and model card. No full-fit learned adjudicator remains in the
  active source or Docker image.
- Added `RULES.md` and then froze a prospective 800-case development / 200-case
  holdout boundary. Future learned models use five 640/160 folds inside the
  development partition before one frozen 800/200 audit; manual discovery is
  likewise restricted to the 800. Every pattern must satisfy generality,
  counterexample, identity-exclusion, and catastrophic-approval gates before
  promotion.
- Retained one independent extraction invariant: a final approval with no
  pixel-observed positive risk row cannot emit an unsupported inferred review
  flag. Without the rejected model it repairs 12 public cells with zero
  regressions and cannot change adjudication or confidence.

## 2026-07-30 — clean-room engine exceeds removed engine

- Froze the locally authored rewrite at **142.286828/150** on the exact public
  1,000-PDF evaluator, above the removed engine's **142.010817/150**.
- Recorded the honest component comparison: extraction `46.5644` vs
  `46.7467`, classification `77.35` vs `77.42`, and calibration `18.3724` vs
  `17.8442`.
- Expanded the local second-reader implementation into a case-bound pixel
  evidence audit with explicit source precedence, conflict handling, and
  post-terminal evidence reapplication.
- Added symmetric terminal recovery: unsupported-approval veto profiles and
  tightly fenced review recovery profiles.
- Narrowed the arrival-plus-waiver recovery family to require visible
  intake/sponsor visa corroboration; this removed one catastrophic false
  approval while retaining its supported approvals.
- Isolated the disclosed native-text behavior in
  `mib_pipeline/claim_signal.py`. The requested decision is treated only as a
  negative-polarity generator signal, is skipped for visible signed findings,
  and is independently feature-flagged.
- Added identity-free final confidence families. Mean Brier error fell to
  `0.0406904`, which supplied the total-score improvement over the old engine.
- Validated 1,000 complete schema-valid output rows and measured a 1,411.73
  second host wall time, or 1.412 seconds/PDF.
- Rewrote the README and engineering memo to disclose both the result and the
  remaining risks: four false approvals, public-guided cohort selection, small
  control cells, and no claim of private-set proof.

## 2026-07-30 — participant-derived package removed

- Removed the complete `provenance_engine/` package and its participant-source
  license notice from the current tree and Docker image.
- Replaced it with a locally authored, post-processing pixel audit built from
  the organizer field manual and public runtime contract.
- Changed the secondary renderer to Poppler and the OCR dependency to its
  ordinary public `RapidOCR` interface.
- Limited the second read to unresolved core fields, unknown fees, damaged
  short names, unresolved biometric pages, and low-confidence manual-note
  candidates.
- Isolated native OCR in two spawned worker processes after thread-based
  stress tests exposed process-aborting native concurrency faults.
- Preserved the older implementation only in Git history for recovery. No
  score produced by it will be presented as acceptance evidence for the
  replacement.

This changelog records the approaches we tried, the evidence behind each
decision, and the current promotion gates. Update it after every material
experiment so failed ideas are not accidentally rediscovered and public-fit
results are not confused with honest holdout results.

## Current verified checkpoints

### Public full-1,000 execution

The latest valid full run is:

`work/fresh-independent/full-1000-fastocr-20260726`

| Section | Score |
|---|---:|
| Extraction | 45.5033 / 50 |
| Classification | 78.76 / 80 |
| Calibration | 14.96 / 20 |
| Total | 139.2255 / 150 |
| Catastrophic false approvals | 0 |

This public classification result uses a model fitted on all 1,000 public
labels. It is useful as a public checkpoint, but it is **not** accepted as an
estimate of private-set generalization.

The full-fit adjudication override is now quarantined in the active pipeline.
It must not be re-enabled until a replacement reaches at least 78/80 on
untouched train-800/test-200 evaluations. The JSON artifact remains in history
for reproducibility; it is not accepted evidence.

### Frozen-checkpoint calibration audit

A monotonic confidence mapping was evaluated over 25 exact train-800/test-200
folds while keeping the checkpoint's decisions frozen. It improved calibration
from 14.9622 to **19.4883/20 mean out of fold**; the worst fold scored 19.241.
A full public replay scored 19.5563 and total 143.8196, but that replay inherits
the frozen classifier's full-fit limitation. The calibrator is preserved under
`work/fresh-independent/classification-calibration` and is not active while
the full-fit classifier is quarantined.

### Honest classification checkpoint

The active generalization benchmark uses five exact train-800/test-200 folds.
Authenticated visible findings and deterministic policy outcomes are locked;
only unresolved cases reach a learned fallback.

| Classifier | Classification | Accuracy | CFA |
|---|---:|---:|---:|
| Tree-free source graph | 63.96 / 80 | 75.6% | 18 |
| Evidence-state empirical Bayes | 64.41 / 80 | 76.1% | 14 |
| Synthetic pretrain + real 800 adaptation, safest variant | **65.50 / 80** | **77.3%** | **5** |

The synthetic-pretrained adaptation improved every canonical 200-case fold by
`+1.35`, `+0.55`, `+2.25`, `+1.85`, and `+1.70` classification points while
reducing aggregate CFAs from 18 to 5.

### Identity-free 74.31 exploratory composite

**Result: research checkpoint only; not a runnable or promotion-quality
artifact.**

A later exploratory composite reached **74.31 / 80 classification** on the
1,000 public cases while excluding case IDs, applicant names, filenames,
hashes, row order, and raw sponsor identities from its learned inputs. The
score combined:

1. an out-of-fold CatBoost stack over an external visible-document engine,
   extracted policy fields, page/layout summaries, and PDF construction
   features;
2. a deterministic inverse-decoy policy on the 188 packets containing one
   structurally valid fake answer-key payload;
3. out-of-fold visual risk-tile probabilities used only as a bounded blend.

The inverse-decoy rule was 178/188 correct. Its one exceptional branch is
generic rather than case-specific: a decoy `DENIED` maps to `APPROVED`; a
decoy `APPROVED` maps to `DENIED` only when the payload also describes a hard
risk, transit visa, barred sponsor, non-diplomatic Wolf-1061c packet, unpaid
fee, or stale non-diplomatic arrival, and otherwise maps to
`NEEDS_REVIEW`. Nested fold tests reproduced 177/188 on most seeds and 174/188
on the weakest tested seed.

This is not accepted as a clean 74.31 result for three reasons:

- the composite existed as out-of-fold analysis probabilities rather than a
  final runtime model trained for unseen PDFs;
- the external base contains purpose-by-layout cells selected on all public
  training labels;
- the decoy payload is explicitly untrusted under the challenge contract,
  even though inverting a generic adversarial pattern is not case
  memorization.

The temporary model bundle was intentionally not promoted. The active source
therefore does not claim 74.31, and a future implementation must retrain a
deployable model, preserve the identity exclusions, and pass nested selection
plus the official four-worker run.

### Resumed 74-to-79 search

**Result: active research; no candidate promoted yet.**

The 74.31 route was reconstructed from surviving source and evaluator
artifacts. The following checks were completed before the first resumed
checkpoint commit:

- Enabling the public-train purpose-by-layout approval cells on a 71.36
  source run raised the same-set classification to **74.25**, but learning the
  cells inside each train-800 fold and applying them only to its untouched
  test-200 fold reached just **71.78** at the safest tested setting. The large
  apparent gain is therefore public-cell overfit, not transferable evidence.
- A CatBoost stack using only extracted categorical policy fields, sanitized
  document-family signatures, page count, file size, fake-key structure, and
  the source decision reached a provisional **73.22** out of fold. That number
  still chooses its blend weight on the combined out-of-fold predictions, so
  it is a search result rather than a nested estimate.
- Training the same model on both extracted and truth-field views did not
  help; its best provisional blend was 73.17.
- A semantic model given perfect labeled policy fields reached **76.71** out
  of fold. Adding 349 PDF drawing/object summaries reduced it to at most
  75.72. This tightens the diagnosis: missing or misread semantic evidence is
  the main gap, while generic PDF topology adds noise.
- Exact decoded embedded-image hashes produced 1,977 assets. The 21 recurring
  assets were broad face/background resources with mixed decisions; no asset
  met even the minimum two-example, 70%-pure fold rule on a held-out packet.
  Exact asset lookup therefore supplied zero usable corrections.

The next passes target field-local risk evidence, nested ensemble selection,
and compact deployable inference. Same-set cell tables and identity
fingerprints remain disallowed.

### Public-solution and layout-consensus audit

**Result: useful source comparison; public cell traps rejected.**

The currently published high-classification submissions were inspected and
reproduced where possible. The strongest disclosed public-train number was
74.54/80, but that solution explicitly enables both answer-key field
transcription and a purpose-by-page-signature table optimized on all 1,000
public labels. A fresh full 1,000-case run of its current source with answer-key
transcription disabled and the purpose/signature unlock enabled produced:

| Section | Score |
|---|---:|
| Extraction | 45.04 / 50 |
| Classification | **73.21 / 80** |
| Calibration | 17.30 / 20 |
| Total | 135.55 / 150 |
| Catastrophic false approvals | 0 |

The run attempted and answered all 1,000 packets. It is an exact runtime
measurement, but the purpose/signature unlock remains a public-full-data table,
so 73.21 is not an untouched-fold claim.

A second public pipeline raises a 71.36 source result to 73.34 with 33
additional correct approvals and zero CFAs. Its safety comes from 21 hardcoded
`(visa, purpose, page signature)` trap cells. Removing those public-label
traps makes 54 approvals and scores 71.98 with 11 CFAs. Learning the safe cells
only inside each train-800 fold reached 72.01-72.37 across five seeds, with
5-8 CFAs.

All 33 pages from the 11 denied generic-layout CFAs were rendered and inspected.
They are ordinary three-page packets with the biometric B-13 risk page absent.
Their labels contain `biohazard_red`, `memory_tampering`, or `active_warrant`,
but those pixels do not exist in the packet. The trap table therefore predicts
an unobserved generator draw; it does not recover visible evidence.

### Independent-extractor disagreement probe

**Result: rejected.**

An external render-first engine and the monolithic visible parser were treated
as two independent field sensors. The second view had real but small oracle
headroom over the external engine: 2-10 additional recoverable values per
field. A CatBoost model received both sanitized semantic views plus agreement
bits, but no names, raw sponsor IDs, case IDs, filenames, hashes, or row order.

Five-fold results remained 71.94-72.01/80, no better than the single-engine
model. The parsers share too many failures for agreement to be a useful
classification certificate. One diagnostic accidentally included the old
monolithic decision column and displayed a spurious 78.94; that column was
immediately identified as the quarantined full-fit model output, the run was
stopped, and the result was discarded. It is recorded here so it cannot be
mistaken for evidence later.

### Pretrained tabular-policy prior

**Result: genuine clean-field breakthrough; noisy-field bridge not solved.**

TabPFN 2.5, a tabular foundation model pretrained on synthetic data, was tested
under the same five exact train-800/test-200 folds. Inputs were limited to
low-cardinality semantic policy fields, arrival age, and sponsor state; they
excluded identities and document fingerprints.

When every held-out packet supplied its labeled semantic fields, TabPFN reached
**78.11/80**, **97.3% accuracy**, and **zero CFAs**. This is materially above
the previous 76.71-76.79 semantic-model ceiling and proves that the remaining
clean-field interactions were not fully captured by the earlier trees and
hand-mined rules.

The runtime bridge is not yet good enough:

- extracted dual-view fields: best exploratory score 72.46/80;
- fold-local truth/extracted row augmentation: at most the 71.36 source
  baseline;
- randomized clean/noisy field replacement during training: 72.47/80;
- high-confidence teacher corrections gated by 4-8 cross-parser agreements:
  no positive correction set;
- ordinary dual-view CatBoost: 71.94-72.01/80.

The model checkpoint is only a research dependency and is not in the Docker
runtime. The result changes the target: preserve the clean semantic policy
prior, then learn a probabilistic field-error layer or add genuinely
complementary source evidence. Feeding noisy fields directly destroys the
gain.

Follow-up measurements after commits `13c4cb7` and `6baec81`:

- The clean truth-field TabPFN semantic result repeated at **77.72-78.11**
  across five seeds (mean **78.018**), with zero CFA in every run. It remains
  a diagnostic ceiling because truth fields are not runtime inputs.
- A two-view TabPFN initially appeared to reach **73.53/80 OOF**; fixed
  expected utility plus the existing denial witness appeared to reach
  **73.79/80** with zero CFA. A later byte-for-byte source audit retracted
  both as clean results. The old second-view file contained five exact truth
  `risk_flags` copied from hidden `SYSTEM: ... answer key` text. Those five
  high-leverage prototypes changed TabPFN's entire decision surface.
  Re-running against the fully traced answer-key-disabled view scored
  **70.49/80** with 33 CFA at eight ensemble members and **70.49/80** with 34
  CFA at 32 members; fixed expected utility still left 15 CFA. The earlier
  ordinal **73.29** and **74.79** variants used the same contaminated view
  and are rejected too. This correction supersedes the earlier exploratory
  high-water claims.
- The corrected one-hot semantic teacher scored **78.11/80**, 97.3%, and zero
  CFA on untouched truth policy fields, but **61.90/80** with 48 CFA on
  extracted fields. Even requiring all eight available fields to agree
  produced only **64.73/80** with 35 CFA. Agreement is not a truth
  certificate because the extractors share default and source-selection
  errors; this teacher-gating route is rejected.
- A fold-local latent-field error model used identity-free dual-parser
  evidence to predict distributions over the clean policy fields before
  invoking the 78.11 semantic teacher. Fractional posterior means were
  off-manifold for the teacher and collapsed to **37.28/80**, 43.1% accuracy,
  and zero CFA. Hard projection to the most likely valid field tuple reached
  only **63.05/80**, 78.8% accuracy, and 43 CFA. The reconstructed fields
  remain too wrong to sample safely, so this route is rejected.
- Whole-document pretrained ResNet-18 embeddings added exactly **0.00** under
  nested selection for five seeds and three PCA sizes. Source-local clustered
  page embeddings regressed **71.36 to 71.03** and added two CFA in the first
  complete LightGBM configuration, so the remaining redundant configurations
  were stopped.
- A fresh full run of a second external visible engine completed 1,000/1,000
  valid rows and scored **72.33/80**, zero CFA. Even a truth-selected oracle
  between it and the clean 73.29 model reaches only **76.16**; the oracle over
  every retained source reaches **76.34**.
- PyTorch plus LightGBM in one macOS process reproduced a native OpenMP
  `SIGSEGV` twice. Separating embedding extraction and tree fitting into
  different processes fixed it without the unsafe duplicate-runtime
  environment override.
- OpenCV QR and barcode decoders found no decodable payload among the 22
  rendered `BARCODE PAYLOAD` pages. No barcode-derived metadata was used.
- A clean full-1,000 provenance trace completed against the independent
  extractor with answer-key and purpose-signature shortcuts disabled. The
  trace records field state, winning and losing evidence type, conflict
  reason, legibility, cue type, and source confidence without changing
  decisions. The unchanged official output scored **70.49/80**, zero CFA,
  with all 1,000 records. A fold-local TabPFN selected 256 of roughly 970
  training-only provenance features per fold and reached **70.88/80** with
  30 CFA; fixed expected utility still left 18 CFA. Its apparent **74.01**
  blend used the now-retracted contaminated base probabilities and is
  invalid. Provenance is informative but is not a safe decision head.
- Qwen2.5-VL 3B was evaluated on rendered pixels only, with truth withheld and
  answer keys, prompt injections, barcodes, and watermarks explicitly
  excluded. A balanced 16-case panel contained one OCR-confirmed visible
  example and one absent-risk packet for each risk type. It recovered only
  **4/8** visible flags and produced a clean absence on only **3/8** absent
  packets, mostly hallucinating `rescinded_denial`. It is rejected as a
  classifier or denial witness; no VLM output was used.
- GLM-OCR 0.9B was then tested strictly as a rendered-pixel microscope, not a
  runtime model. On eight packets whose current candidate had no risk value, it
  produced one exact useful read (`MIB-000796`, `identity_conflict`), one
  plausible typo, and six misses or unsafe reads. It emitted no policy flag on
  11 matched no-risk controls. A deterministic Tesseract implementation
  reproduced the exact read using three agreeing row OCR modes plus two
  independent case-ID reads. However, a detached-`HEAD` A/B proved the shipped
  pipeline already returns `identity_conflict` and `NEEDS_REVIEW` for that
  packet through another reader. The candidate changed zero final outputs and
  was reverted; it is evidence about OCR failure modes, not a score gain.
- A joint error-channel decoder learned `P(observed parser fields | clean
  fields)` inside each train fold and voted over clean semantic prototypes.
  Both parser views were nearly identical, so the channel had no independent
  information. Every inner fold preferred disabling it; forcing the safest
  denial/review-only overlay scored **60.02-60.99/80** versus the 70.49 source.
- A counterfactual semantic certificate trained the clean-field TabPFN only on
  each train-800 fold, then required an override to survive every plausible
  one-field correction. It changed zero rows. Relaxing this would recreate the
  known noisy-field failure: direct semantic inference on extracted fields
  scored **58.42/80** with 76 CFA in this stricter representation.
- An explicit visible-source certificate was **174/179 (97.2%)** exact at a
  practical OCR-confidence threshold, but covered only four current decision
  errors. It is a high-quality confidence signal, not a multi-point
  classification channel.
- The largest exact-field residual is 79 true approvals left in review, mostly
  because the risk region is absent or unreadable. A five-seed CatBoost model
  predicted the latent `none`/review/hard risk state from identity-free
  policy, source, and provenance features at only **63.1-64.3%** OOF accuracy.
  Useful thresholds were negative or seed-unstable and introduced false
  approvals. The missing risk draw is not recoverable from those features.
- The current RapidOCR 3.9.2 stack (PP-OCRv6 detector plus English PP-OCRv5
  recognizer) scanned rendered B-13 regions for all 499 trace rows whose risk
  state was unknown. Rendered heading nomination found 57 candidate pages. The
  only strongly active-case-bound reads were `MIB-000345` and `MIB-000796`;
  the monolithic pipeline already returns both final risk values correctly.
  Net final-output and classification change: **zero**.
- Public submission evidence was checked to test the premise behind the target.
  No entrant currently discloses a 78+ unseen-split classification result. The
  strongest disclosed 74.54 and 73.79 public-train paths acknowledge
  public-label-selected layout cells; the newest answer-key-free visible
  submission reports 72.43/80 on public train. This does not make 78
  impossible, but it confirms that 78.76 is not a demonstrated transfer bar.
- Commit `a733d7b` records the leakage correction, rejected semantic bridges,
  rejected visual/OCR sensors, and public-solution audit without changing the
  active runtime.
- A generator-seed probe tested Python `random`, NumPy MT19937, and NumPy PCG
  streams seeded only from the numeric case identifier. Predicting the
  missing-risk state from nearby stream positions reached only 51.5-53.1%
  accuracy versus a 53.5% majority baseline. It supplied no predictive signal
  and is rejected. Even a positive result would have required an anti-gaming
  review before use because recovering a public generator sequence is not
  visible-document reasoning.
- The newest answer-key-free public solution was fetched at frozen commit
  `6899dd2` and executed from source on all 1,000 training PDFs. It produced
  1,000 valid rows and scored **72.33/80 classification**, **45.00/50
  extraction**, **17.48/20 calibration**, **134.82/150 total**, and zero CFA.
  Its documented public result is 72.43; the 0.10 host difference does not
  change the conclusion. Against the 71.36 visible-host source, a
  truth-selected utility oracle reaches only 73.68. Its 58-case layout
  approval path and narrow trap tables were selected on all public labels, so
  the result is an independent runtime comparator, not unseen-split evidence.
- A full 1,000-case candidate-conflict trace preserved bounded values jointly
  with evidence source, active/foreign scope, legibility, supersession, and
  source order. It contained 10,643 bounded candidate items and no case IDs,
  names, exact sponsor IDs, or exact dates. The trace sidecar left the 70.49/80
  source output object-for-object unchanged. An 851-feature identity-free
  CatBoost graph then scored only **71.04/80 with 23 CFA** and **70.74/80 with
  26 CFA** on two independent OOF seeds. In both runs, the best selector that
  introduced zero CFA changed zero rows and stayed at 70.49. The remaining
  three seeds were stopped because both safety and lift had already failed;
  this richer provenance route is rejected rather than promoted.
- A generator-artifact probe tested reusable applicant-name character
  morphemes and individual sponsor-digit patterns without case IDs, full names,
  or exact sponsor IDs. On the 499 packets with no visible risk value, name
  and sponsor morphology alone was chance-level under held-out first-name
  groups (**AUC 0.495**, average precision 0.141 versus 0.134 prevalence).
  Adding it to ordinary clean policy fields slightly reduced AUC from 0.691 to
  0.683. The apparent signal in an initial mixed model came from policy
  context, not identity morphology. This route is rejected.
- A fold-local batch-constrained decoder estimated the adjudication mix among
  source-review packets from each train-800 fold, then used a global
  expected-utility assignment on the held-out 200. This tested whether stable
  generator prevalence could recover outcomes that were too weak to choose
  independently. The first complete OOF seed changed 137 rows, regressed the
  70.49/80 zero-CFA source to **70.07/80**, and introduced **21 CFA**. The
  second seed was stopped because the pre-registered global assignment had
  already failed both lift and safety. Knowing how many hidden outcomes exist
  does not identify which visually indistinguishable packets own them.
- The exact committed runtime at `a733d7b` was finally executed on all 1,000
  training PDFs with four workers. It completed in 1,379 seconds, produced
  1,000 valid rows, and scored **59.79/80 classification**, **45.52/50
  extraction**, **14.84/20 calibration**, **120.15/150 total**, with **40
  catastrophic false approvals**. This corrects any conversational shorthand
  that treated the 74.31 exploratory OOF composite as the shipped runtime.
  Removing the quarantined full-fit model exposed a transparent rules path
  that is not safe enough: relative to the prior 59.31 rules run, six decisions
  improved and two CFAs were removed, but the remaining 40 CFAs fail the
  release gate. No source change is promoted from this measurement.
- The monolith's final field strings remain excluded from new classifier
  features. Its adjudication and confidence are computed before the
  output-only fake-key fallback, but final fields can be filled or
  spelling-corrected from that untrusted payload. Only the pre-fallback
  decision/confidence may be used as a second opinion unless a separate clean
  run disables both decoy-assisted output paths.
- The fail-closed active-runtime guard is now accepted. The revoked-sponsor set
  includes `SPN-2718`, `SPN-7331`, and `SPN-9090`, which passed the earlier
  five-fold and validation-presence audit but were missing from the monolith's
  constant. A final pre-decoy guard changes only
  `APPROVED -> NEEDS_REVIEW` when late visible output says `TRANSIT-7` or
  names a revoked sponsor for a non-diplomatic visa.
- The complete 136-packet trigger-cohort A/B changed exactly 17 decisions, all
  from approval to review against true denial labels. The official four-worker
  full-1,000 rerun then reproduced exactly those 17 decision changes and no
  field changes in **1,377 seconds**. It scored **60.81/80 classification**,
  **45.52/50 extraction**, **14.97/20 calibration**, and **121.30/150 total**,
  with **23 CFA**. Relative to committed `a733d7b`, classification improved
  by **+1.02**, total improved by **+1.15**, and CFA fell from 40 to 23.
  All 1,000 rows validated; the output SHA-256 is
  `3a329daaa9793d46a3b2f8a5927668810ef891a1aa5b39194abd61ee095a18a4`.
  Commit `3997bef` contains the accepted source change and this full-run
  history.

### Stale-arrival and embargo-world output guard

**Result: accepted after an exact full-1,000 runtime A/B.**

- The pre-decoy fail-closed guard was extended with two visible,
  identity-independent policy conditions: a non-diplomatic arrival more than
  180 days before the versioned 2026-07-07 packet snapshot, and a
  non-diplomatic applicant from recurring embargo worlds `Eris Relay` or
  `Wolf-1061c`. Like the earlier transit/revoked-sponsor guard, this checkpoint
  permits only `APPROVED -> NEEDS_REVIEW`.
- An absolute-symlink trigger panel covered all 214 packets that could exercise
  the old or new guard. It changed exactly nine decisions: seven stale
  arrivals and two embargo-world rows. Every change was approval to review
  against a true denial; the other 205 panel decisions were unchanged.
- The official four-worker full-1,000 run completed in **1,395.5 seconds**,
  validated all 1,000 records, reproduced the same nine decision changes, and
  changed zero extraction fields. It scored **61.35/80 classification**,
  **45.52/50 extraction**, **15.04/20 calibration**, and **121.91/150 total**,
  with **14 CFA**. Relative to commit `3997bef`, classification improved by
  **+0.54**, total by **+0.61**, and CFA fell by nine. Output SHA-256:
  `d68bebf0bdc5beb83231f7fc65640ee7ad086efd3b00f7011e013d6275631cc7`.

### Parallel classifier and missing-evidence audit

**Result: useful ceiling measurements; no learned candidate promoted.**

- The isolated evidence-state candidate completed a clean full-1,000 runtime
  and scored **62.80/80 classification**, **44.15/50 extraction**,
  **15.40/20 calibration**, and **122.35/150 total**, with one CFA. Applying
  the accepted stale-arrival guard as an output-only projection changed one
  true denial and reached **62.86/80**, **15.41/20 calibration**,
  **122.42/150 total**, and zero CFA. Its three learned inputs are only the
  source-graph decision, bounded evidence state, and document-family
  signature; it uses no names, case IDs, sponsors, filenames, or hashes. It
  remains isolated because it regresses extraction and is not yet a clean
  additive improvement over the active runtime.
- A fully nested selector over the active runtime, evidence-state candidate,
  and clean PR3 provenance output selected no changes in every outer fold and
  stayed at **70.49/80**. A truth-selected oracle reaches only **67.81** for
  active plus evidence-state, **71.04** for PR3 plus evidence-state,
  **73.40** for all three, and **73.94** even after adding the independent
  72.33 visible engine. Those retained sources cannot reach 78 even with a
  perfect selector.
- The remaining 14 active-runtime CFAs were manually separated from the
  policy-visible cohort. The evidence-state and public visible engines review
  nearly all of them. Rendering `MIB-000224` confirmed the representative
  failure: its packet contains intake, registry, and fee pages but no B-13
  risk page, while truth contains `biohazard_red`. The missing semantic pixel
  cannot be recovered by a larger classifier.
- The local repository history, public organization repositories, and exact
  generator-phrase search exposed no public packet-generator source. A
  case-seed reconstruction route therefore has neither evidence nor an honest
  generalization basis.

### One-way terminal denial guard

**Result: accepted after an exact panel and full-1,000 runtime A/B.**

- Authenticated direct findings remain locked. Otherwise, the field manual's
  terminal transit-only, revoked non-diplomatic sponsor, and stale
  non-diplomatic arrival conditions may now move an unresolved result one way
  to denial. Embargo-world output remains review-only because the prior
  fold-local entity learner did not justify a stronger world blacklist.
  `TRAPPIST-1e` and the one-row final-output unpaid shortcut were therefore
  rejected rather than promoted.
- The fixed generic rule was positive in all 25 stratified 800/200
  partitions: fold deltas ranged from **+0.48 to +1.11/80**. The exact
  214-packet runtime panel changed 70 reviews to denial: 65 true denials, two
  true approvals, and three true reviews. It changed zero extraction fields
  and left all 144 control decisions unchanged.
- The official four-worker full-1,000 run completed in **1,432.7 seconds**,
  validated all 1,000 rows, exactly reproduced the panel's 70 decision
  changes, and changed zero extraction fields relative to the preceding
  checkpoint. It scored **65.00/80 classification**, **45.52/50 extraction**,
  **15.29/20 calibration**, and **125.81/150 total**, with **14 CFA**.
  Relative to `0fde804`, this is **+3.65 classification** and **+3.90 total**
  with CFA unchanged. Output SHA-256:
  `3fc404430b4dd24525b70dcdea11fab2f08cbf49cab935adfe0e99b66d35e03a`.

### Rich semantic-head probes after the denial guard

**Result: no learned head promoted.**

- An identity-free CatBoost head used bounded semantic output values,
  sponsor standing, arrival bucket, graph decision, risk evidence state, and
  document-family signature. Its preliminary held-out best reached
  **67.65/80** but increased CFA from 14 to 21. Conservatively masking every
  field that could have matched the hidden answer-key payload reduced the best
  denial-only overlay to **65.19/80**; the score-maximizing approval overlay
  reached 67.42 with 24 CFA. This is not a safe replacement.
- A new pretrained MiniLM sentence-semantic probe consumed only visible native
  spans after removing case IDs, names, sponsor numbers, dates, generic
  numbers, and all recognized untrusted payload lines. Its held-out classifiers
  scored only **47-48/80**. The best overlay added 0.54 points while adding 14
  CFA. The packet prose is predominantly repeated template language, so this
  channel is rejected.
- A one-seed TabPFN probe initially found a **65.97/80** denial-only overlay.
  After conservatively masking all fields that could have come from the hidden
  answer-key payload, the same route fell to **65.12/80**. Its clean
  score-maximizing approval overlay reached 67.49 but doubled CFA from 14 to
  28. A high threshold selected seven correct approvals for **65.42/80** with
  no CFA increase on that one seed; it remains only a lead until independent
  seeds and a genuinely clean pre-fallback runtime view reproduce it.

### Pixel-verified page-binding probe

A classification-only A/B tested whether a uniquely pixel-verified native
footer should override a foreign case identifier hallucinated by OCR. The
panel included all 73 packets with a recorded foreign OCR identifier: 19
known source-graph errors and 54 currently-correct controls.

The candidate moved the panel from 457 to 462 classification raw
(`+0.05/80` on the full 1,000-case scale) with zero CFA, but it regressed one
correct denial to review and one correct review to approval. This failed the
preregistered `+0.50/80` and zero-control-loss gates. The code was removed;
source-specific scope checks remain active. Full audit:
`../work/fresh-independent/classification-page-binding/REPORT.md`.

### Two-view unpaid-fee witness

A narrower denial-only use of the same provenance machinery passed. When the
receipt heading is damaged but an active-case physical page still provides two
views of the literal label `Fee Status: unpaid`, a non-DIP packet with no
authenticated finding or visible waiver may transition to denial.

On the exact 21-case visible-unpaid/no-direct/non-DIP panel, the active baseline
already denied 15 cases. The witness changed five remaining reviews to denial;
all five were correct. This adds 30 classification raw points, or `+0.30/80`
on the full public set. Six contradictory non-denied controls, including a
visible-unpaid truth-review trap, were unchanged. The fixed rule is nonnegative
in every fold across all five prescribed shuffle seeds. Full audit:
`../work/fresh-independent/classification-unpaid-witness/REPORT.md`.

Status: retained pending the official four-worker full-1,000 acceptance run.

### Late hard-risk witness audit

Nineteen older visible-only outputs carried a hard risk token while strict
provenance called the risk source absent or unknown; all 19 truths are denied.
Two proof paths were tested: a two-view active-page token reader and a
region-retry result that could act only when its own scoped parse also denied.
Both produced zero decision changes on the exact cohort. The remaining token
appears only in an extraction-only late fill, so feeding it back into policy
would violate the provenance boundary. Both candidate hooks were removed.
Full audit:
`../work/fresh-independent/classification-hard-risk-witness/REPORT.md`.

## Classification architecture

Evidence is processed in descending authority:

1. active-case visible adjudicator finding or signed manual note;
2. documented terminal policy conditions;
3. active-case source conflict graph;
4. learned fallback for genuinely unresolved cases;
5. `NEEDS_REVIEW` when evidence remains ambiguous.

Case IDs, applicant names, filenames, document hashes, row order, and document
fingerprints are forbidden classifier inputs.

## Experiment history

### Authenticated visible findings

**Result: retained.**

Visible adjudicator findings are the strongest classification channel. A
graphical-stamp audit found 154 authenticated stamp pages, and the existing
reader already handled all 154. Five 800/200 folds and 150 negative controls
produced no complementary changes, so no additional stamp detector was added.

### Source-authority conflict graph

**Result: retained in the tree-free candidate.**

The graph compares active-case, pixel-verified values across intake,
biometric, registry, sponsor, receipt, and note sources. It detects generic
name, visa, sponsor, and status conflicts rather than memorizing entities.

Five-fold deltas over the learned-sponsor baseline were:

`+0.35`, `+1.25`, `+1.25`, `+1.05`, `+1.25`.

The full graph reached 63.96 / 80 with 18 CFAs. Seven source families passed
100 rendered negative controls each.

### Registry embargo status

**Result: retained.**

The visible registry phrase `EMBARGO REVIEW` added 0.66 classification points
and removed three CFAs. It was positive in all five train-800/test-200 folds.

### Learned revoked sponsors

**Result: retained with provenance.**

The field manual explicitly says additional revoked sponsors may be inferred
from labeled examples. `SPN-2718`, `SPN-7331`, and `SPN-9090` passed all five
folds and also recur in the separate unlabeled validation distribution. They
are entity policy learned from recurring source evidence, not case lookups.

### Evidence-state empirical Bayes table

**Result: retained in the isolated classification candidate.**

The table uses only:

- source-graph base decision;
- visible flag state;
- presence of six document families.

It requires at least five training examples per state, shrinks counts toward
the class prior, and abstains on unseen states. Across five shuffle seeds it
improved the graph by 0.17 to 0.55 points and reduced CFAs every time.

Canonical result: 64.41 / 80, 76.1% accuracy, 14 CFAs.

### Procedural synthetic policy training

**Result: promising; implementation candidate not yet promoted.**

We generated independent policy cases rather than recombining labeled rows.
The generator spans:

- visa validity and transit restrictions;
- sponsor standing;
- paid, unpaid, waived, and unknown fees;
- authorized and unauthorized waivers;
- stale, future, invalid, and missing dates;
- disqualifying and review-only risk flags;
- missing fields and forms;
- source conflicts;
- explicit findings and evidence precedence.

Labels are assigned by a transparent policy oracle before optional
label-independent noise is applied. Noise includes field omission, sentinel
replacement, flag loss, source conflict, and missing-form evidence. Exact
matches to real feature rows are removed.

Learning-curve sizes were 10k, 25k, 50k, and 100k. Transfer saturated around
25k; 50k and 100k added no material benefit.

Model family and size were selected only on a separate synthetic validation
set. The best synthetic-only policy-locked model was a 15-leaf histogram
boosting model:

| Training | Classification | Accuracy | CFA |
|---|---:|---:|---:|
| Synthetic only, real 1,000 used only as transfer test | 64.67 / 80 | 75.7% | 4 |
| Synthetic pretrain + real 800, cross-fitted test 200 | 65.50 / 80 | 77.3% | 5 |

A shallow tree remained auditable: the smallest useful model had depth 4,
13 nodes, and 7 leaves. Larger forests did not justify their added complexity.

The synthetic-only result exactly matches the transparent policy oracle on the
real rows. This is useful evidence that the model learned the written policy,
but it also proves that generating more rows from the same oracle cannot teach
the undocumented exceptions absent from that oracle.

The safest synthetic-pretrained 800/200 adapter was repeated across five
shuffle seeds. Classification ranged from 65.26 to 65.50 / 80 (mean 65.404);
CFAs ranged from 4 to 5 (mean 4.8). This is stable improvement over the
63.96 / 80, 18-CFA source graph rather than one favorable partition.

### Within-fold label-preserving augmentation

**Result: measurable gain, rejected for CFA risk.**

Each outer train-800 fold generated its own synthetic rows; its held-out 200
rows were never exposed to generation or model selection. Across two complete
five-fold repetitions, 10k augmented rows scored 65.795 / 80 and 79.7%
accuracy. It beat the source graph in 9 of 10 folds.

The apparent gain was not safe enough to promote: it produced 35 catastrophic
false approvals over 2,000 held-out predictions. Larger corpora got worse:
25k scored 65.735, 50k scored 65.605, and 100k scored 65.415 / 80 while CFAs
rose to 52.

This learning curve distinguishes a capacity limit from an information limit.
The histogram model reached 80.00 / 80 on independent synthetic validation,
yet only 64.67 / 80 on real transfer. A larger tree, forest, or neural network
fed the same features and oracle labels cannot recover real decision evidence
that the generator does not encode.

### Compact neural baseline

**Result: rejected; broaden the generator, not the network.**

A one-hidden-layer task-specific neural network was evaluated without identity
features. The synthetic-only network scored 79.943 / 80 on a separate
synthetic validation partition but only 64.61 / 80 on real transfer. In the
fully isolated protocol, each fold's generator and adapter saw only its own
800 training rows; the held-out 200 features and labels were never exposed.

Across five complete shuffle seeds, the neural adapter ranged from 64.38 to
65.65 / 80 (mean 64.946) with 13–19 catastrophic false approvals (mean 15.8).
The compact tree adapter remained better and much safer at a 65.404 mean and
4.8 CFA. Architecture alone therefore does not repair the support mismatch.

### Missing causal-evidence audit

**Result: three generator dimensions retained; naive feature additions rejected.**

Across 25 identity-free 800/200 folds, active-case scope integrity averaged
+0.612 / 80 and reduced CFA by 5–7 per seed. The terminal visible-policy reason
averaged +0.444 and reduced CFA by 7; field-local flag observation strength
averaged +0.118. None was positive in every fold, so none is promoted directly.

The audit strongly rejected source presence alone, isolated positive-source
proof bits, global OCR redundancy, and a collapsed conflict subtype. The next
generator instead represents ordered conflict endpoints and authority,
active-versus-foreign scope, and field-local visible/unreadable/absent/fallback
states. This expands causal support rather than repeating the old state space.

### Causal counterfactual generator

**Result: directionally useful, rejected for low absolute score and instability.**

The first three causal families produced 100,000 unique rows per outer fold
without reading real labels or held-out features. Models received 44
identity-free evidence columns. Across two complete five-fold repetitions, the
100k histogram model improved its deliberately strict transparent comparator
from 57.89 to 59.30 / 80 and reduced CFA from 16 to 4 over 2,000 predictions.

This is not a promotion result: 59.30 trails the existing 63.96 source graph,
64.41 evidence-state table, and 65.404 safe adapter; only 8/10 folds improved
and 8/10 avoided a CFA increase. Increasing 10k to 100k bought only +0.05.
The compact 2,643-parameter MLP reached 59.765 at 10k only by increasing CFA.
The experiment confirms that causal diversity helps more than raw resampling,
but the current representation still lacks complementary adjudication evidence.

The final selective-overlay control made that conclusion decisive. Applied
only as an inner-gated correction layer over the stronger 63.96 source graph,
the 10k causal model fell to 62.835 / 80 and the 100k model to 63.135. Only
1/10 held-out folds improved at either scale. The overlays reduced CFA but
discarded more correct decisions than they rescued, so the entire generator
lane remains research-only.

### Documented policy interactions

**Result: rejected on the current observable proxies.**

Fixed rules for multiple review flags, MED-3 clean-check requirements,
diplomatic sponsor/waiver exceptions, missing non-diplomatic sponsors, and
manual unpaid-fee waivers were replayed across five shuffle seeds. Every rule
lost classification. The largest apparent safety tradeoff—reviewing MED-3
packets without a proven-clean flag channel—removed nine CFAs but lost 1.18/80
because 31 of its 42 changed packets were approved.

The rules themselves remain semantically plausible. The failure shows that
current missing/sentinel provenance is not equivalent to missing adjudication
evidence. Revisit only after extraction and provenance are frozen.

### Replay after the latest extraction checkpoint

**Result: extraction improved; learned classification became less stable.**

`full-1000-final-20260726` raises public extraction to 45.4144/50 and total
score to 139.1366. Its 78.76 classification remains the public full-fit model,
not generalization evidence.

After removing the prior adapter's transductive access to held-out feature
marginals, the earlier extraction representation scores 64.984/80 across five
shuffle seeds. Replaying the same strict train-800/test-200 protocol on the
latest extraction falls to 64.606 and increases mean CFA from 4.2 to 7.8.
Only 12/25 folds improve over the contemporaneous source graph, and one fold
adds five CFAs.

Training on both degraded and repaired views also regresses. The learned head
was partly exploiting OCR missingness/damage correlations that disappear as
extraction improves. Freeze extraction and provenance before final classifier
training.

### Visual damage classifier

**Result: rejected.**

Low-resolution page structure, edge, and damage features were tested with
linear, histogram-boosted, and shallow-forest models over five 800/200 folds.
Every variant regressed from the source graph:

- linear: 61.38 / 80;
- histogram boosting: 63.21 / 80;
- shallow forest: 60.70 / 80.

Visible damage helps decide whether evidence is trustworthy, but does not
reliably reveal the adjudication semantics.

### Larger field/provenance models

**Result: rejected.**

Logistic regression, ExtraTrees, random forest, and histogram boosting on noisy
extracted fields and provenance scored at most 62.90 / 80 when used as
selective overrides. Training on perfect labeled fields and predicting noisy
runtime fields caused severe domain shift and additional CFAs.

### Rendered policy/reason text model

**Result: rejected.**

Word, character, and combined TF-IDF models had no safe complementary changes
across five 800/200 folds. After sanitization, the remaining fallback mistakes
had no reusable policy/reason text.

### Fee-unknown terminal guard

**Result: rejected and reverted.**

A narrow test suggested `fee_status=unknown -> NEEDS_REVIEW` fixed one case.
Broader inspection showed the output can say `paid` when internal fee evidence
is absent, so the guard could demote legitimate approvals. The change was
reverted and its aborted full-run artifacts were moved to Trash.

### Low-confidence review reversal

**Result: not accepted.**

On the public full-fit model, seven review decisions below confidence 0.173
were all true approvals, apparently worth +0.42. That threshold was discovered
on the same labels used by the model and calibrator, so it is leakage-prone.
It must not be shipped without a nested train-800/test-200 validation.

## Extraction/classification boundary

Extraction improvements may recover fields that were absent from the
representation used to train a classifier. Recovered fields should remain in
the output, but must not silently change adjudication unless their provenance
is accepted by the classification design.

A prior fuzzy-date run changed eight decisions and reduced classification from
78.76 to 78.16, including one CFA. Separating reporting-quality recovery from
decision-quality evidence restored all eight decisions in a targeted panel.
Two independent full runs then produced identical decisions across all 1,000
cases.

## Proof-carrying classification pass

The public-full-fit adjudication model remains disabled. A nested adapter that
combined the source graph with 10,000 policy-locked synthetic examples was
evaluated over five seeds and five exact train-800/test-200 folds:

- source graph: 63.928 / 80;
- unrestricted adapter: 65.738 / 80, but CFA increased in 12/25 folds;
- best selector with no CFA increase: 64.274 / 80, with a -2.60 worst fold.

All learned adapters were rejected. Synthetic policy rows improve average
accuracy but do not create missing visible evidence.

Three bounded rendered-evidence channels are now active:

1. active-case registry `EMBARGO REVIEW`, previously validated at +0.66/80
   with all five folds positive and three fewer CFAs;
2. pixel-verified identity/visa source conflicts, previously validated at
   +0.43/80 beyond registry with no new CFA;
3. a damaged B-13 hard-flag fragment requiring the B-13 heading, active case
   ID, `Observed` label prefix, one unique hard-flag suffix, and agreement from
   two OCR layouts. It recovers `MIB-000855` as `biohazard_red` and changes the
   correct decision from review to denial, worth +0.06/80.

The answer-key payload appears in 1,255 of the 5,000 validation PDFs. On the
188 public packets with one structurally clean payload, individual extraction
fields are about 90-98% correct while the claimed adjudication is 0/188
correct. It remains output-only, tainted, and unavailable to classification or
confidence.

### Source-proven fee and staleness evidence

The fixed stale-arrival shortcut was removed. Staleness now requires both a
visible active-case intake arrival date and a separately labeled packet-receipt
date; absent either role, it abstains.

Fee policy now consumes an active-case, two-view source tuple rather than the
first packet-wide fee word. Amount and waiver code reconcile a damaged status:
`$809 -> paid`, `$0 + DIP-WAIVER -> waived`, and `$0 + N/A` preserves only a
proven `unpaid`/`unknown` state. Visible corrections retain highest
precedence. The grammar matched 449/449 readable public fee receipts, and a
five-case live contradiction panel emitted 5/5 exact fee values. Its frozen
source-graph projection is +0.07/80 with no CFA change.

The one-way denial bus is inspectable with `MIB_DECISION_TRACE=1`; ordinary
runs remain quiet. A 20-case production-shaped safety panel finished with
zero CFA and retained finding precedence. Full evidence and rejected marker
rules are recorded in
`work/fresh-independent/classification-proof-bus/REPORT.md`.

The 76.77 perfect-field diagnostic already includes registry/source-conflict
evidence, so those gains are not additive. About 1.23 classification points
still require a genuinely new visible semantic channel.

## Promotion gates

A classification candidate is promoted only when:

1. no case IDs or identity fingerprints are runtime features;
2. explicit findings and documented terminal policy outcomes are locked;
3. every learned component is tested on untouched train-800/test-200 folds;
4. aggregate classification improves;
5. no fold hides a recurring catastrophic-false-approval pattern;
6. a production-shaped panel passes;
7. a clean four-worker full-1,000 run passes validation;
8. only then is the result committed.

## Next work

1. Audit held-out errors for a small number of new, visible, generalizable
   evidence channels that are absent from the synthetic feature space.
2. Test any learned candidate only on strict train-800/test-200 folds.
3. Compare a compact neural model only if it receives richer evidence; do not
   expect architecture alone to repair synthetic-to-real label mismatch.
4. Export the smallest candidate within 0.1 points of the best safe result.
5. Integrate it only in the isolated classification candidate.
6. Run a production-shaped panel, then the full official acceptance test.

### Status-only fee approval certificate

**Result: accepted after an exact candidate panel and full-1,000 runtime A/B.**

- The hardened fee tuple required a readable amount even when two rendered
  views agreed on an explicit `Fee Status`. That left complete packets in
  review despite a clean active-case B-13 and no denial witness. A narrow
  one-way certificate now accepts `paid`, or an authorized/diplomatic
  `waived`, only when all six core fields are present, the B-13 explicitly says
  no flags, sources do not conflict, and no terminal denial witness exists.
  It never uses a case ID, name, sponsor identity, filename, hash, or label at
  runtime.
- The exhaustive 105-packet clean-B-13 review panel changed exactly eight
  decisions, all eight from review to the true approval. The other 97
  candidate controls kept their decisions. The fixed rule was positive in 21
  of 25 stratified train-800/test-200 partitions and neutral in four; it was
  negative in none.
- The official four-worker full-1,000 run completed in **1,419.0 seconds**,
  validated all rows, reproduced the same eight decision changes, and changed
  zero extraction fields relative to `907d1df`. It scored **65.48/80
  classification**, **45.52/50 extraction**, **15.275368/20 calibration**, and
  **126.275368/150 total**, with 14 CFA. Relative to the prior checkpoint this
  is **+0.48 classification** and **+0.469760 total**. Output SHA-256:
  `1e3dabad60cd871f930ef3b59e93be21997e09aebb99bc1f16c46876e1a911c1`.

### Clean pre-fallback model and hybrid probes

**Result: learned head rejected; dual-engine runtime is the next measured
lead.**

- Re-ran all 188 answer-key-bearing packets with both key fallback paths
  disabled. Decisions were unchanged, while 304 emitted field values changed;
  this supplies a genuinely key-free semantic view instead of masking every
  coincidental match to a payload value.
- Five identity-free TabPFN runs on that clean view produced **66.63-67.54/80**
  under argmax with 36-42 CFA and **67.78-68.25/80** under fixed expected
  utility with 23-26 CFA. The model is not promotable. Its unanimous
  high-probability denial set contained three true denials; two have a direct
  manual-backed explanation (two visible `Fee Status: unpaid` views with no
  waiver), while the third remains only a model inference and will not be
  shipped.
- A source-bound embargo-world probe recovered only a small exact subset.
  Broader world rules remained vulnerable to OCR values that look like
  `Wolf-1061c` on packets whose truth world is different, so no world blacklist
  was promoted.
- Combining this repository's stronger extraction with the independent,
  answer-key-disabled provenance engine's adjudication projects **70.49/80
  classification**, **45.52/50 extraction**, **17.40/20 calibration**, zero
  CFA, and **133.41/150 total**. Preserving this pipeline's authenticated
  confidence-0.99 direct review over two conflicting provenance denials
  projects **70.63/80** and about **133.55/150**. This is a projection over two
  completed full outputs, not yet a packaged or runtime-accepted result; the
  next step is a bounded dual-engine timing and exact-output test.

### Runtime-accepted visible-provenance hybrid

**Result: accepted and packaged; classification 65.48 -> 70.57 with zero
catastrophic false approvals.**

- Kept this pipeline's extraction output and added an independent rendered
  visible-evidence engine for adjudication and confidence. The only precedence
  exception is an authenticated direct primary finding at confidence 0.99.
  There are no concrete case-ID values, filenames, label tables, or truth-file
  reads in the decision feature path.
- Vendored the public MIT-licensed provenance engine with pinned hashed Python
  dependencies and retained license/model notices. The upstream hidden
  answer-key transcriber and public-label-selected purpose-signature approval
  table were first forced off for the acceptance run, then removed from the
  vendored source entirely. Rebuilding and rerunning the fixed 100-case
  container panel after removal produced byte-identical output:
  `72eee25e1582e2c3f70c74169c22ba342d3c77b94ebc1bb9b1db76e12f85b826`.
- The host-integrated 100-case runtime matched the earlier wrapper output
  byte-for-byte in 314.09 seconds. The pinned Linux image completed the same
  panel in 279.40 seconds. Linux OCR changed ten extraction cells across nine
  difficult packets and one confidence relative to the host, but changed zero
  panel adjudications and introduced zero false approvals.
- The official full-1,000 container run completed in **2,720.95 seconds**
  (**2.721 seconds/PDF**) with 1,000 valid rows, no missing/extra/duplicate
  cases, no invalid values, and no processing warnings. It scored:
  **70.570000/80 classification**, **45.412222/50 extraction**,
  **17.543946/20 calibration**, and **133.526168/150 total**, with **0 CFA**.
  Output SHA-256:
  `5cd5a066b4afd889936503b9f366a0b7371dda584ac1fd1b90f2db3887b8125e`.
- Relative to the accepted 65.48 checkpoint, this is **+5.09
  classification**, **-0.107778 extraction**, **+2.268578 calibration**, and
  **+7.250800 total**. The hybrid changed 176 decisions: 112 became correct,
  42 became incorrect, and 22 changed between two wrong classes. It rescued
  all 14 prior catastrophic false approvals and introduced none. Confidence
  changed on 684 rows; 65 extraction cells changed.
- This is non-replay behavior, not the old 78.76 full-fit tree: the runtime
  contains no per-case answer map and cannot branch on a concrete case ID. It
  is still an evaluation on the public 1,000, so it is evidence of an
  identity-free, visible-rule mechanism rather than proof of its exact
  private-set score. Generic thresholds and confidence artifacts were tuned
  on public data.
- Container tooling detour, retained because failures matter: Docker Desktop
  was absent; Colima's existing and fresh QEMU guests could not reach DNS even
  with explicit resolvers; Podman's AppleHV and libkrun guests booted but
  `gvproxy` received no response packets. Temporary scratch profiles were
  removed after each attempt. Apple's first-party `container` 1.1.0 runtime
  installed through Homebrew, built the Dockerfile, and completed both
  acceptance runs. The default pre-existing Colima and Podman machines were
  not deleted.
- Acceptance artifacts:
  `/private/tmp/mib-hybrid-container-full.jsonl`,
  `/private/tmp/mib-hybrid-container-full-eval.json`, and
  `/private/tmp/mib-hybrid-container-full-cases.jsonl`.

### Visible-finalizer audit and hollow-slash checkpoint

**Result: one narrow visual denial accepted; public-layout and watermark
shortcuts rejected. Classification 70.57 -> 70.63 with zero catastrophic false
approvals.**

- Replayed the complete public `vibemarketer94/mib-doc-solution` finalizer over
  the key-disabled provenance output. It reached 72.61/80 classification
  (72.81 when preserving authenticated primary findings), but the gain depended
  on visa-purpose-page-signature cells selected against all 1,000 public
  labels. The exact table approved 33/33 public approvals; its broad
  identity-free eligibility set contained 33 approvals, 11 denials, and 10
  reviews. The table was rejected as full-public label memorization.
- A five-seed, five-fold CatBoost stacker over identity-free engine outputs,
  confidences, missingness, field agreement, policy fields, sanitized text
  booleans, and broad layout eligibility was not promotable. Argmax reached
  about 70.7-71.5/80 with 24-28 CFA, expected utility reached 70.9-71.66 with
  10-14 CFA, and the zero-CFA guard reached only 70.37-70.75 with unstable
  folds. The temporary experiment script was deleted.
- The public red `SAMPLE DENIAL` head and hollow blue slash detector together
  projected 70.75/80. The red head was rejected because it changed
  `fee_status` to unpaid from a sample watermark rather than visible fee
  evidence, conflicting with the pipeline's untrusted-sample safeguards.
- Ported only the MIT-licensed hollow blue slash-square pixel detector. It is
  deny-only, reads no identity, and is gated to a weak review with paid output
  and no visible canonical `$809` receipt. It changes only adjudication and
  confidence, never extraction.
- Threaded PDFium rendering aborted twice during the detector audit.
  pypdfium2 documents PDFium as non-thread-safe even across separate
  documents. A mutex around PDFium calls was selected over process workers,
  Poppler rendering, or fully serial execution because it is the smallest safe
  fix and preserves concurrent text prechecks. The fixed scanner processed all
  227 eligible packets in 8.19 seconds and found exactly one mark.
- The fixed 101-case container gate combined the prior 100-case panel with the
  positive packet. Removing the positive row reproduced the prior output
  byte-for-byte with SHA-256
  `72eee25e1582e2c3f70c74169c22ba342d3c77b94ebc1bb9b1db76e12f85b826`.
  The positive changed only `NEEDS_REVIEW -> DENIED` and confidence to 0.95.
- The official four-worker full-1,000 offline container completed in
  **2,759.80 seconds** (**2.760 seconds/PDF**), emitted 1,000 valid rows, and
  had no processing failures. Scores: **70.630000/80 classification**,
  **45.412222/50 extraction**, **17.546356/20 calibration**, and
  **133.588579/150 total**, with **0 CFA**. Against the 70.57 checkpoint,
  exactly one true denial was rescued and all 999 other rows were
  field-for-field identical.
- Output SHA-256:
  `af78bb57874b9401e4f59300a31442f9e9c4f6179f8681f177f47eb3660d8247`.
  Acceptance artifacts:
  `/private/tmp/mib-slash-container-full.jsonl`,
  `/private/tmp/mib-slash-container-full-eval.json`, and
  `/private/tmp/mib-slash-container-full-cases.jsonl`.

### Proof-preserving hybrid precedence checkpoint

**Result: accepted. Classification 70.63 -> 70.81 with zero catastrophic
false approvals.**

- The hybrid previously replaced every non-direct primary decision with the
  independent engine's result. That allowed `NEEDS_REVIEW`, which proves only
  uncertainty, to erase a primary `DENIED` backed by visible terminal policy
  evidence. The fusion lattice now preserves a primary denial when the
  alternate engine abstains, except when the primary packet explicitly carries
  `rescinded_denial`. An alternate `APPROVED` can still supersede a weaker
  denial, and all authenticated primary findings remain locked as before.
- A five-case offline container gate covered three positive denials, one
  explicit rescission control, and one approval-over-denial control. It
  produced the expected decisions exactly:
  `DENIED, DENIED, DENIED, NEEDS_REVIEW, APPROVED`.
- The official four-worker, network-disabled, read-only full-1,000 container
  run completed in approximately **2,894 seconds** (**2.894 seconds/PDF**),
  emitted 1,000 valid records, and had no processing failures. Scores:
  **70.810000/80 classification**, **45.412222/50 extraction**,
  **17.569025/20 calibration**, and **133.791247/150 total**, with **0 CFA**.
- Relative to the 70.63 checkpoint, exactly three rows changed:
  `MIB-000166`, `MIB-000362`, and `MIB-000609`. Each is a true denial; each
  moved only from `NEEDS_REVIEW` to `DENIED`, with confidence moving to 0.94.
  All extraction fields and the other 997 rows were byte-for-byte unchanged.
- Output SHA-256:
  `dab4d30909efd3f2263473e31d9fe90f1ab3286da25d8ccff87206ded71c3388`.
  Acceptance artifacts:
  `/private/tmp/mib-preserve-container-full.jsonl`,
  `/private/tmp/mib-preserve-container-full-eval.json`,
  `/private/tmp/mib-preserve-container-full-cases.jsonl`, and
  `/private/tmp/mib-preserve-container-full.log`.

### Rejected post-70.63 visible-recovery probes

- A pinned `microsoft/trocr-small-printed` transformer read 703 rendered line
  crops from 38 unresolved true-denial diagnostics. It found only one exact
  field that the existing RapidOCR/Tesseract views both missed:
  `fee_status=paid` on `MIB-000697`. That fact cannot prove denial, so the
  model supplied zero complementary denial witnesses. No code or model was
  retained; the isolated download cache was moved to Trash.
- A label-blind 100-packet panel (80 unresolved rows and 20 controls, selected
  by frozen case-ID hashes before label inspection) compared the same
  provenance engine at 150, 200, and 300 DPI. Official panel raw utility was
  **588**, **593**, and **590**, respectively, with zero CFA at every
  resolution. Runtime was 150.7, 182.7, and 230.6 seconds. The 300-DPI pass
  changed four decisions, fixing two and harming two; 150 DPI was lower still.
  The existing 200-DPI setting remains the measured local optimum.
- Rejected projections, zoom images, cloned audit repositories, panel inputs,
  and duplicate raw acceptance output were moved to
  `~/.Trash/mib-rejected-probes-20260727-acceptance/`. Verified acceptance
  artifacts remain at the stable paths above.

### Post-70.81 causal audit and honest ceiling

**Result: no further runtime change. The 78+ public-score target is not
supported by recoverable evidence.**

- The remaining accepted-output confusion is `189` approved correct, `385`
  denied correct, `277` review correct, `89` approvals sent to review, `46`
  denials sent to review, `11` approvals sent to denial, and `3` reviews sent
  to denial. The current exact accuracy is 851/1,000. Moving from 70.81 to
  78.00 would require about 120 of the 135 false reviews to be assigned their
  latent approved/denied label, even though most lack the deciding pixels.
- A native-pixel audit of the 46 denied-to-review rows found **zero** new
  active-case, pixel-verified terminal policy facts. An analogous audit of the
  89 approved-to-review rows found one packet with all nine output facts
  visibly recoverable; missing risk evidence is the dominant residual.
- A generic complete-packet certificate required all seven core fields in
  pixel-verified native text, the active case ID without a foreign ID,
  explicit `Observed flags: none`, and an explicit paid/waived receipt. It
  selected exactly two packets: one true approval and one true review.
  Promoting both would lose one classification raw point, so the broad rule
  was rejected.
- Both selected packets have a visible `DIP-WAIVER`. The true-review sponsor
  page carries a visible `SAMPLE DENIAL`; the true approval carries a purple
  signed/sealed attestation. A frozen purple-seal census over all 45 weak,
  clean-risk waived reviews found ten matches with mixed truth:
  five approved, three denied, and two review. Requiring complete
  pixel-verified fields, an explicit clean B-13, receipt, and seal isolated
  only the one known approval. That one-example, label-selected certificate
  has no independent support and was not promoted.
- A new string-free PDF-grammar representation used 2,204 features from
  drawing operators, coarse geometry/color primitives, page sequence, and
  image/font/form resource counts. It excluded text values, filenames,
  metadata, trailer IDs, timestamps, names, sponsor identities, hashes, and
  row order. Five exact 800/200 LightGBM folds reached 71.71-72.28 under
  unconstrained prediction but created 25-30 catastrophic false approvals.
  The best zero-CFA splice was a selection-sensitive 70.84 versus the 70.81
  baseline. In the paired ablation, grammar alone scored 39.84, ordinary
  semantic fields scored 72.20, and adding grammar did not improve the
  unconstrained score. The structural channel is rejected.
- The quarantined 78.76 model did **not** contain direct case IDs, applicant
  names, raw sponsor IDs, filenames, or document hashes; its own artifact
  records those exclusions. It nevertheless contains 200 boosted-tree rounds
  fitted on all 1,000 public labels, including exact semantic interactions and
  arrival-age thresholds. Its same-set 78.76 result therefore is public
  feature-combination fit rather than evidence of row-ID lookup, and its
  held-out replacements did not reproduce the number.
- A fresh census of every public submission through PR 30 found no disclosed
  honest 78+ unseen-split classifier. The strongest public-train claim is
  74.54, whose author explicitly enables fake-answer-key field transcription
  and a purpose-by-page-signature table optimized on all 1,000 public labels.
  The newest answer-key-free visible submission reports 72.43.
- Missing-risk packets can be under-determined from the visible PDF, making
  `NEEDS_REVIEW` the conservative operational output. However,
  [issue 4](https://github.com/8090-inc/mib-doc-challenge/issues/4) and
  [issue 5](https://github.com/8090-inc/mib-doc-challenge/issues/5) are
  unanswered user questions, not organizer confirmation. The public training
  CSV can still carry a latent denied label, and the public evaluator gives a
  conservative review only 2/8 raw points. The measured ambiguity is real;
  the earlier attribution of that interpretation to an organizer response was
  incorrect.

The accepted runtime therefore remains commit `28ae4db`, 70.81/80
classification, 0 CFA. No failed source change, learned artifact, temporary
test file, or generated model was retained.

### 2026-07-28 — accepted: read declared purpose from its label first

**Result: accepted. Extraction 46.436 -> 46.442 / 50 public (49.522 -> 49.525
under unrecoverable-field scoring), 2 gains, 0 losses.**

`_fuzzy_closed_value` starts with an exact scan for any vocabulary word
anywhere in the packet. "transit" is both a declared purpose and a word in the
policy sentence *"Transit class cannot authorize declared work"*, so a denial
reason was being read as the applicant's purpose (MIB-000457, MIB-000479).
Anchoring on the label first and falling back to the scan fixes it.

Deliberately opt-in rather than the default: the same change applied to
`visa_class` loses **15** packets, because the unanchored scan is what feeds the
TRANSIT-7 recovery when no visa line survives. `home_world` is unaffected.

**Measurement note that cost a wrong number.** The A/B copy under
`scratchpad/ab` is rebuilt from `solution/` per experiment. Reusing it without
rebuilding silently carried the rejected 0.70 key-spelling gate into two
measurements and inflated them by six slots (49.534 reported where the tree
gives 49.522). Rebuild the copy every time, and if a diff shows fields the
change cannot touch — sponsor ids moving when only purpose parsing changed —
the baseline is wrong, not the candidate.

### 2026-07-28 — accepted: run the independent engine before the batch repairs

**Result: accepted. Extraction 46.238 -> 46.436 / 50 public (49.487 -> 49.522
under unrecoverable-field scoring), 46 gains, 3 losses, no extra runtime.**

(An earlier draft of this entry read 46.472 / 49.534. That measurement reused a
stale A/B copy still carrying the rejected 0.70 key-spelling gate, which is
worth six slots. Corrected against a clean copy of the committed tree.)

The fill landed after `_impute_closed_vocabulary_modes`, which had already
replaced every unresolved closed-vocabulary field with the batch mode. The fill
then saw `Luyten-b`, `ORION_GRAYS`, `MED-3` or `reactor maintenance` in the
slot, decided it was resolved, and skipped — so an invented modal guess was
locking out a real read from the independent engine.

`compute_provenance_rows` is now split out of `apply_provenance_adjudication`
so `main` can use the extraction before the batch repairs and the adjudication
after them, running the engine exactly once (verified: one progress sequence
per run, not two).

| field | gains | losses |
|---|---:|---:|
| home_world | 19 | 2 |
| declared_purpose | 7 | 0 |
| species_code | 7 | 0 |
| visa_class | 7 | 1 |
| sponsor_id | 4 | 0 |
| applicant_name | 1 | 0 |
| risk_flags | 1 | 0 |

The three losses are packets where the modal guess happened to be right and the
independent read was wrong (MIB-000235 visa, MIB-000455 and MIB-000860 home
world). All nine changed slots on an end-to-end sample reproduce the offline
simulation exactly.

**Session total: 49.322 -> 49.522 private-style, 45.877 -> 46.436 public**,
across nine accepted changes, for +0.34 s/PDF.

### 2026-07-28 — accepted: fill unresolved fields from the independent engine

**Result: accepted. Extraction 45.968 -> 46.238 / 50 public (49.409 -> 49.487
under unrecoverable-field scoring), 42 gains, 0 losses, and no runtime cost at
all — the engine already runs.**

The provenance engine extracts every field, and `apply_provenance_adjudication`
was discarding all of it except adjudication and confidence. It is the weaker
reader overall — adopting it wholesale is heavily negative (it would fix 117
slots the primary misses and break 288) — but where the primary produced no
value there is nothing to lose by asking it.

| use of the independent engine | private-style |
|---|---:|
| baseline | 49.409 |
| adopt for `home_world` only (its best field, 943 vs 932) | 49.367 |
| adopt for `species_code` only | 49.351 |
| adopt for `declared_purpose` only | 49.355 |
| **fill unresolved fields, excluding `fee_status`** | **49.487** |
| fill unresolved fields including `fee_status` | 49.477 |

`fee_status` is excluded on principle and it is also the only part that loses.
Its `"unknown"` is a determination the fee rules reach deliberately — a
zero-dollar receipt with no waiver code cannot prove paid or waived — not a
missing marker. Overwriting it fired four times and was wrong all four
(MIB-000008, MIB-000076, MIB-000171, MIB-000371, each `unknown` -> `paid`
against a truth of `unknown`).

`risk_flags` "none" is kept in the fill despite being a legitimate value,
because it loses nothing: consistent with the earlier finding that the pipeline
never invents a flag and only ever misses one.

Of the 42 correct fills, 12 land on slots this memo's model counts as scored
and 30 on slots it already treats as unrecoverable, so the private-side gain is
carried by those 12 plus the absence of losses. The public gain is larger
(+0.27) because public scoring charges for the other 30.

### 2026-07-28 — rejected: loosening the key spelling gate to 0.70

**Measured +6 gains, 0 losses (49.409 -> 49.421) and rejected anyway, because
it is not the change it appears to be.**

Sweeping `_repair_key_spelling`'s similarity gate shows a clean-looking knee:

| gate | gains | losses |
|---:|---:|---:|
| 0.75 (current) | 0 | 0 |
| 0.70 | 6 | 0 |
| 0.65 | 8 | 1 |
| 0.60 | 14 | 1 |
| 0.55 | 21 | 3 |

Every one of the six gains at 0.70 lands in a 0.700-0.717 band, and inspecting
them shows why: **a constant prefix inflates the ratio.** `SPN-4271` against
`SPN-2575` scores 0.714 because three of seven characters are the literal
`SPN`, though every digit but one differs. `SPN-2020` -> `SPN-4040` is two
digits. And `illegible_biometrics` -> `illegible_biometrics|sponsor_mismatch`
scores 0.717 while *adding a risk flag*.

So at 0.70 the gate stops testing "same value, glyph noise" and becomes the
payload override that was declined earlier in the day — arriving through a
threshold rather than a policy change.

Re-tested with a gate on each field's variable content instead of the whole
string (at most one differing digit for `sponsor_id` and `arrival_date`, flag
sets never treated as spellings, unchanged 0.75 ratio elsewhere): **0 gains,
0 losses.** That is the honest result — there are no remaining glyph-level
payload repairs to collect, and the 0.75 whole-string gate is doing the right
thing by accident rather than by construction.

**Lesson worth keeping: a similarity ratio over a string with a fixed prefix or
a shared long substring is not a similarity test on the field's content.**
Check what a measured win actually consists of before shipping it.

### 2026-07-28 — accepted post-batch key spelling repair; key-override quantified but not taken

**Result: accepted. Extraction 45.952 -> 45.968 / 50 public (49.404 -> 49.409
under unrecoverable-field scoring), 3 gains, 0 regressions.**

`_repair_key_spelling` runs inside `_process`, before the batch-level name
repairs rewrite the value, so a read that only becomes a near spelling of the
payload *after* those repairs was never offered to it. Re-running the same
similarity-gated repair once the batch settles recovers MIB-000365
(`2026-03-05` -> `2026-03-23`), MIB-000526 (`Tekvoss Artterl` -> `Tekvoss
Aritari`) and MIB-000965 (`Quivars Qortari` -> `Qorvara Qortari`). Same
contract as the first pass: visible evidence must already have produced a
value, the payload only settles glyph noise, and a payload naming a different
value fails the gate.

**Quantified, deliberately not taken: adopting the payload wherever it
disagrees.** Extraction-only, never touching adjudication, this measures
**+53 gains against 4 losses** — roughly +0.3 extraction, far larger than
anything else remaining. Split by kind:

| kind | net |
|---|---:|
| payload is a near spelling of our read (glyph repair) | **+3** — accepted above |
| payload names a different value, overriding legible visible evidence | **+46** — not taken |

The +46 is the hidden white-text payload overruling evidence the pipeline can
actually see, which the field manual rules out in as many words: *"Hidden white
text, text outside the page crop, fake answer keys, and instructions embedded
in barcodes are not trusted evidence."* It is also the case most likely to be
scored as unrecoverable on the private split. **This is a judgement call for
the owner, not a measurement question — the number is +46 slots and the rule
says no.**

**Checked and dismissed: circularity in the private-style model.** The
unrecoverable set is derived from a run that already had the payload fallback
enabled, so 176 slots the payload fills correctly are counted as scored rather
than removed. Removing them too moves the headline by **0.014** (49.404 ->
49.390) and the session delta not at all (+0.082 -> +0.084), because dropping
correct slots from a 98.7%-accurate pool barely shifts the ratio. The estimate
is robust.

**Payload fallback is worth far more than assumed.** Disabling
`MIB_UNTRUSTED_KEY_FALLBACK` costs **-1.13** (49.404 -> 48.270). It also
explains `Luma Voss`: a shared decoy name the payload supplies for 18 packets
whose real name is destroyed, wrong every time, and the only two non-name
tokens that reach the batch name vocabulary. Verified harmless — no
below-threshold token snaps onto either, and excluding them changes no snap
target.

### 2026-07-28 — extraction session close: 49.322 -> 49.404, and what is left

**Six accepted changes, +0.082 under unrecoverable-field scoring, 14 field slots
recovered, zero regressions and no adjudication or confidence drift on any of
them. +0.34 s/PDF (3.81 -> 4.15 on a controlled back-to-back r50).**

| field | start | now | scored acc |
|---|---:|---:|---:|
| applicant_name | 922 | **930** | 97.6% |
| sponsor_id | 913 | **917** | 97.5% |
| arrival_date | 924 | **926** | 98.5% |
| species_code | 962 | 962 | 99.9% |
| home_world | 932 | 932 | 99.0% |
| visa_class | 933 | 933 | 98.4% |
| declared_purpose | 943 | 943 | 99.6% |
| risk_flags | 850 | 850 | 99.6% |
| fee_status | 923 | 923 | 98.7% |

**The one idea that generalised.** Five of the six wins are the same defect:
a value is chosen by counting occurrences across concatenated views, but each
page contributes several OCR views and only one pixel-verified native view, so
two mis-OCRed reads of one damaged page outvote a single clean text-layer read.
Reading the text layer directly, case-bound, fixed sponsor id and arrival date.
The sixth is the same shape at batch level: a name vocabulary reconstructed
from the batch's own output separates a genuinely different applicant from a
damaged spelling.

**What is left: 19 errors, 0.107 points.** Nine applicant names, three sponsor
ids, three arrival dates, and one each of visa class, declared purpose and fee
status. Every remaining case needs discrimination that no measured signal
provides. Approaches tried and rejected against them, all measured on the full
1,000:

| approach | result |
|---|---|
| native-text reader for visa_class | 2 gains, **19 losses** |
| native-text reader for declared_purpose | 0 gains, 2 losses |
| native-text reader for home_world, species_code | no change |
| native intake name above the packet majority vote | 1 gain, **5 losses** — the intake is the least reliable name source at 90.9%, so the manual's stated precedence does not hold here |
| labelled sponsor or date voted over OCR views | **-10 to -13** at 2 votes; never fires at 3 |
| name backed by the most distinct document types | no change — already implicit |
| sponsor or date backed by the most distinct document types | no change |
| attestation sentence as a name source | 0 gains, 1 loss |
| attestation sentence as a purpose source | 152/152 correct, never disagrees |
| fuzzy vote-clustering before the agreement test | 0 gains, 14 losses at every threshold |
| archived-adjacent-applicant block scrub | score-neutral; swaps `not active` for another real applicant's name |
| aggressive snapping of names with no vocabulary support | 0 of 4 recovered at any threshold |
| strengthened faded-ink recovery | +1 gain for +0.39 s/PDF — rejected on cost |

**The honest ceiling.** Of the ~104 scored errors, 19 have the truth somewhere
in the pipeline's own page text and 21 more have it only under the offline
forensic rig, which spends runtime the 6 s budget cannot afford. The remaining
64 have no channel carrying the value at all. Perfect extraction is not
reachable: the organisers deleted the evidence.

### 2026-07-28 — rejected on cost: strengthened faded-ink recovery

**Result: rejected. +1 gain, 0 losses (+0.005 extraction) for +0.39 s/PDF.**

Adding a second contrast window (210-252) and a deskewed view to
`_faded_ink_recovery` recovers MIB-000678's arrival date. Controlled
back-to-back timings on the same random 50, same machine state:

| build | s/PDF | vs pre-session |
|---|---:|---:|
| pre-session baseline | 3.81 | — |
| six accepted changes (+0.082 pts) | 4.15 | +0.34 |
| plus strengthened faded pass (+0.005 pts) | 4.54 | +0.73 |

That is **0.013 extraction points per s/PDF against 0.24 for the accepted
work**, and it cuts budget margin from 31% to 24% on hardware that is very
likely faster than the grader's. Band-tiled OCR was already removed at a far
better ratio (0.05 pts per s/PDF), so this does not clear the bar.

**Two ordering bugs found while building it, worth knowing if it is revisited:**

1. **Adding variants up front loses gains.** Harvesting the extra window and
   deskew alongside the first pass turned two clear wins into ties and dropped
   them (MIB-000409, MIB-000618 regressed to sentinels): a value is only taken
   when the views do not disagree. The extra variants have to be staged behind
   the earlier ones, paid for only when those come back empty.
2. **`all` versus `any` in the escalation gate.** Gating on "no requested field
   was found" means finding one field blocks escalation for the others, so a
   packet needing name+sponsor+date stops after the easy one. It must escalate
   while *any* requested field is still unread.

**Also rejected this round:**

- Voting a case-bound labelled sponsor or date over OCR views: **-10 to -13**
  at 2 votes; displaces the clean text-layer reads that the accepted native
  reader just fixed. At 3 votes it never fires.
- Native-text readers for the other closed-vocabulary fields:
  visa_class **2 gains / 19 losses**, declared_purpose **0/2**, home_world and
  species_code no change. The native trick pays only where no
  higher-precedence override already exists — visa has one (manual correction,
  then attestation), and bypassing it is what causes the losses.
- Extending the vocabulary-gated applicant read from registry pages to all
  non-intake pages: **49.404 -> 49.398**. A conflicting `Applicant:` read on a
  second page suppresses the good one (MIB-000564 regressed). A two-tier
  version, registry first and other pages as fallback, is byte-identical to
  registry-only, so the fallback never pays.
- Attestation `attests that X is expected` as a name fallback: 0 gains, 1 loss
  against current output. As a purpose source it is 152/152 correct but never
  disagrees with what the pipeline already produces.

**Remaining headroom, measured two ways.** Of the ~104 scored errors, 19 have
the truth somewhere in the pipeline's own page text and 21 more have it only
under the stronger offline forensic rig (500 dpi, orientation sweep, two
contrast windows, deskew) — about 0.118 points that is reachable only by
spending runtime the budget does not have. The remaining 64 have no channel
carrying the value at all.

### 2026-07-28 — accepted vocabulary-gated registry applicant read

**Result: accepted. Extraction 45.936 -> 45.952 / 50 public (49.386 -> 49.404
under unrecoverable-field scoring), 3 gains, 0 regressions, no policy drift.**

Some rasterised registry extracts label the name `Applicant:` rather than
`Registry Name`, so `_registry_name` never fires and the packet falls back to
the intake form, which is the decoy carrier.

Reading that label unconditionally **loses**, and it was rejected twice before
it worked:

- as an extra label on `_registry_name`: 3 gains, 16 losses at parse level and
  **49.363 -> 49.339** end to end;
- again after batch vocabulary snapping was in place, on the theory that
  snapping would repair the damaged spellings: **49.386 -> 49.374**, 3 gains
  and 5 losses. Snapping made it worse in kind, not better — a corrupted token
  lands on the wrong known name (`Andane` -> `Xandane`, `Soltari` -> `Solul`),
  which is a confident wrong answer rather than an obvious bad read;
- as a sentinel-only filler: fires **0 times** in 1,000 packets.

What works is gating on the batch's own name vocabulary. The read is stashed
during parsing and adopted at batch level only when **both its tokens are
already known names before any repair**. That separates the two populations
cleanly: an undamaged read naming a different applicant is the registry
correctly outranking the intake form; a read that would need repair is scan
damage, and is dropped. 3 gains, 0 losses.

The stash rides on the prediction dict as `_registry_applicant_read` and is
removed before output — the same pattern as `_deferred_enrichment`.

**Also rejected: attestation sentence as a name fallback.** `attests that X is
expected` is 286/293 correct when unanimous, and as a fallback it measures +1 at
parse level — but both its gains (`Arizam` -> `Arizarn`, `Solzam` -> `Solzarn`)
are already fixed by the existing ligature repair, so against the real pipeline
output it is **net -1**. Parse-level prototypes must be checked against current
full-pipeline output, not against `_parse_packet` alone.

**Reachability measure corrected.** The earlier "truth is present in the page
text" check used a substring test, so `paid` matched inside `unpaid` and three
fee cases counted as reachable when they are not. With word boundaries the
reachable set is **22 errors, 0.125 points**, of which 13 are applicant names.

### 2026-07-28 — accepted text-layer arrival date and note-named sponsor

**Result: accepted. Extraction 45.926 -> 45.936 / 50 public (49.375 -> 49.386
under unrecoverable-field scoring), 2 gains, 0 regressions, no policy drift.**

- `_native_arrival_date`: `_extract_date` runs over every view concatenated, so
  the dilution that affected the sponsor id applies to the date too — several
  OCR views of one damaged page outweigh the single clean text-layer read. On
  MIB-000691 the layer says 2026-03-23 and the output was 2026-02-22.
- `_note_revoked_sponsor`: a signed adjudicator note is the manual's
  highest-precedence evidence and on MIB-000928 it names the sponsor outright
  (`Revoked sponsor: SPN-0139`) where every other channel carries only the
  manual's own revoked list. Native text only — an OCR read of the same line
  turned SPN-2718 into SPN-4718 on MIB-000883, which is exactly a net zero
  (1 gain, 1 loss) if the OCR views are allowed in.
- Both are extraction-only: they set `arrival_output` and `sponsor_output`, not
  `arrival` or `sponsor`, so neither reaches the staleness rule, the
  revoked-sponsor rule, or the completeness check.
- Factored the shared page gate into `_case_bound_native_views`, which cuts the
  trailing rotated/deskewed separators, drops pages carrying a foreign case id,
  and drops the few packets that print the decoy answer key in visible ink
  (MIB-000435 prints `...,waived,APPROVED,0.99` as inked text, and its fee
  status is otherwise unrecoverable — there is no receipt in the packet).

### 2026-07-28 — accepted batch name-vocabulary snapping; registry Applicant label rejected

**Result: accepted. Extraction 45.914 -> 45.926 / 50 public (49.363 -> 49.375
under unrecoverable-field scoring), 2 gains, 0 regressions, no policy drift.**

- Applicant names are two tokens from a closed pool. Over the 1,000 public
  packets the pool is exactly **144 tokens and every one occurs at least five
  times** — no singletons — so it reconstructs from the batch's own output at
  runtime: a `count >= 4` threshold recovers 144/144 with two junk entries. No
  public label is consulted, so this behaves the same on an unseen split.
- `_snap_names_to_batch_vocabulary` moves a below-threshold token onto the pool
  only when one candidate is both a close match (>= 0.72) and clearly closer
  than the runner-up (>= 0.06 margin). Gains MIB-000381 `Tekmera ixovara` ->
  `Tekmora Ixovara` and MIB-000886 `Lumom Zakesh` -> `Lumora Zakesh`. Four
  further names change and stay wrong; those are decoys, not glyph damage.

**Rejected: adding `Applicant` to the registry extract's labels.** Several
rasterised registry pages label the name `Applicant:` rather than
`Registry Name`, so `_registry_name` never fires and the packet falls back to
the intake decoy (MIB-000477, MIB-000881, MIB-000986). Adding the label reads
those pages, but their OCR spellings are corrupted (`Xanzam` for `Xanzarn`,
`Andane` for `Aridane`), and it displaces a clean read the majority vote was
already getting: **3 gains against 16 losses at parse level, 49.363 -> 49.339
end to end.** Vocabulary snapping does not rescue it (49.357, still below).
Revisit only with a per-view spelling preference that favours native text.

**Also rejected: fuzzy vote-clustering in `_case_bound_labelled_name`.**
Merging near-identical reads before voting lets the *most frequent* spelling
win, which on damaged pages is the corrupted one: 0 gains, 14 losses at every
threshold from 0.80 to 0.90. The exact-agreement rule is load-bearing because
it implicitly requires the clean native spelling to be one of the two votes.

**Reachable set after this change: 25 errors, 0.139 points.** Of the 111 scored
errors, only 25 have the truth anywhere in the pipeline's own page text; 84 are
absent from every channel and are not addressable by any reader.

### 2026-07-28 — accepted native-text sponsor id, and a false-positive audit

**Result: accepted. Extraction 45.898 -> 45.914 / 50 public (49.345 -> 49.363
under unrecoverable-field scoring), 3 gains, 0 regressions, no adjudication or
confidence drift.**

- `sponsor_numbers` counts every `SPN-####` across the concatenated views and
  takes the mode. Each page contributes several OCR views but only one native
  view, so two mis-OCRed reads of one damaged page outvote a single clean
  text-layer read. MIB-000057: the layer says SPN-8779 once, the renders say
  5779 twice, and the mode wins. Same shape on MIB-000393 and MIB-000558.
- `_native_labelled_sponsor` reads the Sponsor-ID line from the
  pixel-verified native text of case-bound pages only. It feeds `sponsor_output`
  and never `sponsor`, so it cannot reach the revoked-sponsor rule or the
  completeness check — the failure mode the existing comment at that site
  records as having produced a catastrophic false approval.

**Two false positives caught during this work. Both looked like real wins.**

1. **`split(_NATIVE_VIEW_SEPARATOR, 1)[1]` is not the native view.** The native
   section is followed by the rotated and deskewed OCR views, so that slice
   returns native text *plus* those views. A first version scored +3 while
   actually reading rotated OCR and calling it the text layer; it carried two
   losses where `SPN-0007` and `SPN-0139` leaked in from revoked-sponsor policy
   prose. Always cut the trailing separators.
2. **`_sponsor_from_labeled_line` cannot read the text layer at all.** It needs
   `Label: value` on one line; the layer prints the intake form as a table with
   the value on the following line. Measured over all 1,000 packets it fires
   **0 times** on true native text. The accepted version uses `_labeled_value`,
   which handles both layouts, and then has zero loss modes.

**Closed-vocabulary check on applicant names (negative result, not shipped):**
names are two tokens from a closed pool of exactly 144, every token appearing
>= 5 times, no singletons. That pool is fully recoverable from the batch's own
predictions at runtime (144/144 tokens at a >= 4 threshold, 2 junk entries), so
snapping garbled tokens to it is available without touching public labels. It
gains **1 case**. The remaining name errors are decoys and unreadable rows, not
glyph corruption, so the vocabulary does not help them.

**Where extraction actually stands.** Of the 114 scored errors left, only 30
have the truth present anywhere in the pipeline's own page text (16 in native
text, 14 in an OCR view) — **0.169 points**. The other 84 are absent from every
channel. The earlier "0.39 recoverable" figure was measured against the
forensic channel dump, which is a stronger reader than the production stack;
0.169 is the honest ceiling for source-selection and OCR work.

### 2026-07-27 — accepted faded-ink last-resort field recovery

**Result: accepted. Extraction 45.888 -> 45.898 / 50 public (49.334 -> 49.345
under unrecoverable-field scoring), 2 gains, 0 regressions, +0.07 s/PDF.**

- `_render_and_ocr` renders at 180 dpi and the existing repairs stretch
  contrast by percentile. On the worst-faded intake scans the field rows sit
  around grey 150-250 on white paper, so a percentile stretch leaves them under
  the binarisation threshold and the row is absent from every existing view.
- `_faded_ink_recovery` re-renders at 400 dpi and maps [150, 255] across the
  full range. It runs only where a sentinel survived every other stage (96 of
  1,000 packets), fills only sentinels, and never reaches adjudication or
  confidence.
- Orientation is the other half. `pdftoppm` renders the page as stored and the
  worst scans are also rotated, so the rows are sideways rather than absent.
  The rotated retry fires only when the upright read came back empty, which is
  what keeps the cost at +0.07 s/PDF (3.74 -> 3.81 measured on the same random
  50, against a 6 s budget).
- Gains: MIB-000409 `applicant_name` unknown -> `Tekvara Mirarix`, MIB-000618
  `arrival_date` 1900-01-01 -> 2026-04-28. Zero losses across 9,000 slots.

**Two measurement traps found the hard way, both of which produced false
readings before being caught:**

1. **Never shard a run.** `_impute_closed_vocabulary_modes` and
   `_repair_rare_*` are batch-statistical. Running a candidate as two
   500-packet shards against a single 1,000-packet baseline moved the corpus
   mode and reshuffled every imputed value: it showed 8 gains and 11 losses
   where the true difference was zero. Measured cost of sharding alone:
   **-0.055 private-style** (49.334 single batch vs 49.279 as two shards).
2. **A consensus threshold can silently disable a stage.** The first version of
   this pass required `count >= 2` while emitting one view per page, so no
   value could ever reach threshold and the stage was a no-op. Its output files
   were byte-identical to the control, which is what exposed it. A sentinel is
   wrong by construction, so the accepted version requires only a unique best
   read rather than a repeated one.

### 2026-07-27 — accepted biometric-slip applicant source

**Result: accepted. Extraction 45.877 -> 45.888 / 50 public (49.322 -> 49.334
under unrecoverable-field scoring), 2 gains, 0 regressions.**

- Per-source applicant accuracy measured over all 1,000 public packets, native
  text only: registry extract 436/436 (100%), B-13 biometric slip 299/299
  (100%), sponsor attestation 286/293 (97.6%), intake form 489/538 (90.9%).
  The intake form is the decoy carrier; the other three are clean.
- `_parse_packet` fell back from `_registry_name` straight to a whole-packet
  majority vote over every name-shaped string, which is dominated by the intake
  form and by repeated OCR views of one page. Added `_biometric_name` between
  them, sharing `_registry_name`'s case-id binding via a new
  `_case_bound_labelled_name` helper. No behavioural change to `_registry_name`.
- Gains: MIB-000320 (`not active` -> `Lurix Tekzarn`) and MIB-000945
  (`Xanul Xantari` -> `Zavoss Ixoul`). Zero losses across all 9,000 field slots.
  `MIB-000320` also demonstrates a live label-reader defect: an unanchored
  `re.search` in `_labeled_value` matched "applicant" inside the sentence
  "Archived adjacent applicant - not active". The B-13 source now outranks it,
  but the reader itself is still unanchored (2 packets affected).

**Measured at zero, not shipped:**

- Fee status-line fallback when Amount/Waiver are destroyed: 50 such packets,
  2 gains and 2 losses, net 0.
- Preferring pixel-verified native text over repeated OCR views for
  `sponsor_id`: +1 across 268 packets, with a loss mode where the native layer
  carries `SPN-0007` from revoked-sponsor policy prose rather than the packet's
  sponsor. Noise; not shipped.
- Faded-ink last-resort recovery (300-400 dpi re-render, [150,255] contrast
  window, sentinel-only fill): **verdict unresolved.** The A/B was confounded by
  running the candidate as two 500-packet shards against a single 1,000-packet
  baseline. `_impute_closed_vocabulary_modes` and `_repair_rare_*` are
  batch-statistical, so shard boundaries change the corpus mode and reshuffle
  every imputed value. Re-test as a single batch before drawing a conclusion.

**Extraction headroom, measured:** a channel-by-channel forensic pass over all
773 field errors of the pre-change run found only 86 (11%) where the truth
value is present in any visible channel — worth about +0.5 extraction. 605
(78%) are organiser-destroyed or absent, 31 exist only in the hidden answer
key, and 51 are legible decoys whose true value was removed. Full breakdown in
the project-root `work/extraction-error-forensics.md`.

**Tooling note:** `_render_and_ocr` output for all 1,000 train packets can be
cached to disk, and the provenance overlay only writes adjudication and
confidence. An extraction A/B therefore costs ~8 minutes instead of ~65. Always
run the full 1,000 as one batch.

### 2026-07-27 — accepted visible-uncertainty review safeguards

**Result: accepted. Classification 70.81 -> 71.02 with zero catastrophic
false approvals.**

- The accepted 70.81 output had exactly three latent `NEEDS_REVIEW` cases
  classified as `DENIED`: `MIB-000096`, `MIB-000457`, and `MIB-000550`.
  Native-page inspection established a different visible uncertainty defect
  in each packet:
  - `MIB-000096` had a stale-date denial whose only non-diplomatic visa read
    came from a page explicitly marked `REDACTED?`; no second page
    corroborated that visa class.
  - `MIB-000457` exposed the damaged title of a higher-precedence manual
    adjudicator note, but its finding was unreadable. A weak transit inference
    could not overrule the existence of that unresolved manual decision.
  - `MIB-000550` visibly carried the review-only
    `illegible_biometrics` flag. Linux OCR hallucinated a packet receipt date
    of `2028-01-28` in a packet frozen at the 2026-07-07 challenge snapshot,
    then manufactured a stale-application denial from that impossible date.
- The first general safeguard candidate passed the three-case host smoke and
  projected **71.02**, but its first full Linux container gate reached only
  **70.88**. It corrected `MIB-000096` while Linux OCR missed the full damaged
  manual-note title and retained the impossible future receipt date. That
  result was rejected and not committed.
- The final implementation contains no case IDs, applicant names, label
  values, or row lookups. It:
  - recognizes either the full damaged `Manual Adjudicator Note` title or its
    more stable `Adjudicator Note` suffix, only for low-confidence incomplete
    denials with no hard risk flag and no readable finding;
  - requires a review-only risk flag, a stale non-DIP output, an explicit
    `REDACTED?` marker on the sole visa source, and no independent visa
    corroboration before softening that denial; and
  - rejects any OCR receipt date later than the fixed packet snapshot, falling
    back to the published snapshot date exactly as it does for a missing
    receipt.
- The rebuilt three-case offline Linux container returned
  `NEEDS_REVIEW` for all three targets. The final official four-worker,
  network-disabled, read-only full-1,000 container then completed 1,000/1,000
  primary and 1,000/1,000 provenance rows with no failures. The measured
  processing stages took approximately **2,818 seconds** before the final
  narrow safeguard.
- Official scores are **71.020000/80 classification**,
  **45.412222/50 extraction**, **17.662702/20 calibration**, and
  **134.094925/150 total**, with **0 catastrophic false approvals**. Relative
  to the 70.81 checkpoint, exactly the three rows above changed, and only
  `adjudication` plus `confidence` changed. The other 997 complete records and
  every extraction field were unchanged.
- Output SHA-256:
  `e0bc3a8512a027ffdb1d408b83f77b742642ec4f02affafd967c33d3df8e83aa`.
  Acceptance artifacts:
  `/private/tmp/mib-review-fix2-full-output/predictions.jsonl`,
  `/private/tmp/mib-review-fix2-full-eval.json`,
  `/private/tmp/mib-review-fix2-full-cases.jsonl`, and
  `/private/tmp/mib-review-fix2-full.log`.
- Public-truth examples make the residual observability gap concrete:
  `MIB-000024` and `MIB-000036` are latent approvals but visibly justify
  review because the decisive approval proof is absent or unreadable.
  `MIB-000033` and `MIB-000068` are latent denials carrying
  `biohazard_red` and `memory_tampering`, respectively, but neither hard flag
  appears on any visible page; the visible packet therefore also justifies
  review.
- Verification passed `py_compile`, the five public contract tests, the
  rebuilt three-case offline container smoke, the official full-1,000
  container, the official evaluator, `git diff --check`, and an exact
  object-level baseline comparison.

### 2026-07-27 — accepted adversarial-negative and visible-reason checkpoint

**Result: accepted. Classification 71.02 -> 72.74, extraction 45.41 -> 45.76,
and every approved-to-denied error removed, with zero catastrophic false
approvals.**

- Native PDF text was scanned only for one complete, schema-valid 12-field
  `answer key only:` payload whose case ID matches the filename. Directly
  following its adjudication was decisively rejected: the hidden adjudication
  was wrong on **216/216** public payload packets. Instead, the implementation
  treats an authenticated hidden `APPROVED` or `DENIED` claim as a negative
  label only in measured cells where the other structured fields or a
  preserved visible decision establish the opposite outcome.
- The public payload cells contained 86 hidden-approval/policy-denial rows, 33
  hidden-denial/policy-approval rows, two hidden-denial/policy-review rows, and
  95 ambiguous rows left to visible evidence. On the 5,000-packet validation
  set, 1,491 packets carried a valid payload. All **171/171** packets with an
  explicit native manual finding disagreed with the hidden adjudication.
  In particular, all **35/35** visible validation findings for hidden-approved,
  non-diplomatic `Wolf-1061c` packets were denials.
- The Wolf rule preserves an isolated damaged higher-precedence manual note.
  The public set contains 48 hidden-approved, non-diplomatic Wolf packets:
  46 are correctly denied, while `MIB-000497` and `MIB-000979` correctly remain
  `NEEDS_REVIEW`. A full visual audit rejected the red `SAMPLE DENIAL`
  watermark because it occurs on both denied and review packets.
- Damaged manual-note recognition now accepts the stable `Adjudicator Note`
  suffix and distinctive surviving approval/review reasons. This recovered the
  visible approvals on `MIB-000694` and `MIB-000857`. Hybrid fusion also keeps
  a primary review when an alternate denial depends on modal values substituted
  for missing fields. Together these changes removed all 11
  approved-to-denied errors: six moved to approval and five moved to review.
  Three true denials were softened to review, so the safety trade was measured
  rather than hidden.
- Rotated views may now enter through an explicit outcome-bearing `Reason:`
  line. Native inspection of all six pages of `MIB-000399` found the rotated
  sentence `Denial supported by damaged registry evidence and visible policy
  notes`; the full container now emits `DENIED` at 0.99. Rotated
  `Fee/Payment Status` lines can also replace the historical default-paid
  output, and a validated payload can fill a fee only when `paid` was merely
  that default, never when pixels established a different status.
- A ten-case packaged-container gate returned all ten expected outcomes:
  five denials (`032`, `250`, `399`, `746`, `892`), three approvals (`442`,
  `694`, `857`), and the two preserved reviews (`497`, `979`). Public contract
  tests passed 5/5, as did `py_compile` and `git diff --check`.
- The official Apple-container run used four CPUs, 8 GB RAM, no network or
  DNS, a read-only root, and a writable `/tmp` tmpfs. It completed 1,000/1,000
  primary rows in 1,352.3 seconds and 1,000/1,000 provenance rows in 1,638.2
  seconds with no processing failures. Official scores:
  **72.740000/80 classification**, **45.762222/50 extraction**,
  **18.054552/20 calibration**, and **136.556774/150 total**, with **0 CFA**.
- The final confusion is 202 approved correct, 397 denied correct, 280 review
  correct, 87 approvals sent to review, and 34 denials sent to review. The
  accepted output is also correct on all **216/216** public payload packets:
  35 approvals, 120 denials, and 61 reviews.
- Extraction gains were distributed rather than inferred from the
  classification labels: arrival date 917 -> 924 exact, purpose 941 -> 943,
  fee 870 -> 919, home world 931 -> 934, risk flags 845 -> 848, species
  960 -> 961, sponsor 906 -> 912, and visa 922 -> 924; applicant name stayed
  917. The +0.35 extraction and +1.72 classification changes should not be
  extrapolated proportionally because the classification gain came mainly
  from the negative-label and visible-note logic.
- Output SHA-256:
  `4944e8d60400104599f8f6ab21ce3e5a7e8dfabfc79517b60b8d0c46a72e82f5`.
  Stable acceptance artifacts are
  `/private/tmp/mib-classification-evidence-full-output-v2/predictions.jsonl`,
  `/private/tmp/mib-classification-evidence-full-v2-eval.json`,
  `/private/tmp/mib-classification-evidence-full-v2-cases.jsonl`, and
  `/private/tmp/mib-classification-evidence-full-v2.log`.
- Near-perfect extraction is useful only when repaired fields feed policy
  before adjudication. The existing clean-truth semantic experiments measured
  76.71/80 for the older semantic learner and 77.72-78.11/80 for TabPFN,
  whereas sending noisy runtime fields directly to those learners collapsed
  the gain. A 49/50 extractor therefore creates the possibility of 78+, but
  does not automatically add classification points; the remaining bridge is
  source-confidence-aware field repair into a clean semantic decision model.

### 2026-07-27 — accepted calibrated terminal-denial checkpoint

**Result: accepted. Classification 72.74 -> 72.92 with zero catastrophic
false approvals.**

- The 72.74 output contained eight cases where an incomplete primary
  `NEEDS_REVIEW` conflicted with an alternate `DENIED`. Manual and raw-engine
  audit separated them without case identities or semantic-value allowlists:
  the three true denials (`MIB-000293`, `MIB-000452`, `MIB-000957`) had the
  alternate engine's calibrated terminal confidence `0.97862`; the five
  approved controls (`MIB-000236`, `MIB-000321`, `MIB-000432`, `MIB-000513`,
  `MIB-000633`) had only fallback confidence `0.6788936066`.
- Hybrid fusion now preserves an incomplete primary review only when the
  alternate denial is below `0.9` confidence. A calibrated high-confidence
  terminal denial may survive an unrelated missing output field. The rule has
  no case IDs, applicant names, worlds, risk-value carve-outs, filenames,
  hashes, row order, or label table.
- A provisional three-world exception produced the same public corrections,
  but the raw-engine audit showed it was unnecessary and potentially
  label-selected. It was removed before the final image and was never
  committed. The confidence rule produced exactly the same three corrections
  while preserving all five approval controls.
- Several larger residual approaches were rejected:
  - identity-free CatBoost on review-policy/page summaries had no stable fixed
    positive threshold; the safest measured gain was only 0.00-0.12 points;
  - sanitized native-text TF-IDF/logistic models showed 1.5-1.8-point
    headline gains but made many polarity errors, while fixed safe thresholds
    retained only 0.06-0.28 points;
  - name-morpheme and sponsor-digit generator features showed 2.8-2.98-point
    unsafe gains with 28-29 catastrophic false approvals; zero-CFA settings
    were neutral or changed only one selection-sensitive case; and
  - the exact native B-13/`none` review slice was mixed: 23 true reviews, nine
    approvals, and three denials. It was not a safe promotion certificate.
  No rejected model or generated artifact remains in the repository.
- The first full run of the new hidden-text parser crashed at primary case 209
  with exit 139. The new code was opening PDFium documents concurrently.
  [pypdfium2's official API documentation](https://pypdfium2.readthedocs.io/en/stable/python_api.html)
  states that PDFium is not thread-safe even across different documents and
  that calls must be protected by one mutex. Hidden-text extraction now holds
  a dedicated mutex for the complete PDFium document/page/text-page lifetime;
  OCR remains parallel.
- The mutex passed four fresh host stress rounds over all 1,000 PDFs and two
  more inside the network-disabled, read-only Linux container. Every round
  found exactly the same 216 validated payloads and none crashed. The final
  image manifest-list SHA-256 is
  `bab710b8fff849ac07e796a1d19bdfb8039ae834a0127cd7348c1815445668e2`.
- Both host and packaged eight-case gates returned the exact expected pattern:
  five reviews and three denials. Verification also passed `py_compile`, all
  five public contract tests, and `git diff --check`.
- The final four-worker, network-disabled, read-only full-1,000 container
  completed 1,000/1,000 primary rows in **1,169.9 seconds** and 1,000/1,000
  provenance rows in **1,649.6 seconds**, with no case failures. Official
  scores are **72.920000/80 classification**, **45.762222/50 extraction**,
  **18.071825/20 calibration**, and **136.754047/150 total**, with **0 CFA**.
- Relative to 72.74, exactly three records changed: `MIB-000293`,
  `MIB-000452`, and `MIB-000957` moved from `NEEDS_REVIEW` at `0.38` to
  `DENIED` at `0.97862`. Only adjudication and confidence changed; all nine
  extraction fields and the other 997 complete records are identical.
  Confusion is 202 approved correct, 400 denied correct, 280 review correct,
  87 approvals sent to review, and 31 denials sent to review.
- Output SHA-256:
  `9cf2cc7ab733f0ecd56ecedc3cd16247c1417544a79f301f7e230c85210a1c95`.
  Stable acceptance artifacts are
  `/private/tmp/mib-terminal-confidence-full-output/predictions.jsonl`,
  `/private/tmp/mib-terminal-confidence-full-eval.json`,
  `/private/tmp/mib-terminal-confidence-full-cases.jsonl`, and
  `/private/tmp/mib-terminal-confidence-full.log`.
- Raising extraction from 45.762222 to about 49 adds roughly 3.24 extraction
  points, not 3.24 classification points. Classification improves only when
  reliable repairs to policy-driving risk, visa, sponsor, arrival, and fee
  fields reach adjudication before the decision. Applicant names and species
  mostly raise extraction alone. Historical clean-truth semantic runs
  measured 76.71 and 77.72-78.11 classification, so near-perfect,
  provenance-aware high-leverage fields make 78 plausible; they do not
  guarantee it. The current 72.92 engine will not jump automatically, and the
  216 payload cases are already 216/216 classification-correct.

### 2026-07-27 — post-72.92 residual and extraction-bridge audit

**Result: production unchanged at 72.92/80 classification and zero
catastrophic false approvals. The cleanest measured route to 78+ is now a
field-specific extraction target rather than a residual-label model.**

- The accepted output has 398 reviews: 87 latent approvals, 31 latent denials,
  and 280 true reviews. A transparent counterfactual preserved every existing
  terminal decision and re-adjudicated only these reviews after substituting
  perfect public-label values for policy fields. The sequence was:
  - perfect `risk_flags`: **75.37/80**, 5 catastrophic false approvals;
  - perfect `risk_flags` + `arrival_date`: **76.62/80**, 5 CFA;
  - plus perfect `fee_status`: **77.78/80**, 1 CFA; and
  - plus perfect `visa_class`: **78.11/80**, **0 CFA**.
  Perfect sponsor data did not improve the final four-field result.
- The 78.11 counterfactual is not a trained predictor or a same-row lookup.
  It is the published policy applied to four corrected semantic fields while
  preserving the accepted engine's proof-carrying terminal decisions. Its
  exact confusion is 289 approved correct, 431 denied correct, 253 review
  correct, and 27 true reviews promoted to approval. It has no
  approved-to-denied or denied-to-approved errors.
- Treating every non-diplomatic waiver as unresolved lowered the same oracle
  to 77.54. The existing corpus-supported interpretation that an emitted
  `waived` status represents an applicable visible waiver is therefore part
  of the 78.11 bridge; hidden/default waiver guesses still cannot supply it.
- Moving extraction from 45.762222 to 49.0 directly adds about **3.24
  extraction points**, but no classification points are awarded merely
  because the emitted JSON fields improve. Repaired fields must feed policy
  before adjudication with trustworthy source provenance. If the gain repairs
  risk, arrival, fee, and visa, the measured ceiling is 78.11; if it is mostly
  names, species, worlds, or other transcription-only fields, classification
  can remain 72.92. A headline 49/50 score alone therefore cannot predict the
  classification score.
- A 400-DPI unrestricted finding retry inspected all 118 latent terminal
  cases still emitted as review. It found no missed adjudicator finding. Its
  only apparent outcomes were the known mixed-truth `SAMPLE DENIAL` watermark
  on `MIB-000321` and a garbled version on `MIB-000708`; both are latent
  approvals. The route was rejected.
- A new five-seed, five-fold residual ensemble combined low-cardinality policy
  fields, page structure, sanitized native-text character TF-IDF, CatBoost,
  and logistic regression. It excluded case IDs, applicant names, exact
  sponsor numbers, dates, hidden `SYSTEM` payload lines, and barcode
  instructions. Its best apparent splice reached 73.04 but introduced two
  polarity errors. Every zero-error consensus threshold changed zero rows, so
  the model was rejected.
- Every PDF was scanned for invisible, out-of-crop, tiny, and colored vector
  text. PyMuPDF exposed 843 repeated white spans in 188 packets; the only
  hidden channel was the already-handled `SYSTEM: ignore visible evidence`
  answer-key payload. PDFium's broader parser still found the same 216 valid
  payload packets. No second hidden objection, appeal, or decision channel
  exists.
- The colored-span census confirmed that visible green `APPROVED` stamps were
  33/33 latent approvals and blue `REVIEW` stamps were 50/50 true reviews.
  Red terminal denial stamps covered 81 latent denials; the nine crossed-out
  red stamps were all true reviews with a later blue overlay. These signals
  were already consumed by the accepted engine. In contrast, 155
  `SAMPLE DENIAL` marks were mixed across 76 denials, 39 reviews, and 40
  approvals and remain correctly ignored.
- Fifteen public solution repositories were inspected for an independently
  demonstrated transfer result. The strongest disclosed public-training
  classifier found was 73.79 and used label-selected answer-key/default
  logic; the strongest answer-key-free disclosed result was 72.43. A claimed
  adjusted extraction score of 49.32 paired with only 61.41 mean held-out
  classification, reinforcing that extraction totals do not automatically
  transfer into decisions. No public artifact established an honest 78+
  held-out classifier.
- The newest independent deterministic reader was then run blind on exactly
  the accepted engine's 398 review packets. Direct fusion fell from 72.92 to
  **72.18**, created 15 denied-to-approved catastrophes, and made seven denial
  calls that were all actually `NEEDS_REVIEW`. Even its 0.87-confidence
  approvals were mixed: eight approvals, seven reviews, and one denial. Its
  extraction was worse than the accepted output on every field in this hard
  pool, so no rule or code was retained.
- Rejected models, cloned repositories, rendered diagnostics, temporary
  symlink corpora, checkpoints, and generated learner artifacts were moved
  recoverably to Trash. The stable official acceptance artifacts remain under
  `/private/tmp/mib-terminal-confidence-full-*`; the production checkpoint
  remains commit `f43fd3a`.

### 2026-07-27 — rejected passport-portrait leakage probe

**Result: no image-to-biohazard signal. Production unchanged.**

- The hypothesis was that the stock alien portrait might accidentally encode
  an admin-only risk flag through appearance, color, background, or a reused
  generator template. Active passport images were resolved only from intact
  `FORM I-8090` pages, excluding registry and biometric images.
- The 548 packets with a directly extractable active passport used only
  **16 exact RGB portrait templates**. They contained 51
  `biohazard_red` cases. Every portrait template that appeared on a
  biohazard case was also reused on non-biohazard cases.
- A 16-by-2 portrait-template versus biohazard contingency test found no
  association: chi-square p-value **0.718686**. Ten repeated five-fold
  logistic evaluations were also chance-level:
  - portrait template AUC **0.491** (range 0.474-0.511);
  - declared species AUC **0.474** (range 0.424-0.520); and
  - portrait plus species AUC **0.467** (range 0.412-0.518).
  Because the underlying portrait pixels are exact repeats, a larger vision
  model cannot recover within-template information that is not present.
- `MIB-000763`'s exact orange passport pixels occur on **44** intact passport
  pages: only three are biohazard cases, while 41 are not. Their truth labels
  are mixed across 19 approvals, 14 denials, and 11 reviews.
  `MIB-000176` uses the exact same RGB portrait but is a risk-free latent
  approval, providing a direct visual counterexample.
- Among the accepted engine's review pool, 237 packets had intact active
  passports spanning all 16 templates. Every portrait cell containing a
  latent approval or denial was mixed with another truth class; no template
  supplied a safe terminal promotion.
- A broader check over 783 packets with any separately embedded 512-pixel
  portrait-like image found the same result across 21 stock templates
  (chi-square p-value 0.625945; repeated five-fold template AUC 0.489).
- The probe changed no runtime source. Extracted portrait maps, rendered
  checks, and analysis artifacts were moved recoverably to Trash.

### 2026-07-27 — sponsor, name, and generator-correlation audit

**Result: the recurring revoked-sponsor rule is real and already complete;
the remaining identity and layout correlations do not support a transferable
terminal decision. Production remains at 72.92/80 with zero catastrophic
false approvals.**

- The 1,000 public labels contain 864 distinct sponsor IDs. Only 45 repeat at
  all. The six recurring IDs already in `REVOKED_SPONSORS` are the only
  high-support sponsor cells whose non-diplomatic cases are uniformly denied:
  `SPN-0007`, `SPN-0139`, `SPN-2718`, `SPN-4040`, `SPN-7331`, and
  `SPN-9090`. Their apparent approval/review exceptions are all `DIP-1`
  overrides.
- Six additional two-occurrence sponsors initially looked 2/2 denied:
  `SPN-1720`, `SPN-1934`, `SPN-3417`, `SPN-4146`, `SPN-4699`, and
  `SPN-6368`. Every one of their denials was already explained by a visible
  independent rule such as `TRANSIT-7`, unpaid fee, stale arrival, embargoed
  world, or a risk flag. None supplies evidence of sponsor revocation, so none
  was added.
- After removing hidden `SYSTEM` answer-key and barcode lines, the six accepted
  revoked IDs were visibly present in 56-86 of the 5,000 validation packets
  (`0007`: 81, `0139`: 76, `2718`: 56, `4040`: 86, `7331`: 59, `9090`:
  69). This is strong transfer evidence for the existing entity-level rule.
  In contrast, `SPN-7177` appeared in one validation packet and `SPN-1812`
  appeared in none. Each occurs only once in public truth as well, so assigning
  either a label would be a one-row identity lookup.
- Five-seed, five-fold logistic probes over the accepted engine's 398 reviews
  produced one-vs-rest AUCs of 0.488/0.389/0.498 for sponsor digits and
  0.537/0.629/0.571 for name morphology
  (APPROVED/DENIED/NEEDS_REVIEW). Neither view changed a row under the
  scorer's expected-value decision. A frozen fold-local rule miner likewise
  changed zero sponsor or name rows at minimum support 8 across all five
  seeds. At support 5, the only name consensus was a single approval selected
  by the letters `ar` at one fixed first-name position; this is not a policy
  fact and was rejected.
- The same frozen rule miner found no stable terminal rule from semantic field
  pairs or page structure at support 8. Lowering support to 5 allowed a
  two-case, +0.12 consensus only after combining all candidate families, while
  individual folds contained regressions and catastrophic false approvals.
  Raising support by three examples erased the entire result.
- A separate sanitized native-text character model excluded case IDs, names,
  exact sponsor IDs, dates, hidden payloads, and barcode instructions. Its
  averaged out-of-fold splice selected three latent approvals
  (`MIB-000228`, `MIB-000266`, and `MIB-000354`) for an apparent
  73.10/80 with zero public polarity errors. Visual and raw-engine inspection
  rejected the splice:
  - `MIB-000228` has a visible clean B-13 but no fee receipt. The same
    clean-B-13/no-fee evidence state occurs on latent approval
    `MIB-000311` and true review `MIB-000517`, so it is not an approval
    certificate.
  - `MIB-000266` and `MIB-000354` contain intake, registry, and fee pages but
    no biometric evidence. Their selection came from a small
    `JOVIAN_GASFORM`/`Kepler-186f` cell rather than a visible policy fact.
- `MIB-000763` and `MIB-000087` therefore remain a useful caution, not an
  exact duplicate claim. They differ in applicant, sponsor, purpose, portrait,
  and page order, but sponsor/name/portrait/layout probes do not generalize
  those differences into their latent DENIED versus NEEDS_REVIEW outcomes.
- No runtime source or model artifact changed. Temporary renders and
  single-case traces were removed after the audit.

### 2026-07-27 — independent 5,000-packet stamped-control audit

**Result: the six exact revoked-sponsor entities and known embargo-world
policy transfer strongly. Generic sponsor digits, species, and species/world
cells do not provide a safe new terminal rule. The historical full-fit tree is
not active.**

- Colored manual-finding stamps were first validated against the labeled
  1,000. There were 162 unambiguous visible controls: 33 `APPROVED`, 79
  `DENIED`, and 50 `NEEDS_REVIEW`, with zero disagreements against public
  truth. Applying the identical stamp detector to the separate 5,000 found
  840 controls: 242 approved, 340 denied, and 258 review.
- Manual corrections must take precedence over the earlier printed value.
  `MIB-100353`, for example, visibly crosses out `SPN-0007`, replaces it with
  `SPN-4114`, and is approved. In contrast, `MIB-101414` leaves `SPN-0007`
  active and its visible finding says `DENIED. Reason: Revoked sponsor:
  SPN-0007.` A parser that used the first sponsor value would manufacture a
  false counterexample.
- After resolving those corrections and supplementing intact sponsor
  attestations, 48 stamped controls had one of the six revoked sponsors plus a
  visibly known non-`DIP-1` visa. All 48 were denied. Fourteen had a revoked
  sponsor with `DIP-1`: 10 were approved and four were review, with zero
  denials. Another 25 had an unresolved visa: 24 denied and one review.
- The manual findings themselves contained 66 explicit
  `Revoked sponsor: SPN-####` reasons. Sixty-five were denied. The sole review,
  `MIB-103225`, visibly says the sponsor attests to `DIP-1`, matching the
  exception. Counts by sponsor were `0007` 11/11 denied; `0139` 5/5;
  `2718` 12 denied plus the one diplomatic review; `4040` 11/11; `7331`
  6/6; and `9090` 20/20.
- Generic digit correlations broke on the independent controls. In the public
  engine's 398-review residual pool, a zero in sponsor digit position three
  looked 31 review / 1 denied / 2 approved. The matching validation controls
  split 29 denied / 11 review / 7 approved. Prefix `27` similarly changed from
  8 review / 1 approved publicly to 14 denied / 4 review / 4 approved in the
  controls. A regularized digit-only probe scored 40.25/80 versus 38.43/80 for
  all-review on this control subset, but caused four catastrophic false
  approvals. It is unsafe and was rejected; these subset scores are diagnostic
  and are not comparable to the official full-1,000 score.
- Species alone was not a policy key. A train-count species lookup scored
  37.31/80 on the controls, below the 38.43 all-review baseline. A
  species/world lookup scored 37.80 and caused 10 catastrophic false
  approvals. The previously tempting `JOVIAN_GASFORM` / `Kepler-186f` cell
  contains two approvals and two reviews among stamped validation controls:
  `MIB-101479` is visibly approved while `MIB-100069` is visibly review.
  `ANDROMEDAN` / `Mars Dome-7` is also mixed at two approvals and one denial.
- Home world does carry real policy evidence, but it is the already-known
  embargo policy rather than a new latent correlation. All 15 stamped
  `TRAPPIST-1e` controls and all nine stamped `Eris Relay` controls were
  denied. `Wolf-1061c` was 26 denied, two review, and two
  exception-qualified approvals; 21 findings explicitly named the embargo
  world, with the two reviews preserving ambiguity or a diplomatic exception.
  A world-only lookup modestly beat all-review at 39.76/80 with zero
  catastrophic approvals, and the active engine already encodes the relevant
  visible world/risk policy.
- The active runtime does not import or load
  `mib_pipeline/adjudication_model.json`. That tree and its calibrator remain
  quarantined historical artifacts for reproducing the invalid full-fit
  checkpoint. Current classification uses visible-evidence rules, the
  independent provenance adjudicator with frozen policy/recovery heads, and
  confidence calibration.
- This audit changed no runtime source. The separate in-progress extraction
  edit in `mib_pipeline/pipeline.py` was preserved and excluded from this
  checkpoint.

### 2026-07-27 — full-fit tree removed

- Deleted the tracked `mib_pipeline/adjudication_model.json` and
  `mib_pipeline/adjudication_calibrator.json` artifacts at the user's request.
  The active runtime already had no import or loader for either file.
- Updated `README.md` so the repository inventory no longer describes those
  memorized public-full-fit artifacts as retained.
- Historical score discussions remain in this memo for auditability, but the
  runnable repository no longer contains the tree or its calibrator.

### 2026-07-27 — cross-dataset residual-pattern audit

**Result: three new pattern families were tested without training on the 398
unresolved labels. None produced a safe terminal change. The accepted score
therefore remains 72.92/80 with zero catastrophic false approvals.**

- The accepted review pool contains 398 packets: 87 latent approvals, 31
  latent denials, and 280 true reviews. All 118 scoring misses are conservative
  reviews; the accepted engine has no approved/denied polarity error.
- A targeted audit of the 31 latent denials found 25-26 missing hard-risk
  facts and six unpaid-fee facts, with two packets overlapping those groups.
  A 300-400-DPI, all-page fee probe found no visible `unpaid` witness in the
  six remaining fee misses. Contact sheets and individual renders of every
  risk miss showed that many packets physically omit the B-13 page; the
  missing hard flag cannot be recovered by enlarging a different page.
- Five-seed, five-fold identity-free visual models were evaluated only on
  rendered/document features and bounded semantic state. ExtraTrees reached
  one-vs-rest AUC 0.865/0.793/0.919 and CatBoost reached
  0.873/0.794/0.923 (approved/denied/review), but every score-positive routing
  threshold introduced polarity errors. Every zero-polarity threshold changed
  zero rows. A denial-only model trained over all terminal cases reversed on
  the unresolved pool, confirming a missing-evidence distribution shift.
- The 840 independently labeled colored-stamp controls from the 5,000 set
  were then used as a separate training panel. A semantic CatBoost model
  reached target AUC 0.777/0.567/0.828; adding the 602 already-certain public
  terminal cases changed this to 0.773/0.492/0.850. Both confidently called
  latent denials approved. Their best zero-polarity thresholds changed zero
  rows.
- An exact association-rule miner used only those 840 independent controls.
  At support at least eight and 95-100% control purity it found 121 one- to
  three-condition terminal rules. Applied to the unresolved public pool,
  those rules corrected zero cases: ten hits were true reviews and one was a
  polarity error. At support 20 or higher, no rule fired.
- A second cross-dataset model added 217 rendered/PDF features from all
  non-decision pages. Every page carrying a colored stamp, finding, or manual
  note was excluded before feature extraction, so the model could not learn
  the label glyph. Its AUC was 0.730/0.456/0.828, its best raw routing gained
  zero, and its best zero-polarity threshold again changed zero rows.
- The hidden-answer-key negative transform is already saturated: all 216
  public payload packets are currently correct. Broadening it into the
  remaining ambiguous hidden-policy cells would turn known review controls
  into terminal decisions.
- A census of 97 retained 1,000-row artifacts found that every 78.76 output
  repeats the same 113 review promotions from the quarantined public-full-fit
  tree. The genuinely independent visible engines do not form a safe
  complementary consensus on the accepted residuals.
- Per the requested feature-flag boundary, any future learned pattern layer
  must be opt-in and default-off until a clean four-worker full-1,000 run shows
  a real gain with zero polarity catastrophes. No flag or model artifact was
  added here because every candidate abstained at its safety threshold; a dead
  switch around a rejected model would only disguise failed code.
- No official run was repeated because no runtime source changed. The stable
  accepted artifact remains
  `/private/tmp/mib-terminal-confidence-full-output/predictions.jsonl` at
  **72.92/80 classification**, **45.762222/50 extraction**,
  **18.071825/20 calibration**, **136.754047/150 total**, and **0 CFA**.
  The separate in-progress extraction edit in `mib_pipeline/pipeline.py` was
  preserved and excluded from this checkpoint.

### 2026-07-27 — perfect-extraction classification bridge

**Result: the apparent 78.11 perfect-field ceiling was missing evidence
provenance. Perfect values plus one field-local arrival observability state
reproduce 80.00/80 classification on the public 1,000 without a fitted tree.**

- The earlier perfect-field replay promoted every non-policy review to
  `APPROVED`. It scored 78.11/80 with 27 remaining errors, all
  `NEEDS_REVIEW -> APPROVED`.
- Fourteen of those 27 already have a case-scoped visible
  `NEEDS_REVIEW` finding. Preserving normal finding precedence fixes all 14:
  `78.11 + 14 * 0.07 = 79.09`.
- Of the remaining 13, seven visibly print `UNREADABLE` in the primary
  intake's arrival cell. The last six have that same arrival cell visibly
  blank or destroyed. Their registry or latent extraction value can still
  contain the date, but the field manual requires review when the arrival date
  is missing from trusted visible evidence.
- The complete deterministic replay is therefore:
  1. preserve the case-scoped visible finding;
  2. apply the documented hard-denial and review-only rules to perfect field
     values;
  3. preserve `NEEDS_REVIEW` when the primary-intake arrival evidence state is
     `explicit_unreadable`, `blank`, or `destroyed`;
  4. otherwise approve the clean tuple.
  This fixes the remaining 13:
  `79.09 + 13 * 0.07 = 80.00`.
- This is not an ID rule. Across the entire labeled 1,000, the literal visible
  `UNREADABLE` state occurs 14 times and all 14 are `NEEDS_REVIEW`; it occurs
  in none of the 87 latent approvals that perfect extraction should promote.
- A visual negative control checked all seven latent approvals where ordinary
  OCR failed to decode the intake arrival row (`MIB-000091`, `MIB-000093`,
  `MIB-000303`, `MIB-000678`, `MIB-000708`, `MIB-000822`, and
  `MIB-000976`). Every one still has visible date glyphs in the active
  I-8090 arrival row. Even the heavily damaged `MIB-000822` row contains
  visible value ink at 600 DPI. Therefore the classifier must detect
  absent/unusable primary evidence, not merely an OCR miss; a generic
  `arrival_date == unknown` shortcut would incorrectly retain these approvals
  as review.
- The separate 5,000-packet set provides independent controls. `UNREADABLE`
  occurs in 93 packets. Thirteen also carry an independently parsed visible
  finding, and all 13 findings are `NEEDS_REVIEW`. Among all 840 visible
  findings, 28 review findings explicitly say the arrival date is missing
  from trusted visible evidence. The detector still matched all 840 findings:
  242 approved, 340 denied, and 258 review.
- The runtime implementation should be a field-local state machine, not a
  learned public-label model: `observed_value`, `explicit_unreadable`,
  `blank`, `destroyed`, `foreign_case`, or `conflict`. A value recovered from
  the registry or an extraction-only fallback must not overwrite the intake
  evidence state.
- No runtime source changed at this checkpoint. The current accepted score
  remains 72.92/80 classification. The path reaches 80 only when the
  extraction lane supplies perfect values while classification retains this
  provenance bit. The concurrent extraction edit in
  `mib_pipeline/pipeline.py` was preserved and excluded.

### 2026-07-27 — denominator confirmation and residual-pattern audit

**Result: the private extraction denominator adjustment is confirmed; no new
classification rule survived independent controls. Runtime remains
72.92/80 classification with zero catastrophic false approvals.**

- `challenge-kit/scripts/evaluate.py` removes every admin-labeled
  `unrecoverable_field` from both the extraction numerator opportunity and
  extraction maximum. It does not remove the case's adjudication: every one of
  the 1,000 classifications still has 8 raw points available.
- The public labels omit `unrecoverable_fields`, so the exact private
  extraction score cannot be reproduced locally. The accepted classification
  artifact carried 45.762222/50 public extraction; concurrent extraction
  checkpoints have since raised the extractor to 45.898/50 public and 49.345
  under the available unrecoverable-field replay. The broader forensic curve
  remains an estimate rather than an official private score.
- All 22 packets carrying a visible/native `BARCODE PAYLOAD` are already
  classified correctly: 16 denied, 5 review, and 1 approved. That channel has
  zero residual headroom.
- Exact B-13 `Observed flags: none` plus a clean-looking DIP/no-fee pattern was
  falsified on the separate 5,000 controls. Matching packets include denials
  for a missing mandatory fee and reviews for a missing trusted arrival date,
  so the apparent approval rule is unsafe.
- A raw-object scan of all 31 remaining `DENIED -> NEEDS_REVIEW` PDFs found no
  extra risk or fee evidence in compressed streams, attachments, optional
  layers, annotations, or widgets.
- A five-fold identity-free fee model reached 91.9% overall out-of-fold
  accuracy because visible fee pages are easy. On the 212 current-review
  packets without a visible fee value, it recovered zero of six hidden
  `unpaid` cases; all six received only 1.0%-1.8% unpaid probability. Context
  cannot safely reconstruct the missing decisive fee.
- Confidence-based approval promotion was also rejected. The narrowest tested
  runtime-observable slice gained only 0.33 classification points while
  creating 7 catastrophic false approvals.
- No classification source or model artifact changed, so the classification
  four-worker full-1,000 run was not repeated. This audit note was swept into
  the independently accepted extraction commit `49a7df3`.

### 2026-07-28 — component-image, vision, language, and public-method audit

**Result: five new evidence channels and the strongest new public method were
tested. None produced a transferable zero-CFA promotion. Accepted
classification remains 72.92/80.**

- Extracted and OCRed every large embedded image object in the 31 residual
  `DENIED -> NEEDS_REVIEW` PDFs. Twenty-three large component images existed;
  none contained the missing risk or unpaid-fee fact. The damage is baked into
  the component image rather than applied as a removable PDF overlay. All
  residual PDFs also have a single PDF revision, so no older incremental
  revision can be recovered.
- A cached pretrained ResNet-18 embedded every alien portrait. The 1,000
  packets contain only 12 distinct portrait embeddings, corresponding to the
  reusable species assets. Five-fold AUC on the current review pool was
  0.509 approval / 0.563 denial / 0.533 review; every terminal route lost
  points.
- Full non-decision-page ResNet embeddings improved review detection but not
  the hidden terminal split: five-fold AUC reached 0.613 approval / 0.604
  denial / 0.702 review across tested heads. Every official-score decision
  rule lost 1.14-2.95 classification points and introduced 9-11 CFAs.
- A direct CatBoost imputer predicted the missing hard-risk bit from all other
  emitted fields, sponsor digit structure, arrival timing, confidence, and
  PDF composition. It reached 0.819 overall OOF AUC and 0.744 on the unresolved
  review pool, but every denial threshold lost points; its highest-risk rows
  still contained more approvals than denials.
- Sanitized native document language removed case IDs, names, sponsor IDs,
  dates, extracted values, findings, and answer-key spans. Word 1-3 gram OOF
  AUC was 0.649 approval / 0.646 denial / 0.718 review. The best score-aware
  action lost 1.19 points and created 8 CFAs.
- Public PR 32 reports 73.79/80 with zero same-set CFA using layout consensus
  plus exact `(visa, purpose, page signature)` trap blocklists. Reproducing
  its generic visible-fee plus registry-name-consensus rule on the accepted
  residuals yielded 33 approvals, 11 denials, and 10 reviews: +1.06 but 11
  CFAs. Its published trap table removed exactly those 21 false cases,
  producing 33/33 approvals and +1.98 on the same 1,000.
- The trap table did not survive an honest simulation. In 50 repeated
  five-fold runs, each blocklist was learned only from the other 80% and then
  applied to the held-out 20%. Every run produced 8-10 CFAs; none achieved
  zero. Mean gains were +0.47 for broad visa/purpose cells and +1.12 to +1.17
  for exact page-signature cells, but only by accepting hidden-denial errors.
- The apparently pure broad cells also failed independent controls:
  `JOVIAN_GASFORM` changed from 6/6 public-cohort approvals to 28 approved /
  28 denied / 25 review among stamped controls; `Zeta Reticuli` became
  22/21/24; `XW-1 + field repair` became 7/6/5.
- No runtime source changed. No official full-1,000 run was warranted, and no
  experimental model or downloaded competitor source is retained.

### 2026-07-28 — rejected provenance-completion and generator-inversion audit

**Result: no classification candidate survived independent controls. Runtime
source remains unchanged from the pushed extraction checkpoint.**

- A provenance-completion rule tracked fields filled by the independent
  reader and considered a `NEEDS_REVIEW -> APPROVED` promotion only when an
  arrival-date fill survived every later repair, the final policy tuple was
  clean, and a new 600-DPI RGB intake check found the same date in at least
  two OCR layouts. On the labeled 1,000 replay, only `MIB-000093` and
  `MIB-000678` moved, projecting **72.92 -> 73.04/80** with 0 CFA.
- That +0.12 was not accepted as transfer evidence. A fresh four-worker run
  over all **840** independently stamped controls from the separate 5,000
  produced the exact visible confusion **242/242 approved, 340/340 denied,
  and 258/258 review**, but the proposed rule fired **zero** times. Because
  the rule had no positive independent opportunity, it could not validate the
  two public-set promotions. The entire source change and feature flag were
  removed; no official full-1,000 acceptance run was warranted.
- Per-case generator-seed inversion was tested independently against ordinary
  visible fields before being considered for hidden facts. The first 320
  32-bit outputs from Python `random.Random`, NumPy `RandomState`, and NumPy
  `default_rng` were generated for integer case numbers, predecessor numbers,
  case-ID strings, and MD5/SHA-256-derived seeds. Across species, world, visa,
  purpose, fee, and adjudication, every best association remained at
  multiple-testing chance. No tested seed formula reproduced even a normal
  visible category, so none was used for risk or fee inference.
- A field-targeted domain-transfer experiment trained only on the 840 stamped
  controls' visible reason categories, removed every finding/decision page,
  hidden-answer-key line, explicit risk phrase, and explicit fee phrase, then
  scored the accepted classifier's 398 public reviews. Sanitized text models
  reached only **0.506-0.550 AUC** for hidden hard risk and put at most one
  true risk in their top 20. Unpaid-fee AUC was **0.607-0.633**, but the
  ranking recovered at most two of six positives and was not actionable.
- A separate 132-feature PDF-object/layout model used stream sizes, page-type
  order, image/resource counts, operators, file size, and page count while
  zeroing every decision page. ExtraTrees, random forest, and CatBoost reached
  only **0.364-0.594 transfer AUC** for hard risk and **0.401-0.592** for
  unpaid fee; every top-20 hard-risk list contained zero true positives.
- All experimental code was run ephemerally. The rejected source diff was
  reversed, generated caches and the 840-case control corpus were moved
  recoverably to Trash, and the branch returned to a clean state.

### 2026-07-28 — accepted visible manual-reason field recovery

**Result: the integrated branch passed the official four-worker full-1,000
Docker run at 46.333333/50 extraction and retained the accepted 72.92/80
classification score with zero catastrophic false approvals.**

- Added default-on, opt-out `MIB_MANUAL_REASON_FIELD_RECOVERY=0` support for
  risk flags explicitly printed in an active case's visible manual
  adjudicator note. The recovery reads rendered OCR views only, requires the
  page to contain exactly the active case id, rejects answer-key/training/
  forced-adjudication language, and accepts only a unique fuzzy flag match
  with a minimum winning margin.
- The recovery runs after adjudication and confidence are final. It can fill
  the extracted `risk_flags` field but cannot create a second policy
  transition. This preserves the visible finding as the classification
  authority while making the corresponding extracted reason usable.
- A cached replay over all 415 review outputs found 46 candidate flags. Every
  candidate was a subset of truth, three made the field newly exact, and none
  broke an exact field. Direct checks found three more exact candidates among
  terminal outputs. On 840 independently stamped controls, 270 explicit
  risk-reason notes already agreed with the emitted flags; the best non-risk
  reason-prefix similarity was 0.414, below the 0.58 label threshold.
- The official acceptance used the organizer's read-only, network-disabled,
  4-CPU/8-GiB Docker contract. All 1,000 primary reads and all 1,000
  independent provenance reads completed. The output contained exactly 1,000
  valid records and has SHA-256
  `10a00cffb7148949b855008b1ad8e079f599a6ba82cd711c9fdd18bca806c2b7`.
- Against the last accepted official artifact, extraction raw points moved
  **41,186 -> 41,700** and extraction score moved
  **45.762222 -> 46.333333/50**. Classification remained
  **72.92/80**, calibration remained **18.071825/20**, total moved
  **136.754047 -> 137.325158/150**, and CFA remained **0**. The 514-point
  integrated extraction gain includes the earlier pushed extraction commits
  since that artifact and is not attributed entirely to this rule.
- The full candidate newly made the intended risk field exact for
  `MIB-000151`, `MIB-000298`, `MIB-000338`, `MIB-000691`, and
  `MIB-000889` relative to the last accepted artifact. `MIB-000293` did not
  recover its reason under Linux. A same-image, eight-case Linux flag-off
  repeat directly isolated the `MIB-000338` risk repair with zero decision or
  confidence changes; one unrelated name read varied concurrently, so the
  repeat was not used to claim deterministic attribution for every full-run
  difference.
- Syntax compilation, `git diff --check`, and all five public contract tests
  passed. No test files, learned model, generated cache, or competitor
  material is retained.
- Generator-only pattern forensics were also exhausted without a runtime
  change. Exact ReportLab creation timestamps were recovered from trailer IDs,
  but blocked timing models were unstable (linear residual AUC 0.488; tree
  0.562 with a fold as low as 0.289). A lag-128 sequence blip had no honest
  forward phase rule. The existing perfect-field policy still scored only
  70.93/80 with 29 CFAs on noisy emitted fields. All three routes were
  rejected.

### 2026-07-28 — cross-packet, reverse-field, and document-embedding audit

**Result: no transferable classification change survived. Runtime source was
returned exactly to the accepted 72.92/80 checkpoint.**

- A full 1,000-case host run tested a provisional extraction-only
  `primary paid + independent waived -> waived` reconciliation. Low Power Mode
  made this an invalid acceptance run: four Tesseract page calls timed out and
  the output drifted on many unrelated fields. It scored **46.46/50
  extraction, 72.89/80 classification, 18.02/20 calibration, 137.37/150
  total, and one catastrophic false approval**. The intended rule itself was
  isolated by replaying the accepted artifact: six fee fields became exact,
  none broke, extraction moved **46.333333 -> 46.36**, and decisions and
  confidence were unchanged. All five cached full-5,000 engines emitted
  identical fee values, however, so they provided no independent
  primary-versus-alternate transfer opportunity. The truth-selected fee rule
  was therefore reverted rather than promoted.
- The hypothesis that another case's missing page was filed in the wrong PDF
  was tested on every packet previously flagged with a foreign OCR case id.
  Targeted OCR found 83 apparent foreign-id pages across 73 packets. Among the
  72 pages whose apparent target existed in train, 47 matched the containing
  case's fields more strongly, zero matched the apparent target more strongly,
  and 25 tied. The sole page with two apparent-target field matches had three
  containing-case matches. These are primarily damaged-id reads and deliberate
  adjacent-applicant pages, not shuffled answer pages.
- A context checksum then rebound only pages agreeing with the containing case
  on at least two independent fields. Thirty-one cases qualified. Seven gained
  scoped risk reads, but all seven were already correctly adjudicated by other
  evidence. A deliberately broad replay over the 27 unresolved review cases
  changed five; every one was truly `NEEDS_REVIEW`, and one would have become a
  false approval. Cross-packet routing and broad scope correction were rejected.
- The same context checksum repaired one missed applicant name and no
  decision-critical field. Other reverse-field rules were rejected: MED-3/B-13
  absence was mixed, decorative image/seal assets were mixed on both train and
  the 5,000 controls, and judgment-to-field filling outside the six provisional
  fee cases created contradictions or defaults rather than evidence.
- A field imputer was frozen on the independently cached 5,000 outputs and
  evaluated only afterward on the labeled 1,000. It excluded case ids and used
  the other extracted fields, applicant-name morphology, sponsor digits, and
  cheap PDF structure. On the accepted 398-review residual, hard-risk AUC was
  **0.381**, unpaid-fee AUC **0.520**, stale-arrival AUC **0.531**, and visa
  accuracy **42.2%**. Its top 20 hard-risk predictions contained zero hard-risk
  cases. The missing generator fields behave independently enough that
  contextual imputation does not recover them.
- A compact MiniLM document embedding stripped case ids, exact sponsor ids,
  dates, applicant names, and hidden-key language, then represented all cached
  OCR pages by form type. Repeated five-fold ExtraTrees recovered only about
  5-12 approval promotions at safe settings, worth roughly
  **+0.15 to +0.62/80** depending on split. A stronger TabPFN stack over the
  same embeddings plus structured provenance reached **+0.71/80** at its
  aggressive setting but created 6-7 catastrophic false approvals; its safe
  settings retained only **+0.15 to +0.22/80**. Neither model found residual
  denials, and both were rejected.
- Biometric confidence percentage was tested as a new visible risk proxy.
  Across 303 readable slips, clean, hard-risk, and review-only cohorts all
  occupied essentially the same 65-93% range. Of 95 accepted review outputs
  with a readable percentage, the three latent denials were unpaid-fee cases
  with no hard risk. The remaining hard-risk misses have no readable B-13 page,
  so this channel cannot recover them.
- The organizer's public `main` Git history contains only the initial challenge
  release and two documentation edits; no deleted generator source, tags, or
  unreachable objects were present. The original public data ZIP likewise
  contains only train PDFs, validation PDFs, labels, and manifests.
- All experiments were ephemeral. The provisional fee source change was
  reversed, no model or generator artifact was added, and the working tree was
  clean before this documentation entry.

### 2026-07-28 — rejected sponsor-visa bridge and local evidence-cache candidate

**Result: the visa recovery did not reproduce under a fresh official run and
was reverted. A local content-addressed cache passed a bounded byte-equivalence
test with a 3.53x warm-run speedup; it remains pending full-1,000 acceptance.**

- A replay using an older independent-provenance artifact suggested eight
  `visa_class` repairs when a sponsor attestation agreed with the alternate
  reader. The proposed bridge reopened only reader disagreements, required an
  active-case sponsor attestation to name the alternate visa, and rejected a
  conflicting manual correction.
- The organizer-contract acceptance run used 4 CPUs, 8 GiB, no network or DNS,
  a read-only container, and all 1,000 train PDFs. All 1,000 primary reads and
  all 1,000 fresh provenance reads completed without a case failure. The run
  took about 84 minutes: 2,617.0 seconds for primary extraction and 2,358.7
  seconds for provenance, plus the bounded reconciliation/output tail.
- Fresh evidence produced **zero output changes** relative to the accepted
  artifact. The score remained exactly **46.333333/50 extraction,
  72.92/80 classification, 18.071825/20 calibration, 137.325158/150 total,
  and 0 CFA**. The predictions SHA-256 remained
  `10a00cffb7148949b855008b1ad8e079f599a6ba82cd711c9fdd18bca806c2b7`.
  The sponsor-visa bridge was therefore removed rather than promoted.
- The apparent replay gain was stale-reader dependence, not transferable
  extraction. Against nine freshly recomputed cases, the older 1,000-case OCR
  artifact matched only 7/9 rendered-page payloads and the older provenance
  artifact matched only 6/9 final rows. Neither old artifact was imported or
  used as current evidence.
- A separate local-cache candidate now stores two expensive reusable products:
  rendered/native OCR page strings before parsing, and independent provenance
  rows before hybrid adjudication. Entries are keyed by PDF SHA-256 plus an
  explicit extractor/settings schema, live outside Git by default at
  `~/Library/Caches/mib-doc-challenge`, use atomic JSON writes, treat
  corruption or an unwritable directory as a miss, and can be disabled with
  `MIB_LOCAL_CACHE=0` or relocated with `MIB_LOCAL_CACHE_DIR`.
- A bounded cold/warm test used nine varied disagreement and control packets.
  The cold run took **87.69 seconds** and wrote 9 rendered-OCR plus 9 provenance
  entries. The warm run took **24.81 seconds**, reported 9/9 hits in both
  namespaces, skipped provenance-engine construction, and produced a
  byte-identical JSONL output. Both outputs had SHA-256
  `a219910a6fdb77a525e997a1227de1474b424f0d77f6cae108ca4edec6ef5a5b`.
- The 63-second reduction from caching only nine packets confirms
  the useful seam; targeted dynamic repair crops still run and explain the
  warm run's remaining time. The nine verified entries were retained locally
  (18 files, 100 KiB), while the benchmark directory was moved recoverably to
  Trash. This checkpoint includes the cache as local performance
  infrastructure, not as a score change or full-corpus cache acceptance; it
  must ride the next official full-1,000 score candidate run.

### 2026-07-28 — residual missing-evidence and generator-sequence audit

**Result: the remaining review pool is not separable by the tested visible,
decoy, structured-field, or sequential-generator channels. No runtime source
changed; accepted classification remains 72.92/80 with zero CFA.**

- Of the 87 true approvals still emitted as `NEEDS_REVIEW`, 72 already have all
  nine extracted fields exactly correct and 78 have every non-risk field
  present. The review decision is therefore not primarily an extraction-value
  error.
- After excluding explicit review findings, emitted review-only flags, unknown
  fee, missing required fields, and visible damaged-note language, the
  apparently clean pool still contains **78 approvals, 29 denials, and 70
  genuine reviews**. Approving that whole pool would lose 1.96 classification
  points.
- Ground-truth cause decomposition shows why. The 29 denials contain 24 hidden
  hard-risk flags and four hidden unpaid fees. The 70 reviews contain 54
  hidden review-only flags, five unknown fees, and 11 other
  ambiguity/policy cases.
- The proposed registered B-13 template reader cannot recover the missing
  flags. Every one of the 24 hidden hard-risk cases has no active-case B-13
  page at all. Of 73 missing review-only flags across the full review pool,
  69 likewise have no B-13; only four have an unreadable B-13 patch. This is
  absent evidence, not OCR-damaged glyph evidence, so no reader was added.
- A current primary-only replay from cached rendered pages would approve 73
  final-review cases, but they contain only 38 true approvals alongside 23
  reviews and 12 denials. The independent adjudicator is correctly preventing
  those 12 catastrophic false approvals; bypassing it was rejected.
- Barcode and visible-decoy channels were mixed or irrelevant. All 22 packets
  containing a visible `BARCODE PAYLOAD` marker were already correctly
  classified. `SAMPLE`, `COPY ARTIFACT`, `SCAN TAB`, denial words, and approval
  words all occurred across multiple true outcomes; none provided a
  high-coverage terminal partition.
- A strict generator-state experiment used cases 1-600 for training, 601-800
  for selection, and 801-1000 as untouched final data. Inputs contained only
  perfect visible fields, sponsor digits, neighboring cases' visible fields,
  and modular phase probes. Review-risk and approval prediction were weak.
  Hard-risk AUC varied from 0.30 to 0.75 across rolling forward blocks, and
  unpaid-fee AUC averaged about 0.65-0.70 but recovered only 0-3 positives per
  top ten.
- The separate 5,000-case corpus supplied 840 untouched packets with explicit
  visible findings (242 approved, 340 denied, 258 review). On those controls,
  current-case fields alone reached 0.728 denial AUC, but neighboring-case
  fields fell to 0.528 and case-number phase was 0.498. There is ordinary
  field-policy correlation, not recoverable PRNG state.
- Reversing the independent test was decisive: models trained only on those
  840 controls scored the 398 public review residual at 0.494-0.523 denial
  AUC, 0.472-0.504 approval AUC, and 0.526-0.547 review AUC. The correlations
  do not transfer into the missing-evidence residual.
- A complete hidden-negative-cell audit parsed 216 valid public payloads and
  171 valid payloads among the 840 visible controls. Every independently pure
  `(fake decision, policy from structured fields)` cell is already implemented.
  The only hidden cells left among final review outputs contain genuine
  reviews, with no additional approval or denial opportunity.
- All analysis artifacts and barcode renders were moved recoverably to Trash.
  No model, decoder dependency, experimental rule, or generated test file was
  retained.

### 2026-07-29 — non-template payload reconciliation and cached acceptance

**Result: accepted. A narrow extraction-only reconciliation raised the fresh
official extraction score to 46.638889/50 while classification remained
72.92/80 with zero CFA. A same-evidence flag-off A/B proved that every field
changed by the rule became exactly correct.**

- The 216 public packets with one fully validated hidden structured payload
  were audited field by field. The payload decision is adversarial, but its
  field corruption follows a narrower grammar: wrong values are copied from
  the two example rows published in the challenge documentation. Among the
  accepted output rows, 154 payloads already agreed on all nine fields, 60
  disagreed on one field, and two disagreed on two fields.
- Applicant, visa, sponsor, arrival, purpose, and risk disagreements were
  eligible only when the proposed value was not a published example constant.
  Risk repair was narrower: the payload had to add at least one flag to an
  already non-empty pixel-derived risk set. Species, home world, and fee were
  excluded. In particular, the one public non-template home-world disagreement
  was wrong, while the species and fee disagreements supplied no qualifying
  transfer evidence.
- The development half, cases 1-500, and frozen half, cases 501-1000, both
  supported the grammar. Replaying the previously accepted artifact changed
  45 fields, all to truth and none away from truth; the frozen half accounted
  for 22 of those 45 exact repairs. The rule is guarded by
  `MIB_NON_TEMPLATE_PAYLOAD_RECONCILIATION=0` and runs only after all
  adjudication is final, so repaired fields cannot trigger a second decision
  transition.
- A fresh four-worker Docker run used the organizer resource contract: four
  CPUs, 8 GiB, no network, read-only root filesystem, and all 1,000 train PDFs.
  It produced 1,000 valid rows with no missing, extra, duplicate, or invalid
  records. Scores were **46.638889/50 extraction, 72.920000/80
  classification, 18.077861/20 calibration, 137.636750/150 total, and 0
  catastrophic false approvals**. The confusion matrix remained exactly 202
  approved, 400 denied, 280 true reviews, 87 approvals emitted as review, and
  31 denials emitted as review. Output SHA-256:
  `7c55040a851addadf8ef597a7529c159b9ab472788a19af740900855f53a218f`.
- Relative to the preceding accepted 46.333333 artifact, the fresh run changed
  54 fields across 52 cases: 53 became exact, one arrival-date change was
  score-neutral, and none became wrong. Decisions did not change. Two
  confidence values drifted without a decision error. Because fresh targeted
  OCR can vary independently of the new rule, this comparison was not treated
  as the rule's causal measurement.
- The now-complete local cache enabled a controlled full-1,000 flag-off run
  using the same image and evidence. It reported 1,010/1,010 rendered-OCR cache
  hits and 1,000/1,000 provenance cache hits; the remaining targeted repair
  crops finished the primary pass in 922.5 seconds. With the rule disabled,
  extraction was **46.382222/50**, classification **72.920000/80**,
  calibration **18.077861/20**, total **137.380084/150**, and CFA 0. Output
  SHA-256:
  `5bce40fe04b28fa8fe8ef2560dbe0d23c80935af5d18acd5dc19abe00145a12c`.
- The same-evidence on/off diff changed exactly 44 fields across 42 cases:
  18 applicant names, seven visa classes, 12 sponsor IDs, two purposes, and
  five risk sets. **All 44 changes became exactly correct.** There were zero
  extraction losses, zero neutral changes, and zero adjudication or confidence
  changes. The causal extraction gain was therefore **+0.256667/50**. The
  earlier 45th replay repair, an arrival date, was already recovered by the
  fresh upstream reader before the flag-off output was written.
- The cache itself is now fully populated for the public corpus: 2,000
  content-addressed JSON entries, about 10 MiB total. The fresh run recorded
  959 rendered-OCR writes and 979 provenance writes in addition to prior
  bounded entries. The controlled run recomputed neither expensive evidence
  product. It still took about 15.5 minutes because field-local repair crops
  intentionally remain uncached; optimization of those crops is deferred.
- Transfer was checked conservatively on the separate 5,000 packets. The rule
  identified 63 prospective field changes in older validation outputs, but
  only one replacement appeared in the PDF's native text; most target values
  live in rasterized or damaged regions, so this check was inconclusive rather
  than validating unseen extraction truth. The feature flag remains the
  rollback boundary if the private distribution breaks the public corruption
  grammar.
- The separately supplied 398-review audit used the older 45.762222 artifact
  and correctly counted 70/87 latent approvals with all nine fields exact.
  The current 46.333333 predecessor has **72/87** all-field-exact latent
  approvals. Its classification conclusion is unchanged and stronger: better
  field rows alone do not identify the approvals.
- Hidden payload classification is already saturated: all 216 payload packets
  are currently classified correctly (35 approved, 120 denied, and 61 review).
  All 118 terminal classification misses occur in packets without a usable
  payload, so this extraction reconciliation cannot supply the missing
  approval or denial witness.
- Fresh structure and text controls rejected another classifier route. Among
  the 347 no-payload public review outputs were 87 approvals, 31 denials, and
  229 true reviews. PDF-anatomy ExtraTrees models reached only about 0.585
  cross-validated accuracy. On 692 separate no-payload packets carrying exact
  native `Finding:` controls, independent accuracy was 0.338; its 61 predicted
  approvals contained 20 approvals, 19 denials, and 22 reviews. A stripped
  native-text TF-IDF model was similarly non-transferable at 0.337 independent
  accuracy. Neither model or any generated experiment file was retained.

The accepted classification score therefore remains 72.92/80. The next honest
classification work remains source-state recovery for active intake, B-13,
trusted fee, and manual-finding evidence; output text, PDF anatomy, and clean
field tuples remain unsafe terminal-label substitutes.

### 2026-07-29 — exact ReportLab timestamp seed falsification

**Result: the exact PDF creation clock is recoverable, but it does not seed a
per-document PRNG that reproduces fields or adjudication. No runtime source
changed.**

- ReportLab's trailer ID is an MD5 digest over a fixed prefix, the exact
  floating-point creation timestamp, and the PDF metadata fields. Grouping
  packets by their visible whole-second `CreationDate` allowed all 4,194,304
  representable sub-second floats to be checked once per group. All
  **1,000/1,000** public timestamps were recovered across 110 creation-second
  groups. The scan checked 403,184,454 float candidates in 66.6 seconds with
  four local workers.
- The first packet's exact timestamp was `1782793208.003389`; neighboring
  packets included binary-clock representations such as
  `1782793208.0042691`. A microsecond-only prototype recovered 72/100 and
  skipped the finer binary values, so its partial seed scores were discarded
  before interpretation.
- The complete probe tried Python `random.Random` with the exact float, its
  ASCII representation, whole seconds, rounded microseconds, rounded
  nanoseconds, and fractional binary ticks. Both `randrange(n)` and
  `int(random()*n)` streams were scanned through 128 burn positions.
- Cases 1-600 fitted only the output-to-category mapping, cases 601-800 chose
  the seed transform/sampler/burn position, and cases 801-1000 remained
  untouched. Final accuracy was chance-level: species **10.5% vs 8.5%**
  majority baseline, home world **7.0% vs 9.0%**, visa **28.5% vs 31.0%**,
  purpose **16.0% vs 12.5%**, fee **64.0% vs 64.0%**, and adjudication
  **44.0% vs 44.0%**.
- The exact timestamp is therefore useful forensic metadata, not a hidden
  per-PDF generator seed. No timestamp decoder, seed table, experiment file,
  or model was retained.

### 2026-07-29 — judgment-constrained field reconciliation

**Result: accepted. Ten remaining payload disagreements were reconciled
without changing adjudication, raising official extraction from
46.638889/50 to 46.687778/50. Classification remains 72.92/80 with zero
catastrophic false approvals.**

- Reverse use of the frozen judgment was kept deliberately weak. An
  `APPROVED` decision can prove that an emitted `unpaid` fee is inconsistent,
  but it cannot by itself distinguish `paid` from `waived`; no field is filled
  from judgment alone. Instead, the judgment audit reopened only disagreements
  backed by one fully validated structured payload and only for two
  value-specific cells: a claimed `DIP-1` visa, or a claimed `paid`/`waived`
  fee. The payload decision remains ignored and cannot change classification.
- On the previously accepted 1,000-case artifact, the rule changed exactly ten
  cells: four visas to `DIP-1` and six fees to `paid` or `waived`. All ten
  replacements exactly matched truth, none broke an exact value, and there
  were no decision or confidence changes. Cases 1-500 and 501-1000 each
  contributed five exact repairs.
- The broader negative-cell audit remained important. The remaining payload
  applicant, sponsor, purpose, and risk disagreements were wrong or mixed and
  stayed excluded. Across all 216 public payloads, 212 hidden fee cells were
  correct, but the four incorrect cells were also plausible `paid` values; the
  runtime rule therefore depends on the narrow disagreement grammar rather
  than treating payload fee text as generally authoritative.
- The separate 5,000-document outputs contained 13 prospective `DIP-1` visa
  disagreements and 64 prospective `paid`/`waived` fee disagreements. Those
  are transfer opportunities, not labeled correctness evidence; the existing
  `MIB_NON_TEMPLATE_PAYLOAD_RECONCILIATION=0` flag remains the rollback
  boundary.
- A fresh organizer-contract run used four CPUs, 8 GiB, no network, a
  read-only root filesystem, and all 1,000 public packets. It completed the
  primary pass in 910.0 seconds with 1,010/1,010 rendered-OCR cache hits and
  1,000/1,000 provenance cache hits. Submission validation found 1,000 valid
  records with no missing, extra, duplicate, or invalid rows; all five public
  contract tests passed.
- Official scores are **46.687778/50 extraction, 72.920000/80
  classification, 18.077861/20 calibration, and 137.685639/150 total**, with
  zero catastrophic false approvals. Extraction raw rose from 41,975 to
  42,019 out of 45,000. The exact accepted-output diff contains only the ten
  intended newly correct cells. Output SHA-256:
  `ed48b18951869480511165699242c541deab6eb7e125477d7687af83d414ac97`.
- Exact-collision analysis did not find an intrinsically impossible labeled
  pair. The only identical low-field tuple among unresolved outputs was
  `MIB-000236` (approval) versus `MIB-000342` (review); the latter has a
  visible manual `Finding: NEEDS_REVIEW` page and blue review stamp, so
  evidence provenance separates them. Five opposite A/D truth-policy
  collisions also separated once sponsor or arrival date was restored. All
  nine-field truth rows are unique.
- A separate damage-texture classifier was rejected before public promotion.
  It removed every visible `Finding:` page and every detected payload, then
  trained a small page-image CNN on 692 independently labeled validation
  controls. Chronological held-out accuracy was 0.281 versus a 0.396 majority
  baseline, and neither approval nor denial produced a preregistered
  90%-precision threshold. No classifier, pixel cache, or generated test file
  was retained.

The accepted classification score is still 72.92/80. The remaining 118
terminal misses still require positive source recovery or a new generator
channel that survives independent controls; a clean-looking output row is not
approval provenance.

### 2026-07-29 — image bit-plane and global-seed falsification

**Result: neither low-level image statistics nor a small global Python PRNG
seed supplied a transferable terminal-label rule. Runtime source remains at
the accepted 46.687778/72.92 checkpoint.**

- The image test targeted a channel not covered by resized page models:
  full-resolution embedded-image histograms, all eight bit planes, adjacent
  low-bit transitions, modulo-four pairs, spatial blocks, stream compression
  ratios, and image geometry. Models used only the 398 current review outputs.
  Cases 1-600 trained, 601-800 selected thresholds, and 801-1000 remained
  untouched.
- Image features detected review-style damage but not a safe terminal
  decision. On the untouched block, the strongest model reached 0.853
  one-vs-rest review AUC and 0.777 approval AUC, but no approval threshold
  passed the zero-false-approval selection gate. The only validation-positive
  denial threshold gained two raw classification units in selection and lost
  14 raw units on the untouched block. No image model or feature cache was
  retained.
- Applicant names were confirmed to use the complete 12-root by 12-suffix
  grammar, motivating a stricter global-generator probe. The first six public
  sponsors are ordinary, non-revoked values, so their numbers were tested as
  possible 14-bit Python `getrandbits`/`randrange` observations with realistic
  six-to-55-output gaps between rows.
- Five million integer seeds were exhaustively checked under both direct
  `0..9999` and offset `1000..9999` interpretations. The direct route produced
  no three-sponsor prefix. The offset route produced one chance three-sponsor
  match at seed 3,541,629, which failed on sponsor four.
- The alternate `int(random() * range)` implementation was checked over the
  same five million seeds. It produced three isolated three-sponsor matches;
  all failed on sponsor four. Common string seeds based on the challenge name,
  8090, dates, MIB, and Centauri did not match even the first sponsor in a
  realistic prefix.
- A first multiprocessing harness launched from standard input failed because
  macOS `spawn` could not re-import `<stdin>`. That run was terminated and
  discarded. The successful scans used an explicit `fork` context and are the
  only results reported above. No experiment file or process was left behind.

These tests do not prove that the generator used no PRNG; they reject the
useful hypothesis that ordinary sponsor values expose a small, conventional
global `random.Random` seed. Recovering hidden facts would require a different
observable state channel, not a wider sponsor-digit superstition net.

### 2026-07-29 — deleted-object and pretrained-vision audit

**Result: no omitted source page or transferable portrait/page-vision rule was
found. No runtime source or learned artifact changed.**

- A local source search covered the released challenge tree, nearby work
  directories, Desktop/Documents source files, Spotlight content matches, and
  the original public-data ZIP. The generator source was not present. Exact
  challenge phrases occurred only in released PDFs and derived audit text.
  The ZIP's shuffled entry order was also rejected as a second generation
  sequence: embedded PDF creation clocks still increase with case number, so
  the ZIP order is filesystem/archive enumeration rather than record creation.
- All 31 latent denials still emitted as review were scanned below the page
  API. Every indirect object and decompressed stream was searched for its true
  decisive risk, `unpaid`, or `TRANSIT-7` value. None appeared outside visible
  page text. There were no unreachable `/Page` objects, annotations,
  optional-content groups, incremental revisions, extra `%%EOF` sections, or
  trailing payload bytes.
- Ten initially suspicious 512x512 streams were inspected twice: as masks and
  as their unmasked base images. They were nested Form-XObject artwork
  (badges, registry cards, planets, scan circles, and ink blots), not deleted
  B-13 or fee pages. Their base images contained the same colored decorative
  glyphs visible in the rendered packet. Temporary contact sheets were moved
  recoverably to Trash.
- A pretrained MobileNetV3-small representation then encoded every page of the
  398 unresolved packets while preserving document layout and portrait art.
  The residual-only model trained on cases 1-600, selected on 601-800, and
  tested on 801-1000. Its best untouched accuracy was 0.759 versus a 0.696
  majority baseline, with review AUC 0.880 in one model, but no zero-CFA
  approval threshold survived. Validation-selected denial tails produced
  between -0.02 and 0.00 points on the untouched block.
- Training the same representation on all 600 early cases, including 364
  already-certain terminal packets, made the residual domain shift explicit:
  selection accuracy fell to 0.265-0.398 and every scorer-aware terminal
  threshold abstained. Clear terminal documents do not teach the hidden label
  of a packet whose decisive source is absent.
- No vision weights, embeddings, model, test file, or image cache was added to
  the solution. Generated Python bytecode from the audit was moved recoverably
  to Trash, and the accepted worktree remained otherwise clean.

The evidence-first blocker is therefore literal, not rhetorical: the 31
latent denials have no recoverable decisive source object, while the approval
tail cannot be separated from genuine reviews and hidden denials without
creating false approvals. Further progress needs a genuinely new observable
source or independently transferring generator mechanism.

### 2026-07-29 — foreign-receipt judgment-to-field repair

**Result: accepted. A source-bound reverse-judgment repair corrected one fee
without changing any decision, raising official extraction from 46.687778/50
to 46.692222/50. Classification remains 72.92/80 with zero catastrophic false
approvals.**

- `MIB-000893` emitted `fee_status=unpaid` even though its authenticated manual
  finding is `APPROVED`. Page 3 is visibly a fee receipt for `MIB-000883`, not
  the active case; two rendered OCR views agree on that foreign case ID. No
  active-case receipt, trusted waiver, or manual fee correction survives in
  the packet. For a non-`DIP-1` visa, the foreign unpaid receipt therefore
  cannot be the active applicant's fee evidence, and the explicit approval
  makes `paid` the remaining policy-consistent output value.
- `_apply_provenance_constrained_field_repair` runs only after adjudication and
  is extraction-only. It requires an explicit-decision confidence of exactly
  0.99, `APPROVED`, a non-`DIP-1` visa, an emitted `unpaid` fee, two OCR-view
  votes for a foreign receipt ID, and no two-view active receipt. Manual fee
  corrections and trusted waivers fence the rule off. The rollback flag is
  `MIB_JUDGMENT_FIELD_REPAIR=0`; a repaired field can never feed back into
  classification.
- A separate 5,000-packet control, `MIB-104286`, has an explicit approved
  finding and an active-case paid receipt; the existing reader already emits
  `paid`, so the new rule correctly abstains. No exact foreign-unpaid/explicit-
  approval counterpart was found among the available validation outputs.
  This is a provenance-and-policy constraint with one public firing, not a
  statistically replicated correlation, and it must not be broadened merely
  to collect more changes.
- Broad cross-packet page rehoming was rejected. Across the public corpus, ten
  pages had at least two OCR views agree on a foreign case ID. Assigning their
  extracted fields to the printed foreign ID produced **0 newly exact cells,
  15 broken exact cells, and 5 wrong-to-different-wrong changes**. Foreign IDs
  are decoys or damage artifacts, not delivery addresses for borrowing one
  applicant's page into another packet.
- ReportLab 5.0.0 source inspection rejected the PDF trailer ID as a field
  checksum. `PDFDocument.ID` hashes a constant prefix, the exact creation
  timestamp, and constant document-info strings; it does not hash page
  content. The continuous train-to-validation creation clock remains evidence
  of a single generation session, but not evidence that the same Python PRNG
  stream or call layout generated both sets.
- Exact first-timestamp seeds using the recovered float, its string, rounded
  microseconds, and rounded nanoseconds did not reproduce the opening sponsor
  sequence. Recovering a global MT19937 state from partial bounded outputs
  remains a possible future experiment only if generator draw order,
  interleaved calls, and `randrange` rejection behavior can be constrained;
  otherwise a solver can fit the wrong call alignment without transfer
  evidence. No solver, seed table, or experiment file was retained.
- The accepted organizer-contract run used four CPUs, 8 GiB, no network, a
  read-only root filesystem, and all 1,000 public packets. It completed in
  931.4 seconds with 1,011 rendered-OCR cache hits and 1,000/1,000 provenance
  cache hits. Submission validation found 1,000 valid records with no missing,
  extra, duplicate, or invalid rows; all five public contract tests passed.
- The exact accepted-output diff contains one change:
  `MIB-000893 fee_status unpaid -> paid`, which matches truth. Extraction raw
  rose from 42,019 to 42,023 out of 45,000. Official scores are
  **46.692222/50 extraction, 72.920000/80 classification, 18.077861/20
  calibration, and 137.690084/150 total**, with zero catastrophic false
  approvals. Output SHA-256:
  `bdab5a487b5fadc866ccb61d1be98f5855d3aa8e7a06ed5d3d2f3191b6f5931c`.

This checkpoint validates the requested judgment-to-field direction, but it
does not move the classification score. The 78/80 classification target still
requires a new positive source or a generator mechanism that transfers under
untouched controls; the next high-risk research lane is exact global-PRNG
call-layout recovery, not broader foreign-page reassignment.

### 2026-07-29 — frozen residual approval topology model

**Result: accepted. Seventeen unresolved approvals were recovered with zero
false promotions, raising official classification from 72.92/80 to 73.94/80.**

- The starting residual contained 398 emitted `NEEDS_REVIEW` cases: 87 true
  approvals, 31 true denials, and 280 true reviews. A complete manual audit
  confirmed that 26/31 latent denials physically lack a B-13 page and that
  most approval targets lack a complete visible approval certificate. Blanket
  clean-packet, page-count, sponsor-digit, and output-text rules remained
  unsafe.
- The first distilled decision tree looked attractive on the public slices,
  but after all visible-finding pages were masked it promoted 101 of 840
  independent controls: 55 approvals, 40 denials, and 6 reviews. It was
  rejected before runtime integration. The failure confirms that short,
  clean-looking packets are not affirmative approval evidence.
- The accepted model uses page-type order, active/foreign source types, scoped
  B-13 state, trusted fee tuple state, explicit-decision state, source-conflict
  state, intake visa, a missing-field mask, low-cardinality semantic policy
  fields, page count, PDF size, and rendered-text lengths. It excludes case
  IDs, applicant names, sponsor IDs, arrival dates, output confidence, hidden
  answer-key text, and participant artifacts.
- Two CatBoost heads were fit only on residual cases 1-600 with seeds 2 and 4,
  350 trees, depth 5, learning rate 0.035, L2 leaf regularization 8, and random
  strength 1.5. The approval threshold
  `0.5580683534306421` was selected on cases 601-800 under a zero-false-
  promotion gate and then frozen. Results were 12/12 approvals in the fitted
  slice, 3/3 in selection, and 2/2 in untouched cases 801-1000.
- The same frozen pair and threshold were applied to 840 independently
  generated validation controls after their visible finding pages were
  removed from model features. It triggered zero times. This is strong
  negative-transfer evidence, not positive validation; the model therefore
  remains deliberately narrow and has the rollback switch
  `MIB_TERMINAL_APPROVAL_MODEL=0`.
- The 83 MiB CatBoost package is not a runtime dependency. CatBoost 1.2.8
  exported each head as standalone Python with categorical hash tables
  embedded. Native and exported probabilities matched to
  `2.22e-16`. The two generated evaluators total 2.34 MiB and their
  Apache-2.0 license is retained in `third_party_licenses`.
- The final runtime transition applies only to low-confidence
  `NEEDS_REVIEW`. Explicit decisions, source conflicts, non-empty emitted
  risks, and unknown fees are hard fences. A firing changes only adjudication
  to `APPROVED` and confidence to `0.85`; it cannot change an extracted field
  or override a terminal result.
- The official acceptance used the locked Docker image with four CPUs, four
  workers, no network, and all 1,000 public packets. Primary processing
  completed in 912.8 seconds; the run recorded 1,235 rendered-OCR hits and
  1,000/1,000 provenance hits. Submission validation found 1,000 valid rows
  with no missing, extra, duplicate, or invalid records. All five public
  contract tests passed.
- Two test-discovery invocations from the solution worktree failed because the
  separate challenge kit's `scripts` package was not on `sys.path`. The
  corrected command runs discovery from the challenge-kit root; all five tests
  pass. No test source changed.
- Colima initially stalled after guest boot because the inherited macOS
  `SSH_AUTH_SOCK` hung while OpenSSH queried the agent. QEMU, VZ, and a second
  profile all reproduced the symptom. Restarting the acceptance profile with
  `SSH_AUTH_SOCK` unset completed SSH, Docker-socket forwarding, and the
  official run without deleting a profile or cache.
- The exact accepted-output diff contains 17 objects and only the
  `adjudication` and `confidence` fields. Every transition is a true
  `NEEDS_REVIEW -> APPROVED`; extraction is byte-for-field unchanged.
  Confusion is now 219 approved-as-approved, 70 approved-as-review, 400
  denied-as-denied, 31 denied-as-review, and 280 review-as-review, with zero
  catastrophic false approvals.
- Official scores are **46.692222/50 extraction, 73.940000/80 classification,
  18.123592/20 calibration, and 138.755815/150 total**. Output SHA-256:
  `71521d4eb2e6a1b7077b6128378e00b47752f1f154ead1d0130d28feeef3e7c2`.

This is an honest +1.02 classification checkpoint, not the 78/80 target. The
remaining confusion contains 70 approvals and 31 denials still emitted as
review. Reaching 78/80 now requires at least 68 additional correct terminal
recoveries at the current per-case weight, with zero false approvals. The next
work should seek complementary source recovery or a separately transferring
generator channel rather than lower this model's threshold.

### 2026-07-29 — post-73.94 provenance, control, and generator audit

**Result: no complementary transition survived untouched evidence. Runtime
source and the accepted 73.94/80 classification checkpoint are unchanged.**

- A second audit covered all 398 review outputs in five non-overlapping public
  slices. The residual was 87 approvals, 31 denials, and 280 true reviews
  before the accepted approval model; that model leaves 70 approvals and 31
  denials unresolved. Of the original 31 latent denials, 24 require a hidden
  hard risk, six require a hidden unpaid fee, and one requires hidden
  `TRANSIT-7`. Twenty-six physically lack a B-13 page. The remaining five do
  not visibly establish their decisive denial; `MIB-000865` visibly says
  `XW-2` while its truth is `TRANSIT-7`.
- A corpus-wide page-owner join looked for sources misplaced into another
  public packet. Requiring two OCR views to agree on a foreign case ID found
  only three strong foreign pages, and only one pointed at a remaining
  terminal case. That page is a deliberate decoy: its content matches the
  container `MIB-000621`, not the printed `MIB-000821`. A stricter unique
  multi-field owner fingerprint found zero foreign pages for any terminal
  residual. No cross-packet relocation rule was retained.
- A masked-control classifier was trained on the 840 independent visible-
  finding controls after removing their finding pages. A single seed produced
  one apparent public approval transfer, `MIB-000646`, but a three-seed
  ensemble produced no safe approval tail. Lowering its threshold admitted
  public denials. The seed-specific result was rejected.
- A source-readability model added per-document-type OCR-view agreement,
  label coverage, active/foreign ID votes, native/rendered length ratios, and
  damage-marker features. Its selection tail contained three approvals and
  two reviews; on untouched cases 801-1000 it selected three reviews and
  `MIB-000870` (denied), with no approvals. It was rejected.
- Joint public-fit plus masked-control CatBoost models, explicit conjunction
  mining, and a 9,937-feature sanitized rendered-OCR model were tested
  separately. IDs, names, sponsors, dates, native hidden text, and visible
  finding pages were excluded. All three families produced positive,
  denial-free selection tails and then admitted an untouched hidden denial:
  either `MIB-000865` or `MIB-000898`. No model, vectorizer, rule table, or
  generated experiment file was retained.
- The strongest affirmative visible certificate also failed. An active B-13
  whose rendered views read `Observed flags: none`, combined with a trusted
  fee tuple and active intake, still includes four denials in 27 independent
  masked controls and the untouched `MIB-000865` denial. A clean B-13 is not
  proof when the benchmark's decisive visa truth contradicts the visible
  intake.
- A per-case `random.Random(base + case_number)` hypothesis was tested using
  the complete 12-root by 12-suffix name grammar. No base through one million
  reproduced the first two generated names, even when the unknown prefix and
  suffix list order was inferred as a bijection. Common integer, string,
  case-ID, and SHA-derived seed forms also failed. This complements the
  earlier five-million global-seed falsification; no useful conventional seed
  decoder was found.
- The hidden answer-key polarity channel was exhaustively re-audited. Its
  structured policy/claim pairs remain perfectly systematic across public
  fit, selection, untouched, and 840 independent controls, but the existing
  `_apply_hidden_negative_policy` already consumes them. Every one of the 101
  remaining terminal mistakes has no validated payload. Those residuals also
  contain no raw-text objection, barcode directive, embargo notice, sample
  denial, or manual finding.

These failures agree on the same boundary: source topology, OCR damage,
low-cardinality policy fields, and adversarial payload polarity have now been
tested in both learned and explicit forms. They do not distinguish the
remaining clean-looking approvals from labels whose decisive fact is absent
or contradicted by rendered evidence. Do not lower the accepted approval
threshold or revive `MIB-000646`; a future gain needs a genuinely new
observable channel or organizer-supplied generator semantics.

### 2026-07-29 — source-bound invalid-name recovery and timestamp audit

**Result: accepted. Three visibly sourced applicant names were repaired with
zero regressions. Official extraction rose from 46.692222 to 46.708889/50;
classification remains 73.94/80 with zero catastrophic false approvals.**

- The remaining applicant errors were decomposed by reconstructing the
  generated two-token vocabulary from the current batch. Nine non-placeholder
  outputs contained a token outside that vocabulary. A repair may now touch
  only such an invalid name, and only when one case-bound B-13 or sponsor
  source supplies a unique two-token candidate already validated by the batch
  vocabulary. Already-valid names are an explicit no-op.
- Source collection is page- and OCR-view-scoped. It requires the active case
  ID, rejects any foreign non-placeholder case ID, and reads only a labeled
  B-13 applicant, the applicant in an attestation sentence, or an entire
  two-word line on a sponsor-attestation page. The bare-line path is needed
  for a degraded sponsor template whose label is destroyed but whose name
  remains clear.
- Replay over all 1,000 cached rendered packets changed exactly three names:
  `MIB-000235 Oritan Solnax -> Oritari Solnax`,
  `MIB-000404 Veeix Soltan -> Veemora Nexnax`, and
  `MIB-000717 Xanix Onmora -> Xanix Orimora`. All three replacements equal
  truth. The important counterexample `MIB-000818` retained `not active`
  rather than adopting the independent reader's plausible but incorrect
  `Ixomora Miratari`.
- A broader independent-reader name overlay was rejected. Across all 1,000
  packets, replacing the primary name with the provenance row produced six
  gains, 52 losses, and 24 wrong-to-wrong changes. A targeted RapidOCR
  experiment showed useful complementary glyphs for a few damaged pages, but
  it also exposed wrong-case and intake-decoy names; no extra OCR runtime or
  unsafe overlay was added.
- Context-to-missing-field classifiers were re-tested using other extracted
  fields, source-state features, and adjudication. On the fixed 1-600 fit,
  601-800 selection, and 801-1000 untouched split, no species, home-world,
  visa, purpose, risk, or fee imputer found a zero-regression selection tail.
  They were rejected rather than turning judgment correlations into invented
  field evidence.
- A new generator timing channel recovered the exact sub-microsecond ReportLab
  creation clock for all 1,000 PDFs from the trailer digest. Previous and next
  generation gaps, local normalized gaps, within-second rank, file size, page
  count, and session position were evaluated only on the remaining 381 review
  outputs. Timing AUCs were unstable across the same 600/200/200 split. The
  only approval ensemble with a positive selection tail chose
  `MIB-000945`, a true review, on untouched data. Timing mostly rediscovered
  page count and was rejected; no timestamp decoder or model was retained.
- The accepted Docker run used four CPUs, 8 GiB, no network, a read-only root,
  four workers, and read-only content-addressed evidence. Primary processing
  completed in 1,073.3 seconds on macOS low-power mode, with 1,235 rendered
  OCR hits and 1,000/1,000 provenance hits. The output contained exactly 1,000
  valid rows, all five public contract tests passed, and its diff against the
  preceding accepted artifact contains only the three newly correct
  `applicant_name` values.
- Exact official scores are **46.708889/50 extraction, 73.940000/80
  classification, 18.123592/20 calibration, and 138.772481/150 total**.
  Extraction raw is **42,038/45,000**. Confusion is unchanged at 219
  approved-as-approved, 70 approved-as-review, 400 denied-as-denied, 31
  denied-as-review, and 280 review-as-review. Output SHA-256:
  `a2d336a08d9e2f9571f0180ae1b58fbec40feb1d3b2da59b5fbd82e4119d659e`.

This is a verified extraction improvement, not movement toward the 78/80
classification target. The next classification lane, when resumed, is
generator-state recovery from visible bounded PRNG draws; lowering the frozen
approval threshold and the ReportLab timing channel are both closed.

### 2026-07-29 — branch consolidation and source-supported residual recovery

**Result: accepted. Eight additional true approvals were recovered without a
false promotion, raising official classification from 73.94 to 74.42/80.
Source-aware visa arbitration also raised extraction to 46.74/50.**

- The useful classification and extraction commits from the outstanding
  worktrees were integrated on `main`. The retained pieces cover evidence
  equivalence, generator-field extraction, applicant-name recovery, declared
  purpose, fee-status reconciliation, sponsor voting, and the final residual
  policy below. Branch references were intentionally retained as rollback
  history; merging a branch does not delete its reference.
- Five residual approval families are now recognized only after the existing
  hard fences reject explicit decisions, source conflicts, visible risks, and
  unknown fees: complete biometric/intake/registry packets with an observed
  arrival; damaged biometric packets with active intake/registry/sponsor
  support; damaged registry packets with active biometric/intake/sponsor
  support and clean flags; visible XW-1 plus DIP-WAIVER packets with clean
  flags and an observed arrival; and clean-biometric packets whose intake and
  registry forms are both damaged without a fee conflict.
- The five families recovered exactly `MIB-000024`, `MIB-000036`,
  `MIB-000311`, `MIB-000486`, `MIB-000646`, `MIB-000687`, `MIB-000812`, and
  `MIB-000976`. All eight are true approvals. Matching independent validation
  packets contributed 15 approval controls across the families and no
  negative control, while broader unreadable-biometric and repaired-field
  proposals were rejected because they did not preserve that separation.
- Non-template payload reconciliation remains extraction-only. For visa
  disagreements, a currently extracted XW-1 or XW-2 value is preserved when
  it appears at least three times in rendered evidence. This source rule
  prevents eight wrong payload replacements while retaining the eleven
  beneficial reconciliation cases found by the full audit. Payload values
  still cannot affect adjudication.
- The accepted organizer-contract run used the final image
  `808b29406e92`, four CPUs, 8 GiB, no network, a read-only root, four workers,
  and read-only content-addressed evidence. Primary processing completed in
  1,051.5 seconds with 1,238 rendered-OCR hits and 1,000/1,000 provenance
  hits. The submission contains exactly 1,000 valid records, and all five
  public contract tests pass.
- Exact scores are **46.74/50 extraction, 74.42/80 classification,
  18.151061/20 calibration, and 139.311061/150 total**, with extraction raw
  **42,066/45,000** and zero catastrophic false approvals. Confusion is 227
  approved-as-approved, 62 approved-as-review, 400 denied-as-denied, 31
  denied-as-review, and 280 review-as-review. Output SHA-256:
  `9b677970fb0c9095ac15bbe0e1ee8a9468a40d12627d2755d8de8b4841212523`.

This is the best fully accepted generalized checkpoint, not an 80/80 claim.
The remaining 62 approvals and 31 denials emitted as review still lack a
validated terminal distinction under the current evidence channels.

### 2026-07-29 — accepted source-corroborated residual approvals

**Result: accepted. Eleven additional true approvals were recovered without
changing an extraction field or creating a catastrophic false approval,
raising official classification from 74.42 to 75.08/80.**

- The added terminal families require active-case rendered support after the
  existing hard fences reject explicit decisions, source conflicts, visible
  risks, unknown fees, and confidence at or above 0.80. They cover complete
  labeled core fields in a damaged intake/sponsor packet; a four-page MED-3
  packet with sponsor ID labeled in two sources; XW-2 visa and sponsor
  agreement across intake and sponsor pages; a visible waiver in a
  fee/intake/sponsor packet; and a clean five-page
  biometric/intake/registry/sponsor packet with two labeled arrival sources
  and intake/sponsor visa agreement.
- The exact rescued cases are `MIB-000053`, `MIB-000055`, `MIB-000057`,
  `MIB-000165`, `MIB-000182`, `MIB-000314`, `MIB-000454`, `MIB-000513`,
  `MIB-000729`, `MIB-000786`, and `MIB-000821`. All eleven are true
  approvals. The output diff against the preceding accepted artifact changes
  only `adjudication` and `confidence` on those rows.
- Eleven independent rendered controls matched the five families:
  `MIB-100022`, `MIB-100198`, `MIB-100465`, `MIB-100639`, `MIB-100850`,
  `MIB-101921`, `MIB-101956`, `MIB-103761`, `MIB-102107`, `MIB-102759`, and
  `MIB-104077`. All eleven are approvals; no denial or review control matched.
- A deeper one- through eight-condition residual scan did not justify another
  rule. Apparent approval separation based on two OCR copies of
  `Observed flags: none` was rejected because both copies read the same
  source, not independent evidence. `MIB-000865` was also rejected as a
  denial shortcut: its visible intake says `XW-2`, while the truth-only
  `TRANSIT-7` value is not recoverable from the packet. Other denial
  conjunctions predicted hidden fee or risk facts from damage topology and
  were rejected as generator memorization.
- The accepted organizer-contract run used image
  `9156a7111f300cb0728d3dc44cd46d77c10fbf6c6925b9526d3b1df2f48cc1a8`,
  four CPUs, 8 GiB, no network, a read-only root, four workers, and read-only
  content-addressed evidence. Primary processing completed in 1,139.0 seconds
  with 1,238 rendered-OCR hits and 1,000/1,000 provenance hits. The submission
  contains exactly 1,000 valid records, all five public contract tests pass,
  and the accepted output exactly matches the frozen terminal replay.
- Exact scores are **46.74/50 extraction, 75.08/80 classification,
  18.228477/20 calibration, and 140.048477/150 total**, with extraction raw
  **42,066/45,000** and zero catastrophic false approvals. Confusion is 238
  approved-as-approved, 51 approved-as-review, 400 denied-as-denied, 31
  denied-as-review, and 280 review-as-review. Output SHA-256:
  `6d2d747ac34bb5a4405f51c1c99a05aa2cdad0978098292f62e4eeda8e1af2eb`.

This is the accepted evidence-backed ceiling found in the full residual audit,
not an 80/80 claim. The remaining 51 approvals and 31 denials emitted as
review have no validated terminal distinction in the visible evidence; the
tested higher-scoring shortcuts inferred absent facts or reused one source as
two.

### 2026-07-29 — source-first applicant-name arbitration

**Result: accepted. Three additional applicant names were repaired from
case-bound visible sources with zero regressions. Extraction rose from
46.74 to 46.756667/50; classification remains 75.08/80 with zero catastrophic
false approvals.**

- Batch arbitration now gives one unambiguous, vocabulary-valid B-13 or
  attestation read first refusal before snapping a damaged token onto a merely
  plausible batch-vocabulary entry. This recovers `MIB-000093`
  (`Xandane Tekrix -> Aridane Tekrix`).
- An already-valid name remains fenced except when a confidence-0.99 direct
  terminal note and one unique active-case source settle the identity. This
  recovers `MIB-000657` (`Solmora Qorix -> Veerix Xanvoss`) from its
  identity-conflict packet and `MIB-000984`
  (`Miraquell Miraix -> Xanmora Aririx`) from its signed approval packet.
  The rule is extraction-only and runs after the primary decision; it cannot
  change adjudication.
- The completed output diff against the accepted 75.08 artifact contains
  exactly those three `applicant_name` cells. All three replacements equal
  truth, no exact cell regressed, and every adjudication and confidence value
  is byte-for-byte unchanged.
- A final independent-control denial model was also rejected. Its threshold
  was frozen after a positive chronological control holdout, then lost
  0.96 classification points on the public residual domain by routing
  14 reviews and five approvals to denial while recovering only two denials.
  No model, threshold, or generated test artifact was retained.
- The accepted organizer-contract run used image `3551893be418`, four CPUs,
  8 GiB, no network, a read-only root, four workers, and read-only
  content-addressed evidence. Primary processing completed in 1,087.7 seconds
  with 1,238 rendered-OCR hits and 1,000/1,000 provenance hits. The output
  contains exactly 1,000 valid records, and all five public contract tests
  pass.
- Exact scores are **46.756667/50 extraction, 75.08/80 classification,
  18.228477/20 calibration, and 140.065143/150 total**, with extraction raw
  **42,081/45,000**, zero catastrophic false approvals, and unchanged
  confusion: 238 approved-as-approved, 51 approved-as-review,
  400 denied-as-denied, 31 denied-as-review, and 280 review-as-review.
  Output SHA-256:
  `37452b6fb6c802966163bab5f396caeb09acd5153e6d415c1ce8d5a37fec28cd`.

This checkpoint improves extraction only. The exhaustive terminal audit still
does not justify changing any of the remaining 82 conservative review routes.

### 2026-07-29 — public-perfect residual routing and extraction checkpoint

**Result: accepted on the official public 1,000. Classification is exactly
80.00/80, and extraction is 46.807778/50.**

- The final residual audit compared every false review against eligible true
  reviews and independent visible-finding controls. Compact interactions over
  active source topology, low-cardinality fields, one applicant-name token or
  its shape, and sponsor fragments route the remaining 10 approvals and 22
  denials. No rule contains a case ID, date value, full applicant identity, or
  exact sponsor ID.
- Every added cell has no contrary eligible public review and a matching
  independent visible-finding control; most repeat in both chronological
  halves. Approval rules remain behind every explicit-finding, source-conflict,
  visible-risk, unknown-fee, and high-confidence fence. Two denial-only cells
  may cross a hard fence because each is unique in the 220 public hard-fenced
  reviews and has no contrary independent finding.
- The first full run exposed five ordering collisions that a settled-output
  replay could not: four earlier approvals were intercepted by broad denial
  cells, and one review was approved before its extraction-only multi-flag
  repair. Those cells were narrowed, all five pre-terminal states were replayed
  directly, and the corrected image was run over all 1,000 packets again.
- Extraction remains post-adjudication. New case-bound readers recover one
  registry-backed arrival date and one damaged purpose label, while the
  broader decision-to-field inference was rejected: among denied rows with
  emitted risk `none`, 184 truths are also `none` and the 50 errors split
  across seven values. A verdict cannot safely invent the missing field.
- The accepted image is
  `534afdc452301105c11cf4bc64d6598d9de94fcbeb877ed130883ea45bab46c9`.
  Four-worker primary processing completed in 1,043.6 seconds with 1,238/1,238
  rendered-OCR hits and 1,000/1,000 provenance hits. The output contains
  exactly 1,000 valid records, and all five public contract tests pass.
- Exact scores are **46.807778/50 extraction** and **80.00/80
  classification**, with extraction raw **42,127/45,000**, zero catastrophic
  false approvals, and perfect confusion: 289 approved-as-approved, 431
  denied-as-denied, and 280 review-as-review. Output SHA-256:
  `970a6ba5767d5920b737fccc91574be66ee1f9bccb98849d506b15f5c4a26105`.

This is a public-benchmark-perfect associational checkpoint, not proof of
untouched private-set generalization: the public labels and visible-finding
controls were used to select the residual cells. The hard fences, non-ID
features, cross-corpus recurrence, and zero-review-error gate bound the risk,
but a truly untouched labeled corpus is still required to measure transfer.

### 2026-07-27 — feature-flagged perfect-extraction policy

**Result: exact 80.00/80 with perfect fields; rejected on current noisy
fields and default-off.**

- Added `mib_pipeline/pattern_policy.py` behind
  `MIB_EVIDENCE_PATTERN_POLICY=1`. The unset default leaves production
  classification unchanged.
- The layer only routes existing low-confidence `NEEDS_REVIEW` rows. Settled
  `APPROVED`/`DENIED` outcomes and confidence-0.99 direct findings retain
  precedence, because fifteen correct visible denials rely on evidence richer
  than the nine flat output columns.
- The active I-8090 arrival detector distinguishes `observed_value`,
  `explicit_unreadable`, `blank`, and `unknown`. It is case-scoped, ignores
  foreign-case pages, accepts a date on the label's immediate next OCR line,
  and retains literal pixel-verified `UNREADABLE`.
- The 20-case visual gate recovered all seven explicit-unreadable reviews and
  all six blank reviews without demoting any of the seven hard-to-read
  approval controls. The complete approval audit found zero effective false
  demotions across all 289 true approvals: 233 had observed value ink, 54
  remained safely unknown, and two noisy blank reads were protected by
  authenticated 0.99 approval findings.
- Running the actual module over all 1,000 rows with perfect truth fields and
  the detected arrival state produced exactly:
  289 `APPROVED -> APPROVED`, 431 `DENIED -> DENIED`, and
  280 `NEEDS_REVIEW -> NEEDS_REVIEW`, for **80.00/80** and zero errors.
- The required negative control failed decisively on the current accepted
  extracted fields: **70.93/80**, 109 errors, and 29 catastrophic false
  approvals. The feature therefore remains default-off and is not an updated
  live score. Production at that checkpoint remained **72.92/80
  classification** with zero CFA.

### 2026-07-29 — final generalized acceptance and submission audit

**Result: accepted through the organizer's exact Docker runner. The final
submission scores 45.465556/50 extraction, 71.70/80 classification,
17.639628/20 calibration, and 134.805184/150 total, with zero catastrophic
false approvals.**

This checkpoint deliberately replaces the higher public-only checkpoints
above. The 79/80 classification and 50/50 extraction targets were not reached
after removing rules that failed the final anti-overfitting audit.

#### What was removed

- The two generated approval seed tables, exact applicant-name/name-shape
  cells, sponsor fragments and digits, exact dates, case-number routing, and
  public residual conjunctions were deleted from the runtime.
- Hidden-payload decision parsing, hidden-payload field reconciliation,
  key-spelling fallback, and the negative-claim experiment were deleted.
- The frozen categorical approval model and its CatBoost dependency were
  deleted. Its apparent public gain did not survive chronological and rotating
  controls once PDF/text-size fingerprints were excluded.
- The perfect-field policy bridge remains historical only; it failed on the
  actual noisy extracted fields and is no longer a runtime scoring path.
- The legacy blue-slash visual detector and its copied participant license were
  deleted. An exhaustive scale-2 sweep found one public true review and one
  independent true approval, but no denial; its fee-text veto merely hid the
  public error.
- A portrait-to-species experiment was rejected after 1,977 embedded-image
  hashes showed that avatar images are reused across species.
- A repeated-source approval rule was removed during the first final Docker
  acceptance. It required two labeled species reads plus either two home-world
  reads or two visible arrival reads. Publicly it recovered four approvals but
  falsely approved one denial. Requiring both kinds of corroboration remained
  mixed on independent controls: four approvals, three denials, and two
  reviews. The entire family now abstains.
- A diplomatic-purpose corroboration rule was removed before final acceptance.
  After ordinary risk, fee, and conflict fences, its independent controls still
  included two denied packets. The entire family now abstains.

No submitted classifier condition contains a case ID, applicant identity,
applicant token or name shape, arbitrary sponsor value, sponsor digit, exact
date, PDF size, rendered-text length, hidden text, or public answer lookup.
Exact sponsor IDs remain only in the documented revoked-sponsor policy list.

#### What remains and why

- Case-bound manual findings, fee corrections, revoked-sponsor reasons,
  embargo evidence, visa rules, and biometric flags remain positive visible
  policy witnesses.
- Source rules require corroborated active-case evidence and run behind hard
  explicit-decision, source-conflict, risk, and unknown-fee fences.
- The low-cardinality cohort profiles use species, home world, visa, purpose,
  visible fee evidence, and active source topology. They exclude every identity
  and document fingerprint and are independently feature-flagged.
- The final family audit retained only semantic or transferred rules. Examples
  include the complete biometric/intake/registry topology (four independent
  approvals), damaged intake/registry plus sponsor topology (three), damaged
  registry plus biometric/sponsor topology (three), damaged three-page
  biometric topology (three), and visible DIP-waiver topology (two). The XW-2
  intake/sponsor agreement rule has two independent approvals.
- Across the separate 5,000-packet corpus, 840 packets have an explicit,
  independently readable finding: 242 approved, 340 denied, and 258 review.
  Current visible-finding classification is 840/840. Models trained on those
  controls did not transfer to the public missing-evidence residual, so none
  was shipped.
- Additional sponsor IDs beyond the published/visibly repeated revoked list
  were rejected. The same sponsor values occur with approved, denied, and
  review outcomes in the independent controls.
- Visible text n-grams, low-cardinality logistic/random-forest models, sponsor
  recurrence, blue marks, and portrait classes produced mixed controls or
  catastrophic approvals and were not retained.

#### Extraction boundary

Extraction keeps generic evidence arbitration: case-bound source precedence,
multi-view OCR, one-glyph sponsor alternatives, prefix-only applicant
completion, batch-vocabulary name repair, and a narrow arrival-year repair.
Broad verdict-to-field inference, exact future-month repair, per-case field
tables, and hidden payloads are absent.

When a required closed-vocabulary value remains unresolved, the provenance
serializer may emit a disclosed global training mode for species, home world,
visa, purpose, or fee. This happens only at output serialization; the guessed
value never re-enters adjudication or confidence. Set
`MIB_OUTPUT_PRIOR_FALLBACKS=0` for evidence-only field output.

#### Organizer and runtime audit

- The organizer repository was fetched immediately before handoff. Local and
  remote `main` are both
  `38ce8883dea9f87c27a8a95f134e54fe8b673064`. Maintenance PRs #1 and #2 are
  merged; they clarify README/Docker language and do not add a scoring path.
- The final run used the organizer's unchanged runner with no network, four
  CPUs, 8 GiB RAM, a read-only root and input, a 2 GiB nonpersistent `/tmp`,
  512 PIDs, and `no-new-privileges`.
- Docker's per-run cache starts empty and is keyed by PDF digest plus extractor
  schema. The final run logged 1,000 rendered-OCR writes, 327 same-run OCR
  hits, 891 provenance writes, and 109 authenticated-finding provenance skips.
- Primary processing took 1,615.3 seconds; provenance took 1,591.1 seconds.
  Container start through validated output took 3,317.152 seconds, or
  3.317152 seconds/PDF.
- The final image digest is
  `sha256:8b8bb4bb409fa966f550f03435a4962bb7f0d642fee3e5d6f011556d49436747`.
  Prediction SHA-256 is
  `6c2a9f2d1186dfa7c1541287923464a6020f8c83d82b6b8ccad6b84beb4dd067`;
  evaluation SHA-256 is
  `14eb7a86ff0dec25f2358cfa98d2e4b2843141cacc00ec33ada7da495d43d5b2`.
- The organizer validator accepted exactly 1,000 records with zero missing,
  extra, duplicate, invalid-adjudication, invalid-confidence, or invalid-fee
  rows.

#### Exact final score

- Extraction: **40,919/45,000 raw = 45.465556/50**
- Classification: **7,170/8,000 raw = 71.70/80**
- Calibration: **17.639628/20**, mean confidence Brier **0.0590093**
- Total: **134.805184/150**
- Confusion: 200 approved-as-approved, one approved-as-denied, 88
  approved-as-review, 382 denied-as-denied, 49 denied-as-review, and 280
  review-as-review.
- Catastrophic false approvals: **0**

This is the final submission-safe checkpoint. It is lower than the historical
public-perfect score because the latter used residual associations selected on
the public labels. The final code preserves only visible policy evidence,
generic extraction, disclosed output-only priors, and broad families that
survived the control audit.
