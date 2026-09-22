# Revision Plan 3 — Causal, mitigation, and decision language

## Goal

Ensure the package distinguishes evidence, identification, and decision policy.

## 1. Counterfactual cue diagnostics

Audit SOP-03 and BM-02 for statements such as:

- no performance drop means the model did not use the cue
- a performance drop confirms dependence
- a single edit identifies the causal feature

Replace with language calibrated to the design.

Preferred structure:

- cue removal/editing tests sensitivity or necessity under the chosen intervention
- lack of degradation does not prove non-use because cues may be redundant or compensatory
- degradation may reflect distribution shift or editing artifacts
- stronger causal interpretation requires intervention validity and an identification argument

Retain strong conclusions only when the benchmark construction actually makes them identifiable.

## 2. Explanation evidence

BM-06 and SOP-07 should keep the distinction between:

- model dependence sanity checks
- attribution ordering
- end-goal usefulness
- causal explanation

Do not let explanation quality imply causal feature use by default.

## 3. Mitigation selection

Rewrite SOP-06 so its method menus are examples conditioned on ingredients, not universal routing rules.

For every candidate method record:

- required supervision / information
- assumptions
- objective it optimizes
- compute / label / human cost
- expected trade-offs
- which Benchmark evaluates the intended improvement

Do not equate arbitrary group labels with domain labels.

Do not hard-code a universal numeric boundary such as ≤1% unless clearly labeled as a source-specific experimental regime, not a general threshold.

## 4. Baseline comparison

Replace:

> reject the candidate if it fails to beat the tuned simple baseline

with a decision based on declared objectives.

A method may be justified if it improves a required axis such as:

- worst-group risk
- calibration
- robustness
- coverage at risk
- compute
- memory
- latency
- annotation cost

while accepting a trade-off elsewhere.

Require Pareto-style or constraint-based comparison when objectives conflict.

## 5. Abstention

Abstention is not an automatic fallback.

Before an abstention policy is accepted, require:

- an informative score or decision rule
- validation of ranking / calibration appropriate to the use
- an evaluated risk-coverage or cost-coverage relation
- a feasible fallback path
- fallback capacity and cost

If these do not exist, output should be "no validated action policy", not automatically "abstain".

## Gate C — Evidential discipline

Pass only if:

- counterfactual edits are not overinterpreted causally
- mitigation menus are scoped examples, not rigid universal routing
- no unsupported numeric supervision threshold acts as a general rule
- simple baselines are necessary comparison points but not universal winners
- abstention requires a validated selection signal and fallback process
