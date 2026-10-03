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

- **Deep Learning 2016** — 9 SOPs and 11 active benchmark checks reconstructed by research function from
  Goodfellow, Bengio & Courville's *Deep Learning* (2016): [SOP group](SOP/Deep-Learning-2016/README.md),
  [Benchmark group](Benchmark/Deep-Learning-2016/README.md),
  [source record](Validation/Deep-Learning-2016/SOURCE.md),
  [reconstruction record](Validation/Deep-Learning-2016/concept_reconstruction.md), and
  [plan](plans/Deep-Learning-2016/README.md). The package preserves 2016-era implementation advice as
  historical where appropriate instead of presenting it as current best practice.

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

The Deep Learning 2016 package was likewise extended by an **update layer** rather than by a second
package, covering 2017–2026 work that changes a reusable research workflow or an evaluable claim: see
[`Validation/Deep-Learning-Modern-2017-2026/sources.md`](Validation/Deep-Learning-Modern-2017-2026/sources.md)
for the source record and
[`delta_map.md`](Validation/Deep-Learning-Modern-2017-2026/delta_map.md) for every candidate delta with its
`2016 baseline → modern delta → source → destination → boundary` record and its status. Two modern textbooks
were named as anchors; one was inaccessible, which is recorded in `sources.md` §1.2 together with a standing
prohibition on sourcing any delta to it, so the layer rests on the readable anchor plus the small set of
landmark papers its plan names. Seven existing SOPs and four existing benchmark checks carry clearly marked
*Modern update (2017–2026)* blocks, and **no new SOP or benchmark was created**: the 2016 text and every
2016 citation are unchanged, and where a capability is already owned by the Trustworthy ML lineage the block
cross-links instead of restating it. Contested quantities — notably the compute-allocation exponents, where
the layer's own two sources disagree — and single-source frontier results were left in the delta map rather
than imported. No architecture encyclopaedia, leaderboard, validator or acceptance gate was added.

## Published handbooks

The SOP and Benchmark corpus is also published as readable volumes, built from the repository files by a
conversion pipeline kept outside Git. Each release names its build branch and commit, so a PDF can always
be traced back to the markdown it came from.

- **`handbook-v2`** — *Trustworthy ML Handbook*, Vol. 1 SOP and Vol. 2 Benchmark, English, 56 and 55 pages.
  Built from `plan/deep-learning-modern-update` at `4ca8271`. The English text of both volumes was
  restructured against ASD-STE100 Issue 9: sentences inside the length limit, one instruction per sentence,
  the imperative and the condition first in numbered steps, no semicolon in prose, a vertical list where one
  sentence carried several parallel facts. The controlled dictionary was deliberately not applied, so
  research vocabulary stays as the field writes it. No claim, citation, table or number changed. The Chinese
  volumes are not re-issued here; they follow once the restructured English text is confirmed. The source
  book is **CC BY 4.0**, so these volumes are published as attributed adaptations, and each carries the
  license link and a note that the material was changed.
- **`deep-learning-handbook-v2`** — *Deep Learning: Procedures and Benchmark Checks*, one combined English
  volume, 161 pages, holding the nine procedures and eleven checks of the Deep Learning lineage, with the
  2017–2026 update layer marked in place. Built from `plan/deep-learning-modern-update` at `4ca8271`, under
  the same ASD-STE100 sentence rules as `handbook-v2`. **This volume is framed differently, on purpose**:
  its principal source states no adaptation licence, so it is published as original methodology notes that
  *cite* their sources — not an authorized adaptation, translation, edition or derivative of any of them,
  and it reproduces no source text and ships no source PDF. The rights status of every cited work, including
  the one that could not be accessed at all, is printed inside the volume.
- **`handbook-v1`** and **`deep-learning-handbook-v1`** — the first editions: 48 and 49 pages in English, 66
  and 68 in Chinese, and 146 pages for the combined Deep Learning volume. They hold the same content in the
  pre-restructured English text, and they stay downloadable.

A future volume inherits two rules rather than the wording of the last one. The framing a release uses is
set by what the source's licence permits, not by how the previous volume was described. And a reissue gets a
new tag instead of replacing the old asset, because a reader who cited a page of the first edition must
still be able to open it. The second edition also renders nested lists correctly: the pipeline's markdown
parser changed to a CommonMark one, which reads the two- and three-space nesting these files use.

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

The Deep Learning packages record their sources the same way:
[`Validation/Deep-Learning-2016/SOURCE.md`](Validation/Deep-Learning-2016/SOURCE.md) for the 2016 monograph,
and [`Validation/Deep-Learning-Modern-2017-2026/sources.md`](Validation/Deep-Learning-Modern-2017-2026/sources.md)
for the modern layer. One note on that layer, because its license differs materially from CC BY 4.0: the
readable modern anchor is distributed by its author under **CC BY-NC-ND**, which permits redistribution with
attribution but not commercial use or derivative works. This repository reproduces only short quoted
passages from it, attributed in place, for the purpose of recording what a source does and does not
support; the procedures, benchmarks and delta judgements written around those quotations are this
repository's own original material and are the part the MIT grant covers. The book PDF and its bulk
extracted text are kept out of Git. Neither the quotations nor this repository's material should be read as
a derivative of, or a substitute for, that book. The second named anchor could not be accessed at all, and
`sources.md` §1.2 records that no delta anywhere in the layer is sourced to it.
