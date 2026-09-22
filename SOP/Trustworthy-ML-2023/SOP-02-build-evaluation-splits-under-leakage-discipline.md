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

- **Role of a split by what is optimised on it** — parameters (training), hyper-parameters and
  design choices (validation), methodology and claim (test). Update cadence differs by orders of
  magnitude: milliseconds-to-seconds, minutes-to-days, months-to-years.
- **Information leakage** — any information intended exclusively for deployment becoming available
  during development. Four concrete forms: tuning on labelled target samples; tuning by *visually
  inspecting* target samples; training on target samples labelled **or unlabelled**; tuning to
  maximise publicly reported scores.
- **Test-set spoiling** — the loss of a test set's meaning as a generalization estimate caused by
  any decision being taken from its results, including reading other people's numbers on it.
  Spoiling is a spectrum: you can spoil less, never not at all, if you also want a benchmark.
- **Shifted validation** — a validation subset drawn from a *different* domain than training, used
  only when the setting grants target-domain information. It measures something weaker than
  generalization and must be labelled as such.
- **Upper-bound row** — a result obtained with more supervision than the setting grants (for
  example training on the target domain, or selecting the model on the full test set). Legitimate
  only when marked as an upper bound.

## 5. Procedure

**Core**

1. Partition by *provenance group*, not randomly: assign every raw sample to exactly one of
   train / IID-validation / shifted-validation / final-test, grouping by source (device, site,
   subject, time window, annotator) so that no group straddles two splits.
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

- [ ] **Group-disjointness**: no provenance group appears in two splits (verify by set
      intersection of group ids, not by row count).
- [ ] **Tuning-rights check**: for every tuned object (hyper-parameter, checkpoint, threshold,
      temperature, layer choice) record the split it was selected on; flag any selection made on a
      final-test subset.
- [ ] **Ablation-under-shift check**: any ablation or model-selection table whose numbers come from
      the held-out target domain is leakage; if such a table exists, either rebuild it on permitted
      validation material or delete the claim that depends on it.
- [ ] **Contact budget**: number of final-test evaluations ≤ declared budget; excess contacts are
      reported, not hidden.
- [ ] **Contamination report**: overlap rates recorded with the detection method used; a claim of
      "no leakage" without a measurement is a claim of "not checked".
- [ ] **Integrity of the frozen copy**: hashes match.
- [ ] **Cross-split supervision parity**: every compared method received the same split access and
      the same tuning budget.

## 7. Decision or stop conditions

- **Stop and re-declare the setting** if target-domain labels were used at all: you now have domain
  adaptation or test-time adaptation, and domain-generalization comparisons are void.
- **Stop the run** if any model-selection step is found to have consumed final-test results; the
  affected numbers must be recomputed on permitted material or dropped.
- **Proceed with an explicit caveat** when the field offers no real validation set (the public
  subset that everyone calls "validation" is in fact the de-facto test set): state that your
  validation is the community's test set, and that accumulated overfitting in that field is
  therefore expected.
- **Refuse the comparison** when a contamination rate above your tolerance is found in the
  reference results you are being asked to beat.

## 8. Common methodological failures

- Using the test set as the validation set because "there is no other labelled data".
- Selecting the feature-drop / augmentation / layer strategy by average left-out-domain accuracy —
  an ablation that is individually reasonable and collectively invalid.
- Treating visual inspection of deployment data as harmless because no label was read.
- Repeatedly evaluating on the same public leaderboard and reading it as independent confirmation.
- Assuming a dataset revision is identical to the version you tuned on.
- Reporting one number that mixes methods with different split access.
- Counting "we looked once" while the internal development log shows a dozen passes.

## 9. Required outputs

- A split manifest: per split — provenance groups, size, labels available, construction rule, and
  the tuning rights granted.
- A contamination report: method, thresholds, overlap rates, affected ids.
- A test-contact log (date, subset, purpose, resulting decision).
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
- [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md) — audits this
  SOP's outputs directly.

## 12. Source traceability

Split roles and what each optimises: §2.3.2, Definitions 2.20-2.22 (book pp. 26-27). Validation
must share training domains for true OOD claims, with the pointer to leakage: §2.3.2 (p. 26) and
§2.5.2. Testing as part of development and the impossibility of an unsullied test set: §2.3.3
(p. 29). Information leakage definition and its four concrete forms: §2.5.1, Definition 2.24
(pp. 36-37). Ranking-instead-of-scores and the differential-privacy/noise idea: §2.5.1 fn. 7
(p. 36), §2.5.3 (p. 40). Ablation study definition and the OOD caveat: §2.5.2, Definition 2.25
(pp. 38-39). "Specify the hyper-parameter selection method as part of the learning problem",
test-set-once-per-project, benchmark refresh with significance tests: §2.5.3 (pp. 39-40).
Contamination in public Q&A benchmarks and models scoring near zero on the non-overlapping subset:
§5.1.3 (pp. 339-340). Missing validation set and the second-version accuracy drop: §5.1.3
(p. 340). Oracle test-time selection as an upper bound: §2.14.1 (p. 82). Pretraining-set access
forcing a "zero-shot" re-think: §2.5.1 (p. 37). Contact logging, hashes, and the check-list format
are repository conventions.
