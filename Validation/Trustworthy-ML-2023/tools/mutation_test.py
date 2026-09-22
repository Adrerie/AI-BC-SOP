"""Gate C2-2 as an executable: break each rule on purpose and prove a checker notices.

A regression list is only as good as the assumption that its patterns still match something. This
script restores known-bad wordings, softens known invariants, rewrites a presence marker and drops a
machine-local path into an otherwise clean checkout, and requires `check_gates.py` to fail for the
right reason each time. It then checks that undoing the damage returns the suite to green, so a
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

# (case name, file to mutate, text to replace, replacement, which detector must fire [, replace all])
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
]


def _run_gates(worktree):
    script = os.path.join(worktree, "Validation", G.PACKAGE, "tools", "check_gates.py")
    # The finding lines quote the package's own typography, so decoding must not be allowed to fail:
    # an undecodable byte would empty `out` and this script would report a *silent* detector instead
    # of the fired one. `errors="replace"` degrades a stray byte to a placeholder and keeps the line.
    proc = subprocess.run([sys.executable, script], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=worktree)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main(argv):
    if "--list" in argv:
        for name, _, _, _, expect in CASES:
            print(f"{expect:<12} {name}")
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

        rc, out = _run_gates(worktree)
        if rc != 0:
            print("mutation_test: the tree is not clean before testing, so results are meaningless")
            print(out.strip()[:400])
            return 1

        failures = 0
        for case in CASES:
            name, rel, old, new, expect = case[:5]
            count = case[5] if len(case) > 5 else 1
            path = os.path.join(worktree, *rel.split("/"))
            with open(path, encoding="utf-8") as fh:
                before = fh.read()
            if old not in before:
                print(f"SKIP  {name}: anchor text absent from {rel}")
                failures += 1
                continue
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(before.replace(old, new) if count else before.replace(old, new, 1))
            rc, out = _run_gates(worktree)
            line = next((l for l in out.splitlines() if l.startswith(expect)), None)
            caught = rc != 0 and line is not None
            others = [l.split()[0] for l in out.splitlines()
                      if l.startswith(("GATE", "REGRESSION", "INVARIANT", "HYGIENE"))]
            print(("PASS  " if caught else "FAIL  ") + name.ljust(42)
                  + (f"{expect} fired" if caught else f"expected {expect}, saw {others or 'silence'}"))
            failures += 0 if caught else 1
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(before)

        rc, out = _run_gates(worktree)
        print("restored clean:" , rc == 0)
        failures += 0 if rc == 0 else 1
        print(f"mutation_test cases={len(CASES)} failures={failures}")
        return 1 if failures else 0
    finally:
        subprocess.run(["git", "-C", ROOT, "worktree", "remove", "--force", worktree],
                       capture_output=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
