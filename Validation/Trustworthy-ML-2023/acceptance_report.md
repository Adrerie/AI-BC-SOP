# Acceptance Report — Trustworthy ML (2023) package

Plan 5 artifact. Records PASS / FAIL for every gate in
`plans/Trustworthy-ML-2023/05_VALIDATION_AND_ACCEPTANCE.md`, plus the stage gates A–D.

*(Completion summary required by Plan 6 §4 is prepended at finalization.)*

Verification was performed by mechanical checks over the committed files plus targeted re-reading of
the source PDF; the scripts that produced the numbers are listed in §V and the two
checks-that-could-fail-silently (links, metric naming) are re-runnable.

## Verification method

| Check | How it was executed | Result |
|---|---|---|
| Heading universe | Font-metadata extraction over all 375 PDF pages, cross-checked against the printed table of contents; numbering contiguity test per section | 247 headings; 49/49 sections match the TOC; no numbering gaps |
| Markdown links | Walked every `*.md` outside the local working area, resolved each relative target on disk | 0 broken links in the final package |
| Schema conformance | Tested each `SOP-*.md` for all 12 required sections and each `BM-*.md` for all 13 | 8/8 and 8/8 conform |
| Metric terminology | Extracted the metric register keys from SOP-08 §4 and scanned every artifact for snake_case names not in the register or in an allow-list of output-field names | 22 registered names; 0 unregistered uses |
| Cross-link symmetry | Parsed SOP §11 and BM §12 link sets; flagged one-directional links | 0 asymmetric links |
| Duplication | Shared 9-word verbatim n-grams between artifact pairs, ignoring links and inline code | max pair overlap 9 grams (was 57 before consolidation) |
| Claim grounding | Normalized full-text index of the source PDF; 56 distinctive needles taken from artifact claims, each resolved to its printed page and containing section | 56/56 found verbatim in the source after one needle was replaced by the book's own wording (see Gate 7) |
| Page-citation integrity | Re-derived all 237 numbered headings straight from the PDF (standalone number line + title line) and diffed against the heading map: 0 drift, printed page = PDF page − 2 confirmed on sampled folios. Then bound every `p.`/`pp.` anchor in the artifacts to the section/definition/caption named in the same citation clause and checked it falls inside that locator's real page span | 393 anchors bound; 132 drifted anchors repaired; 0 remaining |
| Non-mirroring | Lexical overlap between each artifact filename and the set of all 247 source headings | max Jaccard 0.01, mean 0.00; no filename equals a chapter or section title |

---

## Gate A — Source coverage (Plan 1)

**PASS.** See [`source_coverage.md`](source_coverage.md): 247 headings with disposition
(132 `incorporate`, 104 `supporting`, 2 `redundant`, 9 `out-of-scope`, **0** `needs-body-reading`),
231 of them with body reading (89 in the main pass, 142 in bounded sub-passes), source record with
file type, edition, completeness and heading machine-readability, plus a fidelity-flags list of six
source inconsistencies recorded rather than repaired. Drafting of SOP/Benchmark artifacts began only
after this gate.

## Gate B — Reconstruction (Plan 2)

**PASS.** See [`concept_reconstruction.md`](concept_reconstruction.md): 20 synthesized concepts with
contributing sections, dependencies and destination; eight separated classification axes; the
resulting 8-SOP / 8-Benchmark taxonomy; and a rule-provenance table labelling 29 rules as
source-derived, synthesized, or repository convention.

## Gate C — SOP quality (Plan 3)

