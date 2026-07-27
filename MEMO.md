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

### One-way denial projection

**Result: strongest next lead; projection only, not yet promoted.**

The documented transit, revoked-sponsor, stale-arrival, and embargo-world
conditions were projected as denial witnesses for unresolved non-diplomatic
outputs, while preserving authenticated direct findings at confidence 0.99.
Adding recurring embargo world `TRAPPIST-1e` produced **66.12/80
classification**, **15.36/20 calibration**, **127.00/150 total**, and the same
14 CFA. A separate visible unpaid-fee projection changed one additional true
denial and reached **66.18/80** and **127.07/150**. These are label-scored
static projections, not runtime acceptance results; the next step is an exact
trigger panel followed by a full run before either rule can be committed.

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
