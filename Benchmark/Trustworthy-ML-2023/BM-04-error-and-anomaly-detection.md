# BM-04 — Error and anomaly detection by the confidence score

**Tier:** Core (one detection task) + Extended (all three targets, mechanism comparison)

## 1. Target capability / failure mode

**Capability.** The same scalar score that expresses confidence can also act as a *detector*: of its
own errors, of out-of-distribution inputs, and of inputs that admit multiple acceptable answers.
This separates model capability from the quality of the model's self-assessment — a system can be
accurate and blind, or uncertain and precise.

**Failure mode under test.** Silent failure: a wrong or unsupported input answered with the same
score as a routine one, so that no downstream rule can decline.

## 2. Evaluation hypothesis

Three binary detection hypotheses, each with its own label construction and none reducible to the
others:

- **H-error** — `c(x)` ranks correct above incorrect predictions (`L` as target).
- **H-ood** — `1 − c(x)` ranks out-of-distribution above in-distribution inputs; a *proxy* for
  epistemic uncertainty, because OOD-ness is a property of the data and independent of any model.
- **H-multiplicity** — `1 − c(x)` ranks inputs with several acceptable answers above unambiguous
  ones; a proxy for aleatoric uncertainty.

The benchmark's stated non-alignment is part of the hypothesis set: an OOD sample may be answered
confidently and correctly, and an ID sample may be answered unconfidently, so H-ood and H-error must
not be pooled.

**H-sensitivity** (Extended) adds a fourth target with its own label construction: an item is
*sensitive* when rephrasing it along an axis the task does not define changes the answer. The event to
flag is neither novelty nor ambiguity nor an error already made — an input can be squarely in
distribution, unambiguous, and still flip on wording — so this row may not be pooled with the three
above, and a detector for it is scored against the prevalence of sensitive items in the family used,
not against one half.

## 3. Required data and split assumptions

- A labeled ID evaluation set, and one or more OOD sets whose relation to the training distribution
  is declared (near / far; same task different domain; unforeseen classes).
- Multiplicity labels: either several human annotations per input, or a constructed ambiguity where
  the legitimate answer set is known by design.
- Corruption labels at declared severities if corruption detection is claimed.
- Detection thresholds are chosen on validation material only, per
  [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md);
  reporting a detector without saying where its threshold came from is out of scope here.
- The positive class named for every detection task, with its prevalence stated per subset —
  `P(OOD)` for a novelty task, `P(L = 0)` for an error-detection task, `P(multiple-answer)` for an
  ambiguity task — since the designated positive is what sets the reference point for every
  precision-based score.

## 4. Shift or stress construction

- Vary OOD *distance*: near-shifted (same semantics, changed style) through far-shifted (unrelated
  distribution); a single OOD pair hides whether the detector responds to novelty or to style.
- Vary ambiguity independently of novelty, so that a distance-based score cannot pass H-ood while
  actually measuring H-multiplicity.
