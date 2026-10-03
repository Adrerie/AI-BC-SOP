# Benchmark group — Trustworthy ML evaluation suite

Reusable benchmark specifications cover the claims a trustworthy-ML system makes about itself. Each
claim is that the system does one of the following:

- generalizes across a change
- relies on the right evidence
- states usable confidence
- notices its own errors
- survives a bounded worst case
- explains itself honestly
- declines safely

The suite also tests the comparison that proves any of those claims. That comparison must itself be
trustworthy.

BM-01 through BM-08 come from a reconstruction of the 2023 book's methodology, not from a
transcription of its chapters. BM-09 and selected later extensions come from the official post-book
course lineage. See [`concept_reconstruction.md`](../../Validation/Trustworthy-ML-2023/concept_reconstruction.md)
and the audited source universe in
[`source_coverage.md`](../../Validation/Trustworthy-ML-2023/source_coverage.md).
[`SOURCE.md`](../../Validation/Trustworthy-ML-2023/SOURCE.md) records the source attribution and the
licensing position of the package. The package is a provenance-bearing staging unit, like the SOP
group. Later sources may extend, revise or merge the rules of that unit.

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

The rules below apply to every component. The rules are the reason the suite exists as a group:

1. A final test set supports a claim only while the test set stays independent. Independence holds
   only when no choice about the reported system came from that set's results. The choices cover the
   model, the threshold, the calibration parameter, the checkpoint and the attack. Once the project
   selects from the set, the set is development evidence for that claim. Re-running the chosen system
   over the set does not restore independence. Follow one of these three routes:
   - Get a new untouched test.
   - Use a pre-existing secondary test.
   - Downgrade the claim and disclose.
2. Name the IID validation, the shifted validation and the final-test conditions separately. A
   shifted validation set changes the setting and therefore the comparison class. Adaptation
   settings that legitimately use target-domain information are in scope. Declare such a setting as
   what the setting is. Score that setting against methods granted the same access.
3. Report where each metric is invalid. The register gives the reason per metric:
   - Proper scores mix accuracy and calibration, and have an unknown floor.
   - A constant set equal to the measured correctness rate of the scored set drives `ece` to zero.
     That constant is an oracle, not a baseline a deployed model can hold. The value of `ece` also
     depends on the bin count.
   - `aupr` tracks the prevalence of whichever class the task declares positive. So the
     success-positive variant and the error-positive variant have different random values.
   - `auroc` means nothing until the report names its positive class and score orientation.
   - `remove_classify_auc` measures the occlusion operator too.
   - A distance score confuses novelty with ambiguity.
4. Score model capability and confidence quality separately. An accurate model can be blind, and an
   uncertain model can rank well.
5. Do not evaluate a robustness or fairness *intervention* by the benchmark that the intervention's
   own tuning targeted. Re-run the untouched protocol instead.
6. Report average **and** failure-oriented views (worst cell, worst bin, worst subgroup, risk at
   coverage) whenever the two differ in direction.
7. Report cost (compute, memory, labels, human review) next to the gain.
8. Mark oracle or stronger-information rows (for example oracle selection or train-on-target)
   explicitly as upper bounds or as stronger-setting references, where appropriate. A certified
   robust accuracy is not an upper-bound row. Under a valid certificate, a certified robust accuracy
   is a provable lower bound. The bound holds for the true robust accuracy of the stated threat
   model.

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

BM-08 is mandatory whenever the project uses a comparison to choose a method. The claim under test
selects the other eight components.

## Metric names

All components use the metric register in
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md) §4.
Components do not redefine names locally. When a component needs a new name, the project adds that
name to the register first.

## Where each component comes from

BM-01 through BM-08 reconstruct the book's evaluation methodology and retain their book traceability.
Selected post-book deltas add to those existing benchmarks. The official-update audit records each
delta centrally, rather than copying the delta into each source section. BM-09 is different. It is
wholly new from the Spring 2026 privacy and data-protection session. The traceability section of
`BM-09` therefore cites that course session, instead of a book section and page. The audit trail for
all update decisions, including candidates that the project examined and rejected, is
[`../../Validation/Trustworthy-ML-Official-Updates-2024-2026/decision_log.md`](../../Validation/Trustworthy-ML-Official-Updates-2024-2026/decision_log.md).

## What this suite does not cover

The source discusses two areas that the operational suite leaves out. The coverage audit records the
reason for each. The first area is the representation-learning showcase, whose own evaluation the
source labels qualitative and unguaranteed. The second area is the navigation, legal, historical and
research-agenda material, which carries no reusable evaluation procedure.

Learning settings that consume target-domain information are **not** out of scope. The source's own
catalogue of learning settings treats the following as first-class entries:

- domain adaptation (§2.4.4)
- test-time training (§2.4.6)
- domain- and task-incremental continual learning (§2.4.7, §2.4.11)
- the K-shot / meta-learning variants (§2.4.9-§2.4.10)

The coverage audit records those settings as `incorporate` or `supporting`. This suite evaluates
those settings on the same terms as any other setting. The project declares which setting the run
uses. The suite then compares that run against methods granted the same access. What the integrity
rules forbid is the mismatch between resources used and setting named, not the use of target
information.
