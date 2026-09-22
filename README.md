# AI-BC-SOP

A living research repository for collecting, organizing, and refining **Standard Operating Procedures (SOPs)** and **Benchmarks** for AI and machine learning research.

This repository is not tied to a single topic, textbook, or research direction. It is intended to grow continuously as new books, papers, courses, and research practices are studied. Useful methodological knowledge is gradually converted into reusable SOPs and benchmark specifications.

## Repository Structure

- `SOP/` — reusable research and experimental procedures.
- `Benchmark/` — reusable benchmark designs, evaluation protocols, metrics, and test frameworks.
- `Validation/` — the audit trail behind each package: what was read from the source, how it was
  reconstructed into SOPs and benchmarks, and whether the result passed its acceptance gates.
- `plans/` — the step plans a package was executed from, kept so the work can be repeated or extended.

## What a source package is, and what it becomes

Materials are grouped into **source-attributed packages**. A package collects the SOPs and benchmarks
derived from one studied source under a single directory name, so the procedure text, its validation
record, and its provenance stay together. Currently:

- **Trustworthy ML (2023)** — 8 SOPs and 8 benchmarks for evaluation discipline on real
  deployments: [SOP group](SOP/Trustworthy-ML-2023/README.md),
  [Benchmark group](Benchmark/Trustworthy-ML-2023/README.md),
  [validation record](Validation/Trustworthy-ML-2023/acceptance_report.md),
  [source attribution](Validation/Trustworthy-ML-2023/SOURCE.md),
  [plan](plans/Trustworthy-ML-2023/README.md).

Packages cite the source by section and page; the source documents themselves are not included here.

A package is a **provenance-bearing staging unit**, not a permanent shelf. It exists so that a rule can
be traced to the reading that produced it while that rule is still mostly one book's way of seeing the
problem. The intended end state of a good rule is *not* to stay inside the package that introduced it:
as later sources are read, their insights may

- **extend** an existing canonical SOP or Benchmark,
- **revise** a rule already there,
- **supersede** an earlier source-derived rule,
- **merge** with several sources into a canonical artifact that names all of them, or
- **remain source-specific** when the rule only makes sense inside that source's framing.

The change should leave a paper trail: a superseded rule stays visible in the package that carried it
rather than being deleted, so a later reader can see which source held which position and when.
Nothing here implies each future source must live in its own forever-isolated silo, and nothing implies
the opposite — that packages should be dissolved as soon as a merged file exists.

`Trustworthy-ML-2023` is therefore kept as the repository's first source package: a traceability record
and a stable snapshot of what this one book contributed. It is **not** claimed to be the final canonical
form of the methods it contains. When a rule from it is restated in a source-independent artifact, the
canonical copy will say which packages fed it, and the package copy stays as the attributed source of
record.

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

That license covers what is written here: the procedures, protocols, scripts and notes. It does not
grant rights in the sources those documents are derived from, and it is not a claim that a source's
terminology or structure is ours to license. Each source package carries an attribution file — see
[`Validation/Trustworthy-ML-2023/SOURCE.md`](Validation/Trustworthy-ML-2023/SOURCE.md) — recording the
book's title, authors and edition, what was verified about its licensing, and the working rule that no
source text is redistributed here. Where an attribution obligation and the MIT grant could interact,
the obligation wins and the uncertainty is documented in that file rather than resolved by assertion.
