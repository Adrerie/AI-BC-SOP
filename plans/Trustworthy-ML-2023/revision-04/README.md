# Revision 04 — Final AUPR contract validation and Cycle 5 acceptance

Revision 04 follows a direct post-Cycle-4 patch that closes the last two metric-definition findings:

- the score orientation of `aupr_success` / `aupr_error`
- the numerical meaning of package-wide `aupr`

The package now defines `aupr` as **non-interpolated Average Precision (AP)**, not trapezoidal
PR-curve integration. Larger scores must point toward the declared positive class.

This revision must not redesign the package. It validates those definitions, proves that the new
metric guard fails on the known regressions, and writes the current Cycle 5 acceptance record.

## Execution order

1. [00_VALIDATE_AUPR_CONTRACT.md](00_VALIDATE_AUPR_CONTRACT.md)
2. [01_CYCLE5_ACCEPTANCE.md](01_CYCLE5_ACCEPTANCE.md)

Do not merge `main` automatically.
