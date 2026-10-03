# SOP-04 — Measure confidence truthfulness

**Stage:** measure · **Tier:** Core + Extended · **Concepts:** C7 contracts, C8 quantity separation,
C9 proxy gap, C10 gaming, C12 guarantee type

## 1. Purpose

Decide which property a reported confidence number should have. Measure the property with the only
instruments sensitive to the property. Prove that the number does not come from an artifact of the
metric. Confidence is where trustworthy-ML claims are most often won cheaply and lost honestly.

## 2. When to use

- Whenever the model emits a score that a human or a threshold uses. Such scores include
  "objectness", retrieval similarity, anomaly flags, or an LLM's log-likelihood.
- Before you claim calibrated uncertainty, well-ranked errors, or usable epistemic uncertainty.
- When you compare two confidence-estimation methods.
- After any intervention that could change confidence without changing decisions
  (recalibration, distillation, temperature scaling, capacity changes, longer training).

## 3. Inputs / prerequisites

- Frozen predictions on a labeled evaluation set.
  [`SOP-02`](SOP-02-build-evaluation-splits-under-leakage-discipline.md) designates that evaluation
  set. Include the per-sample score `c(x)` and the correctness indicator `L = 1[ŷ = y]` with those
  predictions.
- A separate calibration set, if you plan any post-hoc recalibration. Never use the final test set
  as that calibration set.
- The declared quantity: predictive, aleatoric, or epistemic (§4).
- For epistemic claims: an OOD/multiplicity construction, or an ensemble/distribution-parameter
  mechanism whose assumptions you can state.

## 4. Definitions needed for execution

- **Predictive uncertainty** — `c(x) = P(L = 1)`, the probability that this prediction is correct.
  Confidence and uncertainty are used interchangeably here with `confidence = 1 − uncertainty`.
- **Aleatoric uncertainty** — entropy/variance of the true `P(Y | X = x)`. More data does not
  reduce aleatoric uncertainty.
- **Epistemic uncertainty** — multiplicity of plausible models given the data. Supervision in
  underexplored regions of the data manifold reduces epistemic uncertainty.
- **Strictly proper scoring rule** — a score whose unique expected maximiser is the true
  distribution. That property is the mechanism by which training with such a loss *encourages*
  truthful `c(x)`.
- **Perfect calibration** — `P(Ŷ = Y | C = c) = c` for all `c`. That condition is necessary for
  `c(x) = P(L = 1)`, but not sufficient.
- **Ranking condition ("weak calibration")** — order preservation: higher `c` on correct than on
  incorrect cases. The ranking condition is equivalent to calibration up to an unknown monotone map.
- **Contracts**, therefore, are three and not interchangeable:

  - *proper scoring* (probability fidelity)
  - *calibration* (conditional accuracy)
  - *ranking* (order)

## 5. Procedure

**Core**

1. Name the quantity you claim (§4). If you cannot name the quantity, you report a score, not an
   uncertainty.
2. Pick the contract that the downstream use requires:

   - A numeric probability is consumed. Use proper scoring **and** calibration.
   - Only a threshold filter is applied. Ranking suffices, and say so in the report.
   - Worst-bin behavior matters (high-risk). Add the worst-case calibration view.

3. Compute the metric battery on the frozen predictions:

   - **Proper scores**: report NLL/CE, Brier (binary), and multi-class Brier. Use perplexity only for
     language modeling, where perplexity is the exponentiated NLL. Write the value as `exp(nll)` when
     the loss used natural logarithms. Write the value as `2^(nll)` when `nll` uses log base 2. The
     two bases must match. The value is invariant to a *common* base choice, but not to mixing the
     bases.
   - **Calibration**: bin the confidences. Compute the accuracy and the mean confidence in each bin.
     Report ECE (bin-weighted mean absolute gap), MCE (worst-bin gap), and the reliability diagram.
   - **Ranking**: report AUROC plus both correctness AUPR specializations. For `aupr_success`, set
     positive = `L = 1` and rank by confidence `c`. For `aupr_error`, set positive = `L = 0` and rank
     by `1 − c`. An explicitly equivalent score that increases with error likelihood is also
     acceptable. Both variants use the package's non-interpolated Average Precision definition. Read
     each variant against the prevalence of its own positive class.

4. Run the **trivial-score controls** as first-class rows in the same table. A claim is measured
   against those controls, not against zero:

   - A constant confidence, in two forms. The *deployable* form takes a value frozen on the
     calibration split before final testing. The *oracle* form takes the measured correctness rate of
     the set being scored. The oracle form is a metric diagnostic. Label the oracle form as a
     diagnostic, and do not ship the oracle form as a baseline.
   - Uniformly random scores.
   - The uncalibrated softmax baseline of the same model.

5. Decompose the result before you compare two methods. Report task accuracy next to every confidence
   metric. Do not read an improvement in NLL/Brier as an improvement in uncertainty alone. Proper
   scores mix accuracy and calibration.
