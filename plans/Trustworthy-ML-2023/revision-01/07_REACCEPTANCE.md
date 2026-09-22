# Revision Plan 7 — Re-acceptance

## Goal

Re-run acceptance from zero after all substantive revisions.

The old acceptance result is historical evidence only and must not be copied forward.

## 1. Required re-checks

Re-run at minimum:

### Mathematical checks

- AUPR positive-class baseline
- AUROC orientation
- perplexity / log-base consistency
- constant-confidence oracle/deployable distinction

### Setting checks

- information-rights language
- legitimate adaptation settings
- split-dependence logic
- final-test contamination handling
- multi-axis evaluation support

### Evidence checks

- causal wording in SOP-03 / BM-02
- explanation interpretation in SOP-07 / BM-06
- mitigation admissibility and objective trade-offs in SOP-06
- abstention prerequisites in SOP-06 / BM-07

### Robustness checks

- certification limitations scoped to the described method
- empirical versus certified wording
- method-conditional transform requirements
- threat-model-specific attack adequacy

### Reproducibility checks

- validation tools committed
- portable source configuration
- no absolute local paths
- links and schemas
- cross-link symmetry
- source traceability

### Repository checks

- root architecture supports future synthesis across sources
- SOURCE.md attribution present

## 2. Acceptance report rewrite

Rewrite:

`Validation/Trustworthy-ML-2023/acceptance_report.md`

The report must:

- record this revision as a new revision cycle
- list every issue from Revision 01
- state what changed
- state the re-run evidence
- mark each item PASS / FAIL
- retain known limitations honestly

Do not claim "all gates pass" if any P0 remains.

## 3. Regression check against original strengths

Confirm that the revision did not destroy:

- 8 SOP / 8 Benchmark structure unless a justified change was necessary
- non-mirroring concept reconstruction
- source traceability
- operational procedures
- cross-links
- Core / Extended distinction

## 4. Final status

The package may be marked ACCEPTED only if:

- every P0 correction passes
- validation is reproducible
- no new contradiction has been introduced between shared metric definitions and benchmark-local definitions
- all changed files remain internally linked and readable

P1 issues may remain only if explicitly documented and judged non-blocking. The repository architecture and SOURCE.md tasks in this revision are expected to be completed, not deferred.

## 5. Commit and branch rule

Commit all revisions to the existing branch:

`plan/trustworthy-ml-2023`

Do not merge to `main` automatically.

At completion, report:

- files changed
- files added
- acceptance result
- unresolved limitations
- latest commit SHA
