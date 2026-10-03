# SOP-05 — Run worst-case stress evaluation

**Stage:** stress · **Tier:** Core + Extended · **Concepts:** C11 threat model, C12 guarantee type,
C10 gaming under attack, C14 cost

## 1. Purpose

Measure what happens to the model under an explicitly bounded worst case. Make sure the number you
report describes the model rather than the failure of your attack. Worst-case evaluation is the only
place where a *guarantee* is on the table. Worst-case evaluation is also the place most easily fooled
into reporting a guarantee that does not exist.

## 2. When to use

- Whenever the deployment claim is adversarial.
- Whenever there is a possibility of active shaping of the environment to make the model fail
  (camouflage, spoofed inputs, manipulation of the acquisition path).
- When you evaluate a defense, including a preprocessing or randomization "defense".
- When a robustness number from the literature is used to justify a choice.
- When semantic perturbations (corruptions, viewpoint, style, geometry) require a bound, even though
  no adversary is assumed.

## 3. Inputs / prerequisites

- A trained model with access decisions settled: weights and gradients (white-box), logits or
  probabilities only, or labels only (black-box).
- A baseline attack implementation with a shared code path for all evaluated models (see
  [`SOP-08`](SOP-08-report-evidence-and-validity-boundaries.md) on shared metric code).
- Compute allowance. Adversarial evaluation multiplies the forward/backward passes per sample. Set the
  budget before you start.
- For the certification branch: the inputs that the *chosen* bound requires. The source's construction
  needs a loss model and an architecture that its relaxation can carry. That condition belongs to that
  method, not to certification in general.

## 4. Definitions needed for execution

- **Threat model** — three parts, all required: **adversarial goal** (which environment counts as
  worst), **strategy space** (the set of environments the adversary may choose from), and
  **knowledge** (what the adversary knows about the model). Leaving any one unspecified means the
  reported robustness has no referent.
- **Worst-case framing** — the target quantity is model performance under the worst allowed
  perturbation inside the declared strategy space. An empirical attack only probes this quantity, and
  the attack may miss stronger failures. A valid certificate can provide a provable guarantee under its
  own assumptions. The three quantities line up in one direction. That line-up needs the same model,
  the same test set and the same threat model. That line-up also needs a correctly implemented attack
  and a correctly implemented bound. The line-up is then **certified robust accuracy ≤ exact
  finite-sample robust accuracy ≤ empirical attacked accuracy under attack suite A**. The statement
  "this attack left 62 % unbroken" therefore does not bound the worst case from below. A certificate at
  40 % does not say that the true worst case is 40 %. The certificate says only that no failure exists
  below that figure inside its assumptions. The ordering is meaningless across different threat models,
  samples or definitions. Never compare a certificate under one norm bound with an attack under another
  norm bound. The worst-case target may also be unrealistically pessimistic relative to the
  true deployment distribution.
- **ε** — the radius bound of the strategy space, always norm-qualified (`ℓ∞`, `ℓ2`, or a total
  variation budget for flow-style transforms).
- **Gradient masking (obfuscated gradients)** — a defense that breaks the gradient path, so a
  gradient-based attack reports safety that is not there. Three mechanisms: shattering, stochasticity,
  exploding/vanishing gradients.
- **Certified evaluation** — establishes a provable robustness guarantee within a specified threat
  model under the assumptions of the chosen certificate. The source illustrates one relaxation-based
  route through the first-order, LP and SDP bounds. That route is an example of certification, not the
  definition of the field.
- **Empirical attack evaluation** — attempts to find violating inputs, and therefore gives evidence
  about robustness. The result is not a proof that the attack found the worst case. A single gradient
  step is a weak diagnostic in the source's setting. Iterative projected attacks are stronger
  references there. Adequacy still depends on the threat model, the defense, and whether the attack is
  adaptive.

## 5. Procedure

**Core**

1. Write the threat model as three sentences: goal, strategy space with norm and radius, knowledge.
   Re-read the threat model against the deployment scenario from
   [`SOP-01`](SOP-01-specify-deployment-setting.md). If the strategy space does not contain the changes
   you actually expect, the evaluation answers a different question.
2. Fix the value of ε early. Keep the value of ε small. Record the norm in which ε is expressed. Keep ε
   *identical across all methods compared*. Perturbations below a visibility threshold stop being
   humanly meaningful. Also record whether the perturbed samples remain plausible.
3. Run the attack suite that is appropriate to the declared threat model. Report each component
   separately. For the multi-step projected attack, report step size, iteration count, restarts,
   projection, clipping, and loss. Include these four components:
   - a single-step attack, as a fast sensitivity diagnostic where applicable
   - a multi-step projected attack, as a reference for gradient-following norm-bounded settings
   - an adaptive attack against the actual defense mechanism and against the full deployed pipeline
   - complementary or targeted variants, when the threat model makes those variants relevant
