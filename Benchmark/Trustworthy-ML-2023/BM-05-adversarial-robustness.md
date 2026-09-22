# BM-05 — Adversarial robustness under a declared threat model

**Tier:** Core (white-box empirical ladder) + Extended (black-box, semantic stress, certification)

## 1. Target capability / failure mode

**Capability.** Behaviour of the model under the worst case inside an explicitly bounded strategy
space — the adversarial branch of the generalization-type axis, where evaluation returns a bound
rather than a sample average.

**Failure mode under test.** Two, and the second is the one that corrupts the literature: (a) the
model fails on perturbed inputs; (b) the *evaluation* fails, reporting safety that comes from broken
gradients rather than from invariance.

## 2. Evaluation hypothesis

*Inside threat model T (goal G, strategy space S with norm and radius, knowledge K), model M's
accuracy is at least a.* Any missing element of T makes the hypothesis unformulated. Secondary
hypotheses: that M's advantage is not an artefact of the attack used (masking check), and that the
claim transfers to attack configurations and ε values beyond the one reported.

## 3. Required data and split assumptions

- Evaluation inputs from the declared deployment distribution; perturbations are constructed, not
  collected, so no extra test labels are consumed beyond the base set.
- Thresholds and any defense parameters fixed on validation material per
  [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md);
  adaptive attacks must not be tuned on the reported set.
- Access level stated per evaluated model: gradients, logits/probabilities, or labels only — and the
  same level for every compared method.
- Plausibility statement: whether perturbed inputs remain within what deployment can present.

## 4. Shift or stress construction

- **Pixel-ball stress**: single-step perturbation, then multi-step projected gradient descent within
  the ball, with norm and ε declared; sweep ε rather than reporting one point.
- **Semantic/geometry stress**: flow-style or transform-based perturbations bounded by a
  total-variation budget, where the intended worst case is a plausible change rather than pixel noise.
- **Pipeline stress**: the attack is applied to the *whole* inference pipeline, so preprocessing,
  resizing, quantisation and randomised components are inside the attacked function.
- **Black-box stress**: substitute-model transfer, and query-bounded score-based estimation, with the
  access level recorded.
- **Train/test condition matrix**: models trained under each condition evaluated under each other, to
  expose transferability gaps.
- **Certification stress** (Extended): prove invariance inside the ball via a relaxation, on the
  architectures the relaxation admits.

## 5. Required baselines

| Baseline | Role |
|---|---|
| Clean accuracy (no perturbation) | reference level |
| Random guessing / base rate | floor |
| Single-step attack | sensitivity check, explicitly not the strength reference |
| Multi-step projected attack at the strongest affordable configuration | the reference white-box attack |
| Attack run end-to-end through preprocessing | masking detector |
| Expectation-averaged and straight-through variants | randomized/quantising defense breakers |
| Black-box query-bounded attack | access-realistic reference |
| Adversarially trained model | the defense that must be compared at equal inference cost |
| Certified result (where computed) | the only row that may support an existential claim |
| Published defense rows re-evaluated under the above ladder | prevents inheriting a masked number |

## 6. Primary metrics

- `acc_under_eps` — accuracy under the named attack, always printed with dataset, norm, ε, and the
  attack configuration (iterations, step size, restarts).
- Robustness curve: `acc_under_eps` as a function of ε, per method.

## 7. Secondary / diagnostic metrics

- The train × evaluation condition matrix (transferability).
- Loss under attack on a log axis, to distinguish "no error found" from "hardly any loss gained".
- Query count and wall-clock per successful perturbation for black-box rows.
- Certified accuracy and, where computable, the looseness gap between the certified and empirical
  values.
- Confidence behaviour on perturbed inputs, linked to
  [`BM-04`](BM-04-error-and-anomaly-detection.md): does the score notice?
- Gradient-quality diagnostics for the defended model (gradient norm behaviour, variance across
  restarts) as the masking indicator.

## 8. Aggregation and uncertainty reporting

Report per ε and per attack configuration; do not average over configurations with different
strengths. Seed variability for stochastic defenses and stochastic attacks must be given with the
number of runs. Where several datasets are used, keep the rows separate and state the norm/ε used on
each — a cross-dataset average of robust accuracies at different ε values is not a number with a
meaning. Mark combined-defense rows (a defense plus adversarial training) as combined.

