# BM-05 — Adversarial robustness under a declared threat model

**Tier:** Core (white-box empirical ladder) + Extended (black-box, semantic stress, certification)

## 1. Target capability / failure mode

**Capability.** Behavior of the model under the worst allowed perturbation inside an explicitly
bounded strategy space. The target is a worst-case quantity. Empirical attacks probe that quantity and
can miss failures. Certified evaluation may provide a provable guarantee or bound under the assumptions
of a specific certificate.

**Failure mode under test.** Two failure modes are under test, and the second is the one that corrupts
the literature. (a) The model fails on perturbed inputs. (b) The *evaluation* fails, and the evaluation
reports safety that comes from broken gradients rather than from invariance.

## 2. Evaluation hypothesis

This benchmark keeps two claim types separate, and states the conditions each claim depends on:

- **Empirical claim:** under threat model T and attack suite A, the measured attacked accuracy is a.
- **Certified claim:** under threat model T and certificate assumptions C, the certified accuracy is b.

The empirical claim carries one explicit limitation: attack suite A may fail to find existing
adversarial examples. The certified claim means that the stated fraction of examples has a provable
guarantee within that threat model. Any missing element of T makes either claim uninterpretable.

Suppose the two rows share the same model, test set, threat model and valid implementations. Then the
two rows bracket the target quantity. The bracket runs in one direction: **certified robust accuracy ≤
exact finite-sample robust accuracy ≤ empirical attacked accuracy under attack suite A**.

A certificate row is therefore a lower bound on the true robust accuracy. A certificate row is never
an upper-bound row of the kind `SOP-02` defines. An attacked accuracy is an observation, not a bound.
The comparison is void when the two rows use different norm bounds, samples or definitions. An
empirical advantage must additionally survive the adaptive-attack checks and the masking checks.

## 3. Required data and split assumptions

- Take the evaluation inputs from the declared deployment distribution. Construct the perturbations
  rather than collect them, so the evaluation consumes no extra test label beyond the base set.
- Fix the thresholds and any defense parameters on validation material per
  [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md).
  Do not tune adaptive attacks on the reported set.
- State the access level for each evaluated model: gradients, logits/probabilities, or labels only.
  Use the same access level for every compared method.
- Add a plausibility statement. State whether the perturbed inputs remain within what the deployment
  can present.

## 4. Shift or stress construction

- **Pixel-ball stress**: apply a single-step perturbation, then a multi-step projected gradient descent
  inside the ball. Declare the norm and ε. Sweep ε rather than report one point.
- **Semantic/geometry stress**: apply flow-style or transform-based perturbations bounded by a
  total-variation budget. The intended worst case is a plausible change, not pixel noise.
- **Pipeline stress**: apply the attack to the *whole* inference pipeline. Preprocessing, resizing,
  quantization and the randomized components are then inside the attacked function.
- **Black-box stress**: use substitute-model transfer, and query-bounded score-based estimation. Record
  the access level.
- **Train/test condition matrix**: evaluate models trained under each condition under each other
  condition, so that the matrix exposes transferability gaps.
- **Discrete-append stress** (Extended): the perturbation is a token sequence appended to the model's
  instruction. There is no norm to bound, so the budget is a suffix length. State the target output
  that the attack optimizes, and the token budget. State whether you re-ran the attack against the
  defense, or reused the attack from its paper. Gradient-following on the embedding is an approximation
  of a discrete search, not the search itself. Say which candidate-selection rule you used. A result
  obtained by naive continuous descent on one-hot inputs is an artifact of the relaxation.
- **Channel stress** (Extended): the adversary writes content that the system *reads*, rather than
  content that the system classifies. That content is retrieved, supplied or tool-returned text.
  Declare the channel. State whether the injected content is length-bounded or position-bounded. State
  what a compliant reading of the task would produce. This row is not a distribution-shift row and not
  a norm-ball row. There is no input-edit budget to report, and a plausibility argument borrowed from
  either of those rows would be about the wrong variable.
- **Certification stress** (Extended): apply a certificate appropriate to the declared threat model and
  model family. State the certificate's assumptions. Report the certified accuracy, or the
  corresponding certified bound. The relaxation approach discussed by the source is one admissible
  family, not the universal form of certification.

