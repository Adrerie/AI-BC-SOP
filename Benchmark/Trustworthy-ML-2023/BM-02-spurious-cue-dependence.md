# BM-02 — Spurious-cue dependence

**Tier:** Core (one bias–task pair) + Extended (multiple biases, ρ sweep, mitigation stress)

## 1. Target capability / failure mode

**Capability.** Predicting from the cue the whitelist designates as legitimate evidence, when the
training data also offer an easier cue that correlates with the label during development only.

**Failure mode under test.** Misspecification: the model answers a different question than the task
states. Underlying mechanisms named by the source: spurious correlation (development-only
co-occurrence), underspecification (several cues each reach training perfection), and shortcut or
simplicity bias (a systematic preference for the easier cue, reported as colour ≻ scale ≻ shape ≻
orientation in vision-like data regardless of architecture and algorithm).

This benchmark is distinct from `BM-01`: a model can transfer across styles and domains while still
deciding from a cue that a changed correlation would break.

## 2. Evaluation hypothesis

*Model M's decisions depend on the forbidden cue to a degree that costs accuracy on the
off-diagonal evaluation cells, and a mitigation reduces that dependence without destroying average
performance.* Every claim needs a bias-labelled, disentangled evaluation set: on a diagonal training
set alone the deployment cue is not identifiable, so the hypothesis is untestable and any reported
"robustness" implies an undocumented ingredient.

## 3. Required data and split assumptions

- Two declared factors: the task cue and the bias cue, with per-sample labels for both.
- Four cells: diagonal (task and bias agree) and off-diagonal (they disagree), per cue value pair.
- Training material: abundant diagonal samples plus a stated unbiased fraction **ρ** — state the
  direction of ρ explicitly, since the literature uses the symbol both ways.
- Evaluation material: off-diagonal cells with nonzero support, and (Extended) a *biased* and an
  *unbiased* test set scored separately.
- Validation per [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md):
  from the training cells, never from the off-diagonal cells being reported.
- The deployment distribution is deliberately **not** restricted: it may carry a different bias than
  development, and the benchmark must remain readable under that possibility.

## 4. Shift or stress construction

**Core.** Correlation stress: hold the task fixed and flip the cue–label relation in the evaluation
set (swap the bias value while keeping the task cue intact), or remove the bias cue entirely.
Construct it by editing exactly one factor and verifying the others are unchanged.

**Extended.**
- *Cue-by-cue relabelling*: re-label the same off-diagonal set once per candidate cue and score the
  frozen predictions under each labelling; the learned cue shows high accuracy, the others near chance.
- *Task-cue ablation*: mask or remove the task-relevant cue (segmentation + inpainting,
  silhouette-only, texture-only, or text-span deletion). No material drop ⇒ the model was not using it.
- *Bias-cue ablation*: the symmetric construction, where a material drop identifies the bias.
- *Myopia probe*: train a deliberately handicapped model (few epochs, small receptive field, single
  modality) and check that it learns the same cue you call the bias.
- *ρ ladder*: repeat at several unbiased fractions, including the regime where the method's
  assumption is said to hold, and record where it breaks.
- *Role swap*: exchange which factor is task and which is bias, and re-run — several published
  constructions fail here, which is an assumption failure rather than a baseline weakness.

## 5. Required baselines

| Baseline | Role |
|---|---|
| Plain trained model (fairly tuned) | reference dependence level |
| Reweighting of off-diagonal samples | the naive intervention named by the source; must be beaten, not ignored |
| Worst-group objective (group-DRO style), with groups declared as either full cue cells or diagonal/off-diagonal | supervision-consuming comparator |
| Domain-adversarial alignment, with its bias label encoded as domain | comparator when attribute labels exist |
| Contrast method using a biased/myopic model | comparator when bias labels do **not** exist |
| Oracle upper bound trained on off-diagonal data | labelled upper bound only |
| Random-chance-per-cell reference | prevents reading a small-cell number as skill |

## 6. Primary metrics

- `acc_worstgroup` over the cue cells — the headline.
- Off-diagonal accuracy as its own column (never folded into an average).
- Dependence delta: `acc_diagonal − acc_offdiagonal`.
- Counterfactual drop: change in accuracy/loss under each single-cue edit, reported with its
  variability and a pre-declared materiality threshold.

## 7. Secondary / diagnostic metrics

- Cue-by-cue accuracy table (one column per candidate labelling).
- Confusion between cues: how often the model's decision is reproducible from the bias cue alone.
- Calibration per cell (`BM-03`), because a biased model is often confidently biased.
- Explanation-derived importance (`BM-06`) cross-checked against the counterfactual verdict — a
  disagreement is a finding about the instrument, not about the model.
