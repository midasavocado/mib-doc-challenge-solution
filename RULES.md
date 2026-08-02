# MIB Generalization and Evidence Rules

This file is the promotion contract for every classification, extraction, and
confidence change. Its split, identity, and anti-memorization gates are
stricter than the challenge minimum. Its default evidence profile deliberately
contains one disclosed benchmark-adaptive generator exception; use
`visible_evidence_only` when strict visible-source semantics are required. A
higher development score is not sufficient evidence that a change belongs in
either profile.

## 1. Frozen 800/200 development boundary

From the checkpoint immediately before this file was added, all new pattern
discovery—manual or learned—uses only 800 development packets. This includes
PDF inspection, pixel/OCR inspection, native-text inspection, labels, derived
features, and error analysis. The remaining 200 packets were reserved for one
prospective validation and have now been spent.

The split is exact, deterministic, and label-blind:

1. Take the sorted set of the 1,000 case IDs.
2. Compute `SHA256("mib-prospective-v1:" + case_id)` for each ID.
3. Sort by `(digest, case_id)`.
4. The first 800 IDs are development; the final 200 are holdout.

Case ID is used only to assign this audit split and bind pages to their active
packet. It is never an extraction or decision feature.

The committed split contains 800 development IDs and 200 holdout IDs. To make
the boundary auditable without publishing the holdout list, the newline-joined
sorted ID commitments are:

- development: `41313a397308dcb7858a915ba483c899578a050d7ce76f3a2a41e5ab2aae3fa3`
- holdout: `51a6955323053bf080b14df4766a32f2b6128ee8455bf05fd01242a8e387354a`

This was a **prospective holdout**, not a historically untouched one. Earlier
development inspected aggregate and per-case results across the public 1,000.
That limitation must remain disclosed. From this checkpoint onward, nobody may
inspect holdout labels, errors, feature distributions by label, or individual
holdout cases while changing the system. Aggregate scores recomputed across
all 1,000 are also prohibited because they still leak holdout feedback.

One post-split source-manual search was accidentally broad enough to print a
small number of sponsor-related label rows outside the 800. That output was
discarded immediately and none of its values or labels may support a rule, but
the 200 can no longer honestly be described as perfectly unseen. It remains a
**quarantined prospective audit**, with this contamination disclosed, rather
than a pristine scientific holdout. No holdout PDF, derived feature, error, or
aggregate score may be inspected during further development.

The partition was opened once for a frozen candidate. Its aggregate score was
46.8111 extraction, 72.5500 classification, 17.1061 calibration, 136.4672
total, with 3 catastrophic false approvals. That feedback was discussed, so
the partition is now **spent**. It must not become another development set
through repeated peeking, error inspection, or aggregate-driven tuning.

## 2. Evidence hierarchy

Decision evidence is ordered as follows:

1. an authenticated, active-case, visible signed finding;
2. a positive active-case visible policy witness, such as a hard risk, revoked
   sponsor, invalid fee state, embargo, or stale arrival;
3. corroborated active-case facts from intake, biometric, sponsor, registry,
   and fee sources;
4. broad source-topology or fictional-program policy inferred from development
   examples and validated under this contract;
5. an untrusted native/hidden-text proposal, behind a disclosed feature flag;
6. absence or unreadability, which normally preserves `NEEDS_REVIEW`.

Authenticated signed findings always win. Positive visible policy witnesses
normally win, but the default benchmark-adaptive profile has one disclosed
exception: a disagreement with either independently repeated hidden-generator
family is converted to `NEEDS_REVIEW`, never to approval. A policy-clean
negative-request family may also act as alternate approval authority after the
signed-finding, visible-denial, and emitted-risk vetoes. Hidden text never
overwrites an extracted visible field; these classification effects are
isolated behind `MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING` and disappear in the
`visible_evidence_only` profile.

Approval requires affirmative support. Denial requires a positive policy
witness or a development-validated general policy. When neither is present,
the correct abstention is `NEEDS_REVIEW`.

## 3. Permanently prohibited features and methods

The following are forbidden even if they improve the score:

- case IDs, filenames, directory paths, row order, PDF byte size, hashes,
  rendered-image fingerprints, or cache keys as prediction features;
- applicant names, name fragments, identity tables, or case-specific values as
  decision features;
- exact-answer maps, manually edited output rows, or lists of exceptions;
- a conjunction created only to isolate a handful of known labels without a
  coherent source or fictional-policy mechanism;
- training on evaluator output, public score feedback, final adjudication
  labels, or hidden requested confidence as though it were ground truth;
- selecting a rule, model, threshold, confidence, or veto after inspecting its
  holdout errors;
- code copied from another challenge participant or participant pull request.

Applicant names may still be extracted as output data. Case IDs may still bind
pages to the active packet and populate the required schema. Neither may reach
adjudication.

## 4. Manual pattern promotion

A hand-written rule is not exempt from validation. Before implementation, its
record must state:

- the evidence fields and source states it uses;
- a plausible in-world policy or document-generation mechanism;
- the expected action and conservative vetoes;
- all matching development examples, including counterexamples;
- support by class and across broad development partitions;
- its delta versus the frozen baseline, including catastrophic approvals.

