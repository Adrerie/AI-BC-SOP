# AI-BC-SOP

A living research repository for collecting, organizing, and refining **Standard Operating Procedures (SOPs)** and **Benchmarks** for AI and machine learning research.

This repository is not tied to a single topic, textbook, or research direction. It is intended to grow continuously as new books, papers, courses, and research practices are studied. Useful methodological knowledge is gradually converted into reusable SOPs and benchmark specifications.

## Repository Structure

- `SOP/` — reusable research and experimental procedures.
- `Benchmark/` — reusable benchmark designs, evaluation protocols, metrics, and test frameworks.
- `Validation/` — the audit trail behind each package: what was read from the source, how it was
  reconstructed into SOPs and benchmarks, and whether the result passed its acceptance gates.
- `plans/` — the step plans a package was executed from, kept so the work can be repeated or extended.

Materials are grouped into source-attributed packages. A package collects the SOPs and benchmarks
derived from one studied source under a single directory name, so the procedure text, its validation
record, and its provenance stay together. Currently:

- **Trustworthy ML (2023)** — 8 SOPs and 8 benchmarks for evaluation discipline on real
  deployments: [SOP group](SOP/Trustworthy-ML-2023/README.md),
  [Benchmark group](Benchmark/Trustworthy-ML-2023/README.md),
  [validation record](Validation/Trustworthy-ML-2023/acceptance_report.md),
  [plan](plans/Trustworthy-ML-2023/README.md).

Packages cite the source by section and page; the source documents themselves are not included here.

## Development Principle

The repository follows a reading-to-practice workflow:

```text
Read
↓
Extract methodological principles
↓
Compare with existing research practice
↓
Convert into SOPs or Benchmarks
↓
Refine as new evidence and methods are learned
```

An SOP describes **how a research or evaluation process should be carried out**.

A Benchmark describes **what should be tested, under which conditions, and with which metrics or comparison rules**.

Topics may span trustworthy machine learning, computer vision, multimodal learning, efficient AI systems, model evaluation, robustness, uncertainty, generalization, experimental design, reproducibility, and other areas encountered during continued study.

## Status

This is an evolving knowledge and methodology repository. Existing documents may be revised, expanded, split, or replaced as the literature and our understanding develop.

## License

This repository is released under the MIT License. See [LICENSE](LICENSE) for details.
