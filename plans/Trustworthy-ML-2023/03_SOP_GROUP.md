# Plan 3 — SOP Group

## Goal

Create a reusable set of Standard Operating Procedures derived from the reconstructed methodology.

## Output Location

`SOP/Trustworthy-ML-2023/`

Create an index:

`SOP/Trustworthy-ML-2023/README.md`

and multiple SOP documents. Do not create one giant monolithic SOP unless the source audit proves decomposition is impossible.

## SOP Selection Rule

Create an SOP when the source-derived concept can be expressed as a repeatable research procedure.

Examples may include:

- defining deployment assumptions and distribution boundaries
- constructing IID and shifted evaluation sets
- diagnosing distribution-shift failures
- evaluating confidence and calibration
- evaluating uncertainty as a failure signal
- configuring selective prediction or abstention
- comparing mitigation methods
- reporting failure boundaries and validity limits

These examples are provisional. The final set must follow the concept reconstruction.

## Mandatory SOP Schema

Every SOP must contain:

1. **Purpose**
2. **When to use**
3. **Inputs / prerequisites**
4. **Definitions needed for execution**
5. **Procedure**
6. **Mandatory checks**
7. **Decision or stop conditions**
8. **Common methodological failures**
9. **Required outputs**
10. **Minimum reporting requirements**
11. **Links to relevant Benchmarks**
12. **Source traceability**

Procedures must be written as executable research steps, not explanatory prose alone.

## Tiering

Where useful, define:

- **Core**: minimum defensible procedure
- **Extended**: stronger procedure for high-stakes or publication-grade studies

Do not inflate the core procedure with every optional method in the book.

## Cross-SOP Consistency

Use consistent definitions for recurring terms.

Avoid redefining the same metric differently across SOPs.

If one SOP depends on another, link it explicitly rather than duplicating the full procedure.

## Gate C — SOP Quality

Pass only if:

- the SOP group covers the main reusable workflows identified in reconstruction
- every SOP can be executed without reading the source book
- every SOP contains checks and failure conditions, not only steps
- each SOP links to one or more evaluation mechanisms in the Benchmark group where applicable
- source traceability is present but does not dominate the document structure
