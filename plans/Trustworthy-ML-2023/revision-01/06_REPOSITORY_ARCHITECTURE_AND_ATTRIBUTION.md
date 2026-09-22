# Revision Plan 6 — Repository architecture and source attribution

## Goal

Keep this first source package useful without turning the entire repository into a permanent collection of isolated book-specific silos.

## 1. Root architecture wording

Update the root README so that source packages are described as:

- provenance-bearing source-derived packages
- staging / evidence units
- inputs to future canonical SOPs and Benchmarks

Do not state or imply that every future source must forever remain an isolated package.

State that as new sources are read, their insights may:

- extend an existing canonical SOP / Benchmark
- revise an existing rule
- supersede an earlier source-derived rule
- be merged with several sources into a source-independent canonical artifact
- remain source-specific when appropriate

## 2. Preserve this package

Do not delete `Trustworthy-ML-2023/`.

It remains valuable as:

- the first source-derived package
- a traceability record
- a stable snapshot of what this book contributed

But make clear it is not necessarily the final canonical form of those methods.

## 3. Package-level source notice

Create:

`Validation/Trustworthy-ML-2023/SOURCE.md`

Include:

- title
- authors
- year / edition
- official source or bibliographic reference
- source license
- attribution notice
- statement that repository files are reconstructed / adapted methodological artifacts
- statement that the book text itself is not redistributed here
- note that repository code/files remain subject to repository licensing only to the extent compatible with source attribution requirements

Do not copy long source passages.

## 4. Root license wording

Do not casually replace the root MIT license unless necessary.

Instead, clarify in README / SOURCE.md that source-derived documentation carries attribution obligations associated with the underlying source.

If a license conflict or derivative-work issue is uncertain, document the uncertainty rather than inventing a legal conclusion.

## Gate A — Architecture and attribution

Pass only if:

- the root repository is not permanently locked to isolated source silos
- the Trustworthy-ML-2023 source package remains traceable
- SOURCE.md exists and clearly attributes the book
- no long copyrighted text is added
