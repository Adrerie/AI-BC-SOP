"""Revision gate coverage: are the corrected principles still in force, everywhere?

Two kinds of check run here, and they fail for opposite reasons:

*Presence* checks (`PRESENT`) assert that a correction Revision 01 or 02 made is still worded where it
was put. A presence check goes red when someone rewrites a rule away.

*Regression* checks (`REGRESSIONS`) assert that a wording which was found to be wrong does not come
back. A regression check goes red when someone restores a bad sentence -- which is the failure mode
that actually matters, because the bad wording is usually fluent, plausible and easy to reintroduce.
Revision 02 added these after the sweep found files whose text had contradicted a principle that had
already been corrected elsewhere in the same package.

Every regression pattern is paired with a positive example that must fire and a real example of the
package's own corrected phrasing that must not; that self-test runs on every invocation, so a pattern
that has quietly stopped matching anything fails the gate rather than passing it. The patterns are
negation-aware: "not as an OOD family" is the corrected position, not a violation.

Scope, stated because a scanner that over-claims its own reach is a defect (Revision 02 principle 7):
regression and invariant checks cover the **normative package files** listed by `normative_files()`.
`plans/` (reviewer input, kept verbatim) and `acceptance_report.md` (whose job includes quoting
superseded wording) are excluded from the negative scans and are swept by hand each cycle instead.
The hygiene scan covers tracked non-plan files.

    python check_gates.py            # summary
    python check_gates.py --list     # also print every marker and pattern that was checked

Runs on committed files only; no source PDF needed.
"""
import os
import re
import subprocess
import sys

import _common as C

PACKAGE = C.PACKAGE

