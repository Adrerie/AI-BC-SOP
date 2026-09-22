# SOP-07 — Evaluate an explanation method before using it as evidence

**Stage:** explain · **Tier:** Core + Extended · **Concepts:** C17 attribution as instrument,
C6 diagnosis, C9 proxy gap, C10 gaming

## 1. Purpose

Decide whether a given attribution/explanation output is allowed to serve as evidence about the
model, for a stated end goal. Explanations are the one place where a trustworthy-ML pipeline can
pass every aesthetic test and still be vacuous, so the instrument itself has to be evaluated
before any conclusion drawn from it.

## 2. When to use

- Before citing an attribution map, feature importance, influence score, or concept sensitivity as a
  reason for a model's behavior.
- When choosing among explanation methods for a debugging or auditing workflow.
- When an explanation is being offered to a decision-maker as grounds for trust.
- When a claimed explanation-based end goal (debugging, understanding, trust) must be verified.

## 3. Inputs / prerequisites

- Models to be explained, including controls: a randomly initialised model, a model trained on
  randomized labels, and — where available — a model with a *known* dependence from
  [`SOP-03`](SOP-03-diagnose-learned-evidence.md).
- A feature granularity decision (raw inputs, perceptual groups, latent units, semantic parts) and
  the tooling to realize it.
- An occlusion/filling operator with a stated rationale, or an inpainting/blurring alternative.
- For human evaluation: a task, participants with relevant expertise, and a measurable outcome.
- Candidate methods spanning the linearization types (input-space, latent-space, concept-space,
  training-data attribution).

## 4. Definitions needed for execution

- **Explanation** — an answer to a why-question; **interpretability** — a human's degree of
  understanding of the cause of a decision; **explainability** — the same degree *after* receiving
  an explanation; **justification** — an account of why a decision is good, which need not be sound.
- **Attribution** — assigning reasons to factors of one of three kinds: input features, training
  samples, or model parameters.
- **Soundness (faithfulness)** — the explanation identifies the true causes of the prediction, i.e.
  of *this model's* behavior.
- **Completeness / monotonicity axioms** — formal properties some attribution scores satisfy; useful
  as design constraints, not as proof that an explanation is sound or useful.
- **The soundness–explainability trade-off** — a simplification cannot be both fully faithful and
  fully understandable; methods sit on a frontier, so none is "correct by construction".
- **Ground-truth explanation** — does not exist in general; where one is needed, it must be
  manufactured by construction (simulated inputs, controlled noise, planted dependence).
- **Remove-and-classify** — occlude features in the order an attribution ranking dictates and
  measure the accuracy drop relative to a random-occlusion baseline; usually summarised by area
  under the curve, lower meaning the ranking tracked true importance.

## 5. Procedure

**Core**

