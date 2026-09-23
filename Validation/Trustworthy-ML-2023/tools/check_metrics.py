"""Metric-register consistency.

`SOP-08` §4 is the single definition site for registered metric keys used in the SOP/Benchmark
artifacts. This checker covers lower-case snake_case identifiers inside inline-code spans; it does
not claim to detect metric-like names written only in prose, short identifiers such as `x_y`, or
capitalized aliases. Inline-code spans are tokenized internally, so an expression such as
`metric_a > metric_b` cannot hide either identifier from the register check. This catches the failure mode where a
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
INLINE_CODE = re.compile(r"`([^`\n]+)`")
IDENT = re.compile(r"\b[a-z](?:[a-z0-9_]{2,}[a-z0-9])\b")
CELLS = re.compile(r"(?<!\\)\|")          # an escaped \| inside a formula is not a column break


def _row(line):
    return [c.strip() for c in CELLS.split(line.strip().strip("|"))]


def register():
    """(names, rows, columns, row_map) parsed from the first table of SOP-08 §4."""
    text = C.read(REGISTER_FILE)
    section = text.split("## 4.")[1].split("## 5.")[0]
    names, rows, width, row_map = set(), 0, None, {}
    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        cells = _row(line)
        rows += 1
        if width is None:
            width = len(cells)
        elif len(cells) != width:
            print(f"REGISTER ROW WIDTH {rows}: {len(cells)} cells, header had {width}")
        row_names = re.findall(r"`([a-z][a-z0-9_]+)`", cells[0])
        names.update(row_names)
        for name in row_names:
            row_map[name] = cells
    return names, rows, width, row_map


def inline_identifiers(text):
    """Yield snake_case identifiers from inside inline-code spans, including compound expressions."""
    for span in INLINE_CODE.findall(text):
        for tok in IDENT.findall(span):
            if "_" in tok:
                yield tok


def parser_selftest():
    sample = "`metric_alpha > metric_beta` and `plain`"
    got = set(inline_identifiers(sample))
    want = {"metric_alpha", "metric_beta"}
    return [] if got == want else [f"compound inline-code parser got {sorted(got)}, want {sorted(want)}"]


def check_unregistered():
    reg, _, _, _ = register()
    used = defaultdict(set)
    for rel, kind in C.artifacts():
        if kind == "val":
            continue                       # the validation record may quote field names
        text = C.read(rel)
        for tok in inline_identifiers(text):
            if tok in reg or tok in C.METRIC_ALLOW:
                continue
            used[tok].add(rel)
    return used


def check_aupr_contract():
    """Guard the package convention that AUPR means AP and that correctness orientations are explicit."""
    findings = []
    _, _, _, rows = register()
    generic = " ".join(rows.get("aupr", [])).lower()
    success = " ".join(rows.get("aupr_success", [])).lower()
    error = " ".join(rows.get("aupr_error", [])).lower()
    for phrase in ("non-interpolated average precision", "positive class", "score"):
        if phrase not in generic:
            findings.append(f"aupr row missing contract phrase {phrase!r}")
    if "trapezoidal" not in generic:
        findings.append("aupr row does not exclude trapezoidal PR integration")
    if "positive = success" not in success or "confidence `c`" not in success:
        findings.append("aupr_success row does not bind positive=success and score orientation=c")
    if "positive = error" not in error or ("`1 − c`" not in error and "`1 - c`" not in error):
        findings.append("aupr_error row does not bind positive=error and score orientation=1-c")
    return findings


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
    reg, rows, width, _ = register()
    parser = parser_selftest()
    unreg = check_unregistered()
    shape = check_register_cites()
    aupr_contract = check_aupr_contract()
    for f in parser:
        print("PARSER " + f)
    for tok, where in sorted(unreg.items()):
        print(f"UNREGISTERED `{tok}` in {sorted(where)}")
    for f in shape:
        print("REGISTER SHAPE " + f)
    for f in aupr_contract:
        print("AUPR CONTRACT " + f)
    if not quiet:
        print(f"register: {rows} rows x {width} columns, {len(reg)} metric names")
    print(f"check_metrics parser_findings={len(parser)} unregistered={len(unreg)} "
          f"shape_findings={len(shape)} aupr_contract_findings={len(aupr_contract)} "
          f"register_size={len(reg)}")
    return 1 if (parser or unreg or shape or aupr_contract) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
