# Revision Plan 5 — Reproducible validation

## Goal

Make every mechanical acceptance claim independently re-runnable without committing copyrighted book text.

## 1. Commit validation tooling

Create a committed validation tooling directory such as:

`Validation/Trustworthy-ML-2023/tools/`

Include scripts or small programs sufficient to rerun, where applicable:

- Markdown link validation
- SOP / Benchmark schema conformance
- cross-link symmetry
- metric-register consistency
- heading-structure checks that operate on a user-supplied source path
- citation/page-anchor validation when the source PDF is locally available
- acceptance summary generation or check list

Scripts must not embed or emit substantial book text.

## 2. Copyright-safe source handling

Keep out of Git:

- the source PDF
- bulk extracted text
- per-page full-text dumps
- large verbatim excerpts

It is acceptable for scripts to read a local source PDF supplied by the user.

## 3. Portable configuration

Remove machine-specific absolute paths such as:

`D:\...\Trustworthy Machine Learning book 2023.pdf`

from committed validation artifacts.

Use a portable placeholder or configuration, for example:

- environment variable `TRUSTWORTHY_ML_2023_PDF`
- CLI argument `--source /path/to/book.pdf`
- local ignored config file

The audit report may state the source filename and edition, but not depend on one user's filesystem path.

## 4. Reproducibility README

Create:

`Validation/Trustworthy-ML-2023/tools/README.md`

It must state:

- prerequisites
- expected source
- how to point tools to the local PDF
- which checks can run without the source
- which checks require the source
- expected outputs
- that the source PDF itself is not included

## 5. Acceptance-report evidence

The new acceptance report may only claim a mechanical PASS if:

- the relevant validation code is committed, or
- the check is simple enough to verify directly from repository contents and the report states exactly how

Avoid non-reproducible claims like "a local script checked X" when that script is unavailable.

## Gate V — Validation reproducibility

Pass only if:

- non-copyright validation tooling is committed
- no absolute personal path remains in committed files
- source-dependent checks use portable configuration
- every mechanical PASS has a reproducible method
- copyrighted source text remains excluded
