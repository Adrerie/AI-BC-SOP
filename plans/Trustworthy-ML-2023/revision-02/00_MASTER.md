# Revision 02 Master Plan

## Objective

Close the remaining gap between locally corrected files and package-wide consistency.

## Fixed principles

The following are now authoritative for this package and must hold everywhere:

1. **Source license**: official project website `trustworthyml.io`; citation arXiv:2310.08215;
   source license CC BY 4.0.
2. **Information rights**: target/deployment information is legitimate when the declared setting
   grants it; undeclared access is the integrity failure.
3. **Zero-shot terminology**: disclose pretraining exposure; use the benchmark/study's explicit
   definition rather than a repository-wide universal definition.
4. **Adversarial ≠ OOD**: adversarially constructed inputs may be used as an additional stress axis
   for a confidence detector, but are not an OOD family by definition.
5. **Worst-case robustness has three layers**:
   - target quantity: worst allowed perturbation inside the threat model;
   - empirical attack evaluation: attempts to find failures and can miss them;
   - certified evaluation: gives a provable guarantee/bound under certificate assumptions.
6. **Certified robust accuracy direction**: a valid certificate provides a lower bound on true robust
   accuracy for the specified threat model. It is not an oracle upper-bound row.
7. **Validation claims must match checker scope**: if a scanner excludes `plans/`, the report must
   say so.

## Preserve

Preserve the 8 SOP / 8 Benchmark structure, source traceability, and Revision 01 improvements.

## Completion rule

Revision 02 passes only if:

- no contradictory wording remains in package artifacts;
- validation tooling tests the corrected principles rather than only looking for a few positive
  marker phrases;
- all mechanical checks pass;
- acceptance report is regenerated and accurately distinguishes automated checks from reading
  judgments;
- no P0/P1 item from the latest review remains open.
