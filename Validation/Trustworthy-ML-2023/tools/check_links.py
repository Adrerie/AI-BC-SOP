"""Link integrity, SOP<->Benchmark cross-link symmetry, and a near-duplicate prose probe.

Runs on committed markdown only; no source PDF needed.

Links      - every relative markdown target resolves to a file that exists in the repository.
Symmetry   - an SOP that names a benchmark should be named back by that benchmark, and vice versa;
             an asymmetric link is almost always a document that stopped being relevant, or one
             that was never updated when its counterpart changed.
Duplication - a 9-gram of prose repeated verbatim between two artifacts. The package is meant to
             link rather than copy (see the group READMEs' standing rules), so a shared run is a
             smell that a procedure was duplicated instead of referenced. Deliberate table rows and
             link paths are excluded.
"""
import os
import re
import glob
import sys
from collections import defaultdict

import _common as C

ROOT = C.ROOT
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
NAME = re.compile(r"\b(SOP-0\d|BM-0\d)\b")
WORD = re.compile(r"[a-z]{3,}")


def repo_markdown():
    out = []
    for path in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        if rel.startswith(("_audit/", "Validation/Trustworthy-ML-2023/tools/.cache")):
            continue
        if "node_modules" in rel or "/.git/" in rel:
            continue
        out.append(rel)
    return sorted(out)


def check_links():
    bad = []
    for rel in repo_markdown():
        path = os.path.join(ROOT, rel)
        for n, line in enumerate(C.read(rel).splitlines(), 1):
            for _, target in LINK.findall(line):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                tgt = target.split("#")[0]
                if not tgt:
                    continue
                dest = os.path.normpath(os.path.join(os.path.dirname(path), tgt))
                if not os.path.exists(dest):
                    bad.append(f"{rel}:{n} -> {target}")
    return bad


def _doc_index():
    """Map 'SOP-04' / 'BM-03' keys to their artifact paths."""
    idx = {}
    for rel, kind in C.artifacts():
        key = os.path.basename(rel)[:6].rstrip("-")
        if key.startswith(("SOP-", "BM-")):
            idx[key] = rel
    return idx


def _links_out(rel, section_prefix):
    """Document keys named inside the given section of a document."""
    out = set()
    for sec in re.split(r"^## ", C.read(rel), flags=re.M):
        if sec.startswith(section_prefix):
            out.update(NAME.findall(sec))
    return out


def check_symmetry():
    """An SOP->BM or BM->SOP relationship must be acknowledged by the document on the other end.

    Acknowledgement is any mention inside the counterpart -- normally its §11 / §12 or its inputs --
    not a match on the same heading. A link that is not returned usually means one document stopped
    being relevant, or the other was never told it is being audited.
    """
    idx = _doc_index()
    asymmetric = []
    forward = {k: _links_out(p, "11. Links to relevant Benchmarks") for k, p in idx.items()
               if k.startswith("SOP-")}
    backward = {k: _links_out(p, "12. Related SOPs") for k, p in idx.items()
                if k.startswith("BM-")}
    mentioned = {k: set(NAME.findall(C.read(p))) for k, p in idx.items()}
    for sop, targets in sorted(forward.items()):
        for bm in sorted(t for t in targets if t.startswith("BM-")):
            if bm not in idx:
                asymmetric.append(f"{sop} links to {bm}, which does not exist")
            elif sop not in mentioned[bm]:
                asymmetric.append(f"{sop} -> {bm}: {bm} never mentions {sop}")
    for bm, targets in sorted(backward.items()):
        for sop in sorted(t for t in targets if t.startswith("SOP-")):
            if sop not in idx:
                asymmetric.append(f"{bm} links to {sop}, which does not exist")
            elif bm not in mentioned[sop]:
                asymmetric.append(f"{bm} -> {sop}: {sop} never mentions {bm}")
    return asymmetric


def _prose(text):
    """Keep only body prose: drop code, link targets, headings, tables and inline identifiers."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"\]\([^)]*\)", "]( )", text)          # keep labels, drop paths
    text = re.sub(r"`[^`\n]*`", " ", text)               # inline code / metric names
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "|", "-", "* ", "1.", "2.", "3.", "4.", "5.", "6.")):
            continue
        lines.append(s)
    return " ".join(lines)


def check_duplication(min_gram=9):
    """Artifact pairs sharing a verbatim run of `min_gram` prose words.

    Informational, not a gate: the package links rather than copies, so a long shared run means a
    procedure was duplicated and will drift on the next revision.
    """
    grams = defaultdict(set)
    for rel, kind in C.artifacts():
        if kind == "readme":
            continue
        words = WORD.findall(_prose(C.read(rel)).lower())
        for i in range(len(words) - min_gram + 1):
            grams[tuple(words[i:i + min_gram])].add(rel)
    pairs = defaultdict(int)
    for where in grams.values():
        if len(where) > 1:
            ordered = sorted(where)
            for x, a in enumerate(ordered):
                for b in ordered[x + 1:]:
                    pairs[(a, b)] += 1
    return sorted(pairs.items(), key=lambda kv: -kv[1])[:10], len(pairs)


def main(argv):
    bad = check_links()
    asym = check_symmetry()
    top, npairs = check_duplication()
    for b in bad:
        print("BROKEN LINK " + b)
    for a in asym:
        print("ASYMMETRIC " + a)
    for (a, b), n in top:
        if n > 2:
            print(f"SHARED PROSE {n} grams  {a} <-> {b}")
    print(f"check_links broken={len(bad)} asymmetric={len(asym)} "
          f"duplicate_pairs={npairs} docs={len(docs_scanned())}")
    return 1 if (bad or asym) else 0


def docs_scanned():
    return [rel for rel, _ in C.artifacts()]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
