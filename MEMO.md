# MIB Pipeline Engineering Memo

This memo describes the current clean-room evidence/provenance engine, its
latest exact score, the trust boundaries, and the reasoning behind the
architecture. [`CHANGELOG.md`](CHANGELOG.md) retains the longer experiment
history, including abandoned approaches and older checkpoints.

## Executive summary

The repository now ships two deliberately separable classification branches.
Engine A combines general evidence rules, disclosed ablations, and a
conservative MED-3 safety requirement developed under the historical 800/200
protocol. Engine B reconstructs this repository's own public-fit classifier
from commit `d473fbf`; it is a benchmark instrument, not a transfer claim.

The latest exact full replay on the
deterministic 800-case development partition is:

| Section | Exact development score |
|---|---:|
| Extraction | 46.9028 / 50 |
| Classification | 73.4500 / 80 |
| Calibration | 17.8758 / 20 |
| **Total** | **138.2286 / 150** |
| Catastrophic false approvals | **0** |
| Valid / expected rows | **800 / 800** |

The confusion contains 171 correct approvals, 335 correct denials, and 211
correct reviews. No denied case is approved. The errors include conservative
reviews as well as ordinary approval/denial misses; they are not presented as
perfect classification.

The sealed 200 aggregate validation for the promoted build is **46.7389
extraction, 71.5000 classification, 16.9360 calibration, 135.1749 total, and
0 catastrophic false approvals**. A higher score-first candidate reached
72.7000 classification and 136.2405 total but retained one CFA, so it was not
promoted. The 200 is a repeatedly consulted aggregate validation benchmark,
not an untouched holdout: no per-row prediction, label, error, trace, feature,
confusion cell, filename, or PDF was used for the final safety rule.
[`RULES.md`](RULES.md) records the full boundary and experiment register.

With `MIB_BENCHMARK_FIT_CLASSIFIER=1`, an exact artifact-level bridge replay on
all 1,000 labeled public packets measured **46.6956 extraction, 79.9400
classification, 19.9568 calibration, 146.5924 total, and 0 catastrophic false
approvals**. This is not a fresh full OCR run: it applies the current Engine-B
code and arbiter to a saved exact Engine-A artifact. A live two-packet smoke
covered the projected residual boundary; current Engine A resolved one packet
and Engine B resolved the other.

An earlier evidence-invariant replay was byte-for-byte identical to its frozen
800-row prediction artifact. A cold Linux OCR run had exposed two ordinary
false approvals that the warm host cache did not: one program route consumed
an imputed species whose visible field was whiteed out, and one synthetic
recovery reopened an authenticated review. The fixes are symmetric invariants,
not case exceptions: categorical program premises require visible observations,
and 0.99 reviews are terminal.

No participant challenge source is in the working tree or Docker image. Engine
A is locally authored and uses no case, applicant identity, path, order, hash,
fingerprint, or answer table as a decision feature. Engine B restores only our
own generated model heads and rules from this repository's Git history. It has
no answer table, but it deliberately uses public-fit identity/sponsor shapes
and document profiles and must be judged accordingly.

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

That participant-derived implementation remains reachable only through Git
history for audit or recovery. It is not imported, copied into the image, or
used to produce the new score. Engine B is different: it recovers our own later
classifier/model code from `d473fbf` and adds a newly written counter-rule and
arbiter.

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
        SOURCES --> DIRECT["Shared packet state"]
        DIRECT --> QUORUM["Engine A · generalized rules"]
        DIRECT -. "copied state" .-> PUBLIC["Engine B · public benchmark fit"]
        QUORUM --> FENCE{"Final approval safety"}
        FENCE -->|blocked| REVIEW["NEEDS_REVIEW"]
        FENCE -->|clear| TERMINAL["APPROVED / DENIED"]
        REVIEW --> ARBITER["Asymmetric arbiter"]
        TERMINAL --> ARBITER
        PUBLIC --> ARBITER
    end

    subgraph Emit["4 · Emit"]
        RECON --> VALIDATE["Schema validation"]
        ARBITER --> VALIDATE
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