| Condition | Result | Evidence |
|---|---|---|
| Covers the main reusable workflows identified in reconstruction | PASS | Concepts C1–C18 map onto SOP-01 … SOP-08 with no unmapped operational concept; C19/C20 are declared background/catalogue |
| Executable without reading the source book | PASS | Every SOP carries its own §4 definitions, numbered procedure steps, output list and reporting minimum; source anchors live only in §12 (8–13 % of document length) |
| Checks and failure conditions, not only steps | PASS | 6–8 explicit check items per SOP in §6, plus §7 stop conditions and §8 failure lists in all 8 |
| Links to evaluation mechanisms in the Benchmark group | PASS | Each SOP §11 lists 3–8 benchmarks; symmetric back-links in every BM §12 |
| Traceability present but not dominant | PASS | Traceability share per SOP: 8 %, 10 %, 11 %, 13 %, 12 %, 13 %, 12 %, 13 % |

## Gate D — Benchmark quality (Plan 4)

| Condition | Result | Evidence |
|---|---|---|
| Each benchmark has a clearly defined target capability | PASS | §1 of each BM names capability *and* failure mode; the eight targets are distinct (shift, cue dependence, confidence, detection, adversarial, explanation, selection, protocol integrity) |
| Metrics tied to explicit questions | PASS | §2 states the hypothesis set (H-probability/H-calibration/H-ranking in BM-03; H-sound/H-order/H-goal in BM-06; H-error/H-ood/H-multiplicity in BM-04), and §6 metrics are chosen per hypothesis |
| Leakage and test-set tuning prevented | PASS | Every BM §3 designates selection material and forbids final-test selection; the once-per-project rule and the ablation caveat sit in SOP-02, audited by BM-08 |
| Components can compare methods fairly | PASS | §5 baseline tables include the trivial control, the tuned simple baseline, equal-budget requirements, and upper-bound rows marked as such |
| Each major component links back to the SOP group | PASS | 3–7 SOP back-links per benchmark, no asymmetry |

## Acceptance Gate 1 — Structural completeness

**PASS.** Present and non-empty: `SOP/Trustworthy-ML-2023/README.md` + 8 SOP documents;
`Benchmark/Trustworthy-ML-2023/README.md` + 8 benchmark documents;
`Validation/Trustworthy-ML-2023/source_coverage.md`, `concept_reconstruction.md`, and this report.
Package size ≈ 40 000 words. No group is index-only.

## Acceptance Gate 2 — Source coverage accounting

**PASS.** All 247 headings are dispositioned in the coverage table; every `incorporate` row is
reachable from at least one artifact's §12/§13 anchors, `supporting` rows are named as background in
the reconstruction, `out-of-scope` and `redundant` rows carry a stated reason (navigation, index,
historical narrative, author research agenda, deployment-supervision settings, showcase, or
restatement). Zero silent omissions: the residual set is enumerated in the coverage file's
disposition summary and summarised in both group READMEs' scope notes.

## Acceptance Gate 3 — Non-mirroring / reconstruction

**PASS.** Artifact names share essentially no vocabulary with source headings (max Jaccard 0.01,
mean 0.00; no exact title match). The artifact axis is workflow-stage × capability, while the source
axis is four research areas; chapter 4 alone contributes to six concepts and appears in five
artifacts, and the eight benchmarks draw from four different chapters each. Three artifacts
(SOP-02, SOP-08, BM-08) have no chapter counterpart at all.

## Acceptance Gate 4 — SOP operationality

**PASS.** Each SOP: purpose and applicability (§1–§2), explicit inputs (§3), numbered executable
steps with Core/Extended tiers (§5), mandatory checks as a checkbox list (§6), stop conditions (§7),
outputs (§9), reporting minimum (§10), failure modes (§8). None reads as a chapter summary: the
dominant register is imperative ("write", "compute", "stop and re-declare"), and the explanatory
material is confined to definitions and traceability.

## Acceptance Gate 5 — Benchmark validity

**PASS.** Each benchmark states its target, its hypotheses (§2), split assumptions (§3), how stress
is constructed (§4), required baselines with their role (§5), primary and diagnostic metrics tied to
the hypotheses (§6–§7), aggregation and variability rules (§8), a failure-interpretation table (§9),
computational reporting (§10) and validity limits (§11). No artifact is a metric list: metrics always
appear with the question they answer and the condition under which they mislead.

