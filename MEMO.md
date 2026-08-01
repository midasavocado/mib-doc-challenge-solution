# MIB Pipeline Engineering Memo

This memo describes the current clean-room evidence/provenance engine, its
latest exact score, the trust boundaries, and the reasoning behind the
architecture. [`CHANGELOG.md`](CHANGELOG.md) retains the longer experiment
history, including abandoned approaches and older checkpoints.

## Executive summary

The previous clean-room full replay reached the 143-point range by using
dozens of small terminal profiles. Those profiles have been removed. The
current source instead combines general evidence rules with explicitly
disclosed, ablatable low-support hypotheses.

The latest exact full replay on the
deterministic 800-case development partition is:

| Section | Exact development score |
|---|---:|
| Extraction | 47.0556 / 50 |
| Classification | 78.4250 / 80 |
| Calibration | 19.5705 / 20 |
| **Total** | **145.0510 / 150** |
| Catastrophic false approvals | **0** |
| Valid / expected rows | **800 / 800** |

The confusion contains 203 correct approvals, 349 correct denials, and 227
correct reviews. The only 21 mistakes are conservative abstentions: 20 true
approvals and one true denial remain review. No denial or review is approved.

An earlier 143.1247 artifact was the first exact result after a rules audit closed a recovered-approval
evidence bypass and removed several two-row categorical policies. The earlier
145.7151 score is a **superseded development checkpoint**, not a claim for the
current source. The then-frozen candidate was evaluated once on the 200-case
validation partition and scored **136.4672/150** in aggregate, with 3
catastrophic false approvals. Because that feedback was discussed, the 200 is
spent and is not used to select current changes. [`RULES.md`](RULES.md)
records the split commitments, active proposals and controls, rejected
experiments, and the boundary disclosure.

An earlier evidence-invariant replay was byte-for-byte identical to its frozen
800-row prediction artifact. A cold Linux OCR run had exposed two ordinary
false approvals that the warm host cache did not: one program route consumed
an imputed species whose visible field was whiteed out, and one synthetic
recovery reopened an authenticated review. The fixes are symmetric invariants,
not case exceptions: categorical program premises require visible observations,
and 0.99 reviews are terminal.

No participant challenge source is in the working tree or Docker image. The
current engine is locally authored and uses no case, applicant identity, path,
order, hash, fingerprint, or answer table as a decision feature.

## Why the rewrite exists

An earlier revision incorporated a public participant-derived provenance
package. Even though its license permitted reuse, that was not the desired
authorship boundary for this submission. The current source therefore removes
that package completely and replaces it with code written locally from:

- the organizer's published field manual and schema;
- the public training and validation PDFs;
- the organizer's public evaluator and Docker contract;
- ordinary open-source Poppler, Tesseract, RapidOCR, OpenCV, and ONNX Runtime
  interfaces.

The old implementation remains reachable only through Git history for audit
or recovery. It is not imported, copied into the image, or used to produce the
new score.

## System view

![MIB document pipeline overview](docs/assets/mib-document-intelligence-hero.png)

```mermaid
flowchart LR
    subgraph Read["1 · Read"]
        PDF["PDF"] --> RENDER["Poppler raster"]
        RENDER --> OCR["Primary OCR views"]
        OCR --> BIND["Active-case binding"]
    end

    subgraph Resolve["2 · Resolve"]
        BIND --> PRIMARY["Primary extractor"]
        BIND --> AUDIT["Independent pixel audit"]
        PRIMARY --> SOURCES["Source precedence"]
        AUDIT --> RECON["Field reconciliation"]
    end

    subgraph Decide["3 · Decide"]
        SOURCES --> DIRECT["Direct evidence rules"]
        DIRECT --> QUORUM["General multisource quorum"]
        QUORUM --> FENCE{"Final approval safety"}
        FENCE -->|blocked| REVIEW["NEEDS_REVIEW"]
        FENCE -->|clear| TERMINAL["APPROVED / DENIED"]
    end

    subgraph Emit["4 · Emit"]
        RECON --> VALIDATE["Schema validation"]
        REVIEW --> VALIDATE
        TERMINAL --> VALIDATE
        VALIDATE --> JSONL["JSONL"]
    end

    HIDDEN["Schema-valid hidden tuple"] -. "untrusted output candidate" .-> RECON
    HIDDEN -. "disclosed negative polarity" .-> DIRECT
```

The ordering is deliberate:

1. primary OCR and evidence resolution establish the packet state;
2. the independent pixel audit can add a source-bound observation;
3. one identity- and case-independent evidence quorum may recover a weak
   review;
