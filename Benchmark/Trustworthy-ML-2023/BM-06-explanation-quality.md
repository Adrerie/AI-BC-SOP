# BM-06 — Explanation quality: soundness ladder and end-goal usefulness

**Tier:** Core (model-dependence and ordering checks) + Extended (human and application grounded)

## 1. Target capability / failure mode

**Capability.** An explanation method's output is evidence about *this model* (soundness), and it
moves a human or a process toward the stated end goal (understanding, debugging, trust).

**Failure mode under test.** Explanations that are stable artifacts of the input rather than of the
model; metrics that measure the occlusion operator instead of importance; and evaluations that grade
plausibility against human expectations — confirmation bias — instead of the model's behavior.

## 2. Evaluation hypothesis

- **H-sound** — the attribution changes when the model changes, and tracks the dependence that a
  counterfactual edit detects, under that edit's stated intervention assumptions.
- **H-order** — features ranked most important really are the ones whose removal most changes the
  prediction, relative to a random and to a ground-truth ordering.
- **H-goal** — a human or process performs measurably better with the explanation.

Each hypothesis is separate; satisfying H-order does not establish H-goal, and satisfying an axiom
establishes neither. None of the three establishes **causal feature use in the data-generating sense**:
that reading belongs to
[`SOP-03`](../../SOP/Trustworthy-ML-2023/SOP-03-diagnose-learned-evidence.md) and needs an
identification design on the inputs, which an instrument fitted to the model cannot supply — see the
four contracts in [`SOP-07`](../../SOP/Trustworthy-ML-2023/SOP-07-evaluate-explanation-methods.md) §4.

## 3. Required data and split assumptions

- Model controls: a randomly initialised model, a model trained on randomized labels, and a model
  whose true dependence is known (planted cue or the verdict of
  [`BM-02`](BM-02-spurious-cue-dependence.md)).
- A feature granularity definition that partitions the input (perceptual groups or semantic parts),
  with each region assigned exactly once.
- Evaluation samples drawn from the same split used for the model's task metrics — no separate
  explanation-only subset, or the comparison is confounded.
- For human studies: participant population with the relevant expertise, a task with a measurable
  outcome, and the sample sizes needed for an effect to be detectable.

## 4. Shift or stress construction

- **Model stress (cascading randomization)**: randomize weights from the output layers backwards;
  a sound method's map must change visibly. Report the change quantitatively.
- **Label stress (data randomization)**: train on randomized labels; maps must stop highlighting the
  original task's discriminative regions. Score by rank correlation between the two maps.
- **Planted-dependence stress**: build inputs where the correct attribution is known by
  construction — for example a secondary signal (caption, marker, watermark) whose agreement rate p
  with the label is set by the experimenter. At low noise, attribution must concentrate on the
  planted cue; as it becomes uninformative, attribution must move away from it.
- **Occlusion-operator stress**: repeat the ordering check with several filling operators (constant
  value, blur, inpainting), since the operator is a hyper-parameter of the metric.
- **Cross-method stress**: at least two methods from different linearization families (input-space,
  latent/concept-space, activation-based, training-data attribution), reporting their disagreement.

## 5. Required baselines

| Baseline | Role |
|---|---|
| Random feature ordering | floor for the ordering metric |
| Ground-truth ordering where construction allows it | ceiling for the ordering metric |
| Raw input gradient | simplest sound-ish reference |
| Noise-averaged gradient | the "smoother, less local" comparator |
| Path-integrated attribution | completeness-satisfying comparator |
| Local surrogate and coalition-value attribution | the two stability/assumption contrasts |
| Activation-based localization | architecture-dependent comparator |
| Randomly initialised model's maps | model-dependence control |
| Training-item influence scores (self-influence) for the data-attribution branch | retrieval-quality reference |

## 6. Primary metrics

- `sanity_rankcorr` — rank correlation of attributions between the target model and its randomized
  controls (label and weight), reported per method.
- `remove_classify_auc` — area under the accuracy-versus-removed-features curve, relative to random
  occlusion, lower being a better ordering; reported with the occlusion operator named.

## 7. Secondary / diagnostic metrics

- Change magnitude of the map under cascading randomization (a curve over randomized layers).
- Planted-cue recovery: fraction of attribution mass on the planted cue as a function of the noise
  level p.
- `hitl_delta` — human accuracy or behavior change with versus without the explanation; and, for the
  understanding goal, how well a human predicts the model's decision given the explanation.
- `self_influence_auroc` — for training-sample attribution, retrieval quality on suspicious or
  mislabeled items, with its assumption count stated.