## Acceptance Gate 6 — Cross-link consistency

**PASS.** Terminology is single-sourced: the metric register in SOP-08 §4 defines 22 names used
across the package, and 0 unregistered metric names are used. Bidirectional matrix (● mutual,
· not applicable):

|  | BM-01 | BM-02 | BM-03 | BM-04 | BM-05 | BM-06 | BM-07 | BM-08 |
|---|---|---|---|---|---|---|---|---|
| **SOP-01** | ● | ● | · | · | ● | · | ● | ● |
| **SOP-02** | ● | ● | ● | · | ● | · | · | ● |
| **SOP-03** | ● | ● | · | · | · | ● | · | ● |
| **SOP-04** | · | · | ● | ● | · | · | ● | ● |
| **SOP-05** | ● | · | · | ● | ● | · | · | ● |
| **SOP-06** | ● | ● | ● | ● | · | · | ● | ● |
| **SOP-07** | · | ● | · | ● | · | ● | · | ● |
| **SOP-08** | ● | ● | ● | ● | ● | ● | ● | ● |

Minimum per row and per column is 3 links; there is no one-directional pair.

## Acceptance Gate 7 — Evidence discipline

**PASS.** Sampled eight load-bearing claims, checked (a) that the provenance label is honest and
(b) that the wording exists in the source body text at the cited section and printed page:

| # | Claim as used in the package | Label | Source check |
|---|---|---|---|
| 1 | "We can only spoil the test set less, but we can never not spoil it." | source-derived | exact wording found, §2.3.3, p. 28 |
| 2 | Use the test set once per project / "once per paper". | source-derived | exact wording, §2.5.3, p. 39 |
| 3 | A constant confidence equal to global accuracy reaches ECE = 0 without truthfulness. | source-derived | exact wording, §4.6.2, p. 256 |
| 4 | AUROC is recommended over AUPR on unbalanced data; random AUPR equals `P(L = 1)`. | source-derived | both phrasings, §4.9.2, pp. 265-266 |
| 5 | "The model being safe is not equivalent to no gradient-based algorithm being able to find an attack." | source-derived | exact, §2.15.12, p. 103 |
| 6 | Fairly tuned ERM is "not worse at all" than complicated DG methods. | source-derived | exact, §5.2.2, p. 340 |
| 7 | Ranking the four remove-and-classify variants can disagree; the metric is not perfect but is the most popular. | source-derived | §3.7.7-§3.7.8, pp. 188 |
| 8 | Order: declare setting → freeze splits → diagnose → measure → stress → mitigate → report. | **synthesized** | not a book statement; built from §2.3-§2.5, §2.11-§2.14 and §5.1-§5.3, labelled as such in the reconstruction |
| 9 | Core/Extended tiering, checkbox registers, artifact IDs, and the SOP-08 metric register naming. | **repository convention** | explicitly excluded from book attribution in every §12/§13 |
| 10 | Default ε values, iteration budgets, bin counts, or numeric "good" thresholds. | **deliberately absent** | the source supplies none; each artifact instead requires the practitioner to state and record the choice |

Wider sweep: 56 distinctive needles extracted from artifact statements were located in the source
full text with section resolution — all 56 match the book's wording. An earlier pass recorded one
"wording variance" for a claim attributed to the aleatoric-loss recommendation in §4.13.5; on
re-inspection the needle itself had been written as a paraphrase rather than a quotation, and the
claim belongs to SOP-04 step 10, not SOP-06. The needle was replaced by the book's own phrase
(`supported by the theory of proper scoring rules`, p. 302) and the three mislabelled artifact tags
were re-pointed at the files that actually carry the claims. No book-attributed claim in the package
failed the check, and no invented metric or formula was found: every formula in the register traces
to a cited definition number (Definitions 4.8-4.15 for scoring and calibration, 2.24-2.33 for the
shift vocabulary, 3.1-3.16 for explanations).

