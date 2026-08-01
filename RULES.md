# MIB Generalization and Evidence Rules

This file is the promotion contract for every classification, extraction, and
confidence change. It is stricter than the challenge's minimum rules. A higher
public score is not sufficient evidence that a change belongs in the default
pipeline.

## 1. Frozen 800/200 development boundary

From the checkpoint immediately before this file was added, all new pattern
discovery—manual or learned—uses only 800 development packets. This includes
PDF inspection, pixel/OCR inspection, native-text inspection, labels, derived
features, and error analysis. The remaining 200 packets are a prospective
holdout and stay closed until a complete candidate has been frozen.

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

This is a **prospective holdout**, not a historically untouched one. Earlier
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

The holdout may be opened once for a frozen candidate. If it fails, the result
is recorded and that holdout is considered spent; it must not become another
development set through repeated peeking.

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

Visible, source-bound evidence always wins over native hidden text. Hidden text
may propose a spelling, sentinel fill, or disclosed generator-family signal;
it may not overwrite a conflicting visible value or authenticated decision.

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
| Conflicting visible/native decision channels | A hidden generator disagreement cannot support a hard denial; abstain instead | 1 review and 1 approval were false denials; verdict moves only to review |
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
| Barnard five-source safety quorum | Five active source types provide redundant fictional safety authority even when one supporting panel is unreadable | 4 approvals, 0 others; 3 folds |
| Technical diplomatic identity gap | `XW-2` diplomatic missions with registry authority but no biometric channel preserve review rather than borrowing technical authority | 2 reviews, 1 approval; 2 folds; review has positive classification utility |
| Diplomatic reactor authority gap | `DIP-1` reactor work with exactly fee + intake + registry lacks a biometric or sponsor operational channel | 3 reviews, 2 approvals; 3 folds; review has positive classification utility |

The one-packet revoked-sponsor exception was rejected: despite a plausible
source-precedence story, it lacked recurring support and the ordinary visible
revocation fence correctly overruled it. Paid packets with merely unreadable
risk panels were also not promoted as a blanket approval family because
unreadability is not affirmative clean evidence.

Every route that changes review to approval is explicitly marked and passed
through the final safety fence again. A recovered unsigned approval must have
visible fee support, visible arrival support, source-backed observations for
all seven core policy fields, and either a clean risk channel or a separately
documented source-complete registry/electronic interface. Hidden generator
markers have no exception to that contract.

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

Only after the component and all hand-written rules are frozen may a final
model be fit on the complete 800-case development partition and evaluated
once on the sealed 200-case holdout. The holdout cannot select features,
thresholds, exceptions, hyperparameters, or a second candidate.

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
coarse routing-reliability family. Rates were fit on four internal folds and
checked on the excluded fifth fold before rounding to the conservative values
used at runtime:

| Reliability family | Development outcomes | Five held-fold estimates | Runtime confidence |
|---|---:|---:|---:|
| Fallback approval after all review vetoes | 66 correct, 2 incorrect | 0.946–0.982 | 0.95 |
| Inferred denial without a direct witness | 14 correct, 0 incorrect | 0.917–0.929 | 0.92 |
| Visible-source review family | 38 correct, 0 incorrect | 0.966–0.971 | 0.97 |
| Residual review after higher-reliability families | 18 correct, 4 incorrect | 0.706–0.826 | 0.78 |

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
transfer-risk controls. The sealed 200 was not inspected to explain or tune
any of these outcomes.

That artifact is now a **superseded development checkpoint**, not the current
acceptance score. The independent rules audit found that recovered approvals
could bypass affirmative evidence and that several two-row policy cells were
too targeted. Those routes were removed or structurally fenced afterward.

### Current exact generalized candidate

The first exact run after those removals and fences used only the fixed 800
development packets and produced 800 valid rows with no missing, extra,
duplicate, or invalid records:

| Exact development result | Score |
|---|---:|
| Extraction | 46.965278 / 50 |
| Classification | 77.325000 / 80 |
| Calibration | 18.834415 / 20 |
| **Total** | **143.124693 / 150** |
| Catastrophic false approvals | **0** |

The confusion is 205 correct approvals, 18 approvals preserved as review, 344
correct denials, 6 denials preserved as review, 217 correct reviews, and 10
reviews incorrectly approved. Prediction SHA-256 is
`dcabd9e4f3b1b28c2fe578268ad3bf5f25991b819df767cb8417df541a8df63d`;
evaluation SHA-256 is
`6ef64f2a37c31c352d94a7d14f102c128b48187484881505328243f752cc0d24`.
The sealed 200 was not opened to explain or tune any of these outcomes.

