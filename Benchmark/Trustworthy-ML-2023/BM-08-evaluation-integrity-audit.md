# BM-08 — Evaluation integrity audit (a benchmark over benchmarks)

**Tier:** Core (protocol audit) + Extended (perturbation re-runs and public-result reconciliation)

## 1. Target capability / failure mode

**Capability.** Whether a reported comparison of methods is trustworthy at all — independent of which
capability the compared methods target. This artifact sits above `BM-01` … `BM-07`: it audits the
protocol rather than the model.

**Failure mode under test.** The documented failure family that wastes research effort: per-paper
metric implementations, confounded ingredients, hidden resources, train/test contamination, missing
validation sets, gaming by construction, unequal tuning budgets, and unmarked upper bounds. The cost
of getting this wrong is not a slightly off number but a false field-level trend, wasted effort on
non-problems, and practitioners mis-selecting methods.

## 2. Evaluation hypothesis

*Reported comparison R survives the audit: its conclusions still hold when leakage paths are closed,
implementations are shared, budgets are equalised, and controls are added.* The audit is falsified
when a conclusion flips under any of those corrections, or when a required disclosure is absent.

## 3. Required data and split assumptions

The audit consumes, and checks the existence of, the outputs of
[`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md) and
[`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md):

- setting block per compared method, with the supervision each consumed;
- split manifest with the declared independence unit, tuning rights, and contamination measurements,
  plus which recovery was taken for any set whose results guided a selection;
- test-contact log with the number of final-test evaluations;
- shared metric implementation (or the divergence list);
- tuning configuration and budget per method;
- cost accounting per method;
- the frozen evaluation copy or version hashes where the dataset is public.

An audit cannot be completed on missing inputs; "not documented" and "documented as absent" are
different audit results.

## 4. Shift or stress construction

Stress the *protocol*, not the model, and report which perturbations flip the conclusion:

1. **Shared-implementation swap**: recompute all metrics through one implementation, including
   degenerate cases (empty bins, zero-positive thresholds, ties).
2. **Budget equalisation**: give the simplest baseline the same search space and evaluation count as
   the method being promoted.
3. **Rights match**: re-run the selection steps under the information rights the claim's setting
   grants. Where practice exceeded the declared setting — target data used under a
   domain-generalization label — withhold them and record what survives. Where the setting genuinely
   grants target access, the data stay and the audit moves to whether the label and the comparison
   class match the resources used.
4. **Control insertion**: add the trivial controls (constant confidence frozen on the calibration
   split, random ordering, random occlusion, single-step attack) to every table. Where a control uses
   labels of the scored set — an oracle constant, an oracle detector — it is a metric diagnostic and
   must be marked as such, never promoted into the baseline column.
5. **Disclosure sweep**: hide one field at a time (bin count, ε and norm, occlusion operator, ρ
   direction, coverage) and check whether the claim remains interpretable.
6. **Second-version replication** of the evaluation set where the field permits it.
7. **Cross-regime probe**: repeat the Core comparison at a different data scale to test whether the
   ranking was regime-specific.

## 5. Required baselines

| Reference row | Role |
|---|---|
| The original reported numbers | what the audit is comparing against |
| Fairly tuned simplest admissible method | the "no real progress" reference the source documents repeatedly |
| Trivial controls per metric family | the gaming floor; an oracle control diagnoses a metric, it is not a baseline |
| A known-good re-evaluation from the literature, if one exists for this task area | external calibration of the audit itself |
| An unmodified-protocol rerun | isolates audit effects from run-to-run noise |

## 6. Primary metrics

- `audit_pass_rate` — audited requirements passed / requirements applicable, with the requirement
  list from §7 reproduced in the report.
- `conclusion_flip_count` — number of headline conclusions that change sign or significance under the
  step-4 perturbations.
- `disclosure_completeness` — fraction of the SOP-08 §6 checklist items present in the report.

## 7. Secondary / diagnostic metrics

Violation counts by class: leakage, contamination, budget inequality, missing control row, undisclosed
choice, unmarked upper bound, unreported cost. Effect size of each perturbation (how much the number
moved, not only whether it moved). Rank stability of the compared methods under shared
implementation and equal budget — the practical question a reader has.

## 8. Aggregation and uncertainty reporting

Report per requirement, per method, and per perturbation; do not aggregate a pass rate across
requirement classes of different severity. Where a violation cannot be quantified (documentation
absent), record it as unverifiable rather than as a pass or a failure. State the variability source
for re-computed numbers (implementation difference, seed, or both).

