# SOP-05 — Run worst-case stress evaluation

**Stage:** stress · **Tier:** Core + Extended · **Concepts:** C11 threat model, C12 guarantee type,
C10 gaming under attack, C14 cost

## 1. Purpose

Measure what happens to the model under an explicitly bounded worst case, and make sure the number
you report describes the model rather than the failure of your attack. Worst-case evaluation is the
only place where a *guarantee* is on the table, and also the place where evaluation is most easily
fooled into reporting one that does not exist.

## 2. When to use

- Whenever the deployment claim is adversarial, or the environment could be actively shaped to make
  the model fail (camouflage, spoofed inputs, manipulation of the acquisition path).
- When evaluating a defense, including a preprocessing or randomization "defense".
- When a robustness number from the literature is being used to justify a choice.
- When semantic perturbations (corruptions, viewpoint, style, geometry) must be bounded even though
  no adversary is assumed.

## 3. Inputs / prerequisites

- A trained model with access decisions settled: weights and gradients (white-box), logits or
  probabilities only, or labels only (black-box).
- A baseline attack implementation with a shared code path for all evaluated models (see
  [`SOP-08`](SOP-08-report-evidence-and-validity-boundaries.md) on shared metric code).
- Compute allowance: adversarial evaluation multiplies forward/backward passes per sample; budget it
  before starting.
- For the certification branch: a loss model and network architecture simple enough for the bound you
  intend to compute.

## 4. Definitions needed for execution

- **Threat model** — three parts, all required: **adversarial goal** (which environment counts as
  worst), **strategy space** (the set of environments the adversary may choose from), and
  **knowledge** (what the adversary knows about the model). Leaving any one unspecified means the
  reported robustness has no referent.
- **Worst-case framing** — preparing for the worst yields a lower bound on performance *restricted
  to the declared strategy space*, and may be unrealistically pessimistic relative to the true
  deployment distribution.
- **ε** — the radius bound of the strategy space, always norm-qualified (`ℓ∞`, `ℓ2`, or a total
  variation budget for flow-style transforms).
- **Gradient masking (obfuscated gradients)** — a defence that breaks the gradient path, so a
  gradient-based attack reports safety that is not there. Three mechanisms: shattering, stochasticity,
  exploding/vanishing gradients.
- **Certified evaluation** — proving no successful perturbation exists within the ball, as opposed to
  failing to find one; achieved by bounding the loss over the ball through a relaxation chain
  (empirical robust loss → first-order bound → LP → SDP relaxation).
- **Attack strength ordering** — a single gradient step does not in general even find a local
  optimum; iterative projected gradient descent is the reference white-box attack, and its strength
  depends on the optimiser configuration.

## 5. Procedure

**Core**

1. Write the threat model as three sentences: goal, strategy space with norm and radius, knowledge.
   Re-read it against the deployment scenario from
   [`SOP-01`](SOP-01-specify-deployment-setting.md): if the strategy space does not contain the
   changes you actually expect, the evaluation will answer a different question.
2. Fix ε early, keep it small, and keep it *identical across all methods compared*; record the norm
   it is expressed in. Below a visibility threshold the perturbations stop being humanly meaningful,
   so also record whether the perturbed samples remain plausible.
