# 08 — Post-review patch closeout

The substantive review fixes are already committed. Do not redesign the package.

## Already fixed

- BM-09 separates AUROC random reference (0.5) from AUPR/AP member-prevalence reference.
- Surrogate/target membership leakage invalidates the ordinary benchmark row; it is not relabeled as an upper bound.
- The course's sentence-vs-corpus MIA result is treated as a motivating LLM example, not a universal expected shape.
- H-emission now has an explicit primary rate and reporting fields.
- H-channel requires both raw disclosure rates plus `disclosure_gap`.
- SOP-08 correctly identifies `disclosure_gap` as a post-book register addition.
- BM-04 states H-sensitivity positive class, score orientation and AP baseline.
- Root README says 8 SOPs + 9 Benchmarks and distinguishes BM-09 provenance.
- `delta_map.md` / `decision_log.md` were synchronized with the corrected semantics.
- Root lineage wording, the full-deck count, and the stale decision-count sentence were also corrected after review.

## Remaining work

1. Read the touched files once for wording consistency.
2. Run the repository's **existing** acceptance command; do not add new gates, mutation cases, or validation machinery unless an actual failure requires a small repair.
3. If green, update `Validation/Trustworthy-ML-Official-Updates-2024-2026/acceptance_report.md` with the new commit and actual outputs, remove the stale-status note, and mark the review patch closed.
4. Commit and push the same branch. Do not merge `main`.

Report only: PASS/FAIL, any actual regression found, files additionally changed, and final commit SHA.
