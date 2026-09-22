"""Metric-register consistency.

`SOP-08` §4 is the single definition site: every metric name used anywhere in the package must be
registered there, and no document may quietly redefine one. This catches the failure mode where a
revision introduces a locally-defined score that a reader will meet elsewhere with a different
meaning -- the same class of error that made the first implementation state one random baseline for
two AUPR variants that have different positive classes.

Runs on committed markdown only; no source PDF needed.
"""
import os
import re
import sys
from collections import defaultdict

import _common as C

REGISTER_FILE = "SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md"
TOKEN = re.compile(r"`([a-z][a-z0-9_]{3,})`")
CELLS = re.compile(r"(?<!\\)\|")          # an escaped \| inside a formula is not a column break


def _row(line):
    return [c.strip() for c in CELLS.split(line.strip().strip("|"))]


def register():
    """(names, rows, columns) parsed from the first table of SOP-08 §4."""
    text = C.read(REGISTER_FILE)
    section = text.split("## 4.")[1].split("## 5.")[0]
    names, rows, width = set(), 0, None
    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        cells = _row(line)
        rows += 1
        if width is None:
            width = len(cells)
        elif len(cells) != width:
            print(f"REGISTER ROW WIDTH {rows}: {len(cells)} cells, header had {width}")
        names.update(re.findall(r"`([a-z][a-z0-9_]+)`", cells[0]))
    return names, rows, width


def check_unregistered():
    reg, _, _ = register()
    used = defaultdict(set)
    for rel, kind in C.artifacts():
        if kind == "val":
            continue                       # the validation record may quote field names
        for tok in TOKEN.findall(C.read(rel)):
            if "_" not in tok or tok in reg or tok in C.METRIC_ALLOW:
                continue
            used[tok].add(rel)
    return used


def check_register_cites():
    """Every register row must name a degeneracy and a validity condition, so the table can be used
    as a boundary check rather than a glossary."""
    findings = []
    text = C.read(REGISTER_FILE)
    section = text.split("## 4.")[1].split("## 5.")[0]
    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        cells = _row(line)
        if len(cells) < 4:
            findings.append(f"register row has {len(cells)} columns: {cells[0]}")
            continue
        for i, cell in enumerate(cells):
            if not cell:
                findings.append(f"register row {cells[0]} has an empty column {i + 1}")
    return findings


def main(argv):
    quiet = "--quiet" in argv
    reg, rows, width = register()
    unreg = check_unregistered()
    shape = check_register_cites()
    for tok, where in sorted(unreg.items()):
        print(f"UNREGISTERED `{tok}` in {sorted(where)}")
    for f in shape:
        print("REGISTER SHAPE " + f)
    if not quiet:
        print(f"register: {rows} rows x {width} columns, {len(reg)} metric names")
    print(f"check_metrics unregistered={len(unreg)} shape_findings={len(shape)} "
          f"register_size={len(reg)}")
    return 1 if (unreg or shape) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