- Cross-method agreement (how often two methods name the same top-k regions).
- Cost per explanation (forward/backward passes, samples, human minutes).

## 8. Aggregation and uncertainty reporting

Report the ordering metric as a curve plus its area, with the baseline curve in the same figure, and
with the number of samples behind each point. Do not average the four remove-and-classify variants
(most-versus-least important, occlude-versus-inpaint) into one number without also reporting their
spread — they can disagree, and the average hides which convention produced the claim. Human results
are reported with effect size, participant count and variance, not with a preference percentage
alone.

## 9. Failure interpretation

| Observation | Reading |
|---|---|
| Map barely changes across models, or is essentially an edge/texture detector | not model-dependent: cannot serve as evidence about this model |
| Random-label model yields informative maps | the method encodes the input, not the learned dependence |
| Good ordering only when occluding with a constant fill | the filling artifact is being measured |
| Best ordering but worst planted-cue recovery | ranks importance without identifying the dependence |
| Methods disagree on the same model | instrument uncertainty; report it rather than picking a favorite |
| Humans rate the explanation highly but do not predict or act better | plausible, not useful; the end-goal hypothesis fails |
| Attribution "improves" after the model is changed | re-check that the comparison held the model fixed |

## 10. Computational reporting

Per method: passes or samples per explanation, whether it needs retraining or architecture access
(which limits it to white-box settings), the cost of the inpainting or generation machinery behind
the occlusion operator, and — for human-grounded tracks — participant hours. Report explanation cost
alongside explanation quality, since a per-sample optimization loop is often the reason a method is
not usable at deployment scale.

## 11. Validity limits

- There is no ground-truth explanation in general; every quantitative check here is a proxy or a
  manufactured case, and a passing score is not proof of soundness.
- Necessary-condition and sanity checks are filters, not certifications: they can disqualify but not
  validate.
- Satisfying a formal axiom (completeness, monotonicity) is a design property; the source explicitly
  declines to treat these axioms as necessities.
- Localization against object boxes measures agreement with human expectations about where objects
  are, not what the model used — a model may legitimately decide from elsewhere.
- Architecture assumptions bound transfer: a method defined through convolutional structure may be
  meaningless for other families.
- Human-grounded results are study designs, not laws: the task, participants and outcome define what
  was shown.
- A demonstrated debugging use is not established by an attribution map; the source records that no
  specialized, successful explanation-based debugging tool is known.

## 12. Related SOPs

Executed by [`SOP-07`](../../SOP/Trustworthy-ML-2023/SOP-07-evaluate-explanation-methods.md);
planted-dependence cases supplied by
[`BM-02`](BM-02-spurious-cue-dependence.md) via
[`SOP-03`](../../SOP/Trustworthy-ML-2023/SOP-03-diagnose-learned-evidence.md); reporting through
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md).


## 13. Source traceability

The instrument itself is audited in [`SOP-07`](../../SOP/Trustworthy-ML-2023/SOP-07-evaluate-explanation-methods.md)
§12, which carries the full source anchor list for the vocabulary (§3.1-§3.4.1), the method
catalogue and its assumptions (§3.5-§3.6.6, §3.10-§3.11), the axioms discussion (§3.5.10), and the
human-in-the-loop framing (§3.8.2). Anchors specific to this benchmark's measurements:

- Pass/fail scoring of model dependence and the rank-correlation readout: §3.7.5
  (book pp. 182-185).
- Manufactured ground truth by controlled cue agreement: §3.7.6 (pp. 185-186).
- Ordering metric, its four variants and relative-area reporting: §3.7.7, Definition 3.14
  (pp. 186-187).
- Occlusion operator as a metric hyper-parameter: §3.7.8 (pp. 187-188).
- Localization is not soundness, and the qualitative-evaluation prohibition: §3.7.3,
  Definition 3.13 (pp. 179-181).
- End goals as the criterion for choosing the evaluation type: §3.8-§3.8.1 (pp. 190-193).
- Cost per explanation for optimization-based and concept-based methods: §3.5.8 (pp. 142-146),
  §3.5.13 (pp. 155-157), §3.11.6-§3.11.7 (pp. 210-214).
- End-goal evaluation of training-sample attribution with AUROC/AP and its stated assumptions:
  §3.12.1-§3.12.2, Definition 3.16 (pp. 214-217).
- Partition-over-overlap granularity rule: §3.5.1, Definition 3.7 (pp. 128-130).

Hypothesis separation, the ladder tiers, and the requirement to report cross-method disagreement are
repository conventions.
