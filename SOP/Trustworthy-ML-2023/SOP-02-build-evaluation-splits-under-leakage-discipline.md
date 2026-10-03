# SOP-02 — Build evaluation splits under leakage discipline

**Stage:** freeze the evaluation · **Tier:** Core + Extended · **Concepts:** C4 evaluation-information
discipline, C5 test-set finiteness, C1 (partial)

Terminology shared with the rest of the group is defined in
[`SOP-08`](SOP-08-report-evidence-and-validity-boundaries.md).

## 1. Purpose

Construct training, validation and test material whose *provenance* is explicit. *Provenance* means
who you may look at, how often, and for what. Then you can read a reported number as the claim that
number actually supports. This SOP owns split provenance for the whole group. Other SOPs link here
instead of restating that provenance.

## 2. When to use

- Immediately after [`SOP-01`](SOP-01-specify-deployment-setting.md) fixes the setting, before any
  hyper-parameter search.
- When you reuse an existing benchmark, and you need to know which of its subsets legitimately hold
  the name "test".
- When you must select a model, threshold, or checkpoint, and you need to know which data you may
  select on.
- When you audit someone else's evaluation claim.

## 3. Inputs / prerequisites

- The setting block: generalization type, declared supervision, comparison class.
- The raw corpus with domain / group / attribute labels, where such labels exist. Where such labels
  do not exist, record that fact in a documented statement.
- A bookkeeping place for test-set contacts (a dated log; see §9).
- For contamination checks: near-duplicate detection tooling (exact hash plus a fuzzy or embedding
  neighbour search).

## 4. Definitions needed for execution

- **Role of a split by what is optimized on it** — parameters (training), hyper-parameters and
  design choices (validation), methodology and claim (test). Update cadence differs by orders of
  magnitude: milliseconds-to-seconds, minutes-to-days, months-to-years.
- **Information leakage** — any information intended exclusively for deployment becoming available
  during development *under the declared setting*. The source lists four concrete forms:

  - You tune on labeled target samples.
  - You *visually inspect* target samples, and you tune on what you see.
  - You train on target samples labeled **or unlabeled**.
  - You tune to maximize publicly reported scores.

  Each form is a violation only where the setting withholds that information. The second scenario
  in the source's own list is a domain-adaptation method, not a domain-generalization one. The
  label is what decides.
- **Test-set spoiling** — the loss of a test set's meaning as a generalization estimate. Any
  decision taken from the test results causes that loss. Reading other people's numbers on the set
  also counts. Spoiling is a spectrum: you can spoil less, and never not at all, if you also want a
  benchmark. Once final-test results influence a selection, that set is development evidence *for
  the affected claim*. Running the chosen system over that set again does not undo the influence.
- **Shifted validation** — a validation subset drawn from a *different* domain than training. Use
  shifted validation only when the setting grants target-domain information. Shifted validation
  measures something weaker than generalization, and the report must label the subset that way.
- **Upper-bound row** — a result obtained with more supervision than the setting grants (for
  example training on the target domain, or selecting the model on the full test set). Legitimate
  only when marked as an upper bound.

## 5. Procedure

**Core**

1. Choose the **split unit** from the dependence structure the claim actually rests on. Assign
   every raw sample to exactly one split, at that unit level. The four splits are train,
   IID-validation, shifted-validation and final-test. No unit may straddle two splits.
   - The correlation may run through subject, site, device, time, household, sequence, plot,
     patient, or source document. Where such a correlation exists, split by the highest relevant
     independence unit. A random row split leaks there, and the leak is invisible in a per-row
     contamination check.
   - If the samples genuinely are independent and identically distributed for the target claim, a
     random split is valid. Provenance grouping is then unnecessary ceremony.
   - State which of the two you assumed, and the unit you used. The justification is the claim and
     the data-generating process, not the convention of the subfield.
2. Set the test-set policy in writing. The policy states:

   - which subsets are final-test
   - the contact budget (default: one evaluation per project per final-test subset)
   - who may open the log

3. Run the contamination pass before anything is trained. Measure the exact-duplicate and
   near-duplicate overlap of test items against training items. For language tasks the pass covers
   question/answer level overlap. For vision the pass covers identifier/image-hash level overlap.
   Record the overlap rates.
