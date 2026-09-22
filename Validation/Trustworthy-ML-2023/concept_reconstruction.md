# Concept Reconstruction — *Trustworthy Machine Learning* (2023)

Plan 2 artifact. Input: [`source_coverage.md`](source_coverage.md) (Gate A passed).
Output: the methodology model that Plans 3 and 4 must follow.

The book is organised as four research areas plus a closing chapter (OOD generalization,
explainability, uncertainty, evaluation & scalability). The reconstruction below is organised
**by what a researcher has to decide and do**, and deliberately cuts across those areas. Where a
concept gathers material from several chapters, that is noted; where a chapter turns out to
contribute to several concepts, both directions are listed so traceability stays checkable.

---

## Step 1 — Concept graph

Legend for *Destination*: `SOP` = becomes a procedure, `BM` = becomes a benchmark component,
`both` / `background`. *Body* = whether the concept required reading body text beyond headings.

| # | Synthesized concept | Research question it answers | Contributing source sections | Depends on | Destination | Body |
|---|---|---|---|---|---|---|
| C1 | **Setting declaration** | Which resources, labels, target distribution, and time behavior am I actually allowed to use, and therefore which literature may I compare myself to? | 2.3.1 (Def 2.14-2.19), 2.4.2-2.4.11, 2.8.3, 5.3.1, 1.4.2 | — | SOP, BM | yes |
| C2 | **Generalization-type axis** | Which kind of train→test difference am I claiming to survive: domain, cue-correlation, adversarial, or none (ID)? | 2.1.2 (Def 2.8), 2.7.1, 2.8-2.8.2, 2.15, 2.15.1, 1.4.1 | C1 | SOP, BM | yes |
| C3 | **Cue whitelist (causal vs spurious)** | Which factors of variation is the model *allowed* to use as evidence for the task? | 1.4.1, 2.6-2.7.1 (Def 2.27, 2.28), 2.9 (Def 2.29), 2.8.2, 3.1.1 | C1, C2 | SOP, BM | yes |
| C4 | **Evaluation-information discipline (leakage)** | Did information from the deployment stage reach development — through tuning, viewing, pretraining, or leaderboards? | 2.3.2-2.3.3, 2.5-2.5.3 (Def 2.24, 2.25), 5.1.3, 2.14.1, 2.15.12 (leaderboard-adjacent), 3.12.2, 4.8.3 | C1 | SOP, BM | yes |
| C5 | **Test-set finiteness (spoiling)** | How often may the test set be consulted before its number stops meaning generalization? | 2.3.3, 2.5.1 (fn. 7), 2.5.3, 5.1.3, 2.6.1 | C4 | SOP, BM | yes |
| C6 | **Misspecification diagnosis** | Which cue did the model actually learn, and is it the one we asked for? | 2.8.4, 2.10, 2.12 (co-occurrence counting), 3.7.3-3.7.8, 3.11.1, 3.12.2 (Def 3.16), 5.1.1 (upper-bound check) | C3 | SOP, BM | yes |
| C7 | **Confidence-truthfulness contracts** | Must the number be a probability (proper scoring), a conditional accuracy (calibration), or only an order (ranking)? | 4.4, 4.5-4.5.9 (Def 4.8-4.10), 4.6-4.6.3 (Def 4.11-4.15), 4.7, 4.9-4.9.2, 4.13.3 | C8 | SOP, BM | yes |
| C8 | **Uncertainty quantity separation** | Am I measuring predictive, aleatoric, or epistemic uncertainty — and is my instrument sensitive to the one I named? | 4.2-4.2.4 (Def 4.1-4.7), 4.3.1-4.3.3, 4.10-4.10.3, 4.11-4.12.3, 4.13.9, 2.7.1 | C2 | SOP, BM | yes |
| C9 | **Proxy-task gap** | Is my benchmark measuring the property, or a downstream correlate of it? | 4.10.1-4.10.2, 4.12.3, 4.2.3, 3.7.2 (functionally-grounded), 3.12.2, 2.14.1 (oracle selection), 3.7.7 | C7, C8 | SOP, BM | yes |
| C10 | **Metric gaming and degeneracy** | Can a model score perfectly on this metric while the property is absent? | 4.6.2, 4.6.1 (bin sensitivity), 4.9.2 (imbalance), 5.1.3 (AP empty bin), 2.15.12 (masked gradients), 3.7.3 (confirmation bias), 3.7.8 (missingness bias), 5.2.2 (untuned baseline) | C7 | SOP, BM | yes |
| C11 | **Threat-model specification** | For worst-case evaluation: what is the goal, the strategy space, and the attacker's knowledge? | 2.15-2.15.5, 2.15.8-2.15.10, 2.15.15, 2.1.2 (adversarial row) | C2 | SOP, BM | yes |
| C12 | **Guarantee vs empirical claim** | Is the claim "no attack found", "no attack exists within a bound", or "average accuracy held"? | 2.15.15, 2.15.13, 4.11.10, 4.14.2 (no propriety guarantee), 2.7.1 (no rigorous theory), 4.9.1 (monotone g) | C11, C7 | SOP, BM | yes |
| C13 | **Mitigation admissibility** | Given exactly these labels and samples, which interventions are even well-posed? | 2.11, 2.12-2.12.2, 2.13-2.13.2, 2.14, 4.8.3, 2.15.11, 2.15.14, 4.13.5 | C1, C6 | SOP, BM | yes |
| C14 | **Cost-and-scale contract** | What compute, memory, label, human-review and tuning budget does the trustworthy component add, and does the result survive a larger regime? | 5.2-5.2.3, 5.1.3 (hidden resources), 4.11.3/4.11.6/4.11.9 (estimator costs), 2.15.11 (T+1 ledger), 2.15.10 (query accounting), 1.2.2, 3.7.2 (evaluation cost ladder), 5.3.5 | C1, C13 | SOP, BM | yes |
| C15 | **Subgroup / worst-case view** | Does the average hide the cell we care about? | 2.6 (Def 2.26), 2.8 (p. 46 balanced cells), 2.12.1 (worst-group), 4.6.2 (MCE, per-class worst case), 4.5.9 (imbalanced floor), 2.14/2.13.2 (biased vs unbiased test sets) | C3, C7 | SOP, BM | yes |
| C16 | **Selective action and abstention** | When should the system decline, ask, or hand over, and at what cost? | 4.1.2-4.1.3 (cost table, open set, active learning, objectness), 4.9.1 (threshold filtering), 2.14 (test-time selection), 3.1.4-3.1.5 | C7, C8 | SOP, BM | yes |
| C17 | **Explanation-by-attribution as an instrument** | What can an attribution map legitimately tell us about the model, and what is it not allowed to prove? | 3.1-3.6.6 (Def 3.1-3.12), 3.7.1 (trade-off), 3.8.1 (end goals), 3.9, 3.10-3.13 | C3, C6, C9 | SOP, BM | yes |
| C18 | **Reporting and validity boundary** | What must be stated so a reader can tell what the number does and does not license? | 2.3.1 (setting), 4.6.1 (bins), 2.15.3-2.15.4 (ε, norm, attack config), 3.7.7-3.7.8 (occlusion operator), 4.8.2 (architecture family, recalibration), 5.1.3 (metric implementation), 2.14.1 (upper-bound labeling), 4.11.10, 4.12.3 | all | SOP, BM | yes |
| C19 | **What→How framing (ML 2.0)** | Why is predicting Y from X insufficient, and what supervision would make "How" questions answerable? | 1.4-1.4.2 (Def 1.2-1.5), 5.3-5.3.5, 2.14.1, 4.3.2 | — | background | yes |
| C20 | **Illustrative catalogues** | Concrete named datasets/methods that serve as defaults, not as taxonomy. | 2.6.1 (PACS, DomainBed, WILDS, ImageNet-C/-A/-O), 3.5.x method catalogue, 4.11-4.13 estimator catalogue, 5.1.2 scandal list, Table 2.2 shortcut examples | C1-C18 | background (defaults referenced from SOPs) | yes |

