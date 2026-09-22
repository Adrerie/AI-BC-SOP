# Revision 03 — Final metric/parser patch and re-acceptance

Revision 03 is a small finalization pass after external review of Cycle 3.

The substantive direct patches are already on the branch. This revision must **not** redesign the
package. Its job is to validate the direct patch in a real local checkout, repair only regressions
revealed by that run, and write a new Cycle 4 acceptance record.

## Direct patches already applied

- added generic `aupr` for arbitrary declared binary detection tasks
- kept `aupr_success` / `aupr_error` as correctness-specific specializations
- changed BM-04 so OOD and multiplicity detection use generic `aupr`
- hardened `check_metrics.py` to parse multiple snake_case identifiers inside one inline-code span
- added a compound-parser self-test
- removed pseudo metric keys `true_robust_acc` and `empirical_attack_acc`
- replaced local unregistered shorthand such as `acc_shift` / `acc_diagonal`
- clarified SOURCE.md: source-derived documentation vs original repository validation code
- narrowed mutation-test claims to representative end-to-end mutations
- marked Cycle 3 acceptance as superseded pending this re-run

## Execution order

1. [00_VALIDATE_PATCH.md](00_VALIDATE_PATCH.md)
2. [01_FINAL_ACCEPTANCE.md](01_FINAL_ACCEPTANCE.md)

Do not merge `main` automatically.