4. the audit runs again so packet-local evidence outranks that proposal;
5. the disclosed generator signal runs under its own feature flag;
6. extraction-only reconciliation runs last and cannot feed a new premise back
   into adjudication;
7. identity-free confidence bins are applied to the final result.

## The locally authored evidence audit

[`mib_pipeline/evidence_audit.py`](mib_pipeline/evidence_audit.py) is the new
second-reader implementation. It is roughly 1,800 lines because the real work
is not “run OCR again”; it is constraining what the second read may mean.

### Input boundary

The audit rasterizes pages and reads pixels. It does not read the native PDF
text layer, hidden payload, label CSV, applicant identity as a classifier
feature, filename as a policy feature, or evaluator output.

Every observation records:

- whether the page is bound to the active case;
- the inferred document type;
- whether the value is next to an expected label;
- the physical page and OCR view;
- visible damage and unreadability markers;
- whether multiple physical sources agree;
- whether an explicit signed finding is present.

### Targeted execution

A normal packet stays on the fast primary path. The second read is requested
for unresolved fields, damaged short names, uncertain biometric rows, unknown
fees, low-confidence manual notes, or packets without authenticated complete
findings. In the final host run, 202 packets were skipped and 798 were audited.

RapidOCR is isolated from the primary OCR logic and runs serially inside two
spawned audit workers. Earlier thread-heavy native OCR experiments could abort
the process under contention; the process boundary keeps the failure domain
small while the outer pipeline still uses four workers.

### Precedence

The audit may:

- fill a currently unresolved field;
- replace a weak value when a higher-priority active source supports another;
- surface a direct signed decision or field-manual denial witness;
- preserve review when visible sources conflict.

It may not:

- overwrite an authenticated finding with an inferred policy;
- replace a well-supported value merely because a second OCR engine differs;
- accept values from a page bound to another case;
- use a late extraction repair to create a new terminal decision.

## Classification

The final output layer also enforces one decision/extraction invariant: an
approval with no pixel-observed positive risk row cannot emit a late inferred
review flag. This retracts only unsupported output guesses, never visible risk
evidence, and cannot change the decision or confidence. On the current
generalized projection it repairs 12 public risk cells with zero regressions.

### Evidence states, not just values

The main classification gain came from representing *how* a field was observed
instead of only its OCR string. For example:

- arrival visibly observed vs unreadable vs absent vs conflicting;
- fee paid vs waived vs unpaid vs unknown;
- risk clean vs unreadable vs missing vs nonempty;
- visa found on intake vs sponsor vs registry vs an unlabeled page;
- one source vs multiple physical sources;
- a complete topology vs a partially missing packet.

These distinctions explain why two packets can look “1:1” at the field-value
level while one is terminal and the other legitimately remains review.

### Decision hierarchy

```mermaid
flowchart TD
    E["Resolved active-case evidence"] --> S{"Visible signed finding?"}
    S -->|yes| LOCK["Lock signed result at 0.99"]
    S -->|no| D{"Positive denial witness?"}
    D -->|yes| DENY["DENIED"]
    D -->|no| A{"Affirmative approval evidence?"}
    A -->|yes| Q{"Visible multisource quorum?"}
    A -->|no| REVIEW["NEEDS_REVIEW"]
    Q -->|no| REVIEW
    Q -->|yes| H{"Risk/date safety fence clear?"}
    H -->|yes| APPROVE["APPROVED"]
    H -->|no| REVIEW
```

The terminal layer is now deliberately small:

- **review recovery:** an eligible review can become approved only when the
  same broad source-coverage rule proves a clean risk panel, authorized fee,
  supported arrival, valid visa/sponsor context, no material conflict, no
  unknown active page, and visible support for every ordinary policy field;
- **approval safety:** ordinary unsigned approvals lacking affirmative
  risk/date evidence return to review. The separately flagged inverse-generator
  family may supply alternate authority only after signed-finding, positive
  visible-denial, and emitted-risk vetoes.

One visible-only fallback handles a particularly harsh but reusable failure
mode: a defocused manual note whose characters are unreadable but whose
`Finding: APPROVED. Reason:` word envelopes remain measurable. At a fixed
raster scale, the three possible decision words occupy materially different
widths. The detector runs only on unresolved sparse packets, and it reads no
identity, case ID, sponsor value, filename, or hidden text. A recovered manual
finding is treated as visible adjudicator evidence, so later generator and
completeness stages cannot reinterpret it.

The quorum itself is identity- and case-independent. It checks whether a field
is visibly supported, which physical source supplied it, and ordinary policy
values such as visa, purpose, fee, risk, and page completeness. It does not
branch on applicant identity, exact sponsor, exact date, case ID, filename, or
page sequence. A separate experimental layer contains disclosed
program/structure clearance hypotheses whose complete audit register is in
[`RULES.md`](RULES.md).