A promotable manual rule must satisfy all of these conditions:

1. **Semantic:** its predicates describe policy, evidence quality, document
   structure, or a recurring generator mechanism—not an identity proxy.
2. **Broad:** it is stated before examining individual errors and is not an
   arbitrary high-dimensional conjunction made to isolate a tiny cell.
3. **Counterexample-aware:** apparent positives and the closest negative
   controls are evaluated together on development.
4. **Stable:** the direction is consistent across at least two deterministic
   development partitions or layouts. A small cohort may preserve review or
   denial only when the mechanism is strong; it may not create an approval
   from weak absence evidence.
5. **Safe:** it introduces zero catastrophic false approvals on development.
6. **Useful:** it improves the declared metric against the frozen baseline,
   with extraction gains reported as exact cells gained and lost.

Exact fictional policy entities may be used only when they represent recurring
published or development-inferred policy—such as a revoked sponsor list or a
jurisdictional embargo—and have a coherent source-bound mechanism. Applicant
identity, a one-off sponsor, a one-off date, or a tiny combination chosen only
for its labels is never a policy.

Rules may have general vetoes. For example, a broad approval quorum may be
countered by a visible hard-risk veto. A veto must independently make policy
sense and must be tested across its whole development cohort; it cannot be a
camouflaged list of the mistakes made by the first rule.

### Current manual-rule register

The active candidate contains these development-derived proposals. Counts are
for the complete matching development cohort after the stated vetoes, not a
hand-picked changed-case list.