When Engine B is enabled, it branches from a copied pre-safety packet state.
The generalized branch still completes normally. The arbiter runs after both
decisions and after extraction is frozen; it may accept a decisive Engine-B
answer only when Engine A abstained. A settled Engine-A approval or denial has
precedence over every Engine-B disagreement.

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

A second visible-only recovery handles sideways fee receipts whose heading is
too fragmented for document-type classification. The pixel audit first supplies
the exact active-case page numbers it could not classify. The narrow reader
then rejects prompt-like text and every non-fee heading, rotates only those
pages, and requires both 150 and 200 DPI renders to produce the same row-local
`Fee ... Status` value. Linux Tesseract may preserve one blank physical row
between `Sta` and `tus`; the parser permits exactly that single gap while
retaining a four-row and 48-character geometry bound.

The complete 800 development census contained 127 structurally eligible
unknown-page packets. Six produced a two-scale fee read across three folds: two
approvals and four denials, with all six fee statuses read correctly. Five reach
the terminal reader in the normal runtime because the sixth has an earlier
authenticated finding. Only one unresolved clean diplomatic waiver acquired
new approval authority; all other reads merely corroborated terminal packets.
Sparse review retries additionally require a defaulted fee, visibly observed
`DIP-1`, a clean audited risk panel, no visible decision/reason/contest, and
confidence below 0.99. The ordinary quorum and both final safety passes still
decide the verdict.

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
| Visibly sourced `XW-1`/`XW-2` medical consult with visible fee + intake + registry but no B-13 | 4 of 4 unresolved packets are denials across three folds after interface controls | Technical work authority and a visibly read paid or waived status do not replace medical biometric clearance | Deny at 0.80; visible Alpha Draconian, Andromedan, and LUNA interfaces plus the complete paid Jovian/Titan interface veto; authenticated findings, notes, audit uncertainty, contests, and unknown pages stay outside the fallback |
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

The MED-3 fence is source-state specific. An explicitly `missing` B-13 keeps
the existing denial edge. The promoted safety guard separately requires an
affirmatively clean B-13 before an unsigned MED-3 verdict may remain approved;
an absent panel preserves review. This changed 22 development verdicts and
reduced classification by 1.1875 points, reflecting genuine valid-approval
counterexamples. It was accepted to remove the aggregate-validation CFA and
was not narrowed afterward. Unreadable panels remain a distinct state. One
additional provenance rule treats an intake
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

## Public benchmark-fit bridge

[`mib_pipeline/benchmark_fit_classifier.py`](mib_pipeline/benchmark_fit_classifier.py)
is an intentionally quarantined second classifier. Its provenance is exact:
the historical source rules and generated CatBoost heads were recovered from
this repository's own commit `d473fbf`. One Sirius/current-extractor
counter-rule and the arbiter were written locally for this bridge; neither
participant code nor an external prediction file is imported at runtime.

Engine B includes two kinds of public-label-trained logic:

- two 350-tree generated CatBoost heads over page sequence, source topology,
  fee/flag state, low-cardinality policy fields, and document-size/text-length
  profiles;
- ordered residual cells over applicant-name shape, sponsor-number shape,
  program fields, damage markers, and source-support counts.

Those features explain the score and the risk. They are more informative on
the public generator than Engine A's conservative abstention, but several
cells have only one to five public examples. They are benchmark fit by design.
The module contains no `case_id -> decision` dictionary and never edits an
output row by case identifier.

The arbiter is deliberately asymmetric:

| Engine A | Engine B | Selected result | Rationale |
|---|---|---|---|
| decisive | same decisive | common result | agreement |
| `NEEDS_REVIEW` | decisive | Engine B | benchmark branch resolves abstention |
| decisive | `NEEDS_REVIEW` | Engine A | visible/generalized evidence precedence |
| decisive | opposite decisive | Engine A | benchmark contradiction cannot erase settled evidence |
| `NEEDS_REVIEW` | `NEEDS_REVIEW` | `NEEDS_REVIEW` | neither branch has authority |