- Cell support counts, to bound the interpretation of rare cells.

## 8. Aggregation and uncertainty reporting

Report per cell, then a worst-cell, then (separately) an average. Two aggregation traps are
specific to this design: an average over diagonal and off-diagonal cells conceals the failure that
defines the benchmark, and a small off-diagonal cell produces a wide estimate — so give the
bootstrap or seed spread for every cell reported, and mark cells whose support is below the level
needed to interpret them. Do not pool results across different ρ values or different bias
definitions.

## 9. Failure interpretation

| Observation | Reading |
|---|---|
| Off-diagonal accuracy near chance, diagonal high | shortcut bias realized; the model used the bias cue |
| Counterfactual task-cue edit causes no drop | the intended task cue is not what the model uses |
| Bias-cue edit causes a large drop | dependence on the forbidden cue confirmed, and the cue identified |
| Mitigation raises worst cell and lowers average sharply | traded the wrong axis; revisit [`SOP-06`](../../SOP/Trustworthy-ML-2023/SOP-06-choose-mitigation-or-abstain.md) |
| Method collapses under role swap | its "easy cue first" assumption fails in this data |
| Attribution disagrees with counterfactuals | instrument failure (see `BM-06`) or occlusion artefact |
| Only diagonal cells exist | undiagnosable; report the dependence as unknown |

## 10. Computational reporting

State the cost of constructing the disentangled cells (annotation, editing, resynthesis) — for most
of these methods the *data engineering* dominates the training cost. Report per-method tuning
budget, the number of ρ configurations, and the extra model required by contrast methods (a biased
model is an additional training run).

## 11. Validity limits

- The benchmark can only test cues you named and labeled; an unmodelled third factor can carry the
  dependence unnoticed.
- Off-diagonal support is a hard precondition: without it the result is a statement about
  correlation, not about evidence.
- Editing operators are not neutral; a filling value can itself be informative, so an apparent
  dependence change may be an artefact of the occlusion.
- Human-judgement-based edits import the editor's expectations; treat them as hypotheses.
- A clean result does not establish causal use of a cue — it establishes dependence under the tested
  counterfactuals.
- Compositional caveats: treating semantically independent input parts as independent can make
  spurious correlation impossible by construction, which is a property of the design, not of the
  model.

## 12. Related SOPs

Needs [`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md) §5 step 4 (cue
whitelist, ρ) and [`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md)
§5 step 4 (off-diagonal cells); executed by
[`SOP-03`](../../SOP/Trustworthy-ML-2023/SOP-03-diagnose-learned-evidence.md); mitigation results
read by [`SOP-06`](../../SOP/Trustworthy-ML-2023/SOP-06-choose-mitigation-or-abstain.md); reporting
through [`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md).

## 13. Source traceability

Spurious correlation, underspecification/misspecification and their high-capacity precondition:
§2.7.1, Definitions 2.27-2.28 (pp. 45-46). Shortcut/simplicity bias, its cue ordering and the
complexity rationale: §2.9, Definition 2.29 (pp. 49-50); example catalogue of bias/task cue pairs:
§2.9.1 (pp. 50-53); ID-versus-OOD valence: §2.9.2 (pp. 53-54). Non-identifiability of the
deployment cue on a diagonal set and the hidden-ingredient argument: §2.8.2 (p. 47). Subgroup
requirement and unrestricted deployment distribution: §2.8 (p. 46). ρ as part of the setting,
attribute labels, and the domain-adaptation escape route: §2.8.3 (p. 48); ρ-direction inconsistency
observed at §2.13.2 Table 2.5 (p. 74). Cue-by-cue accuracy: §2.8.4 (p. 49). Counterfactual
evaluation with both alteration directions, their ingredients and desiderata: §2.10 (pp. 55-56).
Scenario-1 up-weighting and atypicality counting: §2.12 (pp. 57-59). Worst-group objective, grouping
choice and the average/worst trade-off: §2.12.1, Definition 2.30 (pp. 59-61). Adversarial alignment
with bias-as-domain encodings: §2.12.2 (pp. 62-65). Biased/myopic model definitions and "be
different" supervision: §2.13, Definitions 2.31-2.33 (pp. 65-66, 74-75). Role-swap failure of the
contrast method: §2.13.1 (pp. 67-70). Biased-versus-unbiased dual test sets and the ρ sweep:
§2.13.2 (pp. 70-75). Compositional independence remark: §2.8 (p. 46). Missingness/occlusion
artefacts: §3.7.8 (pp. 188-189). Tiering and the pre-declared materiality threshold are repository
conventions built on the source's note that papers differ in how they judge a "significant" drop.