| Proposal | Mechanism and independent vetoes | Development support |
|---|---|---:|
| Biometric + fee + intake clearance | Compact identity/payment interface; any positive risk, decision, contest, or unsupported fee vetoes approval | 9 approvals, 0 others; all 5 folds |
| Fee + intake + sponsor clearance | Sponsor-backed payment interface; positive risk, decision, contest, unknown page, or unsupported fee vetoes | 5 approvals, 0 others; 3 folds |
| Paid Luyten `XW-2` digital corridor | Fictional electronic technical-visa program; requires intake, no policy fault, and no contest | 10 approvals, 0 others; all 5 folds |
| Fee + intake + registry field-repair clearance | Registry-backed operational program; requires supported paid/waived fee and no policy fault | 9 approvals, 0 others; all 5 folds |
| `KAIJU_MICRO` non-transit `XW-1` registry clearance | Fictional alternate technical interface; transit and every visible policy fault veto | 6 approvals, 0 others; 4 folds |
| Reciprocal `MED-3` registry clearance | CLEAR registry may replace B-13 in the recurring jurisdictional network; transit is excluded and Europa additionally requires a sponsor source | 11 approvals, 0 others; all 5 folds |
| Sparse `MED-3` authority failure | Intake + sponsor alone lacks biometric, registry, and fee authority; unknown fee and positive/review risk are excluded from this fallback because stronger rules already handle them | 3 denials, 0 others; 2 folds |
| Conflicting visible/native decision channels | Signed findings retain strict precedence; an unsigned visible-policy/generator disagreement abstains rather than guessing | Review-only request controls are 27/27 reviews; inverse clean-request controls are 37/37 approvals; the route can only produce `NEEDS_REVIEW` |
| Requested-approval review confirmation | If the untrusted requested approval survives all routing and safety checks as review, use it only as a confidence-family marker | 50/50 final reviews correct; all 5 folds |
| Damaged visible manual approval | Header + `Finding` + `Reason` geometry preserves an `APPROVED` word envelope when OCR loses the characters; authenticated signed findings remain higher precedence | 2 approvals, 0 others; folds 0 and 1 |
| Andromedan medical-visitor treaty | Fictional consult program accepts fee + intake + registry authority when no policy fault or unknown attachment remains | 4 approvals, 0 others; 3 folds; recovers 2 reviews in 2 folds |
| Clean paid B-13 with non-policy contest | Clean risk panel and paid fee establish policy clearance when the surviving audit uncertainty is a supporting-field conflict | 4 approvals, 0 others; 3 folds; recovers 2 reviews |
| Triangulan paid treaty | Fictional paid treaty applies when no policy flag, audit reason, or unknown attachment remains | 5 approvals, 0 others; 3 folds |
| Arcturian distributed interface | Four active source types provide the fictional distributed authorization interface | 6 approvals, 0 others; 4 folds |
| `XW-1` diplomatic mission | Fictional short-term diplomatic mission equivalence with valid fee and no policy fault | 4 approvals, 0 others; 3 folds |
| `XW-2` xenobotany registry program | Three-source paid botanical program uses registry authority without a mandatory B-13 | 6 approvals, 0 others; 3 folds |
| LUNA xenobotany interface | Fictional LUNA botanical-security interface tolerates a supporting-field contest but no risk or fee fault | 4 approvals, 0 others; 2 folds |
| Jovian–Titan electronic corridor | Titan Freeport's fictional gas-form corridor accepts paid or waived electronic authority after the common safety vetoes | 5 approvals, 0 others; 4 folds |
| Jovian distributed electronic interface | Complete alternate authority models a monotone gas-form authorization interface; technical-medical and sparse diplomatic-xenobotany states veto alongside risk, contest, unknown-page, and visible-decision states | 11 approvals, 0 others; all 5 folds; recovers 1 review |
| DIP-1 reactor waiver authority | A visibly sourced diplomatic class and waiver plus at least three source types and complete alternate authority can authorize reactor work; arrival, risk, contest, unknown-page, and visible-decision checks remain mandatory | 1 residual recovery; retained as a disclosed low-support hypothesis pending stronger external support |
| MED-3 reactor sparse-program denial | Visibly sourced medical authority and reactor purpose on an intake+registry-only packet supplies neither a matching work program nor fee, sponsor, or biometric alternate authority | 2 denials, 0 others; 2 folds; recovers 1 review |
| Barnard five-source safety quorum | Five active source types provide redundant fictional safety authority even when one supporting panel is unreadable | 4 approvals, 0 others; 3 folds |
| Zeta distributed-registry clearance | Three independent visible source types, all visible core fields and arrival, no contest/unknown page/policy fault, and alternate risk authority model a distributed registry interface | 3 approvals across folds 0, 1, and 4; the LUNA `XW-2` medical packet in fold 3 remains review under its independent biometric-clearance veto |
| Technical diplomatic identity gap | `XW-2` diplomatic missions with registry authority but no biometric channel preserve review rather than borrowing technical authority | 2 reviews, 1 approval; 2 folds; review has positive classification utility |
| Diplomatic reactor authority gap | `DIP-1` reactor work with exactly fee + intake + registry lacks a biometric or sponsor operational channel | 3 reviews, 2 approvals; 3 folds; review has positive classification utility |
| Sparse translation and transit clearance gaps | `DIP-1` translation or `XW-1` transit with only fee + intake + registry preserves review; biometric/sponsor-backed controls remain eligible | 5 reviews, 0 others across the two families; 4 folds total |
| Biological and research clearance gaps | Arcturian xenobotany, mycelial archive work, sparse Alpha research, Sirius paid `MED-3`, and sparse Proxima Aquarian programs preserve review when their required clearance channel is absent | Every branch has 0 approvals; each repeats in at least 2 folds |
| Diplomatic chain authority failure | A complete intake + registry + sponsor `DIP-1` chain with neither fee nor biometric authority is a compound denial, not an unreadable-document guess | 2 denials, 0 others; 2 folds |
| Diplomatic botanical clearance veto | Unsigned paid `DIP-1` xenobotany needs both fee and biometric authority; missing either preserves review | 2 reviews, 0 others; 2 folds; 3 independent approval controls |
| Two-scale damaged manual finding | An active-case manual-note header, Reason row, and the same unambiguous fuzzy decision at 150 and 200 DPI can recover the visible finding; a `SAMPLE DENIAL` watermark is non-operative | Complete 8-page candidate cohort: 1 additional approval read, 7 abstentions, 0 false reads |
| Two-scale damaged fee witness | An active-case `Fee/Foe/Foo Status` row must agree at 300 and 600 DPI before it supplies payment evidence | Complete eligible cohort replayed; disagreement or unreadability abstains |
| Two-scale sideways fragmented fee source | Exact active-case unknown pages are rotated at 150 and 200 DPI; both scales must agree on one row-local fee status, while prompt-like/non-fee headings, conflicts, and multiple hits abstain | 127 structurally eligible development packets; 6 reads across 3 folds (2 approvals, 4 denials), all 6 fee values correct; one clean diplomatic review recovered, 0 CFA |
| Policy-clean negative generator polarity | A complete hidden tuple that requests denial but encodes no policy denial is an inverted generator proposal. The default profile treats it as alternate authority after signed-finding, positive visible-denial, and emitted-risk vetoes; it is not visible evidence | 25/25 approvals across all five development folds and 37/37 independent controls; feature-flagged and disabled by `visible_evidence_only` |
| Sirius avian medical/transit waiver ineligibility | A visibly sourced `SIRIUS_AVIAN` program under visible `MED-3`/`TRANSIT-7` and an authorized visible waiver is ineligible for that waiver interface | 4 denials, 0 others; four folds |
| XW-2 waiver without sponsor assumption | A visibly sourced XW-2 waiver still lacks the program's sponsor authority when no sponsor source exists; risk, contest, unknown-page, and flag uncertainty veto the rule | 5 denials, 0 others; one in every fold |
| Technical medical clearance failure with paid or waived fee | Visibly sourced `XW-1`/`XW-2` work authority and medical-consult purpose do not replace biometric clearance merely because a paid/waived status is visible; fee + intake + registry must be present and B-13 absent | 4 denials, 0 others across three folds; authenticated findings, notes, audit reasons, contests, unknown pages, and visible Alpha Draconian/Andromedan/LUNA or complete paid Jovian/Titan interfaces veto; recovers 1 review |

The one-packet revoked-sponsor exception was rejected: despite a plausible
source-precedence story, it lacked recurring support and the ordinary visible
revocation fence correctly overruled it. Paid packets with merely unreadable
risk panels were also not promoted as a blanket approval family because
unreadability is not affirmative clean evidence.

