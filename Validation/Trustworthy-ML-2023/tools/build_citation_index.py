"""Rebuild the citation index from your own copy of the source, or check it against one.

    python build_citation_index.py --source /path/to/the-book.pdf            # write citation_index.json
    python build_citation_index.py --source /path/to/the-book.pdf --check    # diff, don't write
    TRUSTWORTHY_ML_2023_PDF=/path/to/the-book.pdf python build_citation_index.py --check

Why an index exists: `check_citations.py` has to know which printed page each section, definition
and caption starts on. Re-deriving that from the PDF for every run would make the citation check
useless to anyone who does not own the file, so the derived facts are committed: a label, a printed
page, and a sort order. No sentence, phrase or passage of the source is stored -- section numbers and
page numbers are facts, not expression -- and the PDF itself is not in this repository.

`--check` is what a reviewer runs to confirm the committed index still describes the book they hold.

Requires PyMuPDF (`pip install pymupdf`).
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

import _common as C

NUM = r"\d+(?:\.\d+){0,3}"
HEADING_NUM = re.compile(r"^(?:\d+(?:\.\d+){0,3}|[A-Z](?:\.\d+){1,2})$")
CHAPTER_SIZE = 18.0            # "Chapter 1" is 19.9pt, "2 OOD Generalization" 20.1pt
CHAPTER_LINE = re.compile(r"^(?:Chapter\s+)?(\d+|[A-Z])\b")
DEF_LINE = re.compile(r"^Definition\s+(" + NUM + r")\s*:", re.I)
CAP_LINE = re.compile(r"^(table|figure)\s*(\d+(?:\.\d+)?)\s*:", re.I)
FOLIO_Y = 0.80                 # printed folios sit in the bottom fifth of the page
MIN_HEADING_SIZE = 11.0        # body text is 10pt in this edition; headings are larger

def _lines(page):
    out = []
    for block in page.get_text("dict").get("blocks", []):
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            text = "".join(s["text"] for s in spans).strip()
            size = max((s["size"] for s in spans), default=0.0)
            if text:
                out.append((text, size, line["bbox"][1]))
    return out


def _page_offset(pages):
    """Printed page = PDF page - offset, with the offset read off the book's own folios."""
    votes = Counter()
    for idx, candidates in pages:
        folio = max(candidates)[1]                # the lowest bare number is the folio
        votes[idx + 1 - folio] += 1               # idx is 0-based, so PDF page = idx + 1
    if not votes:
        raise SystemExit("no printed folios could be read from this PDF")
    offset, agreed = votes.most_common(1)[0]
    if agreed < 0.9 * sum(votes.values()):
        raise SystemExit(f"folios disagree about the page offset: {dict(votes)}")
    return offset


def derive(pdf_path):
    try:
        import fitz
    except ImportError:
        raise SystemExit("this tool needs PyMuPDF: pip install pymupdf")

    doc = fitz.open(pdf_path)
    headings, definitions, captions, folio_pages = {}, {}, {}, []
    order = 0
    for idx, page in enumerate(doc):
        lines = _lines(page)
        folio = [(y, int(t)) for t, _, y in lines
                 if re.fullmatch(r"\d{1,3}", t) and y > page.rect.height * FOLIO_Y]
        if folio:
            folio_pages.append((idx, folio))
        for j, (text, size, _) in enumerate(lines):
            order += 1
            m = DEF_LINE.match(text)
            if m:
                definitions.setdefault(m.group(1), (idx, order))
                continue
            m = CAP_LINE.match(text)
            if m:
                captions.setdefault(f"{m.group(1).lower()} {m.group(2)}", (idx, order))
                continue
            # chapter headings are one line: "Chapter 1", "2 OOD Generalization", "A ..."
            m = CHAPTER_LINE.match(text)
            if m and size >= CHAPTER_SIZE:
                headings.setdefault(m.group(1), (idx, order))
                continue
            if size < MIN_HEADING_SIZE or not HEADING_NUM.match(text):
                continue
            if not re.match(r"^(?:[1-9]|[A-Z])(?:\.\d+)*$", text):
                continue                              # artefacts such as "0.0" are not locators
            if j + 1 >= len(lines):
                continue
            title, tsize, _ = lines[j + 1]
            if HEADING_NUM.match(title) or abs(tsize - size) >= 0.6:
                continue                              # a number line needs its title at the same size
            headings.setdefault(text, (idx, order))

    offset = _page_offset(folio_pages)
    printed = lambda entry: max(1, entry[0] + 1 - offset)
    last_printed = len(doc) - offset
    return {
        "offset": offset,
        "last_printed_page": last_printed,
        "folios_read": len(folio_pages),
        "headings": {k: [printed(v), v[1]] for k, v in sorted(headings.items())},
        "definitions": {k: printed(v) for k, v in sorted(definitions.items())},
        "captions": {k: printed(v) for k, v in sorted(captions.items())},
    }


def committed_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "citation_index.json")


def main(argv=None):
    ap = argparse.ArgumentParser(description="derive or verify the committed citation index")
    ap.add_argument("--source", help="path to the source PDF (or set TRUSTWORTHY_ML_2023_PDF)")
    ap.add_argument("--check", action="store_true", help="diff against the committed index instead of writing")
    args = ap.parse_args(argv)
    pdf = C.source_path(args.source, required=True)
    fresh = derive(pdf)
    if not args.check:
        with open(committed_path(), "w", encoding="utf-8") as fh:
            json.dump(fresh, fh, indent=1, sort_keys=True)
        print(f"wrote citation_index.json: {len(fresh['headings'])} headings, "
              f"{len(fresh['definitions'])} definitions, {len(fresh['captions'])} captions, "
              f"offset {fresh['offset']}")
        return 0
    if not os.path.exists(committed_path()):
        print("no committed citation_index.json to check against")
        return 1
    committed = json.load(open(committed_path(), encoding="utf-8"))
    diffs = []
    if committed.get("offset") != fresh["offset"]:
        diffs.append(f"offset: committed {committed.get('offset')} vs derived {fresh['offset']}")
    for field in ("headings", "definitions", "captions"):
        a, b = committed.get(field, {}), fresh[field]
        for key in sorted(set(a) | set(b)):
            av = a[key][0] if isinstance(a.get(key), list) else a.get(key)
            bv = b[key][0] if isinstance(b.get(key), list) else b.get(key)
            if av != bv:
                diffs.append(f"{field[:-1]} {key}: committed {av} vs derived {bv}")
    for line in diffs[:40]:
        print("DIFF " + line)
    print(f"build_citation_index --check: headings={len(fresh['headings'])} "
          f"definitions={len(fresh['definitions'])} captions={len(fresh['captions'])} "
          f"offset={fresh['offset']} diffs={len(diffs)}")
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())