6. If you apply recalibration, fit the temperature (or other map) on the calibration split only.
   Report the fitted value. Re-run the whole battery after the change. State the number of bins you
   used.

**Extended** — add for high-stakes claims, or when epistemic/aleatoric quality is asserted:

7. For subgroup calibration, repeat ECE/MCE per class, per declared subgroup, and per difficulty
   slice. Report the worst subgroup as a headline-adjacent number.
8. For bin sensitivity, recompute ECE over a range of bin counts. Use at minimum the bin count you
   report, plus one coarser setting and one finer setting. Report the spread of ECE across those
   counts. Consider finer bins in the high-confidence region, where modern models concentrate.
9. Separate the proxies behind an epistemic claim. Evaluate the score as an OOD detector
   (label = inside vs outside the training distribution), *and* re-evaluate the score as a
   multiplicity detector (label = several acceptable answers). Report both readouts. Do not present
   either readout as the other.
10. For an aleatoric check on regression, fit the heteroscedastic Gaussian NLL
    `(1/2σ̂²)‖y − µ̂‖² + (d/2)log σ̂²`. Verify the fitted spread against empirical residual variance in
    bins of predicted spread. The balancing term is what stops "everything is hard".
11. Record the confounds of the score mechanism. A score may come from a feature distance or from a
    centroid kernel. For that kind of score, record that high aleatoric ambiguity can also raise the
    score. A score may instead come from an ensemble. For an ensemble, record that its spread still
    contains aleatoric uncertainty. Record also that its implicit prior is the initialisation scheme.
12. Log the estimator cost. Record the overhead of training and inference for the uncertainty
    mechanism, next to that mechanism's metric gain (see `SOP-08` §10).

## 6. Mandatory checks

- [ ] **Gaming check**: does the reported number beat the *deployable* constant-confidence control?
      A model reaches ECE = 0 by predicting a constant equal to the measured correctness rate of the
      set the model is scored on. The source points out that this construction needs no labeled
      validation set, only the prior probability of correctness. That prior probability is itself
      computed from the labels of that set. The construction is therefore an oracle diagnostic, not a
      baseline a deployed model can hold. That diagnostic exposes a weakness of ECE. A frozen constant
      from the calibration split is the legitimate reference row. The final-set ECE of that frozen
      constant is the gap between the frozen value and the final accuracy. If the trivial control
      matches the claim, the claim is empty.
- [ ] **Quantity-to-instrument check**: an epistemic claim must not rest on proper scores alone. The
      Bayes predictor maximizes the proper scores with zero epistemic uncertainty.
- [ ] **Split-rights check**: no calibration parameter was fitted on a final-test subset.
- [ ] **Bin disclosure**: state the bin count, and state whether the bins are equal-width or
      equal-mass. State both wherever ECE/MCE appears.
- [ ] **Imbalance check**: read each AUPR variant against the prevalence of *its own* positive class.
      The Success variant uses `P(L = 1)`, and the Error variant uses `P(L = 0)`. That prevalence is
      the random detector's value for that task. AUROC sits at 0.5 whatever the balance is. AUROC
      therefore stays the headline when a positive rate is far from one half. State which class is
      positive wherever an AUPR appears.
- [ ] **Coverage check for threshold claims**: a ranking claim states the coverage at which the
      decision is taken.
- [ ] **Capacity check**: report accuracy changes and calibration changes separately after any longer
      training, distillation, or capacity change. Overfitting can appear as probabilistic error while
      the classification error keeps improving.

## 7. Decision or stop conditions

- **Stop: do not report a calibration number** if the binning choice flips the ordering of the
  compared methods. Report the sensitivity instead of a single value.
- **Stop and change the claim** from "calibrated" to "well-ranked" if only the ranking condition
  holds. The converse substitution is not permitted.
- **Stop** if you cannot state the assumptions of the confidence mechanism (posterior family, prior,
  independence of the distance measure from ambiguity). An unstated assumption is an unbounded claim.
- **Escalate to Extended** whenever a human or an automatic action consumes the score directly.
- **Stop and re-report by position** if the inputs are turns of one interaction rather than draws
  from a named distribution. The set of answers that a turn can legitimately take narrows as the
  history grows. That is why a calibration or ranking figure computed by pooling turns across a
  session is not a figure about any single turn. A score that samples the model several times per
  turn must state that count wherever the report quotes the score.
- **Accept and record a negative result** if no mechanism beats the trivial control at the stated
  coverage. The correct output is "we cannot yet quantify confidence here", not a weaker metric.

## 8. Common methodological failures

- You report ECE as if ECE measured the truthfulness of `c(x)` per sample.
- You reach ECE = 0 with an oracle constant, and you present that constant as a calibration
  achievement.
- You compare an error-positive detector against the success-positive prevalence, or you quote one
  baseline for both AUPR variants.