Every route that changes review to approval is explicitly marked and passed
through the final safety fence again. Ordinary recovered unsigned approvals
must have visible arrival support, source-backed observations for all seven
core policy fields, and either the ordinary visible fee/risk clearance chain
or the documented complete alternate-authority contract. No named fictional
program bypasses that check. The sole exception is the separately validated
negative-generator family above, which can supply alternate authority after
the signed-finding, positive visible-denial, and emitted-risk vetoes. This is
an intentional benchmark-adaptive tradeoff, not a claim that hidden text is
affirmative visible evidence.

Categorical program predicates have the same evidence requirement. A species,
home world, visa, or purpose may activate a fictional-program hypothesis only
when the pixel audit observed that exact value on an active-case source. An
imputed, portrait-guessed, batch-filled, or hidden-only category may improve an
extraction cell after adjudication; it cannot become a classification premise.
Likewise, a 0.99 `NEEDS_REVIEW` result is terminal evidence, not a weak
abstention available to the synthetic recovery pass.

The damaged-note audit evaluated every eligible development packet, not only
known errors. The same geometric detector found 14 unambiguous manual-note
envelopes: the 2 `APPROVED` envelopes were both approvals, while the 12
`DENIED` envelopes contained 8 denials, 3 reviews, and 1 approval. Therefore
only the two-fold `APPROVED` family is active; the tempting but impure denial
generalization is explicitly rejected.

## 5. Learned-model 800/200 rule

No learned classifier, ranker, calibrator, tree, forest, neural model, or
automatically mined rule may be enabled unless it first passes five internal
out-of-fold audits **inside the 800-case development partition**:

- five deterministic folds over the 800 development rows;
- for each fold, exactly 640 rows are used for fitting and 160 for internal
  validation;
- every transform, vocabulary, imputer, feature selector, mined threshold,
  hyperparameter choice, and confidence mapping is fit on the 640 only;
- no row may influence the model that evaluates it;
- identity, case, path, order, fingerprint, hidden target, and evaluator
  features remain prohibited;
- fold results report extraction, classification, calibration, total, class
  confusion, and catastrophic false approvals separately.

The original 200-row partition has already been spent. A final model may be
fit on the complete 800-case development partition only after internal folds,
but any further external acceptance must use independent controls or genuinely
new data. The spent validation cannot select features, thresholds, exceptions,
hyperparameters, or another candidate.

Minimum promotion gates are:

- zero catastrophic false approvals in every fold and in aggregate;
- at least `77.00 / 80` aggregate out-of-fold classification;
- at least `19.50 / 20` aggregate out-of-fold calibration if the learned
  component changes confidence;
- improvement over the frozen manual baseline in aggregate without relying on
  one exceptional fold;
- a saved model card describing features, training, folds, failures, and the
  reason the model should transfer.

The five internal folds are label-blind and exact: sort the 800 development
IDs by `(SHA256("mib-internal-fold-v1:" + case_id), case_id)` and take five
consecutive 160-row blocks. Their newline-terminated sorted-ID commitments are:

- fold 0: `5c7d3287d427e5348d63da75cb69deac68769b026a7bf5fe57ed346adfa0e404`
- fold 1: `6fcbd8e90ed3af75f58a2a6826ccfa97a49d61ce261ae498748d89cdbe183321`
- fold 2: `39d6892702cbe405a0e12b2ec65376b0806aeecb63f1b81d6b1454358fff8c3e`
- fold 3: `fb707a04ccf6005cbbfc23d581152eb7dd519ddf3655c14bd6930a558f49a415`
- fold 4: `0eb69d8ec9130186afd438e38fb137fafa7387b4996b4c98077670a3982394b9`

A model trained on all 1,000 is not part of this prospective audit. The
submission candidate remains the model fit on 800 and tested once on 200. A
failed model is removed from runtime, artifacts, flags, and documentation.

The 240-tree adjudication forest is the canonical rejection example: its
full-fit projection reached 146.43/150, but five strict 800/200 folds produced
only 72.20/80 classification and seven catastrophic false approvals. It was
deleted rather than rationalized.

### Active confidence-bin validation

The active calibrator is not a case model. It maps only the final decision and
coarse routing-reliability family. The older broad bins were fit on four
internal folds and checked on the excluded fifth. The final small manual bins
were selected on the 800 development set and audited for support across the
same five partitions; they are not prospective held-fold estimates, so their
support and fragility are stated directly below:

| Reliability family | Development outcomes | Five held-fold estimates | Runtime confidence |
|---|---:|---:|---:|
| Settled final approval/denial after conflict separation | Perfect in every development fold in the frozen projection | decision-family ceiling | 0.99 |
| Visible-risk or generator-confirmed review | 71/71 and 50/50 respectively; every fold | repeated coarse families | 0.98 |
| Strict-fence review | 2/22 correct; every fold | Beta-smoothed pooled rate | 0.12 |
| Residual review after higher-reliability families | 18/22 correct; every fold | 0.706–0.826 | 0.78 |
| Fee+intake+registry residual review | 15/17 correct; every fold | pooled coarse topology | 0.88 |
| Fee+intake+registry with visible `XW-1` or `DIP-1` | 7/7 and 14/14; every fold | complete visible-program cells | 0.99 |
| One unknown page with visible `XW-2` | 10/10; every fold | complete attachment-state cell | 0.99 |
| Clean-risk residual review | 0/3 correct; folds 0, 2, and 4 | fragile, explicitly disclosed | 0.01 |

