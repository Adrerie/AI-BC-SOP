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

- [`Trustworthy-ML-2023/`](Trustworthy-ML-2023/README.md) — 9 benchmarks covering shift generalization,
  cue dependence, confidence truthfulness, error detection, adversarial robustness, explanation quality,
  selective prediction, evaluation integrity, and disclosure/privacy. `BM-09` is a post-book extension
  traced in [`Validation/Trustworthy-ML-Official-Updates-2024-2026/`](../Validation/Trustworthy-ML-Official-Updates-2024-2026/decision_log.md).
- [`Deep-Learning-2016/`](Deep-Learning-2016/README.md) — 11 active benchmark checks for output/loss coupling,
  capacity/data curves, regularization mechanisms, optimization diagnostic probes, long-range dependency,
  implementation health, inductive-bias assumptions, search resolvability, sharing/transfer gains,
  generative-evaluation integrity, and representation quality. Four of the eleven carry clearly marked
  *Modern update (2017–2026)* blocks — an added comparison condition on an existing arm, added
  interpretation rules, added validity limits, and one metric block whose entries each carry the failure
  modes their own source states. No arm was added, no claim under test was changed and no new benchmark was
  created; the judgements behind that are recorded per delta in
  [`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../Validation/Deep-Learning-Modern-2017-2026/delta_map.md).
- [`Lacan-Studies-Preliminary/`](Lacan-Studies-Preliminary/README.md) — **draft**, 3 checks paired one-to-one with the
  preliminary Lacan SOPs. Each tests a specific text-analysis failure (level promotion and demotion across
  need/demand/desire, mechanism over-assignment in metaphor/metonymy, and claim inflation across attribution layers
  and missing devices), with pass cases and deliberately confusable controls. Materials are self-authored neutral vignettes plus paraphrased
  claims carrying locators; no invented book quotation or page. No numeric thresholds are used, because neither
  source supplies a tolerance — pass/fail rests on four observable readouts, and each file's §6 records what the
  trial run actually found.
