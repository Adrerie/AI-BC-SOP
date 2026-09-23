# SOP-04 — Measure confidence truthfulness

**Stage:** measure · **Tier:** Core + Extended · **Concepts:** C7 contracts, C8 quantity separation,
C9 proxy gap, C10 gaming, C12 guarantee type

## 1. Purpose

Decide which property a reported confidence number is supposed to have, measure that property with
the only instruments that are sensitive to it, and prove that the number is not obtained by an
artifact of the metric. Confidence is where trustworthy-ML claims are most often won cheaply and
lost honestly.

## 2. When to use

- Whenever the model emits a score used by a human or by a threshold — including "objectness",
  retrieval similarity, anomaly flags, or an LLM's log-likelihood.
- Before claiming calibrated uncertainty, well-ranked errors, or usable epistemic uncertainty.
- When comparing two confidence-estimation methods.
- After any intervention that could change confidence without changing decisions
  (recalibration, distillation, temperature scaling, capacity changes, longer training).

## 3. Inputs / prerequisites

- Frozen predictions on a labeled evaluation set designated by
  [`SOP-02`](SOP-02-build-evaluation-splits-under-leakage-discipline.md), plus the per-sample score
  `c(x)` and the correctness indicator `L = 1[ŷ = y]`.
- A separate calibration set if any post-hoc recalibration is contemplated — never the final test set.
- The declared quantity: predictive, aleatoric, or epistemic (§4).
- For epistemic claims: an OOD/multiplicity construction, or an ensemble/distribution-parameter
  mechanism whose assumptions you can state.

## 4. Definitions needed for execution

- **Predictive uncertainty** — `c(x) = P(L = 1)`, the probability that this prediction is correct.
  Confidence and uncertainty are used interchangeably here with `confidence = 1 − uncertainty`.
- **Aleatoric uncertainty** — entropy/variance of the true `P(Y | X = x)`; irreducible by more data.
- **Epistemic uncertainty** — multiplicity of plausible models given the data; reducible by
  supervision in underexplored regions of the data manifold.
- **Strictly proper scoring rule** — a score whose unique expected maximiser is the true
  distribution; the mechanism by which training with such a loss *encourages* truthful `c(x)`.
- **Perfect calibration** — `P(Ŷ = Y | C = c) = c` for all `c`. A necessary, not sufficient,
  condition for `c(x) = P(L = 1)`.
- **Ranking condition ("weak calibration")** — order preservation: higher `c` on correct than on
  incorrect cases; equivalent to calibration up to an unknown monotone map.
- **Contracts**, therefore, are three and not interchangeable: *proper scoring* (probability
  fidelity), *calibration* (conditional accuracy), *ranking* (order).

## 5. Procedure

**Core**

1. Name the quantity you are claiming (§4). If you cannot name it, you are reporting a score, not an
   uncertainty.
2. Pick the contract that the downstream use requires:
   - a numeric probability is consumed → proper scoring **and** calibration;
   - only a threshold filter is applied → ranking suffices, and say so;
   - worst-bin behavior matters (high-risk) → add the worst-case calibration view.
3. Compute the metric battery on the frozen predictions:
   - **Proper scores**: NLL/CE, Brier (binary), multi-class Brier; perplexity only for language
     modeling, where it is the exponentiated NLL — `exp(nll)` when the loss used natural logarithms,
     `2^(nll)` when `nll` was computed with log base 2. The two bases must match; the value is
     invariant to a *common* base choice but not to mixing them.
   - **Calibration**: bin the confidences, compute per-bin accuracy and mean confidence, report ECE
     (bin-weighted mean absolute gap), MCE (worst-bin gap), and the reliability diagram.
   - **Ranking**: AUROC plus both correctness AUPR specializations. For `aupr_success`, set
     positive = `L = 1` and rank by confidence `c`; for `aupr_error`, set positive = `L = 0` and rank
     by `1 − c` (or an explicitly equivalent score that increases with error likelihood). Both use
     the package's non-interpolated Average Precision definition and are read against their own
     positive-class prevalence.