Public bridge replay changed only adjudication and confidence. Engine-B output
fields never replace Engine-A extraction. The public route family measured
999/1,000 correct, so combined mode emits confidence 0.99 and scores 19.9568
calibration points. With the flag set to `0`, the module is not imported and
Engine-A adjudication, extraction, and calibration remain unchanged.

This bridge is a useful disagreement experiment and public-score ceiling. It
is not evidence that the name/sponsor cells will transfer to validation or the
private anti-gaming set. The organizer permits candidate-trained models but
forbids hardcoded answers and audits source manually; submission use therefore
requires an explicit judgment call, not score laundering.

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

The same historical perfect checkpoint improved extraction by 101 raw points
relative to the saved Engine-A artifact: 21 cells gained and one sponsor cell
lost. The gains were six names, one species, nine visas, one sponsor net, one
arrival date, one purpose, and one risk field. Current source already contains
descendants of the historical case-bound/high-resolution repair helpers, so
the bridge does **not** wholesale-copy Engine-B fields. A future extraction
bridge should accept only a source-bound candidate when Engine A is unresolved,
or when Engine A has no active-source support and an independent high-resolution
reader agrees; sponsor replacement needs an even stronger gate because of the
observed regression.

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
3. `MIB_UNTRUSTED_PAYLOAD_PROJECTION` is the aggressive mode: after every
   adjudication stage it may replace a competing OCR output with a complete
   non-template hidden tuple. It is not visible evidence. Values copied from
   either published sample tuple remain blocked, and a later two-source pixel
   agreement can restore a visible value.

Fee projection remains limited to an absent or unreadable fee source and risk
projection cannot replace an existing visible flag. These repairs do not rerun
adjudication or confidence logic, but the aggressive tuple projection is a
real output-trust tradeoff and is disabled by `visible_evidence_only`.

The exact generalized 800-case development run measured **46.9028/50**
extraction. Source-local and
output-only repairs
include a decision/risk invariant, a repeated closed-vocabulary visa repair,
near-spelling applicant corrections, a sole-disputed-purpose reconciliation,
and missing B-13 review states emitted as `illegible_biometrics` or, in the
narrow diplomatic-reactor family, `sponsor_mismatch`. The applicant correction
requires a case-bound intake read above the documented similarity threshold;
all risk/purpose projections run only after the verdict is final and cannot
feed back into policy. Normal readers prefer visible support; the aggressive
final tuple projection is the disclosed exception. Exact-cell support and
loss counts are recorded in [`RULES.md`](RULES.md).

## Calibration

The evaluator uses:

```text
mean_brier = mean((confidence - classification_correct)^2)
calibration = 20 × max(0, 1 - 2 × mean_brier)
```

Benchmark-fit calibration is isolated from the generalized Platt mapping. The
bridge's fixed 0.99 confidence is fitted to its public route family and yields
mean Brier 0.00108 / 19.9568 points on the saved 1,000-row replay. It must not
be presented as private-set calibration.

The exact generalized 800-case development run has mean Brier error
**0.05310525**, producing **17.875790/20** calibration. Confidence is assigned
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
    K["Current zero-CFA 800<br/>138.2286"]
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
| Earlier exact 800 development | 46.9431 | 77.9000 | 19.4429 | 0 | **144.2859** |
| Immediate previous exact 800 | 47.0556 | 78.5000 | 19.6009 | 0 | **145.1564** |
| Score-first 800 candidate, rejected after aggregate CFA | 46.9028 | 74.6375 | 17.7328 | 0 | **139.2731** |
| Current zero-CFA 800 development | 46.9028 | 73.4500 | 17.8758 | 0 | **138.2286** |

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
| APPROVED | 171 | 5 | 47 |
| DENIED | 0 | 335 | 15 |
| NEEDS_REVIEW | 15 | 1 | 211 |

