"""Run the whole mechanical acceptance suite and print one PASS/FAIL line per check.

    python run_acceptance.py              # every check that needs no source
    TRUSTWORTHY_ML_2023_PDF=/path/to/the-book.pdf python run_acceptance.py
    python run_acceptance.py --source /path/to/the-book.pdf --rebuild-index

Checks that only read committed markdown run anywhere. The citation check reads
`citation_index.json`, which is committed; when a source PDF is configured -- through `--source` or
the environment variable -- the suite also verifies that committed index against it (needs PyMuPDF).
`--rebuild-index` regenerates the index instead of only comparing it.

Exit status is 0 only when every executed check passes, so this is usable as a gate.
"""
import argparse
import os
import subprocess
import sys

import _common as C

HERE = os.path.dirname(os.path.abspath(__file__))

CHECKS = [
    ("structure",   "schema, headings, titles, tables",              "check_structure.py",  False),
    ("links",       "link targets, cross-link symmetry, duplication", "check_links.py",      False),
    ("metrics",     "metric register consistency",                    "check_metrics.py",    False),
    ("prose",       "vague phrasing, spelling variants",              "check_prose.py",      False),
    ("citations",   "page anchors vs the source's section structure",  "check_citations.py",  False),
]


def run(script, extra=()):
    cmd = [sys.executable, os.path.join(HERE, script)] + list(extra)
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    line = (proc.stdout or "").strip().splitlines()
    return proc.returncode, (line[-1] if line else (proc.stderr or "").strip().splitlines()[:1])


def main(argv=None):
    ap = argparse.ArgumentParser(description="re-run the mechanical acceptance checks")
    ap.add_argument("--source", help="source PDF, used with --rebuild-index")
    ap.add_argument("--rebuild-index", action="store_true",
                    help="regenerate citation_index.json from --source before checking")
    args = ap.parse_args(argv)

    print(f"repository root: {C.ROOT}")
    pdf = args.source or C.source_path(required=False)
    print(f"documents: {len(C.artifacts())}   source configured: "
          f"{'yes' if pdf else 'no (not needed for these checks)'}")
    failures = []
    if args.rebuild_index:
        rc, summary = run("build_citation_index.py",
                          ["--source", pdf] if pdf else [])
        print(f"{'PASS' if rc == 0 else 'FAIL'}  index-rebuild   {summary}")
        if rc:
            failures.append("index-rebuild")
    elif pdf:
        rc, summary = run("build_citation_index.py", ["--source", pdf, "--check"])
        print(f"{'PASS' if rc == 0 else 'FAIL'}  index-verify    {summary}")
        if rc:
            failures.append("index-verify")
    for name, what, script, _ in CHECKS:
        rc, summary = run(script)
        print(f"{'PASS' if rc == 0 else 'FAIL'}  {name:<14}  {what}  ->  {summary}")
        if rc:
            failures.append(name)
    print(f"run_acceptance: executed={len(CHECKS) + (1 if pdf or args.rebuild_index else 0)} "
          f"failed={len(failures)}{' (' + ', '.join(failures) + ')' if failures else ''}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
