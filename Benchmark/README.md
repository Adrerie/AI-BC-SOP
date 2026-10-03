# Benchmark

The Benchmark directory is a growing collection of **Benchmark specifications for AI and machine learning research**.

Each benchmark converts evaluation principles from textbooks, papers, courses, and research practice into a reusable testing framework. A benchmark may define datasets, splits, stress conditions, metrics, baselines, and reporting rules, or a combination of these.

A benchmark answers the following:

- the capability, failure mode, or research claim under evaluation
- the data and the evaluation conditions it requires
- the baselines to include
- the metrics to report
- how to make the comparisons
- the limitations and the validity boundaries to state

The directory covers more than one research area. Add a new benchmark when further reading introduces new evaluation problems, metrics, or methodological standards.

## Packages

Group benchmarks by the source they reconstruct. Each package has one directory:

- [`Trustworthy-ML-2023/`](Trustworthy-ML-2023/README.md) — 9 benchmarks covering shift generalization,
  cue dependence, confidence truthfulness, error detection, adversarial robustness, explanation quality,
  selective prediction, evaluation integrity, and disclosure and privacy. `BM-09` is a post-book extension
  traced in [`Validation/Trustworthy-ML-Official-Updates-2024-2026/`](../Validation/Trustworthy-ML-Official-Updates-2024-2026/decision_log.md).
- [`Deep-Learning-2016/`](Deep-Learning-2016/README.md) — 11 active benchmark checks that cover the following
  areas. They check output and loss coupling, capacity and data curves, regularization mechanisms,
  optimization diagnostic probes, and long-range dependency. They also check implementation health,
  inductive-bias assumptions, search resolvability, sharing and transfer gains, generative-evaluation
  integrity, and representation quality. Four of the eleven carry clearly marked
  *Modern update (2017–2026)* blocks. Those blocks add a comparison condition on an existing arm,
  interpretation rules, validity limits, and one metric block. Each entry in that metric block carries the
  failure modes that its own source states. The update added no arm, changed no claim under test, and created
  no new benchmark. The judgements behind that are recorded per delta in
  [`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../Validation/Deep-Learning-Modern-2017-2026/delta_map.md).
