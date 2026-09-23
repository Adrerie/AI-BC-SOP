# Acceptance Report — Trustworthy ML (2023) package

> **Status note:** Cycle 4 was accepted at `ddd1736`, then superseded by a post-review AUPR
> definition/orientation patch. The current branch must complete Revision 04 before this report can
> again be treated as the current acceptance record. Cycle 4 remains historical evidence below.



This package has been accepted four times.

| Cycle | What it was | Result | Where it stands |
|---|---|---|---|
| **1** | Plans `00`–`06` of `plans/Trustworthy-ML-2023/`: source audit, reconstruction, SOP group, Benchmark group, acceptance, wrap-up | 4 stage gates + 9 acceptance gates recorded as PASS | **Historical.** Superseded by external review; its checks were re-run from zero in Cycle 2 and its numbers appear below only where they were reproduced |
| **2** | Revision 01, `plans/Trustworthy-ML-2023/revision-01/00`–`07`: metric, setting, evidence, robustness, reproducibility and architecture corrections | ACCEPTED, then superseded on two points | **Historical**, kept because it records the corrections that still stand. Its licensing limitation and its four-level disclosure ladder were both replaced by the direct corrections that opened Revision 02 |
| **3** | Revision 02, `plans/Trustworthy-ML-2023/revision-02/00`–`03`: package-wide consistency sweep, validator hardening, final re-acceptance | ACCEPTED at `4f33897`, then superseded on metric semantics and validator wording | **Historical**, kept because its sweep and its hardened validators are the ones still in force. Its citation and duplication counts predate Revision 03 and are superseded in C4.5 |
| **4** | Revision 03, `plans/Trustworthy-ML-2023/revision-03/00`–`01`: validate the direct metric/parser patch, repair only what the run reveals, re-accept | ACCEPTED at `ddd1736`, then superseded on AUPR numerical definition and score orientation | **Historical** pending Revision 04 / Cycle 5 |

Every cycle here applies the same rule the last review handed down: a prior PASS is evidence about the
past, not a result to copy forward. Each mechanical claim below is produced by a committed script that
was re-run in a clean checkout, and each claim that is not mechanical is labeled as a reading judgement
and says what was read.

---

## Cycle 4 — Revision 03 metric semantics and validator patch

### What Revision 03 was for

A small finalization pass, deliberately. Four findings came back from the review of Cycle 3: a metric
register that named only the two correctness-positive AUPR variants, a `check_metrics` tokenizer that
could be walked past by writing a score inside a comparison expression, documentation that claimed the
mutation run covered every detector when it covered ten representative cases, and a `SOURCE.md` opening
that described the repository's own Python tooling as source-derived. The direct patch for all four was
already on the branch when this cycle started (`879915d`…`c5f75d5`). The job here was to run it in a
real checkout, repair only the regressions that run revealed, and write a current record — not to
redesign anything.

### How to re-run this

| Field | Value |
|---|---|
| Branch | `plan/trustworthy-ml-2023` |
| Direct patch under test | `879915d`…`c5f75d5` (20 artifact and tooling commits, plus the Revision 03 plan set) |
| Acceptance commit | *(this commit)* — the tree the clean runs below were taken from |
| Interpreter | Python 3.14.0, standard library only; PyMuPDF is needed for the index-verify row alone |
| Source PDF | unset for the first row, `TRUSTWORTHY_ML_2023_PDF` for the second |

```
python Validation/Trustworthy-ML-2023/tools/run_acceptance.py --with-mutations
TRUSTWORTHY_ML_2023_PDF=/path/to/the-book.pdf \
  python Validation/Trustworthy-ML-2023/tools/run_acceptance.py --with-mutations
```

Both were executed in a clean clone of the pushed branch at a different absolute path, with no local
audit working area present:

| Invocation | Checks executed | Result |
|---|---|---|
| clean checkout, no source | 7 | 7 PASS, 0 FAIL |
| clean checkout, `TRUSTWORTHY_ML_2023_PDF` set | 8 | 8 PASS, 0 FAIL |

Current output, so a reader can diff theirs against it:
`structure findings=0` · `links broken=0 asymmetric=0 duplicate_pairs=8 docs=22` ·
`metrics parser_findings=0 unregistered=0 shape_findings=0 register_size=23` ·
`prose vague=0 spelling_variants=0` ·
`citations bound=437 drifting=0 unanchored=30` ·
`gates markers_found=52 markers_total=20 regression_patterns=11 regressions=0 invariants=6
invariant_misses=0 normative_files=23 hygiene_scanned=36 hygiene_misses=0` ·
`mutation_test cases=10 failures=0` · index verified at `headings=243 definitions=87 captions=231
offset=2 diffs=0`. The scope table in C3.1 still describes the scanners exactly; nothing about what is
and is not scanned changed in this revision.

### C4.1 The four findings, closed

