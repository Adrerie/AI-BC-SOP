# Plan 2 — Cycle 4 final acceptance

## Goal

Replace the now-superseded Cycle 3 status with a current Cycle 4 record based on an actual clean run.

## 1. Clean environment

Run acceptance from a clean checkout or detached worktree whose path differs from the development
workspace.

Record:

- branch
- commit SHA
- Python version
- source PDF configured or not
- exact command
- actual summary lines

## 2. Source-dependent verification

If the local book PDF is available, verify the citation index against it.

Record the actual:

- headings
- definitions
- captions
- offset
- diffs

Do not invent or copy the prior cycle's counts without rerunning.

## 3. Acceptance report

Update `Validation/Trustworthy-ML-2023/acceptance_report.md`.

Add **Cycle 4 — Revision 03** at the top as the current record.

Cycle 4 must explicitly close the four findings that opened this revision:

1. generic AUPR semantics for OOD/multiplicity
2. compound inline-code metric-parser blind spot
3. mutation-test coverage wording
4. SOURCE.md source-derived/original-code scope

For each, record:

- defect
- direct patch
- mechanical evidence
- final status

Cycle 3 remains historical.

## 4. Current counts

Update current-output examples in documentation only with values actually produced by the run.

Pay special attention to:

- `check_metrics parser_findings=...`
- `unregistered=...`
- `register_size=...`
- mutation case count
- gate/invariant counts
- citation counts

## 5. Final review

Manually inspect:

- SOP-08 metric register
- BM-03
- BM-04
- SOP-05
- BM-05
- SOURCE.md
- tools/check_metrics.py
- tools/README.md

Check that no wording still treats generic OOD/multiplicity AUPR as `aupr_success` or
`aupr_error`.

## Final merge gate

Ready for `main` only if:

- R3-1 passes
- Cycle 4 acceptance is current
- all mechanical checks pass
- source-dependent check passes when source is available
- no unresolved P0/P1 remains
- branch remains unmerged

Report final commit SHA and whether the branch is ready to merge.
