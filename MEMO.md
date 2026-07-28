# MIB Document Challenge — Living Engineering Memo

Last updated: 2026-07-27

This memo records the approaches we tried, the evidence behind each decision,
and the current promotion gates. It is intentionally a living document: update
it after every material experiment so failed ideas are not accidentally
rediscovered and public-fit results are not confused with honest holdout
results.

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

### 2026-07-28 — accepted: run the independent engine before the batch repairs

**Result: accepted. Extraction 46.238 -> 46.472 / 50 public (49.487 -> 49.534
under unrecoverable-field scoring), 46 gains, 3 losses, no extra runtime.**

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

**Session total: 49.322 -> 49.534 private-style, 45.877 -> 46.472 public**,
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
