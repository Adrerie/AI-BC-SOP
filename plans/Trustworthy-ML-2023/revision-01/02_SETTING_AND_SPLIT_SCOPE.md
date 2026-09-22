# Revision Plan 2 — Setting and split scope

## Goal

Replace universal prohibitions with information-rights rules tied to the declared learning setting.

## 1. Rewrite the governing integrity principle

Across SOP-01, SOP-02, group READMEs, BM-08, and related files, replace variants of:

- deployment data must never enter development
- target-domain data are always leakage
- target labels automatically invalidate the project
- deployment-stage supervision is forbidden by the suite

with:

> A method may use only the information rights granted by its declared setting. Use of additional target/deployment information changes the setting and therefore the valid comparison class, unless that information was already declared as part of the setting.

Examples:

- domain generalization: target-domain data may be prohibited
- unsupervised domain adaptation: unlabeled target-domain data are allowed
- supervised domain adaptation: labeled target-domain data are allowed
- test-time adaptation: specified test-time information is allowed
- continual learning: post-deployment updates may be allowed
- ordinary IID supervised learning: standard validation is allowed

Do not treat these as integrity failures merely because they use target information.

## 2. Fix SOP-01 one-type rule

The current rule says each project must classify the claim into exactly one generalization type.

Replace with:

- each **reported claim / result** must have a clearly defined condition and setting
- multi-axis evaluations are allowed
- do not collapse heterogeneous conditions into one scalar without a justified aggregation rule

A single project may evaluate domain shift, corruption, subgroup shift, and adversarial stress separately.

## 3. Fix split construction

SOP-02 currently says partition by provenance group, not randomly, as a universal rule.

Replace with a conditional rule:

- if observations are correlated through subject, site, device, time, household, sequence, plot, patient, source document, or another leakage unit, split by the highest relevant independence unit
- if IID samples are genuinely independent and identically distributed for the target claim, random splitting is valid
- the chosen split unit must be justified by the claim and data-generating process

## 4. Final-test contamination

Explicitly state:

If final-test outcomes influenced any selection decision, then that test set has become development evidence for the affected claim.

Allowed responses:

1. obtain a new untouched final test drawn from the intended evaluation distribution
2. use a pre-existing untouched secondary test set
3. downgrade the claim and disclose that no independent final test remains

Not allowed:

- simply rerun the chosen model on the same contaminated test and call independence restored

## 5. Pretraining and zero-shot wording

Replace overbroad rules such as "target classes in pretraining means zero-shot is unavailable" with a more precise disclosure rule.

Distinguish:

- no task-specific examples or adaptation
- class-name or semantic exposure during pretraining
- exact or near-duplicate contamination
- benchmark-specific fine-tuning

Require explicit disclosure rather than a universal terminology ban unless the term has a formal definition in the benchmark.

## Gate S — Setting correctness

Pass only if:

- integrity is defined relative to declared information rights
- legitimate adaptation settings are no longer mislabeled as violations
- split strategy is conditional on the dependence structure
- contaminated final tests cannot be "repaired" by rerunning the same set
- multi-axis projects are permitted while claim-level conditions stay explicit