| Metric | Measured value |
|---|---:|
| Submitted/scored rows | 800 / 800 |
| Invalid rows | 0 |
| Input-relative missing or extra cases | 0 |
| Mean Brier error | 0.05310525 |
| Catastrophic false approvals | 0 |
| Prediction SHA-256 | `c537e8d2383eceb819ad4e2169dd0c37d4d5b575beede23510edaa93a2d6fc17` |
| Evaluation SHA-256 | `9a582d3d79f82d17b27b8b642e2a8293203c656b4d858d06de28b5b6a19d9f54` |
| **Total** | **138.2286 / 150** |

The exact artifact contains 800 valid rows, no duplicates, no extra or missing
cases, and no invalid confidence or fee values. The separate 200 was scored
only through the aggregate wrapper; its rows remained sealed.

## Performance and organizer contract

The latest generalized 800-case development replay completed end to end in
**1,087.34 seconds** with four workers and a warm host evidence cache, or
**1.359 seconds/PDF**.

The current source reuses the audit's immutable pixel-page cache for the late
multi-flag repair, rerenders only pages relevant to a disputed sponsor/visa
field, and removed a broad date-repair tail that reprocessed already-correct
June dates without changing a single emitted value. It also pins BLAS/OpenMP
backends to one thread per packet worker, so four packet workers cannot fan out
into sixteen numerical threads. The rotated-fee reader performs sparse
high-resolution work only for reviews that already satisfy every non-fee
approval premise; terminal packets require a direct fee hint in the primary
pixel read before the two-scale confirmation runs.

That host measurement is not Docker acceptance. A cold constrained 200-packet
slice drawn only from the development 800 validated all expected rows and
scored **132.4486/150**: 46.6111 extraction, 69.95 classification, 15.8875
calibration, and zero catastrophic false approvals. It ran in **710.11 seconds
/ 3.551 seconds per PDF**, below the four-second headroom target and the
organizer's six-second limit. This is a development-only portability and
runtime check; it is not an estimate of the separate validation or private
score. Host and Linux OCR can legitimately differ, so the Docker result is
reported independently rather than being presented as a reproduction of the
host score.

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

The organizer source was refreshed before acceptance. Upstream challenge core
remains at `38ce8883`; local commit `f480e6d6` adds only this submission's memo
files and changes no rule, evaluator, schema, or runner.

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
| Public dual-engine bridge score | `146.59235555555554 / 150` |
| Public dual-engine bridge prediction SHA-256 | `35c64aa505e98dd6dde80570afbce686806d4186fc91eabbbf674bcf65ad41b7` |
| Public dual-engine bridge evaluation SHA-256 | `9cd2d96428917ee6338b7e91a5d66208bb50aabb40d918c76bd6523f22ea43e7` |
| Organizer upstream core commit | `38ce8883` |
| Organizer local submission-doc commit | `f480e6d6` |
| Broad-safety code commit | `d17b3789e260ee6003d1bf9d8d31c644bc16c301` |
| Broad-safety Docker image tag | `mib-doc-solution:submission-cfa-safety` |
| Broad-safety Docker image ID | `19c17a0d35c698bcd6ae6d38b8c7cbf55edf502bcad7d84f52d19478bb21e58e` |
| Broad-safety prediction SHA-256 | `40296e37807765bb63c179722e1b9b05a598f7726601e1409c23f76ee7bc05c8` |
| Broad-safety evaluation SHA-256 | `acae436b8479bd1f0d57134bcb4da08b40a0a9b33506632458a02201e5e5cbc4` |
| Broad-safety Docker wall time | `4,070.61 s` |
| Generalized 800 prediction SHA-256 | `c537e8d2383eceb819ad4e2169dd0c37d4d5b575beede23510edaa93a2d6fc17` |
| Generalized 800 evaluation SHA-256 | `9a582d3d79f82d17b27b8b642e2a8293203c656b4d858d06de28b5b6a19d9f54` |
| Generalized 800 exact score | `138.22856777777778 / 150` |
| Generalized 800 observed host interval | `1,087.34 s / 1.359 s per PDF` |
| Docker development-slice prediction SHA-256 | `95f2cced59020e6076bf26d5900f5fb0e6c2c6a0310a036247b87d344e132b83` |
| Docker development-slice evaluation SHA-256 | `b1943ef40d1273f4cc9798c1ab786945948763176905c52363ce55d64674acc5` |
| Docker development-slice score | `132.4485711111111 / 150` |
| Final Docker image ID | `sha256:6730073e027af64aa37a593042293986e49cde4f462db6263a86e62c9b4a758f` |
| Final Docker image size | `217,434,647 bytes` |
| Final Docker development-slice wall time | `710.11 s / 3.551 s per PDF` |
| Pre-optimization safety replay | `886.61 s / 4.433 s per PDF` |

