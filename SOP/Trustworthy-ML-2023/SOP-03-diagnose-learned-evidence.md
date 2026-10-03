# SOP-03 — Diagnose which evidence the model actually uses

**Stage:** diagnose · **Tier:** Core + Extended · **Concepts:** C6 misspecification diagnosis,
C3 cue whitelist, C15 subgroup view, C17 (partial)

## 1. Purpose

Establish whether the model's predictions rest on the cues that the whitelist in
[`SOP-01`](SOP-01-specify-deployment-setting.md) allowed. Use measurement here, not a look at
pictures. A model can reach high in-distribution accuracy while answering a different question than
the one you asked. This SOP is how you find that out before deployment does.

## 2. When to use

- After the first reasonable training run, before tuning anything further.
- Whenever the setting's generalization type is cross-bias, or any forbidden cue is plausibly
  predictive in the training data.
- When an OOD drop occurs, and you must attribute that drop to a cue rather than to "the shift".
- When you use an explanation method as evidence about the model (then also run
  [`SOP-07`](SOP-07-evaluate-explanation-methods.md)).

## 3. Inputs / prerequisites

- A trained model plus its validation predictions and per-sample losses.
- The cue whitelist (factors of variation with allowed/tolerated/forbidden status).
- **Per-cue labels on evaluation data** — attribute or group labels, or a way to construct the
  labels (segmentation masks, editing tooling, controlled resynthesis).
- A disentangled (off-diagonal) evaluation subset, from
  [`SOP-02`](SOP-02-build-evaluation-splits-under-leakage-discipline.md) §5 step 4.
- A budget for intervention: cue-editing or re-synthesis of test samples.

## 4. Definitions needed for execution

- **Spurious correlation** — co-occurrence of cues, features or labels that holds during
  development and not during deployment.
- **Underspecification** — the setting admits several cues that each reach training-set perfection.
  The data cannot say which one the model took. Choosing the wrong one is a **misspecification**.
- **Shortcut (simplicity) bias** — the systematic preference for the "simpler" cue. For
  vision-like factors the reported order is color ≻ scale, scale ≻ shape, and shape ≻ orientation.
  That order holds independently of the architecture and the training algorithm.
- **Diagonal / off-diagonal cell** — a combination of (task cue, bias cue) where the two agree /
  disagree.
- **Cue-by-cue accuracy** — accuracy of the same fixed predictions computed under each alternative
  labeling of the evaluation set by cue.
- **Counterfactual evaluation** — measure the model on edited inputs where exactly one cue was
  altered. Read the *change* in performance as evidence about that intervention. Counterfactual
  evaluation licenses a statement of the form "the model's behavior responds to this edit". That
  statement supports a dependence claim only when the edit is a valid intervention on the cue named
  by the edit. Absence of a change is weaker still. Redundant cues, compensatory cues, and cues the
  edit left recoverable all preserve accuracy. That preservation does not show that the cue went
  unused.

## 5. Procedure

**Core**

1. Build the contingency table of cue against label on the development data. List every cell with
   its count. A cell with near-zero support is a cue that you cannot verify later. Record that
   blind spot before you interpret results.
2. **Cue-by-cue accuracy.** On the off-diagonal evaluation subset, re-label the set once per
   candidate cue. Compute the accuracy of the frozen predictions under each labeling. The expected
   signature of a cue-dependent model is high accuracy under the label that model actually exploits.
   Under the other labels the accuracy is near chance.
3. **Counterfactual — alter the task cue.** For every evaluation sample, remove or replace the
   task-relevant cue. The edit may be mask + inpaint, silhouette-only, or texture-only. For text,
   the edit may be a paraphrase that deletes the task-bearing span. A material drop shows the
   model's predictions are **sensitive to this edit**. A non-drop does *not* show that the model
   never used the cue. The cue may be recoverable from what remains. The cue may be redundant with
   another factor. The edit itself may shift the inputs out of distribution. Record which of those
   you ruled out.