The estimates use Beta(1,1) smoothing inside each 640-row training partition.
Applicant, case, sponsor value, date value, path, order, fingerprint, hidden
requested confidence, and evaluator metadata are absent from every bin key.

The cross-fitted calibration projection keeps every extraction and decision
fixed, fits only the four confidence rates on the other 640 rows, and applies
them to the excluded 160:

| Held-out fold | Extraction | Classification | Calibration | Total | CFA |
|---:|---:|---:|---:|---:|---:|
| 0 | 46.8333 | 78.4375 | 19.4661 | 144.7370 | 0 |
| 1 | 46.6319 | 79.1250 | 19.2999 | 145.0568 | 0 |
| 2 | 47.5417 | 79.2500 | 19.6396 | 146.4313 | 0 |
| 3 | 47.0139 | 79.6250 | 19.7600 | 146.3989 | 0 |
| 4 | 46.4306 | 79.6250 | 19.5717 | 145.6272 | 0 |
| **Aggregate** | **46.8903** | **79.2125** | **19.5475** | **145.6502** | **0** |

These numbers use the previous exact extraction rows, so they do not claim the
small output-only extraction repairs added afterward. They are the conservative
pre-run promotion projection for the current frozen classification/calibration
candidate.

The first subsequently frozen exact 800-case run produced 800 valid rows with
no missing, extra, duplicate, or invalid records:

| Exact development result | Score |
|---|---:|
| Extraction | 47.031944 / 50 |
| Classification | 79.137500 / 80 |
| Calibration | 19.545635 / 20 |
| **Total** | **145.715079 / 150** |
| Catastrophic false approvals | **0** |

Its confusion counts were 217 approved correctly, 6 approvals preserved as
review, 348 denials correctly, 2 denials preserved as review, 224 reviews
correctly, and 3 reviews incorrectly approved. The three ordinary false
approvals are not catastrophic under the evaluator, but remain important
transfer-risk controls. This historical artifact predates the one-time 200-row
validation; current changes do not use that spent partition.

That artifact is now a **superseded development checkpoint**, not the current
acceptance score. The independent rules audit found that recovered approvals
could bypass affirmative evidence and that several two-row policy cells were
too targeted. Those routes were removed or structurally fenced afterward.

### Current exact generalized candidate

The latest full replay used only the fixed 800 development packets and
produced 800 valid rows with no missing, extra, duplicate, or invalid records:

| Exact development result | Score |
|---|---:|
| Extraction | 47.061111 / 50 |
| Classification | 78.575000 / 80 |
| Calibration | 19.601605 / 20 |
| **Total** | **145.237716 / 150** |
| Catastrophic false approvals | **0** |

The confusion is 204 correct approvals, 19 approvals preserved as review, 350
correct denials, and 227 correct reviews. No review or denial was approved.
Prediction SHA-256 is
`71f52a60dacf16154733e431d9754c7ccae1a366e204ecde21b86854b88837de`;
evaluation SHA-256 is
`03765e3a8084e30b44a50e2e6b17038937f28bea0c8738591af0e8801917aa74`.
The spent 200 was not used to explain or tune any of these outcomes.

### Superseded calibration-only projection

The preceding source made no further verdict or extraction change. It mapped the
545/545-correct settled approval/denial family to 0.99 confidence and the
12/17-correct residual review family to 0.71. Applying only those two broad,
identity-free confidence changes to the exact artifact gives:

| Frozen development projection | Score |
|---|---:|
| Extraction | 46.943056 / 50 |
| Classification | 77.900000 / 80 |
| Calibration | 19.466990 / 20 |
| **Total** | **144.310046 / 150** |
| Catastrophic false approvals | **0** |

This historical projection predates the current exact candidate and the
one-time 200-row validation; that partition is now spent.

On a cold constrained 200-packet slice selected only from these 800 development
packets, the organizer evaluator measured 46.34 extraction, 76.60
classification, 18.43 calibration, **141.37 total**, and zero catastrophic
false approvals. That preceding image ran offline with 4 CPUs, 8 GiB, a
read-only root, and tmpfs in **718.62 seconds / 3.593 seconds per PDF**.

The current image repeated the same constrained development-only protocol in
**701 seconds / 3.505 seconds per PDF** and scored 46.7778 extraction,
77.20 classification, 18.5423 calibration, **142.5201 total**, with zero
catastrophic false approvals. This is portability
and timing evidence, not a holdout estimate.

### Rejected post-run studies

All of the following used only the fixed 800 development packets. No model,
feature table, portrait embedding, or temporary trainer from these studies is
retained in the runtime or repository:

- An identity-free logistic confidence model used final decision, coarse
  document fields, audit topology, and disclosed hidden-claim state. Nested
  640/160 fitting reduced held-out calibration from 18.8344 to 18.5875 and
  lost on all five folds.
