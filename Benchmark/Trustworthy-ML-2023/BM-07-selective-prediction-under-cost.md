# BM-07 — Selective prediction under cost

**Tier:** Core (risk-coverage curve) + Extended (cost-sensitivity, routing, drift re-check)

## 1. Target capability / failure mode

**Capability.** The system declines, defers, or escalates exactly where the system should do so. The
system answers where the system is right, and abstains where the system is not right. The abstention
rate is worth its cost.

**Failure mode under test.** The system delivers an answer where the system should not answer. That
failure is the practical consequence of two things. One is a confidence score that is not
trustworthy. The other is a threshold chosen by convention rather than by consequence.

## 2. Evaluation hypothesis

*Under cost table C, operating model M at threshold τ achieves expected cost no greater than the best
baseline's. That cost result holds at a coverage acceptable for the process.* Coverage without cost,
or cost without coverage, is not a claim this benchmark accepts. A secondary hypothesis: the ranking
quality measured by [`BM-04`](BM-04-error-and-anomaly-detection.md) is sufficient for the operating
point chosen. A system can rank perfectly and still mis-state the probability that a fixed threshold
implies.

## 3. Required data and split assumptions

- Attach the *cost table* to the labeled evaluation set: the cost of each wrong action, of each
  correct action, and of abstaining. The cost table is a stakeholder input, not a modeling choice.
  Record the source of the cost table and its uncertainty.
- Choose the threshold and any routing rule on validation material only, per
  [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md).
- State the review-capacity constraint: how many cases a human, or a fallback path, can handle per
  period.
- Check score comparability across the whole input stream, not only per-sample validity. Make that
  check when the decision is a competition between candidates (retrieval, detection pruning).

## 4. Shift or stress construction

- Sweep the abstention threshold across the full coverage range. Report the curve. Do not report one
  point alone.
- Re-run under each shift condition from
  [`BM-01`](BM-01-distribution-shift-generalization.md) and
  [`BM-02`](BM-02-spurious-cue-dependence.md): a threshold tuned on one distribution is an
  assumption about the next.
- Cost stress: vary the abstain-versus-error cost ratio around the nominal value. Report where the
  optimal operating point moves.
- Ambiguity stress: build subsets where several answers are legitimate. On such subsets the system
  should abstain, even though the model is not wrong about the world.
- Human-in-the-loop stress: replace abstention with an escalation. Then measure the end-to-end cost,
  including the review errors that the human makes.

## 5. Required baselines

| Baseline | Role |
|---|---|
| Always answer | the no-selection reference cost |
| Always abstain (where legal) | the trivial floor, cost of total refusal |
| Random abstention at matched coverage | isolates whether the score guides selection |
| Threshold on max-probability | default rule |
| Threshold on a recalibrated score | isolates calibration's contribution |
| Threshold on an alternative detector from `BM-04` | mechanism comparison |
| Oracle abstention (abstain on the cases actually wrong) | upper bound, labeled as such |
| Human-alone and human-plus-model | the real comparison for escalation policies |

## 6. Primary metrics

- `risk_at_coverage` — error rate among the accepted fraction, as a curve over coverage.
- Expected cost under the declared cost table at the chosen operating point.
- Coverage achieved at the tolerated risk (the dual reading of the same curve).

## 7. Secondary / diagnostic metrics

- Area under the risk-coverage curve as a single summary, reported with the curve.
- Abstention composition: what fraction of abstentions are ambiguous inputs, unfamiliar inputs, or
  genuinely hard-but-familiar inputs (cross-read with `BM-04`).
- `ece` at the accepted region only, since the operating region is what the decision-maker sees.
- Escalation quality: the agreement between model and human on the escalated subset, and the rate of
  human errors on the escalated subset.
