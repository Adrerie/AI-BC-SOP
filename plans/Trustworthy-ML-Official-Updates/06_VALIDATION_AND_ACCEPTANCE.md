# 06 — Validation and Acceptance

## Goal

Verify that official-course updates improve coverage without weakening the accepted package.

Create:

`Validation/Trustworthy-ML-Official-Updates-2024-2026/acceptance_report.md`

## A. Source gate

Check:

- every accepted addition has an official source locator
- partial/inaccessible materials are labeled
- project-topic suggestions are not misrepresented as established standards
- post-2023 content is never labeled book-derived

## B. Delta gate

For every accepted addition, answer:

1. What exact capability/failure/protocol was absent before?
2. Why is this not only a modern example?
3. Why is its chosen destination minimal?
4. What would be lost if it were omitted?

If these cannot be answered, reject the extension.

## C. Regression gate

Re-run the full existing Trustworthy-ML-2023 validation suite.

Required:

- structural checks green
- links green
- metric register green
- AUPR contract green
- prose checks green
- citation checks green
- principle gates green
- mutation suite green

If the source PDF is available, also rerun source-dependent index verification.

## D. New-validation requirements

Add mechanical checks where feasible for any new load-bearing rule.

Examples:

- provenance marker for official-course-derived text
- detector positive-class/score-orientation invariants
- threat-model fields for new security tracks
- no cross-family agreement ⇒ truth wording
- replication result taxonomy, if added to BM-08

Use mutation tests for new high-risk regression patterns where useful.

## E. External-source cross-check

Compare the final extensions back to:

- official 2024/25 materials
- official 2026 materials
- optionally StatProofBook for scoring-rule math only

Record disagreement rather than silently "fixing" a source.

## F. Acceptance classification

Final outcome for each candidate:

- ACCEPTED INTO CORE
- ACCEPTED AS EXTENDED TRACK
- EXAMPLE ONLY
- RECORDED / FUTURE SCOPE
- REJECTED
- INSUFFICIENT EVIDENCE

## Gate U6

PASS only if:

- old package validation remains green;
- all new accepted rules are traceable;
- no candidate silently changes meaning across SOP and Benchmark layers;
- no unresolved P0 methodological issue remains.
