# BM-01 — Distribution-shift generalization

**Tier:** Core (one held-out domain) + Extended (multi-domain, severity, scale)
Metric names and their definitions come from the register in
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md) §4.

## 1. Target capability / failure mode

**Capability.** Performance retained when the evaluation data come from a domain the model was not
trained on — the cross-domain branch of the generalization-type axis, plus the subpopulation-shift
variant where the evaluation set is a minority slice of the training distribution.

**Failure mode under test.** Ill-defined behaviour off the training support: a model that reaches
training accuracy through cues that do not carry across domains, and a reported average that hides
the domain where it fails.

## 2. Evaluation hypothesis

The hypothesis a run tests is of the form: *method M retains task performance on domain d ∉
train-domains better than the baselines, under setting S and equal tuning budget.* A result supports
nothing unless the setting, the domain inventory, and the tuning budget are all fixed and reported.
The Core tier additionally tests the null hypothesis that a fairly tuned simple method is not worse
than M — historically the more common outcome.

## 3. Required data and split assumptions

- Domains identified by an explicit provenance label (capture device, style, site, time, sensor,
  population), assigned by
  [`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md).
- Class set shared across domains, so a domain change is not silently a task change.
- Training domains disjoint from evaluation domains at *group* level, per
  [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md).
- Validation drawn from training domains unless the declared setting grants target-domain
  information; if it does, this benchmark's regime changes and must be renamed (domain adaptation or
  test-time adaptation), and the comparison class with it.
- Contamination measured between every training/evaluation pair.
- Group sizes reported; a domain with too few samples to bound its error is reported as coverage-
  insufficient, not as a zero.

## 4. Shift or stress construction

**Core.** Leave-one-domain-out: hold out each declared domain in turn, train on the rest, evaluate
on the held-out one.

**Extended.** Add:
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
| Untuned plain training (default settings) | exposes the untuned-baseline artefact |
| **Fairly tuned** plain training with the same budget as the method | the reference a claimed gain must beat |
| Train-on-source-only lower reference and train-on-target upper reference (Extended) | brackets what is achievable, with the upper row labelled as an upper bound |
| Prior state-of-the-art method(s) from the same declared setting, same tuning budget | comparability class |
| Human or expert reference where the task admits it | anchors the metric in interpretable terms |
| Oracle model-selection row (Extended, when test-time selection is used) | must be marked as an upper bound, never merged into the average |

## 6. Primary metrics

- `acc_avg` over each held-out domain, and the mean across domains.
- `acc_worstgroup` over the declared cells (domains, and severity or subpopulation levels) —
  the first-class number for deployment decisions.
- Degradation relative to the ID cell: `acc_ID − acc_shift` per domain, which separates "the method
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

- Report every domain and every cell; the aggregate is *in addition to*, never instead of.
- Averaging across domains is permitted only when each domain's protocol is identical (same tuning
  rights, same supervision, same metric implementation).
- Provide variability: ≥3 seeds, or a bootstrap over evaluation samples where the cell is small;
  report the spread with the mean, and state which comparisons are within noise.
- Do not compare across scale regimes with the same aggregate row.
- Significance framing follows the source's own remedy for a moving evaluation set: prefer a
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

Report, per method: training overhead relative to plain training, evaluation cost (number of held-out
domains × seeds × severity levels), memory, and any extra supervision consumed (domain labels,
unbiased-sample fraction ρ). Cost is part of the result, not a footnote; a method that requires
per-domain tuning must state that budget in the comparison table.

## 11. Validity limits

- The benchmark measures transfer to *declared* domains. Unforeseen domains remain unmeasured; no
  score here licenses an open-world claim.
- Cross-bias dependence is out of scope for this artifact — a model can transfer across styles while
  relying entirely on a spurious cue; run `BM-02`.
- Adversarial worst case is out of scope; run `BM-05`.
- A leave-one-out protocol assumes domain identity is known and meaningful; when the real shift is
  within-domain drift, this design under-reports.
- Corruption benchmarks perturb the data-generating process, not the task semantics; they do not
  measure understanding.
- If the evaluation set has been widely used over a field's lifetime, part of any measured "gain" is
  community-level adaptation to it.

## 12. Related SOPs

Executed by [`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md) (domain
axes, comparison class) and [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md)
(split provenance, contact budget); interpreted by
[`SOP-06`](../../SOP/Trustworthy-ML-2023/SOP-06-choose-mitigation-or-abstain.md) and reported by
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md).

## 13. Source traceability

Cross-domain versus ID generalization and the domain/environment vocabulary: §2.1.2,
Definitions 2.5-2.8 (book pp. 18-19); learning settings §2.4.2-§2.4.7 (pp. 31-35). Leave-one-domain
protocol and the shared-class-set convention, plus the named benchmark family (PACS-style
leave-one-out, the DomainBed suite, and a mixed DG/subpopulation-shift suite): §2.6-§2.6.1
(pp. 40-43). Subpopulation-shift definition and worst-case-subpopulation requirement: §2.6,
Definition 2.26 (p. 40). Ill-defined behaviour off the training support: §2.7.1 (p. 44).
Tuning-rights parity, once-per-project test use, and benchmark refresh with significance testing:
§2.5.3 (pp. 39-40). Upper-bound rows for target-domain training and oracle selection: §2.12.2
(p. 65), §2.14.1 (p. 82). Worst-group versus average reporting: §2.12.1 (pp. 59-61). Second-version
evaluation-set drop as evidence of accumulated overfitting: §5.1.3 (p. 340). Fairly tuned simple
baseline, and the accuracy-without-cost reporting failure: §5.2.2 (pp. 341-343), §5.1.3 (p. 338).
Toy-versus-real regime properties: §5.2 (pp. 338-340). Corruption benchmark construction (many
corruptions applied to a held-out set) is described in §2.6.1 (p. 42). Severity curves, matrix
reporting and the tier split are repository conventions shaped by those sections.