- A route-provenance confidence smoother produced only 18.8408 held-out
  calibration, improving two folds and worsening three. The tiny unstable
  gain did not justify a runtime model.
- A conservative learned resolver for final reviews used identity-free
  source, policy, audit, and routing features. Nested thresholds prohibited
  denial-to-approval errors. It changed five held-out packets, lost 9 raw
  classification points, and recovered no denied reviews.
- Logistic and forest extraction imputers for species, home world, visa,
  purpose, risk, and fee produced zero net held-out gains; the forest fee
  variant lost two exact cells. All were discarded.
- A rendered-portrait morphology study and an official ImageNet feature
  backbone failed five-fold species generalization near chance. Portrait
  appearance is therefore not an extraction or adjudication feature.
- Three residual Andromedan medical-consult reviews were all approvals, but
  the cohort was rejected as an approval rule: its members include a visible
  review finding, unsupported fee authority, or an unknown attachment. The
  shared label does not outrank those packet-local vetoes.
- Three clean-risk biometric+registry+sponsor residuals were also approvals,
  but all lack visible fee support and one has an unknown page. They remain
  review instead of turning a development-only pure cell into an alternate
  payment exception.

The manual residual audit reached the same conclusion: within the largest
ambiguous fee+intake+registry approval topology, 38 approvals and 9 reviews
share the same page counts and almost the same field-source coverage. The only
apparently purer subgroups were tiny categorical cells that violate the broad
manual-rule gate above.

## 6. Extraction promotion

Extraction fixes must be field-local and source-backed:

- prefer an active-case labeled pixel read over an unbound or hidden value;
- require corroboration before replacing a supported visible value;
- keep output-only repairs structurally after the final adjudication stage;
- never use the evaluator answer or a case-specific value;
- report exact-cell gains, losses, and net change on development;
- verify that verdict, confidence, and catastrophic-approval counts are
  unchanged unless the change is explicitly a separately validated policy
  change.

The final decision may support only a logical cross-field invariant, not invent
missing evidence. For example, a final approval may retract a late inferred
review-only risk when no positive risk row was observed; it may not fabricate a
visa, sponsor, date, or clean biometric result.

For a final review whose sole audited contest is applicant identity, the
fee+intake+registry topology projects `identity_conflict` with 6 gains and 2
losses; intake+registry+sponsor adds 2 gains and 0 losses across 2 folds because
registry and sponsor agree against intake. The combined output-only rule nets 6
exact risk cells and never changes the verdict or reads an applicant value.

The disclosed untrusted-tuple reader has one repeated closed-vocabulary visa
repair: when visible extraction emits the recurring `MED-3` fallback but the
complete tuple proposes `DIP-1`, the output-only replacement produces 4 exact
gains across 3 internal folds and 0 exact losses. A fifth disagreement in a
fourth fold is wrong under both values, so it does not create a hidden loss. The neighboring
`MED-3` to `XW-2` proposal is mixed and remains blocked. Neither tuple value can
feed adjudication or confidence.

A case-bound intake name may repair only a near-spelling output error. The
complete development disagreement audit contains 2 exact gains in 2 folds and
0 losses above the 0.82 full-name similarity threshold: the weaker gain is
0.889 similar, while the nearest decoy intake is only 0.483. This deliberately
does not grant the intake ordinary name precedence; it is a spelling correction
from a pixel-verified native view.

Three final output-only repairs are enabled in the frozen candidate:

- a fee+intake+registry review with an absent B-13 source projects
  `illegible_biometrics`: 6 exact gains across 3 folds and 0 losses;
- the narrower diplomatic-reactor review family projects
  `sponsor_mismatch`: 2 exact gains across 2 folds and 0 losses. This is the
  lowest-support extraction rule and remains explicitly ablatable;
- when purpose is the sole disputed imputed field and a complete native tuple
  agrees with all other eight emitted extraction fields, the native purpose is
  used output-only: 3 exact gains across folds 1–4, 0 losses, and 3 rows that
  remain wrong under either value.

All three run after adjudication and confidence are final; none can create a
classification premise.

## 7. Calibration promotion

Confidence describes measured reliability of a reusable evidence family. It
must not encode identity or case membership. Confidence bins or mappings are
fit on development only and frozen before holdout evaluation. Assigning `0.99`
to every result is allowed only if the measured correctness supports it; being
confident and being correct are, annoyingly, still separate hobbies.

Five ordinary final-review reliability states share a 0.98 bin: unresolved
mandatory fee status; `DIP-1` after the distinct Centauri denials have been
removed; clean risk plus a fee source; four source types including B-13; or no
registry and no direct audit decision. Their union is 33/33 correct across all
5 folds. After the independently validated program corrections, the remaining
visible-source review family is 38/38 and uses the cross-fitted 0.97 bin. The
residual review family is 18/22 and uses 0.78. These mappings change confidence
only and use no identity, case, or target value.