## 9. Failure interpretation

| Observation | Reading |
|---|---|
| Ranking changes under shared metric implementation | the field's numbers were partly an implementation artifact |
| Method loses its lead under equal tuning budget | the contribution was budget, not method |
| A conclusion requires target-domain information | setting mis-declared; reclassify and re-compare |
| Trivial control matches or beats the claim on a metric | the metric is gameable at that claim; change metric or claim |
| Second-version replication drops notably | accumulated benchmark overfitting, possibly field-wide |
| Cost undisclosed but plausibly large | the comparison is incomplete, not favorable |
| Requirement list not applicable in part | state which, and why — silent omission is the failure this artifact exists to catch |

## 10. Computational reporting

The audit itself has a cost: number of re-runs, evaluation-set contacts consumed, and metric
recomputation time. Report it, because "we did not check" is usually a budget statement in disguise.

## 11. Validity limits

- An audit establishes protocol integrity, not model quality: a clean comparison of two poor methods
  is still a poor result.
- Absence of a violation is bounded by the requirement list; new failure patterns appear as fields
  optimize against old audits (the source's own scandal list is a snapshot, not a closed set).
- Public results may be unreproducible for reasons invisible to the audit; where the audit cannot
  recompute, it records unverifiable.
- Second-version replication is available only where a field re-collects data.
- This artifact presumes the setting was declared in good faith; a deliberately vague setting block
  degrades it to a disclosure check.

## 12. Related SOPs

Audits the outputs of [`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md),
[`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md),
[`SOP-03`](../../SOP/Trustworthy-ML-2023/SOP-03-diagnose-learned-evidence.md) (cell support,
materiality threshold, occlusion operator),
[`SOP-04`](../../SOP/Trustworthy-ML-2023/SOP-04-measure-confidence-truthfulness.md),
[`SOP-05`](../../SOP/Trustworthy-ML-2023/SOP-05-run-worst-case-stress-evaluation.md),
[`SOP-06`](../../SOP/Trustworthy-ML-2023/SOP-06-choose-mitigation-or-abstain.md),
[`SOP-07`](../../SOP/Trustworthy-ML-2023/SOP-07-evaluate-explanation-methods.md) and
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md); applies
to every other benchmark in this group.

## 13. Source traceability

Purpose of evaluation as a ranking, and the obligation to explain an upper-bound violation:
§5.1.1 (p. 333). Costs of wrong evaluation, the metric-learning case, opportunity cost and
practitioner mis-selection, plus the eight-case scandal list: §5.1.2 (pp. 333-335). Failure recipes:
per-paper metric code and the undefined-precision corner case, confounded ingredients, hidden
resources and the accuracy-only plot, train/test overlap with the reported overlap rates and the
zero-accuracy non-overlapping subset, missing validation sets with ImageNet/CIFAR second-version
evidence, and the three practical pointers (find-or-write a fair comparison; trust only simple
ingredients; stay sceptical): §5.1.3 (pp. 335-338). Leakage forms and their remedies, ranking-only
exposure and the noised-accuracy idea: §2.5.1 (pp. 36-37), §2.5.3 (pp. 39-40). Test-set spoiling as
unavoidable-but-minimisable: §2.3.3 (p. 28). Ablation-study caveat for OOD claims: §2.5.2
(pp. 38-39). Equal-budget hyper-parameter practice and reading how papers choose hyper-parameters:
§2.12.2 (p. 64). Random search with a fixed shared budget: §5.2.3 (pp. 341-342). Fairly tuned simple
methods and the untuned-baseline/weight-decay example: §5.2.2 (pp. 339-341). Toy-versus-real regime
costs: §5.2 (pp. 338-340). Equal-ingredients-as-fairness and the information cap of a fixed
benchmark: §5.3.1 (p. 344), §5.3.5 (pp. 349-350). Metric gaming: the constant-confidence ECE
degeneracy — which the source notes needs only the prior probability of correctness, i.e. an oracle
quantity rather than a deployable baseline — §4.6.2 (pp. 256-257); the random-detector AUPR value for
the success-positive task, and AUPR-Error defined by swapping the positive class, §4.9.2
(pp. 265-266). Apparent robustness from broken gradients:
§2.15.12 (pp. 102-107). Explanation metrics distorted by the occlusion operator: §3.7.8
(pp. 187-188). Requirement lists, pass-rate scoring and the perturbation protocol are repository
conventions built on these sections.
