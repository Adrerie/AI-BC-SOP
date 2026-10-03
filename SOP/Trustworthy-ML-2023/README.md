# SOP group — Trustworthy ML methods

Reusable standard operating procedures for building and evaluating ML systems whose claims
(generalization, confidence, explanation, robustness) must survive contact with a changed
environment. The eight SOPs originate from a concept reconstruction of the 2023 book. The eight SOPs
now carry selected official-course updates, where those updates extend the same workflow. See
[`concept_reconstruction.md`](../../Validation/Trustworthy-ML-2023/concept_reconstruction.md) for the
model that these eight documents implement, and
[`source_coverage.md`](../../Validation/Trustworthy-ML-2023/source_coverage.md) for the audited source
universe.

A reader who did not read the book can execute any SOP here end to end.

The source attribution of this group is recorded in
[`SOURCE.md`](../../Validation/Trustworthy-ML-2023/SOURCE.md). That record also states what a reader
may and what a reader may not infer about licensing.

The group is a provenance-bearing staging unit. The rules of this group carry their own citations.
Later sources are expected to extend, revise, supersede or merge those rules. Those rules are not
expected to stay in this package forever. See the root README.

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
| SOP-01 | [Specify the deployment setting before training](SOP-01-specify-deployment-setting.md) | define | Core + Extended | BM-08, BM-09 |
| SOP-02 | [Build evaluation splits under leakage discipline](SOP-02-build-evaluation-splits-under-leakage-discipline.md) | freeze | Core + Extended | BM-01, BM-02, BM-08, BM-09 |
| SOP-03 | [Diagnose which evidence the model actually uses](SOP-03-diagnose-learned-evidence.md) | diagnose | Core + Extended | BM-02, BM-06 |
| SOP-04 | [Measure confidence truthfulness](SOP-04-measure-confidence-truthfulness.md) | measure | Core + Extended | BM-03, BM-04 |
| SOP-05 | [Run worst-case stress evaluation](SOP-05-run-worst-case-stress-evaluation.md) | stress | Core + Extended | BM-05, BM-09 |
| SOP-06 | [Choose a mitigation, or choose to abstain](SOP-06-choose-mitigation-or-abstain.md) | decide | Core + Extended | BM-01, BM-02, BM-03, BM-07 |
| SOP-07 | [Evaluate an explanation method before using it as evidence](SOP-07-evaluate-explanation-methods.md) | explain | Core + Extended | BM-06 |
| SOP-08 | [Report evidence and state validity boundaries](SOP-08-report-evidence-and-validity-boundaries.md) | report | Core + Extended | BM-08, BM-09 |

## How to use this group with the benchmarks

Each SOP states its links in §11. Each benchmark states its execution counterpart in §12. The
consolidated matrix lives in
[`acceptance_report.md`](../../Validation/Trustworthy-ML-2023/acceptance_report.md) and is the
cross-link check used at acceptance.

## Standing rules for this group

- **Core** is the minimum defensible procedure. **Extended** is required for high-stakes, published,
  or reused results. Do not fold optional methods into Core.
- Recurring terms take their meaning from the SOP-08 register. A local file may not redefine a
  metric name.
- Where one SOP depends on another SOP, link to the other SOP. Do not copy the procedure.
- **Integrity is setting-relative.** A method may use only the information rights that its declared
  setting grants. A method that takes more information than those rights grant changes the setting.
  That change also changes the comparison class for the results of that method. Nothing in this
  group forbids target-domain supervision as such. Nothing in this group licenses quoting a stricter
  setting's published results as the competition for a richer setting.
- Numbers quoted as examples come from the source, and each such number carries its section and page.
  The source's numeric values are **experimental regimes**, not general thresholds. Where a
  procedure repeats one of those values, that procedure names the experiment the value came from. No
  routing decision rests on that value.
- Every SOP retains book traceability for its book-derived rules. Later-source deltas are recorded
  in the relevant update audit rather than duplicated across every file.

## Scope note

The group is method-agnostic, application-neutral and **setting-neutral**. The group covers the
following as evaluation and execution practice:

- distribution shift
- adversarial stress
- uncertainty
- explanation evaluation

The group grants nothing and forbids nothing on its own.

Provided a project reports against the comparison class that its setting implies, that project may
declare one of the following as its setting:

- domain adaptation with labeled targets
- test-time training
- continual or few-shot adaptation
- target-informed calibration

The book catalogs those settings as first-class learning settings, not as violations. What the
procedures reject is a mismatch between the resources used and the setting named, not the use of
target information as such.

The group does not cover the authors' representation-learning showcase, nor their forward-looking
research agenda. The coverage audit records each item with its disposition.
