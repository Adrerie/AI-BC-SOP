# BM-03 — Confidence truthfulness

**Tier:** Core (battery + controls) + Extended (subgroup, sensitivity, mechanism comparison)

## 1. Target capability / failure mode

**Capability.** The reported score `c(x)` behaves as the probability it is claimed to be — either as
a calibrated conditional accuracy, or as a faithful probability of correctness, or at minimum as a
correct ordering of cases by likelihood of being right.

**Failure mode under test.** Confident wrongness that no metric detects, and the more subtle
failure where the metric is satisfied while the property is absent (a gameable score), including a
model that overfits its likelihood while its classification error keeps improving.

## 2. Evaluation hypothesis

Three separate hypotheses, and a run must say which one it addresses:

- **H-probability** — training with a strictly proper scoring rule drives `c(x)` toward
  `P(L = 1 | x)`; tested by proper-score comparison against controls.
- **H-calibration** — `P(Ŷ = Y | C = c) = c` holds within tolerance; tested by `ece`/`mce`, which is
  a *necessary*, not sufficient, condition of H-probability.
- **H-ranking** — higher `c` on correct than on incorrect cases; equivalent to calibration up to an
  unknown monotone map, and the weakest claim available.

A fourth, easily confused hypothesis: *the score reflects a named uncertainty source* — that belongs
to [`BM-04`](BM-04-error-and-anomaly-detection.md), not here.

## 3. Required data and split assumptions

- A labelled evaluation set frozen per
  [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md),
  plus a **separate calibration split** if any post-hoc map is fitted; fitting a temperature on the
  reported test set invalidates the benchmark.
- Per-sample outputs: predicted class, score `c(x)` ∈ [0,1] (or a monotone scalar), and correctness
  indicator `L`.
- The declared quantity: predictive, aleatoric, or epistemic.
- Slices defined in advance: class, group, difficulty, and (Extended) an ambiguity-rich subset where
  multiple answers are legitimate, since that is where aleatoric and epistemic claims separate.
- Sample counts per confidence bin reported, because bin-weight noise dominates the metric at the
  high-confidence end.

## 4. Shift or stress construction

- Evaluate the battery separately on ID and on each shifted subset from
  [`BM-01`](BM-01-distribution-shift-generalization.md) and
  [`BM-02`](BM-02-spurious-cue-dependence.md): calibration is a property of a distribution, not of a
  model.