# ---------------------------------------------------------------- presence (Revision 01 / 02 edits)
# (issue, plan, artifact, [phrases that must appear])
PRESENT = [
    ("P0-A metric definitions", "01", "SOP/%s/SOP-04-measure-confidence-truthfulness.md" % PACKAGE,
     ["The two bases must match", "prevalence of *its own* positive", "deployable", "oracle"]),
    ("P0-A metric register", "01", "SOP/%s/SOP-08-report-evidence-and-validity-boundaries.md" % PACKAGE,
     ["no-skill reference is the prevalence of the designated positive", "positive class", "oracle quantity"]),
    ("P0-A AUPR in the suite", "01", "Benchmark/%s/BM-04-error-and-anomaly-detection.md" % PACKAGE,
     ["prevalence of the task's declared positive"]),
    ("P0-B information rights", "02", "SOP/%s/SOP-01-specify-deployment-setting.md" % PACKAGE,
     ["Information rights", "Claim-level typing", "Pretraining disclosure", "Re-declare"]),
    ("P0-B split by unit", "02", "SOP/%s/SOP-02-build-evaluation-splits-under-leakage-discipline.md" % PACKAGE,
     ["highest relevant independence unit", "Post-selection independence", "Unit-disjointness"]),
    ("P0-B adaptation is in scope", "02", "Benchmark/%s/README.md" % PACKAGE,
     ["not out of scope", "changes the setting and therefore the comparison class"]),
    ("P0-C contamination is auditable", "02", "Benchmark/%s/BM-08-evaluation-integrity-audit.md" % PACKAGE,
     ["declared independence unit", "contamination measurements"]),
    ("P0-C post-selection independence", "02", "SOP/%s/SOP-02-build-evaluation-splits-under-leakage-discipline.md" % PACKAGE,
     ["Post-selection independence"]),
    ("P0-D edit is sensitivity", "03", "SOP/%s/SOP-03-diagnose-learned-evidence.md" % PACKAGE,
     ["sensitivity to the edit", "identification"]),
    ("P0-D cue-dependence reading", "03", "Benchmark/%s/BM-02-spurious-cue-dependence.md" % PACKAGE,
     ["identification argument", "sensitivity to the edited factor"]),
    ("P0-D explanation contracts", "03", "SOP/%s/SOP-07-evaluate-explanation-methods.md" % PACKAGE,
     ["model-dependence sanity", "attribution ordering", "end-goal usefulness", "Contract boundary"]),
    ("P0-E mitigation admissibility", "03", "SOP/%s/SOP-06-choose-mitigation-or-abstain.md" % PACKAGE,
     ["admissible", "Pareto", "no validated action policy"]),
    ("P0-E abstention validity", "03", "Benchmark/%s/BM-07-selective-prediction-under-cost.md" % PACKAGE,
     ["the operating point is a modeling artifact", "risk-coverage result as evidence of calibration"]),
    ("P0-F certification scope", "04", "SOP/%s/SOP-05-run-worst-case-stress-evaluation.md" % PACKAGE,
     ["Attack adequacy argued, not counted", "field limit", "the *chosen* certificate"]),
    ("P0-F attack adequacy in the suite", "04", "Benchmark/%s/BM-05-adversarial-robustness.md" % PACKAGE,
     ["adaptive", "the only row that may support an existential claim"]),
    ("P1-A staging architecture", "06", "README.md",
     ["provenance-bearing staging unit", "supersede", "merge"]),
    ("P1-B attribution", "06", "Validation/%s/SOURCE.md" % PACKAGE,
     ["Mucsányi", "trustworthyml.io", "2310.08215", "CC BY 4.0", "does not redistribute"]),
    ("R2 worst-case ordering", "r2", "SOP/%s/SOP-05-run-worst-case-stress-evaluation.md" % PACKAGE,
     ["certified robust accuracy ≤ exact finite-sample robust accuracy ≤ empirical attacked accuracy under attack suite A", "never compare a certificate"]),
    ("R2 benchmark ordering", "r2", "Benchmark/%s/BM-05-adversarial-robustness.md" % PACKAGE,
     ["certified robust accuracy ≤ exact finite-sample robust accuracy ≤ empirical attacked accuracy under attack suite A", "never an upper-bound row"]),
    ("R2 zero-shot by benchmark definition", "r2", "SOP/%s/SOP-01-specify-deployment-setting.md" % PACKAGE,
     ["does not impose a universal zero-shot definition", "Information-rights compliance"]),

    # Official-course update cycle (plans/Trustworthy-ML-Official-Updates). Each phrase below is the
    # load-bearing half of an accepted delta: drop the sentence and the rule it carries disappears.
    ("U-17 test-batch right declared separately", "u1",
     "SOP/%s/SOP-01-specify-deployment-setting.md" % PACKAGE,
     ["Test-batch right", "one-hot answer"]),
    ("U-09 interaction claims reported by position", "u1",
     "SOP/%s/SOP-04-measure-confidence-truthfulness.md" % PACKAGE,
     ["Stop and re-report by position"]),
    ("U-02 robustness results dated", "u1",
     "SOP/%s/SOP-05-run-worst-case-stress-evaluation.md" % PACKAGE,
     ["Dating nothing"]),
    ("U-02/U-03 BM-05 carries the discrete-append and channel rows", "u1",
     "Benchmark/%s/BM-05-adversarial-robustness.md" % PACKAGE,
     ["Discrete-append stress", "Channel stress", "suffix length"]),
    ("U-05 BM-04 carries the sensitivity target", "u1",
     "Benchmark/%s/BM-04-error-and-anomaly-detection.md" % PACKAGE,
     ["H-sensitivity", "prevalence of sensitive items"]),
    ("U-08 BM-03 carries the separability probe", "u1",
     "Benchmark/%s/BM-03-confidence-truthfulness.md" % PACKAGE,
     ["Separability probe", "one quantity reported twice"]),
    ("U-16 BM-06 splits one-time from per-case cost", "u1",
     "Benchmark/%s/BM-06-explanation-quality.md" % PACKAGE,
     ["what is paid once and what is paid per case"]),
    ("U-14 BM-08 gives the reproduction outcome vocabulary", "u1",
     "Benchmark/%s/BM-08-evaluation-integrity-audit.md" % PACKAGE,
     ["inapplicable, which is neither replication nor failure", "regime-specific"]),
    ("U-10 BM-09 states its provenance in both directions", "u1",
     "Benchmark/%s/BM-09-disclosure-of-training-data-and-context.md" % PACKAGE,
     ["official-course-derived", "repository conventions"]),
]