| # | Finding | Direct patch | Mechanical evidence | Final status |
|---|---|---|---|---|
| 1 | Generic AUPR semantics. The register defined `aupr_success` and `aupr_error` only, so a novelty- or ambiguity-positive detection score had no registered name and was written with a correctness-positive baseline attached | `SOP-08` §4 now registers generic `aupr` — declared binary task, positive class and score orientation stated, no-skill reference equal to that positive class's prevalence — and re-labels the two variants as named specializations for prediction correctness. `BM-04` §6 asks for `aupr` per declared target (H-ood positive = OOD, H-multiplicity positive = multiple-answer) and keeps the specializations for H-error only; its base-rate row and failure-mode row were re-worded to match | `register_size=23`, `unregistered=0`, `shape_findings=0`; gate markers `prevalence of the task's declared positive` (BM-04) and `no-skill reference is the prevalence of the designated positive` (SOP-08) | **CLOSED** — reading judgement: SOP-08 §4/§5, BM-03 §5/§6, BM-04 §5/§6/§9 and the Benchmark README rule 3 were read end to end; no statement now attaches a success- or error-positive baseline to a novelty- or ambiguity-positive task, and BM-03's use of the two specializations is correct because its target *is* prediction correctness |
| 2 | Compound inline-code blind spot. The tokenizer matched a whole code span, so `metric_a > metric_b` was one non-matching token and neither identifier reached the register check | `check_metrics.py` extracts identifiers from *inside* each inline-code span and adds `parser_selftest()`, which asserts that a compound span yields both names and a plain one yields none | `parser_findings=0` in every run above; probe confirmed on demand: a compound span returns both identifiers, and a deliberately invented `fake_score` inside an expression is reported as UNREGISTERED | **CLOSED for the stated class** — the residual boundary is written down rather than hidden: identifiers shorter than four characters or containing capitals (`x_y`, `Acc_shift`) are still not treated as metric names, see C4.5 |
| 3 | Mutation coverage overstated. `--with-mutations` was documented as provoking *every* gate detector, which ten worktree cases cannot do against 20 marker rows, 6 invariants and two hygiene scans | Docstring, `run_acceptance.py` label and help, `tools/README.md` and this report now say ten representative end-to-end mutations, and state separately that every regression pattern is exercised by a synthetic self-test inside `check_gates.py` | The separate claim is now countable rather than prose: `selftest()` runs 2 × 11 pattern assertions plus 6 path cases = 28 assertions, and returns empty | **CLOSED** — the two coverage kinds are distinguished wherever either is described |
| 4 | `SOURCE.md` scope. Its opening said everything under the three package directories is source-derived, which mis-attributed the validators and matters because attribution obligations differ for derived text versus original code | The paragraph now separates source-derived documentation (`SOP/`, `Benchmark/`, the validation notes) from original repository code (`Validation/Trustworthy-ML-2023/tools/`) | Attribution markers `Mucsányi`, `trustworthyml.io`, `2310.08215`, `CC BY 4.0`, `does not redistribute` still present; the license regression pattern still quiet | **CLOSED** — reading judgement: the whole file was re-read against the Cycle 2 license verification; the license, attribution and non-redistribution statements are unchanged |

### C4.2 What this cycle's run caught on its own

The patch as delivered was not green. Four validator-side regressions were repaired, and one small
benchmark consistency edit (`P(multiple)` → `P(multiple-answer)`) was added during the same cycle — which is the honest signature of a patch that
changed wording under a checker built to watch wording.

- **A gate marker broke, and it broke for the reason Revision 02 warned about.** `check_gates` required
  SOP-08 to contain `random baseline = prevalence`; Revision 03 rewrote that row for the better
  — `no-skill reference is the prevalence of the designated positive` — and the marker failed while the
  corrected position stood intact in the file. Re-pointed at the surviving phrase. This is the second
  cycle in a row where a marker encoded a *sentence* rather than a *principle*; the difference now is
  that the failure was loud.
- **`nll_bits` was allowlisted as if it were a field name.** It is not: it names a score — the
  registered `nll` with a stated log base — so allowing it past the register check is exactly what
  Plan 00 §3 forbids. The formulas in SOP-04 step 3 and the SOP-08 `perplexity` row now read
  `2^(nll)` with the base condition stated in words, the reading note in `source_coverage.md` matches,
  and the allowlist entry is gone. `METRIC_ALLOW` still carries `c_frozen` (a formula-local symbol in
  the one-bin ECE identity) and `comparison_class`, `cue_whitelist`, `deployment_axes`,
  `target_samples` (all four are output-schema fields listed in SOP-01 §10); each was checked in place.
- **A self-test example had gone stale.** The must-not-fire case for the AUPR pattern quoted the
  pre-Revision-03 sentence, so the self-test was asserting against wording the package no longer
  contains. Refreshed to the current row, which is what a regression guard should be quiet on.
- **A comment described a rule that no longer exists.** The suppression note in `check_gates.py` still
  said "the 48 characters before" a match, which is the window Revision 02 replaced with clause
  scoping after it swallowed a real violation. Corrected.

One measured side effect is worth recording because it looks like drift and is not:
`duplicate_pairs` moved from 7 to 8. The new pair is BM-05 ↔ SOP-05, sharing a 14-word run — the
robustness ordering sentence, which Revision 03 moved out of inline code and into prose, where the
duplication probe can see it for the first time. It is the package's normal SOP-to-Benchmark restatement
of one rule, the probe is informational, and the largest shared run is unchanged at 9 grams (SOP-01 ↔
`source_coverage.md`).

### C4.3 Regression check: what Revision 03 must not have broken

| Property | Cycle 3 value | Now | Reading |
|---|---|---|---|
| SOP / Benchmark counts, schema | 8 / 8, `findings=0` | unchanged | No artifact renamed, split or merged |
| Registered metric names | 22 | 23 | `aupr` added; the two specializations kept their names and their own baselines |
| Cross-links | `broken=0 asymmetric=0` | unchanged | Nothing was orphaned by the row rewrites |
| Presence markers | 52 of 52 | 52 of 52 | Two marker strings were re-pointed at wording that survives Revision 03; none was deleted |
| Regression patterns, invariants, hygiene | 11 / 6 / 36 files, all quiet | unchanged | No pre-revision sentence came back |
| Citation anchors | `bound=437 drifting=0 unanchored=30` | unchanged by the patch | The patch added no new page claims; the counts move only when this report is rewritten |
| Mutation cases | 10 / 10 | 10 / 10 | Same ten cases, now described accurately |
| Committed index | 243 / 87 / 231, offset 2, `diffs=0` | unchanged | Re-verified against the PDF, not copied |

### C4.4 Limitations that remain open

C3.5 is the standing list; these are the items whose numbers or wording Cycle 4 changes, plus one
addition. The others carry forward unchanged.

1. **`check_metrics` has a stated boundary.** A score name is only checked when it appears in an
   inline-code span, is at least four characters long, is lower-case, and contains an underscore.
   `x_y`, `Acc_shift`, or a metric named only in running prose pass unnoticed. This is the residual of
   finding 2, not a closed case.
2. **30 page anchors carry no locator** in their own clause (unchanged by this patch), and
   `duplicate_pairs=8` with a largest shared run of 9 grams, both informational.
3. **Wording-level guards stay wording-level.** The re-pointed marker in C4.2 shows the failure mode
   plainly: a rewrite that keeps a principle but changes its sentence trips the guard, and a rewrite
   that keeps the sentence but hollows the principle would not. Only the source-reading checks, recorded
   in `source_coverage.md`, settle which of the two happened.
4. **Claim grounding, numeric defaults, `ρ` direction, bounded sub-passes, printed folios, the CV-centric
   example base and second-version replication** are unchanged from C3.5 items 1, 6, 7, 8, 9, 10 and 11.

### Cycle 4 result

**ACCEPTED, and ready for review toward `main` — but not merged.** Gate R3-1 passes: AUPR semantics are
consistent across SOP-08, BM-03 and BM-04 with a generic name for declared detection targets, a compound
code span cannot bypass the register check, no pseudo metric key survives as a registered-looking name
in a normative artifact, the allowlist holds only schema fields and one formula-local symbol, and the
mechanical suite is green both with and without the source. All four findings that opened the revision
are closed above, and the five additional repairs/consistency edits made during that cycle are listed rather than
quietly folded in. Nothing from Revision 01 or Revision 02 was weakened: 52 markers, 11 silent
regression patterns, 6 invariants and 36 hygiene-scanned files behave as at Cycle 3.

| Revision 03 commit | Plan |
|---|---|
| `879915d`…`c5f75d5` | direct metric/parser patch, documentation and attribution scope, plus the Revision 03 plan set |
| *(this commit)* | 00–01 — validation of the patch, the six repairs in C4.2, and this record |

`main` was not touched: it remains at `ffdd0c0`, and the plan branch is the only thing pushed.

---

## Cycle 3 — Revision 02 consistency and final re-acceptance

### What Revision 02 was for

Revision 01 corrected positions; the review that followed found that correcting a position in one file
does not retire it from the others. Six residues survived into the package that this cycle swept, and
the more durable problem was that the validators could not see them: `check_gates` tested whether
certain sentences were still present, which says nothing about a sentence elsewhere that quietly
re-adopted the position those sentences reject. So this cycle did two things — swept the normative
files against the seven fixed principles, and rebuilt the checks to test the principles rather than
their own markers.

### How to re-run this

```
cd Validation/Trustworthy-ML-2023/tools
python run_acceptance.py --with-mutations
```

Python 3.8+, no third-party packages, no network, and no copy of the book. Add
`TRUSTWORTHY_ML_2023_PDF=/path/to/the-book.pdf` to verify the committed citation index against a PDF
you hold (needs PyMuPDF). `--with-mutations` is the Revision 02 addition: it runs 10 representative end-to-end gate mutations
in a scratch `git worktree`; every regression regex is separately exercised by the gate self-test.

Executed in a detached clean checkout at a different absolute path, with no local audit area:

| Invocation | Checks | Result |
|---|---|---|
| clean checkout, no source | 7 | 7 PASS, 0 FAIL |
| clean checkout, `TRUSTWORTHY_ML_2023_PDF` set | 8 | 8 PASS, 0 FAIL |

Current output, so a reader can diff theirs against it:
`structure findings=0` · `links broken=0 asymmetric=0 duplicate_pairs=7 docs=22` ·
`metrics unregistered=0 register_size=22` · `prose vague=0 spelling_variants=0` ·
`citations bound=437 drifting=0 unanchored=30` ·
`gates markers_found=52 markers_total=20 regression_patterns=11 regressions=0 invariants=6
invariant_misses=0 normative_files=23 hygiene_scanned=36 hygiene_misses=0` ·
`mutations cases=10 failures=0` · index verified at `headings=243 definitions=87 captions=231
offset=2 diffs=0`.

### C3.1 Validation scope, stated exactly

Claims about coverage are the easiest thing in a report to overstate, so the tool prints its own scope
and this section repeats it rather than paraphrasing it generously.

| Scan | Covers | Does not cover |
|---|---|---|
| Hygiene (paths, bulk text) | 36 tracked non-plan files (`.md`, `.py`, `.json`, `.yaml`, `.txt`) | `plans/` (22 files: reviewer input, kept verbatim, and it contains the elided example path `D:\...` that is the thing under discussion); this checker's own two source files, which carry the patterns as regex text |
| Regression wording (11 patterns) | 23 normative files: root README, both group READMEs, 8 SOPs, 8 Benchmarks, SOURCE.md, `concept_reconstruction.md`, `source_coverage.md`, `tools/README.md` | `plans/`, and `acceptance_report.md` — this document, whose job is to quote superseded wording; it is swept by hand each cycle, and this cycle's sweep is C3.2 below |
| Presence markers, invariants, schema, links, metrics, prose, citations | the committed package artifacts | anything requiring the source's text; see C3.4 |
| Wording matches inside a clause that denies them | suppressed ("not as an OOD family" asserts the corrected position) | suppression is clause-scoped, deliberately: a wider window once hid a real violation because the previous sentence happened to contain "not" |

### C3.2 The latest review's issues, item by item

Each row gives the defect, whether the fix came in the direct corrections or in Revision 02, the
mechanical evidence, and the reading judgement where a script cannot settle it.

| # | Fixed principle | Defect as found | Correction | Mechanical evidence | Reading judgement | Result |
|---|---|---|---|---|---|---|
| 1 | Source license | Cycle 2 recorded the license as unverified because the audited PDF carries no notice, and `SOURCE.md` said to treat the work as all rights reserved | Direct: `SOURCE.md` now cites the official website, arXiv:2310.08215 and CC BY 4.0; the PDF scan is retained only as an edition/metadata check | `check_gates` presence markers + the attribution invariant; the regression pattern fires if "all rights reserved" or a license-unknown claim returns anywhere in the normative files | Verified independently for this cycle: the official site states "CC BY 4.0" with the subtitle *Theory, Applications, Intuitions* and a bibtex entry for arXiv:2310.08215; the arXiv record lists the same five authors, calls the work a 373-page textbook, and links the same website. Read 2026-09-22, and consistent with the audited file (375 PDF pages, printed = PDF − 2) | **PASS** |
| 2 | Information rights | SOP-01's check-list still demanded that "nothing from the deployment stream … enter development", a universal ban the same revision had just replaced | Direct: the check is now "no deployment or target-domain information beyond the rights granted by the declared setting", with undeclared access named as the failure | Regression pattern 2 across 23 normative files; presence markers in SOP-01; the mutation test restores the old sentence and requires a failure | The rule is a scope condition, not a permission to be careless: reading of SOP-01 §6/§7 and SOP-02 §4-§6 confirms every other statement is rights-relative | **PASS** |
| 3 | Zero-shot terminology | SOP-01 imposed a repository-wide definition ("zero-shot may be used only for level (i)", semantic exposure counted as contamination), and two other files still described a four-level ladder | Direct: SOP-01 now requires exposure disclosed by kind and defers the term to the benchmark or study's own definition. Revision 02: SOP-02's and `concept_reconstruction.md`'s stale ladder references rewritten to match | Regression pattern 3 (fires on "may be used only for level (i)" or semantic exposure called contamination); SOP-01 presence markers `does not impose a universal zero-shot definition` | Reading SOP-01 §6, SOP-02 §12 and the reconstruction rows together: duplicate contamination, benchmark-specific adaptation and semantic exposure are now kept separate everywhere, and the book's single remark (§2.5.1, printed p. 37) is labeled synthesized | **PASS** |
| 4 | Adversarial ≠ OOD | BM-04 told the reader to feed BM-05's inputs "as an extreme OOD family" | Direct: that bullet now calls it a separate stress axis and denies OOD-evidence. Revision 02 added a sentence reconciling it with SOP-01 listing adversarial as a generalization *type* — the source's taxonomy of train-to-test differences, not a detection claim | Regression pattern 4; the BM-04 invariant requires both "separate stress axis" and the denial of OOD-detection evidence | `source_coverage.md` keeps the book's own §2.15 title "Adversarial OOD Generalization" as a quoted heading, which is a source fact, not the package's position | **PASS** |
| 5 | Three layers of worst-case robustness | SOP-05 and BM-05 collapsed the target, the attack and the certificate; the attack ladder was presented as if its top rung settled the worst case, and certification was defined through the source's LP/SDP chain | Direct: both files now name the target quantity, the empirical probe and the certificate separately; LP/SDP is labeled one admissible family rather than the definition | Regression patterns 5 and 6; invariants require all three layers in both files | The source supplies the masking progression and the bound chain (§2.15.12, §2.15.15, printed pp. 102-113); the separation into layers is ours, and is labeled **synthesized** in both traceability sections | **PASS** |
| 6 | Certified accuracy direction | BM README rule 8 listed "post-hoc certificate" among upper-bound rows, inverting the inequality | Direct: rule 8 now separates oracle/stronger-information rows from certificates. Revision 02: the ordering is stated where the claims are made — SOP-05 §4, BM-05 §2, the `certified_acc` register row, and the reconstruction row | Regression pattern 7 (denial-aware, so "is not an upper-bound row" passes while the old list fails); presence markers for the ordering string in both files | `certified ≤ true ≤ empirical` is analytic, not a book statement, and is now labeled that way in three places; the proviso that the comparison is void across different threat models, samples or definitions is included wherever it appears | **PASS** |
| 7 | Validation claims must match checker scope | The report and the tool described path hygiene as covering "tracked files" while the implementation skipped `plans/` | Revision 02: the tool prints its own scope, this section restates it in a table, and the exemption list is in `tools/README.md` | Regression pattern 8 catches over-claiming phrases such as "all tracked files in the repository"; the gate line reports `hygiene_scanned=36` and `normative_files=23` | — | **PASS** |

### C3.3 What the sweep found beyond the seven issues

Contradictions are usually older than the review that names them, so the same scan was run against the
principles as a set rather than one at a time.

- Two `check_gates` presence markers had encoded the *pre-correction* position: they required
  `SOURCE.md` to say "unverified" and "no book text is redistributed". They passed while the file was
  correct and would have failed once the license was fixed. Replaced with the attribution facts.
- Three superseded sentences were pinned to one file each in the checker's absence list, so the same
  wording reintroduced anywhere else would have passed. All three are now package-wide patterns
  (`random baseline = P(L = 1)`, `exponentiated nll (base 2)`, `Always split by subject`).
- `concept_reconstruction.md` contained a garbled sentence — "The two-layer/binary conditions on the
  source's bound scope that construction" — which has been rewritten.
- The clause-scoped suppression rule was itself found by a failing self-test: the first version used a
  fixed 48-character window, and a mutation injecting "attacked accuracy proves the worst case" into
  SOP-05 slipped through because the preceding sentence contained "not".
- Two defects in the checking environment surfaced only on the re-run, and both are now fixed in the
  tools rather than worked around by hand. A checker's finding line is written to the console in the
  machine's code page, and on one such console the em dash in the quoted sentence came back as bytes
  the parent could not decode: the output was lost and a detector that had in fact fired was reported
  as silent — the worst possible failure mode for a gate. `_common.py` now forces UTF-8 on the streams
  every checker writes to, and both callers decode with replacement rather than exception. Separately,
  `check_citations` flagged a real drift in this document: an internal reference written "§3.2" is
  indistinguishable from a citation to the book's own §3.2, and it sat in the same clause as a list of
  page numbers. Cycle 3's subsections therefore carry a `C3.` prefix, which no source section number
  can be confused with; the citation check across the whole report is `drifting=0`.

### C3.4 Regression check: what Revision 02 must not have broken

| Property | Status | Evidence |
|---|---|---|
| 8 SOP / 8 Benchmark structure | Unchanged | `check_structure findings=0`, 22 documents, 12- and 13-section schemas in order |
| Source traceability | Extended, not reduced | 437 anchors bound to their locator's span, 0 drifting; every SOP §12 and BM §13 present; four new traceability clauses added this cycle |
| Non-mirroring reconstruction | Unchanged | No artifact renamed, split or merged; the reconstruction gained two provenance rows |
| Operational executability | Unchanged | Steps remain numbered and imperative; `check_prose vague=0`, so no rule was softened into discretion |
| Cross-links | Unchanged | `broken=0 asymmetric=0`; the new BM-04 → SOP-01 and BM-05 → reconstruction references resolve and are answered |
| Core / Extended tiering | Unchanged | All 16 group documents carry the tier vocabulary |
| Package size | ≈57 800 words across 22 committed documents | `wc -w` over the three artifact directories |
| Revision 01's corrections | Still in force | 52 of 52 presence markers found; nothing in Revision 02's diffs removed a Revision 01 rule |

### C3.5 Limitations that remain open

The Revision 01 list is carried forward except where Revision 02 resolved it; the source-license
uncertainty is **no longer an open limitation** and appears nowhere below this line except as history.

1. **Claim grounding is not mechanically decidable here.** `check_citations` proves a page number does
   not contradict the section beside it; it cannot prove the stated position occurs in that section.
   Cycle 1 checked 56 needles by reading; Revision 02's re-reads covered printed pp. 37, 55-56, 89-92,
   102-113, 252, 256-257, 263-266, 333-342, plus the two web records in C3.2 row 1. Re-checking those
   requires the book and, for the license, the official site.
2. **The gate checks test wording, not truth.** A pattern can be satisfied by a sentence that states the
   right position fluently and misapplies it in the next paragraph. That is why `mutation_test.py`
   exists — it shows the detectors bite on the specific known regressions, which is a weaker claim than
   "the package is correct".
3. **Negative scans skip this document and `plans/`.** Both exclusions are deliberate and listed in
   C3.1; the report's own wording is swept by hand each cycle, which is a judgement, not a check.
4. **30 page anchors carry no locator** in their own clause, all of them in `source_coverage.md`'s
   reading notes and in this report's narrative, where the page is the citation.
5. **`duplicate_pairs=7` remains informational** — the largest shared run is 9 words and both printed
   cases are definitional.
6. **Numeric defaults are still absent by design**; the source supplies none and the package invents none.
7. **`ρ` direction stays a documented fidelity flag** — each artifact states the direction it uses.
8. **Catalogue clusters were read in bounded sub-passes** (attribution methods, uncertainty estimator
   families, DG benchmark survey).
9. **Page anchors are printed folios of this edition** (`printed = pdf page − 2`); section numbers
   survive another typesetting, folios do not.
10. **The package inherits the book's CV-centric examples**; a text or tabular deployment substitutes its
    own edit and partition operators.
11. **Second-version replication** is only runnable where a field re-collects evaluation data, and is
    recorded as inapplicable rather than passed where it cannot run.

### Cycle 3 result

**ACCEPTED, and ready for review toward `main` — but not merged.** All seven fixed principles hold
package-wide, both Revision 02 gates pass (C2-1 sweep with zero unresolved contradictions; C2-2
representative mutation provocation, 10/10 injected cases detected and the clean tree passing again), every pre-existing
mechanical check passes in a clean checkout, and Revision 01's corrections are all still in force.
No P0 or P1 item from the latest review remains open; the open items in C3.5 are limitations, not
unaddressed findings.

| Revision 02 commit | Plan |
|---|---|
| `e810c46`…`4cf0ce1` | direct post-Revision-01 corrections (license, information rights and zero-shot, adversarial vs OOD, three robustness layers, certificate direction, report scope) |
| `9329881` | Revision 02 plan set added |
| `39c62fb` | 01 — package-wide consistency sweep and repairs |
| `405e91c` | 02 — validators rebuilt around the principles, plus `mutation_test.py` |
| *(this commit)* | 03 — final re-acceptance and this record |

`main` was not touched: it remains at `ffdd0c0`, and the plan branch is the only thing pushed.

---

## Cycle 2 — Revision 01 re-acceptance

> **Superseded on two points, recorded here in full because Revision 01's corrections still stand.**
> The licensing limitation in §2.5 item 2 and the four-level pretraining-disclosure ladder referred to
> in §2.1 were both replaced by the direct corrections that opened Revision 02 — see Cycle 3, C3.2
> rows 1 and 3. Everything else below was re-run in Cycle 3 and still passes.

### How to re-run this

```
cd Validation/Trustworthy-ML-2023/tools
python run_acceptance.py
```

Python 3.8+, no third-party packages, no network, no copy of the book required. To also verify the
committed citation index against a PDF you hold, set `TRUSTWORTHY_ML_2023_PDF` or pass `--source`;
that adds one check and needs PyMuPDF. [`tools/README.md`](tools/README.md) explains each check and
what it cannot prove.

The suite was run in a fresh `git clone` of `plan/trustworthy-ml-2023`, at a different absolute path
from the one this package was written on, with no local audit working area present:

| Invocation | Checks executed | Result |
|---|---|---|
| clean clone, no source | 6 | 6 PASS, 0 FAIL |
| clean clone, `TRUSTWORTHY_ML_2023_PDF` set | 7 | 7 PASS, 0 FAIL |

The second row is what a reader with their own copy of the book gets: the committed
`citation_index.json` verified against the PDF at `headings=243 definitions=87 captions=231 offset=2
diffs=0`.

### 2.1 What Revision 01 changed, item by item

Each row states the defect as the reviewer put it, the repair, and the evidence re-run against it. The
result column is the status of the *repair*, not of the underlying claim — see 2.5 for what no script
here can establish.

| Issue (Revision 01 class) | Defect | Repair | Re-run evidence | Result |
|---|---|---|---|---|
| **P0-A** AUPR baseline | The shared register gave `P(L = 1)` as *the* random baseline for both AUPR variants, which is wrong for the error-positive one | The register binds the baseline to the designated positive: `P(L = 1)` for `aupr_success`, `P(L = 0)` for `aupr_error`; every PR task must name its positive class | `check_metrics`: 22 registered names, 0 unregistered, 0 malformed rows. Targeted re-read of printed pp. 265-266 confirms the book's "if P(L = 1) = 0.99 … AUPR is already 99% for a random detector" is stated for the success-positive task, and that AUPR-Error is defined by taking errors as positive. `check_gates`: marker `random baseline = prevalence` present, the pre-revision sentence absent | **PASS** |
| **P0-A** AUROC orientation | AUROC was described in a way that read as task-specific | The register makes it target-agnostic: probability a drawn positive outranks a drawn negative, under a declared positive class *and* score orientation | Re-read of printed p. 266: "the probability that a correct sample (L = 1) has a higher certainty c(x) than an incorrect one"; "for a random order, AUROC = 0.5, regardless of P(L = 1)" | **PASS** |
| **P0-A** perplexity / log base | "exponentiated NLL (base 2)" was stated once and did not constrain the NLL it exponentiates | The register and SOP-04 step 3 require a *matching* base: `exp(nll)` for natural-log NLL, `2^(nll_bits)` for NLL in bits; invariant to a common base, not to mixing | Re-read of printed p. 252 and its footnote 18 ("using base 2 in both the exponential and the logarithm"). `check_gates` marker `The two bases must match` | **PASS** |
| **P0-A** constant-confidence ECE row | The trivial control did not separate the deployable constant from the oracle one | SOP-04 step 4 carries both: a constant frozen on the calibration split (the legitimate reference row) and a constant set to the scored set's measured correctness rate (a metric diagnostic that must be labeled as one, never shipped as a baseline); the register's degeneracy column says the same | Re-read of printed pp. 256-257: the source's constant is `c = P(Ŷ = Y)`, the global accuracy, so constructing it needs label information about the scored set. `check_gates` markers `oracle`, `deployable`, `oracle quantity` | **PASS** |
| **P0-A** final-test labels in baselines | An oracle row could be read as a deployable reference | SOP-08 §5/§6 and the BM-05/BM-07 baseline tables label every oracle row as an upper bound; SOP-02 keeps the split-rights check that forbids fitting on the final test | `check_gates` marker `the only row that may support an existential claim`; `check_links` shows the cross-references are mutual | **PASS** |
| **P0-B** integrity stated as universal | Leakage and split rules were written as if one setting were the only legitimate one | Integrity is defined relative to **declared information rights** (SOP-01 §4); claims are typed per axis (step 3); rights are declared per task family (step 5, citing §2.4.2-§2.4.11); a 4-level pretraining-disclosure ladder; the setting must be re-declared when rights change | `check_gates` markers `Information rights`, `Claim-level typing`, `Pretraining disclosure`, `Re-declare`; 0 broken links, 0 asymmetric cross-links | **PASS** |
| **P0-B** legitimate adaptation mislabeled | Target-domain tuning was treated as a violation rather than as a different setting | SOP-02's ablation-under-shift check is conditional on whether the setting withholds the domain; the Benchmark README states adaptation settings are in scope and change the comparison class; SOP-01 §7 requires re-declaration instead of prohibition | `check_gates` markers `changes the setting and therefore the comparison class`, `not out of scope` | **PASS** |
| **P0-B** split strategy unconditional | Group-disjoint splitting was asserted for every project | SOP-02 step 1 splits by the highest relevant independence unit, and permits random splits where IID is the declared regime | `check_gates` marker `highest relevant independence unit` | **PASS** |
| **P0-C** contaminated final test "repaired" by rerunning | Nothing stopped a project from re-reporting on the set it had selected on | SOP-02 §6 **Post-selection independence**: three admissible responses (a new untouched test, a pre-existing untouched secondary test, downgrade and disclose), and "re-running the selected system on the same set is not a response and must not be reported as one". BM-08 audits the declared independence unit and the contamination measurement | `check_gates` markers `Post-selection independence`, `declared independence unit`, `contamination measurements` | **PASS** |
| **P0-C** independence across compared methods | Cross-split supervision parity was implicit | SOP-02 requires identical split access and tuning budget per compared method; BM-08 carries budget inequality as a violation class | Markers present in both files; symmetry check passes | **PASS** |
| **P0-D** counterfactual edits read causally | SOP-03/BM-02 presented an accuracy drop under an edit as proof of cue use | The edit outcome is now *sensitivity to the edited factor*; a causal reading requires the identification argument (isolate the cue, edit the competing cues, rule out the off-manifold route), which SOP-03 states and BM-02 §9/§11 repeat. SOP-03 also carries an explicit block on where it reads the source more narrowly than the source reads itself | Re-read of printed pp. 55-56, where the book's own decision rules are quoted and then scoped. `check_gates` markers `sensitivity to the edit`, `identification argument` | **PASS** |
| **P0-D** explanation scores over-read | A sanity or ordering result could license a soundness or human-usefulness claim | SOP-07 declares four separate contracts — model-dependence sanity, attribution ordering, end-goal usefulness, causal — plus a check that no claim moves between them | `check_gates` markers `model-dependence sanity`, `attribution ordering`, `end-goal usefulness`, `Contract boundary` | **PASS** |
| **P0-E** mitigation menu as routing table | Step 1 read as "if you have X, use method family Y" universally | Rewritten as worked examples drawn from the source's regimes; the sub-1 % unbiased fraction is now explicitly the source's *experimental regime*, "not a threshold that decides when the family applies"; simple baselines are required comparison points, not automatic winners | `check_gates` markers `admissible`, `Pareto`; direct reading of SOP-06 step 1 and §12 | **PASS** |
| **P0-E** abstention without prerequisites | Abstention was offered as an outcome without conditions | SOP-06 step 6 lists five prerequisites and step 7 four outcomes; the fall-through is "no validated action policy", not abstention by default; BM-07 §11 states the cost-table and ranking-only limits | `check_gates` markers `no validated action policy`, `the operating point is a modeling artifact`, `risk-coverage result as evidence of calibration` | **PASS** |
| **P0-F** certification limits generalized to the field | SOP-05 stated the source's certification limitation as a limit on certified robustness as a field | Prerequisites are those of the *chosen* bound; the stop condition is "no guarantee from this bound", and the certificate families considered must be listed before either sentence is written | Re-read of the source's limitation passages. `check_gates` markers `the chosen certificate`, `field limit` | **PASS** |
| **P0-F** empirical vs certified claims | An empirical result could support an existential claim | Only a certificate may support it, and only inside its assumptions; BM-05 reports the looseness gap between certified and empirical where computable | `check_gates` marker `the only row that may support an existential claim`; BM-05 §6/§7 | **PASS** |
| **P0-F** transform-defense checks unconditional | Randomized/quantizing defense breakers were prescribed without the condition that makes them apply | Attacks go through the joint pipeline where non-gradient-friendly steps are *inside the attacked function*; the requirement is method-conditional, and adversarial and corruption robustness stay different capability claims | `check_gates` marker `Attack adequacy argued, not counted`; SOP-05 §6/§7 | **PASS** |
| **P0-F** attack adequacy by iteration count | "Strong enough attack" was implied by hyper-parameters | Adequacy is threat-model-specific: an adaptive attack built against the defense under test, configuration reported rather than counted, complementary attacks. BM-05's baseline table adds the adaptive row and keeps PGD as a reference floor, not the strength oracle | Re-read of the obfuscated-gradients material (printed pp. 102-107). `check_gates` markers `adaptive`, `Attack adequacy argued, not counted` | **PASS** |
| **P0-G** acceptance not reproducible | The checks lived in a gitignored working directory; the report asked the reader to trust a script it could not see | `Validation/Trustworthy-ML-2023/tools/` now holds six checks plus an orchestrator, stdlib-only and committed. The citation check works from a committed derived index of labels and page numbers containing no source text. The source location became a runtime argument | Clean-clone runs (two invocations above); `check_gates` hygiene scan: 0 machine-local paths in tracked non-plan files covered by the hygiene scan, 0 bulk text files, audit working area still ignored | **PASS** |
| **P1-A** repository locked into silos | The root README presented source packages as the permanent shape of the repository | Packages are described as provenance-bearing staging units whose rules may extend, revise, supersede, merge, or stay source-specific; Trustworthy-ML-2023 is kept as the first package and a traceability record, explicitly not the canonical form | `check_gates` markers `provenance-bearing staging unit`, `supersede`, `merge`; nothing deleted | **PASS** |
| **P1-B** attribution and license | Cycle 2 initially treated the source license as unverified because the local PDF carried no embedded notice | Corrected after external verification: the official project website `trustworthyml.io` identifies the book, gives the arXiv:2310.08215 citation, and states CC BY 4.0. `SOURCE.md` now records that official source and removes the all-rights-reserved fallback | Official project website plus arXiv record; local PDF scan retained only as an edition/metadata check | **PASS after correction** |

### 2.2 Revision gate results

| Gate | Plan | Criteria | Result |
|---|---|---|---|
| **M** — Metric correctness | 01 | positive class declared for all PR tasks; AUPR baselines use that prevalence; AUROC target-agnostic in the register; perplexity matches the NLL log base; oracle and deployable constant-confidence separated; no final-test label inside an ordinary baseline | **PASS** (6/6) |
| **S** — Setting correctness | 02 | integrity relative to declared information rights; adaptation not mislabeled as violation; split strategy conditional on dependence structure; contaminated final tests not repairable by rerunning; multi-axis projects permitted with claim-level conditions explicit | **PASS** (5/5) |
| **C** — Evidential discipline | 03 | edits not overinterpreted causally; mitigation menus scoped as examples; no unsupported numeric threshold as a general rule; simple baselines necessary but not winners; abstention needs a validated signal and a fallback | **PASS** (5/5) |
| **R** — Robustness scope | 04 | source-specific certification limits labeled as such; empirical and certified claims distinct; transform-defense checks method-conditional; attack adequacy threat-model-specific; adversarial ≠ corruption robustness | **PASS** (5/5) |
| **V** — Validation reproducibility | 05 | tooling committed; no absolute personal path in committed files; portable source configuration; every mechanical PASS has a reproducible method; copyrighted text still excluded | **PASS** (5/5) |
| **A** — Architecture and attribution | 06 | repository not locked to silos; package remains traceable; SOURCE.md attributes the book; no long copyrighted text added | **PASS** (4/4) |
| **Re-acceptance** | 07 | all of the above re-run from zero; report rewritten; regression checked; committed to the plan branch, not merged | **PASS** — this document |

`check_gates` is the mechanical half of this table: it prints one line per Revision 01 issue class and
fails if a marker disappears or pre-revision wording returns. Current output:
`check_gates checked=47 markers_found=44 issues=20 missing=0 hygiene=0`.

### 2.3 Metric-definition consistency (shared register vs local definitions)

Plan 7 requires that no contradiction be introduced between the SOP-08 §4 register and the places that
use those metrics. `check_metrics` proves registration and row completeness, not agreement in
substance, so the metrics Revision 01 touched were read across every file that constrains them: `nll`,
`perplexity`, `ece`, `auroc`, `aupr_success`, `aupr_error`, and the oracle/deployable constant
distinction.

Files compared: SOP-04 §5/§6/§9/§12, SOP-08 §4/§5/§6/§8/§12, BM-03 §4/§6/§9, BM-04 §5/§6/§9/§13,
BM-05 §5/§6, BM-07 §5/§11, BM-08 §13, `Benchmark/README.md` rule 3, `concept_reconstruction.md`'s
provenance rows, and `source_coverage.md`'s reading notes.

Outcome: one statement of each rule, consistent everywhere it appears. AUPR's no-skill value is the
prevalence of the designated positive in all six places that state it; BM-04's novelty-positive
`P(OOD)` is an application of the same rule to a third declared positive, not a competing definition;
the 0.5 reference is attached to AUROC alone; the oracle constant is described as an oracle in all
three places that mention it. Two statements stay marked **synthesized** rather than attributed: the
class-swap generalization of the random-AUPR rule, and the report-both-curves recommendation. No
contradiction found — this was a reading check, not a script, and is recorded as such.

### 2.4 Regression check against the original strengths

| Strength from Cycle 1 | Still there? | Evidence |
|---|---|---|
| 8 SOP / 8 Benchmark decomposition | Yes — unchanged; Revision 01's master plan asked for repair rather than replacement | `check_structure`: 8 documents with the 12-section schema, 8 with the 13-section schema, in numbered order, 22 documents total |
| Non-mirroring concept reconstruction | Yes; no artifact was renamed or re-split, so the organizing axis is still workflow-stage × capability rather than the book's four areas | Reconstruction file extended with new provenance rows; chapter-to-artifact fan-out untouched |
| Source traceability | Yes, and now mechanically checked | 435 page anchors bound to their locator's real span, 0 drifting; every SOP §12 and BM §13 still present |
| Operational procedures, not chapter summaries | Yes | Steps remain numbered and imperative; Revision 01 replaced universal claims with conditional ones *inside* the same steps (SOP-01 step 5, SOP-02 step 1, SOP-06 step 1) rather than softening them into discretion, and `check_prose` fails on placeholder phrasing (`vague=0`) |
| Cross-links | Yes | `broken=0 asymmetric=0`; the two links this revision added (SOURCE.md, tools/README.md) resolve |
| Core / Extended tiering | Yes | All 16 group documents still use the tier vocabulary; 8/8 benchmark rows still `Core / Extended` |
| Duplication discipline | Yes | 7 artifact pairs share at least one 9-word prose run; the largest is 9 grams, and both printed cases are definitional (the source's generalization-type list; an AUPR clause in a register row and in a benchmark's traceability list) — informational, not a gate |
| Package size / completeness | Yes | ≈50 600 words across 22 committed documents |

### 2.5 Known limitations and what remains unproven

1. **Claim grounding is not mechanically decidable here.** `check_citations` proves a page number does
   not contradict the section named beside it; it cannot prove that the stated position occurs in that
   section. Cycle 1 verified 56 distinctive needles by reading, and Revision 01's additions were
   verified by targeted re-reads of printed pp. 55-56, 252, 256-257, 263-266 and 340. Those are reading
   judgements recorded as such, and re-checking them requires a copy of the book.
2. **The local PDF does not embed its licensing notice.** This is no longer treated as a
   licensing uncertainty. The official project website identifies the book and states CC BY 4.0,
   while the arXiv record identifies arXiv:2310.08215 and the dedicated website. The remaining local
   limitation is only that the audited PDF copy itself lacks publisher/license metadata.
3. **`check_gates` proves presence, not truth.** It catches a correction being silently reverted; it
   cannot catch a correction that was wrong when it was written.
4. **29 page anchors carry no locator** in the same clause (this report's own page references are part of that count; it moves when the report cites more pages) (`check_citations --verbose` lists them). All
   sit in `source_coverage.md`'s reading notes and in this report's own narrative, where the page *is*
   the citation; they were checked when written and lie outside the mechanical guarantee.
5. **`duplicate_pairs=7` is informational.** The package links rather than copies, so the probe reports
   shared runs without failing them; every printed case is a definitional list or a traceability clause.
6. **Numeric defaults are still absent by design.** ε, iteration budgets, bin counts and acceptance
   thresholds must be declared by the practitioner; the source supplies none and the package invents
   none.
7. **`ρ` direction remains a fidelity flag** — the source uses the symbol inconsistently between a table
   caption and its own numbers; each artifact that uses ρ states the direction it means.
8. **Catalogue clusters were read in bounded sub-passes** (attribution methods, uncertainty estimator
   families, DG benchmark survey); their use is limited to baseline menus, cost statements and
   assumption lists.
9. **Page anchors are printed folios of this edition** (`printed = pdf page − 2`, measured from the book's
   own folios and stored in the committed index). A different printing or a reflowed format moves them;
   section numbers stay valid.
10. **The package inherits the book's CV-centric examples.** Procedures are written application-neutral,
    but illustrative constructions come from that area; a text or tabular deployment substitutes its own
    edit and partition operators.
11. **The only `D:\` string in the repository sits in the reviewer's own plan file**
    (`plans/.../05_REPRODUCIBLE_VALIDATION.md`, elided there as `D:\...\`). Plans are kept verbatim as the
    input record, so it was left alone; no artifact or tool depends on it, and `check_gates`' hygiene
    scan exempts `plans/` and reports 0 everywhere else.
12. **Re-deriving the index depends on this typesetting.** `build_citation_index.py` recovers headings
    from font metadata; it verified 0 differences against this PDF (243 headings, 87 definitions, 231
    captions, offset 2) and matched an independent extraction of the same tree label-for-label and
    page-for-page, but a different typesetting would need its thresholds revisited.

### Cycle 2 result

**ACCEPTED on the plan branch.** All six Revision 01 gates (M, S, C, R, V, A) and the re-acceptance
requirements pass; every mechanical claim above was reproduced by a committed script in a clean clone;
no P0 item remains open. Two things are deliberately *not* claimed: that the source's publisher and
license have been established (limitation 2), and that any artifact-level claim has been machine-proved
against the book's text (limitation 1).

Nothing was merged to `main`. The work sits on `plan/trustworthy-ml-2023`:

| Cycle 2 commit | Plan |
|---|---|
| `4d7e12f` | 01 — metric and confidence corrections |
| `016e0db` | 02 — integrity made setting-relative |
| `a4b65cf` | 03 — causal, mitigation and abstention language |
| `1a36b5c` | 04 — certification scope and attack adequacy |
| `f2eedbd` | 05 — reproducible validation tooling |
| `3c89a68` | 06 — staging architecture and attribution |
| `e3a9c91` | 07 — re-acceptance and this report |
| `de8fa4c` | 07 — fix to the new path detector, found by the clean-clone run |
| *(and the commit that adds this row)* | 07 — keeping this table honest about itself |

The last row is why the suite is run from a clone rather than from the directory it was written in:
`check_gates`' hygiene scan passed in the working tree because its own source file was still untracked,
and failed once it was committed. Both bugs it exposed were fixed and the detector now self-tests
before it scans.

---

## Cycle 1 — original acceptance (historical record)

> **Status.** What follows is the record produced by the original Plans 1-5 run, kept because Revision
> 01's master plan asks that history stay traceable. It is **not** the current acceptance result. Two of
> its statements are flagged below where Revision 01 changed them. Apart from those flagged notes and
> Cycle 2's spelling normalization, the text is reproduced as it was written, including figures that
> Cycle 2's re-run later restated — where the two differ, Cycle 2's number is the live one.

Plan 5 artifact. Records PASS / FAIL for every gate in
`plans/Trustworthy-ML-2023/05_VALIDATION_AND_ACCEPTANCE.md`, plus the stage gates A–D.

### Completion summary

| Item | Value |
|---|---|
| Source used | *Trustworthy Machine Learning*, first edition (2023) — Mucsányi, Kirchhof, Nguyen, Rubinstein, Oh; University of Tübingen / Tübingen AI Center. Local PDF, 375 pages, full text layer, no outline (see `source_coverage.md` Step 1) |
| Work completed | 2026-09-22, on branch `plan/trustworthy-ml-2023`, executed in plan order 00 → 06 |
| Source headings audited | 247 headings in the audit tree: 243 numbered, plus 4 unnumbered front/back-matter blocks *(Cycle 2 note: the Cycle-1 text below says 237 numbered headings, from a stricter font-size rule that missed 6 subsections whose titles begin with a digit; the committed `build_citation_index.py` recovers all 243)* |
| SOP artifacts created | 8 (`SOP/Trustworthy-ML-2023/`, 12-section schema each) |
| Benchmark artifacts created | 8 (`Benchmark/Trustworthy-ML-2023/`, 13-section schema each) |
| Validation artifacts | 3 at that point: `source_coverage.md`, `concept_reconstruction.md`, this report |
| Acceptance result | **PASS** — stage gates A–D and Acceptance Gates 1–9, one revision cycle recorded in Gate 7 *(superseded: see Cycle 2)* |
| Known limitations | Seven items, listed under "Remaining issues and known limitations" below; the binding one for reuse is that no numeric default (ε, iteration budget, bin count, acceptance threshold) is supplied, because the source supplies none |

Verification was performed by mechanical checks over the committed files plus targeted re-reading of
the source PDF; the scripts that produced the numbers are listed in §V and the two
checks-that-could-fail-silently (links, metric naming) are re-runnable.
*(Cycle 2 note: all of them are now committed under `tools/`.)*

### Verification method

| Check | How it was executed | Result |
|---|---|---|
| Heading universe | Font-metadata extraction over all 375 PDF pages, cross-checked against the printed table of contents; numbering contiguity test per section | 247 headings; 49/49 sections match the TOC; no numbering gaps |
| Markdown links | Walked every `*.md` outside the local working area, resolved each relative target on disk | 0 broken links in the final package |
| Schema conformance | Tested each `SOP-*.md` for all 12 required sections and each `BM-*.md` for all 13 | 8/8 and 8/8 conform |
| Metric terminology | Extracted the metric register keys from SOP-08 §4 and scanned every artifact for snake_case names not in the register or in an allow-list of output-field names | 22 registered names; 0 unregistered uses |
| Cross-link symmetry | Parsed SOP §11 and BM §12 link sets; flagged one-directional links | 0 asymmetric links |
| Duplication | Shared 9-word verbatim n-grams between artifact pairs, ignoring links and inline code | max pair overlap 9 grams (was 57 before consolidation) |
| Claim grounding | Normalized full-text index of the source PDF; 56 distinctive needles taken from artifact claims, each resolved to its printed page and containing section | 56/56 found verbatim in the source after one needle was replaced by the book's own wording (see Gate 7) |
| Page-citation integrity | Re-derived the numbered headings straight from the PDF (standalone number line + title line) and diffed against the heading map: 0 drift, printed page = PDF page − 2 confirmed on sampled folios. Then bound every `p.`/`pp.` anchor in the artifacts to the section/definition/caption named in the same citation clause and checked it falls inside that locator's real page span | 394 anchors bound; 132 drifted anchors repaired; 0 remaining. *(Cycle 2 re-run: 435 bound, 0 drifting, after Revision 01 added citations)* |
| Editorial pass | Single-H1 and heading-level continuity per file, artifact filename matched against its own title line, schema sections present **and** in numbered order, spelling-convention scan, and a filler/hedge scan (`probably`, `roughly`, `etc.`, `it should be noted`, …) | 18 files, 0 structural findings; 129 spellings normalized to the repository's American convention with quoted book wording excluded from the change; 2 scan hits, both legitimate (a question phrasing and a quoted source sentence) |
| Non-mirroring | Lexical overlap between each artifact filename and the set of all 247 source headings | max Jaccard 0.01, mean 0.00; no filename equals a chapter or section title |

### Gate A — Source coverage (Plan 1)

**PASS.** See [`source_coverage.md`](source_coverage.md): 247 headings with disposition
(132 `incorporate`, 104 `supporting`, 2 `redundant`, 9 `out-of-scope`, **0** `needs-body-reading`),
231 of them with body reading (89 in the main pass, 142 in bounded sub-passes), source record with
file type, edition, completeness and heading machine-readability, plus a fidelity-flags list of six
source inconsistencies recorded rather than repaired. Drafting of SOP/Benchmark artifacts began only
after this gate.

### Gate B — Reconstruction (Plan 2)

**PASS.** See [`concept_reconstruction.md`](concept_reconstruction.md): 20 synthesized concepts with
contributing sections, dependencies and destination; eight separated classification axes; the
resulting 8-SOP / 8-Benchmark taxonomy; and a rule-provenance table labeling rules as
source-derived, synthesized, or repository convention.

### Gate C — SOP quality (Plan 3)

| Condition | Result | Evidence |
|---|---|---|
| Covers the main reusable workflows identified in reconstruction | PASS | Concepts C1–C18 map onto SOP-01 … SOP-08 with no unmapped operational concept; C19/C20 are declared background/catalogue |
| Executable without reading the source book | PASS | Every SOP carries its own §4 definitions, numbered procedure steps, output list and reporting minimum; source anchors live only in §12 (8–13 % of document length) |
| Checks and failure conditions, not only steps | PASS | 6–8 explicit check items per SOP in §6, plus §7 stop conditions and §8 failure lists in all 8 |
| Links to evaluation mechanisms in the Benchmark group | PASS | Each SOP §11 lists 3–8 benchmarks; symmetric back-links in every BM §12 |
| Traceability present but not dominant | PASS | Traceability share per SOP: 8 %, 10 %, 11 %, 13 %, 12 %, 13 %, 12 %, 13 % |

### Gate D — Benchmark quality (Plan 4)

| Condition | Result | Evidence |
|---|---|---|
| Each benchmark has a clearly defined target capability | PASS | §1 of each BM names capability *and* failure mode; the eight targets are distinct (shift, cue dependence, confidence, detection, adversarial, explanation, selection, protocol integrity) |
| Metrics tied to explicit questions | PASS | §2 states the hypothesis set (H-probability/H-calibration/H-ranking in BM-03; H-sound/H-order/H-goal in BM-06; H-error/H-ood/H-multiplicity in BM-04), and §6 metrics are chosen per hypothesis |
| Leakage and test-set tuning prevented | PASS | Every BM §3 designates selection material and forbids final-test selection; the once-per-project rule and the ablation caveat sit in SOP-02, audited by BM-08 |
| Components can compare methods fairly | PASS | §5 baseline tables include the trivial control, the tuned simple baseline, equal-budget requirements, and upper-bound rows marked as such |
| Each major component links back to the SOP group | PASS | 3–7 SOP back-links per benchmark, no asymmetry |

### Acceptance Gate 1 — Structural completeness

**PASS.** Present and non-empty: `SOP/Trustworthy-ML-2023/README.md` + 8 SOP documents;
`Benchmark/Trustworthy-ML-2023/README.md` + 8 benchmark documents;
`Validation/Trustworthy-ML-2023/source_coverage.md`, `concept_reconstruction.md`, and this report.
Package size ≈ 40 000 words at that point. No group is index-only.

### Acceptance Gate 2 — Source coverage accounting

**PASS.** All 247 headings are dispositioned in the coverage table; every `incorporate` row is
reachable from at least one artifact's §12/§13 anchors, `supporting` rows are named as background in
the reconstruction, `out-of-scope` and `redundant` rows carry a stated reason (navigation, index,
historical narrative, author research agenda, deployment-supervision settings, showcase, or
restatement). Zero silent omissions: the residual set is enumerated in the coverage file's
disposition summary and summarized in both group READMEs' scope notes.

### Acceptance Gate 3 — Non-mirroring / reconstruction

**PASS.** Artifact names share essentially no vocabulary with source headings (max Jaccard 0.01,
mean 0.00; no exact title match). The artifact axis is workflow-stage × capability, while the source
axis is four research areas; chapter 4 alone contributes to six concepts and appears in five
artifacts, and the eight benchmarks draw from four different chapters each. Three artifacts
(SOP-02, SOP-08, BM-08) have no chapter counterpart at all.

### Acceptance Gate 4 — SOP operationality

**PASS.** Each SOP: purpose and applicability (§1–§2), explicit inputs (§3), numbered executable
steps with Core/Extended tiers (§5), mandatory checks as a checkbox list (§6), stop conditions (§7),
outputs (§9), reporting minimum (§10), failure modes (§8). None reads as a chapter summary: the
dominant register is imperative ("write", "compute", "stop and re-declare"), and the explanatory
material is confined to definitions and traceability.

### Acceptance Gate 5 — Benchmark validity

**PASS.** Each benchmark states its target, its hypotheses (§2), split assumptions (§3), how stress
is constructed (§4), required baselines with their role (§5), primary and diagnostic metrics tied to
the hypotheses (§6–§7), aggregation and variability rules (§8), a failure-interpretation table (§9),
computational reporting (§10) and validity limits (§11). No artifact is a metric list: metrics always
appear with the question they answer and the condition under which they mislead.

### Acceptance Gate 6 — Cross-link consistency

**PASS.** Terminology is single-sourced: the metric register in SOP-08 §4 defines 22 names used
across the package, and 0 unregistered metric names are used. Bidirectional matrix (● mutual,
· not applicable):

|  | BM-01 | BM-02 | BM-03 | BM-04 | BM-05 | BM-06 | BM-07 | BM-08 |
|---|---|---|---|---|---|---|---|---|
| **SOP-01** | ● | ● | · | · | ● | · | ● | ● |
| **SOP-02** | ● | ● | ● | · | ● | · | · | ● |
| **SOP-03** | ● | ● | · | · | · | ● | · | ● |
| **SOP-04** | · | · | ● | ● | · | · | ● | ● |
| **SOP-05** | ● | · | · | ● | ● | · | · | ● |
| **SOP-06** | ● | ● | ● | ● | · | · | ● | ● |
| **SOP-07** | · | ● | · | ● | · | ● | · | ● |
| **SOP-08** | ● | ● | ● | ● | ● | ● | ● | ● |

Minimum per row and per column is 3 links; there is no one-directional pair.

### Acceptance Gate 7 — Evidence discipline

**PASS.** Sampled load-bearing claims, checked (a) that the provenance label is honest and (b) that
the wording exists in the source body text at the cited section and printed page:

| # | Claim as used in the package | Label | Source check |
|---|---|---|---|
| 1 | "We can only spoil the test set less, but we can never not spoil it." | source-derived | exact wording found, §2.3.3, p. 28 |
| 2 | Use the test set once per project / "once per paper". | source-derived | exact wording, §2.5.3, p. 39 |
| 3 | A constant confidence equal to global accuracy reaches ECE = 0 without truthfulness. | source-derived | exact wording, §4.6.2, p. 256 |
| 4 | AUROC is recommended over AUPR on unbalanced data; random AUPR equals `P(L = 1)`. | source-derived | both phrasings, §4.9.2, pp. 265-266 *(Cycle 2 qualified this: the value is the prevalence of the **designated** positive, and the swap to error-positive is ours, not the book's)* |
| 5 | "The model being safe is not equivalent to no gradient-based algorithm being able to find an attack." | source-derived | exact, §2.15.12, p. 103 |
| 6 | Fairly tuned ERM is "not worse at all" than complicated DG methods. | source-derived | exact, §5.2.2, p. 340 |
| 7 | Ranking the four remove-and-classify variants can disagree; the metric is not perfect but is the most popular. | source-derived | §3.7.7-§3.7.8, p. 188 |
| 8 | Order: declare setting → freeze splits → diagnose → measure → stress → mitigate → report. | **synthesized** | not a book statement; built from §2.3-§2.5, §2.11-§2.14 and §5.1-§5.3, labeled as such in the reconstruction |
| 9 | Core/Extended tiering, checkbox registers, artifact IDs, and the SOP-08 metric register naming. | **repository convention** | explicitly excluded from book attribution in every §12/§13 |
| 10 | Default ε values, iteration budgets, bin counts, or numeric "good" thresholds. | **deliberately absent** | the source supplies none; each artifact instead requires the practitioner to state and record the choice |

Wider sweep: 56 distinctive needles extracted from artifact statements were located in the source
full text with section resolution — all 56 match the book's wording. An earlier pass recorded one
"wording variance" for a claim attributed to the aleatoric-loss recommendation in §4.13.5; on
re-inspection the needle itself had been written as a paraphrase rather than a quotation, and the
claim belongs to SOP-04 step 10, not SOP-06. The needle was replaced by the book's own phrase
(`supported by the theory of proper scoring rules`, p. 302) and the three mislabeled artifact tags
were re-pointed at the files that actually carry the claims. No book-attributed claim in the package
failed the check, and no invented metric or formula was found: every formula in the register traces
to a cited definition number (Definitions 4.8-4.15 for scoring and calibration, 2.24-2.33 for the
shift vocabulary, 3.1-3.16 for explanations).

#### Gate 7 revision cycle — page anchors

Gate 7 initially looked weaker than the wording check implied. Re-deriving the heading pages from the
PDF independently (standalone number line plus matching-size title line, over all 375 pages) agreed
with the working heading map on 237/237 numbered headings, so the section labels were sound — but
binding each printed-page anchor to the locator in its own citation clause exposed **132 anchors**
whose pages had drifted by 1-6 pages away from the section they named. The cause was transcription:
those pages had been copied from body-reading notes rather than from the heading map, and the notes
counted pages from the extract dumps.

Repair policy, applied mechanically to digits only (no prose was rewritten):

| Situation | Action |
|---|---|
| Cited pages inside the locator's real span | Left untouched, including pinpoint single-page cites |
| Cited pages outside the span | Replaced by the span of the locator(s) in the same clause, `p.`/`pp.` adjusted |
| Several locators in one clause (`§2.2.1-§2.2.2, Definitions 2.9-2.11`) | Union of their spans |
| Page bound to a table or figure caption (`Table 2.8 (p. 103)`) | Checked against a caption map built from the PDF; a mixed list (`§2.15.3-§2.15.4 and Table 2.8 (pp. 90-92, 103)`) is validated part by part |
| Page bound to a phrase instead of a locator (5 anchors) | Resolved by locating the phrase in the full text: `p. 46` (Definition 2.28), `p. 49`, `p. 50` (Kolmogorov-complexity formula), `p. 107` (expectation-over-transformation identity), `p. 181` (chicken-and-egg) — all correct; one `p. 264` was wrong and is now `p. 263` |

After the repair: 393 page anchors bound to a section, definition or caption, **0 outside the span
those locators occupy**. The artifact text is unchanged apart from the page numbers themselves.

### Acceptance Gate 8 — Practicality

**PASS.** Two generic scenarios walked through the package as a researcher would.

**Scenario 1 — image classifier retrained yearly for a retail shelf task, new stores and camera
models.** What to define before training: SOP-01 setting block, generalization type = cross-domain,
cue whitelist marking camera/site cues as forbidden, ρ and label inventory. Splits/stress: SOP-02
group-disjoint split by store and camera, contamination pass, BM-01 leave-one-store/one-camera-out
plus a severity ladder. What to measure: `acc_avg` and `acc_worstgroup` per held-out store
(BM-01 §6), plus confidence battery per domain (BM-03). Misleading confidence detection: constant
confidence control, bin sensitivity, `mce` on the small-bin pitfall (SOP-04 §6, BM-03 §9).
Abstain/flag: BM-07 risk-coverage at the review capacity, fallback = re-photograph request.
To report: SOP-08 §10 list with cost line (yearly retraining labor is part of the result).
Remaining limits: unforeseen store formats, within-store drift, cue dependence only where
off-diagonal cells exist.

**Scenario 2 — clinical triage model where a false reassurance is far worse than a deferral.**
Define: SOP-01 with the cost table owned by the clinical stakeholder, asymmetric cost explicit,
deployment axes (site, device, population). Splits: SOP-02 with final-test contact budget and
per-subgroup support; BM-01 subpopulation cells. Measure: BM-03 with per-class `ece`/`mce` and
worst-subgroup risk; BM-04 H-error for the "does the score notice" question. Misleading confidence:
the gaming check and the probabilistic-overfitting check are mandatory before any assurance claim
(SOP-04 §6). Abstain: BM-07 operating point chosen on risk-coverage at the tolerated risk with the
escalation cost; SOP-06 stops at abstention when no admissible mitigation exists. Report: SOP-08,
including the "does not show" list. Limits: calibration is distribution-bound, so a threshold transfer
across sites is invalid; explanation-based assurance additionally needs BM-06's human-grounded track,
which the source explicitly demands rather than assumes.

In both scenarios the researcher can answer all seven questions the gate lists, and neither forces an
application-specific SOP — the scenario findings stay in this report.

### Acceptance Gate 9 — Minimal duplication

**PASS.** Shared definitions are single-sourced: recurring terms and all metric names live in SOP-08
§4, and other artifacts reference rather than restate them. Dependencies are linked, not copied
(SOP-04 links the split rules to SOP-02; BM-03 links the calibration recipe to SOP-04). Duplication
probe: the three heaviest SOP↔benchmark overlaps (57, 26 and 19 shared 9-grams) were consolidated by
making the benchmark traceability sections cite the executing SOP's anchor list and keep only
measurement-specific anchors; the remaining maximum is 9 shared 9-grams between a SOP and its own
benchmark counterpart, which is definitional restatement required to keep each document executable
standalone (Gate C). Cross-benchmark overlap is 3 grams. Book chapters that repeat a concept are
merged once (for example ECE appears in SOP-04 and BM-03 only as a name resolving to SOP-08 §4).

### Remaining issues and known limitations (as at Cycle 1)

1. **Numeric defaults are intentionally absent.** The source provides none for ε, PGD iterations, ECE
   bins, or "acceptable" calibration; the package requires them to be declared and recorded instead.
2. **`ρ` direction.** The source uses the symbol inconsistently (Table 2.5 caption versus its own
   numbers); every artifact that uses ρ states the direction. This is a documented fidelity flag, not
   a resolved ambiguity.
3. **Catalogue clusters were read in bounded sub-passes** (attribution method catalogue, uncertainty
   estimator families, DG benchmark survey) rather than line-by-line in the main pass; their use in
   the artifacts is limited to baseline menus, cost statements and assumption lists, each with
   section and page anchors.
4. **Certified robustness scope.** BM-05's certification branch is conditioned on the source's own
   limitation (binary, shallow networks); the artifact keeps it as an Extended track and forbids
   guarantee language without a certificate. *(Revision 01 Plan 4 rewrote this as prerequisites of the
   chosen method rather than a limit on the field — see 2.1, P0-F.)*
5. **Second-version replication** (a documented anti-overfitting device) is only executable where a
   field re-collects evaluation data; where it cannot be run, BM-01 and BM-08 record it as
   inapplicable rather than passed.
6. **The package inherits the book's CV-centric examples.** Procedures and metrics are written
   application-neutral, but the illustrative constructions (segmentation masks, caption noise,
   corner-case objectness scores) come from that area; a text or tabular deployment must substitute
   its own edit and partition operators.
7. **Page anchors are printed pages of this edition.** They refer to the folio numbers of the 2023
   PDF recorded in `source_coverage.md` Step 1 (printed page = PDF page − 2). A different printing or
   reflowed format shifts them; the section numbers stay valid.

### §V — Reproduction of the checks (as written in Cycle 1)

> **Superseded by Revision 01 Plan 5.** The paragraph below was true of Cycle 1 and is no longer: the
> checks are committed under [`tools/`](tools/README.md), they need no machine-local path, and the
> source-dependent step takes the PDF as a runtime argument. It is kept because it records why the
> citation binder is the check worth re-running after any edit.

The mechanical checks were a link/schema/terminology walker, a source-needle verifier, a cross-link
and duplication analyzer, and a page-citation binder. They were not committed: the verifier reads the
copyrighted PDF and the extracted text lived only in the local working area, so a future maintainer
needed the source file at a path recorded in `source_coverage.md` Step 1 to re-run it. Committed
artifacts carried the citations instead.

The citation binder is the part worth re-running after any edit, because it is the only check that
can catch a page number that contradicts its own section label. It needs three derived inputs, all
reproducible from the PDF: the heading map (number → printed page, with each section's span ending
where the next non-child heading begins), the definition map (`Definition N.M` box locations), and
the caption map (`Table N.M:` / `Figure N.M:` first pages). A heading is a standalone number line
whose following title line shares its font size; recovering headings by font metadata is necessary
because this PDF has no outline. The binder then takes the locator group in the same citation clause
as each `p.`/`pp.` anchor — including trailing locators after the closing bracket, and excluding
`Table`/`Figure` labels — and requires the cited pages to lie inside the union of those spans. That
binder is now `tools/check_citations.py`, and its three derived inputs are the committed
`tools/citation_index.json`.

### Final acceptance result (Cycle 1, superseded)

All nine acceptance gates and the four stage gates (A–D) were recorded as PASS on 2026-09-22. External
review then produced the Revision 01 finding list, which is what Cycle 2 above addresses; the live
result is the one in "Cycle 2 result".
