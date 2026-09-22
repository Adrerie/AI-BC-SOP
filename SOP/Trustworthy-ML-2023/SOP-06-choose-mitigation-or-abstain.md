# SOP-06 — Choose a mitigation, or choose to abstain

**Stage:** mitigate / decline · **Tier:** Core + Extended · **Concepts:** C13 admissibility,
C16 selective action, C8 quantity, C14 cost

## 1. Purpose

Select an intervention that is *admissible for the supervision you actually have*, verify that it
changed the failure you targeted rather than the metric you were watching, and — when no
intervention is admissible — convert the situation into a defensible abstention policy instead of a
silent failure.

## 2. When to use

- After [`SOP-03`](SOP-03-diagnose-learned-evidence.md) identifies a dependence you cannot accept,
  or [`SOP-04`](SOP-04-measure-confidence-truthfulness.md) shows the confidence is not usable.
- Before committing to a method choice on the basis of published rankings.
- Whenever the marginal gain of a complicated method over a simple one is being argued.
- When the honest answer to the deployment question may be "decline to answer".

## 3. Inputs / prerequisites

- Setting block and cue whitelist; diagnosis verdicts; the confidence battery.
- Label inventory: which group/attribute/domain labels exist, and the unbiased-sample fraction ρ.
- Retraining budget (a mitigation is a training-time intervention; measure it as one).
- An untouched evaluation configuration from
  [`SOP-02`](SOP-02-build-evaluation-splits-under-leakage-discipline.md) so before/after numbers are
  comparable.
- For abstention: the cost table of wrong actions (see §4).

## 4. Definitions needed for execution

- **Admissible mitigation** — an intervention whose required ingredients your setting grants.
  Admissibility, not popularity, decides the candidate list.
- **Resource-keyed scenarios** — the three supervision regimes the source distinguishes:
  (S1) abundant biased samples plus a small amount of *labelled* unbiased samples; (S2) essentially
  no unbiased supervision and no bias labels, so an assumption about which cue a limited model
  learns first must carry the weight; (S3) a small *labelled sample from the deployment
  distribution* available at decision time.
- **Intentionally biased / myopic model** — a deliberately handicapped model (few epochs, small
  receptive field, single modality) used to expose which cue the easy solution is.
- **"Be different" supervision** — regularising the final model away from the biased one, via sample
  weighting or a representation-independence penalty.
- **Worst-group objective** — minimise the maximum loss over groups rather than the average loss;
  trades average accuracy for the minimum cell.
- **Abstention / selective prediction** — declining to answer above a confidence or coverage
  constraint; the operating point, not the score, is the decision.
- **Cost table** — the expected-loss matrix over (predicted class × true class × abstain), which is
  what turns a confidence number into an action.

## 5. Procedure

**Core**

1. Enumerate candidate mitigations by admissibility:
   - group/attribute labels available → worst-group objective; domain-adversarial alignment;
     off-diagonal up-weighting;
   - no bias labels, ≤1 % unbiased samples → biased-model contrast ("be different") methods, and
     only if the "easy cue first" assumption is testable in your data;
   - a few labelled deployment samples at decision time → diverse-ensemble plus test-time selection;
   - confidence is the problem, decisions are fine → post-hoc recalibration;
   - adversarial strategy space declared → adversarial training
     ([`SOP-05`](SOP-05-run-worst-case-stress-evaluation.md));
   - nothing admissible → abstention branch (step 6).
2. Establish the **tuned simple baseline first**: train the plainest admissible method with the same
   tuning budget as every candidate. Complicated candidates must beat this, not a default-settings
   straw man.
3. Re-run the *whole* evaluation battery on the mitigated model with the configuration unchanged:
   task metrics, worst-group view, confidence battery, and the diagnosis of
   `SOP-03`. A mitigation that is only reported through the metric it targets has not been tested.
4. Record side effects explicitly: average accuracy cost of a worst-group objective, coverage loss
   from abstention, inference overhead, added hyper-parameters, and label cost incurred to obtain
   the mitigation's supervision.
5. Test the assumption the mitigation rests on, and report it as pass/fail: for contrast-style
   methods, check that the handicapped model really learned the cue you call the bias; if roles are
   swapped and the method degrades, that is the assumption failing, not the baselines being unlucky.
6. **Abstention branch.** Build the cost table; choose the operating point on the risk-coverage
   curve of the ranking score rather than on a raw threshold; state the coverage you accept and the
   residual risk at it; define the fallback (human review, re-ask for better input, safe state) and
   who pays for it.
7. Decide and record: mitigated-and-verified, abstain-above-coverage-X, or no-admissible-action with
   the reason.

**Extended** — add for publication-grade or safety-relevant work:

8. Add a ladder of escalating interventions (re-weight → align → relabel/add supervision → change the
   setting) and stop at the first that meets the requirement; each promotion must be justified by a
   measured failure of the previous one.
9. Where extra supervision is the only route, cost it explicitly: acquiring attribute labels or
   unbiased samples is a *setting change*, and the comparison class changes with it.
10. Add a robustness-to-ρ study: repeat the mitigation at several unbiased fractions and report where
    it stops working; this is the honest form of the "how much supervision did this need" question.