4. Run the **trivial-score controls** as first-class rows in the same table:
   (i) a constant confidence — the *deployable* form, whose value is frozen on the calibration split
   before final testing, plus the *oracle* form set equal to the measured correctness rate of the set
   being scored, which is a metric diagnostic and must be labeled as one rather than shipped as a
   baseline; (ii) uniformly random scores; (iii) the uncalibrated softmax baseline of the same model.
   A claim is measured against these, not against zero.
5. Decompose before comparing: report task accuracy next to every confidence metric, and never read
   an improvement in NLL/Brier as an improvement in uncertainty alone — proper scores mix accuracy
   and calibration.
6. If recalibration is applied: fit the temperature (or other map) on the calibration split only,
   report the fitted value, and re-run the whole battery after the change; state the number of bins
   used.

**Extended** — add for high-stakes claims, or when epistemic/aleatoric quality is asserted:

7. Subgroup calibration: repeat ECE/MCE per class, per declared subgroup, and per difficulty slice;
   report the worst subgroup as a headline-adjacent number.
8. Bin sensitivity: recompute ECE over a range of bin counts (at minimum the one you report, plus a
   coarser and a finer setting) and report the spread; consider finer bins in the high-confidence
   region where modern models concentrate.
9. Proxy separation for epistemic claims: evaluate the score as an OOD detector (label = inside vs
   outside the training distribution) *and* re-evaluate it as a multiplicity detector
   (label = several acceptable answers). Report both, and never present either as the other.
10. Aleatoric-check for regression: fit the heteroscedastic Gaussian NLL
    `(1/2σ̂²)‖y − µ̂‖² + (d/2)log σ̂²`, and verify the fitted spread against empirical residual
    variance in bins of predicted spread — the balancing term is what stops "everything is hard".
11. Mechanism honesty: if the score comes from a feature distance or a centroid kernel, record that
    high aleatoric ambiguity can also raise it; if it comes from an ensemble, record that its spread
    still contains aleatoric uncertainty and that its implicit prior is the initialisation scheme.
12. Estimator cost: log training and inference overhead of the uncertainty mechanism next to its
    metric gain (see `SOP-08` §10).

## 6. Mandatory checks

- [ ] **Gaming check**: does the reported number beat the *deployable* constant-confidence control?
      A model reaches ECE = 0 by predicting a constant equal to the measured correctness rate of the
      set it is scored on; the source points out this needs no labeled validation set, only the prior
      probability of correctness — which is itself computed from the labels of that set, so the
      construction is an oracle diagnostic that exposes a weakness of ECE, not a baseline a deployed
      model can hold. A frozen constant from the calibration split is the legitimate reference row,
      and its final-set ECE is the gap between the frozen value and final accuracy. If the trivial
      control matches the claim, the claim is empty.
- [ ] **Quantity-to-instrument check**: an epistemic claim must not rest on proper scores alone —
      the Bayes predictor maximizes them with zero epistemic uncertainty.
- [ ] **Split-rights check**: no calibration parameter was fitted on a final-test subset.
- [ ] **Bin disclosure**: bin count, and whether bins are equal-width or equal-mass, stated wherever
      ECE/MCE appears.
- [ ] **Imbalance check**: each AUPR variant is read against the prevalence of *its own* positive
      class — `P(L = 1)` for Success, `P(L = 0)` for Error — because that prevalence is the random
      detector's value for that task. AUROC sits at 0.5 whatever the balance is, so it stays the
      headline when a positive rate is far from one half; state which class is positive wherever an
      AUPR appears.
- [ ] **Coverage check for threshold claims**: a ranking claim states the coverage at which the
      decision is taken.
- [ ] **Capacity check**: accuracy and calibration changes are reported separately after any
      longer training, distillation or capacity change, since overfitting can show up as probabilistic
      error while classification error keeps improving.

## 7. Decision or stop conditions

- **Stop: do not report a calibration number** if the binning choice flips the ordering of the
  methods being compared — report the sensitivity instead of a single value.
- **Stop and change the claim** from "calibrated" to "well-ranked" if only the ranking condition
  holds; the converse substitution is not permitted.
- **Stop** if the confidence mechanism's assumptions cannot be stated (posterior family, prior,
  independence of the distance measure from ambiguity). An unstated assumption is an unbounded claim.
- **Escalate to Extended** whenever a human or an automatic action consumes the score directly.
- **Accept and record a negative result** if no mechanism beats the trivial control at the stated
  coverage: the correct output is "we cannot yet quantify confidence here", not a weaker metric.

