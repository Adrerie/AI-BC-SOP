# Plan 1 — Source Audit

## Goal

Build a complete, auditable representation of what the book covers before creating any SOP or Benchmark.

## Step 1: Locate the source

Search the local workspace for the 2023 *Trustworthy Machine Learning* book or its local export.

Prefer the most complete available source. Record:

- source path
- file type
- edition/year
- whether the source contains full text or only partial text
- whether headings are machine-readable

If several copies exist, choose one primary source and note secondary copies only when they help recover missing structure.

## Step 2: Extract the structural universe

Extract the complete hierarchy of:

- chapters
- sections
- subsections
- lower-level headings where present

Preserve source order and identifiers in the audit only.

Create:

`Validation/Trustworthy-ML-2023/source_coverage.md`

The file must contain a coverage table with at least:

| Source ID | Heading | Level | Initial concept tags | Body read? | Disposition |
|---|---|---:|---|---|---|

Allowed dispositions:

- `incorporate`
- `supporting`
- `redundant`
- `out-of-scope`
- `needs-body-reading`

No heading may be silently omitted.

## Step 3: Decide where body reading is needed

Mark a heading for body reading when any of the following is true:

- the title is too broad or vague
- the title names a method without stating its role
- the section likely defines a metric or protocol
- assumptions or caveats matter
- the relation to other concepts is unclear
- the section may contain a reusable procedural sequence
- the section may distinguish closely related concepts
- the section may change how an SOP or Benchmark should be designed

Read only enough surrounding text to resolve the methodological point. Record concise notes in the coverage file.

## Step 4: Normalize concepts

Assign normalized concept tags independent of chapter names.

Examples:

`distribution-shift`, `ood-generalization`, `calibration`, `uncertainty`, `selective-prediction`, `robustness`, `failure-analysis`, `evaluation-design`, `scalability`.

Do not force the source into these examples if the book supports a better concept.

## Gate A — Source Coverage

Pass only if:

- the complete available heading hierarchy has been captured
- every heading has a disposition
- ambiguous or methodologically important headings have been checked against body text
- no final SOP or Benchmark drafting has started before this gate passes