- **Adversarial stress:** additionally test whether the confidence mechanism reacts to
  adversarially constructed failures from
  [`BM-05`](BM-05-adversarial-robustness.md). Treat this as a separate stress axis, not as an OOD
  family and not as evidence of OOD-detection capability. This does not contradict
  [`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md) listing adversarial
  as one generalization *type*: that is the source's taxonomy of train-to-test differences, whereas
  the claim excluded here is the detection-specific one — that firing on constructed inputs would
  show the detector finds natural novelty.
- Open-set stress: unforeseen classes that *should* produce low confidence; here a top-1 accuracy
  score is the wrong readout and the confidence statistic is the right one.
- Coverage sweep: detection quality as a function of accepted coverage, which is what
  [`BM-07`](BM-07-selective-prediction-under-cost.md) turns into a decision.
- **Rephrasing family stress** (Extended, for H-sensitivity): build a family per item where the intended
  answer is fixed by construction and only the wording moves, then ask the detector to flag the unstable
  items using the family alone, with no reference answer at test time. Report the family size and the
  number of forward passes per item with every detection figure: a detector that samples the model
  several times per item is buying its score, and the same figure from a single-pass detector is not
  comparable to it.

## 5. Required baselines

| Baseline | Role |
|---|---|
| Random score | `auroc` = 0.5 reference, base-rate-independent |
| Base-rate predictor (constant score) | the `aupr` reference, which is the prevalence of the task's declared positive: `P(L = 1)` success-positive, `P(L = 0)` error-positive, `P(OOD)` novelty-positive, `P(multiple-answer)` ambiguity-positive |
| Max-probability of the unmodified model | the default every mechanism is compared to |
| Entropy / margin over the class distribution | the same logits, a different readout |
| Feature-space distance score (class-conditional Gaussian, or kernel centroid) | a genuinely different mechanism |
| Ensemble disagreement (predictive variance or entropy of the averaged prediction) | a Bayesian-style mechanism |
| Oracle detector using the ground-truth labels | upper bound, labeled as such |
| Prior published detector at the same OOD pairs | comparability, only if the training corpus matches |

## 6. Primary metrics

- `auroc` per detection target — the headline, because its random reference stays at 0.5 regardless
  of the base rate.
- `aupr` for each declared detection target using the package's non-interpolated Average Precision
  convention, with positive class and a score that increases toward that class stated explicitly.
  For H-error, `aupr_success` uses positive = correct with score `c`, while `aupr_error` uses positive
  = error with score `1 − c` (or an explicitly equivalent error-likelihood score). For H-ood use
  positive = OOD and an OOD-oriented score such as `1 − c`; for H-multiplicity use positive =
  multiple-answer and a multiplicity-oriented score such as `1 − c` when that interpretation is
  justified. For H-sensitivity use positive = sensitive and the detector's sensitivity-oriented score;
  its AP no-skill reference is `P(sensitive)` in the evaluated rephrasing families.
- `tnr_at_high_tpr` (true-negative rate at a fixed high true-positive rate, for example 95 %) —
  the operating-point form used when a false alarm budget rather than an average matters.

## 7. Secondary / diagnostic metrics

- The full ROC and precision-recall curves, not only their areas.
- `risk_at_coverage` on the error-detection target (bridges to `BM-07`).
- Separability of the three targets: how much of H-ood performance is explained by H-multiplicity
  on the same model, measured by evaluating each with the other's labels.
- Calibration of the same score (`BM-03`), since a detector can rank well and still mis-state
  probabilities.
- Per-class detection rates, to expose detectors that only work on majority classes.

## 8. Aggregation and uncertainty reporting

Report each detection target on each OOD/ambiguity family separately; an average over heterogeneous
OOD pairs is the single most common way this benchmark is over-claimed. Give the number of OOD pairs
and the prevalence of the designated positive behind every area. Provide seed or bootstrap
variability, and state which
comparisons are within noise. Never pool H-error with H-ood or H-multiplicity into one "uncertainty
quality" number.

## 9. Failure interpretation

| Observation | Reading |
|---|---|
| High `auroc` on OOD, high `ece` on ID | ranks novelty, mis-states probability: two different claims |
| Distance score fires on ambiguous-but-familiar inputs | mechanism conflation, not epistemic detection |
| Detector is strong on far-OOD, chance on near-OOD | sensitivity to style/density, not to support |
| Ensemble disagreement grows with M only on OOD | expected; check the accuracy confound before claiming better uncertainty |
| Good `aupr` on an imbalanced subset only | compare with the prevalence of the declared positive class for that detection task; may be no skill |
| Detector does not fire on adversarial examples | confidence and adversarial failure are separate axes |
| H-sensitivity detector fires exactly where confidence is low | it detected difficulty, not wording dependence; re-run against the H-multiplicity and H-ood rows before claiming the flag means sensitivity |
| H-sensitivity label taken from items whose intended answer is not fixed by construction | the "sensitive" items are ambiguous items; the detector is measuring H-multiplicity under another name |

## 10. Computational reporting

State: forward passes per prediction for each mechanism (a single deterministic model, K stochastic
samples, or M ensemble members), memory for stored models or checkpoints, and the cost of the
statistics a distance score needs. Also state the false-alarm workload a threshold implies for
review capacity — detection is bought with human attention downstream.

## 11. Validity limits

- Every target here is a *proxy*: OOD detection for epistemic uncertainty, multiplicity detection for
  aleatoric uncertainty. The source is explicit that the proxies are not the quantities.
- Results depend on the chosen OOD families; a ranking established on one pair does not transfer, so
  do not generalize a single dataset pair's ordering of mechanisms.
- A calibrated detector on a fixed deployment distribution need not remain one after drift.
- "No data region" behavior is not guaranteed by any of these scores; a detector can rank
  confidently on inputs far off the data manifold.
- Detection metrics assume the labels used to define the target are trustworthy, which circularly
  requires data-quality checks for the multiplicity target.

## 12. Related SOPs

Executed by [`SOP-04`](../../SOP/Trustworthy-ML-2023/SOP-04-measure-confidence-truthfulness.md)
§5 steps 9-11, with the mitigation reading in
[`SOP-06`](../../SOP/Trustworthy-ML-2023/SOP-06-choose-mitigation-or-abstain.md); stress inputs from
[`SOP-05`](../../SOP/Trustworthy-ML-2023/SOP-05-run-worst-case-stress-evaluation.md); abstention
consequences in [`SOP-06`](../../SOP/Trustworthy-ML-2023/SOP-06-choose-mitigation-or-abstain.md) and
[`BM-07`](BM-07-selective-prediction-under-cost.md); training-data attribution variant in
[`BM-06`](BM-06-explanation-quality.md), executed as described in
[`SOP-07`](../../SOP/Trustworthy-ML-2023/SOP-07-evaluate-explanation-methods.md) §5 step 11;
reported through
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md).

## 13. Source traceability

Confidence as a detector of three different targets and the non-alignment arguments: §4.10
(pp. 266-268); OOD-detector construction: §4.10.1 (p. 267); multiplicity detector: §4.10.2 (p. 267);
menu of evaluation methods so far: §4.10.3 (pp. 267-268). Epistemic-uncertainty proxy reasoning and the
model-independence of "OOD-ness": §4.2.3 (pp. 236-239) and §4.3.1 (p. 239). AUROC/AUPR definitions,
base-rate behavior and the AUROC recommendation: §4.9.2 (pp. 265-266), where the random-detector
value is given for the success-positive task and AUPR-Error is defined by swapping which class is
positive. Threshold filtering as the
application that only needs ranking: §4.9.1 (pp. 263-264). Distance-score comparison against
max-probability with detection metrics on multiple OOD pairs, and the cautions against generalizing
one pair and against reading ambiguity as novelty: §4.12.1-§4.12.2 (pp. 291-297); the summary that
both estimator families are evaluated through OOD detection *as a proxy task*: §4.12.3 (p. 297).
Ensemble spread behavior with M and the accuracy confound: §4.11.5 (p. 275). Open-set recognition
with and without an explicit "I don't know" output: §4.1.3 (pp. 225-226). Unforeseen-class
benchmark whose meaningful readout is confidence rather than top-1 accuracy: §2.6.1 (p. 43).
Corruption benchmark as a family of severe perturbations: §2.6.1 (p. 42). Self-influence detection
of mislabeled training items with `auroc`/AP and its stated assumptions: §3.12.2, Definition 3.16
(pp. 216-217). TNR-at-fixed-TPR reporting appears in the source's own comparison tables
(§4.12.1, p. 293). Target separation, the aggregation rules, the requirement that every detector use
a score increasing toward its declared positive class, and the package-wide use of non-interpolated
Average Precision for `aupr` are synthesized/repository conventions rather than claims attributed to
the source.