Cross-chapter synthesis is the normal case here, not the exception: C4 and C5 fuse chapter 2's
setting theory with chapter 5's evaluation scandals and chapter 4's recalibration protocol; C10
fuses chapters 4, 5 and 3 (calibration gaming, benchmark scandals, explanation sanity); C6 fuses
chapter 2's counterfactual diagnostics with chapter 3's attribution evaluation; C14 fuses chapter 5
with the cost statements buried in chapters 2-4. Conversely, chapter 4 contributes to six different
concepts and chapter 3 to five.

---

## Step 2 — Separated classification axes

The following stay in separate columns everywhere in this package. Conflating them is one of the
book's recurring complaints, so the artifacts keep them apart by construction.

| Axis | Values used in this package | Source anchor |
|---|---|---|
| **Research problem** | survive a changed distribution; act on the right evidence; report honest confidence; decline safely; explain the decision; compare methods fairly | 1.4, 2.1.2, 4.3.3, 3.8.1, 5.1 |
| **Evaluation capability** | ID task performance, OOD/domain generalization, cross-bias robustness, adversarial robustness, uncertainty quality, calibration, error/OOD/multiplicity detection, explanation soundness, selective coverage, cost at scale | Def 2.8, Def 2.26, 2.15, 4.7, 4.10, 3.7, 4.1.3, 5.2 |
| **Method family** (never a capability name) | re-weighting / group-DRO; domain-adversarial; biased-model ("be different"); diverse-ensemble + test-time selection; ensembling / BBiA / SWA-family; feature-distance; distribution-parameter heads (heteroscedastic NLL, MoG); recalibration (temperature); attribution estimators (gradient / smoothing / integration / partition-value / concept / activation / influence); adversarial training; certified relaxation | 2.12-2.14, 4.11-4.13, 4.8.3, 3.5-3.11, 2.15.11, 2.15.15 |
| **Data / distribution condition** | ID; domain shift; bias-cue correlation (diagonal vs off-diagonal); corruption severity; multiplicity / ambiguity; subpopulation imbalance; adversarial ε-ball; scale regime (toy vs large-scale) | 2.1.2, 2.4, 2.7.1, 2.8, 4.10, 2.6, 2.15, 5.2 |
| **Metric** | accuracy; average vs worst-group accuracy; accuracy-under-ε (norm-qualified); NLL / CE / perplexity; Brier (binary, multi-class); ECE / MCE / reliability diagram; AUROC; AUPR-Success / AUPR-Error; risk-coverage of a abstention rule; remove-and-classify AUC; rank correlation under randomization; certified accuracy | 2.12.1, 2.15.3, 4.5-4.6, 4.9.2, 3.7.5-3.7.7, 2.15.15 |
| **Deployment constraint** | labeled target samples at dev (none / few / many); unbiased-sample fraction ρ; attribute or group labels; visual access to deployment data; pretraining corpus; human review budget; latency/memory; leaderboard visibility | 2.4, 2.8.3, 2.5.1, 4.1.3, 5.2 |
| **Failure mode** | information leakage; test-set spoiling; benchmark contamination; confounded ingredients; untuned baseline; metric gaming; metric degeneracy under imbalance; wrong proxy for the property; ill-defined behavior on no-data regions; underspecification; shortcut bias; gradient masking; missingness bias; confirmation bias; NLL overfitting; architecture-dependent calibration | 2.5, 2.3.3, 5.1.3, 5.2.2, 4.6.2, 4.9.2, 4.10, 2.7.1, 2.8.2, 2.9, 2.15.12, 3.7.8, 3.7.3, 4.8.1, 4.8.2 |
| **Reporting requirement** | setting block; split provenance; ρ and label inventory; ε + norm + attack configuration and iteration budget; bin count and confidence-histogram; occlusion/inpainting operator; recalibration status and the set it was fitted on; compute/human cost; upper-bound rows labeled; metric implementation identity | C18 sources above |

