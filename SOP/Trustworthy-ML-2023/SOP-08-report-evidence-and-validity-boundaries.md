# SOP-08 — Report evidence and state validity boundaries

**Stage:** report · **Tier:** Core + Extended · **Concepts:** C18 reporting, C15 subgroup view,
C14 cost

This document also carries the **shared glossary and metric register** for the whole group. Other
SOPs and all benchmarks link here rather than restating definitions, so a term has exactly one
meaning inside the package.

## 1. Purpose

Make a result auditable: a reader must be able to tell what was measured, under which setting, at
what cost, and what the number does *not* license. Under-reported evidence — not bad models — is
what makes trustworthy-ML claims unrepeatable.

## 2. When to use

- Before publishing, handing off, or shipping any result produced with SOP-01 … SOP-07.
- When inheriting someone else's result as a baseline.
- When a benchmark package is being maintained and its numbers refreshed.

## 3. Inputs / prerequisites

- All §9 outputs of the SOPs that were run.
- The shared evaluation implementation used for every metric (see step 2 of §5).
- Compute, label and human-cost accounting for the whole pipeline, not only the final model.

## 4. Definitions needed for execution — shared glossary

*Setting terms.* **Setting** = (development resources, deployment environment, time).
**Development** covers training *and* all design choices, including reported testing.
**Deployment** is the frozen model meeting a changing environment.
**Generalization type** ∈ {ID, cross-domain, cross-bias, adversarial, declared-other}.
**Cue** = factor of variation in the data; **causal/robust** vs **spurious/non-causal** relative to
the declared deployment. **ρ** = fraction of unbiased (off-diagonal) development samples, with its
direction always stated. **Underspecification** = several cues each reach training perfection, so
the data do not determine which was learned; **misspecification** = the learned one was wrong.

*Metric register.* Names are fixed package-wide; use these, not synonyms.

| Metric | Definition to use | Where it is valid | Known degeneracy |
|---|---|---|---|
| `acc_avg` | fraction correct over the evaluation set | any labelled subset | averages away minority cells |
| `acc_worstgroup` | minimum accuracy over declared groups/cells | groups defined and non-empty | noisy when a cell is tiny |
| `nll` | −(1/N) Σ log f_y(x) on the evaluation set | probabilistic outputs | mixes accuracy and calibration; floor unknown |
| `brier` | (1/N) Σ [ (1 − f_y)² + Σ_{k≠y} f_k² ] | probabilistic outputs | as `nll`, softer tails |
| `perplexity` | exponentiated `nll` (base 2) | language modelling | same confound as `nll` |
| `ece` | Σ_m (|B_m|/N) · \|acc(B_m) − conf(B_m)\|, bins disclosed | scalar confidence in [0,1] | gameable by constant confidence; bin-sensitive |
| `mce` | max_m \|acc(B_m) − conf(B_m)\| | high-risk claims | pessimistic on small bins |
| `reliability` | per-bin acc and (conf − acc), plotted with the confidence histogram | diagnosis of over/under-confidence | does not reveal `ece` without bin weights |
| `auroc` | probability that a correct case outranks an incorrect one by `c` | ranking claims | insensitive to the absolute scale |
| `aupr_success`, `aupr_error` | area under precision-recall for correct-as-positive / error-as-positive | ranking under imbalance | random baseline = P(L = 1), so near-useless at extreme rates |
| `risk_at_coverage` | error rate among the top-k fraction by confidence | abstention | undefined without the coverage stated |
| `acc_under_eps` | accuracy under a named attack, **norm + ε + attack configuration attached** | adversarial claims | fake-safe when the defense masks gradients |
| `certified_acc` | fraction of inputs with a proof of invariance inside the ball | architectures the bound admits | bound may be arbitrarily loose |
| `remove_classify_auc` | area under accuracy-vs-removed-feature-count curve, relative to random occlusion | ordering claims about attributions | measures the occlusion artefact as well as importance |
| `sanity_rankcorr` | rank correlation between attributions of a true-label and a random-label model | explanation soundness | a necessary, not sufficient, condition |
| `hitl_delta` | change in human task performance / behaviour with vs without the explanation | trust and understanding goals | costly, design-sensitive |
| `self_influence_auroc` | detection of suspicious training items by their self-influence score | training-data attribution | assumes few, non-systematic mislabels |
| `tnr_at_high_tpr` | true-negative rate evaluated at a fixed high true-positive rate (state the rate) | false-alarm budgets matter more than averages | meaningless without the fixed TPR stated |
| `audit_pass_rate` | applicable integrity requirements passed ÷ applicable requirements | protocol audits | inflates if inapplicable requirements are dropped silently |
| `conclusion_flip_count` | number of headline conclusions that change sign or significance under a protocol perturbation | protocol audits | depends on which perturbations were run |
| `disclosure_completeness` | fraction of this SOP's §6 checklist items present in the report | any report | measures documentation, not correctness |

*Cost terms.* **Tuning budget** = search space and number of evaluations granted to every compared
method. **Training overhead** = multiplier on passes/epochs/capacity. **Inference overhead** = added
cost per prediction. **Query cost** = black-box interactions needed. **Label cost** = extra
supervision consumed.

## 5. Procedure

**Core**

1. Assemble the report from the SOP outputs in this order: setting block → split manifest and
   contamination report → main results with worst-cell view → diagnosis verdicts → confidence
   battery with trivial controls → stress results with threat model → mitigation decision and cost →
   explanation usability decision (if any) → validity boundaries.
2. Compute every metric through one shared implementation for all compared methods, including the
   corner cases (empty bins, zero-positive thresholds, tie handling). If a corner case is
   conventionally handled differently in your subfield, state the convention chosen.
