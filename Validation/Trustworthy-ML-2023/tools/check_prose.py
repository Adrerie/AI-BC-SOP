"""Prose checks: vague placeholder phrases and spelling-variant drift.

Both are mechanical because both are the kind of thing a long revision introduces silently: an
instruction that reads "handle the usual cases" instead of naming them, or the same word spelled two
ways across eight documents.

Spelling is reported, never auto-fixed: the package is American-English, but a spelling that appears
inside a quotation of the source, or inside a registered metric name, is correct and must not be
touched. Each finding therefore carries the file and line so a human can decide.

Runs on committed markdown only; no source PDF needed.
"""
import re
import sys

import _common as C

VAGUE = [
    "it is important to note", "should generally", "in general, one should", "etc.",
    "various methods", "as appropriate", "handle edge cases", "note that it", "sufficiently robust",
    "state of the art", "recent work shows", "obviously", "clearly,", "simply put",
]

# American target form -> British variants seen in this literature.
FORMS = {
    "behavior": ["behaviour"], "color": ["colour"], "favor": ["favour"],
    "labeled": ["labelled"], "labeling": ["labelling"], "modeling": ["modelling"],
    "modeled": ["modelled"], "canceled": ["cancelled"], "optimize": ["optimise"],
    "optimizing": ["optimising"], "optimized": ["optimised"], "optimizes": ["optimises"],
    "optimize": ["optimise"], "generalize": ["generalise"], "generalized": ["generalised"],
    "minimize": ["minimise"], "minimized": ["minimised"], "maximize": ["maximise"],
    "maximized": ["maximised"], "utilize": ["utilise"], "prioritize": ["prioritise"],
    "standardize": ["standardise"], "randomize": ["randomise"], "randomized": ["randomised"],
    "characterize": ["characterise"], "characterized": ["characterised"],
    "quantize": ["quantise"], "quantized": ["quantised"],
    "specialize": ["specialise"], "summarize": ["summarise"], "analyze": ["analyse"],
    "artifact": ["artefact"], "artifacts": ["artefacts"], "fulfill": ["fulfil"],
    "license": ["licence"], "defense": ["defence"], "center": ["centre"],
    "favorite": ["favourite"], "favorable": ["favourable"],
    "labor": ["labour"], "color": ["colour"],
    "toward": ["towards"], "while": ["whilst"],
}

QUOTES = [re.compile(r"“[^”]*”"), re.compile(r'"[^"]*"')]   # a quoted source wording may wrap lines


def _pairs(forms):
    """Flatten `american -> [british...]` into (british, american) search pairs.

    Each listed root also gets its regular inflexions, so `randomise` catches `randomisation` too. The
    dictionary stays the source of truth for which roots are variants at all: deriving from listed stems
    is what keeps `advise`, `supervise`, `noise` and `otherwise` out of the results.
    """
    out = set()
    for american, variants in forms.items():
        for variant in variants:
            out.add((variant, american))
            if variant.endswith("ise") and american.endswith("ize"):
                stem_b, stem_a = variant[:-3], american[:-3]
                out.update((stem_b + s, stem_a + a) for s, a in
                           (("ises", "izes"), ("ised", "ized"), ("ising", "izing"),
                            ("isation", "ization"), ("isations", "izations")))
            elif variant.endswith("yse") and american.endswith("yze"):
                # `-yses` is left out on purpose: "analyses" is also the American plural of "analysis".
                stem = variant[:-3]
                out.update((stem + s, american[:-3] + a) for s, a in
                           (("ysed", "yzed"), ("ysing", "yzing")))
            elif variant.endswith("ce"):
                out.add((variant + "s", american + "s"))
    # longest British form first: `defences` must be tried before `defence`, or it half-matches.
    return sorted(out, key=lambda p: (-len(p[0]), p[0]))


VARIANTS = _pairs(FORMS)


def _quoted_spans(text):
    spans = []
    for rx in QUOTES:
        spans += [(m.start(), m.end()) for m in rx.finditer(text)]
    return spans


def _inside(pos, spans):
    return any(a <= pos < b for a, b in spans)


def _prose_only(text):
    """Keep only flowing prose for the phrase scan.

    Fenced code, headings and table rows are dropped: a table that *names* a phrase it forbids (the
    register's degeneracy column does exactly this) is a mention, not usage.
    """
    out = []
    fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            out.append("")
            continue
        if fence or line.startswith("#") or line.strip().startswith("|"):
            out.append("")
            continue
        out.append(re.sub(r"`[^`\n]*`", " ", line))
    return "\n".join(out)


def check_vague():
    findings = []
    for rel, _ in C.artifacts():
        text = _prose_only(C.read(rel))
        lowered = text.lower()
        for phrase in VAGUE:
            for m in re.finditer(re.escape(phrase), lowered):
                line = text.count("\n", 0, m.start()) + 1
                snippet = text.splitlines()[line - 1].strip()[:100]
                findings.append(f"{rel}:{line} '{phrase}': {snippet}")
    return findings


def check_spelling():
    """Report British-variant spellings outside quotations; capitalization is preserved.

    A prefix is allowed, so `mislabelled` and `unlabelled` are caught as forms of `labelled` and the
    suggested fix keeps the prefix (`mislabeled`, `unlabeled`). A suffix is not: `\b...labelled\b`
    cannot match `labelledly`, and prefix-only avoids inventing matches inside unrelated words.
    """
    findings = []
    for rel, _ in C.artifacts():
        text = C.read(rel)
        spans = _quoted_spans(text)
        seen = set()
        for variant, american in VARIANTS:
            for m in re.finditer(r"\b[A-Za-z]*" + variant + r"\b", text, re.I):
                if _inside(m.start(), spans) or m.start() in seen:
                    continue
                seen.add(m.start())
                word = m.group(0)
                cut = len(word) - len(variant)
                replacement = word[:cut] + (
                    american.capitalize() if word[cut].isupper() else american)
                line = text.count("\n", 0, m.start()) + 1
                findings.append(f"{rel}:{line} '{word}' -> '{replacement}'")
    return findings


def main(argv):
    quiet = "--quiet" in argv
    vague, spell = check_vague(), check_spelling()
    if not quiet:
        for f in vague:
            print("VAGUE " + f)
        for f in spell:
            print("SPELLING " + f)
    print(f"check_prose vague={len(vague)} spelling_variants={len(spell)}")
    return 1 if (vague or spell) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