Deliberate separations worth naming:

- *OOD generalization* is a capability (C2/C8), not a method: domain-adversarial training,
  re-weighting and test-time selection are three different method families that can each be
  evaluated under the same capability, and each requires a different supervision condition (2.11-2.14).
- *Calibration* is a metric family (C7), not the property "good confidence"; the property is
  c(x) = P(L = 1), and calibration is only a necessary condition for it (4.6.1).
- *Uncertainty estimate quality* splits three ways — a score may be well-calibrated, well-ranked, and
  still wrong per sample (4.6.2 vs 4.9.1).
- *Explainability* is a capability whose instruments (attribution methods) are themselves objects of
  evaluation (C17); the method is never the metric (3.7.3).
- *Robustness intervention* (adversarial training) and *robustness evaluation* (the attack ladder and
  its configuration) are separated, because a defense can make the evaluation lie (2.15.12).

---

## Step 3 — Operational taxonomy

Workflow shape derived from the concept graph (the book's own arc, made sequential):

```text
declare the setting  ->  freeze splits under leakage discipline  ->  train
   ->  diagnose which evidence the model uses  ->  measure confidence honestly
   ->  stress the model in the worst case      ->  mitigate and/or abstain
   ->  re-measure under the same declared setting  ->  report evidence and limits
```

### Proposed SOP taxonomy — `SOP/Trustworthy-ML-2023/`

| Artifact | Workflow stage | Concepts covered | Why this is the unit |
|---|---|---|---|
| `SOP-01-specify-deployment-setting.md` | declare the setting | C1, C2, C3 | Everything downstream is only comparable if the setting and the generalization-type claim are written down first. |
| `SOP-02-build-evaluation-splits-under-leakage-discipline.md` | freeze splits | C4, C5, C1(partial) | A single procedure owns split provenance, tuning rights and test-set budget; referenced by all other SOPs instead of being repeated. |
| `SOP-03-diagnose-learned-evidence.md` | diagnose | C6, C3, C15 | The cue-diagnosis procedure merges the counterfactual protocols of 2.10 with the attribution diagnostics of 3.7 — one workflow, two source areas. |
| `SOP-04-measure-confidence-truthfulness.md` | measure confidence | C7, C8, C9, C10, C12 | Choosing a contract, then applying anti-gaming checks, is one decision procedure. |
| `SOP-05-run-worst-case-stress-evaluation.md` | stress | C11, C12, C10, C14 | Adversarial and corruption stress share one structure: declare, attack with a reported configuration, check that the evaluation is not fooled. |
| `SOP-06-choose-mitigation-or-abstention.md` | mitigate / decline | C13, C16, C8, C14 | Resource-keyed decision table plus the rule that a mitigation re-opens evaluation, not closes it. |
| `SOP-07-evaluate-explanation-methods.md` | explain (and use explanations) | C17, C6, C9, C10 | Explanation methods are evaluated as instruments for an end goal; not a chapter echo of chapter 3's method catalogue. |
| `SOP-08-report-evidence-and-validity-boundaries.md` | report | C18, C15, C14 | Closing checklist that also carries the shared definition/metric glossary used by every other SOP. |

No SOP is named after a chapter; two of them (SOP-02, SOP-08) gather material that the book spreads
over three and five chapters respectively. Nothing in the book's chapter structure corresponds to
SOP-04 or SOP-05, both of which are keyed to a decision rather than a topic.

### Proposed Benchmark taxonomy — `Benchmark/Trustworthy-ML-2023/`

| Artifact | Capability under test | Condition axis | Concepts |
|---|---|---|---|
| `BM-01-distribution-shift-generalization.md` | does performance survive a changed domain / subpopulation | domain shift, subpopulation imbalance, scale regime | C1, C2, C15 |
| `BM-02-spurious-cue-dependence.md` | does the model depend on an evidence cue that breaks when the correlation breaks | diagonal / off-diagonal cue construction | C3, C6, C15 |
| `BM-03-confidence-truthfulness.md` | is the reported number a probability, a calibrated conditional, or an order | ID vs shifted, imbalance, ambiguity-rich subsets | C7, C8, C9, C10, C12 |
| `BM-04-error-and-anomaly-detection.md` | can the score tell right from wrong / in from out / single from multiple answers | error, OOD, multiplicity, corruption | C8, C9, C10 |
| `BM-05-adversarial-robustness.md` | worst-case behavior inside a declared strategy space | ε-ball, transform, black-box access, certification | C11, C12, C14 |
| `BM-06-explanation-quality.md` | does the explanation reflect the model, and does it help a human | randomization, simulated ground truth, occlusion, HITL | C17, C9, C10 |
| `BM-07-selective-prediction-under-cost.md` | does the system decline safely where it should | coverage thresholds, asymmetric cost, human budget | C16, C7, C14 |
| `BM-08-evaluation-integrity-audit.md` | is the comparison itself trustworthy (a benchmark over benchmarks) | any | C4, C5, C10, C14, C18 |

`BM-08` is where the book's two most transferable findings live (5.1.3 failure recipes and 5.2.2
simple-wins), and it is intentionally *not* a capability benchmark: it audits leakage, contamination,
unequal tuning, hidden resources, shared metric implementations, and cost disclosure. Core / Extended
tiers are defined inside each spec rather than as separate files, except in BM-01 and BM-05 where the
stress construction differs enough to warrant an explicit split inside the document.

