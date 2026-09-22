# Plan 4 — Benchmark Group

## Goal

Create a reusable Benchmark suite that evaluates trustworthy-ML capabilities and failure modes identified during reconstruction.

## Output Location

`Benchmark/Trustworthy-ML-2023/`

Create an index:

`Benchmark/Trustworthy-ML-2023/README.md`

and multiple benchmark documents or benchmark components.

## Benchmark Design Principle

A Benchmark is not merely a list of datasets or metrics.

Each benchmark component must state:

- what capability or claim is being tested
- under which data/distribution conditions
- against which baselines
- with which metrics
- how results are aggregated
- what constitutes degradation or failure
- which limitations remain outside the benchmark

## Required Coverage Dimensions

Derive the actual dimensions from the source audit, but explicitly consider whether the book supports evaluation of:

- IID task performance
- distribution shift and OOD generalization
- robustness to corruptions or perturbations
- uncertainty quality
- calibration
- error detection
- selective prediction / abstention
- subgroup or worst-case behavior
- computational or scalability cost
- explainability-related evaluation, if operationally justified by the source

Do not include a dimension merely because it appears in this list. Include it only when justified by the reconstructed source content.

## Mandatory Benchmark Schema

Each benchmark specification must contain:

1. **Target capability / failure mode**
2. **Evaluation hypothesis**
3. **Required data and split assumptions**
4. **Shift or stress construction**
5. **Required baselines**
6. **Primary metrics**
7. **Secondary / diagnostic metrics**
8. **Aggregation and uncertainty reporting**
9. **Failure interpretation**
10. **Computational reporting**
11. **Validity limits**
12. **Related SOPs**
13. **Source traceability**

## Core vs Extended Benchmark

Where appropriate, create:

- **Core benchmark**: low-friction minimum evaluation
- **Extended benchmark**: stronger stress testing, multiple shifts, subgroup analysis, or additional cost analysis

This prevents the benchmark from being unusably heavy while retaining a rigorous publication-grade path.

## Benchmark Integrity Rules

- Never use the final test set for model or threshold selection.
- Distinguish IID validation, shifted validation, and final test conditions when relevant.
- State when a metric is invalid or misleading under class imbalance, selective coverage, distribution shift, or other conditions.
- Separate model capability from confidence quality.
- Separate a robustness intervention from the benchmark used to evaluate it.
- Report both average and failure-oriented views when the source supports them.

## Gate D — Benchmark Quality

Pass only if:

- each benchmark has a clearly defined target capability
- metrics are tied to explicit questions rather than listed generically
- data leakage and test-set tuning are explicitly prevented where relevant
- benchmark components can compare methods fairly
- each major benchmark component links back to the SOP group