- Worst-subgroup risk at the chosen coverage, per
  [`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md) §6.

## 8. Aggregation and uncertainty reporting

Report the full risk-coverage curve per condition and per subgroup. Mark the operating point on the
curve, and give its confidence interval (bootstrap over evaluation samples).

Averaged cost across subgroups is admissible only when the cost table is genuinely identical for every
subgroup. If the cost differs by class or population, report the per-group cost. Report the worst group
as well. State the coverage at which every risk number is quoted.

## 9. Failure interpretation

| Observation | Reading |
|---|---|
| Risk falls with abstention but only marginally better than random abstention | the score is not informative for selection, even if calibration looks acceptable |
| Operating point optimal for the nominal cost table moves sharply under cost stress | the decision rests on an unmeasured stakeholder assumption |
| Coverage high, worst-subgroup risk unbounded | average is buying aggregate performance with minority failures |
| Abstention concentrated on ambiguous inputs | correct behavior if the fallback is a human, wrong if it is a re-ask |
| Curve good on ID, collapses under shift | threshold is distribution-bound; schedule re-fitting as part of deployment |
| Human escalation raises total cost | the abstention rule works, the routing does not |

## 10. Computational reporting

Report score cost per prediction (from `BM-03`/`BM-04`), the review load implied by the chosen
coverage, and re-thresholding or re-fitting cost over the deployment lifetime. Abstention is not
free: an unpriced fallback path turns a good curve into a bad system.

## 11. Validity limits

- The benchmark is only as good as the cost table. With an unowned or guessed cost table, the
  operating point is a modeling artifact.
- A ranking-only claim licenses threshold filtering but not probability reporting. Do not present a
  risk-coverage result as evidence of calibration.
- The amount of the stream that the system can decline bounds the coverage. A process that must
  answer every input cannot use this artifact's conclusion directly.
- Deployment drift invalidates a fitted threshold. The reported operating point is conditioned on the
  evaluated distribution.
- Ambiguity handled by abstention is not the same as ambiguity resolved by returning a set of answers,
  or by a request for better input. This benchmark measures only the first kind.

## 12. Related SOPs

- Execution: the abstention branch of
  [`SOP-06`](../../SOP/Trustworthy-ML-2023/SOP-06-choose-mitigation-or-abstain.md), on the cost
  statement registered by
  [`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md).
- Scores: [`SOP-04`](../../SOP/Trustworthy-ML-2023/SOP-04-measure-confidence-truthfulness.md).
- Detection mechanisms: [`BM-04`](BM-04-error-and-anomaly-detection.md).
- Audit: [`BM-08`](BM-08-evaluation-integrity-audit.md).
- Reporting: [`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md).

## 13. Source traceability

The source anchors for this benchmark are:

- The two-output contract, prediction plus uncertainty, and the contract's consumers: §4.1.2
  (pp. 222-223).
- Human intervention only when confidence is low: §4.1.2 (pp. 222-223).
- The rule to act only when confident, and otherwise to stop, or to fall back to a safe state:
  §4.1.2 (pp. 222-223).
- Worked cost table where abstention is cheaper than the asymmetric error, and the
  threshold-on-reported-confidence acceptance rule: §4.1.3 (pp. 223-225).
- A further request to the user for a better photo, and the return of several candidate results as
  alternative responses: §4.1.3 (p. 224).
- Open-set regimes with and without an explicit "I don't know" output, and the stated disadvantage of
  the unsupervised variant: §4.1.3 (pp. 225-226).
- Active learning as uncertainty-driven sample selection, and comparable scores across candidates for
  proposal pruning: §4.1.3 (pp. 226-228).
- Ranking condition being sufficient for threshold filtering: §4.9.1 (pp. 263-264).
- Detection-metric definitions used for the curves: §4.9.2 (pp. 264-266).
- Calibration under shift and recalibration cost: §4.8.1-§4.8.3 (pp. 259-263).
- Test-time selection from a small labeled deployment sample, and its oracle-selection caveat: §2.14
  (pp. 75-77), §2.14.1 (p. 82).
- Retraining/model-selection cadence as the standard response to drift: §2.2.1 (pp. 20-24),
  Definitions 2.9-2.11.
- Worst-group reporting obligation: §2.12.1 (pp. 59-61).

Cost table ownership, curve-only reporting and the tiering are repository conventions.