### Gate 7 revision cycle — page anchors

Gate 7 initially looked weaker than the wording check implied. Re-deriving the heading pages from the
PDF independently (standalone number line plus matching-size title line, over all 375 pages) agreed
with the working heading map on 237/237 numbered headings, so the section labels were sound — but
binding each printed-page anchor to the locator in its own citation clause exposed **132 anchors**
whose pages had drifted by 1-6 pages away from the section they named. The cause was transcription:
those pages had been copied from body-reading notes rather than from the heading map, and the notes
counted pages from the extract dumps.

Repair policy, applied mechanically to digits only (no prose was rewritten):

| Situation | Action |
|---|---|
| Cited pages inside the locator's real span | Left untouched, including pinpoint single-page cites |
| Cited pages outside the span | Replaced by the span of the locator(s) in the same clause, `p.`/`pp.` adjusted |
| Several locators in one clause (`§2.2.1-§2.2.2, Definitions 2.9-2.11`) | Union of their spans |
| Page bound to a table or figure caption (`Table 2.8 (p. 103)`) | Checked against a caption map built from the PDF; a mixed list (`§2.15.3-§2.15.4 and Table 2.8 (pp. 90-92, 103)`) is validated part by part |
| Page bound to a phrase instead of a locator (5 anchors) | Resolved by locating the phrase in the full text: `p. 46` (Definition 2.28), `p. 49`, `p. 50` (Kolmogorov-complexity formula), `p. 107` (expectation-over-transformation identity), `p. 181` (chicken-and-egg) — all correct; one `p. 264` was wrong and is now `p. 263` |

After the repair: 393 page anchors bound to a section, definition or caption, **0 outside the span
those locators occupy**. The artifact text is unchanged apart from the page numbers themselves.

## Acceptance Gate 8 — Practicality

**PASS.** Two generic scenarios walked through the package as a researcher would.

**Scenario 1 — image classifier retrained yearly for a retail shelf task, new stores and camera
models.** What to define before training: SOP-01 setting block, generalization type = cross-domain,
cue whitelist marking camera/site cues as forbidden, ρ and label inventory. Splits/stress: SOP-02
group-disjoint split by store and camera, contamination pass, BM-01 leave-one-store/one-camera-out
plus a severity ladder. What to measure: `acc_avg` and `acc_worstgroup` per held-out store
(BM-01 §6), plus confidence battery per domain (BM-03). Misleading confidence detection: constant
confidence control, bin sensitivity, `mce` on the small-bin pitfall (SOP-04 §6, BM-03 §9).
Abstain/flag: BM-07 risk-coverage at the review capacity, fallback = re-photograph request.
To report: SOP-08 §10 list with cost line (yearly retraining labour is part of the result).
Remaining limits: unforeseen store formats, within-store drift, cue dependence only where
off-diagonal cells exist.

**Scenario 2 — clinical triage model where a false reassurance is far worse than a deferral.**
Define: SOP-01 with the cost table owned by the clinical stakeholder, asymmetric cost explicit,
deployment axes (site, device, population). Splits: SOP-02 with final-test contact budget and
per-subgroup support; BM-01 subpopulation cells. Measure: BM-03 with per-class `ece`/`mce` and
worst-subgroup risk; BM-04 H-error for the "does the score notice" question. Misleading confidence:
the gaming check and the probabilistic-overfitting check are mandatory before any assurance claim
(SOP-04 §6). Abstain: BM-07 operating point chosen on risk-coverage at the tolerated risk with the
escalation cost; SOP-06 stops at abstention when no admissible mitigation exists. Report: SOP-08,
including the "does not show" list. Limits: calibration is distribution-bound, so a threshold transfer
across sites is invalid; explanation-based assurance additionally needs BM-06's human-grounded track,
which the source explicitly demands rather than assumes.