11. Add a re-deployment clause: state what monitoring or retraining cadence the residual failure rate
    implies, since constant retraining is the normal industry response to drift.

## 6. Mandatory checks

- [ ] **Admissibility audit**: every candidate's required ingredient is present in the setting block;
      no candidate relies on data you do not have.
- [ ] **Equal tuning budget** between the simple baseline and every candidate, with the search space
      and sample count reported.
- [ ] **Setting-drift check**: if the mitigation used target-domain information, the result is
      reclassified to that stronger setting and no longer compared against the original class.
- [ ] **Full-battery re-evaluation** after mitigation, with the pre-mitigation configuration restored.
- [ ] **Assumption test recorded** for every method that depends on one (easy-cue-first, myopia,
      posterior family, separability).
- [ ] **Cost parity**: added compute, memory, label and human cost are reported next to the gain.
- [ ] **Abstention operating point justified by the cost table**, not by a convention such as 0.9.

## 7. Decision or stop conditions

- **Stop: no admissible mitigation** if the setting grants neither bias labels, nor unbiased samples,
  nor deployment labels. The defensible outputs are abstention, a change of setting with its cost, or
  an explicit statement that the dependence cannot be removed with available resources.
- **Reject the candidate** if it fails to beat the tuned simple baseline under equal budget — the
  recurring pattern in this literature is that fairly tuned simple methods are not worse.
- **Stop and go back to `SOP-01`** if the mitigation succeeded by changing what the task means
  (for example by exploiting an attribute label that the deployment will not provide).
- **Escalate to abstention** when the residual worst-cell risk exceeds the tolerated risk even after
  mitigation.

## 8. Common methodological failures

- Beating an untuned baseline and publishing the delta as the method's contribution.
- Silently using target-domain information to select the mitigation's hyper-parameters.
- Reporting only the improved cell and hiding the average-accuracy cost.
- Treating a worst-group objective as strictly better than average-risk training.
- Applying a contrast method in a domain where its "easy cue first" assumption was never checked.
- Choosing the abstention threshold by habit and then presenting the resulting coverage as capability.
- Adopting a method whose extra supervision nobody can afford to collect at scale.

## 9. Required outputs

- Admissibility table (candidate × required ingredient × present? × cost).
- Tuned-simple-baseline result and the shared search configuration.
- Before/after full-battery table, per metric, including worst cell.
- Assumption test report.
- If abstaining: cost table, chosen risk-coverage point, coverage, residual risk, fallback owner.
- Decision record with the reason and the setting (original or stronger) the result belongs to.

## 10. Minimum reporting requirements

State which supervision the mitigation consumed; the tuning budget each compared method received;
average *and* worst-cell results before and after; the assumption you tested and its outcome; and
the added cost in compute and labels. If a stronger setting was used, name it and keep it in a
separate table from the original setting's results.

## 11. Links to relevant Benchmarks

- [`BM-02`](../../Benchmark/Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md) — measures whether
  a mitigation removed the dependence rather than the symptom.
- [`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md) — the
  comparison class whose ranking a mitigation must beat.
- [`BM-03`](../../Benchmark/Trustworthy-ML-2023/BM-03-confidence-truthfulness.md) — recalibration
  and confidence-side effects.
- [`BM-07`](../../Benchmark/Trustworthy-ML-2023/BM-07-selective-prediction-under-cost.md) — the
  abstention branch.
- [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md) — equal-budget
  and setting-drift audit.

## 12. Source traceability

Scenario-keyed admissibility and the up-weight-off-diagonal option: §2.11-§2.12
(pp. 57-59). Worst-group objective, its algorithm and the average-versus-worst-group trade-off:
§2.12.1, Definition 2.30 (pp. 59-61). Domain-adversarial objective and its label encodings, and the
reproduced "no significant difference" comparison: §2.12.2 (pp. 62-65). Missing-bias-label regime,
intentionally biased and myopic model definitions, "be different" supervision: §2.13,
Definitions 2.31-2.33 (pp. 65-66, 74-75). Contrast methods' documented failure when task and bias
roles are swapped: §2.13.1 (pp. 67-70); dual biased/unbiased evaluation sets and the ρ sweep:
§2.13.2 (pp. 70-75). Deployment-label regime, test-time selection, and the diversity-by-orthogonal
gradients construction with its oracle-selection caveat: §2.14-§2.14.1 (pp. 75-85). Retraining and
model-selection cadence as an engineering cost: §2.2.1-§2.2.2 (pp. 19-24), Definitions 2.9-2.11.
Recalibration as a cheap confidence fix: §4.8.3 (pp. 264-265). Cost table with abstention preferred
over an asymmetric error, and the confidence-threshold acceptance rule: §4.1.3 (pp. 223-228).
Ranking being sufficient for threshold filtering: §4.9.1 (pp. 265-266). "Fairly tuned ERM is not
worse", the untuned-baseline pathology and the weight-decay example: §5.2.2 (pp. 341-343). Shared
random-search budget: §5.2.3 (p. 343). Toy-versus-real cost of validating complicated methods:
§5.2 (pp. 338-340). Extra supervision as the scalable direction and the information cap of a fixed
benchmark: §5.3-§5.3.5 (pp. 342-350). Admissibility table format and the escalation ladder are
repository conventions.
