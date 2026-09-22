"""Check every printed-page anchor in the artifacts against the source's own section structure.

    python check_citations.py                 # uses the committed citation_index.json
    python check_citations.py --verbose       # list each unanchored page for manual review

What this catches, and why it exists: a citation such as "§4.6.2 (pp. 256-257)" is two claims -- the
section named, and the pages named -- and they can disagree. In the first implementation of this
package 132 of them did, because the page numbers had been transcribed from reading notes rather than
from the heading structure. The failure is silent to a reader and fatal to an audit trail, so the pair
is checked mechanically instead of by eye.

Rule: a section's text runs from its own heading to the page before the next heading that is not one
of its children; a definition or caption anchor is checked against the page its box starts on. An
anchor is only compared with the locators in its own citation clause (the text back to the previous
`;`, `)`, `|` or anchor), never with a locator from an unrelated sentence -- an earlier version that
widened the window produced a 20-263 page span and wrongly "corrected" a good citation.

No text from the source is stored or printed by this tool.
"""
import argparse
import json
import os
import re
import sys

import _common as C

NUM = r"\d+(?:\.\d+){0,3}"
ANCHOR = re.compile(r"(?<![\w.])(p{1,2}\.)\s*(\d{1,3}(?:\s*[-–]\s*\d{1,3})?"
                    r"(?:\s*,\s*\d{1,3}(?:\s*[-–]\s*\d{1,3})?)*)")
NON_PAGE = re.compile(r"^\s*%")                       # "p. 263, 8-10 %" is not a page list
SECRANGE = re.compile(r"§\s*(" + NUM + r")\s*(?:[-–]\s*§?\s*(" + NUM + r"))?")
DEFRANGE = re.compile(r"Def(?:inition)?s?\s+(" + NUM + r")\s*(?:[-–]\s*(?:Def(?:inition)?s?\s+)?("
                      + NUM + r"))?", re.I)
BARESEC = re.compile(r"(?<![\w.§])(\d+\.\d+(?:\.\d+)?)(?![\d.])")
LABEL = re.compile(r"(?:Table|Figure|Fig\.?|Eq\.?|Equation|Chapter)\s*$")
BOUNDARY = re.compile(r"[);|]")


def load_index(path=None):
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "citation_index.json")
    if not os.path.exists(path):
        raise SystemExit(f"no citation index at {path}; run build_citation_index.py --source <pdf>")
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    headings = {k: v[0] for k, v in raw["headings"].items()}
    last_page = raw.get("last_printed_page") or max(headings.values())
    # two headings can share a printed page, so the PDF reading order breaks the tie
    ordered = sorted(headings.items(), key=lambda kv: (kv[1], raw["headings"][kv[0]][1]))
    spans = {}
    for i, (num, page) in enumerate(ordered):
        hi = max(page, last_page)
        for other, opage in ordered[i + 1:]:
            if other.startswith(num + "."):
                continue                      # children stay inside the parent's span
            hi = max(page, opage)
            break
        spans[num] = (page, hi)
    return spans, raw["definitions"], raw["captions"]


def _locator_mentions(clause, spans):
    hits = [(m.start(), m.end(), "def" if rx is DEFRANGE else "sec", m)
            for rx in (SECRANGE, DEFRANGE) for m in rx.finditer(clause)]
    taken = [(a, b) for a, b, _, _ in hits]
    for m in BARESEC.finditer(clause):
        if any(a <= m.start() < b for a, b in taken):
            continue
        if LABEL.search(clause[:m.start()]):
            continue                          # "Table 2.8" is an artefact label, not a section
        if m.group(1) in spans:
            hits.append((m.start(), m.end(), "bare", m))
    return sorted(hits)


def _span_of(group, spans, defs):
    pts, ends, toks = [], [], []
    for _, _, kind, m in (group or []):
        if kind in ("sec", "bare"):
            for num in (m.group(1), m.group(2) if kind == "sec" else None):
                if num and num in spans:
                    pts.append(spans[num][0])
                    ends.append(spans[num][1])
                    toks.append("§" + num)
        else:
            nums = [m.group(1)]
            b = m.group(2)
            if b and b in defs and m.group(1) in defs:
                pa, pb = m.group(1).split("."), b.split(".")
                if len(pa) == 2 and len(pb) == 2 and pa[0] == pb[0]:
                    nums += [f"{pa[0]}.{k}" for k in range(int(pa[1]) + 1, int(pb[1]) + 1)]
            pages = [defs[n] for n in nums if n in defs]
            if pages:
                pts += pages
                ends += pages
                toks.append("Def " + "/".join(n for n in nums if n in defs))
    if not pts:
        return None
    return (min(pts), max(ends), toks)


