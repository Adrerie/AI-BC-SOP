# SOP group — Trustworthy ML methods (from *Trustworthy Machine Learning*, 2023)

Reusable standard operating procedures for building and evaluating ML systems whose claims
(generalization, confidence, explanation, robustness) must survive contact with a changed
environment. Derived from the book by concept reconstruction, not by chapter: see
[`concept_reconstruction.md`](../../Validation/Trustworthy-ML-2023/concept_reconstruction.md)
for the model these eight documents implement, and
[`source_coverage.md`](../../Validation/Trustworthy-ML-2023/source_coverage.md) for the audited
source universe.

A reader who has not read the book can execute any SOP here end to end.

## Workflow order

```text
SOP-01 declare the setting      -> SOP-02 freeze splits under leakage discipline
  -> (train)                    -> SOP-03 diagnose which evidence the model uses
  -> SOP-04 measure confidence truthfulness
  -> SOP-05 stress the worst case
  -> SOP-06 mitigate, or abstain
  -> SOP-07 (if explanations are used) evaluate the explanation instrument
  -> SOP-08 report evidence and validity boundaries
```

SOP-08 is also the **glossary owner**: every recurring term and metric name used in this group is
defined once in its §4 register. Other SOPs link there instead of redefining, and the benchmark
group uses the same names.

| ID | Procedure | Stage | Tier | Measured by |
|---|---|---|---|---|
| SOP-01 | [Specify the deployment setting before training](SOP-01-specify-deployment-setting.md) | define | Core + Extended | BM-08 |
| SOP-02 | [Build evaluation splits under leakage discipline](SOP-02-build-evaluation-splits-under-leakage-discipline.md) | freeze | Core + Extended | BM-01, BM-02, BM-08 |
| SOP-03 | [Diagnose which evidence the model actually uses](SOP-03-diagnose-learned-evidence.md) | diagnose | Core + Extended | BM-02, BM-06 |
| SOP-04 | [Measure confidence truthfulness](SOP-04-measure-confidence-truthfulness.md) | measure | Core + Extended | BM-03, BM-04 |
| SOP-05 | [Run worst-case stress evaluation](SOP-05-run-worst-case-stress-evaluation.md) | stress | Core + Extended | BM-05 |
| SOP-06 | [Choose a mitigation, or choose to abstain](SOP-06-choose-mitigation-or-abstain.md) | decide | Core + Extended | BM-01, BM-02, BM-03, BM-07 |
| SOP-07 | [Evaluate an explanation method before using it as evidence](SOP-07-evaluate-explanation-methods.md) | explain | Core + Extended | BM-06 |
| SOP-08 | [Report evidence and state validity boundaries](SOP-08-report-evidence-and-validity-boundaries.md) | report | Core + Extended | BM-08 |

## How to use this group with the benchmarks

Each SOP states its links in §11; each benchmark states its execution counterpart in §12. The
consolidated matrix lives in
[`acceptance_report.md`](../../Validation/Trustworthy-ML-2023/acceptance_report.md) and is the
cross-link check used at acceptance.

## Standing rules for this group

- **Core** is the minimum defensible procedure; **Extended** is required for high-stakes,
  published, or reused results. Do not fold optional methods into Core.
- Recurring terms take the SOP-08 register meaning. A metric name may not be redefined locally.
- Where one SOP depends on another, link it; do not copy the procedure.
- Numbers quoted as examples come from the source and are labelled with their section and page.
  The source supplies no default thresholds, bin counts, iteration budgets, or ε values, so none is
  invented here: a procedure names the choice you must make and record.
- Every SOP ends with traceability so a later revision can re-check the claim against the book.

## Scope note

This group is method-agnostic and application-neutral: it covers distribution shift, adversarial
stress, uncertainty, and explanation evaluation as evaluation and execution practice. It does not
cover the book's learning-setting variants that require deployment-stage supervision the procedures
here forbid (domain adaptation with labelled targets, test-time training, continual and few-shot
variants), nor its representation-learning showcase, nor the authors' forward-looking research
agenda — each of which is recorded with its disposition in the coverage audit.