The measured score is lower than the superseded checkpoint because this
candidate keeps ambiguous source-identical packets in review instead of using
two-row categorical exceptions. That is an intentional generalization cost,
not a score to be silently backfilled with the rejected rules.

The frozen replay after adding the categorical-evidence and terminal-review
invariants produced the identical prediction SHA-256 above. On a cold
constrained 200-packet slice selected only from these 800 development packets,
those invariants changed exactly two verdicts: both ordinary false approvals
became correct reviews. No other verdict or ordinary extraction field moved;
one of those review packets also restored its source-supported review risk.
The organizer evaluator measured 46.572222 extraction, 76.55 classification,
18.40768 calibration, **141.529902 total**, and zero catastrophic false
approvals on that runtime slice. This is portability evidence, not a holdout
estimate.

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
| Approval safety | Unsigned approvals face fee, MED-3 missing-panel, archival-intake, and visible-risk checks | Must not demote an already supported approval merely because one redundant source is unreadable |
| Strict-fence recovery | A review may resolve from a direct denial witness or a broad clean source topology | No weak absence-only approval |
| Blurred manual finding | Visible word-envelope geometry reads a damaged adjudicator note | Requires note structure and never uses hidden text or identity |
| Fictional program policy | Species/visa/purpose or jurisdiction/source combinations model a recurring clearance requirement | Flagged, disclosed, counterexample-tested, and never a real-world demographic claim |
| Negative generator family | A schema-valid hidden request can serve as an explicitly untrusted generator-level polarity proposal | Signed evidence and visible policy veto; feature-flagged |
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
| Technical medical mission | XW technical authority plus medical-consult purpose does not replace required biometric clearance | Deny only for the repeated complete paid source topology with no alternate-interface exception; otherwise retain review |
| Explicitly missing MED-3 B-13 | The active biometric form explicitly marks its panel missing | Deny under the inferred edge policy; mere absence or unreadability is excluded |
| MED-3 compound clearance conflict | Unreadable biological clearance and an independent sponsor conflict jointly fail two mandatory controls | Deny; either single fault alone stays review |
| MED-3 transit mismatch | Transit purpose cannot satisfy a medical authorization when no biometric source exists | Low-confidence denial; visible/signed evidence still outranks it |
| Invalid waiver composition | A non-diplomatic medical program relies only on a diplomatic waiver and lacks intake/clearance authority | Deny or review according to the complete source state; a valid program source vetoes |
| Specialized interface review | LUNA XW-2 medical and AQUARIAN XW-1 packets without readable interface clearance need an additional check | Preserve review only; this hypothesis cannot create approval or a hard denial |
| ANDROMEDAN short-term neural clearance | The fictional ANDROMEDAN XW-1 program requires neural-integrity clearance in a repeated sparse topology | Experimental denial; diplomatic travel, readable clearance, other source topologies, or signed evidence vetoes |
| Europa sponsor clearance | An unsigned Europa Station strict-fence packet without a current sponsor source lacks jurisdictional clearance | Experimental denial after the ordinary visible-witness pass; generator-family and signed evidence are excluded |
| Negative generator polarity | A schema-valid hidden request has a repeated inverse generator polarity | Disclosed approval/denial proposal only; visible signed findings and ordinary policy witnesses veto |
| Native registry notice | A case-bound native registry embargo or sponsor-verification notice can propose a policy denial | Diplomatic and review-fault exceptions veto; feature-flagged separately from visible evidence |

This table is an audit map, not proof that every experimental hypothesis will
transfer. Promotion still depends on the 800-case development record and the
one-time sealed holdout. If an experimental row fails the contract, the row,
code, flag documentation, and any artifact derived from it are removed
together.

## 9. Required experiment record

Every attempted change must leave a concise changelog entry containing:

1. the frozen baseline artifact and score;
2. whether discovery used only the 800 development rows;
3. the exact proposed rule or learned feature set;
4. development support and counterexamples;
5. score and catastrophic-approval deltas;
6. whether the candidate was kept or completely removed;
7. the one-time holdout result, only after the candidate is frozen;
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
- [x] The prospective holdout remains sealed; it has not selected a rule,
      threshold, confidence, or performance optimization.
- [x] Extraction reports exact-cell gains and losses with verdict invariants.
- [x] Confidence is supported by held-out reliability rather than a desired
      score.
- [x] Before holdout release, schema and Docker checks use the 800 development
      packets and the unlabeled organizer validation corpus only. A combined
      1,000-row train run is allowed only as part of the frozen one-time
      holdout audit.
- [x] Total Docker runtime is below five seconds per PDF under the organizer
      resource contract; sub-four remains a best-effort optimization target.
- [x] `README.md`, `MEMO.md`, and `CHANGELOG.md` match the promoted code and
      distinguish the full-800 host score from the Docker development slice.