In both scenarios the researcher can answer all seven questions the gate lists, and neither forces an
application-specific SOP — the scenario findings stay in this report.

## Acceptance Gate 9 — Minimal duplication

**PASS.** Shared definitions are single-sourced: recurring terms and all metric names live in SOP-08
§4, and other artifacts reference rather than restate them. Dependencies are linked, not copied
(SOP-04 links the split rules to SOP-02; BM-03 links the calibration recipe to SOP-04). Duplication
probe: the three heaviest SOP↔benchmark overlaps (57, 26 and 19 shared 9-grams) were consolidated by
making the benchmark traceability sections cite the executing SOP's anchor list and keep only
measurement-specific anchors; the remaining maximum is 9 shared 9-grams between a SOP and its own
benchmark counterpart, which is definitional restatement required to keep each document executable
standalone (Gate C). Cross-benchmark overlap is 3 grams. Book chapters that repeat a concept are
merged once (for example ECE appears in SOP-04 and BM-03 only as a name resolving to SOP-08 §4).

---

## Remaining issues and known limitations

1. **Numeric defaults are intentionally absent.** The source provides none for ε, PGD iterations, ECE
   bins, or "acceptable" calibration; the package requires them to be declared and recorded instead.
2. **`ρ` direction.** The source uses the symbol inconsistently (Table 2.5 caption versus its own
   numbers); every artifact that uses ρ states the direction. This is a documented fidelity flag, not
   a resolved ambiguity.
3. **Catalogue clusters were read in bounded sub-passes** (attribution method catalogue, uncertainty
   estimator families, DG benchmark survey) rather than line-by-line in the main pass; their use in
   the artifacts is limited to baseline menus, cost statements and assumption lists, each with
   section and page anchors.
4. **Certified robustness scope.** BM-05's certification branch is conditioned on the source's own
   limitation (binary, shallow networks); the artifact keeps it as an Extended track and forbids
   guarantee language without a certificate.
5. **Second-version replication** (a documented anti-overfitting device) is only executable where a
   field re-collects evaluation data; where it cannot be run, BM-01 and BM-08 record it as
   inapplicable rather than passed.
6. **The package inherits the book's CV-centric examples.** Procedures and metrics are written
   application-neutral, but the illustrative constructions (segmentation masks, caption noise,
   corner-case objectness scores) come from that area; a text or tabular deployment must substitute
   its own edit and partition operators.
7. **Page anchors are printed pages of this edition.** They refer to the folio numbers of the 2023
   PDF recorded in `source_coverage.md` Step 1 (printed page = PDF page − 2). A different printing or
   reflowed format shifts them; the section numbers stay valid.

## §V — Reproduction of the checks

The mechanical checks are a link/schema/terminology walker, a source-needle verifier, a cross-link
and duplication analyser, and a page-citation binder. They are not committed: the verifier reads the
copyrighted PDF and the extracted text lives only in the local working area, so a future maintainer
needs the source file at the path recorded in `source_coverage.md` Step 1 to re-run it. Committed
artifacts carry the citations instead.

The citation binder is the part worth re-running after any edit, because it is the only check that
can catch a page number that contradicts its own section label. It needs three derived inputs, all
reproducible from the PDF: the heading map (number → printed page, with each section's span ending
where the next non-child heading begins), the definition map (`Definition N.M` box locations), and
the caption map (`Table N.M:` / `Figure N.M:` first pages). A heading is a standalone number line
whose following title line shares its font size; recovering headings by font metadata is necessary
because this PDF has no outline. The binder then takes the locator group in the same citation clause
as each `p.`/`pp.` anchor — including trailing locators after the closing bracket, and excluding
`Table`/`Figure` labels — and requires the cited pages to lie inside the union of those spans.

## Final acceptance result

**All nine acceptance gates and the four stage gates (A–D) PASS.** No known FAIL item remains open.
