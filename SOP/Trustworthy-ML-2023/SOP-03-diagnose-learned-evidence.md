# SOP-03 — Diagnose which evidence the model actually uses

**Stage:** diagnose · **Tier:** Core + Extended · **Concepts:** C6 misspecification diagnosis,
C3 cue whitelist, C15 subgroup view, C17 (partial)

## 1. Purpose

Establish, by measurement rather than by looking at pictures, whether the model's predictions rest
on the cues the whitelist in
[`SOP-01`](SOP-01-specify-deployment-setting.md) allowed. A model can reach high in-distribution
accuracy while answering a different question than the one you asked; this SOP is how you find out
before deployment does.

## 2. When to use

- After the first reasonable training run, before tuning anything further.
- Whenever the setting's generalization type is cross-bias, or any forbidden cue is plausibly
  predictive in the training data.
- When an OOD drop occurs and you must attribute it to a cue rather than to "the shift".
- When an explanation method is to be used as evidence about the model (then also run
  [`SOP-07`](SOP-07-evaluate-explanation-methods.md)).

## 3. Inputs / prerequisites

- A trained model plus its validation predictions and per-sample losses.
- The cue whitelist (factors of variation with allowed/tolerated/forbidden status).
- **Per-cue labels on evaluation data** — attribute or group labels, or a way to construct them
  (segmentation masks, editing tooling, controlled resynthesis).
- A disentangled (off-diagonal) evaluation subset, from
  [`SOP-02`](SOP-02-build-evaluation-splits-under-leakage-discipline.md) §5 step 4.
- A budget for intervention: cue-editing or re-synthesis of test samples.

## 4. Definitions needed for execution

- **Spurious correlation** — co-occurrence of cues, features or labels that holds during
  development and not during deployment.
- **Underspecification** — the setting admits several cues that each reach training-set perfection,
  so the data cannot say which one the model took; choosing the wrong one is a **misspecification**.
- **Shortcut (simplicity) bias** — the systematic preference for the "simpler" cue; reported order
  for vision-like factors is colour ≻ scale ≻ shape ≻ orientation, independent of architecture and
  training algorithm.
- **Diagonal / off-diagonal cell** — a combination of (task cue, bias cue) where the two agree /
  disagree.
- **Cue-by-cue accuracy** — accuracy of the same fixed predictions computed under each alternative
  labelling of the evaluation set by cue.
- **Counterfactual evaluation** — measure the model on edited inputs where exactly one cue was
  altered, and read the *change* in performance as the evidence of dependence.

## 5. Procedure

**Core**

1. Build the cue × label contingency table on the development data; list every cell with its count.
   Any cell with near-zero support is a cue the model cannot be verified on later — record it as a
   blind spot before interpreting results.
2. **Cue-by-cue accuracy.** On the off-diagonal evaluation subset, re-label the set once per
   candidate cue, and compute accuracy of the frozen predictions under each labelling.
   Expected signature of a cue-dependent model: high accuracy under the label it actually exploits,
   near chance under the others.
3. **Counterfactual — alter the task cue.** For every evaluation sample, remove or replace the
   task-relevant cue (mask + inpaint, silhouette-only, texture-only, text paraphrase that deletes
   the task-bearing span). Decision: if performance does **not** drop materially, the model is not
   using the cue you believed.
4. **Counterfactual — alter the bias cue.** Same construction on the forbidden/tolerated cue.
   Decision is reversed: a material drop means the model *is* dependent on the bias cue, and this
   run also identifies which cue.
5. Report both diagnostics **per cell**, not averaged: average accuracy hides the off-diagonal
   failure that motivates the whole exercise.
6. Write the verdict into the cue whitelist: `verified-uses`, `verified-independent`,
   `undetermined-insufficient-support`.

**Extended** — add for high-stakes use, or when the counterfactuals are inconclusive:

7. Add a worst-group view: compute accuracy per (task cue × bias cue) cell and report the minimum
   cell as a first-class number alongside the average.
8. Use atypicality counting to find suspect samples without bias labels: rank training samples by
   how rarely their (cue, label) co-occurrence appears, and inspect or re-weight the tail. Treat the
   tail as a *hypothesis list*, never as proof.
9. Add an attribution-assisted probe: run one attribution method that has passed the checks in
   [`SOP-07`](SOP-07-evaluate-explanation-methods.md) on the failure cells, and compare its claimed
   evidence against the counterfactual verdict. Disagreement is itself a finding — record which
   instrument you doubt.
10. Add a capacity/recipe probe for the "bias is the first cue learned" assumption: train a
    deliberately myopic variant (few epochs, small receptive field, single modality) and check
    whether it recovers the same dependence you measured.
