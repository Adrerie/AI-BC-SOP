# BM-01 — Distribution-shift generalization

**Tier:** Core (one held-out domain) + Extended (multi-domain, severity, scale)
Metric names and their definitions come from the register in
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md) §4.

## 1. Target capability / failure mode

**Capability.** The capability is performance retained when the evaluation data come from a domain
the model was not trained on. The benchmark tests the cross-domain branch of the
generalization-type axis. The benchmark also tests the subpopulation-shift variant, where the
evaluation set is a minority slice of the training distribution.

**Failure mode under test.** The failure mode is ill-defined behavior off the training support. A
model can reach training accuracy through cues that do not carry across domains. A reported average
can hide the domain where the model fails.

## 2. Evaluation hypothesis

A run tests a hypothesis in one declared form:

*method M retains task performance on domain d ∉ train-domains better than the baselines, under
setting S and equal tuning budget.*

A result supports nothing unless the setting, the domain inventory and the tuning budget are all
fixed and reported. Historically, the more common outcome is that a fairly tuned simple method is
not worse than M. The Core tier therefore tests that null hypothesis as well.

## 3. Required data and split assumptions

- Domains identified by an explicit provenance label (capture device, style, site, time, sensor,
  population), assigned by
  [`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md).
- Class set shared across domains, so a domain change is not silently a task change.
- Training domains disjoint from evaluation domains at *group* level, per
  [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md).
- Draw validation from the training domains, unless the declared setting grants target-domain
  information. When the setting grants that information, the regime of this benchmark changes.
  Rename the regime as domain adaptation or test-time adaptation, and rename the comparison class
  with the regime.
- Contamination measured between every training/evaluation pair.
- Report the group sizes. Report a domain with too few samples to bound the error of that domain as
  coverage-insufficient, not as a zero.

## 4. Shift or stress construction

**Core.** Use the leave-one-domain-out construction. Hold out each declared domain in turn. Train on
the remaining domains, and evaluate on the held-out domain. Leave-one-domain-out is the construction
for a setting that withholds the target domain.

A project may instead declare domain adaptation, test-time training, or continual/few-shot
adaptation. Such a project does not fail the check. The project reports a different comparison class.
Per [`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md), this benchmark
scores the project under its own setting label against methods granted the same access.

**Extended.** The extended tier adds constructions to the Core:
- *multi-source*: train on a subset of domains, evaluate on several unseen ones at once.
- *severity ladder*: corruptions or style changes at ≥3 levels, reported as a curve rather than a
  point, to expose cliffs rather than averages.
- *worst-case slice*: the subpopulation-shift construction, where evaluation cells are minorities of
  the training distribution.
- *second-version replication*: re-collect an evaluation set from the same claimed distribution with
  an independent collection procedure, to measure accumulated benchmark overfitting.
- *scale replication*: repeat the Core at a larger regime (order-of-magnitude more samples and
  dimensions) to test whether the method survives the step from controlled to realistic data.
Never construct a shift by peeking at the held-out domain's labels.

## 5. Required baselines

| Baseline | Why required |
|---|---|
| Untuned plain training (default settings) | exposes the untuned-baseline artifact |
| **Fairly tuned** plain training with the same budget as the method | the reference a claimed gain must beat |
| Train-on-source-only lower reference and train-on-target upper reference (Extended) | brackets what is achievable, with the upper row labeled as an upper bound |
| Prior state-of-the-art method(s) from the same declared setting, same tuning budget | comparability class |
| Human or expert reference where the task admits it | anchors the metric in interpretable terms |
| Oracle model-selection row (Extended, when test-time selection is used) | must be marked as an upper bound, never merged into the average |

## 6. Primary metrics

- `acc_avg` over each held-out domain, and the mean across domains.
- `acc_worstgroup` over the declared cells (domains, and severity or subpopulation levels) —
  the first-class number for deployment decisions.
- Degradation relative to the ID cell: `Acc(ID) − Acc(shifted domain)` per domain, which separates "the method
  is good" from "the method transfers".

## 7. Secondary / diagnostic metrics

- Per-cell accuracy matrix (domain × class), to see whether the failure is broad or concentrated.
- Calibration under shift (`ece`, `mce`, `reliability`) via
  [`BM-03`](BM-03-confidence-truthfulness.md): a shift often leaves accuracy intact while confidence
  becomes fiction, or the reverse.
- Error-detection quality under shift (`auroc`) via
  [`BM-04`](BM-04-error-and-anomaly-detection.md).
- Dependence verdict from [`BM-02`](BM-02-spurious-cue-dependence.md) before and after the shift.
- Coverage counts per cell, so a tiny-cell result is read with its noise.

## 8. Aggregation and uncertainty reporting

- Report every domain and every cell. The aggregate is *in addition to* those rows, never instead of
  those rows.
