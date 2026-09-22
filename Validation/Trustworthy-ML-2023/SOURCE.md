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

## Official source and license

The book's official project website is [trustworthyml.io](https://trustworthyml.io/). The site
identifies the work as *Trustworthy Machine Learning: Theory, Applications, Intuitions*, provides the
book download and table of contents, gives the citation as arXiv:2310.08215, and explicitly labels the
book **CC BY 4.0**.

The arXiv record for *Trustworthy Machine Learning* is **arXiv:2310.08215** and names the same five
authors. It also identifies `https://trustworthyml.io/` as the book's dedicated website.

### License

The official project website states **CC BY 4.0 (Creative Commons Attribution 4.0 International)**.

For this repository, that means source-derived adaptations must provide appropriate attribution,
identify the source, link to the license, and indicate that the material has been adapted or
reconstructed. The repository does not redistribute the source PDF or bulk extracted book text.

| Source fact | Verified from |
|---|---|
| Official project website | [https://trustworthyml.io/](https://trustworthyml.io/) |
| Citation | Mucsányi et al., *Trustworthy Machine Learning*, arXiv:2310.08215 (2023) |
| Source license | CC BY 4.0, stated on the official project website: [creativecommons.org/licenses/by/4.0](https://creativecommons.org/licenses/by/4.0/) |
| Repository relationship | reconstructed/adapted methodology artifacts, not a verbatim republication |

The website and the arXiv record were both read on 2026-09-22 for this entry. A reader re-checking the
license should re-read the official site rather than this file, and update the date if the two diverge.

The audited local PDF itself does not expose the license in its metadata or front matter. That is a
property of that PDF copy, not evidence that the work is unlicensed or all-rights-reserved. External
source verification therefore takes precedence for the bibliographic and licensing record.

The practical source-handling rule remains conservative:

| Kept out of Git | Present in the artifacts |
|---|---|
| the source PDF itself | section numbers and printed page numbers (`§4.6.2`, `pp. 256-257`) |
| bulk extracted text and per-page dumps | short cited notes needed to identify a definition, and occasional brief quotations |
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
material — the procedures, protocols, scripts and notes written here. It does not, and cannot, license
the book, which is distributed by its authors under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The two are compatible, and the compatibility has one concrete requirement rather than a vague
obligation: CC BY 4.0 asks an adapter to give attribution, link to the license, and indicate if
changes were made. This package does all three — the authors and title are named above and in every
group README, the license is linked here, and each file's traceability section marks what is
`source-derived`, `synthesized`, or a `repository convention`. Nothing in the MIT grant conflicts with
that, because the MIT grant applies to the original material written in this repository while the
book's terms travel with the material adapted from it.

The working rules that follow: no redistribution of the source PDF or bulk extracted text; the source
is named and cited by section and page wherever a claim depends on it; and anything that is our
inference, calculation or convention is labeled as such rather than presented as the book's position.
Quotation is permitted under the license and is still kept short here as an editorial choice, so that
the artifacts remain a reconstruction rather than a condensed edition.

## Re-running local source checks

The local PDF scan remains useful for confirming edition metadata, pagination, headings, and the
absence of an embedded license notice in that particular file. It is **not** the authority for the
book's licensing status. Licensing should be verified from the official project website.

With PyMuPDF installed, the local-file metadata scan can still be repeated with:

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

A missing license string in the local PDF must not be interpreted as overriding the CC BY 4.0 notice
on the official project website.
