# Benchmark

This directory is a growing collection of **Benchmark specifications for AI and machine learning research**.

Each benchmark converts evaluation principles from textbooks, papers, courses, and research practice into a reusable testing framework. Benchmarks may define datasets, splits, stress conditions, metrics, baselines, reporting rules, or combinations of these.

A benchmark should answer questions such as:

- What capability, failure mode, or research claim is being evaluated?
- What data and evaluation conditions are required?
- Which baselines should be included?
- Which metrics should be reported?
- How should comparisons be made?
- What limitations or validity boundaries must be stated?

The directory is not restricted to a single research area. New benchmarks should be added as continued reading introduces new evaluation problems, metrics, or methodological standards.

## Packages

Benchmarks are grouped by the source they were reconstructed from, one directory per package:

- [`Trustworthy-ML-2023/`](Trustworthy-ML-2023/README.md) — 8 benchmarks for shift generalization,
  cue dependence, confidence truthfulness, error detection, adversarial robustness, explanation
  quality, selective prediction, and evaluation integrity.
