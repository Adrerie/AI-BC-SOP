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

| Package | Source | Contents |
| --- | --- | --- |
| [`Deep-Learning-2016/`](Deep-Learning-2016/README.md) | *Deep Learning*, Goodfellow, Bengio & Courville, MIT Press 2016 (local copy: Simplified Chinese edition, 人民邮电出版社 2017) | 12 benchmark checks, each tied to a claim the book actually makes: output-unit/loss coupling, capacity and data-size curves, regularization mechanisms, adversarial linearity, optimization-pathology separability, long-range dependency, implementation-health instruments, inductive-bias assumptions, search efficiency and resolvability, sharing gains versus labeled data, generative-evaluation integrity, representation quality. |

A model family is not a benchmark: architectures appear only where a distinct evaluable claim attaches. Each package keeps its source record under `Validation/<Package>/` and its executing procedures under `SOP/<Package>/`.
