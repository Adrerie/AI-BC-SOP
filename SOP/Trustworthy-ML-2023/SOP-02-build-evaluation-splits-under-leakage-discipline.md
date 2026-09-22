# SOP-02 — Build evaluation splits under leakage discipline

**Stage:** freeze the evaluation · **Tier:** Core + Extended · **Concepts:** C4 evaluation-information
discipline, C5 test-set finiteness, C1 (partial)

Terminology shared with the rest of the group is defined in
[`SOP-08`](SOP-08-report-evidence-and-validity-boundaries.md).

## 1. Purpose

Construct training, validation and test material whose *provenance* — who may be looked at, how
often, and for what — is explicit, so that a reported number can be read as the claim it actually
supports. This SOP owns split provenance for the whole group; other SOPs link here instead of
restating it.

## 2. When to use

- Immediately after [`SOP-01`](SOP-01-specify-deployment-setting.md) fixes the setting, before any
  hyper-parameter search.
- When reusing an existing benchmark and needing to know which of its subsets may legitimately be
  called "test".
- When a model, threshold, or checkpoint must be selected and you need to know which data you are
  allowed to select on.
- When auditing someone else's evaluation claim.

## 3. Inputs / prerequisites

- The setting block: generalization type, declared supervision, comparison class.
- The raw corpus with domain / group / attribute labels where they exist (or a documented statement
  that they do not).
- A bookkeeping place for test-set contacts (a dated log; see §9).
- For contamination checks: near-duplicate detection tooling (exact hash plus a fuzzy or embedding
  neighbour search).

## 4. Definitions needed for execution

- **Role of a split by what is optimized on it** — parameters (training), hyper-parameters and
  design choices (validation), methodology and claim (test). Update cadence differs by orders of
  magnitude: milliseconds-to-seconds, minutes-to-days, months-to-years.
- **Information leakage** — any information intended exclusively for deployment becoming available
  during development *under the declared setting*. The source lists four concrete forms: tuning on
  labeled target samples; tuning by *visually inspecting* target samples; training on target samples
  labeled **or unlabeled**; tuning to maximize publicly reported scores. Each is a violation only
  where the setting withholds that information — the second scenario in the source's own list is a
  domain-adaptation method, not a domain-generalization one, and the label is what decides.
- **Test-set spoiling** — the loss of a test set's meaning as a generalization estimate caused by
  any decision being taken from its results, including reading other people's numbers on it.
  Spoiling is a spectrum: you can spoil less, never not at all, if you also want a benchmark.
  Once final-test results have influenced a selection, that set is development evidence *for the
  affected claim*, and running the chosen system over it again does not undo that.
- **Shifted validation** — a validation subset drawn from a *different* domain than training, used
  only when the setting grants target-domain information. It measures something weaker than
  generalization and must be labeled as such.
- **Upper-bound row** — a result obtained with more supervision than the setting grants (for
  example training on the target domain, or selecting the model on the full test set). Legitimate
  only when marked as an upper bound.

## 5. Procedure

**Core**

1. Choose the **split unit** from the dependence structure the claim actually rests on, then assign
   every raw sample to exactly one of train / IID-validation / shifted-validation / final-test at that
   unit level so that no unit straddles two splits.
   - If observations are correlated through subject, site, device, time, household, sequence, plot,
     patient, or source document, the split must be made by the highest relevant independence unit —
     a random row split there leaks, and the leak is invisible in a per-row contamination check.
   - If the samples genuinely are independent and identically distributed for the target claim, a
     random split is valid and provenance grouping is unnecessary ceremony.
   - State which of the two you assumed, and the unit you used. The justification is the claim and the
     data-generating process, not the convention of the subfield.
2. Set the test-set policy in writing: which subsets are final-test, what the contact budget is
   (default: one evaluation per project per final-test subset), and who may open the log.
3. Run the contamination pass before anything is trained: exact-duplicate and near-duplicate
   overlap of test items against training items (including question/answer level overlap for
   language tasks, and identifier/image-hash level overlap for vision). Record the overlap rates.