## 5. Required baselines

| Baseline | Role |
|---|---|
| Clean accuracy (no perturbation) | reference level |
| Random guessing / base rate | floor |
| Single-step attack | sensitivity check, explicitly not the strength reference |
| Multi-step projected attack at the strongest affordable configuration | a reference floor for gradient-following threat models — not a sufficient adversarial evaluation on its own |
| An **adaptive** attack built against the specific defense under test | the row that decides whether the defense survives the mechanism it claims |
| Attack run end-to-end through preprocessing | masking detector |
| Expectation-averaged and straight-through variants | randomized/quantizing defense breakers |
| Black-box query-bounded attack | access-realistic reference |
| Adversarially trained model | the defense that must be compared at equal inference cost |
| Certified result (where computed) | the only row that may support an existential claim |
| Published defense rows re-evaluated under the above ladder | prevents inheriting a masked number |
| Random-suffix and no-injection controls at matched budget (Extended) | the floor for the two discrete rows; without it a long suffix looks effective simply for being long |

## 6. Primary metrics

- `acc_under_eps` — accuracy under a named norm-bounded attack, always printed with dataset, norm, ε,
  and the attack configuration (iterations, step size, restarts).
- Robustness curve: `acc_under_eps` as a function of ε, per method.
- For **discrete-append** and **channel** stress, do not reuse `acc_under_eps`: there is no ε. Report
  the fraction of eligible trials in which the **predeclared adversarial goal is achieved**, together
  with the corresponding clean/no-injection task performance. Define the success event before the run
  (for example target-string elicitation, policy-violating action, or instruction-source confusion)
  and attach the suffix length or channel/placement budget to the rate.

## 7. Secondary / diagnostic metrics

- The matrix of train conditions against evaluation conditions (transferability).
- Loss under attack on a log axis, to distinguish "no error found" from "hardly any loss gained".
- Query count and wall-clock per successful perturbation for black-box rows.
- Certified accuracy and, where computable, the looseness gap between the certified and empirical
  values.
- Confidence behavior on perturbed inputs, linked to
  [`BM-04`](BM-04-error-and-anomaly-detection.md): does the score notice?
- Gradient-quality diagnostics for the defended model (gradient norm behavior, variance across
  restarts) as the masking indicator.

## 8. Aggregation and uncertainty reporting

Report the norm-bounded rows per ε and per attack configuration. Do not average configurations of
different strengths together. Report the discrete-append rows per suffix budget, and the channel-stress
rows per channel and placement. Do not pool either family with ε-ball rows into one robustness scalar.

Report the seed variability of a stochastic defense or a stochastic attack with the number of runs.
Keep the rows separate where you use several datasets, and state the norm/ε used on each dataset. An
average of robust accuracies across datasets at different ε values is not a number with a meaning.
Mark combined-defense rows (a defense plus adversarial training) as combined.

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

Report the cost on each side of the evaluation:

- Training: the passes per step (a projected-attack inner loop multiplies forward/backward passes),
  the extra epochs, and the capacity change.
- Inference: usually unchanged for attack-time training, non-trivial for transform- or ensemble-based
  defenses, and explicitly non-zero for randomized smoothing style approaches.
- Attack side: the iterations, the restarts, the time per example, and the queries.

Report all three cost families. Hiding resources is a documented failure mode of this literature.

## 11. Validity limits

- A worst-case bound is valid **inside the declared strategy space only**, and may be unrealistically
  pessimistic relative to the deployment distribution.
- Empirical robustness means "no attack found in configuration C". Empirical robustness never means
  "no attack exists". Only a certificate supports the existential claim, and only under the assumptions
  of the certificate actually used. The source's own bound is demonstrated on a small network and a
  simplified task. That demonstration describes the method the source analyzes. The demonstration does
  not describe the reach of certified robustness as a field. Do not quote that demonstration as a
  limit on what certification can cover.
- Adversarial robustness is not corruption robustness, not OOD generalization, and not reliability
  under distribution drift. Each of those three needs its own artifact (`BM-01`, `BM-04`).
