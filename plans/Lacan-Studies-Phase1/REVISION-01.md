# Phase 1, focused repair (Revision 01)

## Scope

The substantial two-book reading notes already exist. **Do not reread both books from scratch, rewrite the notes wholesale, or start phase 2.** This pass closes only issues that require the local EPUB/PDF or original session record. The immediately verifiable editorial corrections have already been committed to this branch.

## Remaining work

1. **EPUB note references.** Inspect the preserved note component in the local Zhang Yibing EPUB. Check the actual correspondence for notes [31]–[71], especially the biography/序幕 passages previously marked wholly unavailable. Keep [72]–[1023] as missing unless the source actually contains them. Amend only affected sentences in `SOURCE.md`, `reading_map.md` and the Zhang notes. Do not claim that a present endnote was checked against Lacan's original text.

2. **Execution record.** Check the actual prior Codex session if accessible. The `reading_map.md` says subagents read the files, contrary to the user's earlier instruction. Confirm whether subagents were actually used. Preserve an honest statement of any deviation. If logs are unavailable, say **unverified**; do not erase the recorded claim or pretend compliant execution. Keep the difference between chapter-index coverage and demonstrated full-body reading explicit.

3. **Targeted source-dependent corrections only.** Inspect local passages needed to settle the outstanding note-range ambiguity and any quotations/formula descriptions directly affected by the editorial fixes. Preserve "missing figure / formula" and "primary text unverified" markers. Do not reconstruct absent figures, assert primary-source fidelity or turn controversial philosophical interpretations into certain facts.

4. **Finish.** Read the diff for these affected files once, correct remaining local mismatches, and update this plan's short status. Commit and push the current branch; **do not merge main**. Report actual checks and unresolved limits.

## Limits

One interactive Codex session only. **No `exec` invocation or subagents.** No third book, clinical SOP/BC, new framework, additional scoring, scripts, hashes, acceptance cycles, empty files, or blanket revalidation. Expand the task only to repair a concrete inconsistency uncovered by these four steps.

## Status (2026-10-10)

1. **EPUB note references — done.** All 71 preserved note paragraphs were matched against the body anchors (no orphan note, no missing number): [1] in `02_卷首语`, [2]–[6] in `03_修订版前言`, [7]–[30] in `04_序`, [31]–[71] in `06_一_拉康出生_活着和死去`, whose body markers actually run to [78]. Items [31]–[71] were each inspected (long ones read at their opening), and [1][2][5][6][21][65][70][71] were read in full. The break therefore starts **inside 序幕·一 at [72]** (same file, P015), not at 第一章; [72]–[1023] remain absent and keep their 不可核 marks. The correspondence holds at the **numbering** level only, and one content-level mismatch was found inside the preserved range: [70]'s anchor sits on the sentence about Althusser's 1964 "Freud and Lacan" while the note discusses the 1969 "Ideology and Ideological State Apparatuses"; neighbours [65]–[68] and [71] do match their anchors. Statements in `SOURCE.md`, `reading_map.md`, the Zhang note (§一/§二/§五/§九) and `concept_reconstruction.md` were corrected accordingly. Surviving notes are registered as 张一兵's own secondary-source entries only — none was checked against Lacan or a third-party original, and two internal defects in the note apparatus itself are recorded ([48] Bataille "1814 … baptised" against his 1897 birth; [65] item 10 《忧郁症》 against French L'angoisse). The four doubtful biography facts were re-checked individually and all stay unverified ([53] and [57] turn out not to source the claims they are attached to).
2. **Execution record — done, deviation confirmed.** Parsing the local session transcript showed the previous round **did launch subagents**: 25 calls (17 chapter-evidence reads, 8 book-note drafting attempts), 13 returned, 12 aborted (3 connection interruptions, 3 rejected calls, 4 content-filter refusals, 2 credit-limit stops). This contradicts the plan's "no subagents" rule; the user's mid-session instruction is recorded as the trigger but does not erase the deviation. Registered as such in `reading_map.md` §三 and the plan Status; the original claim was not deleted or softened. Coverage is now stated explicitly as chapter/index correspondence, not a demonstrated paragraph-level reading rate.
3. **Targeted source checks — done.** Only passages needed to settle the note range and the affected citations were opened: every item of the `66_注释.txt` component, the anchors in `02`/`03`/`04`/`06`, `63_参考文献.txt`, and `34_二_概念_存在的尸体.txt` P004. The 《被窃的信》"第一篇" problem is now stated as an internal conflict between 正文 and the book's own preserved note [71] (which lists it as item 11 of the French Écrits and gives no order for the 19-piece 褚孝泉 selection); no judgment was substituted for the missing 中译本目录. No lost formula, figure, note or primary citation was reconstructed.
4. **Finish — done.** Affected files only; no rereading of either book, no wholesale rewrite, no new file besides this status.

**Unresolved after this pass**: page/issue verification of any citation against Lacan, Freud or third-party originals; the 褚孝泉 translation's table of contents; the paper editions of both books; all formulas/plates lost in the 永夜微光 re-typeset copy; and every citation carried by [72]–[1023].
