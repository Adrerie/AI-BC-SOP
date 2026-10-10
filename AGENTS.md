# Repository working rules

This repository converts studied sources into reusable SOPs, Benchmarks and traceable research notes. Preserve the existing `SOP/`, `Benchmark/`, `Validation/` and `plans/` conventions. Do not rewrite unrelated packages.

## Source and reasoning discipline
- Read accessible primary material before making source-level claims. Never invent quotations, page numbers, chapter content or source access.
- Cite a resolvable chapter/section and page when available. Distinguish printed pages from PDF page indices and note translation/edition differences.
- Keep the source author's argument, another author's interpretation, and our own reconstruction distinct. Report disagreements instead of silently forcing consistency.
- Prefer substantive argument reconstruction over paraphrase, invented certainty or decorative terminology.
- Keep research writing compact and readable. Add a file, template, script or validation step only if the work genuinely needs it.
- Never commit copyrighted source books or bulk verbatim extracts. Use limited, attributed quotations and original analysis.

## Lacan phase 1: two-book reconstruction
When working under `plans/Lacan-Studies-Phase1/` or `Validation/Lacan-Studies-Phase1/`:
- Follow `plans/Lacan-Studies-Phase1/README.md`.
- Cover the actual contents of both target books, not merely their tables of contents. Maintain chapter-level traceability while organizing explanations around arguments and concepts.
- Treat the two studied books as secondary research. A scholar's account of Lacan must not be presented as a claim independently verified in Lacan's own texts.
- Distinguish Lacan's historical stages, theoretical registers and contested terminology. Preserve uncertainty and viable rival readings.
- This phase produces reading and concept-reconstruction notes only. Do not preemptively write SOPs/Benchmarks, clinical protocols, assessment scores or software infrastructure.
- Analysis of real people is not clinical diagnosis. Avoid unsupported assertions about anyone's unconscious motives or mental health.

## Git scope
Work on the requested topic branch. Keep `main` unchanged, make focused commits and do not merge without a separate request.

## Review and execution limits
- Keep work in one interactive Codex session. Do not use `codex exec`, other exec-style task invocations, or subagents.
- Claim “fully read”, “verified” or “100% covered” only to the extent supported by the actual reading record. A coverage table or agent summary alone is not independent evidence of full reading.
- Record real tool/use deviations and source gaps truthfully. Never rewrite an execution history to make it appear compliant.
- Check original publication date separately from manuscript/foreword dates; identify official editions separately from community retypeset copies.
- Cite EPUB references as file or section plus paragraph, never as page numbers. Recheck endnotes actually present before marking a range unavailable.
- Before making a strong philosophical criticism, distinguish a real contradiction from a tension that admits an alternative interpretation. A local formal model failure is not proof that an entire formalization program failed.
- Descriptions of transference or other clinical claims remain attributed textual interpretations, not universal clinical instructions. Source coverage is not clinical validity.
- For review repairs, prefer small edits to existing analyses and one short repair plan. No extra infrastructure or repetitive acceptance rituals.

## Lacan preliminary SOP/BC (Codex authoring branch)
When working in `SOP/Lacan-Studies-Preliminary/`, `Benchmark/Lacan-Studies-Preliminary/` or `plans/Lacan-Studies-Preliminary/`:
- Follow `plans/Lacan-Studies-Preliminary/README.md`. The withdrawn assistant-written prototype files are not source material or a required design.
- Build a **small number of substantive, theory-derived** research procedures and matched checks from `Validation/Lacan-Studies-Phase1/`. Merely checking citation hygiene or paraphrasing concept definitions is not sufficient for a substantive Lacanian SOP/BC.
- Each SOP needs a concrete intellectual task and a justified reading procedure. BCs must detect a real error in reasoning, not just require a preselected category or rigid output fields. Do not invent necessary/sufficient conditions, thresholds, or fabricated outcomes.
- Source notes are **two secondary studies**: preserve each author's interpretation and point to its PDF page or EPUB file/paragraph; do not claim independent confirmation of Lacan or use missing formulas/endnotes as proof.
- Do not turn interpretive operations into clinical diagnosis, universal rules of desire or advice for treating real people. Keep alternatives when the text permits competing readings.
- Favor concise analytical paragraphs over checklist padding, repetitive warnings, invented categories or one-line AI-style paragraphs. Do not add extra validation files, rigid schemas, scoring rubrics, scripts or agent orchestration.
- Complete work in a single interactive Codex session, without `exec` or subagents. Do not modify `main` or merge this draft branch without a new instruction.

- **No manufactured certainty:** Repeated object changes alone do not prove Lacanian desire; ordinary topic shifts or avoidance alone do not establish unconscious metonymy. State textual support, rival readings and what is not determined.
- **Correct concept mapping:** Freud's condensation (Verdichtung) corresponds to metaphor; displacement (Verschiebung) to metonymy. Compare the actual source wording before changing an inherited note.
- **Bibliographic cross-check:** Distinguish a book's print table of contents from chronology or enumeration in a footnote. In the 1966 French `Écrits`, `Le séminaire sur « La Lettre volée »` follows the opening text as the first substantive article (p.11). Do not revive the false “item 11 contradicts first article” finding.
- When a BC's expected answer or the SOP's criteria change, mark previous trial PASS as superseded. Rerun **only affected arms**, preserve the history and report actual observed failures; never silently convert old trials to new PASS.