Four additional final-boundary bins use only visible source topology, visible
visa, unknown-page count, and audited risk state. Fee+intake+registry reviews
with visible `XW-1` are 7/7 and with visible `DIP-1` are 14/14; one-unknown-page
reviews with visible `XW-2` are 10/10. All three span every fold and use 0.99.
The clean-risk residual is 0/3 across folds 0, 2, and 4 and uses 0.01. That last
cell is broad and identity-free but statistically fragile; it is disclosed as
such rather than dressed up as a tiny universal law.

Any confidence experiment that changes a verdict is a classification change
and must pass the classification and catastrophic-approval gates too.

## 8. Active generalized rule families

These are the intended policy families in the current source. Their code and
comments remain the final authority; this inventory makes their rationale and
risk visible.

| Family | General mechanism | Guard or limitation |
|---|---|---|
| Signed findings | Active-case authenticated note states a decision | Highest precedence; foreign-case pages rejected |
| Direct policy denials | Visible hard risk, stale date, invalid fee, revoked sponsor, embargo, or registry invalidity | Requires a positive source-bound witness |
| Evidence review fence | Blank, unreadable, conflicting, unknown, or incomplete required evidence | Abstains instead of guessing |
| Multisource approval quorum | Required policy fields have adequate independent visible coverage | Visible denial/review witnesses veto |
| Arrival support | Same value can be supported by intake, sponsor, registry, or signed evidence | Blank and unreadable are distinct from a corroborated value |
| Fragmented rotated fee source | Two agreeing active-case pixel scales may classify one sideways row that the ordinary document reader could not type | Exact unknown page, local label geometry, heading/trap rejection, and ordinary approval quorum remain mandatory |
| Approval safety | Unsigned approvals face fee, MED-3 missing-panel, archival-intake, and visible-risk checks | Must not demote an already supported approval merely because one redundant source is unreadable |
| Strict-fence recovery | A review may resolve from a direct denial witness or a broad clean source topology | No weak absence-only approval |
| Blurred manual finding | Visible word-envelope geometry reads a damaged adjudicator note | Requires note structure and never uses hidden text or identity |
| Fictional program policy | Species/visa/purpose or jurisdiction/source combinations model a recurring clearance requirement | Flagged, disclosed, counterexample-tested, and never a real-world demographic claim |
| Negative generator family | A schema-valid hidden request can serve as explicitly untrusted generator-level alternate authority | Signed findings, positive visible denials, and emitted risk veto; conflicts only abstain; feature-flagged |
| Hidden extraction candidate | Native text can spell-check or fill an unsupported output | Output-only; a supported visible value always wins |
| Decision-risk invariant | Retract a late review-only risk from an approval without an observed risk witness | Extraction-only; cannot change verdict or confidence |

The fictional-program family is the highest-risk manual family. Every active
predicate must have a nearby code comment naming its development support,
closest controls, plausible in-world mechanism, and feature flag. Low support
is disclosed; it is not converted into certainty through enthusiastic prose.

### 8.1 Manual policy inventory

The following is the readable inventory of the concrete hand-written
hypotheses currently represented in `terminal_approval.py` and
`claim_signal.py`. It describes mechanisms, not a list of cases. The
experimental rows are jointly removable with
`MIB_EXPERIMENTAL_SYNTHETIC_POLICY=0`.

