"""Structural conformance for the Trustworthy-ML-2023 artifacts: schema, headings, tables.

Runs on committed markdown only; no source PDF needed.

  python check_structure.py            # human-readable findings
  python check_structure.py --quiet    # one summary line, non-zero exit on findings

Schema: every SOP carries the same 12 numbered sections and every benchmark the same 13, in order.
That is what lets a reader move between documents without relearning the shape, so it is checked
mechanically rather than by convention.
"""
import os
import re
import sys

import _common as C


def check_schema():
    """Missing, misnumbered or out-of-order sections."""
    findings = []
    for rel, kind in C.artifacts():
        want = C.SOP_SECTIONS if kind == "sop" else C.BM_SECTIONS if kind == "bm" else None
        if not want:
            continue
        titles = [(lvl, t) for lvl, t, _ in C.headings(C.read(rel)) if lvl == 2]
        got = [t for _, t in titles]
        nums = [C.section_number(t) for t in got]
        for i, name in enumerate(want):
            if i >= len(got):
                findings.append(f"{rel}: missing section {i + 1} '{name}'")
            elif not got[i].lower().startswith(f"{i + 1}. {name.lower()}"):
                findings.append(f"{rel}: section {i + 1} should be '{name}', found '{got[i]}'")
            elif nums[i] != i + 1:
                findings.append(f"{rel}: section numbering out of order at '{got[i]}'")
        for extra in got[len(want):]:
            findings.append(f"{rel}: unexpected extra section '{extra}'")
    return findings


def check_heading_shape():
    """One H1, and no skipped heading levels."""
    findings = []
    for rel, _ in C.artifacts():
        prev = 0
        h1 = 0
        for lvl, title, line in C.headings(C.read(rel)):
            if lvl == 1:
                h1 += 1
                if h1 > 1:
                    findings.append(f"{rel}:{line} second H1 '{title}'")
            if prev and lvl > prev + 1:
                findings.append(f"{rel}:{line} heading level jumps {prev}->{lvl}: '{title}'")
            prev = lvl
        if h1 == 0:
            findings.append(f"{rel}: no H1 title")
    return findings


def check_titles_match_filenames():
    """The document title should share a subject word with its filename (catches renamed files)."""
    stop = {"the", "and", "for", "with", "from", "into", "under", "a", "of", "to", "on", "or", "in"}
    findings = []
    for rel, kind in C.artifacts():
        if kind not in ("sop", "bm"):
            continue
        text = C.read(rel)
        title = next((t for lvl, t, _ in C.headings(text) if lvl == 1), "")
        stem = os.path.basename(rel).split("-", 1)[-1][2:].replace("-", " ")
        tw = {w for w in re.findall(r"[a-z]{5,}", title.lower())} - stop
        fw = {w for w in re.findall(r"[a-z]{5,}", stem.lower())} - stop
        shared = {a for a in tw for b in fw if a.startswith(b[:5]) or b.startswith(a[:5])}
        if not shared:
            findings.append(f"{rel}: title '{title}' shares no subject word with filename")
    return findings


def check_tables():
    """Every pipe table has the same cell count in each of its rows."""
    findings = []
    for rel, _ in C.artifacts():
        text = C.read(rel)
        lines = text.splitlines()
        fences, in_fence = [], False
        for i, line in enumerate(lines):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
            fences.append(in_fence)
        pipes = re.compile(r"(?<!\\)\|")
        i = 0
        while i < len(lines):
            if fences[i] or not pipes.search(lines[i].strip()):
                i += 1
                continue
            block = []
            while i < len(lines) and not fences[i] and pipes.search(lines[i].strip()):
                block.append((i + 1, lines[i]))
                i += 1
            if len(block) < 2:
                continue
            widths = []
            for ln, line in block:
                row = line.strip().lstrip("|").rstrip("|")
                widths.append((ln, len(pipes.split(row))))
            base = widths[0][1]
            bad = [ln for ln, w in widths if w != base and not re.fullmatch(r"[\s:|-]+",
                                                                            dict(block)[ln - 1].strip())]
            for ln in bad:
                findings.append(f"{rel}:{ln} table row has a different cell count "
                                f"(header has {base})")
    return findings


def main(argv):
    quiet = "--quiet" in argv
    findings = (check_schema() + check_heading_shape() + check_titles_match_filenames()
                + check_tables())
    if not quiet:
        for f in findings:
            print("FINDING " + f)
        print(f"structure: {len(C.artifacts())} documents checked")
    print(f"check_structure findings={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
