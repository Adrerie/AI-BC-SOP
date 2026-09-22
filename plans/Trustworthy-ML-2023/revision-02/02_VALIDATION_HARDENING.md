# Plan 2 — Validation hardening

## Goal

Make the validators catch the exact residual contradictions discovered after Revision 01.

## 1. Strengthen check_gates.py

Do not rely only on presence markers.

Add negative/regression checks for normative package files.

At minimum detect forbidden or suspicious patterns equivalent to:

- source license treated as unknown/unverified/all-rights-reserved
- universal "nothing from deployment stream may enter development"
- repository-wide zero-shot prohibition based only on class/semantic pretraining exposure
- "adversarial ... OOD family"
- empirical adversarial evaluation described as returning a bound/proof
- certification defined only as LP/SDP relaxation without being labeled source-specific
- certified result classified as an upper-bound row

The checker may exempt:

- historical plans
- explicitly quoted/superseded passages in the acceptance history

Document every exemption.

## 2. Add semantic invariant checks where feasible

The tool cannot prove research truth, but it can enforce local invariants.

Examples:

- SOURCE.md contains `trustworthyml.io`, `2310.08215`, and `CC BY 4.0`
- SOP-01 contains information-rights compliance language
- BM-04 contains an explicit statement that adversarial stress is a separate axis, not OOD evidence
- SOP-05 and BM-05 contain all three layers: target quantity, empirical attack, certificate
- Benchmark README does not place certificate in an upper-bound list

## 3. Hygiene scope

Either:

- scan `plans/` too, while allowing known placeholder/example paths safely, or
- continue excluding plans but make both tool output and acceptance report explicitly say
  `tracked non-plan files`.

Do not claim whole-repository coverage when the implementation excludes a subtree.

## 4. SOURCE verification

Do not require network access for routine acceptance.

The committed SOURCE.md is the normative attribution record. The validation tool should verify the
presence and internal consistency of that record.

Optional online verification may be documented separately but must not make local acceptance
non-reproducible.

## Gate C2-2

PASS only if intentionally restoring any one of the known bad phrases causes the corresponding
checker to fail.
