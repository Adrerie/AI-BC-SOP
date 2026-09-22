"""Revision-01 gate coverage: does each corrected issue still have its correction in place?

This is a presence-and-absence check, not a proof of correctness. Revision 01 changed a specific set of
claims in a specific set of files; each change left a phrase behind that is distinctive to the corrected
position (`Attack adequacy argued, not counted`, `highest relevant independence unit`, ...), and each
change also *removed* a phrase that was only ever true of the wrong position (`random baseline = P(L = 1),
so near-useless`, which is false for the error-positive variant). A regression that quietly restores a
pre-revision sentence is therefore caught here even though nobody can mechanically prove the new claim
is right -- establishing that stays a source-reading job, recorded in `source_coverage.md`.

Two repository-level invariants are checked here too, because they are gates in their own right:
no machine-local path in a committed file, and no bulk source text (the derived index holds labels and
page numbers only). The path detector runs a self-test first, since a scan that has quietly stopped
matching anything is worse than no scan; and it skips this file, which necessarily contains the
patterns it looks for.

    python check_gates.py            # summary
    python check_gates.py --list     # also print every marker that was found

Runs on committed files only; no source PDF needed.
"""
import os
import re
import subprocess
import sys

import _common as C

# (issue, revision plan, artifact, [phrases that must appear])
PRESENT = [
    ("P0-A metric definitions", "01", "SOP/%s/SOP-04-measure-confidence-truthfulness.md" % C.PACKAGE,
     ["The two bases must match", "prevalence of *its own* positive", "deployable", "oracle"]),
    ("P0-A metric register", "01", "SOP/%s/SOP-08-report-evidence-and-validity-boundaries.md" % C.PACKAGE,
     ["random baseline = prevalence", "positive class", "oracle quantity"]),
    ("P0-A AUPR in the suite", "01", "Benchmark/%s/BM-04-error-and-anomaly-detection.md" % C.PACKAGE,
     ["prevalence of the task's declared positive"]),
    ("P0-B information rights", "02", "SOP/%s/SOP-01-specify-deployment-setting.md" % C.PACKAGE,
     ["Information rights", "Claim-level typing", "Pretraining disclosure", "Re-declare"]),
    ("P0-B split by unit", "02", "SOP/%s/SOP-02-build-evaluation-splits-under-leakage-discipline.md" % C.PACKAGE,
     ["highest relevant independence unit", "Post-selection independence", "Unit-disjointness"]),
    ("P0-B adaptation is in scope", "02", "Benchmark/%s/README.md" % C.PACKAGE,
     ["not out of scope", "changes the setting and therefore the comparison class"]),
    ("P0-C contamination is auditable", "02", "Benchmark/%s/BM-08-evaluation-integrity-audit.md" % C.PACKAGE,
     ["declared independence unit", "contamination measurements"]),
    ("P0-C post-selection independence", "02", "SOP/%s/SOP-02-build-evaluation-splits-under-leakage-discipline.md" % C.PACKAGE,
     ["Post-selection independence"]),
    ("P0-D edit is sensitivity", "03", "SOP/%s/SOP-03-diagnose-learned-evidence.md" % C.PACKAGE,
     ["sensitivity to the edit", "identification"]),
    ("P0-D cue-dependence reading", "03", "Benchmark/%s/BM-02-spurious-cue-dependence.md" % C.PACKAGE,
     ["identification argument", "sensitivity to the edited factor"]),
    ("P0-D explanation contracts", "03", "SOP/%s/SOP-07-evaluate-explanation-methods.md" % C.PACKAGE,
     ["model-dependence sanity", "attribution ordering", "end-goal usefulness", "Contract boundary"]),
    ("P0-E mitigation admissibility", "03", "SOP/%s/SOP-06-choose-mitigation-or-abstain.md" % C.PACKAGE,
     ["admissible", "Pareto", "no validated action policy"]),
    ("P0-E abstention validity", "03", "Benchmark/%s/BM-07-selective-prediction-under-cost.md" % C.PACKAGE,
     ["the operating point is a modeling artifact", "risk-coverage result as evidence of calibration"]),
    ("P0-F certification scope", "04", "SOP/%s/SOP-05-run-worst-case-stress-evaluation.md" % C.PACKAGE,
     ["Attack adequacy argued, not counted", "field limit", "the *chosen* certificate"]),
    ("P0-F attack adequacy in the suite", "04", "Benchmark/%s/BM-05-adversarial-robustness.md" % C.PACKAGE,
     ["adaptive", "the only row that may support an existential claim"]),
    ("P1-A staging architecture", "06", "README.md",
     ["provenance-bearing staging unit", "supersede", "merge"]),
    ("P1-B attribution", "06", "Validation/%s/SOURCE.md" % C.PACKAGE,
     ["Mucsányi", "no book text is redistributed", "unverified"]),
]

