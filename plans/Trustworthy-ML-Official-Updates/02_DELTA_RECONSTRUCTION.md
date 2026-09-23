# 02 — Delta Reconstruction

## Goal

Compare the official update material against the accepted 2023 package by **research function**, not
by lecture title.

Create:

`Validation/Trustworthy-ML-Official-Updates-2024-2026/delta_map.md`

## 1. Compare against current package

Use the current SOP/Benchmark set as the reference:

### SOP
- SOP-01 setting
- SOP-02 splits/leakage
- SOP-03 learned evidence
- SOP-04 confidence truthfulness
- SOP-05 worst-case stress
- SOP-06 mitigation/abstention
- SOP-07 explanation evaluation
- SOP-08 reporting/evidence boundaries

### Benchmark
- BM-01 distribution shift
- BM-02 spurious cue dependence
- BM-03 confidence truthfulness
- BM-04 error/anomaly detection
- BM-05 adversarial robustness
- BM-06 explanation quality
- BM-07 selective prediction under cost
- BM-08 evaluation integrity

For every extracted official-course item assign one primary status:

- **covered**
- **covered but modern example**
- **covered but protocol extension**
- **new failure mode**
- **new capability**
- **new deployment constraint**
- **new metric/aggregation requirement**
- **new reporting requirement**
- **new SOP workflow**
- **pedagogy only**
- **insufficient evidence**

## 2. Keep axes separate

Do not mix:

- problem/capability
- failure mode
- method family
- architecture/model family
- application
- threat model
- dataset
- metric
- decision policy
- deployment information rights

"LLM" or "RAG" alone is not a capability.

## 3. Candidate-delta records

For every item not simply "covered", create a record:

- delta ID
- observed official source
- existing artifact(s) it touches
- what is actually new
- why an existing artifact is insufficient
- required information rights
- target capability/failure
- candidate evaluation design
- candidate baselines
- candidate metrics
- validity boundary
- provenance class
- disposition recommendation

## 4. Explicit tests for preliminary candidates

### Prompt sensitivity

Ask whether the new contribution is:

- perturbation robustness,
- failure detection,
- selective prediction,
- or all three under separate hypotheses.

Do not collapse them.

### RAG conflict

Separate:

- conflict occurrence
- conflict detection
- conflict explanation/surfacing
- conflict resolution
- downstream answer correctness

### Attribution agreement

Separate:

- attribution method quality
- cross-family agreement
- causal truth
- usefulness for debugging

Agreement is not automatically correctness.

### Confidence under shift / multi-turn

Separate:

- calibration
- ranking/detection
- temporal/turn-level drift
- decision/abstention

Do not call all confidence degradation "uncertainty estimation".

### Privacy/security

Decide whether the material fits BM-05 threat-model logic or requires a separate capability family.
Do not force privacy leakage into adversarial robustness.

### Reproduction

Decide whether it extends BM-08 with claim-boundary mapping, or is only a course project format.

## Gate U2

PASS only if every candidate delta has a disposition recommendation and no proposed new artifact is
just a model/application renaming of an existing capability.