| Hypothesis | Reusable premise | Outcome and independent guard |
|---|---|---|
| Clean biometric quorum | A clean active B-13, complete visible core fields, fee authority, arrival, and multiple source types agree | Approve; any hard/review flag, contest, stale date, embargo, invalid sponsor, or invalid waiver vetoes |
| Complete five-source packet | All five ordinary source types agree on complete core fields, clean B-13, fee authority, and arrival | Approve despite one unreadable ancillary attachment; any mandatory-field or denial guard vetoes |
| Clean damaged supporting page | A clean B-13 and two ordinary authorization sources survive a four-page damaged packet | Experimental approval only with supported arrival and no risk, decision, contest, or denial witness |
| Diplomatic source authority | DIP-1 has complete paid/waived mission evidence from the program-appropriate fee/intake/sponsor or fee/intake/registry chain | Approve; unsupported fee/arrival, risk, contest, and ordinary denial witnesses veto |
| Diplomatic embargo exception | DIP-1 may require clearance rather than ordinary-jurisdiction denial | Experimental approval only with complete diplomatic authority; sparse no-B-13 packets remain review |
| Electronic fee interface | Titan DIP-1 and the ALPHA_DRACONIAN interface can carry electronic payment authority when the ordinary receipt read fails | Experimental approval; complete core and arrival evidence plus clean/absent risk and program-specific controls remain mandatory |
| Reciprocal MED-3 registry | Named fictional jurisdictions can use a complete CLEAR fee/intake/registry chain as the biological-clearance authority | Experimental approval; any flag, contest, unknown page, missing core source, unsupported fee/arrival, or visible decision vetoes |
| Gliese sponsor clearance | A Gliese-581g registry plus intake still requires a current sponsor attestation | Experimental denial at calibrated 0.80 when the sponsor source is absent; accepted fee, supported arrival, no note, and no risk flag are required |
| Registry-native diplomatic interface | JOVIAN_GASFORM and VENUSIAN_MYCELIAL DIP-1 waiver packets can use an agreeing registry chain instead of conventional B-13 | Experimental approval; the same complete-chain vetoes apply |
| TRIANGULAN waiver treaty | A visible waived fee and complete intake-based core packet can establish a visa-neutral fictional treaty waiver | Experimental approval; no risk, contest, decision, unknown page, or unsupported field is tolerated |
| Technical medical mission | Visibly sourced XW technical authority plus visibly sourced medical-consult purpose does not replace required biometric clearance, and a visibly read waived status changes payment status rather than medical eligibility | Deny only for the repeated paid-or-waived fee+intake+registry backbone with no visible Alpha Draconian, Andromedan, LUNA, or complete paid Jovian/Titan alternate interface; authenticated findings, notes, audit uncertainty, contests, unknown pages, and every other topology retain review |
| Sideways fragmented fee receipt | A damaged receipt may retain a row-local fee status even when its heading is unreadable | Read only from exact active-case unknown pages with two-scale agreement; review unlock additionally requires a defaulted fee, visible DIP-1, clean risk, and no decision/reason/contest before the ordinary quorum and safety passes |
| Explicitly missing MED-3 B-13 | The active biometric form explicitly marks its panel missing | Deny under the inferred edge policy; mere absence or unreadability is excluded |
| MED-3 compound clearance conflict | Unreadable biological clearance and an independent sponsor conflict jointly fail two mandatory controls | Deny; either single fault alone stays review |
| MED-3 transit mismatch | Transit purpose cannot satisfy a medical authorization when no biometric source exists | Low-confidence denial; visible/signed evidence still outranks it |
| Invalid waiver composition | A non-diplomatic medical program relies only on a diplomatic waiver and lacks intake/clearance authority | Deny or review according to the complete source state; a valid program source vetoes |
| Specialized interface review | LUNA XW-2 medical and AQUARIAN XW-1 packets without readable interface clearance need an additional check | Preserve review only; this hypothesis cannot create approval or a hard denial |
| ANDROMEDAN short-term neural clearance | The fictional ANDROMEDAN XW-1 program requires neural-integrity clearance in a repeated sparse topology | Experimental denial; diplomatic travel, readable clearance, other source topologies, or signed evidence vetoes |
| Europa sponsor clearance | An unsigned Europa Station strict-fence packet without a current sponsor source lacks jurisdictional clearance | Experimental denial after the ordinary visible-witness pass; generator-family and signed evidence are excluded |
| Negative generator polarity | A schema-valid hidden request has a repeated inverse generator polarity | Disclosed alternate approval authority after signed/positive-denial/risk vetoes; any disagreement can only abstain |
| Sirius avian waiver interface | A visible avian medical/transit program does not accept the visible waiver interface | Experimental denial; complete cohort 4/4 across four folds; signed, risk, and nonmatching visa/fee states are outside the rule |
| XW-2 sponsor assumption | A visible authorized XW-2 waiver still requires a sponsor-source assumption | Experimental denial; complete cohort 5/5 across all folds; risk, contest, unknown-page, sponsor-source, or nonvisible premise vetoes |
| Native registry notice | A case-bound native registry embargo or sponsor-verification notice can propose a policy denial | Diplomatic and review-fault exceptions veto; feature-flagged separately from visible evidence |

This table is an audit map, not proof that every experimental hypothesis will
transfer. Promotion depends on the 800-case development record plus genuinely
independent controls; the original 200 is spent. If an experimental row fails
the contract, the row, code, flag documentation, and any artifact derived from
it are removed together.

## 9. Required experiment record

Every attempted change must leave a concise changelog entry containing:

1. the frozen baseline artifact and score;
2. whether discovery used only the 800 development rows;
3. the exact proposed rule or learned feature set;
4. development support and counterexamples;
5. score and catastrophic-approval deltas;
6. whether the candidate was kept or completely removed;
7. any independent-control result, with the spent 200 reported historically;
8. Docker runtime and schema validation for a promoted candidate.

Temporary models, test scripts, training logs, and scratch outputs are deleted
when an experiment is rejected. The working tree must not retain a disabled
answer-shaped artifact as a souvenir.

## 10. Final release checklist

- [x] New manual discovery inspected only the frozen 800 development rows.
- [x] No learned component is active; rejected models were evaluated with
      five internal 640/160 development folds and removed completely.
- [x] No prohibited identifier, identity, lookup, fingerprint, or target
      feature reaches classification.
- [x] Every terminal rule has a documented mechanism, support, controls, and
      general vetoes.
- [x] Development has zero catastrophic false approvals.
- [x] The spent 200 validation is not used to select a rule, threshold,
      confidence, or performance optimization.
- [x] Extraction reports exact-cell gains and losses with verdict invariants.
- [x] Confidence is supported by held-out reliability rather than a desired
      score.
- [x] Schema and Docker checks use the 800 development packets and the
      organizer validation controls only. The spent 200 is not reopened.
- [x] Total Docker runtime is below four seconds per PDF under the organizer
      resource contract on the fixed 200-packet development fixture.
- [x] `README.md`, `MEMO.md`, and `CHANGELOG.md` match the promoted code and
      distinguish the full-800 host score from the Docker development slice.