4. For the declared generalization type, build the evaluation cells:
   - ID → held-out samples from the same distribution.
   - cross-domain → held-out *domains*, with the training domains disjoint from the held-out
     domains.
   - cross-bias → diagonal training cells plus at least one off-diagonal evaluation cell, with the
     construction recorded (how the correlation was induced or broken).
   - adversarial → the ε-ball / transform family declared by
     [`SOP-05`](SOP-05-run-worst-case-stress-evaluation.md).
5. Choose hyper-parameters, checkpoints, thresholds, and calibration parameters **only** on
   validation material permitted by the setting. If the setting is domain generalization with no
   target-domain access, the validation set must come from the training domains.
6. Log every evaluation contact: date, subset, purpose, decision taken afterwards.
7. Before publication, re-derive every headline number from the log. Any number without a logged
   contact is not reportable.

**Extended** — add for publication-grade or reused benchmarks:

8. Add a *frozen* evaluation copy. Hash the final-test files, and store the hashes. Verify the
   hashes at each contact. That check detects silent upstream dataset revisions.
9. Where you own a benchmark, add a refresh policy. Rotate or add test domains on a stated cadence.
   Prefer comparison with significance tests over the assumption of one fixed comparable test set.
   The standard a field can actually satisfy is "the same distribution", not "the same samples".
10. Where score exposure is the leak vector, expose a ranking (or a noised statistic) instead of
    exact scores to submitters.
11. Maintain a shifted-validation twin of the tuning path. Then you can report how much of the gain
    came from tuning rather than from the method.
12. Record the supervision actually used for every row in the final table. Then the report marks
    upper-bound rows as such, instead of averaging the rows in silently.

## 6. Mandatory checks

- [ ] **Unit-disjointness**: the unit chosen in step 1 appears in only one split (verify by set
      intersection of unit ids, not by row count). If the declared unit is the individual row, the
      IID assumption that licenses it is stated in the setting block.
- [ ] **Tuning-rights check**: for every tuned object (hyper-parameter, checkpoint, threshold,
      temperature, layer choice) record the split used for that selection. Flag any selection made
      on a final-test subset.
- [ ] **Post-selection independence**: for every flagged final-test selection, record which
      response was taken:

   - (i) a new untouched test drawn from the intended evaluation distribution
   - (ii) a pre-existing untouched secondary test
   - (iii) downgrade the claim, and disclose that no independent final test remains

   Re-running the selected system on the same set is not a response. Do not present such a rerun
   as a response.
- [ ] **Ablation-under-shift check**: an ablation or model-selection table can take its numbers from
      the held-out target domain. That table is leakage **when the setting withholds that domain**.
      Where the setting grants that access, the table is legitimate. The project is then reported
      under that setting, and compared against methods with the same access, not against the
      stricter setting.
- [ ] **Contact budget**: the number of final-test evaluations ≤ the declared budget. Report every
      excess contact, and hide nothing.
- [ ] **Contamination report**: the record holds the overlap rates and the detection method used. A
      claim of "no leakage" without a measurement is a claim of "not checked".
- [ ] **Integrity of the frozen copy**: hashes match.
- [ ] **Cross-split supervision parity**: every compared method received the same split access and
      the same tuning budget.

## 7. Decision or stop conditions

- **Re-declare the setting** if the project used target-domain labels or unlabeled target data. The
  project is then a domain-adaptation, test-time-training or continual-learning one, and the
  domain-generalization comparison no longer applies. That ends the old comparison, not the work.
  Report the work under the new setting, against methods granted the same access.
- **Stop the run** if you find that any model-selection step consumed final-test results. For the
  affected claim, that set is now development evidence. Take one of the permitted responses instead:
  - recompute on permitted material
  - obtain a new untouched test
  - use a pre-existing untouched secondary test
  - downgrade the claim, and disclose that no independent final test remains

  A rerun of the selected system over the same set after the fact is not one of these responses.
  Such a rerun does not restore independence. Do not present such a rerun as independence
  restored.
- **Proceed with an explicit caveat** when the field offers no real validation set (the public
  subset that everyone calls "validation" is in fact the de-facto test set): state that your
  validation is the community's test set, and that accumulated overfitting in that field is
  therefore expected.
- **Refuse the comparison** when a contamination rate above your tolerance appears in the reference
  results someone asks you to beat.

## 8. Common methodological failures

- You use the test set as the validation set because "there is no other labeled data".
- You select the feature-drop / augmentation / layer strategy by average left-out-domain accuracy.
  That ablation is individually reasonable and collectively invalid.
- You treat visual inspection of deployment data as harmless because no label was read. The source
  counts visual inspection as leakage where the setting withholds the target domain. The source
  counts visual inspection as legitimate adaptation where the setting grants that domain. Visual
  inspection is never independent of the setting.