## 9. Failure interpretation

| Observation | Reading |
|---|---|
| Robust accuracy high only against naive gradient attacks | suspect masking; run the pipeline, straight-through and expectation-averaged attacks |
| Robustness collapses when the attack goes through preprocessing | the defense was the gradient path, not the model |
| A single-step attack and a multi-step attack give similar numbers | attack strength may still be inadequate; increase iterations before concluding |
| Robust on the trained condition, fragile on a nearby one | transferability gap; report the matrix |
| Certified accuracy far below empirical robust accuracy | the bound is loose in the region of interest |
| Certified accuracy far above it | impossible — an evaluation bug, a flawed bound, or different ingredients; explain which |
| Defense needs more capacity and epochs to reach clean parity | cost, reported as part of the result |

## 10. Computational reporting

Training: passes per step (a projected-attack inner loop multiplies forward/backward passes), extra
epochs, capacity change. Inference: usually unchanged for attack-time training, non-trivial for
transform- or ensemble-based defenses, and explicitly non-zero for randomized smoothing style
approaches. Attack side: iterations, restarts, time per example, queries. Report all of it — hiding
resources is a documented failure mode of this literature.

## 11. Validity limits

- A worst-case bound is valid **inside the declared strategy space only**, and may be unrealistically
  pessimistic relative to the deployment distribution.
- Empirical robustness is "no attack found in configuration C", never "no attack exists"; only a
  certificate supports the existential claim, and only under its assumptions (small networks,
  simplified tasks, possibly loose).
- Adversarial robustness is not corruption robustness, not OOD generalization, and not reliability
  under distribution drift; each needs its own artifact (`BM-01`, `BM-04`).
- Absence of gradient-following failure does not prove absence of failure: the model being safe is
  not equivalent to no gradient-based algorithm being able to find an attack.
- Black-box results inherit the substitute model's assumptions about architecture, size and
  optimizer.
- The source provides no default iteration count, step size or restart rule; those are choices this
  benchmark requires you to state.

## 12. Related SOPs

Executed by [`SOP-05`](../../SOP/Trustworthy-ML-2023/SOP-05-run-worst-case-stress-evaluation.md);
threat model registered by
[`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md); split and tuning
rights by [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md);
cost and masking audit by
[`BM-08`](BM-08-evaluation-integrity-audit.md); reporting by
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md).


## 13. Source traceability

Threat-model vocabulary, attack formulations, and the defense-side discussion are anchored in
[`SOP-05`](../../SOP/Trustworthy-ML-2023/SOP-05-run-worst-case-stress-evaluation.md) §12: the
worst-case framing (§2.15, pp. 86-87), the threat model and its parts (§2.15.1, Definitions 2.35-2.40,
pp. 87-88), the attack formulations and their strength ordering (§2.15.2-§2.15.4, pp. 89-92),
strategy spaces beyond pixel norms (§2.15.5-§2.15.7, Definition 2.41, pp. 92-97), access levels and
query accounting (§2.15.8-§2.15.10, Definitions 2.42-2.43, pp. 93-100), adversarial training cost
(§2.15.11, §2.15.13, pp. 101-107), gradient masking and its circumvention progression (§2.15.12,
Definitions 2.44-2.46, pp. 102-107), transform defences at train and inference time (§2.15.14,
pp. 108-110), and certification with its scope limits (§2.15.15, Definition 2.47, pp. 111-113).

Anchors specific to this benchmark's measurements:

- The reporting row shape — dataset, norm-qualified distance, accuracy, with combined defenses
  footnoted: Table 2.8 (p. 103).
- Sweeps over adversary strength and over ε, and the train × evaluation condition matrix:
  §2.15.13 (pp. 107-113), §2.15.15 (p. 110).
- Defenses whose theoretical optimum is full failure, reported as nonzero only through
  implementation imperfection: §2.15.12 (p. 103).
- Certification assumes a bounded loss model; the looseness question and the joint training
  objective: §2.15.15 (pp. 111-113).
- An upper-bound violation must be explained as bug, flawed bound, or different ingredients:
  §5.1.1 (p. 333).
- Hiding resources behind an accuracy-only comparison: §5.1.3 (pp. 335-338).

Per-configuration reporting as an acceptance requirement, and the Core/Extended split between
empirical and certified tracks, are repository conventions.
