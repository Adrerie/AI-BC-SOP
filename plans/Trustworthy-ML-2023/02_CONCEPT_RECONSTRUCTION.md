# Plan 2 — Concept Reconstruction

## Goal

Transform the source structure into an independent methodology model suitable for reusable SOPs and Benchmarks.

## Required Artifact

Create:

`Validation/Trustworthy-ML-2023/concept_reconstruction.md`

## Step 1: Build a concept graph

Group source material by methodological function rather than by chapter.

For each synthesized concept, record:

- concept name
- research question it answers
- source sections that contribute to it
- dependencies on other concepts
- whether it primarily belongs in SOP, Benchmark, both, or background only
- whether targeted body reading was required

A single synthesized concept may combine material from multiple chapters.

A single source section may contribute to multiple synthesized concepts.

## Step 2: Separate different axes

Do not mix distinct classification axes.

Keep separate when applicable:

- research problem
- evaluation capability
- method family
- data/distribution condition
- metric
- deployment constraint
- failure mode
- reporting requirement

For example, `OOD generalization` as a capability should not be conflated with a specific domain-generalization method.

## Step 3: Derive the operational taxonomy

Create a proposed SOP taxonomy and Benchmark taxonomy.

The taxonomies should reflect how a researcher works:

```text
define problem
→ identify assumptions and risks
→ design evaluation
→ run checks
→ measure failures and uncertainty
→ mitigate if needed
→ re-evaluate
→ report limits
```

This flow is illustrative. Adjust it to the source-derived concept graph.

## Step 4: Mark source-derived vs derived guidance

For each major rule, distinguish:

- `source-derived`: directly supported by the book
- `synthesized`: reconstructed from multiple source points
- `repository convention`: added to make the SOP/Benchmark operational

Do not present repository conventions as claims made by the book.

## Gate B — Reconstruction

Pass only if:

- the final taxonomy does not mirror book chapter order
- major artifact names are task/capability oriented rather than chapter oriented
- at least some final concepts synthesize material from multiple source sections where appropriate
- source-to-concept traceability is preserved
- methods, metrics, capabilities, and failure modes are not collapsed into one classification axis
