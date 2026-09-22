# Plan 3 — Final re-acceptance

## Goal

Regenerate acceptance after the direct corrections and Revision 02 consistency sweep.

## Required procedure

1. Run all committed validation tools from a clean checkout.
2. Run the source-dependent citation-index verification if the local PDF is available.
3. Run the new Revision 02 regression checks.
4. Manually read the changed normative passages in:
   - SOURCE.md
   - SOP-01
   - SOP-05
   - BM-04
   - BM-05
   - Benchmark group README
5. Check all affected traceability notes for correct provenance labels.
6. Update acceptance_report.md.

## Acceptance report requirements

The report must clearly distinguish:

- Revision 01 result
- direct post-Revision-01 corrections
- Revision 02 re-acceptance

For each latest-review issue, record:

- original defect
- direct correction or Revision 02 correction
- mechanical evidence
- reading judgment if required
- final PASS / FAIL

Remove stale open limitations that are now resolved, especially the source-license uncertainty.

Do not keep historical wording that says the source license is unknown except inside an explicitly
historical/superseded account.

## Final merge gate

The branch is ready for main only if:

- all Revision 02 gates pass
- all existing mechanical checks pass
- no unresolved P0/P1 remains from the latest review
- acceptance report states the exact validation scope
- no automatic merge has occurred

At completion report:

- changed files
- validation command(s)
- PASS / FAIL
- unresolved limitations
- latest commit SHA
