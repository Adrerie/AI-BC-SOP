# Master Plan

## Objective

Create the first book-derived methodology package in AI-BC-SOP from *Trustworthy Machine Learning* (2023).

The output must contain:

- a coherent **SOP group** under `SOP/Trustworthy-ML-2023/`
- a coherent **Benchmark group** under `Benchmark/Trustworthy-ML-2023/`
- validation artifacts sufficient to demonstrate source coverage, conceptual reconstruction, internal consistency, and acceptance

The result should be useful to a researcher who has never read the book.

## Non-Goals

Do not:

- write a chapter-by-chapter book summary
- mirror the book's table of contents as the final taxonomy
- create one SOP or one Benchmark per chapter
- copy headings as artifact names unless the heading independently describes a reusable research task
- treat every concept in the book as equally important
- invent metrics, definitions, or claims unsupported by the source or established methodology
- make the package application-specific unless the underlying procedure is genuinely domain-specific

## Source Strategy

Use a two-level source strategy.

### Level 1: Mandatory structural reading

Read and record:

- complete table of contents
- chapter titles
- section titles
- subsection titles
- any lower-level headings available in the source

This is mandatory because the full heading structure defines the source coverage universe.

### Level 2: Targeted body reading

Read body text when needed to resolve:

- ambiguous headings
- definitions
- assumptions
- procedural steps
- evaluation protocols
- metric definitions
- caveats and failure cases
- relations between concepts
- examples that materially clarify a reusable rule

Body reading is targeted, not a requirement to summarize the entire book.

## Reconstruction Principle

The final knowledge structure must be organized by research function rather than publication structure.

Prefer axes such as:

- problem and deployment definition
- distribution assumptions and shift
- generalization and robustness
- uncertainty and calibration
- selective prediction and abstention
- evaluation design and metrics
- failure analysis
- computational and scalability constraints
- reporting and validity boundaries

These are examples, not a mandatory final taxonomy. The actual taxonomy must be derived after source audit.

## Deliverable Architecture

Minimum required structure:

```text
SOP/Trustworthy-ML-2023/
  README.md
  <multiple reusable SOP documents>

Benchmark/Trustworthy-ML-2023/
  README.md
  <multiple reusable benchmark documents>

Validation/Trustworthy-ML-2023/
  source_coverage.md
  concept_reconstruction.md
  acceptance_report.md
```

Additional files are allowed when they improve traceability or execution.

## Quality Standard

Every final artifact must satisfy three conditions:

1. **Source-grounded**: concepts can be traced back to the book headings and, where needed, body text.
2. **Reconstructed**: organization reflects our own methodology, not the book's chapter order.
3. **Operational**: a researcher can use the artifact to design, execute, or evaluate a real experiment.

## Completion Rule

The task is complete only when all acceptance gates in `05_VALIDATION_AND_ACCEPTANCE.md` pass and the final indexes are updated.