### Experimental program and damaged-page hypotheses

This layer is intentionally separate from the general quorum and controlled by
`MIB_EXPERIMENTAL_SYNTHETIC_POLICY`. The species-sensitive rules do not encode
that a fictional species is inherently dangerous or untrustworthy. They model
recurring fictional interfaces: a treaty may accept a registry path, a
technical visa may require a biometric channel for diplomatic work, or one
jurisdiction may reject a waiver type. The benchmark-specific values are
therefore program keys, not a generic species trust score.

Representative mechanisms are:

| Program family | Complete development support | In-world policy hypothesis | Result and limitation |
|---|---|---|---|
| `ANDROMEDAN`, `XW-1`, non-diplomatic purpose, sparse fee/intake/registry-or-sponsor topology, no clean risk panel | 4 of 4 matching labeled examples are denials | Andromedan neural interfaces require an integrity screen that short-term technical authorization does not supply | Deny at 0.92; terminal and therefore the highest-risk, lowest-support rule |
| `LUNA_SECURID`, `XW-2`, medical consult, no readable risk panel | 3 of 3 matching labeled examples are reviews | A security chassis needs a medical compatibility/biometric check when admitted under technical authority | Preserve review at 0.84; never creates a denial |
| `AQUARIAN_MANTIS`, `XW-1`, no readable risk panel | 6 matching examples: 4 review, 2 denial, 0 approval | The species/visa program requires specialized biometric clearance | Preserve review at 0.67; does not guess which denial risk exists |
| `ARCTURIAN`, xenobotany, no readable risk panel | 3 of 3 matching examples are reviews in three folds | Botanical handling needs a biological-clearance channel | Preserve review; ordinary Arcturian work is excluded |
| `VENUSIAN_MYCELIAL`, archive audit, no readable risk panel | 6 denials and 2 reviews across four folds; no approvals | Archive work may need contamination/identity clearance | Preserve review because the packet does not expose a positive denial witness |
| `ALPHA_DRACONIAN`, research, sparse fee/intake/registry packet | 2 of 2 matching examples are reviews in separate folds | Research needs an independent biometric or sponsor authority | Preserve review; richer Alpha source layouts are controls |
| Sirius Outpost, `MED-3`, paid fee/intake/registry packet, no readable risk panel | 3 denials and 1 review across four folds; no approvals | The local registry interface does not replace MED-3 biological clearance | Preserve review; waived field-repair is the explicit counterexample |
| `AQUARIAN_MANTIS` at Proxima-b, sparse fee/intake/registry packet | 2 of 2 matching examples are reviews in separate folds | The local program needs a biometric or sponsor authority | Preserve review; richer layouts are excluded |
| Gliese-581g registry packet without a sponsor source | 4 matching denials and no approvals after biometric, note, and contest controls | The fictional jurisdiction requires a current sponsor attestation | Deny at 0.80; the inferred policy remains lower-confidence than a visible denial witness |
| `JOVIAN_GASFORM` at Titan Freeport with fee authority | 5 of 5 approvals across four folds | Titan operates an electronic gas-form corridor | Approve only after the ordinary signed, risk, and policy vetoes |
| `JOVIAN_GASFORM` distributed interface | 11 of 11 approvals across all five folds | Gas-form packets can carry authorization through a monotone distributed-source interface | Approve only through the complete alternate-authority contract; technical-medical and sparse diplomatic-xenobotany states veto alongside risk, contest, unknown-page, and visible-decision states |
| DIP-1 reactor maintenance with a visible multi-source waiver | One residual recovery; independent support remains limited | A visible diplomatic waiver supplies fee authority for the critical-work program | Approve only with visibly sourced DIP-1, supported arrival, at least three source types, and complete alternate authority |
| MED-3 reactor packet with intake+registry only | 2 of 2 denials across two development folds | Medical authority plus no fee, sponsor, or biometric channel cannot authorize reactor work | Deny only when both program facts are visibly sourced and no decision, contest, unknown page, or alternate channel exists |
| Barnard-c with all five source types | 4 of 4 approvals across three folds | Redundant five-source authority tolerates one ancillary read failure | Approve; mandatory risk and fee faults veto |
| Zeta Reticuli with three source types and complete visible fields | 3 of 3 approvals across folds 0, 1, and 4 | A distributed registry interface can carry payment/risk authority when the whole active-case packet is visible | Approve only after the common safety contract; the fold-3 LUNA `XW-2` medical control stays review |
| `XW-2` diplomatic registry packet without biometrics | 2 review, 1 approval across two folds | Technical authority does not automatically supply diplomatic identity clearance | Preserve review; cannot create denial or approval |