- Imbalance stress: at least one subset with positive rate far from one half, to expose AUPR
  inflation (a random detector's `aupr` equals `P(L = 1)` there).
- Ambiguity stress: samples with several acceptable labels, where a truthful predictive score must
  stay high while a claimed epistemic score must not.
- Overfitting stress: compare checkpoints by training epoch where available, since probabilistic
  overfitting can appear while classification error improves.
- Binning stress (`ece` at several bin counts and both equal-width and equal-mass binning).

## 5. Required baselines

| Baseline | Why required |
|---|---|
| **Constant confidence** equal to global accuracy | reaches `ece` = 0 with no per-sample information; the gaming reference |
| Uniform random scores | the reference for ranking metrics |
| Uncalibrated softmax/max-prob of the same model | isolates the contribution of any calibration step |
| Temperature-scaled version, fitted on the calibration split | the cheap fix that must be reported, not assumed |
| Trivial per-class priors | prevents reading prior knowledge as calibration |
| Alternative score mechanism on the same model (entropy, margin, distance-based, ensemble disagreement) | separates "better estimator" from "better model" |

## 6. Primary metrics

- `nll` and `brier` (multi-class variant where applicable) — proper scores.
- `ece` with the binning disclosed; `mce` for worst-bin risk.
- `auroc` as the ranking headline, with `aupr_success` / `aupr_error` reported alongside.

## 7. Secondary / diagnostic metrics

- `reliability` diagram **with the confidence histogram** — the diagram alone cannot recover `ece`
  and can mislead about which bins matter.
- Per-class and per-group `ece`/`mce` (worst-class variant for high-risk claims).
- Bin-sensitivity spread of `ece`.
- Residual-variance check for heteroscedastic regression scores: predicted spread bins versus
  empirical squared-error bins.
- Decomposition note: task accuracy next to every confidence metric, since proper scores mix accuracy
  and calibration and have no knowable floor (the irreducible aleatoric term is unknown).

## 8. Aggregation and uncertainty reporting

Report the battery per subset and per slice; never a single scalar "calibration" number for a model
evaluated on several distributions. Give bin counts, seed/run variability, and the sample count
behind each bin-average. When comparing two methods, state the binning used for both — differing
bin counts make the comparison meaningless. Where a metric's floor is unknown (`nll`, `brier`),
compare against a control row rather than interpreting the absolute value.

## 9. Failure interpretation

| Observation | Reading |
|---|---|
| `ece` ≈ 0 but constant-confidence control also ≈ 0 | calibration claim is empty; check ranking and proper scores |
| Better `nll` while accuracy also improves | not evidence about uncertainty alone |
| `auroc` high, `ece` high | good ranking, bad probability: acceptable for a threshold filter, unacceptable as a reported probability |
| `aupr` high on an imbalanced subset | may be the base rate; read against `P(L = 1)` and prefer `auroc` |
| Worst-bin (`mce`) large while `ece` small | a rare but badly mis-stated confidence region; high-risk use fails |
| Calibration degrades under shift while accuracy holds | confidence is distribution-bound; re-fit and disclose, do not silently transfer |
| Distance-based score "detects" ambiguity as unfamiliarity | mechanism conflation; route to `BM-04` interpretation |

## 10. Computational reporting

Record the cost of producing the score: passes per prediction for an ensemble or a Monte-Carlo
mechanism, storage for stored checkpoints, statistics needed for a distance score, and the
calibration-fitting cost. A calibration gain that multiplies inference cost must be reported as a
trade-off, not as a free improvement.

## 11. Validity limits

- Calibration is not truthfulness: per-sample `c(x) = P(L = 1 | x)` can fail arbitrarily while group
  calibration holds.
- Proper scores bound behaviour in expectation over the data distribution; they say nothing about
  epistemic uncertainty, whose Bayes-predictor value is zero.
- A strictly proper score for the predictive (max-prob) target is guaranteed to also be strictly
  proper for recovering the true conditional distribution in the **binary** case; beyond binary the
  converse fails, and matched argmax values can hide a wrong distribution. Do not carry the binary
  equivalence across without checking.
- Estimator-level guarantees (posterior families, priors, intractable verification) are assumptions
  inherited from the mechanism, not properties measured here.
- No numeric default for "well calibrated" is available from the source; thresholds are a deployment
  decision that this benchmark requires you to state, not invent.

## 12. Related SOPs

Executed by [`SOP-04`](../../SOP/Trustworthy-ML-2023/SOP-04-measure-confidence-truthfulness.md);
splits from [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md);
threshold consequences read by
[`SOP-06`](../../SOP/Trustworthy-ML-2023/SOP-06-choose-mitigation-or-abstain.md) and
[`BM-07`](BM-07-selective-prediction-under-cost.md); reported through
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md).

## 13. Source traceability

Predictive uncertainty as `c(x) = P(L = 1)`: §4.2.1, Definition 4.1 (p. 228). Formats of
uncertainty (scalar, per-evidence vector, distribution over embeddings, disentangled pair): §4.4
(pp. 240-242). Proper scoring definition and instances: §4.5.1-§4.5.3, Definition 4.8 (pp. 243-246);
BCE/max-prob §4.5.5, Definition 4.9 (pp. 246-247); CE lower bound §4.5.6 (p. 248); "not all strictly
proper rules are equally good objectives" §4.5.7 (p. 252); multi-class Brier §4.5.8 (pp. 251-252);
test-set evaluation, perplexity reading and the four caveats §4.5.9 (pp. 253-254). Calibration
definitions and recipes: §4.6.1, Definitions 4.11-4.13 with the 5-step ECE procedure (pp. 254-256);
MCE and per-class worst case §4.6.2 (p. 256); gaming ECE with a constant prediction §4.6.2
(pp. 257-258); bin-count sensitivity and fine bins at high confidence §4.6.2 (p. 258); reliability
diagrams, their relation to ECE/MCE and the binary-axis pitfall §4.6.3 (pp. 259-261); tool summary
§4.7 (p. 261). Probabilistic overfitting while accuracy improves: §4.8.1 (pp. 261-263).
Architecture-family dependence and recalibration status: §4.8.2 (pp. 263-264). Temperature scaling
protocol and fitted-on-validation rule: §4.8.3 (pp. 264-265). Ranking condition and its sufficiency
for threshold filtering: §4.9.1 (pp. 265-266). Detection metrics, AUPR-at-base-rate and the AUROC
recommendation: §4.9.2 (pp. 266-268). Aleatoric/predictive scoring equivalence and its binary-case
limit: §4.13.3 (pp. 303-305); heteroscedastic NLL recommendation and preconditions §4.13.5
(pp. 307-308). Ensemble-score improvement confounded by accuracy: §4.11.5 (p. 275). Distance-score
conflation of ambiguity and OOD: §4.12.1-§4.12.2 (pp. 291-296). Controls, tiers and the table of
interpretations are repository conventions.
