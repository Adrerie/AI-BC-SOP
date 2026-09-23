# 00 — Master Plan

## Objective

Use official post-book course material from the same Trustworthy ML lineage as an **external update
source** for the accepted SOP/Benchmark package.

The central question is:

> What appears in the 2024/25 and 2026 official teaching/research materials that is not already
> represented adequately in the current 8 SOP + 8 Benchmark package?

## Source hierarchy

### Tier A — authoritative official update sources

Audit first:

1. University of Tübingen / STAI TML 2024/25 course page.
2. The linked 2024/25 official lectures/slides/videos where accessible.
3. The three 2024/25 exercises:
   - Exercise 1 — OOD
   - Exercise 2 — XAI
   - Exercise 3 — uncertainty
4. STAI / KAIST TML Spring 2026 course page.
5. Linked 2026 official lectures/slides/videos where accessible.
6. 2026 project topics and grading rubrics.

The course pages explicitly state that the book is based on earlier course material and that the
course is updated yearly, so later official material is a valid update source but **not part of the
2023 book**.

### Tier B — external verification only

May be consulted for mathematical or implementation sanity checks, but must not be silently treated
as part of the official course lineage:

- StatProofBook entries citing the book
- official repositories/pages for methods explicitly taught in the course
- primary papers linked by the official course
- library documentation needed to disambiguate a metric implementation

### Tier C — discovery only

Search engines, GitHub search, blogs, community notes, Reddit, etc. may identify candidates but do not
establish package rules by themselves.

## Candidate deltas to test, not assume

The following are hypotheses from the preliminary scan. They must be accepted, merged into an existing
artifact, or rejected after source reading:

- LLM-specific adversarial attacks / security stress
- prompt-sensitivity detection at test time
- RAG parametric–contextual knowledge-conflict detection
- mechanistic attribution vs training-data attribution agreement
- confidence/calibration under distribution shift and multi-turn interaction
- privacy and data-protection evaluation
- paper reproduction as boundary-finding rather than binary replication
- modern experimental-design expectations: appropriate baselines, error bars, limitation analysis

Do not create artifacts merely because these phrases appear on a course page.

## Non-goals

- No chapter-by-chapter or lecture-by-lecture mirror.
- No wholesale rewrite of the accepted 2023 package.
- No importing every referenced 2024–2026 paper.
- No treating project-topic suggestions as established benchmark standards.
- No claiming that a classroom exercise is a field-wide protocol.
- No folding privacy/security into adversarial robustness without checking whether the capability and
  threat model are actually the same.
- No new metric without a definition, orientation, aggregation rule, implementation convention where
  needed, and failure interpretation.

## Required provenance classes

Every accepted delta must be labeled as one of:

1. **official-course-derived** — explicitly taught or required in the official post-book material;
2. **synthesized-from-official-course** — repository reconstruction combining several official
   materials;
3. **repository convention** — our operational choice needed to make the procedure executable;
4. **external-primary-source support** — supported by a linked paper or specification but not itself
   an official-course rule.

Never relabel post-2023 content as book-derived.

## Architectural rule

Do not rename or relocate the accepted 2023 package during this cycle.

First build a delta audit under:

`Validation/Trustworthy-ML-Official-Updates-2024-2026/`

Only after the decision gate may the branch modify existing SOP/Benchmark artifacts or add new ones.

Prefer, in order:

1. add a missing test/procedure to an existing artifact;
2. add a clearly marked Extended Track to an existing artifact;
3. add a new Benchmark when the target capability/failure mode is genuinely distinct;
4. add a new SOP only when there is a reusable workflow not expressible by the existing eight.

Avoid source-silo duplication.

## Completion rule

The cycle completes only when:

- Tier A sources are inventoried and access limitations recorded;
- every candidate delta has an explicit disposition;
- accepted deltas have provenance and implementation boundaries;
- existing validation still passes;
- new rules receive regression checks where feasible;
- the final report separates "new capability" from "new example" and "new course pedagogy";
- no automatic merge occurs.