- The absence of a gradient-following failure does not prove the absence of failure. A safe model is
  not equivalent to a model for which no gradient-based algorithm can find an attack.
- Black-box results inherit the substitute model's assumptions about architecture, size and
  optimizer.
- The two Extended rows do not share an axis with the pixel rows. A suffix budget and a channel claim
  have no ε. You cannot plot either row on the same accuracy-versus-ε curve as the pixel rows. You
  cannot average either row into one robustness number with the rows that do have ε. Report the two
  Extended rows as their own table. Read a discrete-append result as a statement about the model
  revision and the attack family named with that result, since both move.
- The source provides no default iteration count, step size or restart rule. Those items are choices
  that this benchmark requires you to state. Stating a choice is not the same as defending it. Attack
  adequacy is an argument about the threat model and the defense. A ladder that never broke a defense
  may simply have been the wrong ladder. Say which complementary attacks you ran, and which you did
  not run.

## 12. Related SOPs

- Execution: [`SOP-05`](../../SOP/Trustworthy-ML-2023/SOP-05-run-worst-case-stress-evaluation.md).
- Threat model registration: [`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md).
- Split and tuning rights: [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md).
- Cost and masking audit: [`BM-08`](BM-08-evaluation-integrity-audit.md).
- Reporting: [`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md).


## 13. Source traceability

The threat-model vocabulary, the attack formulations and the defense-side discussion are anchored in
[`SOP-05`](../../SOP/Trustworthy-ML-2023/SOP-05-run-worst-case-stress-evaluation.md) §12. That section
anchors the following:

- the worst-case framing (§2.15, pp. 86-87)
- the threat model and its parts (§2.15.1, Definitions 2.35-2.40, pp. 87-88)
- the attack formulations and the ordering of their strength (§2.15.2-§2.15.4, pp. 89-92)
- strategy spaces beyond pixel norms (§2.15.5-§2.15.7, Definition 2.41, pp. 92-97)
- access levels and query accounting (§2.15.8-§2.15.10, Definitions 2.42-2.43, pp. 93-100)
- adversarial training cost (§2.15.11, §2.15.13, pp. 101-107)
- gradient masking and its circumvention progression (§2.15.12, Definitions 2.44-2.46, pp. 102-107)
- transform defenses at train and inference time (§2.15.14, pp. 108-110)
- certification with its scope limits (§2.15.15, Definition 2.47, pp. 111-113)

Anchors specific to this benchmark's measurements:

- The reporting row shape — dataset, norm-qualified distance, accuracy, with combined defenses
  footnoted: Table 2.8 (p. 103).
- Sweeps over adversary strength and over ε, and the matrix of train conditions against evaluation
  conditions: §2.15.13 (pp. 107-113), §2.15.15 (p. 110).
- Defenses whose theoretical optimum is full failure, reported as nonzero only through
  implementation imperfection: §2.15.12 (p. 103).
- The bounded-loss-model assumption of certification, the looseness question and the joint training
  objective: §2.15.15 (pp. 111-113).
- Explain an upper-bound violation as bug, flawed bound, or different ingredients: §5.1.1 (p. 333).
- Hiding resources behind an accuracy-only comparison: §5.1.3 (pp. 335-338).

Per-configuration reporting as an acceptance requirement, and the Core/Extended split between the
empirical and certified tracks, are repository conventions. The scope limits in §2.15.15 (pp. 111-113)
describe the construction analyzed there. This package reads those limits as conditions on one
certificate, not as limits of the field. This package also requires an adaptive attack per defense
mechanism. This package synthesizes both of those moves — see
[`SOP-05`](../../SOP/Trustworthy-ML-2023/SOP-05-run-worst-case-stress-evaluation.md) §12.

The ordering in §2 (`certified ≤ true ≤ empirical`) comes from definition, not from the source. The
book gives the certified row and the attacked row separately, and never lines the two rows up. So the
treatment of a certificate as a lower bound on the target quantity is labeled **synthesized** here and
in [`concept_reconstruction.md`](../../Validation/Trustworthy-ML-2023/concept_reconstruction.md).
