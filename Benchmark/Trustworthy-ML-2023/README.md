# Benchmark group — Trustworthy ML evaluation suite (from *Trustworthy Machine Learning*, 2023)

Reusable benchmark specifications for the claims a trustworthy-ML system makes about itself: that it
generalizes across a change, relies on the right evidence, states usable confidence, notices its own
errors, survives a bounded worst case, explains itself honestly, declines safely — and that the
comparison proving any of this is itself trustworthy.

The suite was derived by reconstructing the source book's methodology rather than by transcribing its
chapters; see [`concept_reconstruction.md`](../../Validation/Trustworthy-ML-2023/concept_reconstruction.md)
and the audited source universe in
[`source_coverage.md`](../../Validation/Trustworthy-ML-2023/source_coverage.md).

## The eight components

| ID | Component | Capability under test | Condition axis | Tiering |
|---|---|---|---|---|
| BM-01 | [Distribution-shift generalization](BM-01-distribution-shift-generalization.md) | performance off the training domains | domain, severity, subpopulation, scale | Core / Extended |
| BM-02 | [Spurious-cue dependence](BM-02-spurious-cue-dependence.md) | reliance on a cue that breaks with the correlation | diagonal / off-diagonal cells, ρ | Core / Extended |
| BM-03 | [Confidence truthfulness](BM-03-confidence-truthfulness.md) | probability, calibration, or ordering of `c(x)` | ID vs shifted, imbalance, ambiguity, binning | Core / Extended |
| BM-04 | [Error and anomaly detection](BM-04-error-and-anomaly-detection.md) | detecting own errors, OOD inputs, multiple answers | OOD distance, ambiguity, adversarial, open-set | Core / Extended |
| BM-05 | [Adversarial robustness](BM-05-adversarial-robustness.md) | worst case inside a declared strategy space | ε-ball, semantic transforms, black-box, certification | Core / Extended |
| BM-06 | [Explanation quality](BM-06-explanation-quality.md) | soundness of attributions and their human usefulness | model/label randomisation, planted cue, occlusion, HITL | Core / Extended |
| BM-07 | [Selective prediction under cost](BM-07-selective-prediction-under-cost.md) | declining where the system should decline | coverage, cost ratio, drift, escalation | Core / Extended |
| BM-08 | [Evaluation integrity audit](BM-08-evaluation-integrity-audit.md) | whether the comparison itself can be believed | protocol perturbations | Core / Extended |

## Standing integrity rules for this suite

These apply to every component and are the reason the suite exists as a group:

1. The final test set is never used for model, threshold, calibration-parameter, or attack selection.
2. IID validation, shifted validation, and final-test conditions are named separately; a shifted
   validation set changes the setting and therefore the comparison class.
3. Every metric states where it is invalid: proper scores mix accuracy and calibration and have an
   unknown floor; `ece` is gameable by a constant score and depends on the bin count; `aupr` is
   base-rate bound; `remove_classify_auc` measures the occlusion operator too; a distance score
   confuses novelty with ambiguity.
4. Model capability and confidence quality are scored separately — an accurate model can be blind and
   an uncertain model can rank well.
5. A robustness or fairness *intervention* is never evaluated by the benchmark it was tuned to
   satisfy; re-run the untouched protocol.
6. Report average **and** failure-oriented views (worst cell, worst bin, worst subgroup, risk at
   coverage) whenever they differ in direction.
7. Report cost — compute, memory, labels, human review — next to the gain.
8. Mark every upper-bound row (oracle selection, train-on-target, post-hoc certificate) as such.

## How to pick components

```text
only task performance matters                 -> BM-01
suspect the model answers a different question -> BM-02
a number is reported as confidence/probability -> BM-03
the system must notice its own failures        -> BM-04 (+ BM-07 to act on it)
inputs can be adversarially manipulated        -> BM-05
explanations are offered as evidence           -> BM-06
decisions have asymmetric costs                -> BM-07
comparing methods or inheriting a leaderboard   -> BM-08 (always)
```

BM-08 is mandatory whenever a comparison is used to choose a method; the other seven are selected by
the claim under test.

## Metric names

All components use the metric register in
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md) §4. Names
are not redefined locally; if a component needs a new one, it is added to that register first.

## What this suite does not cover

Two evaluation areas the source discusses were deliberately left out of the operational suite, each
recorded with its reason in the coverage audit: (a) benchmarks that require deployment-stage
supervision the integrity rules here forbid (domain adaptation with labelled targets, test-time
training, continual and few-shot variants), and (b) the representation-learning showcase whose own
evaluation the source labels qualitative and unguaranteed. The book's forward-looking research agenda
and its historical narrative are likewise not operationalised.
