"""Shared discovery and configuration for the Trustworthy-ML-2023 validation tools.

Nothing in this package reads or stores the source PDF's text: the markdown checks work on the
committed artifacts only, and the two source-dependent tools take a path from the caller
(`--source`, then the `TRUSTWORTHY_ML_2023_PDF` environment variable). No filesystem location of any
particular user is recorded here or in the artifacts.
"""
import os
import re
import glob
import sys

SOURCE_ENV = "TRUSTWORTHY_ML_2023_PDF"
PACKAGE = "Trustworthy-ML-2023"


def _utf8_streams():
    """Print findings in UTF-8 no matter what the console's code page is.

    The artifacts contain em dashes, section signs and mathematical symbols, and the finding lines
    quote them. On a Windows console the default stream encoding is the ANSI code page, so a child
    writing "—" emits bytes its parent -- which decodes as UTF-8 -- cannot read; the reader thread
    dies and the caller sees an empty result, which a gate runner would report as "detector silent"
    rather than as "output lost". Forcing the encoding here, in the module every checker imports,
    removes that whole class of environment-dependent false negative. `errors="replace"` covers a
    stream that cannot be reconfigured at all.
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):      # not a reconfigurable stream, or Python < 3.7
            pass


_utf8_streams()

# Repository root is two levels above this file: <root>/Validation/<PACKAGE>/tools/_common.py
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

SOP_DIR = os.path.join(ROOT, "SOP", PACKAGE)
BM_DIR = os.path.join(ROOT, "Benchmark", PACKAGE)
VAL_DIR = os.path.join(ROOT, "Validation", PACKAGE)

# Local, git-ignored working area for derived indexes (see .gitignore).
CACHE_DIR = os.path.join(VAL_DIR, "tools", ".cache")

SOP_SECTIONS = [
    "Purpose", "When to use", "Inputs / prerequisites",
    "Definitions needed for execution", "Procedure", "Mandatory checks",
    "Decision or stop conditions", "Common methodological failures",
    "Required outputs", "Minimum reporting requirements",
    "Links to relevant Benchmarks", "Source traceability",
]
BM_SECTIONS = [
    "Target capability / failure mode", "Evaluation hypothesis",
    "Required data and split assumptions", "Shift or stress construction",
    "Required baselines", "Primary metrics", "Secondary / diagnostic metrics",
    "Aggregation and uncertainty reporting", "Failure interpretation",
    "Computational reporting", "Validity limits", "Related SOPs",
    "Source traceability",
]

# snake_case tokens that name output fields or artifacts rather than registered metrics.
METRIC_ALLOW = {
    "generalization_type", "resource_envelope", "time_behavior", "source_coverage",
    "concept_reconstruction", "acceptance_report", "build_citation_index", "run_acceptance",
    # The 2024-2026 update audit is cited by file name inside link text, which the inline-code
    # tokenizer reads the same way it reads a metric name. These are document names, not scores.
    "source_inventory", "delta_map", "decision_log",
    "check_citations", "check_metrics", "check_prose", "check_schema", "check_structure",
    "check_tables", "citation_index", "source_index",
    "comparison_class", "cue_whitelist", "deployment_axes", "target_samples",
    "c_frozen",
}


def artifacts():
    """(relative_path, kind) for every document the checks cover. kind: sop | bm | val | readme."""
    out = []
    for rel in md_files():
        base = os.path.basename(rel)
        if rel.startswith("SOP/") and base.startswith("SOP-"):
            kind = "sop"
        elif rel.startswith("Benchmark/") and base.startswith("BM-"):
            kind = "bm"
        elif base == "README.md":
            kind = "readme"
        else:
            kind = "val"
        out.append((rel, kind))
    return out


def md_files():
    """Every committed artifact of this package, as paths relative to the repository root."""
    out = []
    for base in (SOP_DIR, BM_DIR, VAL_DIR):
        for path in sorted(glob.glob(os.path.join(base, "*.md"))):
            out.append(os.path.relpath(path, ROOT).replace("\\", "/"))
    for name in ("SOP/%s/README.md" % PACKAGE, "Benchmark/%s/README.md" % PACKAGE):
        if os.path.isfile(os.path.join(ROOT, name)):
            out.append(name)
    return sorted(set(out))


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def is_group_file(rel):
    return rel.endswith("README.md")


def source_path(cli_value=None, required=False):
    """Resolve the source PDF from the caller, without ever guessing a user's directory."""
    candidate = cli_value or os.environ.get(SOURCE_ENV)
    if candidate:
        candidate = os.path.abspath(os.path.expanduser(candidate))
        if os.path.isfile(candidate):
            return candidate
        if required:
            raise SystemExit("source PDF not found: %s" % candidate)
    if required:
        raise SystemExit(
            "this check reads the source PDF; pass --source /path/to/book.pdf or set %s" % SOURCE_ENV)
    return None


def source_ready():
    """True when a source PDF can be located, so source-dependent checks can run."""
    return source_path() is not None


def cache_file(name):
    return os.path.join(CACHE_DIR, name)


HEAD = re.compile(r"^(#{1,6})\s+(.*)$")


def headings(text):
    """Yield (level, title, line_number) for ATX headings, skipping fenced code blocks."""
    out, fence = [], 0
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fence ^= 1
            continue
        if fence:
            continue
        m = HEAD.match(line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip(), i))
    return out


def section_number(title):
    m = re.match(r"^(\d+)\.", title)
    return int(m.group(1)) if m else None


def split_table_rows(text):
    """Return lists of cell-counts for each pipe table, ignoring escaped pipes and code fences."""
    tables, current, fence = [], [], 0
    pipes = re.compile(r"(?<!\\)\|")
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence ^= 1
            continue
        if fence:
            continue
        if pipes.search(line.strip()):
            row = line.strip()
            if row.startswith("|"):
                row = row[1:]
            if row.endswith("|"):
                row = row[:-1]
            current.append(len(pipes.split(row)))
        elif current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    return tables