4. If any part of the system is non-gradient-friendly (cropping, resizing, quantization,
   randomization), attack the **joint pipeline** rather than the differentiable core. Attack that
   pipeline in these three ways:
   - Compose the transforms.
   - Use a straight-through estimator for quantizing steps.
   - Average the gradients over sampled transforms when a single sampled gradient is too noisy to
     optimize.
5. In a black-box setting, state the access level. Count the queries that the attack makes. An
   estimation-of-gradient attack pays a per-coordinate cost. That attack may also require logits
   rather than labels.
6. Report robustness as a curve or a matrix, not as a scalar. Report accuracy versus ε, and the
   training-condition × evaluation-condition matrix. That matrix makes transferability gaps visible.
7. Record the compute ledger: passes per training step, number of epochs added, capacity change, and
   inference overhead (which for attack-time training is typically zero at inference).
8. Run the masking checks in §6 before believing any high robust accuracy.

**Extended** — add for publication-grade robustness claims or safety-relevant deployment:

9. Add the certification branch where the *chosen* certificate's assumptions admit your model and task.
   Report which relaxation you used. Report the assumptions that relaxation needs. Report how loose the
   resulting bound may be. The source states its construction for a shallow network and a binary task.
   Record that fact as the scope of the method described there. State the scope of whichever method you
   actually used. Do not inherit the source's scope as a field limit. A post-hoc certificate can
   be arbitrarily loose. A loss trained with a plain classification objective can inflate the quantity
   that the certificate bounds. If you certify, train for the bound.
10. Add a semantic-stress branch for the non-adversarial case. Use corruptions and geometry/style
    transforms there. Keep the same reporting discipline: a severity sweep, not a single point.
11. Add a plausibility filter to the strategy space when the deployment only ever sees realistic
    inputs. Report both the pessimistic variant and the realistic variant.
12. Add a defense-progress report. For each defense, name the attack that broke that defense. Or record
    the explicit statement "not broken by X, Y, Z at configuration C".

## 6. Mandatory checks

- [ ] **Three-part threat model present**, with no field left implicit.
- [ ] **Strategy-space/goal alignment**: the declared space contains the perturbations that the goal
      calls worst. If the goal is semantic and the space is a pixel ball, say so in the result line.
- [ ] **Masking check**: robust accuracy that rises when the attack is *weakened* or when gradients
      are made unavailable is an artifact. Re-run the joint-pipeline attack (step 4) and compare.
- [ ] **Attack adequacy argued, not counted**: check these four points.

    - The attack family matches the declared threat model and the defense mechanism.
    - Against a defense, the attack is **adaptive**. The attack runs against the full deployed
      pipeline, and the defense's own parameters are known to the attack.
    - Complementary families are run where one family could be blind.
    - The strength claim rests on the configuration — restarts, step count, loss form, gradient
      handling — and not on the iteration count alone.

    Reporting the strongest affordable PGD is a useful floor for one threat model. That report is not
    a sufficient adversarial evaluation in general.
- [ ] **Strongest-attack check**: the reported attack configuration is at least as strong as the
      configuration that established the baseline being beaten. Do not silently reduce the iteration
      count.
- [ ] **ε parity** across all methods, including prior work you quote.
- [ ] **Query accounting** present for every black-box number.
- [ ] **Guarantee wording discipline**: the phrase "no attack found within configuration C" never
      becomes the word "robust". Only a certificate supports the existential claim, and only inside
      that certificate's assumptions.
- [ ] **Transform-defense check, conditioned on a defense that is claimed**: state the training-time
      transformation and the inference-time transformation separately. Then test whether the
      *definition* of that defense requires train-time exposure. Some definitions do. Several
      definitions do not. What is mandatory is the adaptive evaluation of the full deployed pipeline,
      and a check for masking or broken-gradient effects. Training with the transform is not mandatory.

## 7. Decision or stop conditions

- **Stop and rebuild the evaluation** if masking is suspected (high apparent robustness plus a
  benign-looking PGD output on samples the model should fail on). The safety of the model is not
  equivalent to the inability of a gradient-based attack to find a failure.
- **Drop that certificate** if the model violates an assumption of the specific relaxation you planned
  to use. The source states its construction for a simple architecture and a binary task. That
  limitation is a property of **that method**, not a limit on certified robustness as a field. So the
  correct stop is "no guarantee from this bound". That stop is never "certification is impossible for
  my model". Before you write either sentence, list the certificate families you considered. Give why
  you admitted or rejected each family. You may use families outside this source. Cite such a family as
  its own method, with its own assumptions, and mark that family as not source-derived here.
- **Reclassify the claim** from adversarial robustness to corruption robustness if the strategy space
  changes to semantic transforms. That reclassification changes the capability claim. It also changes
  the comparison class. The two claims may share a reporting table. The two claims never share a
  headline number. A model can be robust to one of those classes and defenseless against the other
  class. An ε-ball result says nothing about natural distribution shift.
- **Accept a null result** where the only configurations that survive are ones the adversary cannot
  afford: state the cost asymmetry rather than the margin.

## 8. Common methodological failures

