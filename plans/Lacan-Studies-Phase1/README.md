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

## Status (2026-10-10)

Delivered under `Validation/Lacan-Studies-Phase1/`: `SOURCE.md`, `reading_map.md`, `book_notes/yongye_weiguang.md`, `book_notes/bu_keneng_de_cunzai_zhizhen.md`, `concept_reconstruction.md`. The previous executor reported finding and fully reading both local books; chapter-to-note coverage is documented. The local session record has now been checked and confirms that round **did use subagents** (25 calls, 13 completed), contrary to the "no subagents" rule here — the deviation is registered verbatim in `reading_map.md` rather than rewritten. Because agent output plus spot checks is not independent proof of paragraph-by-paragraph reading, the "100%" figure in the coverage table is a chapter/index coverage claim only. No third source was added and no SOP/Benchmark was created. Completed and remaining items of the focused repair are in [REVISION-01.md](REVISION-01.md).

Three limits are load-bearing for anything built on this phase, and none of them is a reading gap:
(1) the available 《永夜微光》 copy is a community re-typeset PDF with no printed page numbers and with many formulas, figure plates and one clinical list lost, so its locators are PDF pages and several formal devices are unverifiable; (2) the 张一兵 EPUB has no page numbers and its endnote apparatus survives only as [1]–[71] of [1]–[1023], so notes [72]–[1023] are unavailable, while preserved notes [1]–[71] require individual correspondence checks; (3) neither book is Lacan, and no claim labelled as his here has been checked against his own texts. Verification against paper editions or primary texts is deliberately left for a later phase.