4. Use the same construction on the forbidden or tolerated cue, with the reading reversed. A
   material drop is evidence of dependence on the factor you edited, provided the edit isolated
   that factor. Naming *which* cue carries the prediction needs more than this one run. You must
   edit and compare the competing cues under the same intervention standard. The drop must also
   survive a further check. The drop must not be an editing artifact or a generic distribution
   shift.
5. Report both diagnostics **per cell**, not averaged. Average accuracy hides the off-diagonal
   failure that motivates the whole exercise.
6. Write the verdict into the cue whitelist. Phrase the verdict at the strength the design supports.
   The verdict labels are:

   - `edit-sensitive`
   - `no-sensitivity-detected-under-this-edit`
   - `undetermined-insufficient-support`

   A causal reading is an additional claim. The two readings
   are "the model uses cue C" and "the model ignores cue C". That claim needs an identification
   argument. Usually the argument is a controlled construction where C is the only route to the
   label. A designed benchmark gives that construction. State the argument, or withhold the reading.
   The `verified-*` labels are reserved for the cases where an argument exists.

**Extended** — add for high-stakes use, or when the counterfactuals are inconclusive:

7. Add a worst-group view. Compute accuracy per (task cue × bias cue) cell. Report the minimum cell
   as a first-class number alongside the average.
8. Use atypicality counting to find suspect samples when no bias labels exist. Rank the training
   samples by how rarely the (cue, label) co-occurrence appears. Inspect the tail of that ranking,
   or re-weight the samples in that tail. Treat the tail as a *hypothesis list*, never as proof.
9. Add an attribution-assisted probe. Use one attribution method that passed the checks in
   [`SOP-07`](SOP-07-evaluate-explanation-methods.md). Run that method on the failure cells. Compare
   the evidence that method claims against the counterfactual verdict. A disagreement is itself a
   finding. Record which instrument you doubt.
10. Add a capacity/recipe probe for the "bias is the first cue learned" assumption. Train a
    deliberately myopic variant (few epochs, small receptive field, single modality). Check whether
    that variant recovers the same dependence you measured.
11. Pre-register the edit types that a person applies by hand. Ad-hoc editing imports the
    editor's expectations into the result.

## 6. Mandatory checks

- [ ] **Cue disentanglement**: the evaluation set contains off-diagonal cells with nonzero support
      for every cue under test. Otherwise the diagnosis is undefined, not negative.
- [ ] **Single-cue editing**: each counterfactual changes exactly one factor. Verify that change by
      checking that the remaining factors are unchanged (mask area, style statistics, token diff).
- [ ] **Occlusion honesty**: whatever fills the removed region must not add information. That is
      the same control that governs remove-and-classify in `SOP-07`. A fixed color is a claim, not
      a null.
- [ ] **Significance stated as a range**: report the drop with a variability estimate (seeds or
      bootstrap). The source gives no universal threshold for "materially". Declare your own
      threshold before you read the result.
- [ ] **No expected-shape criterion**: the verdict may not be "the map looks right". Judge against
      the model's behavior, not against your prior about the object's location.
- [ ] **Blind-spot list is reproduced in the report** (§5 step 1).

## 7. Decision or stop conditions

- **Stop: undiagnosable** if no off-diagonal support exists, and if you cannot construct such
  support. Record the dependency as *unknown*, and treat any cross-bias generalization claim as
  unsupported.
- **Stop and re-run `SOP-01`** if the counterfactual verdict contradicts the whitelist. The
  setting, not the model, is what failed to describe the situation.
- **Do not proceed to mitigation** while an occlusion artifact could explain the result
  (`SOP-07` §8 on missingness bias). Fix the instrument first.
- **Escalate** and report by subgroup whenever the average and the worst cell disagree in
  direction.

## 8. Common methodological failures

- You confirm the explanation against what a human would say, instead of against what the model
  did.
