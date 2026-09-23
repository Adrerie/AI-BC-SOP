# 05 — Benchmark / BC Extension

## Goal

Integrate only accepted capability/failure-mode deltas.

## Existing-Benchmark extension checklist

For each accepted D2/D3 change specify:

- hypothesis added
- target label / event
- information rights
- split/stress construction
- required baselines
- primary metrics
- aggregation
- variability/error bars if relevant
- failure interpretation
- resource/cost reporting
- validity limits
- link to executing SOP

## Candidate mappings to test

### BM-04 — detection

Possible additions:

- prompt-sensitivity detection
- RAG knowledge-conflict detection

Only if the detector target can be defined independently of the mitigation action.

### BM-05 — adversarial/security

Possible addition:

- LLM-specific attack track

Only if the threat model can be declared with comparable rigor. Prompt injection, jailbreak,
privacy leakage and ordinary distribution shift must not be silently merged.

### BM-06 — explanation

Possible addition:

- agreement/disagreement between mechanistic and training-data attribution families

Agreement must be reported as agreement, not truth.

### BM-03 / BM-04 / BM-07 combination

Possible addition:

- confidence degradation under shift / multi-turn interaction

Keep:
- calibration,
- ranking/detection,
- and action/abstention
as separate hypotheses even when tested in one study.

### BM-08 — integrity / replication

Possible extension:

- reproduce a claim under a new model/dataset and map where the conclusion holds, weakens, reverses or
  becomes inapplicable.

This should become claim-boundary evidence, not a binary "replicated / failed" label.

### New privacy benchmark

Create only if the official privacy/data-protection material yields a distinct evaluable capability
with enough protocol detail. Otherwise record it as future scope.

## New Benchmark gate

A new Benchmark must include the same 13-section operational schema as the current group and pass all
current structural/link/metric checks.

## Gate U5

PASS only if no new BC is merely an application-specific clone and every extension has an interpretable
failure case.
