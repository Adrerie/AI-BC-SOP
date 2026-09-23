# Benchmark group — Trustworthy ML evaluation suite (from *Trustworthy Machine Learning*, 2023)

Reusable benchmark specifications for the claims a trustworthy-ML system makes about itself: that it
generalizes across a change, relies on the right evidence, states usable confidence, notices its own
errors, survives a bounded worst case, explains itself honestly, declines safely — and that the
comparison proving any of this is itself trustworthy.

The suite was derived by reconstructing the source book's methodology rather than by transcribing its
chapters; see [`concept_reconstruction.md`](../../Validation/Trustworthy-ML-2023/concept_reconstruction.md)
and the audited source universe in
[`source_coverage.md`](../../Validation/Trustworthy-ML-2023/source_coverage.md). Source attribution and
the licensing position of this package are recorded in
[`SOURCE.md`](../../Validation/Trustworthy-ML-2023/SOURCE.md); like the SOP group, this is a
provenance-bearing staging unit whose rules are meant to be extended, revised or merged by later
sources.

## The nine components

| ID | Component | Capability under test | Condition axis | Tiering |
|---|---|---|---|---|
| BM-01 | [Distribution-shift generalization](BM-01-distribution-shift-generalization.md) | performance off the training domains | domain, severity, subpopulation, scale | Core / Extended |
| BM-02 | [Spurious-cue dependence](BM-02-spurious-cue-dependence.md) | reliance on a cue that breaks with the correlation | diagonal / off-diagonal cells, ρ | Core / Extended |
| BM-03 | [Confidence truthfulness](BM-03-confidence-truthfulness.md) | probability, calibration, or ordering of `c(x)` | ID vs shifted, imbalance, ambiguity, binning | Core / Extended |
| BM-04 | [Error and anomaly detection](BM-04-error-and-anomaly-detection.md) | detecting own errors, OOD inputs, multiple answers | OOD distance, ambiguity, adversarial, open-set | Core / Extended |
| BM-05 | [Adversarial robustness](BM-05-adversarial-robustness.md) | worst case inside a declared strategy space | ε-ball, semantic transforms, black-box, certification | Core / Extended |
| BM-06 | [Explanation quality](BM-06-explanation-quality.md) | soundness of attributions and their human usefulness | model/label randomization, planted cue, occlusion, HITL | Core / Extended |
| BM-07 | [Selective prediction under cost](BM-07-selective-prediction-under-cost.md) | declining where the system should decline | coverage, cost ratio, drift, escalation | Core / Extended |
| BM-08 | [Evaluation integrity audit](BM-08-evaluation-integrity-audit.md) | whether the comparison itself can be believed | protocol perturbations | Core / Extended |
| BM-09 | [Disclosure of training data and context](BM-09-disclosure-of-training-data-and-context.md) | whether the model reveals what it was fitted on or shown | unit of analysis, access level, exposed channel | Core / Extended — **official-course-derived, not book-derived** |

## Standing integrity rules for this suite

These apply to every component and are the reason the suite exists as a group:

1. A final test set stays independent for a claim only if nothing about the reported system was
   selected from that set's results — no model, threshold, calibration parameter, checkpoint or attack
   choice. Once a selection has been made, the set is development evidence for that claim, and
   re-running the chosen system over it does not restore independence: get a new untouched test, use a
   pre-existing secondary one, or downgrade the claim and disclose.
2. IID validation, shifted validation, and final-test conditions are named separately; a shifted
   validation set changes the setting and therefore the comparison class. Adaptation settings that
   legitimately use target-domain information are in scope — they must simply be declared as what they
   are and scored against methods granted the same access.
3. Every metric states where it is invalid: proper scores mix accuracy and calibration and have an
   unknown floor; `ece` is driven to zero by a constant set equal to the measured correctness rate of
   the scored set — an oracle, not a baseline a deployed model can hold — and depends on the bin
   count; `aupr` is bound to the prevalence of whichever class the task declares positive, so the
   success- and error-positive variants have different random values; `auroc` means nothing until its
   positive class and score orientation are named; `remove_classify_auc` measures the occlusion
   operator too; a distance score confuses novelty with ambiguity.
4. Model capability and confidence quality are scored separately — an accurate model can be blind and
   an uncertain model can rank well.
5. A robustness or fairness *intervention* is never evaluated by the benchmark it was tuned to
   satisfy; re-run the untouched protocol.
6. Report average **and** failure-oriented views (worst cell, worst bin, worst subgroup, risk at
   coverage) whenever they differ in direction.
7. Report cost — compute, memory, labels, human review — next to the gain.
8. Mark oracle or stronger-information rows (for example oracle selection or train-on-target)
   explicitly as upper bounds or stronger-setting references where appropriate. A certified robust
   accuracy is not an upper-bound row: under a valid certificate it is a provable lower bound on the
   true robust accuracy for the stated threat model.

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
the model must not reveal what it knows of a specific item or context -> BM-09
```

BM-08 is mandatory whenever a comparison is used to choose a method; the other eight are selected by
the claim under test.

## Metric names

All components use the metric register in
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md) §4. Names
are not redefined locally; if a component needs a new one, it is added to that register first.

## Where each component comes from

BM-01 through BM-08 reconstruct the book's evaluation methodology and retain their book traceability.
Selected post-book deltas added to those existing benchmarks are traced centrally in the official-update
audit rather than copied into each source section. BM-09 is different: it is wholly new from the Spring
2026 privacy and data-protection session, so its own traceability section cites that course session
instead of a book section and page. The audit trail for all update decisions, including candidates that
were examined and rejected, is
[`../../Validation/Trustworthy-ML-Official-Updates-2024-2026/decision_log.md`](../../Validation/Trustworthy-ML-Official-Updates-2024-2026/decision_log.md).

## What this suite does not cover

Two areas the source discusses were left out of the operational suite, each recorded with its reason
in the coverage audit: the representation-learning showcase whose own evaluation the source labels
qualitative and unguaranteed, and the navigation, legal, historical and research-agenda material that
carries no reusable evaluation procedure.

Learning settings that consume target-domain information are **not** out of scope. Domain adaptation
(§2.4.4), test-time training (§2.4.6), domain- and task-incremental continual learning (§2.4.7,
§2.4.11) and the K-shot / meta-learning variants (§2.4.9-§2.4.10) are first-class entries in the
source's own setting catalogue, and the coverage audit records them as `incorporate` or `supporting`.
This suite evaluates them on the same terms as any other setting: the project declares which setting
it is running, and is compared against methods granted the same access. What the integrity rules
forbid is the mismatch between resources used and setting named — not the use of target information.
