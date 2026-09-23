# Trustworthy ML Official Updates — 2024–2026

## Purpose

Use official post-book Trustworthy ML course material to extend the existing SOP/Benchmark lineage
only where it adds a genuinely new research capability, failure mode, evaluation protocol, or
operational requirement.

The source audit and delta analysis are already complete. The resulting evidence lives in:

- `Validation/Trustworthy-ML-Official-Updates-2024-2026/source_inventory.md`
- `Validation/Trustworthy-ML-Official-Updates-2024-2026/delta_map.md`
- `Validation/Trustworthy-ML-Official-Updates-2024-2026/decision_log.md`

## Working rules

- Prefer a small extension to an existing SOP/Benchmark over a new file.
- A new Benchmark is justified only for a genuinely distinct evaluable capability.
- Do not create artifacts just because a newer model family or application appears.
- Keep post-2023 material explicitly separate from book-derived provenance.
- If a source cannot be read, mark it partial/unavailable rather than infer its contents.
- Do not add new validation machinery unless an actual failure requires it.

## Current state

The official-update content and the post-review corrections are already committed. In particular,
BM-09 now separates AUROC and AP baselines, treats surrogate leakage as invalid evaluation, limits the
sentence-vs-corpus observation to its source setting, gives H-emission a primary measurement, and
requires both raw channel rates with `disclosure_gap`.

## Remaining work

1. Read the files changed by the post-review patch once for obvious wording/consistency problems.
2. Run the repository's existing acceptance command. If the local source PDF is available, run the
   existing source-dependent check as well.
3. Fix only actual failures found by that run.
4. Update the official-updates acceptance report with the current commit and actual outputs, removing
   its stale status note.
5. Commit and push this branch. Do not merge `main`.

No additional gates, mutation cases, validation layers, or architecture work are requested.