11. Where human text/image editing is feasible, pre-register the edit types used, because
    ad-hoc editing imports the editor's expectations into the result.

## 6. Mandatory checks

- [ ] **Cue disentanglement**: the evaluation set contains off-diagonal cells with nonzero support
      for every cue under test; otherwise the diagnosis is undefined, not negative.
- [ ] **Single-cue editing**: each counterfactual changes exactly one factor; verify by checking
      that the remaining factors are unchanged (mask area, style statistics, token diff).
- [ ] **Occlusion honesty**: whatever fills the removed region must not add information — the same
      control that governs remove-and-classify in `SOP-07`. A fixed colour is a claim, not a null.
- [ ] **Significance stated as a range**: report the drop with a variability estimate (seeds or
      bootstrap); the source gives no universal threshold for "materially", so declare yours before
      reading the result.
- [ ] **No expected-shape criterion**: the verdict may not be "the map looks right". Judge against
      the model's behaviour, not against your prior about the object's location.
- [ ] **Blind-spot list is reproduced in the report** (§5 step 1).

## 7. Decision or stop conditions

- **Stop: undiagnosable** if no off-diagonal support exists and none can be constructed. Record the
  dependency as *unknown*, and treat any cross-bias generalization claim as unsupported.
- **Stop and re-run `SOP-01`** if the counterfactual verdict contradicts the whitelist — the
  setting, not the model, is what failed to describe the situation.
- **Do not proceed to mitigation** while an occlusion artefact could explain the result
  (`SOP-07` §8 on missingness bias); fix the instrument first.
- **Escalate** to subgroup reporting whenever the average and the worst cell disagree in direction.

## 8. Common methodological failures

- Confirming the explanation against what a human would have said, instead of against what the
  model did.
- Treating localization quality ("the map covers the object") as evidence about the model's
  evidence: a model may legitimately decide from a non-object region, in which case the *worse*
  localizer explained the model better.
- Reading one dataset's cue ranking as universal.
- Editing several correlated factors at once and attributing the drop to the intended one.
- Averaging over diagonal and off-diagonal cells.
- Using a constant fill value that is itself informative for the architecture under test.
- Interpreting "the model has no cue labels" as "the model has no cue dependence".

## 9. Required outputs

- Contingency table with cell support counts.
- Cue-by-cue accuracy table (one column per candidate labelling, one row per subset).
- Counterfactual result tables for both alteration directions, per cell, with variability estimates.
- Updated cue whitelist with `verified-*` / `undetermined` statuses and the blind-spot list.

## 10. Minimum reporting requirements

Report: which cues could be tested and which could not; the editing operator used and what it fills
with; the pre-declared materiality threshold; per-cell and worst-cell numbers next to the average;
and, where an attribution instrument contributed, which `SOP-07` checks that instrument had passed.

## 11. Links to relevant Benchmarks

- [`BM-02`](../../Benchmark/Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md) — the standardized
  version of this SOP's two counterfactual protocols.
- [`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md) —
  supplies the shifted cells this SOP diagnoses.
- [`BM-06`](../../Benchmark/Trustworthy-ML-2023/BM-06-explanation-quality.md) — governs the
  instruments used in step 9.

## 12. Source traceability

Spurious correlation and underspecification definitions: §2.7.1, Definitions 2.27-2.28
(book pp. 45-46), with the high-capacity precondition noted on p. 46. Shortcut/simplicity bias, its
cue-preference order and the Kolmogorov-complexity rationale: §2.9, Definition 2.29 (pp. 49-50) and
its example catalogue §2.9.1 (pp. 50-53); ID-versus-OOD valence of the bias: §2.9.2 (pp. 53-54).
Unidentifiability of the deployment cue on a diagonal set: §2.8.2 (p. 47). Cue-by-cue accuracy:
§2.8.4 (p. 49). Counterfactual evaluation, both alteration strategies, their ingredients and their
decision rules, plus the "different papers do it differently" caveat: §2.10 (pp. 55-56).
Atypicality/co-occurrence counting without bias labels: §2.12 (pp. 57-59). Myopic-model assumption
used as a diagnostic handle: §2.13, Definitions 2.31-2.33 (pp. 65-66, 74-75). Confirmation bias and
the localization-evaluation fallacy: §3.7.3 (pp. 179-181). Missingness bias in occlusion operators:
§3.7.8 (pp. 188-189). Worst-group versus average reporting: §2.12.1 (pp. 59-61). Pre-declaring the
materiality threshold and the output-file shapes are repository conventions.