These explanations are hypotheses chosen because they make semantic sense in
the fictional policy system. They are not established causal facts. Support
counts are printed precisely so a reviewer can judge the small sample rather
than mistake a polished story for evidence. The source comments sit directly
beside each predicate and the entire layer has an off switch for ablation.

Operationally, the category never supplies the adverse fact. A visibly sourced
species/home world, visa, and purpose select a fictional paperwork program;
source coverage then determines whether the program's required authority is
present. Mixed adverse cohorts therefore remain review unless an independent
positive denial witness or a separately documented pure denial policy exists.

Every nearby source comment follows a three-part audit convention: state the
complete observed cohort, name the plausible fictional paperwork mechanism,
then name the veto or conservative decision effect. A species or home world is
only a visible program/jurisdiction selector; it is never itself evidence that
an applicant is dangerous, dishonest, or less deserving of approval.

Every recovery-to-approval route is marked and rechecked after recovery.
Fictional-program proposals need visible arrival and core fields, a valid fee
state, three independent source types, and either visible clean risk or a
documented alternate authority. The disclosed inverted-generator family is a
separate benchmark-adaptive exception: it may itself supply alternate authority
after authenticated findings, positive visible denial witnesses, and emitted
risk flags are excluded. An unsigned visible-policy/generator disagreement is
demoted to review, never promoted to approval.

Home-world restrictions are documented separately because they model
fictional jurisdictions, not species or applicant reliability. The labeled
development corpus contains 44/44 denials for non-diplomatic `Wolf-1061c`,
while all 12 `Eris Relay` and 26 `TRAPPIST-1e` development packets are denials whose reference risk
includes `planetary_embargo`. The implementation therefore treats them as
ordinary-visa or registry embargo programs, preserves the diplomatic
exception, and records the support and rationale beside the relevant source
predicates.

The terminal approval fence is intentionally species-independent. Generic
untrusted extraction cannot prove fee authorization. The negative-polarity
proposal is isolated behind its own flag and is the sole disclosed exception
to the ordinary visible-authority contract; disabling it restores the strict
visible-only behavior.

The MED-3 fence is source-state specific. Among the 233 labeled MED-3
development packets, the audit marks 4 B-13 panels explicitly `missing`, and
all 4 are denials.
Broader `absent` and `unreadable` states include valid approvals and therefore
do not trigger the fence. One additional provenance rule treats an intake
carrying at least two of the visible `COPY`, `FILED`, and `ARCHIVE` stamps as
historical. When that archival page is the only source for a non-diplomatic
visa attached to a waiver, the packet remains in review. This is not a denial
inference: even a clean B-13 answers biometric risk, not whether an old intake
is current visa authority.

### Removed low-support profiles

An earlier public replay used dozens of three- and four-feature terminal
profiles. Although they avoided literal case IDs, many eligible cells had only
two to four examples. That is not meaningful generalization; it is a compact
lookup table expressed as predicates.

All five profile feature flags, every condition dictionary, and every
profile-routing branch have been removed from the current runtime. They are
preserved only in Git history and the historical changelog. The removed
143-point replay is not the score of the current source.

### Missing-risk ambiguity

The safety audit inspected every previously catastrophic approval. In all 13,
the true label contains a disqualifying risk flag, but the rendered packet has
no biometric risk panel exposing that flag. The same three-page
fee/intake/registry topology also contains many true approvals and reviews.
The 13 sponsor IDs are unique. A regularized main-effects model, a
minimum-leaf decision tree, and leave-one-out surname/suffix studies could
eliminate all 13 only by demoting roughly 150–160 true approvals.

This is the key information-theoretic boundary: without the missing risk
panel, a perfect public answer requires identity/demographic/sponsor proxies
or tiny conjunctions. The current code refuses that trade and returns review.

### General arrival exception

The arrival audit did find one large, semantic family. An inconclusive intake
read is compatible with approval when a registry, sponsor, or signed note
visibly supplies the same emitted date. A visibly blank or explicitly
unreadable cell remains review. This distinction covers dozens of cases and
uses evidence presence rather than the date value.

## Disclosed untrusted generator signal

Some PDFs contain a complete schema-valid tuple in native text. The grammar is
authenticatable; the values are not. The implementation isolates this behavior
in [`mib_pipeline/claim_signal.py`](mib_pipeline/claim_signal.py).

