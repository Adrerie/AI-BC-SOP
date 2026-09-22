# Source attribution — *Trustworthy Machine Learning* (2023)

Everything in `SOP/Trustworthy-ML-2023/`, `Benchmark/Trustworthy-ML-2023/` and
`Validation/Trustworthy-ML-2023/` is a **reconstructed and adapted methodology artifact** written
against one source. This file records what that source is, what was verified about it, and what was
not.

## The source

| Field | Value |
|---|---|
| Title | *Trustworthy Machine Learning* |
| Authors | Bálint Mucsányi, Michael Kirchhof, Elisa Nguyen, Alexander Rubinstein, Seong Joon Oh |
| Affiliation as printed in the file | University of Tübingen / Tübingen AI Center |
| Year / edition | 2023; the audited copy is the first edition, PDF created 2023-10-11 |
| Physical form of the audited copy | PDF 1.5, 375 pages, produced by `pdfTeX-1.40.25` (LaTeX + hyperref); no bookmark outline, so section structure was recovered from font metadata |
| File name as received | `Trustworthy Machine Learning book 2023.pdf` |
| Keywords in file metadata | Machine Learning, Scalability, Trustworthiness, OOD Generalization, Explainability, Uncertainty, Evaluation |
| Pagination | printed book page = PDF page − 2, measured from the book's own printed folios and recorded in `tools/citation_index.json` |

Title, authors, year, format and page structure above are read directly from the audited file, so they
are verifiable by anyone who holds the same copy.

## Official source and license: recorded as unverified

The audited copy contains **no publisher page, ISBN, DOI of its own, or license/copyright notice**.
This was checked, not assumed: scanning all 375 pages plus the PDF metadata finds no ISBN or
ISBN-shaped number anywhere, and the word "copyright" occurs exactly once — in §3.13 (printed p. 218),
where training-data attribution is floated as a way to investigate copyright infringement in
generative models. That is a topic the book discusses, not a notice about this book. Every occurrence
of "DOI", "arXiv", "Springer" or "MIT Press" sits in a bibliography entry describing some *other*
work. PDF metadata carries title, authors, keywords and the `pdfTeX` producer only, with no publisher
field. An attempt to confirm an official publisher or project page from the web during Revision 01 did
not produce something verifiable enough to cite, so nothing is cited here.

This file therefore does **not** assert a URL, a publisher, or a license for the book. Treat the work
as **all rights reserved by its authors** unless and until an official notice says otherwise. Anyone
who confirms the official reference should add it here with the date and the page it was read from,
rather than editing this section in place.

The consequence we act on is deliberate and does not depend on the uncertainty: **no book text is
redistributed in this repository.**

| Kept out of Git | Present in the artifacts |
|---|---|
| the source PDF itself | section numbers and printed page numbers (`§4.6.2`, `pp. 256-257`) |
| bulk extracted text and per-page dumps | short cited notes needed to identify a definition, and the occasional quoted phrase or clause-length fragment |
| any machine-local path to the book | a derived citation index of labels → printed pages, containing no sentences (`tools/citation_index.json`) |

## What these files are

- Reading the source: the audit trail in `source_coverage.md` records what was read, at which section,
  and with what disposition (`incorporate`, `supporting`, `redundant`, `out-of-scope`).
- `concept_reconstruction.md` reorganizes the material by evaluation problem rather than by chapter,
  and labels each rule `source-derived`, `synthesized`, or `repository convention`.
- The SOPs and Benchmarks are **not** a restatement of the book. They are procedures and evaluation
  protocols written by hand for this repository, motivated by the source's distinctions; where they go
  beyond it, the traceability section of each file says so, and Revision 01's corrections say so too.
- Verification of the source-dependent claims requires your own copy of the book, pointed at with
  `--source` or `TRUSTWORTHY_ML_2023_PDF`; see [`tools/README.md`](tools/README.md).

## Relationship to the repository license

The repository as a whole is MIT-licensed (`LICENSE`). That license covers the repository's own
material — the procedures, protocols, scripts and notes written here. It does not, and cannot, grant
rights in the underlying book: quotation, adaptation and term ownership in the artifacts remain
subject to the attribution obligations associated with that source, which this file records.

Where the two interact, the working rules are: no redistribution of source text; the source is named
and cited by section and page wherever a claim depends on it; and anything that is our inference,
calculation or convention is labeled as such rather than presented as the book's position. If a
derivative-work question becomes material (for example, publishing these artifacts under a different
license, or quoting at greater length), resolve the "Official source and license" gap above first —
the uncertainty is documented here precisely so that it is not silently assumed away.

## Re-running the license scan

The statements above are a claim about one file, and they take ten lines to re-check against a copy you
hold. With PyMuPDF installed:

```python
import re, sys, fitz
doc = fitz.open(sys.argv[1])
pat = re.compile(r"(97[89][\s-]?(?:\d[\s-]?){10}|copyright|©|creative commons|cc[- ]by|"
                 r"all rights reserved|licensed under)", re.I)
for n, page in enumerate(doc, 1):
    for line in page.get_text("text").splitlines():
        if pat.search(line):
            print(f"pdf p.{n}: {line.strip()[:100]}")
print("metadata:", doc.metadata)
```

Expected on the audited edition: one body-text hit for "copyright" (§3.13), no ISBN or license hit, and
a metadata dictionary with no publisher or rights field.