3. Run the attack ladder, reporting each rung separately:
   - single-step attack (fast sanity bound on the model's sensitivity);
   - multi-step projected attack at the *strongest configuration you can afford*, with the
     configuration reported: step size, iteration count, restarts, projection, clipping;
   - targeted variants if the goal is targeted misclassification rather than any error.
4. If any part of the system is non-gradient-friendly (cropping, resizing, quantisation,
   randomisation), attack the **joint pipeline** rather than the differentiable core: compose the
   transforms, use a straight-through estimator for quantising steps, and average gradients over
   sampled transforms when a single sampled gradient is too noisy to optimise.
5. For black-box settings, state the access level and count the queries: an estimation-of-gradient
   attack pays a per-coordinate cost and may additionally require logits rather than labels.
6. Report robustness as a curve or matrix, not a scalar: accuracy versus ε, and the
   training-condition × evaluation-condition matrix, so transferability gaps become visible.
7. Record the compute ledger: passes per training step, number of epochs added, capacity change, and
   inference overhead (which for attack-time training is typically zero at inference).
8. Run the masking checks in §6 before believing any high robust accuracy.

**Extended** — add for publication-grade robustness claims or safety-relevant deployment:

9. Add the certification branch only where the architecture and task admit it; report which
   relaxation was used, what assumptions it needs, and how loose it may be. A post-hoc certificate
   can be arbitrarily loose, and a loss trained with a plain classification objective can inflate the
   quantity being bounded — if you certify, train for the bound.
10. Add a semantic-stress branch for the non-adversarial case: corruptions and geometry/style
    transforms with the same reporting discipline (severity sweep, not a single point).
11. Add a plausibility filter to the strategy space where the deployment only ever sees realistic
    inputs, and report both the pessimistic and the realistic variant.
12. Add a defence-progress report: for each defence, the attack that broke it, or an explicit
    "not broken by X, Y, Z at configuration C".

## 6. Mandatory checks

- [ ] **Three-part threat model present**; no field implicit.
- [ ] **Strategy-space/goal alignment**: the declared space contains the perturbations the goal
      calls worst; if the goal is semantic and the space is a pixel ball, say so in the result line.
- [ ] **Masking check**: robust accuracy that rises when the attack is *weakened* or when gradients
      are made unavailable is an artefact. Re-run the joint-pipeline attack (step 4) and compare.
- [ ] **Strongest-attack check**: the reported attack configuration is at least as strong as the one
      used to establish the baseline being beaten; iteration count is not silently reduced.
- [ ] **ε parity** across all methods, including prior work you quote.
- [ ] **Query accounting** present for every black-box number.
- [ ] **Guarantee wording discipline**: "no attack found within configuration C" is never written as
      "robust"; only a certificate supports the existential claim, and only inside its assumptions.
- [ ] **Training-time/inference-time consistency** for transform-based defences: if transforms are
      applied at inference, they must have been applied during training too.

## 7. Decision or stop conditions

- **Stop and rebuild the evaluation** if masking is suspected (high apparent robustness plus a
  benign-looking PGD output on samples the model should fail on). The model being safe is not
  equivalent to no gradient-based attack being able to find a failure.
- **Stop the certification branch** if the bound requires assumptions your model does not meet
  (shallow network, binary task); report the empirical result and the absence of a guarantee.
- **Reclassify the claim** from adversarial robustness to corruption robustness if the strategy
  space was changed to semantic transforms — different capability, different comparison class.
- **Accept a null result** where the only configurations that survive are ones the adversary cannot
  afford: state the cost asymmetry rather than the margin.

## 8. Common methodological failures

- Reporting single-step-attack accuracy as "adversarial robustness".
- Leaving the norm implicit (a number without `ℓ∞` or `ℓ2` cannot be compared).
- Changing ε between your method and the baseline.
- Defending by non-differentiable preprocessing and evaluating with a naive gradient attack.
- Presenting a defense whose theoretical optimum is a full failure, justified by implementation
  imperfection.
- Combining a defense with adversarial training and reporting the combination under the defense's
  own name.
- Certifying on a relaxed bound that is loose in exactly the region of interest, without checking
  looseness.
- Ignoring the cost of the robustness you are claiming, or transferring it to inference time in the
  narrative.

## 9. Required outputs

- Threat-model statement (goal / strategy space with norm and radius / knowledge).
- Attack configuration record per attack rung, including iteration budget and restarts.
- Robustness curves (accuracy versus ε) and the train × evaluation-condition matrix.
- Query-cost record for black-box settings.
- Masking-check outcome, pass or fail, with the evidence.
- Compute ledger; certificate statement with its assumptions if the certification branch ran.

## 10. Minimum reporting requirements

Every robustness number must carry: dataset, norm, ε, attack used and its configuration, whether the
attack was run end-to-end through preprocessing, and the compute cost. Comparative tables must keep
the distance column norm-qualified and must mark which rows combine adversarial training.

## 11. Links to relevant Benchmarks

- [`BM-05`](../../Benchmark/Trustworthy-ML-2023/BM-05-adversarial-robustness.md) — the standardized
  threat-model + attack-ladder + masking-check protocol.
- [`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md) —
  corruption/severity sweeps as the non-adversarial sibling.
- [`BM-04`](../../Benchmark/Trustworthy-ML-2023/BM-04-error-and-anomaly-detection.md) — whether the
  confidence score notices stressed inputs.
- [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md) — audits ε
  parity, configuration reporting, and guarantee wording.

## 12. Source traceability

Educated-guess versus worst-case framing and its pessimism caveat: §2.15 (pp. 86-87). Threat-model
parts and the "missing critical ingredients" statement: §2.15.1, Definitions 2.36-2.40
(pp. 87-88). Attack formulations for the single-step and projected attacks, non-convexity caveat,
and optimiser dependence: §2.15.2-§2.15.3 (pp. 89-91). Strength ordering and the ε policy:
§2.15.4 (pp. 91-92). Strategy spaces beyond pixel norms and the total-variation definition:
§2.15.5-§2.15.7, Definition 2.41 (pp. 92-97). White-box versus black-box, substitute models and
zeroth-order access requirements with query cost: §2.15.8-§2.15.10, Definitions 2.42-2.43
(pp. 93-100). Adversarial-training objective, cost ledger, and transferability observation:
§2.15.11 (pp. 101-102). Gradient masking, its three mechanisms, the "7 of 9 defenses" evidence, the
joint-pipeline / straight-through / expectation-over-transforms progression, and the bit-depth and
estimator definitions: §2.15.12, Definitions 2.44-2.46 (pp. 102-107). Effectiveness and limits of
adversarial training: §2.15.13 (pp. 107-108). Transform-based defence applied at both train and
inference: §2.15.14 (pp. 108-110). Certification, the bound chain, looseness of post-hoc bounds and
the joint training objective, and the two-layer/binary scope: §2.15.15, Definition 2.47
(pp. 111-113). Reporting table conventions with norm-qualified distance columns and footnoted
combined defenses: Table 2.8 (p. 103). The attack-ladder step numbering and the guarantee-wording
rule are repository conventions built on the masking discussion above.
