# 03 — Extension Decision Gate

## Goal

Decide the smallest correct repository change for every delta.

Create:

`Validation/Trustworthy-ML-Official-Updates-2024-2026/decision_log.md`

## Decision order

For each delta choose exactly one:

### D0 — Reject / record only

Use when:

- pedagogical only
- no actionable protocol
- insufficient evidence
- merely a modern example
- already fully covered

### D1 — Example refresh

Use when the existing method is unchanged and the new material only supplies a modern application.

Examples belong in notes or traceability, not as new Benchmark identities.

### D2 — Extend existing artifact

Use when the capability is already present but the official material adds:

- a new stress construction
- a new detector target
- a new reporting condition
- a new deployment constraint
- a new validity caveat

Prefer this over a new file.

### D3 — Add Extended Track

Use when the new protocol is useful but:

- source support is still limited,
- it is model-family-specific,
- or it is not universal enough to become Core.

### D4 — New Benchmark

Allowed only if all are true:

1. distinct target capability/failure mode;
2. cannot be expressed as a hypothesis/track inside an existing benchmark without semantic overload;
3. has enough source detail to specify design, baselines, metrics, aggregation, failure interpretation
   and validity limits;
4. adds reusable research value beyond one application.

### D5 — New SOP

Highest bar.

Allowed only if there is a reusable workflow with its own inputs → procedure → checks → stop
conditions → outputs that cannot be represented by the existing SOP chain.

## Mandatory decision cases

Give explicit decisions for:

- LLM attacks
- prompt-sensitivity detection
- RAG conflict detection
- attribution-family agreement
- confidence under shift/multi-turn
- privacy/data protection
- reproduction as boundary mapping
- rubric requirements (baselines/error bars/limitations)

## Architecture check

Before adding files, ask whether the repository now needs a canonical cross-source layer.

Do **not** create a second source-silo copy of an existing SOP/Benchmark just because the source year
changed.

If canonicalization is warranted, document it as a future architecture plan unless it is strictly
required for this update.

## Gate U3

PASS only if every accepted extension has a minimal-change destination and every proposed new file
passes the D4/D5 bar.
