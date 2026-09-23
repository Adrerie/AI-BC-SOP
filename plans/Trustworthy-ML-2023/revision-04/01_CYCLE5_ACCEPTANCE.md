# Plan 2 — Cycle 5 final acceptance

## Goal

Replace superseded Cycle 4 with a current acceptance record based on the final AUPR contract.

## 1. Clean-run record

Use a clean checkout or detached worktree.

Record:

- exact commit tested
- Python version
- commands
- source configured / not configured
- actual output summaries

Do not reuse Cycle 4 counts without rerunning.

## 2. Acceptance report

Add **Cycle 5 — Revision 04** at the top of
`Validation/Trustworthy-ML-2023/acceptance_report.md`.

Close these findings explicitly:

1. `aupr_error` score orientation was previously under-specified
2. package-wide `aupr` previously did not distinguish AP from trapezoidal PR-AUC
3. Cycle 4's additional-repair count text was internally inconsistent
4. `check_metrics.py` documentation previously overclaimed its coverage

For each, give:

- defect
- direct correction
- mechanical evidence
- reading judgement where needed
- final PASS / FAIL

Cycle 4 remains historical.

## 3. Current validator scope

The Cycle 5 report must state the checker's real boundary:

`check_metrics.py` checks lower-case snake_case identifiers found inside inline-code spans in the
SOP/Benchmark artifacts plus explicit AUPR contract invariants. It does not prove that prose-only,
capitalized, or very short metric-like names are registered.

Do not describe it as checking "every metric name anywhere in the package".

## 4. Provenance

Confirm that the source traceability does not attribute the final numerical AP convention or the
`c` / `1-c` orientation rule to the book unless the source explicitly states them.

They are package synthesis / repository convention built on the source's positive-class definitions.

## Final merge gate

The branch is ready to merge into `main` only if:

- R4-1 passes
- Cycle 5 is the current acceptance record
- the three AUPR mutation probes are detected
- all full-suite checks pass
- source-dependent verification passes when the PDF is available
- no unresolved P0/P1 finding remains
- no automatic merge has occurred

At completion report the latest commit SHA and whether the branch is ready for merge.