# Wording that was only ever true of a superseded position, kept as package-wide regression patterns
# rather than file-pinned absences: a bad sentence re-introduced in *some other* document is still a
# regression. The examples below are the actual pre-revision wording and its replacement.
ABSENT_PATTERNS = [
    ("P0-A AUPR baseline stated for one positive class",
     r"(random baseline = p\(l = 1\)|random aupr = p\(l = 1\)(?! for)|aupr.{0,40}near-useless)",
     "random baseline = P(L = 1), so near-useless at extreme rates",
     "no-skill reference is the prevalence of the designated positive; values are not comparable "
     "across different positive-class definitions without relabeling"),
    ("P0-A perplexity base asserted without the log-base condition",
     r"exponentiated ?`?nll`? ?\(base 2\)",
     "| `perplexity` | exponentiated `nll` (base 2) | language modeling | same confound as `nll` |",
     "perplexity only for language modeling, where it is the exponentiated NLL — `exp(nll)` when "
     "the loss used natural logarithms"),
    ("P0-B split rule asserted unconditionally",
     r"\balways split by (?:subject|group|entity)\b",
     "Always split by subject; a random split is never acceptable.",
     "split by the highest relevant independence unit, and where the claim is IID, a random split is"),
]

# --------------------------------------------------------------------------- regression patterns
# Pattern names refer to the fixed principles in plans/Trustworthy-ML-2023/revision-02/00_MASTER.md.
# Each entry: (principle, regex, must-fire example, must-not-fire example).
#
# Matched against the flattened text (fenced code removed, emphasis markers removed, whitespace
# collapsed, lowercased), so the patterns are written in lower case. A match is ignored when a negation
# or a history marker sits in the same *clause* -- the run of text since the last sentence end, table
# cell or heading. A fixed-width window was tried and rejected: it let a real violation pass because
# some earlier sentence happened to contain "not".
SUPPRESS = re.compile(r"\b(not|never|without|neither|no longer|dropped|removed|replaced|"
                      r"superseded|corrected|revised)\b")
# Where a clause ends in already-flattened text: sentence punctuation, a table cell, or a heading.
CLAUSE_BOUNDARY = re.compile(r"(?:[.;:!?]\s|\|\s|#{2,3}\s)")