4. For the declared generalization type, build the evaluation cells:
   - ID → held-out samples from the same distribution;
   - cross-domain → held-out *domains*, with training domains disjoint from them;
   - cross-bias → diagonal training cells plus at least one off-diagonal evaluation cell, with the
     construction recorded (how the correlation was induced or broken);
   - adversarial → the ε-ball / transform family declared by
     [`SOP-05`](SOP-05-run-worst-case-stress-evaluation.md).
5. Choose hyper-parameters, checkpoints, thresholds, and calibration parameters **only** on
   validation material permitted by the setting. If the setting is domain generalization with no
   target-domain access, the validation set must come from the training domains.
6. Log every evaluation contact: date, subset, purpose, decision taken afterwards.
7. Before publishing, re-derive every headline number from the log; any number without a logged
   contact is not reportable.

**Extended** — add for publication-grade or reused benchmarks:

8. Add a *frozen* evaluation copy: hash the final-test files, store the hashes, and verify them at
   each contact; detect silent upstream dataset revisions.
9. Where you own a benchmark, add a refresh policy: rotate or add test domains on a stated cadence,
   and prefer comparing with significance tests over assuming one fixed comparable test set — the
   standard a field can actually satisfy is "the same distribution", not "the same samples".
10. Where score exposure is the leak vector, expose a ranking (or a noised statistic) instead of
    exact scores to submitters.
11. Maintain a shifted-validation twin of the tuning path so you can report how much of the gain
    came from tuning rather than from the method.
12. Record, for every row in the final table, the supervision actually used, so upper-bound rows
    can be marked rather than silently averaged in.

## 6. Mandatory checks

- [ ] **Unit-disjointness**: the unit chosen in step 1 appears in only one split (verify by set
      intersection of unit ids, not by row count). If the declared unit is the individual row, the
      IID assumption that licenses it is stated in the setting block.
- [ ] **Tuning-rights check**: for every tuned object (hyper-parameter, checkpoint, threshold,
      temperature, layer choice) record the split it was selected on; flag any selection made on a
      final-test subset.
- [ ] **Post-selection independence**: for every flagged final-test selection, record which response
      was taken — (i) a new untouched test drawn from the intended evaluation distribution, (ii) a
      pre-existing untouched secondary test, (iii) downgrade the claim and disclose that no
      independent final test remains. Re-running the selected system on the same set is not a
      response and must not be reported as one.
- [ ] **Ablation-under-shift check**: an ablation or model-selection table whose numbers come from the
      held-out target domain is leakage **when the setting withholds that domain**. Where the setting
      grants it, the table is legitimate — but the project is then reported under that setting, and
      compared against methods with the same access, not against the stricter one.
- [ ] **Contact budget**: number of final-test evaluations ≤ declared budget; excess contacts are
      reported, not hidden.
- [ ] **Contamination report**: overlap rates recorded with the detection method used; a claim of
      "no leakage" without a measurement is a claim of "not checked".
- [ ] **Integrity of the frozen copy**: hashes match.
- [ ] **Cross-split supervision parity**: every compared method received the same split access and
      the same tuning budget.

## 7. Decision or stop conditions

- **Re-declare the setting** if target-domain labels or unlabeled target data were used: the project
  is now a domain-adaptation, test-time-training or continual-learning one, and the
  domain-generalization comparison no longer applies. That ends the old comparison, not the work —
  report it under the new setting, against methods granted the same access.
- **Stop the run** if any model-selection step is found to have consumed final-test results. For the
  affected claim that set is now development evidence, so recompute on permitted material, obtain a
  new untouched test, use a pre-existing untouched secondary test, or downgrade the claim and disclose
  that no independent final test remains. Rerunning the selected system over the same set after the
  fact is not one of these and must not be presented as independence restored.
- **Proceed with an explicit caveat** when the field offers no real validation set (the public
  subset that everyone calls "validation" is in fact the de-facto test set): state that your
  validation is the community's test set, and that accumulated overfitting in that field is
  therefore expected.
- **Refuse the comparison** when a contamination rate above your tolerance is found in the
  reference results you are being asked to beat.

## 8. Common methodological failures