Dimensions from the reading list that were **considered and shaped**: computational cost became a
mandatory field of every benchmark plus BM-08/BM-07 content rather than its own file (avoiding
duplication with SOP-08); explainability-related evaluation was kept because it is operationally
justified (3.7 has protocols and metrics, not just aspiration); subgroup / worst-case behavior
became a cross-cutting requirement inside BM-01/BM-02/BM-03 rather than a separate benchmark, since
the source supports it as a *view* on existing metrics (2.12.1, 4.6.2).

---

## Step 4 — Provenance of the rules the artifacts will state

`source-derived` = the book states it; `synthesized` = reconstructed from several source points;
`repository convention` = our operational addition, not a claim by the book.

| Rule as it will appear | Provenance | Anchor |
|---|---|---|
| A setting must enumerate dev resources, deployment distribution, and time; methods with different resources are not comparable | source-derived | Def 2.18 + 2.3.1 "How to compare methods…" (p. 25) |
| Allowing extra ingredients turns a benchmark into an unfair comparison | source-derived | 5.3.1 (pp. 342-343) |
| Tuning on target-domain data — even visually, even unlabeled — changes the setting: the "domain generalization" label is void and the work is a different problem with its own comparison class, not a failed project | source-derived | 2.5.1 Scenarios 1-3 (pp. 36-37) |
| Integrity is defined by the information rights the declared setting grants, so adaptation settings (domain adaptation, test-time training, continual, K-shot) are legitimate as declared | source-derived (setting catalogue) + synthesized (rights formulation) | 2.4.2-2.4.11 (pp. 29-35), 2.5.1 (pp. 36-37) |
| A contaminated final test cannot be repaired by rerunning it; obtain a new untouched set, use a secondary one, or downgrade and disclose | synthesized from the spoiling spectrum | 2.3.3 (p. 28), 2.5.3 (pp. 39-40) |
| Split by the highest relevant independence unit; a random split is valid when rows really are IID for the claim | synthesized (the source argues the grouped case only) | 2.3.2 (p. 26), 5.1.3 (pp. 335-338) |
| A counterfactual edit evidences sensitivity under its intervention assumptions; the source's own ingredient "cue disentanglement" is the identification condition for the stronger causal reading, which is kept only where construction meets it | source-derived (recipes, decision directions) + synthesized (verdict calibration) | 2.10 (pp. 55-56) |
| Mitigation choice is admissibility plus declared objective, not a routing table; the sub-1 % unbiased figure is the source's experimental regime, not a general threshold | source-derived (scenarios) + synthesized (decision form) | 2.11-2.14 (pp. 57-85), 2.13.2 (pp. 70-75) |
| A tuned simple baseline is a required reference row, not an automatic winner; conflicting objectives compare by Pareto domination or constraint form | synthesized from the source's fairly-tuned-ERM finding | 5.2.2, 5.2.3 (pp. 339-342) |
| Abstention is admissible only with a validated selection signal, a measured risk/cost-coverage relation and a resourced fallback; otherwise report "no validated action policy" | synthesized from the source's cost-table rule | 4.1.3 (pp. 223-228), 4.9.1 (pp. 263-264) |
| Under one model, test set, threat model and valid implementations, **certified robust accuracy ≤ exact finite-sample robust accuracy ≤ empirical attacked accuracy under attack suite A**; a certificate row is a lower bound on the target and an attacked row is an observation, so neither alone settles the worst case | synthesized — the source reports the certified and attacked rows separately and never orders them | 2.15.3-2.15.4 (pp. 89-92), 2.15.15 (pp. 111-113) |
| The two-layer/binary conditions in §2.15.15 scope *that construction*, not certified robustness as a field; the certificate family actually used must state its own assumptions, and a valid certificate is a lower bound on true robust accuracy for its threat model, not an upper-bound row | source-derived (the limits) + synthesized (the scope reading) | 2.15.15, Definition 2.47 (pp. 111-113) |
| Attack adequacy is argued against threat model and defense — adaptive, complementary configurations — not inferred from iteration count; strongest affordable PGD is a floor | source-derived (ladder, masking) + synthesized (adequacy rule) | 2.15.2-2.15.4 (pp. 89-92), 2.15.12 (pp. 102-107) |
| Train-time transform exposure is required only where the defense's definition needs it; attacking the joint pipeline adaptively is required always | synthesized from the masking and transform discussion | 2.15.12-2.15.14 (pp. 102-110) |
| Pretraining exposure is disclosed by kind (semantic/class exposure, duplicate exposure, benchmark-specific adaptation), and whether an experiment counts as "zero-shot" follows the definition used by the benchmark or study, not a repository-wide rule; the earlier four-level ladder was dropped because it imposed one | synthesized from the source's single remark | 2.5.1 (p. 37) |
| Use the held-out test set sparingly; once per paper is the book's own rule of thumb | source-derived | 2.5.3 (p. 39) |
| Publish a ranking instead of scores to slow test-set spoiling | source-derived (as a suggestion) | 2.5.1 fn. 7 (p. 36) |
| Reporting a proper-scoring number alone cannot separate calibration from accuracy | source-derived | 4.5.9 remarks 3-4 (p. 254) |
| A constant confidence equal to the measured correctness rate reaches ECE = 0 without truthfulness; it is an oracle diagnostic because that constant is computed from the scored set's labels | source-derived (degeneracy) + synthesized (oracle labeling) | 4.6.2 (pp. 256-257) |
| A constant frozen on the calibration split is a legitimate baseline, but its final ECE is the gap to final accuracy | synthesized | 4.6.2 (pp. 256-257) |
| Fix the number of ECE bins and report it; consider finer bins at high confidence | source-derived (bin sensitivity) + repository convention (make disclosure mandatory) | 4.6.2 (pp. 256-257) |
| Perplexity is the exponentiated NLL and must share that NLL's logarithm base; the value is invariant to a *common* base | source-derived, incl. fn. 18 | 4.5.9 (p. 252) |
| Prefer AUROC over AUPR when the relevant positive rate is far from 0.5; report both curves anyway | source-derived (AUROC recommendation) + synthesized (report-both) | 4.9.2 (pp. 265-266) |
| The no-skill value of a PR area is the prevalence of the designated positive, so `aupr_success` and `aupr_error` have different baselines; every ranking number names its positive class | synthesized from the source's success-positive value and its class-swap definition of AUPR-Error | 4.9.2 (pp. 265-266) |
| Epistemic uncertainty and OOD-detection performance are related but not interchangeable | source-derived | 4.3.1 (p. 239), 4.12.3 (p. 297) |
| Distance-based confidence conflates OOD-ness with aleatoric ambiguity; do not read it as pure epistemic | source-derived | 4.12.1-4.12.2 (p. 292-296) |
| Attack strength must be reported as a configuration; a single-attack evaluation underestimates the attack | source-derived (FGSM < PGD reasoning, ε policy) | 2.15.2-2.15.4 (p. 89-92) |
| A defense that breaks gradients can look robust; run the progression of attacks before believing high robust accuracy | source-derived | 2.15.12 (pp. 102-107) |
| Certified and empirical robustness are different claims; post-hoc certificates may be arbitrarily loose | source-derived | 2.15.15 (p. 110-113) |
| Tuning is a shared budget, and an untuned baseline invalidates the ranking | source-derived | 5.2.2 (pp. 62-341), 2.12.2 (p. 64) |
| Random search over sensible exponential ranges with a fixed shared sample count | source-derived | 5.2.3 (pp. 341-342) |
| Report compute alongside accuracy; accuracy-only plots hide the decisive axis | source-derived | 5.1.3 (pp. 335-338) |
| Explanations must not be judged by human plausibility alone | source-derived | 3.7.3 (p. 179-181) |
| Occlusion choice is a hyperparameter of the soundness metric, not a detail | source-derived | 3.7.7-3.7.8 (p. 186-188) |
| Ground-truth explanations do not exist in general; use proxies and say so | source-derived | 3.7.3 (p. 181) |
| **Ordering**: declare the setting before choosing metrics, and re-evaluate after mitigation | synthesized | C1 → C18 chain; 2.11's resource-keyed scenarios; 2.5.1 "treat it as a new setting" |
| **Core / Extended tiering** of every SOP and benchmark | synthesized | 4.6.2 (MCE for high-risk), 5.2 (toy vs real regimes), 2.12.1 vs 2.13 (supervision availability) |
| **Worst-case views as a standing requirement** rather than an optional extra | synthesized | 2.12.1 worst-group, 4.6.2 MCE, 2.6 Def 2.26 |
| Splitting "confidence truthfulness" (BM-03) from "detection quality" (BM-04) into two benchmarks | synthesized | 4.7 vs 4.9-4.10 |
| Making an integrity audit itself a benchmark artifact (BM-08) | synthesized | 2.3.3 + 2.5 + 5.1.3 + 5.2.2 |
| SOP numbering, ID scheme, mandatory 12-section SOP schema, 13-section benchmark schema, cross-link matrix, check/stop-condition vocabulary | repository convention | from the plan files, not the book |
| Concrete pass/fail thresholds, bin defaults, iteration budgets, and any numerical "good" value not quoted above | repository convention or absent | the book gives none; do not present invented numbers as the book's |

