"""Representative end-to-end gate and metric-contract mutations, in an isolated worktree.

A regression list is only as good as the assumption that its patterns still match something. This
script injects representative known-bad wordings, softens selected invariants, rewrites a presence
marker and drops a machine-local path into an otherwise clean checkout, then requires the checker that
owns that rule -- `check_gates.py`, or `check_metrics.py` for the AUPR contract cases -- to fail for
the right reason each time. It is not one worktree mutation per marker or invariant; `check_gates.py`
separately self-tests every regression regex against positive and negative examples. It then checks
that undoing the damage returns the suite to green, so a
pattern that fires on everything also fails here.

Nothing in the working repository is touched: the mutations run in a detached `git worktree` in the
system temp directory, which is created and removed by this script.

    python mutation_test.py          # run every case
    python mutation_test.py --list   # list cases without running them

Exit status is 0 only when every case is caught.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

import check_gates as G                                    # noqa: E402

BACKSLASH = chr(92)
MINUS = chr(8722)          # the register writes the error-orientation score with a typographic minus

# (case name, file to mutate, text to replace, replacement, which detector must fire
#  [, checker to run [, replace every occurrence]])
#
# The trailing two fields are optional and type-selected: a string names a checker other than
# `check_gates.py`, a truthy value asks for all occurrences of the anchor to be replaced.
CASES = [
    ("presence marker rewritten away",
     "SOP/%s/SOP-04-measure-confidence-truthfulness.md" % G.PACKAGE,
     "The two bases must match", "Keep the bases broadly consistent", "GATE MISSING"),
    ("attribution reference removed",
     "Validation/%s/SOURCE.md" % G.PACKAGE,
     "2310.08215", "the arXiv record", "GATE MISSING", True),
    ("invariant softened (rule 8)",
     "Benchmark/%s/README.md" % G.PACKAGE,
     "is not an upper-bound row", "should be read with care", "INVARIANT"),
    ("information rights made universal again",
     "SOP/%s/SOP-01-specify-deployment-setting.md" % G.PACKAGE,
     "## 8. Common methodological failures",
     "As a rule, nothing from the deployment stream may enter development.\n\n"
     "## 8. Common methodological failures", "REGRESSION"),
    ("adversarial stress renamed an OOD family",
     "Benchmark/%s/BM-04-error-and-anomaly-detection.md" % G.PACKAGE,
     "## 5. Required baselines",
     "The BM-05 inputs form an extreme OOD family.\n\n## 5. Required baselines", "REGRESSION"),
    ("certificate reclassified as an upper bound",
     "Benchmark/%s/BM-05-adversarial-robustness.md" % G.PACKAGE,
     "## 6. Primary metrics",
     "Mark every upper-bound row (oracle selection, train-on-target, post-hoc certificate) as such."
     "\n\n## 6. Primary metrics", "REGRESSION"),
    ("empirical attack re-described as a proof",
     "SOP/%s/SOP-05-run-worst-case-stress-evaluation.md" % G.PACKAGE,
     "## 6. Mandatory checks",
     "The attacked accuracy proves the worst case inside the ball.\n\n## 6. Mandatory checks",
     "REGRESSION"),
    ("license re-declared unknown",
     "Validation/%s/SOURCE.md" % G.PACKAGE,
     "## License",
     "Until the publisher is confirmed, treat the work as all rights reserved by its authors."
     "\n\n## License", "REGRESSION"),
    ("AUPR baseline sentence restored",
     "SOP/%s/SOP-08-report-evidence-and-validity-boundaries.md" % G.PACKAGE,
     "## 5. Procedure",
     "The random baseline = P(L = 1), so near-useless at extreme rates.\n\n## 5. Procedure",
     "REGRESSION"),
    ("machine-local path added to prose",
     "README.md",
     "## License",
     "## License\n\nMy copy of the book sits at C:" + BACKSLASH + "Users" + BACKSLASH
     + "someone" + BACKSLASH + "books" + BACKSLASH + "tml.pdf", "HYGIENE"),
    # The three AUPR contract cases go to `check_metrics.py`, whose guard reads the register rows
    # themselves rather than the prose around them.
    ("generic aupr redefined as trapezoidal PR-AUC",
     "SOP/%s/SOP-08-report-evidence-and-validity-boundaries.md" % G.PACKAGE,
     "**non-interpolated Average Precision (AP)** for a declared binary task",
     "**trapezoidal integration of the precision-recall polyline** for a declared binary task",
     "AUPR CONTRACT", "check_metrics.py"),
    ("aupr_success scored by the error-oriented score",
     "SOP/%s/SOP-08-report-evidence-and-validity-boundaries.md" % G.PACKAGE,
     "positive = success (`L = 1`), score = confidence `c`",
     "positive = success (`L = 1`), score = `1 " + MINUS + " c`",
     "AUPR CONTRACT", "check_metrics.py"),
    ("aupr_error scored by confidence",
     "SOP/%s/SOP-08-report-evidence-and-validity-boundaries.md" % G.PACKAGE,
     "score = `1 " + MINUS + " c` or an explicitly equivalent score increasing with error likelihood",
     "score = confidence `c`",
     "AUPR CONTRACT", "check_metrics.py"),

    # Official-course cycle: the three new regression patterns, and the register row that keeps BM-09's
    # own metric name legal.
    ("post-2023 disclosure rule given a book citation",
     "Benchmark/%s/BM-09-disclosure-of-training-data-and-context.md" % G.PACKAGE,
     "## 13. Source traceability",
     "The book's privacy session already covered membership inference.\n\n## 13. Source traceability",
     "REGRESSION"),
    ("sensitivity target pooled back into the OOD target",
     "Benchmark/%s/BM-04-error-and-anomaly-detection.md" % G.PACKAGE,
     "## 5. Required baselines",
     "H-sensitivity can be pooled with H-ood into one detection figure.\n\n## 5. Required baselines",
     "REGRESSION"),
    ("attribution agreement written as correctness",
     "Benchmark/%s/BM-06-explanation-quality.md" % G.PACKAGE,
     "## 6. Primary metrics",
     "Agreement between the two attribution families proves the explanation is correct.\n\n"
     "## 6. Primary metrics",
     "REGRESSION"),
    ("disclosure_gap removed from the register",
     "SOP/%s/SOP-08-report-evidence-and-validity-boundaries.md" % G.PACKAGE,
     "| `disclosure_gap` | disclosure-event rate",
     "| gap | disclosure-event rate",
     "UNREGISTERED", "check_metrics.py"),
]


def _case(case):
    """Expand a case tuple to (name, rel, old, new, expect, checker, replace_all)."""
    name, rel, old, new, expect = case[:5]
    checker, replace_all = "check_gates.py", False
    for extra in case[5:]:
        if isinstance(extra, str):
            checker = extra
        else:
            replace_all = bool(extra)
    return name, rel, old, new, expect, checker, replace_all


def _run(checker, worktree):
    script = os.path.join(worktree, "Validation", G.PACKAGE, "tools", checker)
    # The finding lines quote the package's own typography, so decoding must not be allowed to fail:
    # an undecodable byte would empty `out` and this script would report a *silent* detector instead
    # of the fired one. `errors="replace"` degrades a stray byte to a placeholder and keeps the line.
    proc = subprocess.run([sys.executable, script], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=worktree)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main(argv):
    if "--list" in argv:
        for name, _, _, _, expect, checker, _ in (_case(c) for c in CASES):
            print(f"{expect:<14} {checker:<16} {name}")
        return 0
    if not shutil.which("git"):
        print("mutation_test: git is unavailable, so an isolated worktree could not be created")
        return 1

    worktree = tempfile.mkdtemp(prefix="tml-mut-")
    os.rmdir(worktree)
    # git echoes the worktree path, which on this repository is not ASCII; decoding that with the
    # console's code page and reading it as UTF-8 is what made a child look silent.
    added = subprocess.run(["git", "-C", ROOT, "worktree", "add", "--detach", "--quiet", worktree,
                            "HEAD"], capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
    if added.returncode != 0:
        print("mutation_test: could not create a worktree:", added.stderr.strip()[:200])
        return 1
    try:
        # the checker under test is the working copy, not whatever HEAD happens to contain
        dst = os.path.join(worktree, "Validation", G.PACKAGE, "tools")
        for name in os.listdir(HERE):
            if name.endswith((".py", ".md", ".json")):
                shutil.copy(os.path.join(HERE, name), os.path.join(dst, name))

        baseline = [(c, _run(c, worktree)) for c in ("check_gates.py", "check_metrics.py")]
        dirty = [(c, res) for c, res in baseline if res[0] != 0]
        if dirty:
            print("mutation_test: the tree is not clean before testing, so results are meaningless")
            print(dirty[0][1][1].strip()[:400])
            return 1

        failures = 0
        for raw in CASES:
            name, rel, old, new, expect, checker, replace_all = _case(raw)
            path = os.path.join(worktree, *rel.split("/"))
            with open(path, encoding="utf-8") as fh:
                before = fh.read()
            if old not in before:
                print(f"SKIP  {name}: anchor text absent from {rel}")
                failures += 1
                continue
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(before.replace(old, new) if replace_all else before.replace(old, new, 1))
            rc, out = _run(checker, worktree)
            line = next((l for l in out.splitlines() if l.startswith(expect)), None)
            caught = rc != 0 and line is not None
            others = [l.split()[0] for l in out.splitlines()
                      if l.startswith(("GATE", "REGRESSION", "INVARIANT", "HYGIENE",
                                       "AUPR", "PARSER", "UNREGISTERED", "REGISTER"))]
            print(("PASS  " if caught else "FAIL  ") + name.ljust(49)
                  + (f"{expect} fired ({checker})" if caught
                     else f"expected {expect} from {checker}, saw {others or 'silence'}"))
            failures += 0 if caught else 1
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(before)

        rc_gates = _run("check_gates.py", worktree)[0]
        rc_metrics = _run("check_metrics.py", worktree)[0]
        print("restored clean:", rc_gates == 0 and rc_metrics == 0)
        failures += 0 if (rc_gates == 0 and rc_metrics == 0) else 1
        print(f"mutation_test cases={len(CASES)} failures={failures}")
        return 1 if failures else 0
    finally:
        subprocess.run(["git", "-C", ROOT, "worktree", "remove", "--force", worktree],
                       capture_output=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