- Using the test set as the validation set because "there is no other labeled data".
- Selecting the feature-drop / augmentation / layer strategy by average left-out-domain accuracy —
  an ablation that is individually reasonable and collectively invalid.
- Treating visual inspection of deployment data as harmless because no label was read. The source
  counts it as leakage in a setting that withholds the target domain and as legitimate adaptation in
  one that grants it; what it never is, is setting-neutral.
- Repeatedly evaluating on the same public leaderboard and reading it as independent confirmation.
- Assuming a dataset revision is identical to the version you tuned on.
- Reporting one number that mixes methods with different split access.
- Counting "we looked once" while the internal development log shows a dozen passes.
- Re-running the selected model over a set whose results guided the selection and calling the second
  number independent evidence.

## 9. Required outputs

- A split manifest: the independence unit chosen in step 1 and why, then per split — the units
  assigned, size, labels available, construction rule, and the tuning rights granted.
- A contamination report: method, thresholds, overlap rates, affected ids.
- A test-contact log (date, subset, purpose, resulting decision), and for any subset whose results
  entered a selection, which recovery was taken.
- Frozen-copy hashes (Extended).
- A per-result supervision annotation table for the final report, marking every upper-bound row.

## 10. Minimum reporting requirements

State the split provenance and grouping key; which split each tuned object was selected on; the
number of final-test evaluations performed; the contamination measurement and its result; and
whether the validation material was drawn from training domains or from target domains. Any
comparison against a public benchmark must note whether that benchmark's de-facto test set was also
your validation set.

## 11. Links to relevant Benchmarks

- [`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md) and
  [`BM-02`](../../Benchmark/Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md) — take their cells
  from this SOP's manifest.
- [`BM-03`](../../Benchmark/Trustworthy-ML-2023/BM-03-confidence-truthfulness.md) —
  post-hoc-recalibration parameters must be fitted on the split designated here.
- [`BM-05`](../../Benchmark/Trustworthy-ML-2023/BM-05-adversarial-robustness.md) — attack-time
  thresholds and defense parameters are selected on validation material only, under this manifest.
- [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md) — audits this
  SOP's outputs directly.

## 12. Source traceability

Split roles and what each optimizes: §2.3.2, Definitions 2.20-2.22 (book pp. 26-27). Validation drawn
from the training domains **for a claim that withholds the target domain**, with the pointer to
leakage: §2.3.2 (p. 26) and §2.5.2; the source's own companion statement that a target-domain
validation subset is a different setting rather than a sin: §2.5.1 (pp. 36-37). Testing as part of
development and the impossibility of an unsullied test set: §2.3.3 (p. 28). Information leakage
definition and its four concrete forms: §2.5.1, Definition 2.24 (pp. 36-37). Ranking-instead-of-scores and the differential-privacy/noise idea: §2.5.1 fn. 7
(p. 36), §2.5.3 (p. 40). Ablation study definition and the OOD caveat: §2.5.2, Definition 2.25
(pp. 38-39). "Specify the hyper-parameter selection method as part of the learning problem",
test-set-once-per-project, benchmark refresh with significance tests: §2.5.3 (pp. 39-40).
Contamination in public Q&A benchmarks and models scoring near zero on the non-overlapping subset:
§5.1.3 (pp. 335-338). Missing validation set and the second-version accuracy drop: §5.1.3
(pp. 335-338). Oracle test-time selection as an upper bound: §2.14.1 (p. 82). Pretraining-set access
forcing a "zero-shot" re-think: §2.5.1 (p. 37). Contact logging, hashes, and the check-list format
are repository conventions. Three rules here are **synthesized** and carry that label in
`concept_reconstruction.md`: the split-unit conditionality (a random split is valid when the rows
really are independent and identically distributed for the claim), since the source argues the grouped
case without licensing either choice; the three permitted responses to a contaminated final test and
the statement that rerunning cannot restore independence, which sharpens the spoiling spectrum
(§2.3.3, p. 28; §2.5.3, pp. 39-40); and the four-level pretraining disclosure ladder, which turns the
source's single "zero-shot needs re-thinking" remark (§2.5.1, p. 37) into a reporting rule.
