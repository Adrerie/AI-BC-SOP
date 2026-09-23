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

- **Trustworthy ML lineage** — 8 SOPs and 9 benchmarks for evaluation discipline on real
  deployments: [SOP group](SOP/Trustworthy-ML-2023/README.md),
  [Benchmark group](Benchmark/Trustworthy-ML-2023/README.md),
  [validation record](Validation/Trustworthy-ML-2023/acceptance_report.md),
  [source attribution](Validation/Trustworthy-ML-2023/SOURCE.md),
  [plan](plans/Trustworthy-ML-2023/README.md). BM-01…08 reconstruct the 2023 book; BM-09 is a
  post-book extension from the official Spring 2026 course and is traced separately in the update audit.

Book-derived material cites the source by section and page; post-book additions cite their own course or paper locators. The source documents themselves are not included here.

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

`Trustworthy-ML-2023` remains the repository's first provenance-bearing lineage: the original
book-derived contribution is still traceable, while selected files may be extended in place by later
official material whose deltas are recorded in the corresponding update audit. It is
**not** claimed to be the final canonical form of the methods it contains. When a rule is later restated
in a source-independent artifact, the canonical copy will say which sources fed it, while this lineage
retains the provenance record for both the book-derived core and any clearly labeled later additions.

The same course lineage continued after the book, and its official 2024/25 and 2026 teaching material was
audited as an **update layer** rather than as a second package: see
[`Validation/Trustworthy-ML-Official-Updates-2024-2026/`](Validation/Trustworthy-ML-Official-Updates-2024-2026/source_inventory.md).
Most of what that material teaches was already covered, and most of what was not was rejected as a
classroom practice rather than a research protocol. The surviving deltas extend selected existing SOP
and Benchmark files and are traced in the update audit; BM-09 is the one wholly new benchmark and marks
its course provenance locally. No post-2023 rule is presented as book-derived, and no lecture became a
file of its own.

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
license the sources those documents are derived from. Each source package carries an attribution file —
for the first package, [`Validation/Trustworthy-ML-2023/SOURCE.md`](Validation/Trustworthy-ML-2023/SOURCE.md)
— recording the book's title, authors, official website and license. That book is distributed by its
authors under **CC BY 4.0**, so adapting it requires attribution, a link to that license, and a note
that changes were made; the package does all three, and the MIT grant applies to this repository's own
original material on top of that. The source PDF and bulk extracted text are kept out of Git as an
editorial choice, not because the license requires it.