REGRESSIONS = [
    ("1 source license treated as unknown",
     r"(all[- ]rights[- ]reserved|licen[cs]e (?:is |remains |was |recorded as )?"
     r"(?:unknown|unverified|unclear|undetermined|unresolved)|no official (?:source|publisher|website)"
     r"|treat the work as all rights|licensing (?:status|position) is (?:unknown|undocumented)"
     r"|does not assert a url)",
     "Treat the work as all rights reserved by its authors until an official notice says otherwise.",
     "That is a property of that PDF copy, not evidence that the work is unlicensed or "
     "all-rights-reserved."),

    ("2 information rights stated as universal",
     r"(nothing from the deployment stream|no deployment (?:data|information|labels?|images?) "
     r"(?:may|must|can|never)|target(?:-domain)? (?:data|labels?|information) are always "
     r"(?:leakage|a violation|forbidden)|adaptation (?:is|remains) out of scope)",
     "Nothing from the deployment stream (labels, images, logs, scores) may enter development.",
     "Target-domain access is legitimate when the setting grants it; undeclared access is the "
     "integrity failure."),

    ("3 zero-shot imposed as a repository-wide definition",
     r"(zero[- ]shot (?:may be used only|is only permitted|is invalid|may not be claimed)"
     r"|semantic exposure (?:during pretraining )?(?:is|counts as) (?:contamination|a violation)"
     r"|only for level \(i\))",
     '"Zero-shot" may be used only for level (i); semantic exposure during pretraining is '
     'contamination.',
     "Whether the resulting experiment is called \"zero-shot\" follows the explicit definition of "
     "the benchmark or study setting being used."),

    ("4 adversarial inputs treated as an OOD family",
     r"(adversar\w+.{0,60}an OOD family|extreme OOD family|adversar\w+.{0,40}family of OOD"
     r"|robustness to adversarial.{0,40}(?:evidence for|implies).{0,20}OOD)",
     "The inputs produced by BM-05 as an extreme OOD family -- report whether the detector fires.",
     "Treat this as a separate stress axis, not as an OOD family and not as evidence of "
     "OOD-detection capability."),

    ("5 empirical attack described as a bound or proof",
     r"((?:attacked|empirical)[^.]{0,60}?(?:proves|is a proof|guarantees|establishes the worst case"
     r"|bounds the worst case|is a certified)|(?:the|this|a) attack (?:proves|guarantees|bounds))",
     "The attacked accuracy proves the worst case inside the ball.",
     "An empirical attack only probes this quantity and may miss stronger failures."),

    ("6 certification defined only as an LP/SDP relaxation",
     r"(certification (?:is|means|refers to) (?:only |the )?(?:lp|sdp|a relaxation)"
     r"|certified (?:robustness|evaluation|defen\w+) (?:is|means) (?:the )?lp"
     r"|certificates? (?:are|is) (?:only|always) relaxation[- ]based)",
     "Certification is the LP/SDP relaxation chain; anything else is not certification.",
     "The source illustrates one relaxation-based route through first-order, LP, and SDP bounds; "
     "that is an example of certification, not the definition of the field."),

    ("7 certified row classified as an upper bound",
     r"(certif\w+[^.]{0,80}?upper[- ]bound|upper[- ]bound[^.]{0,80}?certif\w+)",
     "Mark every upper-bound row (oracle selection, train-on-target, post-hoc certificate) as such.",
     "A certified robust accuracy is not an upper-bound row: under a valid certificate it is a "
     "provable lower bound on the true robust accuracy."),

    ("8 validation claim exceeding checker scope",
     r"(all tracked files (?:in the repository|were scanned)|whole[- ]repository coverage"
     r"|every file including plans)",
     "The hygiene scan covers all tracked files in the repository, including plans.",
     "The hygiene scan covers tracked non-plan files; plans/ is excluded and stated here."),

    # Official-course cycle. These three wordings are the failures the update layer is most likely to
    # introduce: a post-2023 rule acquiring a book citation, a comparison being read as a truth, and a
    # fourth detection target being folded back into the three it was separated from.
    ("9 post-2023 disclosure material acquiring a book citation",
     r"((?:the )?book[^.]{0,60}?(?:membership inference|data disclosure|contextual norm|privacy session)"
     r"|(?:membership inference|disclosure_gap)[^.]{0,50}?(?:the book|§\d))",
     "The book's privacy session already covered membership inference as an attack.",
     "Nothing in this file is book-derived, and no book section or page is cited here for that reason."),

    ("10 attribution agreement reported as correctness",
     r"(agreement (?:between|across)[^.]{0,60}?(?:proves|establishes|confirms|is ground truth"
     r"|shows the truth)|attribution agreement (?:proves|establishes|is correct))",
     "Agreement between the two attribution families proves the explanation is correct.",
     "Methods disagree on the same model -> instrument uncertainty"),

    ("11 sensitivity target pooled into another detection target",
     r"(h[- ]sensitivity[^.]{0,60}?(?:pooled? with|the same as|counts as (?:h[- ]ood|h[- ]error))"
     r"|(?:pooled|merged) with (?:h[- ]ood|h[- ]error|h[- ]multiplicity))",
     "H-sensitivity can be pooled with H-ood into one detection figure.",
     "so this row may not be pooled with the three above"),
] + ABSENT_PATTERNS

# ------------------------------------------------------------------------ semantic invariants (R2)
# (what must hold, artifact, [phrases]) -- local consistency of the corrected record, not truth.
INVARIANTS = [
    ("SOURCE.md carries the attribution triple", "Validation/%s/SOURCE.md" % PACKAGE,
     ["trustworthyml.io", "2310.08215", "CC BY 4.0", "indicate"]),
    ("SOP-01 compliance is worded as rights, not prohibition",
     "SOP/%s/SOP-01-specify-deployment-setting.md" % PACKAGE,
     ["beyond the rights granted by the declared setting", "undeclared access is the integrity failure"]),
    ("BM-04 keeps adversarial stress off the OOD axis",
     "Benchmark/%s/BM-04-error-and-anomaly-detection.md" % PACKAGE,
     ["separate stress axis", "not as evidence of ood-detection capability"]),
    ("SOP-05 states all three robustness layers",
     "SOP/%s/SOP-05-run-worst-case-stress-evaluation.md" % PACKAGE,
     ["the target quantity is", "empirical attack evaluation", "certified evaluation"]),
    ("BM-05 states all three robustness layers",
     "Benchmark/%s/BM-05-adversarial-robustness.md" % PACKAGE,
     ["target is a worst-case quantity", "empirical claim", "certified claim"]),
    ("Benchmark README rule 8 excludes certificates from upper-bound rows",
     "Benchmark/%s/README.md" % PACKAGE,
     ["is not an upper-bound row", "provable lower bound"]),
    ("BM-09 names the course session it comes from",
     "Benchmark/%s/BM-09-disclosure-of-training-data-and-context.md" % PACKAGE,
     ["Privacy & Data Protection", "Spring 2026"]),
    ("SOP-08 register carries the disclosure-gap row",
     "SOP/%s/SOP-08-report-evidence-and-validity-boundaries.md" % PACKAGE,
     ["disclosure_gap", "both channels can be silent"]),
    ("Benchmark README separates book-derived components from the update layer",
     "Benchmark/%s/README.md" % PACKAGE,
     ["BM-09 does not", "book section and page"]),
]