- Averaging across domains is permitted only when each domain's protocol is identical (same tuning
  rights, same supervision, same metric implementation).
- Provide variability over ≥3 seeds. Where a cell is small, a bootstrap over the evaluation samples
  of that cell is acceptable instead. Report the spread with the mean, and state which comparisons
  are within noise.
- Do not compare across scale regimes with the same aggregate row.
- The source's own remedy for a moving evaluation set frames the significance question. Prefer a
  statistical test over the assumption that two runs saw the same samples.

## 9. Failure interpretation

| Observation | Reading | Next check |
|---|---|---|
| Method beats fairly tuned plain training only on average, not worst cell | trade-off, not progress | `acc_worstgroup`, per-cell matrix |
| Gain disappears when the tuning budget is equalised | the gain was tuning | baseline parity in `BM-08` |
| Second-version replication drops notably | accumulated benchmark overfitting | refresh policy, contact log |
| Confidence stays high while accuracy collapses | no failure detection | `BM-03`, `BM-04` |
| Gain requires target-domain information | different setting | re-declare per SOP-02 §7 |
| Only the controlled/small-scale regime works | scale fragility | Extended scale replication |

## 10. Computational reporting

Report the cost per method. State the training overhead relative to plain training. State the
evaluation cost (number of held-out domains × seeds × severity levels), the memory, and any extra
supervision consumed (domain labels, unbiased-sample fraction ρ). Cost is part of the result, not a
footnote. A method that requires per-domain tuning must state that tuning budget in the comparison
table.

## 11. Validity limits

- The benchmark measures transfer to *declared* domains. Unforeseen domains remain unmeasured. No
  score on this benchmark licenses an open-world claim.
- Cross-bias dependence is out of scope for this artifact. A model can transfer across styles while
  relying entirely on a spurious cue. Run `BM-02`.
- Adversarial worst case is out of scope. Run `BM-05`.
- A leave-one-out protocol assumes that each domain carries a known and meaningful identity. When
  the real shift is within-domain drift, the leave-one-out design under-reports.
- Corruption benchmarks perturb the data-generating process, not the task semantics. A corruption
  benchmark does not measure understanding.
- The source treats a long-lived evaluation set as a confound. Where a field uses one evaluation set
  widely across its lifetime, part of any measured "gain" is community-level adaptation to that set.

## 12. Related SOPs

- [`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md) and
  [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md)
  execute this benchmark (`SOP-01`: domain axes and comparison class; `SOP-02`: split provenance and
  contact budget).
- [`SOP-06`](../../SOP/Trustworthy-ML-2023/SOP-06-choose-mitigation-or-abstain.md) interprets the
  result, and
  [`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md) carries
  the reporting.
- [`SOP-03`](../../SOP/Trustworthy-ML-2023/SOP-03-diagnose-learned-evidence.md) attributes the
  failure to a specific cue.
- [`BM-05`](BM-05-adversarial-robustness.md) measures the adversarial branch of the same condition
  axis, under [`SOP-05`](../../SOP/Trustworthy-ML-2023/SOP-05-run-worst-case-stress-evaluation.md).

## 13. Source traceability

- Cross-domain versus ID generalization, and the domain/environment vocabulary: §2.1.2,
  Definitions 2.5-2.8 (book pp. 18-19).
- Learning settings: §2.4.2-§2.4.11 (pp. 29-35). The same list is also the list of legitimate
  alternative settings for the clause in §4.
- Leave-one-domain protocol and the shared-class-set convention, plus the named benchmark family:
  §2.6-§2.6.1 (pp. 40-43). The family is PACS-style leave-one-out, the DomainBed suite, and a mixed
  DG/subpopulation-shift suite.
- Subpopulation-shift definition and worst-case-subpopulation requirement: §2.6,
  Definition 2.26 (p. 40).
- Ill-defined behavior off the training support: §2.7.1 (p. 44).
- Tuning-rights parity, once-per-project test use, and benchmark refresh with significance testing:
  §2.5.3 (pp. 39-40).
- Upper-bound rows for target-domain training and oracle selection: §2.12.2 (p. 65), §2.14.1 (p. 82).
- Worst-group versus average reporting: §2.12.1 (pp. 59-61).
- Second-version evaluation-set drop as evidence of accumulated overfitting: §5.1.3 (pp. 335-338).
- Fairly tuned simple baseline, and the accuracy-without-cost reporting failure: §5.2.2 (pp. 335-341),
  §5.1.3 (p. 338).
- Toy-versus-real regime properties: §5.2 (pp. 338-340).
- Corruption benchmark construction (many corruptions applied to a held-out set) is described in
  §2.6.1 (p. 42).
- Severity curves, matrix reporting and the tier split are repository conventions shaped by those
  sections.