- You treat localization quality ("the map covers the object") as evidence about the model's
  evidence. A model may legitimately decide from a non-object region. In that case the *worse*
  localizer explained the model better.
- You read one dataset's cue ranking as universal.
- You edit several correlated factors at once, and you attribute the drop to the intended factor.
- You average over diagonal and off-diagonal cells.
- You use a constant fill value that is itself informative for the architecture under test.
- You interpret "the model has no cue labels" as "the model has no cue dependence".

## 9. Required outputs

- Contingency table with cell support counts.
- Cue-by-cue accuracy table (one column per candidate labeling, one row per subset).
- Counterfactual result tables for both alteration directions, per cell, with variability
  estimates.
- Updated cue whitelist with `verified-*` / `undetermined` statuses and the blind-spot list.

## 10. Minimum reporting requirements

Report which cues you could test, and which cues you could not test. Report the editing operator
used, and what that operator fills with. Report the pre-declared materiality threshold. Report the
per-cell and worst-cell numbers next to the average. Where an attribution instrument contributed,
report which `SOP-07` checks that instrument passed.

## 11. Links to relevant Benchmarks

- [`BM-02`](../../Benchmark/Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md) — the standardized
  version of this SOP's two counterfactual protocols.
- [`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md) —
  supplies the shifted cells this SOP diagnoses.
- [`BM-06`](../../Benchmark/Trustworthy-ML-2023/BM-06-explanation-quality.md) — governs the
  instruments used in step 9.
- [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md) — checks that
  the diagnosis consumed no final-test information and disclosed its thresholds.

## 12. Source traceability

- Spurious correlation and underspecification definitions: §2.7.1, Definitions 2.27-2.28
  (book pp. 45-46), with the high-capacity precondition noted on p. 46.
- Shortcut/simplicity bias, its cue-preference order and the Kolmogorov-complexity rationale:
  §2.9, Definition 2.29 (pp. 49-50) and its example catalogue §2.9.1 (pp. 50-53).
- ID-versus-OOD valence of the bias: §2.9.2 (pp. 53-54).
- Unidentifiability of the deployment cue on a diagonal set: §2.8.2 (p. 47).
- Cue-by-cue accuracy: §2.8.4 (p. 49).
- Counterfactual evaluation, both alteration strategies, their ingredients and their decision
  rules, plus the "different papers do it differently" caveat: §2.10 (pp. 55-56).
- Atypicality/co-occurrence counting without bias labels: §2.12 (pp. 57-59).
- Myopic-model assumption used as a diagnostic handle: §2.13, Definitions 2.31-2.33
  (pp. 65-66, 74-75).
- Confirmation bias and the localization-evaluation fallacy: §3.7.3 (pp. 179-181).
- Missingness bias in occlusion operators: §3.7.8 (pp. 187-188).
- Worst-group versus average reporting: §2.12.1 (pp. 59-61).
- Pre-declaring the materiality threshold and the output-file shapes are repository conventions.

**Where this SOP reads the source more narrowly than the source reads itself.** The source states
its decision rules causally. For the task-cue alteration, no significant drop means "our model is
biased towards an irrelevant cue, meaning our system is misspecified". For the bias-cue alteration,
a significant drop means "we also know what our model is biased towards" (§2.10, pp. 55-56). Steps
3-4 and 6 here keep the two alterations and their decision directions unchanged. Those steps report
the outcome as sensitivity to the edit, rather than as proven cue use or non-use.

The reason is internal to the same passage. Both rules are listed with the ingredient *cue
disentanglement* — "the ability to change cues in the input independently". That ingredient is an
identification condition, not a property of the editing software. Where construction meets that
condition, the source's stronger reading is available, and step 6 says so. Where the condition is
only asserted, a non-drop can also mean a redundant or recoverable cue. In that case a drop can
also mean an out-of-distribution artifact.

The two-recipe structure, the ingredients and the "different papers do it differently" caveat are
source-derived. This calibration of the verdict language is **synthesized**.
