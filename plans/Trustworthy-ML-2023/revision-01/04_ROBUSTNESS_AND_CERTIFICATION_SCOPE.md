# Revision Plan 4 — Robustness and certification scope

## Goal

Separate source-specific adversarial robustness examples from general robustness principles.

## 1. Certification scope

Audit:

- SOP-05
- BM-05
- acceptance_report.md
- concept_reconstruction.md
- source_coverage notes where necessary

The book's discussed certificate / relaxation may have constraints such as shallow architectures or simplified tasks. Those constraints belong to that **specific method described in the source**, not to certified robustness as a field.

Replace universal wording like:

- certification is limited to shallow networks
- certification is limited to binary tasks

with:

> the specific certification approach discussed in the source has these assumptions / limitations; other certification families may have different scopes.

The package may remain book-derived, but it must not turn one example into a universal truth.

## 2. Empirical versus certified claim

Preserve the important distinction:

- empirical attack result: no failure found under attack configuration C
- certified result: a property proven within a stated threat model and certificate assumptions

Do not call empirical attack accuracy a proof of robustness.

## 3. Transform defenses

Remove any universal mandatory rule that an inference-time transformation must always have been applied at training time.

Instead:

- verify whether the defense definition or claimed method requires train-time exposure
- evaluate the full deployed pipeline adaptively
- state training and inference transformations separately
- test for masking / broken-gradient effects

## 4. Attack selection

Do not require "strongest affordable PGD" as if it were a universally sufficient adversarial evaluation.

Retain it as one useful reference for the source's setting.

General rule:

- attacks must be appropriate to threat model and defense
- adaptive attacks are required against defense mechanisms
- multiple complementary attacks may be needed
- attack adequacy must be argued, not inferred from iteration count alone

## 5. Adversarial versus corruption robustness

Keep these separate.

Semantic corruption, natural distribution shift, and adversarial perturbation can share reporting machinery, but they are not one capability and should not be collapsed.

## Gate R — Robustness scope

Pass only if:

- source-specific certification limitations are labeled as source-specific
- empirical and certified claims remain distinct
- transform-defense checks are method-conditional
- attack adequacy is threat-model-specific
- adversarial and non-adversarial robustness are not conflated