- You silently choose a bin count that flatters the result.
- You read lower NLL across model scales as better uncertainty rather than as better fit.
- You use OOD detection accuracy as a definition of epistemic uncertainty.
- You attribute low confidence to "the model knows it does not know". The score may instead be a
  distance in feature space, and the sample may be merely ambiguous.
- You fit temperature scaling on the test set, and you report the test ECE afterwards.
- You claim a decomposition into aleatoric plus epistemic as though the decomposition were exact.
- You treat MC-style sampling noise as free. Report how many samples/backward passes produced the
  score.

## 9. Required outputs

- The metric battery table, reported per subset: accuracy, NLL, Brier, ECE (bins disclosed), MCE,
  AUROC, AUPR-Success and AUPR-Error. For each AUPR variant, name its positive class and its own
  no-skill value. Include the trivial-control rows, and flag the oracle constant as a diagnostic
  rather than as a baseline.
- Reliability diagram with the confidence histogram.
- Bin-sensitivity and subgroup slices (Extended).
- Calibration-parameter record: the value, the split used for the fit, and the search range.
- A one-line statement of which contract the claim uses and which quantity the claim is about.

## 10. Minimum reporting requirements

Every confidence number must travel with the items below:

- the quantity claimed
- the contract used
- the binning
- the trivial-control comparison
- task accuracy
- the split used for any fitted map
- the cost of producing the score

A comparison of two confidence methods is invalid if those items differ between the two methods.

## 11. Links to relevant Benchmarks

- [`BM-03`](../../Benchmark/Trustworthy-ML-2023/BM-03-confidence-truthfulness.md) — the standardized
  battery, controls and tiers.
- [`BM-04`](../../Benchmark/Trustworthy-ML-2023/BM-04-error-and-anomaly-detection.md) — the
  detection-style readout of the same scores.
- [`BM-07`](../../Benchmark/Trustworthy-ML-2023/BM-07-selective-prediction-under-cost.md) — where a
  ranking-only claim becomes an operating point.
- [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md) — the
  gaming/split-rights audit.

## 12. Source traceability

- Quantity definitions: §4.2.1-§4.2.4, Definitions 4.1-4.7 (pp. 228-238), including the caution that
  the decomposition requires assumptions and remains open.
- Score formats: §4.4 (pp. 240-242).
- Proper scoring: §4.5.1, Definition 4.8 (p. 243).
- Log-probability and Brier claims and proofs: §4.5.2-§4.5.3 (pp. 245-246).
- BCE/max-prob §4.5.5, Definition 4.9 (pp. 246-247).
- CE as a lower bound: §4.5.6 (p. 248).
- Multi-class Brier: §4.5.8 (pp. 250-251).
- The caution "not all strictly proper rules are equally good objectives": §4.5.7 (pp. 249-250).
- Perplexity as the exponentiated NLL, using base 2 in both the logarithm and the exponential:
  §4.5.9 (p. 252).
- The footnote that the value is independent of the *common* base: §4.5.9 (p. 252).
- Evaluation on the test set and the four interpretation caveats: §4.5.9 (pp. 253-254).
- Calibration: §4.6.1, Definitions 4.11-4.15 with the 5-step ECE recipe and MCE (pp. 254-257).
- Gaming ECE with a constant equal to the global accuracy: §4.6.2 (pp. 256-257).
- The remark that only the prior probability of correctness is needed: §4.6.2 (pp. 256-257).
- Bin-count dependence and the fine-bins suggestion: §4.6.2 (pp. 256-257).
- Reliability diagrams and their limits: §4.6.3 (p. 259).
- The tool summary: §4.7 (p. 259).
- DNN calibration evidence and the NLL/accuracy disconnect: §4.8.1-§4.8.2 (pp. 259-262).
- Temperature scaling protocol: §4.8.3 (pp. 262-263).
- Ranking condition and detection metrics with the AUROC-over-AUPR recommendation:
  §4.9.1-§4.9.2 (pp. 263-266).
- The random-detector value `P(L = 1)` for the success-positive task: §4.9.2 (p. 265).
- AUPR-Error, defined by making errors the positive class: §4.9.2 (p. 265).
- The AUROC recommendation: §4.9.2 (p. 266).
- Non-predictive readouts as OOD and multiplicity detectors: §4.10-§4.10.3 (pp. 266-268).
- Epistemic mechanisms and their stated confounds: §4.11.2 (p. 271), §4.11.5 (p. 275), §4.11.9
  (p. 290), §4.11.10 (pp. 290-291), §4.12.1-§4.12.3 (pp. 291-297).
- Aleatoric loss and its preconditions: §4.13.1-§4.13.5 (pp. 298-308).
- Binary-only equivalence of the predictive and aleatoric scoring properties: §4.13.3 (pp. 303-305).
- Control tables, cost logging, and the checklist wording are repository conventions.