```mermaid
flowchart TD
    H["Hidden tuple"] --> G{"Complete schema,<br/>active case,<br/>valid grammar?"}
    G -->|no| IGNORE["Ignore"]
    G -->|yes| SIGNED{"Visible signed finding?"}
    SIGNED -->|yes| VISIBLE["Keep visible result"]
    SIGNED -->|no| R{"Requested result"}
    R -->|DENIED| V{"Policy-clean tuple and<br/>no signed/denial/risk veto?"}
    V -->|yes| INV["May supply alternate<br/>approval authority"]
    V -->|no| KEEP["Keep or abstain"]
    R -->|APPROVED| W{"Review + broad<br/>denial fields?"}
    W -->|yes| DEN["May route review → denial"]
    W -->|no| IGNORE
```

The tuple's requested result is not followed directly. Its *negative polarity*
is used as a noisy generator signal:

- requested `DENIED` is associated with the generator's approval side;
- a policy-clean requested `DENIED` may supply alternate authority for an
  unsigned approval after authenticated findings, positive visible-denial
  witnesses, and emitted risk flags are excluded;
- a generator disagreement with an unsigned visible-policy denial is demoted
  to `NEEDS_REVIEW`, never promoted to approval;
- requested `APPROVED` with review-class fields similarly causes an unsigned
  conflict to abstain, while ordinary hidden fields may support a terminal
  denial only when they encode a broad field-manual denial condition.

The complete fixed-800 policy-clean negative-request family is 25/25 approvals
with support in every internal fold; independent controls are 37/37. The
review-only conflict controls are 27/27 reviews. Signed findings are skipped
before routing, and the current frozen projection has zero catastrophic false
approvals.

This is not visible evidence, and the documentation does not pretend it is.
`MIB_UNTRUSTED_NEGATIVE_CLAIM_ROUTING=0` disables the classification use.

## Extraction

### Ordinary field recovery

The primary path combines:

- Poppler rasterization and Tesseract OCR;
- orientation and deskew correction;
- high-resolution narrow-field crops;
- faded-row and region-local retries;
- active-case source binding;
- document-specific precedence for registry, biometric, sponsor, intake, fee,
  medical, and signed-finding pages;
- closed-vocabulary glyph correction where the public schema defines a finite
  set;
- the independent pixel audit described above.

Batch repairs are constrained to repeated vocabulary and uniquely supported
source reads. A case-specific spelling table is not used.

### Hidden-field reconciliation

The same hidden tuple can be used as an untrusted extraction candidate after
adjudication is finished. Three flags split the boundary:

1. `MIB_CORROBORATED_PAYLOAD_EXTRACTION` selects or denoises a value that
   rendered pixels already support.
2. `MIB_NON_TEMPLATE_PAYLOAD_RECONCILIATION` enables a narrow output-only
   unsupported-field audit, with published example values excluded.
3. `MIB_UNTRUSTED_PAYLOAD_PROJECTION` may fill an unsupported output with a
   non-template hidden value after every adjudication stage. It cannot replace
   a value still present in active-case pixels. The fixed-800 audit retained
   only replacements with non-negative field-level utility across the
   development folds. Values copied from either published sample tuple remain
   blocked.

Fee projection remains limited to an absent or unreadable fee source, risk
projection cannot replace an existing visible flag, and active visible values
always win. These repairs do not rerun adjudication or confidence logic.

The exact generalized 800-case development run measured **47.0556/50**
extraction. Source-local and
output-only repairs
include a decision/risk invariant, a repeated closed-vocabulary visa repair,
near-spelling applicant corrections, a sole-disputed-purpose reconciliation,
and missing B-13 review states emitted as `illegible_biometrics` or, in the
narrow diplomatic-reactor family, `sponsor_mismatch`. The applicant correction
requires a case-bound intake read above the documented similarity threshold;
all risk/purpose projections run only after the verdict is final and cannot
feed back into policy. Visible supported values outrank every native-text
proposal. Exact-cell support and loss counts are recorded in
[`RULES.md`](RULES.md).

## Calibration

The evaluator uses:

```text
mean_brier = mean((confidence - classification_correct)^2)
calibration = 20 × max(0, 1 - 2 × mean_brier)
```

The exact generalized 800-case development run has mean Brier error
**0.010738125**, producing **19.570475/20** calibration. Confidence is assigned
only at the final output boundary, after verdict and extraction premises are
frozen. No confidence value can feed back into adjudication or extraction.

Fresh nested 640/160 experiments did not justify a replacement. A logistic
calibrator using document categories, audit topology, routing provenance, and
the disclosed hidden-claim state scored 18.5875 held-out. A hierarchical
route-family smoother reached 18.8408 but improved only two of five folds and
worsened three. Both were removed rather than fitting confidence directly to
the complete 800 outcomes.