- A report presents single-step-attack accuracy as "adversarial robustness".
- A report leaves the norm implicit. A number without `ℓ∞` or `ℓ2` is not comparable.
- The evaluation changes ε between your method and the baseline.
- The report defends with non-differentiable preprocessing. The evaluation then uses a naive gradient
  attack.
- The report presents a defense whose theoretical optimum is a full failure. Implementation
  imperfection is then given as the justification.
- The report combines a defense with adversarial training. The combination then appears under the
  defense's own name.
- The certification uses a relaxed bound that is loose in exactly the region of interest. The looseness
  is not checked.
- The narrative ignores the cost of the claimed robustness. Or the narrative transfers that cost to
  inference time.
- Dating nothing. A robustness figure or a safety figure is an observation about one model revision,
  against one attack family, at one time. Without the revision date and the attack date, the same claim
  can be true in the report and false in the deployment. A defense that was already broken when the
  measurement was taken is not repaired by a quotation of the old figure.

## 9. Required outputs

- Threat-model statement (goal / strategy space with norm and radius / knowledge).
- Attack configuration record per attack rung, including iteration budget and restarts.
- Robustness curves (accuracy versus ε) and the train × evaluation-condition matrix.
- Query-cost record for black-box settings.
- Masking-check outcome, pass or fail, with the evidence.
- Compute ledger, and the certificate statement with its assumptions if the certification branch ran.

## 10. Minimum reporting requirements

Every robustness number must carry these items:

- the dataset
- the norm, and the value of ε
- the attack used, and that attack's configuration
- whether the attack ran end-to-end through preprocessing
- the compute cost

Comparative tables must keep the distance column norm-qualified. The tables must also mark which rows
combine adversarial training.

## 11. Links to relevant Benchmarks

- [`BM-05`](../../Benchmark/Trustworthy-ML-2023/BM-05-adversarial-robustness.md) — the standardized
  threat-model + attack-ladder + masking-check protocol.
- [`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md) —
  corruption/severity sweeps as the non-adversarial sibling.
- [`BM-04`](../../Benchmark/Trustworthy-ML-2023/BM-04-error-and-anomaly-detection.md) — whether the
  confidence score notices stressed inputs.
- [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md) — audits ε
  parity, configuration reporting, and guarantee wording.
- [`BM-09`](../../Benchmark/Trustworthy-ML-2023/BM-09-disclosure-of-training-data-and-context.md)
  reuses this SOP's access-level ladder and its query accounting. That reuse serves a different
  adversary goal, which is disclosure rather than misbehavior.

## 12. Source traceability

- Educated-guess versus worst-case framing and its pessimism caveat: §2.15 (pp. 86-87).
- Threat-model parts and the "missing critical ingredients" statement: §2.15.1, Definitions 2.36-2.40
  (pp. 87-88).
- Attack formulations for the single-step and projected attacks, non-convexity caveat, and optimiser
  dependence: §2.15.2-§2.15.3 (pp. 89-91).
- Strength ordering and the ε policy: §2.15.4 (pp. 91-92).
- Strategy spaces beyond pixel norms and the total-variation definition: §2.15.5-§2.15.7,
  Definition 2.41 (pp. 92-97).
- White-box versus black-box, substitute models and zeroth-order access requirements with query cost:
  §2.15.8-§2.15.10, Definitions 2.42-2.43 (pp. 93-100).
- Adversarial-training objective, cost ledger, and transferability observation: §2.15.11
  (pp. 101-102).
- Gradient masking and its three mechanisms, and the "7 of 9 defenses" evidence: §2.15.12,
  Definitions 2.44-2.46 (pp. 102-107).
- The joint-pipeline / straight-through / expectation-over-transforms progression, and the bit-depth
  and estimator definitions: §2.15.12 (pp. 102-107).
- Effectiveness and limits of adversarial training: §2.15.13 (pp. 107-108).
- Transform-based defense applied at both train and inference: §2.15.14 (pp. 108-110).
- Certification, the bound chain, looseness of post-hoc bounds and the joint training objective, and
  the two-layer/binary scope: §2.15.15, Definition 2.47 (pp. 111-113).
- Reporting table conventions with norm-qualified distance columns and footnoted combined defenses:
  Table 2.8 (p. 103).
- The attack-ladder step numbering and the guarantee-wording rule are repository conventions built on
  the masking discussion above.

**Scope correction.** The two-layer network and binary-task conditions in §2.15.15 belong to the
construction analyzed there. This SOP reads those conditions as conditions on *that* bound. That
reading is why step 9, §6 and §7 require the family considered and its assumptions. Those sections also
require a statement that other certificates were, or were not, applicable.

The corresponding requirements are **synthesized**:

- argument-based attack adequacy
- adaptive attacks against the mechanism
- train-time exposure only where the defense's definition needs that exposure

The source supplies the masking progression, the attack ladder and the train-and-inference transform
example. The source states no general rule of those forms. The ordering in §4,
`certified ≤ true ≤ empirical`, is likewise ours. That ordering follows from what the two rows are
defined to measure. The book reports the two rows separately. The book does not line the two rows up.
