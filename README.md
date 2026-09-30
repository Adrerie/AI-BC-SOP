# AI-BC-SOP

A living research repository for collecting, organizing, and refining **Standard Operating Procedures (SOPs)** and **Benchmarks** for AI and machine learning research.

This repository is not tied to a single topic, textbook, or research direction. It is intended to grow continuously as new books, papers, courses, and research practices are studied. Useful methodological knowledge is gradually converted into reusable SOPs and benchmark specifications.

## Repository Structure

- `SOP/` — reusable research and experimental procedures.
- `Benchmark/` — reusable benchmark designs, evaluation protocols, metrics, and test frameworks.
- `Validation/` — per-source records: identification, pagination/citation convention, and the reconstruction notes that explain which material became an artifact and which stayed theory-only.
- `plans/` — per-source plans describing the scope and boundaries of each reading-to-practice cycle.

## Source Packages

Artifacts are grouped by the source they were reconstructed from. Each package keeps its SOPs, benchmark checks and source record aligned.

| Package | Source | SOPs | Benchmark checks | Source record |
| --- | --- | --- | --- | --- |
| `Deep-Learning-2016` | *Deep Learning*, Goodfellow, Bengio & Courville, MIT Press 2016 (local copy: Simplified Chinese edition, 人民邮电出版社 2017) | [`SOP/Deep-Learning-2016/`](SOP/Deep-Learning-2016/README.md) — 9 | [`Benchmark/Deep-Learning-2016/`](Benchmark/Deep-Learning-2016/README.md) — 12 | [`Validation/Deep-Learning-2016/`](Validation/Deep-Learning-2016/SOURCE.md) |

Packages are reconstructed **by research function, not by chapter**. Material with no reusable procedure or evaluable claim is recorded as theory-only in the package's `concept_reconstruction.md` instead of being forced into an artifact, and era-specific implementation detail is labeled historical rather than promoted to current practice.

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