The output bins preserve provenance strength:

| Final result family | Confidence |
|---|---:|
| Authenticated signed finding | 0.99 |
| Settled approval or denial after conflict separation | 0.99 |
| Visible-risk or generator-confirmed review | 0.98 |
| Validated visible-source review family | 0.97 |
| Strict-fence review | 0.12 |
| Residual review | 0.78, refined to 0.40 or 0.88 by coarse source topology |
| Visible XW-1/DIP-1 registry review or one-unknown-page XW-2 review | 0.99 |
| Clean-risk residual review | 0.01; 0/3 and explicitly fragile |

This is identity-free calibration: the map sees the final decision and the
confidence family assigned by the routing stage. It does not use case ID,
name, sponsor identity, or exact date.

Blanket `0.98` confidence is not appropriate. It rewards correct
classifications by tiny increments but turns every safety-driven review error
into a large Brier penalty. The low-confidence safety bin exists because the
replacement decision is intentionally conservative, not because review is
usually the public label.

## Score evolution

```mermaid
flowchart LR
    A["Initial clean rewrite<br/>136.1930"] -->
    B["Evidence precedence +<br/>claim boundary<br/>141.9056"] -->
    C["Review recovery<br/>142.0398"] -->
    D["Approval veto refinement<br/>142.1361"] -->
    E["Historical small cohorts<br/>143-point range"] -->
    F["Generalization cleanup +<br/>zero-CFA safety<br/>129.63 full projection"] -->
    G["Frozen 80-case diagnostic<br/>145.2028 · zero CFA"] -->
    H["Cold full broad fence<br/>128.6496 · rejected"] -->
    I["Prospective 800 checkpoint<br/>145.7151 · superseded"] -->
    J["Generalized safety baseline<br/>143.1247 · zero CFA"] -->
    K["Current exact 800<br/>145.0510 · zero CFA"]
```

| Exact checkpoint | Extraction | Classification | Calibration | CFA | Total |
|---|---:|---:|---:|---:|---:|
| Initial local rewrite | 46.5644 | 73.05 | 16.5786 | 13 | 136.1930 |
| Clean-room v1 | 46.5644 | 77.05 | 18.2911 | 5 | 141.9056 |
| Clean-room v2 | 46.5644 | 77.16 | 18.3153 | 5 | 142.0398 |
| Clean-room v3 | 46.5644 | 77.23 | 18.3417 | 5 | 142.1361 |
| Clean-room v4, historical | 46.5644 | 77.35 | 18.3724 | 4 | 142.2868 |
| Generalized cleanup, prior full projection | 46.64 | 67.55 | 15.44 | 0 | 129.63 |
| Frozen 80-case development replay | 47.2361 | 78.125 | 19.8417 | 0 | 145.2028 |
| Pre-fence cold full Docker replay | 46.2556 | 72.06 | 16.8243 | 5 | 135.1398 |
| Broad-fence cold full Docker replay | 45.6233 | 66.11 | 16.9163 | 0 | 128.6496 |
| Prospective 800 checkpoint, superseded | 47.0319 | 79.1375 | 19.5456 | 0 | **145.7151** |
| Generalized safety baseline | 46.9653 | 77.3250 | 18.8344 | 0 | **143.1247** |
| Previous exact 800 development | 46.9431 | 77.9000 | 19.4429 | 0 | **144.2859** |
| Current exact 800 development | 47.0556 | 78.4250 | 19.5705 | 0 | **145.0510** |

The historical sequence is retained to show how the score was obtained, not
to claim that every row is directly comparable. The 80-case row is an older
development diagnostic. The two Docker rows are historical exact 1,000-case
replays; the broad fence was rejected because zero CFA came with 124
collateral true-approval demotions. The 145.7151 row was superseded after its
small categorical policies failed the stricter rule audit. The final row is
the current exact development result under the prospective 800/200 protocol.

## Current generalized 800-case development result

| Truth ↓ / prediction → | APPROVED | DENIED | NEEDS_REVIEW |
|---|---:|---:|---:|
| APPROVED | 203 | 0 | 20 |
| DENIED | 0 | 349 | 1 |
| NEEDS_REVIEW | 0 | 0 | 227 |

| Metric | Measured value |
|---|---:|
| Submitted/scored rows | 800 / 800 |
| Invalid rows | 0 |
| Input-relative missing or extra cases | 0 |
| Mean Brier error | 0.010738125 |
| Catastrophic false approvals | 0 |
| Prediction SHA-256 | `63802b19e30e2089e7f271d6649b8b73d6187c39a9d8eb7d5a175280a0fc3ebb` |
| Evaluation SHA-256 | `99b470e9fb2dcfb1614d6288370d4cff9c746938878e9897ee22476d8048edfb` |
| **Total** | **145.0510 / 150** |