3. Attach a trivial or reference row to every table: constant baseline, random ordering, unmodified
   model, tuned-simple baseline. A number without a reference row is not evidence.
4. State the boundaries explicitly as a short list of "does not show" claims, drawn from the checks
   that failed or were skipped.
5. Report average *and* failure-oriented views side by side whenever they differ in direction.
6. Report cost next to gain, including human label cost.
7. Record reproducibility facts that affect the numbers: data version/hashes, model family,
   recalibration status, seeds and number of runs with variability.

**Extended** — publication-grade or safety-relevant:

8. Add the provenance appendix: which results were reused from prior work, whether their settings
   matched, and any re-implementation difference observed.
9. Add a sensitivity panel: bin counts, ε values, occlusion operators, ρ, group definitions — one
   small table per axis that could flip a conclusion.
10. Add a negative-results section; a mitigation that failed its assumption test is a finding.
11. Where you maintain a benchmark, record the refresh policy and the leaderboard exposure policy.

## 6. Mandatory checks

- [ ] Every metric name in the report appears in the register above with the definition used.
- [ ] Every table has a reference row and a variability statement.
- [ ] Every confidence claim carries binning, split provenance, and the trivial-control comparison.
- [ ] Every robustness claim carries norm, ε, attack configuration, and masking-check outcome.
- [ ] Every explanation claim carries the controls that method passed.
- [ ] Every comparison states tuning-budget parity, or is moved to a separate setting.
- [ ] Cost is reported for the trustworthy components, not just the base model.
- [ ] The "does not show" list is non-empty unless every check passed.

## 7. Decision or stop conditions

- **Do not publish** if a headline number's meaning depends on an undisclosed choice (bins, ε,
  occlusion operator, group definition, ρ direction).
- **Stop and re-run `SOP-02` checks** if the report shows any selection made on a final-test subset.
- **Downgrade the claim** to the strongest setting actually evidenced; move stronger-setting results
  into their own table rather than merging them.

## 8. Common methodological failures

- Reporting accuracy only, letting the reader assume calibration and robustness.
- Different metric implementations per method, so tiny code-level differences become "gains".
- Silent convention choices in degenerate cases (empty-bin precision).
- Quoting a leaderboard number as independent confirmation.
- Presenting an oracle-selection or train-on-target row inside the main table without marking it.
- Reporting the average while the deployment decision is made on the worst cell.
- Omitting the cost of the trustworthy component, which is how complicated methods get adopted and
  then fail at scale.
- Treating architecture-family differences in calibration as a property of the method being studied.

## 9. Required outputs

- `report.md` following §5 step 1 order, with the metric register names.
- `tables/` with reference rows and variability.
- `boundaries.md` — the "does not show" list and the failed/skipped checks.
- `cost.md` — tuning, training, inference, query, label and human cost.
- Sensitivity panel and provenance appendix (Extended).

## 10. Minimum reporting requirements

Minimum viable report: setting block verbatim; split provenance and test-contact count; main table
with average *and* worst cell; reference rows; per-claim attachments as in §6; cost line; boundary
list. If any of these is absent, the result is not yet a trustworthy-ML result — it is a number.

## 11. Links to relevant Benchmarks

- [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md) — executes the
  audit of this SOP's outputs.
- All other benchmarks (`BM-01` … `BM-07`) define their reporting fields against §4 of this document.

## 12. Source traceability

Setting and resources vocabulary: §2.3.1, Definitions 2.14-2.19 (book pp. 24-25). Split roles:
§2.3.2, Definitions 2.20-2.22 (pp. 26-27). Test-set spoiling as a spectrum: §2.3.3 (p. 29).
Cue/ID-OOD/generalization types: §2.1.2, Definitions 2.5-2.8 (pp. 18-19). Spurious correlation,
underspecification, shortcut bias: §2.7.1, §2.8.2, §2.9, Definitions 2.27-2.29 (pp. 45-50).
Metric-implementation divergence and the empty-bin precision case; hidden-resources/compute axis;
train-test contamination; missing-validation-set pathology; shared evaluation server or library:
§5.1.3 (pp. 337-341). Upper-bound violation must be explained (bug, flawed bound, or different
ingredients): §5.1.1 (p. 335). Cost of wrong evaluation and the scandal list: §5.1.2 (pp. 335-337).
Tuned-baseline and weight-decay examples: §5.2.2 (pp. 341-343). Random search with shared budget:
§5.2.3 (p. 343). Toy-versus-large-scale trade-off: §5.2 (pp. 338-340). Benchmark fairness requires
equal ingredients: §5.3.1 (p. 344). Metric definitions: ECE/MCE/reliability §4.6.1-§4.6.3,
Definitions 4.11-4.15 (pp. 254-259); NLL/Brier/perplexity §4.5.2-§4.5.9 (pp. 245-254);
AUROC/AUPR §4.9.2 (pp. 267-268); risk at coverage and threshold filtering §4.9.1 (pp. 265-266);
`acc_under_eps` and its reporting table §2.15.3-§2.15.4 and Table 2.8 (pp. 90-92, 103); certified
accuracy §2.15.15 (pp. 111-113); remove-and-classify §3.7.7, Definition 3.14 (pp. 186-188); sanity
rank correlation §3.7.5 (pp. 185-187); HITL §3.8.2, Definition 3.15 (pp. 193-197); self-influence
§3.12.2, Definition 3.16 (pp. 216-217). Worst-group reporting: §2.12.1 (pp. 59-61). Architecture
family and recalibration status: §4.8.1-§4.8.3 (pp. 261-265). The register format, the "does not
show" list and the sensitivity panel are repository conventions.
