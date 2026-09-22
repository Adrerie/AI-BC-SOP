# Plan 1 — Cross-file consistency sweep

## Goal

Search every tracked package artifact, not only the files directly edited, for wording that conflicts
with the fixed principles in `00_MASTER.md`.

## Scope

Inspect at minimum:

- root README
- SOP and Benchmark group READMEs
- all 8 SOPs
- all 8 Benchmarks
- concept_reconstruction.md
- source_coverage.md
- SOURCE.md
- acceptance_report.md

Plans may contain historical reviewer text and are not normative package content.

## Required searches and repairs

### A. Licensing and attribution

Search for:

- `all rights reserved`
- `license unknown`
- `license unverified`
- claims that no official source exists
- claims that the local PDF is the licensing authority

Normative files must state or defer to:

- official project website: `https://trustworthyml.io/`
- arXiv:2310.08215
- CC BY 4.0

Historical statements may remain only when explicitly labeled as superseded history.

### B. Information-rights consistency

Search for universal forms of:

- no deployment data may enter development
- target data are always leakage
- target labels always invalidate an experiment
- adaptation is out of scope

Replace with setting-relative information-rights logic.

### C. Zero-shot consistency

Search for rules that make zero-shot depend on a repository-defined universal ban on semantic or
class exposure during pretraining.

Require:

- exposure disclosure
- benchmark/study definition
- duplicate contamination and task-specific adaptation kept separate

### D. Adversarial / OOD separation

Search for:

- adversarial examples called an OOD family
- adversarial robustness used as evidence of OOD robustness
- OOD detection results used as adversarial robustness evidence

Keep these axes separate.

### E. Robustness semantics

Search for statements equivalent to:

- empirical attack evaluation returns a robustness bound
- attacked accuracy proves worst-case robustness
- certification is defined specifically as LP/SDP relaxation
- certification is universally restricted to shallow or binary models
- certificate rows are upper bounds on robust accuracy

Correct hierarchy:

```text
true worst-case robust accuracy
        ↑ certified lower bound
        ↓ empirical attacked accuracy can remain above truth if attacks miss failures
```

More precisely, under the same model, test set, threat model, and valid implementations:

`certified_acc <= true_robust_acc <= empirical_attack_acc`

Do not state this ordering when the quantities use different threat models, samples, or definitions.

### F. Acceptance-report scope

Every claim such as "all tracked files" must match the actual checker's inclusion/exclusion rules.

## Gate C2-1

PASS only if the sweep records zero unresolved contradictory normative statements.
