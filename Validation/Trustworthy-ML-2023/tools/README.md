# Validation tools — Trustworthy-ML-2023

Mechanical checks behind the acceptance claims in
[`acceptance_report.md`](../acceptance_report.md). They exist so a reader who does not trust the report
can reproduce it: every PASS in that document is either produced by a script in this directory, or is
a judgement recorded as a judgement.

## Prerequisites

- Python 3.8 or newer. Nothing else — no third-party packages, no network.
- For one optional step only: [PyMuPDF](https://pymupdf.readthedocs.io/) (`pip install pymupdf`) and
  a copy of the source book — the authors distribute it under CC BY 4.0 at
  [trustworthyml.io](https://trustworthyml.io/), and [`../SOURCE.md`](../SOURCE.md) records the
  attribution. See *Source-dependent checks* below.

Run everything from this directory:

```
python run_acceptance.py
```

Output is one `PASS` / `FAIL` line per check plus a final `failed=N` count; the exit status is 0 only
when every executed check passes, so it can be wired into a commit hook or CI job.

## The checks

| Script | What it proves | Needs the source? |
|---|---|---|
| `check_structure.py` | every SOP carries the same 12 numbered sections and every benchmark the same 13, in order; one H1 per file; no skipped heading levels; a document's title still matches its filename; every pipe table is rectangular | no |
| `check_links.py` | every relative markdown link resolves; each SOP↔benchmark cross-reference is acknowledged by the document on the other end; flags artifacts sharing a verbatim 9-word run (the package links rather than copies) | no |
| `check_metrics.py` | every metric token used in the group is registered in `SOP-08` §4, and each register row is complete (definition, validity, degeneracy) | no |
| `check_prose.py` | placeholder phrasing ("various methods", "as appropriate", "etc.") and non-American spelling outside quoted source wording; the spelling list expands each root to its inflexions, so `randomise` also catches `randomisation` | no |
| `check_citations.py` | every printed-page anchor agrees with the section, definition or caption it is attached to | no (uses the committed index) |
| `check_gates.py` | three things: each Revision 01/02 correction is still worded where it was put; none of the known-bad wordings has come back anywhere in the normative files; and no tracked file holds a machine-local path or a bulk text dump | no |
| `mutation_test.py` | runs representative end-to-end mutations in a scratch worktree and requires the relevant gate class to fail; regex-level self-tests inside `check_gates.py` separately exercise every regression pattern | no (needs `git`) |
| `build_citation_index.py` | regenerate or verify `citation_index.json` against a PDF you hold | yes |
| `run_acceptance.py` | run the suite and report the gate table | no |

Individual scripts take `--quiet` (summary line only) where that is meaningful;
`check_citations.py --verbose` lists the anchors that carry no locator.

## Source-dependent checks

The citation check is the one that could fail silently: a page number can stay plausible while
contradicting the section named beside it. It works from
[`citation_index.json`](citation_index.json), which holds only derived facts — a section /
definition / caption label, the printed page it starts on, the reading order, and the page offset
between PDF pages and printed pages (`printed = pdf page − 2`, measured from the book's own folios).
**No text from the source is stored or printed by these tools**, and the source PDF is not part of
this repository.

To confirm the committed index still describes the copy you hold:

```
python build_citation_index.py --source /path/to/the-book.pdf --check
```

or point the tools at it once for the whole session:

```
export TRUSTWORTHY_ML_2023_PDF=/path/to/the-book.pdf
python run_acceptance.py
```

`--source <pdf>` without `--check` rewrites the index; `run_acceptance.py --rebuild-index --source
<path>` does the same and then re-runs the suite. Both forms exist because no user's filesystem path
is recorded anywhere in the repository: the bibliographic description of the source lives in
[`SOURCE.md`](../SOURCE.md), and the location of the file is a runtime argument.

## Reading the output

- `check_structure findings=0` — schema and layout conform.
- `check_links broken=0 asymmetric=0` — links resolve; every relationship is acknowledged both ways.
  The `duplicate_pairs` count is informational.
- `check_metrics unregistered=0 register_size=22` — the shared register covers every score used.
- `check_prose vague=0 spelling_variants=0` — phrasing and spelling conform. Text inside typographic or
  straight double quotes is exempt by design, because wording reproduced from the source must not be
  restyled: the book is American-English apart from "towards", which it writes 37 times.
- `check_citations bound=N drifting=0 unanchored=M` — `drifting` is the gate: an anchor whose pages
  contradict its own locator. `unanchored` counts page numbers stated without any locator in the same
  clause — permitted, and listed by `--verbose` so a human can confirm each is intentional.
- `check_gates markers_found=M markers_total=20 regression_patterns=11 regressions=0
  invariants=6 invariant_misses=0 normative_files=23 hygiene_scanned=N hygiene_misses=0` — corrections
  still in place, no known-bad wording anywhere in the normative files, the attribution record
  internally consistent, and no machine-local path or bulk text in tracked files. `--list` prints the
  per-issue and per-principle tables.
- `mutation_test cases=10 failures=0` — all 10 representative end-to-end injected regressions were detected. This is not a claim that every individual marker/invariant has its own worktree mutation; every regression regex is additionally exercised by `check_gates.py`'s synthetic self-test.

Output is UTF-8 whatever the console's code page is, and that is a correctness property rather than
cosmetics: `run_acceptance.py` and `mutation_test.py` read a checker's stdout as UTF-8, so a finding
line written in a legacy code page would be *lost* on the way to the caller, who would report a
detector that had in fact fired as silent. `_common.py` sets the encoding on import, and both callers
decode with replacement instead of raising.

## What is deliberately not scanned, and why

Every exemption is a place a regression could hide, so they are listed rather than implicit.

- `plans/` is excluded from the hygiene scan. It is the reviewer's input, kept verbatim, and it contains
  one elided example path (`D:\...`) that is precisely the thing being discussed. Nothing in the
  package reads it.
- `acceptance_report.md` is excluded from the **negative** wording scans. Its job is to quote superseded
  positions in order to record them, so a phrase-level scanner cannot tell its history from a
  regression; the report is swept by hand each revision cycle instead, and the sweep is reported.
- Fenced code blocks are excluded from wording scans, since commands and sample scripts are not
  normative claims — `SOURCE.md`'s own license scanner, for instance, contains the strings it hunts.
- A wording match is ignored when the *same clause* denies it: "not as an OOD family" asserts the
  corrected position. The window is clause-scoped on purpose; a wider one suppressed real violations
  that merely followed a sentence containing "not".
- `check_gates.py` and `mutation_test.py` do not scan themselves, because they carry the patterns as
  regex source.

## What these tools do not cover

Claim grounding — that a stated position really appears in the source at the cited section — cannot be
checked without reading the source. The book is CC BY 4.0, so short quotation is permitted; this
repository still keeps the PDF and bulk extracts out of Git as an editorial choice, which means those
grounding checks stay in the audit trail: `source_coverage.md` records what was read and where, and
`acceptance_report.md` states which claims were verified by targeted re-reading rather than by script,
so the reader can see which is which.