## 8. Common methodological failures

- Reporting ECE as if it measured truthfulness of `c(x)` per sample.
- Reaching ECE = 0 with an oracle constant and presenting it as a calibration achievement.
- Comparing an error-positive detector against the success-positive prevalence, or quoting one
  baseline for both AUPR variants.
- Silently choosing a bin count that flatters the result.
- Reading lower NLL across model scales as better uncertainty rather than better fit.
- Using OOD detection accuracy as a definition of epistemic uncertainty.
- Attributing low confidence to "the model knows it does not know" when the score is a distance in
  feature space and the sample is merely ambiguous.
- Fitting temperature scaling on the test set and reporting the test ECE afterwards.
- Claiming a decomposition into aleatoric plus epistemic as though it were exact.
- Treating MC-style sampling noise as free: report how many samples/backward passes produced the score.

## 9. Required outputs

- Metric battery table: per subset — accuracy, NLL, Brier, ECE (bins disclosed), MCE, AUROC,
  AUPR-Success and AUPR-Error (each with its positive class and its own no-skill value named), plus
  the trivial-control rows, the oracle constant flagged as a diagnostic rather than a baseline.
- Reliability diagram with the confidence histogram.
- Bin-sensitivity and subgroup slices (Extended).
- Calibration-parameter record: value, split it was fitted on, search range.
- A one-line statement of which contract the claim uses and which quantity it is about.

## 10. Minimum reporting requirements

Every confidence number must travel with: the quantity claimed, the contract used, the binning, the
trivial-control comparison, task accuracy, the split used for any fitted map, and the cost of
producing the score. A comparison of two confidence methods is invalid if these differ between them.

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

Quantity definitions: §4.2.1-§4.2.4, Definitions 4.1-4.7 (pp. 228-238) including the caution that
the decomposition requires assumptions and remains open. Score formats: §4.4 (pp. 240-242). Proper
scoring: §4.5.1, Definition 4.8 (p. 243); log-probability and Brier claims and proofs §4.5.2-§4.5.3
(pp. 245-246); BCE/max-prob §4.5.5, Definition 4.9 (pp. 246-247); CE as a lower bound §4.5.6
(p. 248); multi-class Brier §4.5.8 (pp. 250-251); "not all strictly proper rules are equally good
objectives" §4.5.7 (pp. 249-250); perplexity as the exponentiated NLL, using base 2 in both the
logarithm and the exponential, plus the footnote that the value is independent of the *common* base
§4.5.9 (p. 252); evaluation on the test set and the four interpretation caveats §4.5.9 (pp. 253-254).
Calibration: §4.6.1, Definitions 4.11-4.15 with the 5-step ECE recipe and MCE (pp. 254-257); gaming
ECE with a constant equal to the global accuracy, and the remark that only the prior probability of
correctness is needed, §4.6.2 (pp. 256-257); bin-count dependence and the fine-bins suggestion
§4.6.2 (pp. 256-257); reliability diagrams and their limits §4.6.3 (p. 259);
the tool summary §4.7 (p. 259). DNN calibration evidence and the NLL/accuracy disconnect:
§4.8.1-§4.8.2 (pp. 259-262); temperature scaling protocol §4.8.3 (pp. 262-263). Ranking condition
and detection metrics with the AUROC-over-AUPR recommendation: §4.9.1-§4.9.2 (pp. 263-266), where
§4.9.2 (p. 265) gives the random-detector value `P(L = 1)` for the success-positive task and defines
AUPR-Error by making errors the positive class, and §4.9.2 (p. 266) records the AUROC recommendation.
Non-predictive readouts as OOD and multiplicity detectors: §4.10-§4.10.3 (pp. 266-268). Epistemic
mechanisms and their stated confounds: §4.11.2 (p. 271), §4.11.5 (p. 275), §4.11.9 (p. 290),
§4.11.10 (pp. 290-291), §4.12.1-§4.12.3 (pp. 291-297). Aleatoric loss and its preconditions:
§4.13.1-§4.13.5 (pp. 298-308). Binary-only equivalence of the predictive and aleatoric scoring
properties: §4.13.3 (pp. 303-305). Control tables, cost logging, and the checklist wording are
repository conventions.
