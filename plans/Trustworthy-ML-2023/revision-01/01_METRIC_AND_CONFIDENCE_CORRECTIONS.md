# Revision Plan 1 — Metric and confidence corrections

## Goal

Repair mathematical definitions and remove metric semantics that depend on an implicit positive label.

## 1. AUPR baseline

Search all SOP, Benchmark, Validation, and README files for claims equivalent to:

- random AUPR = P(L = 1)
- both AUPR-Success and AUPR-Error share the same random baseline

Replace with the general rule:

> For a precision-recall task, the random/no-skill average-precision or PR baseline is the prevalence of the class designated positive for that task.

Therefore:

- success-positive baseline = P(L = 1)
- error-positive baseline = P(L = 0)
- OOD-positive baseline = P(OOD)
- multiplicity-positive baseline = P(multiple-answer)

Any benchmark using AUPR must explicitly state which class is positive.

## 2. AUROC definition

The package-level metric register must not define AUROC only as:

> probability that a correct case outranks an incorrect one

Replace with a target-agnostic ranking definition:

> probability that a randomly drawn positive example receives a higher score than a randomly drawn negative example, with score orientation and positive class declared.

Then give correctness ranking as one example.

Check BM-03 and BM-04 for orientation consistency.

## 3. Perplexity

Repair the metric register so perplexity is tied to the logarithm base used for NLL.

Preferred wording:

- if NLL uses natural logarithms, perplexity = exp(NLL)
- if cross-entropy is measured in bits using log base 2, perplexity = 2^(NLL_bits)

Do not retain an unconditional "base 2" definition.

## 4. Constant-confidence diagnostic

Separate two concepts.

### Diagnostic oracle control

A constant score equal to **test-set empirical accuracy** can demonstrate ECE degeneracy, but it uses test labels and is therefore an oracle diagnostic only.

It may be used to show a metric weakness, not as a deployable baseline.

### Deployable constant baseline

If a constant confidence is estimated from a separate calibration / validation set and frozen before final testing, it is a legitimate baseline, but it is not guaranteed to achieve zero ECE on the final test.

Update:

- SOP-04
- BM-03
- BM-08 if needed
- SOP-08 metric / control language
- acceptance report examples

## 5. Additional consistency sweep

Search for:

- "random baseline"
- "chance level"
- "positive rate"
- "correct-as-positive"
- "error-as-positive"
- "OOD-positive"
- "perplexity"
- "ECE = 0"
- "constant confidence"

Repair all dependent statements.

## Gate M — Metric correctness

Pass only if:

- all PR tasks declare a positive class
- all AUPR baselines use that positive-class prevalence
- AUROC is target-agnostic in the shared register
- perplexity matches the NLL log base
- oracle constant-confidence and deployable constant-confidence are clearly separated
- no final-test label is used to construct an ordinary baseline
