# Deep Learning (Goodfellow, Bengio & Courville, 2016) — SOP / Benchmark plan

## Goal

Build a source-traceable SOP and Benchmark/BC package from the local copy of *Deep Learning* ("the
flower book") without mirroring its chapter structure.

This branch starts from `framework/book-base`. Do not import the Trustworthy ML package into this
branch and do not merge `main` automatically.

## Source handling

1. Locate the local book file already present in the workspace. Do not download another copy unless the
   local file is unusable.
2. Record the exact edition/language, title, authors, year, publisher/ISBN if present, local filename,
   table of contents, and the pagination actually used for citations.
3. Do not commit the PDF or bulk extracted book text. Commit only notes, source coverage, concise
   quotations where necessary, and page/section references.
4. If the local copy is a translation, use standard English technical terminology in the repository
   and cite the local edition consistently. If a translation is ambiguous, consult the original
   terminology only to resolve the term; do not silently switch pagination.

Create a small provenance record under:

`Validation/Deep-Learning-2016/`

At minimum:
- `SOURCE.md` — source identity and citation convention
- `source_coverage.md` — what parts were read and what was intentionally not operationalized
- `concept_reconstruction.md` — the research-function reconstruction used to form SOPs and BCs
- `acceptance_report.md` — short final summary of coverage, files produced, and any known limits

## Reconstruction rule

Do **not** create one SOP or Benchmark per chapter.

Classify the book's material into three buckets:

1. **Foundations / theory** — mathematics, probability, information theory, graphical-model or
   optimization theory needed to understand later procedures. Keep these in reconstruction notes unless
   they directly define an executable research step or an evaluable claim.
2. **Reusable research procedures** — material that can be turned into a sequence of inputs, decisions,
   steps, checks, failure modes, and outputs. These become SOP candidates.
3. **Evaluable capabilities / failure modes** — claims that can be tested with a defined setup,
   baselines, metrics, comparisons, and interpretation. These become Benchmark/BC candidates.

A method family or architecture name by itself is not a Benchmark.

## Research-function axes to inspect

Use these as prompts, not as a fixed file list:

- problem/objective formulation and probabilistic interpretation
- capacity, bias/variance, underfitting/overfitting and generalization
- data splitting, model selection and hyperparameter search
- initialization, optimization stability and convergence diagnosis
- regularization and its trade-offs
- architecture-specific inductive bias: feedforward, convolutional and sequence/recurrent models
- practical debugging and experimental methodology
- representation learning, transfer, semi-supervised learning and disentangling claims
- structured/probabilistic modeling where it yields a reusable workflow
- approximate inference, Monte Carlo, partition-function estimation and generative modeling where the
  book supplies an executable evaluation protocol

Do not force every axis to produce an artifact.

## SOP construction

Create:

`SOP/Deep-Learning-2016/`

Choose the number of SOPs from the reconstructed workflows rather than in advance.

Each SOP should contain only what is needed to execute it:

- purpose / when to use
- required inputs and assumptions
- procedure
- essential checks and common failure modes
- outputs to retain/report
- links to relevant BCs
- source traceability

Prefer broad reusable workflows over method-specific recipes. For example, "diagnose optimization
failure" is preferable to a file for every optimizer.

## Benchmark / BC construction

Create:

`Benchmark/Deep-Learning-2016/`

A BC should exist only when the book supports a concrete evaluable question. Each BC should state:

- capability or failure mode
- evaluation hypothesis
- data/split assumptions
- comparison or stress conditions
- required baselines
- primary metrics and their direction
- aggregation/reporting
- failure interpretation
- computational/resource notes where material
- validity limits
- related SOPs
- source traceability

Avoid inventing a metric merely to make the schema look complete. A directly defined rate or loss is
fine when it is local to one BC.

## 2016-to-2026 boundary

The book is foundational but old enough that some implementation advice, architecture choices and
empirical expectations are historical.

For every operational rule, distinguish:

- **book-derived principle** — still meaningful independent of the period;
- **book-era implementation/example** — useful historically but should not be presented as a current
  universal default;
- **repository convention** — a small operational choice needed to make an SOP/BC executable.

Do not silently modernize the book with Transformers, AdamW, modern scaling laws, current benchmark
leaderboards, etc. Those belong to later sources and can extend the package in a future cycle.

Likewise, do not preserve obsolete implementation detail as a mandatory 2026 practice merely because
the book used it.

## Scope decisions

The package should emphasize reusable research methodology, not encyclopedic coverage.

It is acceptable to leave a chapter or section with no SOP/BC when it is primarily explanatory theory.
Record that decision briefly in `source_coverage.md`.

Pay particular attention to Chapter 11 practical methodology: it is likely to contain high-value
cross-cutting SOP material and should be integrated into the relevant workflows rather than copied into
a single chapter-summary file.

For Parts III / deep generative models, create SOPs or BCs only where the text yields an operational
workflow or evaluable claim. Do not create a generative-model taxonomy just to claim coverage.

## Final package review

Before stopping:

- confirm every SOP/BC is traceable to the local book;
- remove obvious chapter-shaped duplication;
- check that theory-only material was not forced into procedures;
- check that historical examples are not written as current universal defaults;
- ensure internal links and package indexes resolve;
- compare the final artifact names at a high level with current `main` and note obvious cross-source
  overlaps, but do not merge or redesign them in this branch.

No new validator framework, mutation suite, multi-stage gates, or repeated review cycles are required.

## Deliverable

The finished branch should contain:

```text
SOP/Deep-Learning-2016/
Benchmark/Deep-Learning-2016/
Validation/Deep-Learning-2016/
plans/Deep-Learning-2016/README.md
```

Update the branch's root/SOP/Benchmark indexes only enough to expose this source package.

Commit and push `plan/deep-learning-2016`. Do not merge `main`.