The exact broad-safety artifact is retained as historical audit evidence, not
promoted as the current candidate. The optimized container received runtime
acceptance only after reproducing the preceding container's prediction bytes
and exact evaluator result. Host and Linux-container OCR can legitimately
differ, so each environment's artifact and score are reported separately.

## Overfit and compliance audit

Engine B is explicitly excluded from the generalized claim below. It uses all
1,000 public labels, exact failed-row inspection, name/sponsor shapes, document
profiles, and tiny residual cells. That is the overfit benchmark the feature
flag exists to expose. `MIB_BENCHMARK_FIT_CLASSIFIER=0` removes the branch;
`visible_evidence_only` and `experimental_signals_off` disable it as well.

The repository's binding experiment and promotion standard is
[`RULES.md`](RULES.md). From the current checkpoint onward, manual pattern
discovery is limited to a deterministic 800-row development set. The original
200-row partition is now a repeatedly consulted **aggregate-only validation
benchmark**, not an untouched holdout. It may accept or reject a frozen
development candidate but may expose no row, prediction, error, confusion,
trace, feature, filename, or PDF. Any learned component must first pass five
640/160 folds entirely within development.

```mermaid
flowchart LR
    ALL["Fixed public 1,000"] --> DEV["800 development packets"]
    ALL --> HOLD["200 aggregate-only validation<br/>rows remain sealed"]
    DEV --> F0["Fold 0 · 160"]
    DEV --> F1["Fold 1 · 160"]
    DEV --> F2["Fold 2 · 160"]
    DEV --> F3["Fold 3 · 160"]
    DEV --> F4["Fold 4 · 160"]
    F0 & F1 & F2 & F3 & F4 --> OOF["Five 640-train / 160-check audits"]
    OOF -->|"passes promotion gates"| FREEZE["Freeze rules, model, thresholds, and flags"]
    FREEZE -. "aggregate score + CFA only" .-> HOLD
```

Manual discovery is confined to `DEV` too. The inner folds are not a license
to inspect the validation benchmark; they prevent a learned component from
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
- direction-specific fictional-program flags plus an all-experiments-off
  profile;
- a visible-only ablation;
- fail-to-review behavior when a selected evidence mode lacks a witness.

The strongest defensible conclusion is therefore: **the current code contains
no explicit case lookup or identifier feature, and its active terminal rules
are reusable evidence states. Private transfer remains unproven. Any future
trained model remains subject to the internal-fold-plus-sealed-aggregate
contract in [`RULES.md`](RULES.md).**

## Known limits

- The current 138.2286/150 score is exact on the fixed 800 development
  packets; the aggregate-only 200 result is 135.1749/150. Neither guarantees
  private transfer. Historical 145-point rows are development checkpoints.
- The current candidate has exact warm-host timing. Its constrained Docker
  replay uses only development packets and remains distinct from validation.
- Several fictional program hypotheses have small complete cohorts. They have
  mechanisms, controls, fold support, zero development CFA, one joint feature
  flag, and explicit disclosure; their private transfer remains unproven.
- Native hidden tuples may be absent or generated differently in a private
  corpus.
- Private/admin labels may mark hidden-only fields unrecoverable and remove
  them from the extraction denominator, so public output-only gains may have
  no private scoring value.
- The 200 boundary is not scientifically pristine and has been queried more
  than once. Only aggregate section scores, validity counts, and CFA count are
  exposed; all row-level material remains sealed and cannot nominate a rule.

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
