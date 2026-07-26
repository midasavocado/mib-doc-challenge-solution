# MIB Document Challenge — Living Engineering Memo

Last updated: 2026-07-26

This memo records the approaches we tried, the evidence behind each decision,
and the current promotion gates. It is intentionally a living document: update
it after every material experiment so failed ideas are not accidentally
rediscovered and public-fit results are not confused with honest holdout
results.

## Current verified checkpoints

### Public full-1,000 execution

The latest valid full run is:

`work/fresh-independent/full-1000-deskew-20260726`

| Section | Score |
|---|---:|
| Extraction | 44.37 / 50 |
| Classification | 78.76 / 80 |
| Calibration | 14.96 / 20 |
| Total | 138.09 / 150 |
| Catastrophic false approvals | 0 |

This public classification result uses a model fitted on all 1,000 public
labels. It is useful as a public checkpoint, but it is **not** accepted as an
estimate of private-set generalization.

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
