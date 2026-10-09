# Lacan studies, phase 1: two-book reading and concept reconstruction

## Objective

Read **both books in full** and produce a usable, source-traceable interpretation of their arguments. The result should support later SOP/Benchmark design, but **this phase does not create SOPs or Benchmarks**.

Target books:
1. 沈志中，《永夜微光：拉康与未竟之精神分析革命》。
2. 张一兵，《不可能的存在之真：拉康哲学映像》（identify the edition actually available).

These are **studies of Lacan**, not replacements for Lacan's primary texts. Do not describe an interpretation or quotation found only in these books as independently verified in Lacan.

## Execution

### 1. Verify sources and coverage
- Search the local book directory and workspace for both books. Check actual title, author, edition, file type and readable extent; do not guess missing details or download unauthorized copies.
- Read each table of contents **and the substantive body text**. Establish a full chapter/section list and a stable locator rule. Distinguish print page numbers from PDF page indices.
- Record confirmed access and limitations in `Validation/Lacan-Studies-Phase1/SOURCE.md`. If a source is missing or unreadable, report exactly what is blocked and do not mark it complete.

### 2. Reconstruct each book in full
- Read chapter by chapter. For each chapter or substantive section, explain its driving question, central argument, supporting reasoning, key conceptual distinctions and what the argument leaves unresolved.
- Explain difficult passages where needed, including the author's assumptions and at least one plausible alternative reading where interpretation is genuinely disputed. Do not inflate straightforward passages with a fixed template.
- Maintain a concise, complete chapter/section checklist in `reading_map.md`, linking to the corresponding analysis. **A table of contents summary is not completion.**
- Put the substantive analyses in two book-level notes under `book_notes/`. Split by major parts only if a single file becomes unmanageable.

### 3. Reconstruct concepts across the two books
- Build `concept_reconstruction.md` by **concept and argument**, not by chapter. Prioritize the concepts actually developed by the two books.
- For each major concept, identify how each author uses it, the textual evidence, historical/theoretical context, agreements, disagreements and unresolved questions.
- Keep three claims separate: what the studied author argues, what the author attributes to Lacan/Freud/others, and what we infer. Mark primary-text verification as pending when appropriate.
- Cross-link to the two book notes instead of copying long explanations or source quotations.

### 4. Close out with a content review
- Check that every chapter and major section in both accessible books has a corresponding substantive analysis and locator.
- Check a focused sample of difficult claims against the actual pages, and correct unsupported attribution, terminology, chronology and cross-book comparisons. Revisit other passages when the same problem appears.
- Update the repository README with one short entry and links to the new material **only once the analysis is genuinely complete**.
- Commit and push the branch; do not merge into `main`. State exactly what was finished and what remains unverified.

## Deliverables

```text
Validation/Lacan-Studies-Phase1/
├── SOURCE.md
├── reading_map.md
├── book_notes/
│   ├── yongye_weiguang.md
│   └── bu_keneng_de_cunzai_zhizhen.md
└── concept_reconstruction.md
```

The plan and repository instructions already live at `plans/Lacan-Studies-Phase1/README.md` and root `AGENTS.md`. Create the deliverable files as work proceeds, not empty placeholders.

## Deliberately excluded

No third book, no Lacan original-text verification campaign, no fixed SOP/BC counts, no rating rubric or question bank, no vector database, knowledge graph, agent swarm, validators, hashes, acceptance-cycle machinery or chapter-per-file bureaucracy. Those belong to later phases only if a concrete need appears.

**Completion standard:** complete reading coverage of both verified sources, arguments supported by usable locators, a coherent cross-book concept reconstruction, and transparent unresolved claims. If a book is unavailable, the phase remains incomplete.