---

## Gate B — Reconstruction

| Condition | Result | Evidence in this file |
|---|---|---|
| Final taxonomy does not mirror book chapter order | PASS | Chapter 2 → C1-C6, C13, C15 (split across SOP-01/02/03/06 and BM-01/02/08); chapter 3 → C6, C17 (SOP-07, BM-06); chapter 4 → C7-C10, C16 (SOP-04, BM-03/04/07); chapter 5 → C4, C10, C14, C18 (SOP-08, BM-08). No artifact corresponds to one chapter. |
| Artifact names are task/capability oriented | PASS | All 8 SOP and 8 benchmark names are verbs/capabilities (`specify-deployment-setting`, `spurious-cue-dependence`), none is a chapter rename. |
| Major concepts synthesize multiple source sections where appropriate | PASS | 15 of 20 concepts draw on ≥3 sections; C4, C10, C14, C18 draw on sections from three or more chapters (Step 1 table). |
| Source-to-concept traceability preserved | PASS | Every concept row lists contributing sections with definition numbers; Step 4 lists rule-level anchors with page numbers; coverage dispositions in `source_coverage.md`. |
| Methods, metrics, capabilities and failure modes are not collapsed into one axis | PASS | Step 2 keeps eight separate axes, with five named deliberate separations and the reason for each. |

**Gate B result: PASS.** The taxonomy below is what Plans 3 and 4 must implement; any deviation
discovered while writing an artifact must be brought back to this file.