1. Fix the end goal first and write it as a falsifiable question: debugging ("will this tell me what
   to change?"), understanding ("can a human predict the model's behavior from it?"), or
   trust/approval ("does it change the decision-maker's accuracy or calibration?"). Attribution is
   an intermediate step; a method may be sound and still not serve the goal.
2. Choose the attribution target (input features / training samples / parameters) and the
   granularity. Prefer a *partition* of the input (perceptual groups or semantic parts) over a set of
   overlapping instance masks, so that every region is accounted for exactly once.
3. Verify model dependence before interpreting anything: compute the map for the randomly
   initialised control. The requirement is not that the map be informationless — a random network can
   still carry structure — but that the map change visibly when the model changes.
4. Run the label-randomisation check: a model trained on randomized labels must not yield maps that
   highlight the features discriminative for the original task. Score it quantitatively (rank
   correlation between the true-label and random-label maps), not by eye.
5. Run an ordering check on a subset where the true dependence is known by construction: simulated
   inputs with a planted, controllable cue (for example a secondary signal whose agreement rate with
   the label you set), or the `SOP-03` counterfactual cases. The method must attribute to the planted
   cue at high agreement and must *stop* doing so when the planted cue becomes uninformative.
6. Run remove-and-classify with a stated occlusion operator and a random-occlusion baseline; report
   the curve and its area. Run the occlusion-informativeness check: does the filling value itself
   carry class information (see §8)?
7. Compare across at least two methods of different linearization type. Where they disagree, do not
   average them into a conclusion — record the disagreement as the finding and check which one passed
   steps 3-5.
8. Decide and log: usable-as-evidence for this goal / usable-with-caveats / not usable.

**Extended** — add when the explanation is a deliverable, or when human action depends on it:

9. Add a human-grounded study: participants judge explanation quality or predict model behavior with
   and without the explanation; report the effect size and the task.
10. Add an application-grounded study on the real task (debugging throughput, expert decision
    accuracy), accepting that this is the most expensive and the most aligned option.
11. For training-sample attribution, evaluate against the end goal (find suspicious or mislabelled
    training items and check retrieval quality with ranking metrics) rather than only against an
    expensive retraining approximation; state how many mislabels the setup assumes and whether
    systematic mislabelling is excluded.
12. For concept-level or latent-space methods, verify the separability assumption the method needs
    (a concept direction that a linear probe can recover) and report the failure when it does not
    hold, for example with architectures whose latent geometry the method was not designed for.
13. Report a cost line: explanations differ by orders of magnitude in added compute and in
    human review time.

## 6. Mandatory checks

- [ ] **Model-dependence check** passed (step 3) before any interpretive claim.
- [ ] **Random-label check** passed and quantified (step 4).
- [ ] **Known-dependence check** present: at least one case where the correct answer is fixed by
      construction (step 5).
- [ ] **Occlusion operator declared** with its rationale, and an alternative operator run at least
      once, because the choice is a hyper-parameter of the metric.
- [ ] **Baseline row** present: random ordering, and — where available — the ground-truth ordering.
- [ ] **No plausibility criterion**: the result line may not rest on "the map looks reasonable".
- [ ] **Axiom language bounded**: satisfying an axiom is reported as a design property, never as
      proof of soundness or usefulness.
- [ ] **Goal match**: the evaluation type (functional / human / application grounded) is the one the
      stated end goal requires; a functional evaluation may not be presented as evidence of
      human understanding.

## 7. Decision or stop conditions

- **Stop: the instrument is not model-dependent.** If the map barely changes across models, or is
  essentially an edge/texture detector, it cannot be used as evidence about *this* model.
- **Stop: no ground truth reachable.** If neither simulated inputs nor a planted dependence is
  available for your modality, report the attribution as descriptive only and route the decision
  through counterfactual evaluation (`SOP-03`) instead.
- **Reclassify the claim** from "explains the model" to "explains the prediction pipeline" if only
  functional-grounded evidence exists.
- **Do not ship an explanation-based assurance** if the human-grounded study shows no effect on the
  decision-maker's behavior.
- **Accept and report** the debugging-goal limitation directly: an attribution output is not, by
  itself, a demonstrated route to fixing a systematic model failure.

## 8. Common methodological failures

- Confirmation bias: grading the explanation against what a human thinks the cause should be.
- Localization-as-soundness: rewarding maps that cover the object's bounding box even though the
  model may have decided from background or artifacts.
- Cherry-picked qualitative figures standing in for a measurement.
- Reading a completeness axiom as a soundness proof.
- Occluding with a constant value that is itself class-informative, so the metric measures the
  filling artifact rather than importance — and, symmetrically, treating random occlusion as the
  worst possible baseline when it can add confusing structure.
- Averaging the four remove-and-classify variants into one number without reporting that the variants
  can disagree.
- Reusing an attribution method beyond the architecture family it was defined for.
- Presenting a functionally-grounded proxy result as an answer to a human-understanding question.

## 9. Required outputs

- End-goal statement with the falsifiable question and chosen evaluation type.
- Granularity/partition definition and the occlusion operator(s) used.
- Control results: random-initialisation sensitivity, random-label score (quantified), known-cue
  check.
- Remove-and-classify curves with baseline, plus the area and its variance across operators.
- Cross-method disagreement log, with which checks each method passed.
- Usability decision per method per goal.

## 10. Minimum reporting requirements

For every explanation-based claim, report: which method, which target and granularity, which model
controls it passed, which occlusion operator the metric used, the human/application evidence if the
claim is about understanding or trust, and the added cost. If the map is offered as evidence for a
fix, state what changed in the model afterwards and how it was measured.

## 11. Links to relevant Benchmarks

- [`BM-06`](../../Benchmark/Trustworthy-ML-2023/BM-06-explanation-quality.md) — the standardized
  ladder of controls and its metrics.
- [`BM-02`](../../Benchmark/Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md) — supplies the
  planted-dependence cases used in step 5.
- [`BM-04`](../../Benchmark/Trustworthy-ML-2023/BM-04-error-and-anomaly-detection.md) — for the
  training-data attribution branch, whose end goal is detection of bad data.
- [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md) — audits
  baseline and operator disclosure.

## 12. Source traceability

Explanation/interpretability/explainability/justification and attribution targets: §3.1-§3.1.2,
Definitions 3.1-3.6 (pp. 117-118). Properties of good explanations: §3.3.1 (pp. 122-123).
Taxonomy and the soundness–explainability trade-off: §3.4-§3.4.1 (pp. 124-127); linearization types
§3.6.6 (pp. 176-177); no attribution method is fully sound and fully explainable: §3.5.3 (p. 135).
Why empirical evaluation is required: §3.7.1 (p. 178). Evaluation types and their cost ladder:
§3.7.2 (pp. 178-179). Confirmation bias and the rejection of qualitative-only evidence: §3.7.3,
Definition 3.13 (pp. 179-181); the localization fallacy and "we should not evaluate according to our
expectations": §3.7.3 (p. 181). Necessary conditions and their relaxation: §3.7.4 (pp. 181-182).
Sanity checks (cascading randomisation, label randomisation, rank correlation) and the explicit
conflict with completeness axioms: §3.7.5 (pp. 182-185). Simulated inputs with controllable ground
truth: §3.7.6 (pp. 185-186). Remove-and-classify and its variants: §3.7.7, Definition 3.14
(pp. 186-187). Missingness bias and the occlusion-operator caveat: §3.7.8 (pp. 187-188). End goals
and the absence of a demonstrated debugging use case: §3.8-§3.8.1 (pp. 190-193). Human-in-the-loop
evaluation: §3.8.2, Definition 3.15 (pp. 189-193). Feature granularity and partition preference:
§3.5.1, Definition 3.7 (pp. 128-130). Method-specific assumptions (concept separability,
architecture transfer): §3.5.13, §3.5.14, §3.5.16-§3.5.19 (pp. 153-174). Training-sample attribution
and its end-goal evaluation with self-influence: §3.11.1, §3.12.1-§3.12.2, Definition 3.16
(pp. 203, 214-217). Axioms are not necessities: §3.5.10 (p. 150). Control-first ordering and the
usability log are repository conventions.