- You evaluate repeatedly on the same public leaderboard, and you treat that repetition as
  independent confirmation.
- You assume that a dataset revision is identical to the version you tuned on.
- You report one number that mixes methods with different split access.
- You count "we looked once" while the internal development log shows a dozen passes.
- You re-run the selected model over a set whose results guided the selection. You then call the
  second number independent evidence.

## 9. Required outputs

- A split manifest. The manifest names the independence unit chosen in step 1, and the reason for
  that unit. For each split the manifest gives the units assigned, the size, the labels available,
  the construction rule, and the tuning rights granted.
- A contamination report: method, thresholds, overlap rates, affected ids.
- A test-contact log (date, subset, purpose, resulting decision), and for any subset whose results
  entered a selection, which recovery was taken.
- Frozen-copy hashes (Extended).
- An annotation table of per-result supervision for the final report, marking every upper-bound row.

## 10. Minimum reporting requirements

State the split provenance and the grouping key. State which split you selected each tuned object
on. State the number of final-test evaluations performed. State the contamination measurement and
its result. State whether the validation material came from training domains or from target
domains. Any comparison against a public benchmark must note whether that benchmark's de-facto test
set was also your validation set.

## 11. Links to relevant Benchmarks

- [`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md) and
  [`BM-02`](../../Benchmark/Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md) — take their cells
  from this SOP's manifest.
- [`BM-03`](../../Benchmark/Trustworthy-ML-2023/BM-03-confidence-truthfulness.md) — fit the
  post-hoc-recalibration parameters on the split designated here.
- [`BM-05`](../../Benchmark/Trustworthy-ML-2023/BM-05-adversarial-robustness.md) — attack-time
  thresholds and defense parameters are selected on validation material only, under this manifest.
- [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md) — audits this
  SOP's outputs directly.
- [`BM-09`](../../Benchmark/Trustworthy-ML-2023/BM-09-disclosure-of-training-data-and-context.md) —
  build the member/non-member control sets under this SOP's disjointness rules. Build the
  shadow-model splits under the same rules. A control set chosen after you see the scores is not a
  control.

## 12. Source traceability

- Split roles and what each optimizes: §2.3.2, Definitions 2.20-2.22 (book pp. 26-27).
- Validation drawn from the training domains **for a claim that withholds the target domain**, with
  the pointer to leakage: §2.3.2 (p. 26) and §2.5.2.
- The source's own companion statement that a target-domain validation subset is a different setting
  rather than a sin: §2.5.1 (pp. 36-37).
- Testing as part of development, and the impossibility of an unsullied test set: §2.3.3 (p. 28).
- Information leakage definition and its four concrete forms: §2.5.1, Definition 2.24
  (pp. 36-37).
- The differential-privacy/noise idea, and ranking instead of scores: §2.5.1 fn. 7 (p. 36),
  §2.5.3 (p. 40).
- Ablation study definition and the OOD caveat: §2.5.2, Definition 2.25 (pp. 38-39).
- "Specify the hyper-parameter selection method as part of the learning problem",
  test-set-once-per-project, benchmark refresh with significance tests: §2.5.3 (pp. 39-40).
- Contamination in public Q&A benchmarks, and models scoring near zero on the non-overlapping
  subset: §5.1.3 (pp. 335-338).
- Missing validation set and the second-version accuracy drop: §5.1.3 (pp. 335-338).
- Oracle test-time selection as an upper bound: §2.14.1 (p. 82).
- Pretraining-set access forcing a "zero-shot" re-think: §2.5.1 (p. 37).
- Contact logging, hashes, and the check-list format are repository conventions.

Three rules here are **synthesized** and carry that label in `concept_reconstruction.md`:

- The split-unit conditionality: a random split is valid when the rows really are independent and
  identically distributed for the claim. The source argues the grouped case without licensing
  either choice.
- The three permitted responses to a contaminated final test, and the statement that rerunning
  cannot restore independence. That statement sharpens the spoiling spectrum (§2.3.3, p. 28;
  §2.5.3, pp. 39-40).
- The pretraining exposure disclosure rule. The rule turns the source's single "zero-shot needs
  re-thinking" remark (§2.5.1, p. 37) into a reporting rule. Name the corpus, and report
  semantic/class exposure, duplicate exposure and benchmark-specific adaptation separately, rather
  than collapsing those exposures into one contamination label.