def _group(hits, clause, reverse=False):
    """The contiguous run of locators nearest the anchor; a sentence break stops the run."""
    if not hits:
        return []
    seq = list(reversed(hits)) if reverse else hits
    group = [seq[0]]
    for nxt in seq[1:]:
        a, b = (nxt[1], group[-1][0]) if reverse else (group[-1][1], nxt[0])
        gap = clause[min(a, b):max(a, b)]
        if re.search(r"\.\s", gap) or len(gap) > 60:
            break
        group.insert(0 if reverse else len(group), nxt)
    return group


def derive(clause, spans, defs, trailing=""):
    """(lo, hi, tokens) implied by the locators beside the anchor, or (None, None, [])."""
    parts = [p for p in (_span_of(_group(_locator_mentions(clause, spans), clause, reverse=True),
                                  spans, defs),
                         _span_of(_group(_locator_mentions(trailing, spans), trailing), spans, defs))
             if p]
    if not parts:
        return None, None, []
    return min(p[0] for p in parts), max(p[1] for p in parts), [t for p in parts for t in p[2]]


def cited_pages(txt):
    out = set()
    for part in txt.replace("–", "-").split(","):
        part = part.strip()
        if "-" in part:
            a, b = [int(x) for x in part.split("-", 1)]
            out.update(range(min(a, b), max(a, b) + 1))
        elif part.isdigit():
            out.add(int(part))
    return out


def check(verbose=False):
    spans, defs, captions = load_index()
    bound = drift = unbound = 0
    findings, manual = [], []
    for rel, _ in C.artifacts():
        text = C.read(rel)
        last_end = 0
        for m in ANCHOR.finditer(text):
            tail = text[m.end(2):m.end(2) + 90]
            if NON_PAGE.match(tail):
                continue
            bounds = [b.end() for b in BOUNDARY.finditer(text) if b.end() <= m.start()]
            clause = text[max(bounds + [last_end]):m.start()]
            line = text.count("\n", 0, m.start()) + 1
            old = re.sub(r"\s+", " ", m.group(2)).strip()
            pages = cited_pages(old)
            if not pages:
                continue
            context = text[max(0, m.start() - 60):m.end(2) + 60]
            label = re.search(r"(Table|Figure|Fig\.?)\s*(\d+(?:\.\d+)?)\D{0,8}$", clause)
            # the locator following the anchor, cut at the next boundary or sentence break
            tail = re.sub(r"^\s*\)", "", text[m.end(2):m.end(2) + 90])
            stop = re.search(r"[();|]|\.\s|(?<=\.)$", tail)
            trailing = tail[:stop.start()] if stop else tail
            lo, hi, toks = derive(clause, spans, defs, trailing)
            allowed = set(range(lo, hi + 1)) if lo is not None else set()
            if label:
                # a caption may be cited alone or mixed into a section list ("pp. 90-92, 103")
                page = captions.get(f"{label.group(1).lower()} {label.group(2)}")
                if page:
                    allowed = allowed | {page}
                    if pages <= allowed:
                        bound += 1
                        last_end = m.end(2)
                        continue
            if not allowed:
                unbound += 1
                manual.append(f"{rel}:{line}  {m.group(1)} {old}  | "
                              f"{re.sub(chr(10), ' ', context)[:70]}")
                continue
            bound += 1
            last_end = m.end(2)
            if not pages <= allowed:
                drift += 1
                findings.append(f"{rel}:{line}  {m.group(1)} {old} should fall inside "
                                f"{min(allowed)}-{max(allowed)}  [{' '.join(toks)}]")
    return bound, drift, unbound, findings, (manual if verbose else [])


def main(argv=None):
    ap = argparse.ArgumentParser(description="check page anchors against the source structure")
    ap.add_argument("--verbose", action="store_true", help="list anchors with no locator in reach")
    ap.add_argument("--index", help="alternative citation_index.json")
    args = ap.parse_args(argv)
    if args.index:
        os.environ["_CITATION_INDEX_OVERRIDE"] = args.index
    bound, drift, unbound, findings, manual = check(args.verbose)
    for f in findings:
        print("DRIFT " + f)
    for m in manual:
        print("UNANCHORED " + m)
    print(f"check_citations bound={bound} drifting={drift} unanchored={unbound}")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