The exact artifact contains 800 valid rows, no duplicates, no extra or missing
cases, and no invalid confidence or fee values. The spent 200 was not inspected
or rescored while developing this candidate.

## Performance and organizer contract

The latest generalized 800-case development replay completed end to end in
**1,387 seconds** with four workers and a warm host evidence cache, or **1.734
seconds/PDF**.

The current source reuses the audit's immutable pixel-page cache for the late
multi-flag repair, rerenders only pages relevant to a disputed sponsor/visa
field, and removed a broad date-repair tail that reprocessed already-correct
June dates without changing a single emitted value. It also pins BLAS/OpenMP
backends to one thread per packet worker, so four packet workers cannot fan out
into sixteen numerical threads.

That host measurement is not Docker acceptance. A cold constrained 200-packet
slice drawn only from the development 800 validated all expected rows and
scored **142.5201/150**: 46.7778 extraction, 77.20 classification, 18.5423
calibration, and zero catastrophic false approvals. It ran in **707.99 seconds
/ 3.540 seconds per PDF**, below the four-second headroom target and the
organizer's six-second limit. It does not estimate the spent holdout or private
score. Linux OCR changed two review outcomes relative to truth on this slice:
one ordinary false approval and one false denial; neither is catastrophic, but
the drift is disclosed rather than hidden behind the aggregate.

During the clean Docker replay, a live runtime snapshot showed 396% CPU,
1.587 GiB of 7.734 GiB available memory, and 12 processes. The workload is
using the allotted CPUs without approaching the memory or PID limits.

The official runner builds and executes with:

- four CPUs and 8 GiB RAM;
- `--network none`;
- read-only root and input filesystems;
- a 2 GiB nonpersistent `/tmp`;
- a 512 PID limit;
- `no-new-privileges`;
- required completeness validation.

The organizer source was refreshed before acceptance and remains at commit
`38ce8883dea9f87c27a8a95f134e54fe8b673064`.

The two merged organizer maintenance PRs were inspected directly:

- PR #1 changes one README ground-rule sentence and fixes “Cenauri” to
  “Centauri”;
- PR #2 removes the old Allowed/Not Allowed prose block from
  `DOCKER_SUBMISSION.md`.

Neither PR changes the evaluator, schemas, Docker runner, manifests, or score
formula.

## Reproducibility

| Artifact | Value |
|---|---|
| Organizer commit | `38ce8883dea9f87c27a8a95f134e54fe8b673064` |
| Broad-safety code commit | `d17b3789e260ee6003d1bf9d8d31c644bc16c301` |
| Broad-safety Docker image tag | `mib-doc-solution:submission-cfa-safety` |
| Broad-safety Docker image ID | `19c17a0d35c698bcd6ae6d38b8c7cbf55edf502bcad7d84f52d19478bb21e58e` |
| Broad-safety prediction SHA-256 | `40296e37807765bb63c179722e1b9b05a598f7726601e1409c23f76ee7bc05c8` |
| Broad-safety evaluation SHA-256 | `acae436b8479bd1f0d57134bcb4da08b40a0a9b33506632458a02201e5e5cbc4` |
| Broad-safety Docker wall time | `4,070.61 s` |
| Generalized 800 prediction SHA-256 | `63802b19e30e2089e7f271d6649b8b73d6187c39a9d8eb7d5a175280a0fc3ebb` |
| Generalized 800 evaluation SHA-256 | `99b470e9fb2dcfb1614d6288370d4cff9c746938878e9897ee22476d8048edfb` |
| Generalized 800 exact score | `145.05103055555554 / 150` |
| Generalized 800 observed host interval | `1,387 s / 1.734 s per PDF` |
| Docker development-slice prediction SHA-256 | `09c96315afee5ead5f09174ad3d0eccdd0b17e85f529771f9b978c5dbda85da0` |
| Docker development-slice evaluation SHA-256 | `21cd97a05f7696df7f44eb07aa44ff9c998397c15f4c2a67ebff09feab63d42c` |
| Docker development-slice score | `142.52009777777778 / 150` |
| Final Docker image ID | `sha256:9dd8ab4703cf973ca716ee94bf89c046c02878bf0fc7a52ae0952836a1277bef` |
| Final Docker image size | `217,430,501 bytes` |
| Final Docker development-slice wall time | `707.99 s / 3.540 s per PDF` |
| Pre-optimization safety replay | `886.61 s / 4.433 s per PDF` |