# --------------------------------------------------------------------------------- repo hygiene
# An absolute path in a committed file: a drive-qualified Windows path, or a unix home directory.
# The lookbehind keeps `https://` from reading as a drive letter, and inline code is stripped before
# matching, because that is where this package writes the placeholder paths it tells a reader to
# substitute. A real home directory in running prose is still caught.
LOCAL_PATH = re.compile(
    r"(?:(?:^|(?<=[\s\"'(=]))[A-Za-z]:[\\/][^\s\"'`,)]{2,})|(?:(?:/home|/Users|/root)/[A-Za-z0-9._-]+/)")
INLINE_CODE = re.compile(r"`[^`\n]*`")
FENCE = re.compile(r"```.*?```", re.S)
BULK_TEXT = re.compile(r"\.txt$")
HERE = os.path.dirname(os.path.abspath(__file__))
SELF = os.path.relpath(os.path.abspath(__file__), C.ROOT).replace("\\", "/")
# Excluded from the negative (regression) scans, deliberately and on stated grounds:
#  - plans/ is reviewer input, kept verbatim, and quotes the wrong wordings by design;
#  - acceptance_report.md records superseded wording as history, so it is swept by hand each cycle.
NEGATIVE_EXCLUDE = ("plans/", "Validation/%s/acceptance_report.md" % PACKAGE)


def _text(rel):
    path = os.path.join(C.ROOT, *rel.split("/"))
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _norm(s):
    return re.sub(r"\s+", " ", s.replace("*", "")).strip().lower()


def _flat(rel):
    """Artifact text with fenced code removed, emphasis collapsed and line wrapping joined.

    Fenced blocks are dropped because they are commands and sample scripts, not normative claims --
    SOURCE.md's own license scanner contains the words it is looking for, for instance. Markers match
    across hard returns and across `*` emphasis for the same reason: the check is about the sentence.
    """
    text = _text(rel)
    if text is None:
        return None
    return _norm(FENCE.sub("", text))


def normative_files():
    """Every normative package document, as repository-relative paths."""
    out = ["README.md"]
    for rel, kind in C.artifacts():
        if kind in ("sop", "bm", "val", "readme") and not rel.endswith("acceptance_report.md"):
            out.append(rel)
    if "Validation/%s/SOURCE.md" % PACKAGE not in out:
        out.append("Validation/%s/SOURCE.md" % PACKAGE)
    for extra in ("Validation/%s/tools/README.md" % PACKAGE,):
        if extra not in out:
            out.append(extra)
    return sorted(set(out))


# --------------------------------------------------------------------------------------- checks
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
    return missing, found


def _negated(text, start, end=None):
    """True when a denial or history marker sits in the same clause as the match.

    The corrected sentences are usually denials of the bad claim -- "a certified accuracy is not an
    upper-bound row", "not as an OOD family" -- so a negator has to be honoured. It is honoured only
    inside the current clause, though: an earlier window that crossed sentence boundaries suppressed
    genuine violations merely because the preceding sentence happened to contain the word "not".
    """
    clause_start = 0
    for m in CLAUSE_BOUNDARY.finditer(text[:start]):
        clause_start = m.end()
    window = text[clause_start:(end or start)][-240:]
    return bool(SUPPRESS.search(window)) or bool(SUPPRESS.search(text[start:(end or start)]))


def _hits(rx, flat_text):
    """Non-suppressed matches of a regression pattern in already-flattened text."""
    return [m for m in re.finditer(rx, flat_text, re.I) if not _negated(flat_text, m.start(), m.end())]


def scan_regressions():
    """Report every normative file that still contains wording against a fixed principle."""
    hits = []
    for rel in normative_files():
        if rel.startswith(NEGATIVE_EXCLUDE) or rel == SELF:
            continue
        text = _flat(rel)
        if text is None:
            continue
        for principle, rx, _, _ in REGRESSIONS:
            for m in _hits(rx, text):
                hits.append(f"{principle}: {rel} says {text[max(0, m.start()-40):m.end()+60]!r}")
    return hits


