# 04 — SOP Extension

## Goal

Modify SOPs only for accepted workflow-level deltas.

## Rules

1. Preserve existing IDs and meanings.
2. Do not turn one SOP into an LLM-specific document.
3. Add modern examples only when they clarify an already-general rule.
4. Any official-course-derived addition must be labeled in traceability.
5. Do not rewrite book-derived text as if later course material were part of the book.
6. New procedure steps require matching checks/failure conditions where appropriate.
7. New decision logic must name required information rights and deployment assumptions.
8. New metric use must resolve to the shared metric register or add a fully specified metric through
   the same discipline used in Cycle 5.

## Likely SOP destinations to test

These are hypotheses, not predetermined edits:

- SOP-01: new setting axes for foundation-model / interaction settings
- SOP-03: mechanistic-vs-data attribution as complementary evidence
- SOP-04: confidence degradation under shift or across turns
- SOP-05: LLM/security threat-model extension
- SOP-06: surface conflict / flag prompt sensitivity / abstain as distinct actions
- SOP-07: cross-family attribution agreement as a diagnostic, not causal proof
- SOP-08: error bars, limitation reporting, claim-boundary reporting

## New SOP gate

If a new SOP is proposed, document why none of SOP-01…08 can own the workflow without violating its
purpose.

## Gate U4

PASS only if SOP changes are minimal, provenance-complete, and preserve the original operational
chain.