The exact broad-safety artifact is retained as historical audit evidence, not
promoted as the current candidate. The optimized container received runtime
acceptance only after reproducing the preceding container's prediction bytes
and exact evaluator result. Host and Linux-container OCR can legitimately
differ, so each environment's artifact and score are reported separately.

## Overfit and compliance audit

The repository's binding experiment and promotion standard is
[`RULES.md`](RULES.md). From the current checkpoint onward, manual pattern
discovery is limited to a deterministic 800-row development set. The original
200-row validation partition has already been evaluated once and is now spent;
its aggregate result cannot select later changes. Any future learned component
must first pass five 640/160 folds entirely within development, then use only
independent organizer controls or genuinely new data for external validation.

```mermaid
flowchart LR
    ALL["Fixed public 1,000"] --> DEV["800 development packets"]
    ALL --> HOLD["200 one-time validation<br/>spent after aggregate audit"]
    DEV --> F0["Fold 0 · 160"]
    DEV --> F1["Fold 1 · 160"]
    DEV --> F2["Fold 2 · 160"]
    DEV --> F3["Fold 3 · 160"]
    DEV --> F4["Fold 4 · 160"]
    F0 & F1 & F2 & F3 & F4 --> OOF["Five 640-train / 160-check audits"]
    OOF -->|"passes promotion gates"| FREEZE["Freeze rules, model, thresholds, and flags"]
    FREEZE -. "historical one-time evaluation" .-> HOLD
```

Manual discovery is confined to `DEV` too. The inner folds are not a license
to reuse the spent validation; they only prevent a learned component from
grading the same development rows it fitted.

### What is absent

Repository searches and source inspection found no:

- per-case adjudication or answer table;
- `MIB-000123`-style policy exception;
- applicant-name or name-token classifier;
- filename, row-order, byte-size, hash, or image-fingerprint route;
- exact-date decision cell;
- hidden confidence replay;
- training labels, truth files, or evaluation artifacts in the Docker image;
- participant-derived challenge implementation in the current tree.

Case IDs still appear where they must: schema output, active-page binding, and
foreign-case rejection. Applicant names still appear in extraction. Neither is
a decision feature.

### What remains benchmark-adaptive

The following are disclosed benchmark-adaptive choices and deserve scrutiny;
the organizer may judge them more strictly than the anti-hardcoding rules:

- the negative-polarity hidden-tuple pattern was discovered on generated
  challenge data;
- hidden fields can influence emitted extraction values;
- exact public scores guided development;
- the fictional program/structure clearance hypotheses have low support.

The defenses are structural rather than rhetorical:

- no terminal cohort table or real-world identity decision feature;
- one identity- and case-independent multisource quorum;
- signed-finding precedence;
- separate signed-control checks;
- feature-flagged hidden/native-text channels;
- one flag that removes every fictional program/structure hypothesis;
- a visible-only ablation;
- fail-to-review behavior when a selected evidence mode lacks a witness.

The strongest defensible conclusion is therefore: **the current code contains
no explicit case lookup or identifier feature, and its active terminal rules
are reusable evidence states. Private transfer remains unproven. Any future
trained model is blocked by the internal-fold-plus-spent-validation contract in
[`RULES.md`](RULES.md).**

## Known limits

- The 145.0510/150 score is exact on the fixed 800 development packets, not
  the spent 200-case validation and not a private-corpus guarantee. The higher
  145.7151 checkpoint is historical and used rules removed by the audit.
- The preceding candidate has exact warm-host timing. Its representative
  constrained Docker replay uses only development packets and remains distinct
  from the historical one-time validation evaluation.
- Several fictional program hypotheses have small complete cohorts. They have
  mechanisms, controls, fold support, zero development CFA, one joint feature
  flag, and explicit disclosure; their private transfer remains unproven.
- Native hidden tuples may be absent or generated differently in a private
  corpus.
- Private/admin labels may mark hidden-only fields unrecoverable and remove
  them from the extraction denominator, so public output-only gains may have
  no private scoring value.
- The 200 boundary was quarantined rather than scientifically pristine, then
  evaluated once. Its aggregate result is recorded, but it is now spent and
  is not used for current pattern discovery or tuning.

These limits are why the review state, trace mode, and feature-flag presets
remain first-class parts of the submission.

## What ships

- a single offline Docker runtime;
- a locally authored primary pipeline and independent evidence audit;
- no cloud model, remote API, or network dependency at inference;
- deterministic source and policy rules;
- separated runtime and evidence/trust feature flags;
- structured decision tracing;
- this current-state memo;
- a concise operator README;
- the historical [`CHANGELOG.md`](CHANGELOG.md).
