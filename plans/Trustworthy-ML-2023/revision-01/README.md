# Revision 01 — Methodological correction and reproducible acceptance

This revision repairs the first implementation of the *Trustworthy Machine Learning* (2023) package after external review.

The existing 8-SOP / 8-Benchmark structure is **not** to be discarded by default. The goal is to preserve the useful reconstruction while correcting methodological overreach, metric errors, setting-specific rules presented as universal rules, and a validation process that is not independently reproducible.

## Execution order

1. [00_REVISION_MASTER.md](00_REVISION_MASTER.md)
2. [01_METRIC_AND_CONFIDENCE_CORRECTIONS.md](01_METRIC_AND_CONFIDENCE_CORRECTIONS.md)
3. [02_SETTING_AND_SPLIT_SCOPE.md](02_SETTING_AND_SPLIT_SCOPE.md)
4. [03_CAUSAL_AND_DECISION_LANGUAGE.md](03_CAUSAL_AND_DECISION_LANGUAGE.md)
5. [04_ROBUSTNESS_AND_CERTIFICATION_SCOPE.md](04_ROBUSTNESS_AND_CERTIFICATION_SCOPE.md)
6. [05_REPRODUCIBLE_VALIDATION.md](05_REPRODUCIBLE_VALIDATION.md)
7. [06_REPOSITORY_ARCHITECTURE_AND_ATTRIBUTION.md](06_REPOSITORY_ARCHITECTURE_AND_ATTRIBUTION.md)
8. [07_REACCEPTANCE.md](07_REACCEPTANCE.md)

## Governing rule

Do not repair by weakening everything into vague prose. Preserve strong rules where they are logically or experimentally justified. Replace only unjustified universal claims with properly scoped conditional rules.

All previous PASS statements are provisional. The final acceptance report must be regenerated after this revision and may not reuse prior PASS status without rerunning the relevant checks.