def check_invariants():
    missing = []
    for what, rel, phrases in INVARIANTS:
        text = _flat(rel)
        if text is None:
            missing.append(f"{what}: {rel} does not exist")
            continue
        for phrase in phrases:
            if _norm(phrase) not in text:
                missing.append(f"{what}: {rel} is missing {phrase!r}")
    return missing


def selftest():
    """Each regression pattern must fire on its bad example and stay quiet on the corrected one.

    Without this, a pattern that stopped matching anything would look like a clean sweep.
    """
    bad = []
    for principle, rx, must_fire, must_not in REGRESSIONS:
        if not _hits(rx, _norm(must_fire)):
            bad.append(f"{principle}: no longer matches its own bad example")
        if _hits(rx, _norm(must_not)):
            bad.append(f"{principle}: fires on the corrected wording {must_not[:56]!r}")
    for text, want in PATH_CASES:
        if bool(_scan_line(text)) != want:
            bad.append(f"path detector {'missed' if want else 'matched'}: {text!r}")
    return bad


# Cases the path detector must keep getting right.
PATH_CASES = [
    (r"read from D:\.Myfile\books\the-book.pdf", True),
    (r"read from C:\Users\someone\the-book.pdf", True),
    (r"read from /home/someone/books/the-book.pdf", True),
    ("see https://example.org/a/b and `pip install pymupdf`", False),
    ("python build_citation_index.py --source /path/to/the-book.pdf", False),
    ("recorded as `D:\\...` in the plan, which is an elision, not a location", False),
]


def _scan_line(line):
    return LOCAL_PATH.search(INLINE_CODE.sub(" ", line))


def check_hygiene():
    """No machine-local paths and no bulk source text among tracked non-plan files."""
    problems = []
    try:
        out = subprocess.run(["git", "-C", C.ROOT, "ls-files"], capture_output=True, text=True,
                             encoding="utf-8", errors="replace", check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError, AttributeError):
        return ["git is unavailable, so tracked-file hygiene was not checked"], 0
    scanned = 0
    for rel in out:
        if rel == SELF:
            continue
        if not rel.endswith((".md", ".py", ".json", ".yaml", ".yml", ".txt")):
            continue
        if rel.startswith("plans/"):          # reviewer input, quoted verbatim; see module docstring
            continue
        scanned += 1
        if BULK_TEXT.search(rel):
            problems.append(f"{rel}: a .txt file is tracked; bulk extracts stay out of Git")
            continue
        for n, line in enumerate((_text(rel) or "").splitlines(), 1):
            if _scan_line(line):
                problems.append(f"{rel}:{n}: machine-local path in a tracked file")
    if "_audit" not in (_text(".gitignore") or ""):
        problems.append(".gitignore no longer excludes the local audit working area")
    return problems, scanned


def main(argv):
    missing, found = check_markers()
    regress = selftest() + scan_regressions()
    invar = check_invariants()
    hygiene, scanned = check_hygiene()
    files = [r for r in normative_files() if not r.startswith(NEGATIVE_EXCLUDE)]
    if "--list" in argv:
        for issue, _, rel, phrases in PRESENT:
            print(f"OK  marker      {issue:<38} {rel}  {len(phrases)} phrases")
        for principle, _, _, _ in REGRESSIONS:
            print(f"OK  regression  {principle}")
        for what, rel, phrases in INVARIANTS:
            print(f"OK  invariant   {what:<38} {rel}  {len(phrases)} phrases")
    for m in missing:
        print("GATE MISSING " + m)
    for r in regress:
        print("REGRESSION " + r)
    for v in invar:
        print("INVARIANT " + v)
    for h in hygiene:
        print("HYGIENE " + h)
    print(f"check_gates markers_found={found} markers_total={len(PRESENT)} "
          f"regression_patterns={len(REGRESSIONS)} regressions={len(regress)} "
          f"invariants={len(INVARIANTS)} invariant_misses={len(invar)} "
          f"normative_files={len(files)} hygiene_scanned={scanned} (tracked non-plan files; "
          f"plans/ and acceptance_report.md excluded from the negative scans, stated per design) "
          f"hygiene_misses={len(hygiene)}")
    return 1 if (missing or regress or invar or hygiene) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