# (issue, artifact, phrase that must NOT appear) -- pre-revision wording.
ABSENT = [
    ("P0-A AUPR baseline over-generalised",
     "SOP/%s/SOP-08-report-evidence-and-validity-boundaries.md" % C.PACKAGE,
     "random baseline = P(L = 1), so near-useless"),
    ("P0-A perplexity base stated once",
     "SOP/%s/SOP-08-report-evidence-and-validity-boundaries.md" % C.PACKAGE,
     "exponentiated `nll` (base 2)"),
    ("P0-B splits asserted universally",
     "SOP/%s/SOP-02-build-evaluation-splits-under-leakage-discipline.md" % C.PACKAGE,
     "Always split by subject"),
]

# An absolute path in a committed file: a drive-qualified Windows path, or a unix home directory.
# The lookbehind keeps `https://` from reading as a drive letter, and inline code is stripped before
# matching, because that is where this package writes the placeholder paths it tells a reader to
# substitute. A real home directory in running prose is still caught.
LOCAL_PATH = re.compile(
    r"(?:(?:^|(?<=[\s\"'(=]))[A-Za-z]:[\\/][^\s\"'`,)]{2,})|(?:(?:/home|/Users|/root)/[A-Za-z0-9._-]+/)")
INLINE_CODE = re.compile(r"`[^`\n]*`")
BULK_TEXT = re.compile(r"\.txt$")
# This file necessarily contains the patterns above as regex source; scanning it would report itself.
SELF = "Validation/Trustworthy-ML-2023/tools/check_gates.py"


def _text(rel):
    path = os.path.join(C.ROOT, *rel.split("/"))
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _flat(rel):
    """Artifact text with line wrapping and emphasis collapsed.

    A marker must match whether the author italicised part of it (`are **not** out of scope`) or broke
    it across two lines, so `*` and runs of whitespace are removed from both sides of the comparison.
    """
    text = _text(rel)
    return None if text is None else _norm(text)


def _norm(s):
    return re.sub(r"\s+", " ", s.replace("*", "")).strip().lower()


def check_markers():
    missing, found = [], 0
    for issue, plan, rel, phrases in PRESENT:
        text = _flat(rel)
        if text is None:
            missing.append(f"{issue} (plan {plan}): {rel} does not exist")
            continue
        for phrase in phrases:
            if _norm(phrase) in text:
                found += 1
            else:
                missing.append(f"{issue} (plan {plan}): {rel} no longer says {phrase!r}")
    for issue, rel, phrase in ABSENT:
        text = _flat(rel)
        if text is not None and _norm(phrase) in text:
            missing.append(f"{issue}: pre-revision wording back in {rel}: {phrase!r}")
    return missing, found


def _scan_line(line):
    return LOCAL_PATH.search(INLINE_CODE.sub(" ", line))


# Cases the detector must keep getting right. A checker that quietly stops matching is worse than none.
PATH_CASES = [
    (r"read from D:\.Myfile\books\the-book.pdf", True),
    (r"read from C:\Users\someone\the-book.pdf", True),
    (r"read from /home/someone/books/the-book.pdf", True),
    ("see https://example.org/a/b and `pip install pymupdf`", False),
    ("python build_citation_index.py --source /path/to/the-book.pdf", False),
    ("recorded as `D:\\...` in the plan, which is an elision, not a location", False),
]


def selftest():
    bad = []
    for text, want in PATH_CASES:
        got = bool(_scan_line(text))
        if got != want:
            bad.append(f"path detector {'missed' if want else 'matched'}: {text!r}")
    return bad


def check_hygiene():
    """No machine-local paths and no bulk source text among the tracked files."""
    problems = selftest()
    try:
        out = subprocess.run(["git", "-C", C.ROOT, "ls-files"], capture_output=True, text=True,
                             encoding="utf-8", check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        return ["git is unavailable, so tracked-file hygiene was not checked"]
    for rel in out:
        if rel == SELF:
            continue
        if not rel.endswith((".md", ".py", ".json", ".yaml", ".yml", ".txt")):
            continue
        if rel.startswith("plans/"):          # the plans are the reviewer's input, quoted verbatim
            continue
        if BULK_TEXT.search(rel):
            problems.append(f"{rel}: a .txt file is tracked; bulk extracts stay out of Git")
            continue
        text = _text(rel) or ""
        for n, line in enumerate(text.splitlines(), 1):
            if _scan_line(line):
                problems.append(f"{rel}:{n}: machine-local path in a tracked file")
    ignored = _text(".gitignore") or ""
    if "_audit" not in ignored:
        problems.append(".gitignore no longer excludes the local audit working area")
    return problems


def main(argv):
    missing, found = check_markers()
    hygiene = check_hygiene()
    if "--list" in argv:
        for issue, _, rel, phrases in PRESENT:
            print(f"OK  {issue:<38} {rel}  {len(phrases)} markers")
    for m in missing:
        print("GATE MISSING " + m)
    for h in hygiene:
        print("HYGIENE " + h)
    total = len(PRESENT) + len(ABSENT) + len(hygiene)
    print(f"check_gates checked={found + len(ABSENT) + len(hygiene)} "
          f"markers_found={found} issues={total} missing={len(missing)} hygiene={len(hygiene)}")
    return 1 if (missing or hygiene) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
