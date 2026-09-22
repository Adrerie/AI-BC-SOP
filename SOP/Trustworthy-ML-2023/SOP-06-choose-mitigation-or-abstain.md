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
  (S1) abundant biased samples plus a small amount of *labeled* unbiased samples; (S2) essentially
  no unbiased supervision and no bias labels, so an assumption about which cue a limited model
  learns first must carry the weight; (S3) a small *labeled sample from the deployment
  distribution* available at decision time.
- **Intentionally biased / myopic model** — a deliberately handicapped model (few epochs, small
  receptive field, single modality) used to expose which cue the easy solution is.
- **"Be different" supervision** — regularising the final model away from the biased one, via sample
  weighting or a representation-independence penalty.
- **Worst-group objective** — minimize the maximum loss over groups rather than the average loss;
  trades average accuracy for the minimum cell.
- **Abstention / selective prediction** — declining to answer above a confidence or coverage
  constraint; the operating point, not the score, is the decision.
- **Cost table** — the expected-loss matrix over (predicted class × true class × abstain), which is
  what turns a confidence number into an action.

## 5. Procedure

**Core**

1. Enumerate candidate mitigations by admissibility. The list below is a set of **worked examples
   keyed to ingredients**, not a routing table: the same ingredient can admit several methods, and the
   choice among them is made on the declared objective, the assumptions each needs, and the costs.
   For every candidate record, in the admissibility table of §9, its required supervision, its
   assumption, the objective it optimizes, its compute/label/human cost, the trade-off it is expected
   to impose, and which benchmark evaluates the intended improvement.
   - domain labels available → domain-adversarial alignment, off-diagonal up-weighting. Note that
     *group* or *attribute* labels are not domain labels: a worst-group objective needs the groups to
     be the units whose minimum risk you care about, while alignment needs them to index
     distributions you expect to shift. If your labels are one kind, do not spend them as the other.
   - group labels tied to a declared worst-cell objective → worst-group / distributionally-robust
     training, accepting the average-case cost the source documents.
   - essentially no unbiased supervision, with the "easy cue first" assumption testable in your data
     → biased-model contrast ("be different") methods. The source studies this regime at very small
     unbiased fractions — at or below about 1 % in its ρ sweeps — which is the *experimental regime*
     those numbers come from, not a threshold that decides when the family applies.
   - a labeled sample from the deployment distribution available at decision time → diverse-ensemble
     plus test-time selection, with the oracle-selection caveat stated.
   - confidence is the problem, decisions are fine → post-hoc recalibration.
   - adversarial strategy space declared → adversarial training
     ([`SOP-05`](SOP-05-run-worst-case-stress-evaluation.md)).
   - nothing admissible → step 6, and note that "abstain" is admissible only if its own
     prerequisites hold; otherwise the output is "no validated action policy".
2. Establish the **tuned simple baseline first**: train the plainest admissible method with the same
   tuning budget as every candidate. Every candidate is measured against this reference, not against a
   default-settings straw man — and the reference is a necessary comparison point, not an automatic
   winner (see §7).
3. Re-run the *whole* evaluation battery on the mitigated model with the configuration unchanged:
   task metrics, worst-group view, confidence battery, and the diagnosis of
   `SOP-03`. A mitigation that is only reported through the metric it targets has not been tested.
4. Record side effects explicitly: average accuracy cost of a worst-group objective, coverage loss
   from abstention, inference overhead, added hyper-parameters, and label cost incurred to obtain
   the mitigation's supervision.
5. Test the assumption the mitigation rests on, and report it as pass/fail: for contrast-style
   methods, check that the handicapped model really learned the cue you call the bias; if roles are
   swapped and the method degrades, that is the assumption failing, not the baselines being unlucky.
6. **Abstention branch** — a policy, not a default. Abstention is available only when all of these
   have themselves been established; if any is missing, the honest output is "no validated action
   policy", and saying that is not the same as abstaining:
   - an informative selection signal exists, and its ranking or calibration has been validated on
     permitted material for this use (`SOP-04`, `BM-03`);
   - a risk-coverage or cost-coverage relation has been *measured* over the deployment distribution,
     not assumed from the ID subset;
   - the operating point is chosen on that curve against the cost table, rather than on a raw score
     threshold;
   - a fallback path exists and has capacity — human review, re-ask for better input, or a safe state
     — with its cost and its owner named;
   - the coverage you accept and the residual risk at that coverage are stated.
7. Decide and record one of: **mitigated-and-verified**, **abstain above coverage X** (with the five
   items above satisfied), **no admissible mitigation**, or **no validated action policy** — the last
   two with their reasons, so that a refusal to act is distinguishable from an untested intention to
   act.

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
- [ ] **Abstention prerequisites all present**: an informative score that was validated for this use,
      a measured risk-coverage or cost-coverage relation, an operating point chosen from it against
      the cost table, and a fallback path with named capacity, cost and owner. If any is missing, the
      result is recorded as "no validated action policy", not as an abstention policy.
- [ ] **Abstention operating point justified by the cost table**, not by a convention such as 0.9.

## 7. Decision or stop conditions

- **Stop: no admissible mitigation** if the setting grants neither bias labels, nor unbiased samples,
  nor deployment labels. The defensible outputs are a validated abstention (step 6), a change of
  setting with its cost, an explicit statement that the dependence cannot be removed with available
  resources, or "no validated action policy" when even abstention lacks its prerequisites.
- **Do not reject a candidate merely because it loses to the tuned simple baseline on average
  accuracy.** The baseline is a required reference and an efficiency check, not an automatic winner:
  a candidate is admissible to keep if it improves an axis the declared objective requires — worst-group
  risk, calibration, robustness, coverage at risk, compute, memory, latency, annotation cost — while
  accepting a stated trade-off elsewhere. When objectives conflict, compare by Pareto domination or by
  the constraint form ("meets the requirement at least cost"), and record which was used. A candidate
  that is dominated on every declared axis and costs more is the one to drop.
- **Stop and go back to `SOP-01`** if the mitigation succeeded by changing what the task means
  (for example by exploiting an attribute label that the deployment will not provide).
- **Escalate to the abstention branch** when the residual worst-cell risk exceeds the tolerated risk
  even after mitigation — and only to *validated* abstention: if step 6's prerequisites do not hold,
  report the absence of a validated action policy instead.

## 8. Common methodological failures

- Beating an untuned baseline and publishing the delta as the method's contribution.
- Silently using target-domain information to select the mitigation's hyper-parameters.
- Reporting only the improved cell and hiding the average-accuracy cost.
- Treating a worst-group objective as strictly better than average-risk training.
- Applying a contrast method in a domain where its "easy cue first" assumption was never checked.
- Choosing the abstention threshold by habit and then presenting the resulting coverage as capability.
- Treating "abstain" as the inherently safe default when no validated selection signal and no staffed
  fallback exist: that converts an unmeasured policy into the appearance of one.
- Routing on a numeric regime taken from a single source experiment as though it were a general
  admissibility threshold.
- Discarding a candidate that improves the axis the objective requires because it loses the
  average-accuracy comparison.
- Adopting a method whose extra supervision nobody can afford to collect at scale.

## 9. Required outputs

- Admissibility table: candidate × required supervision × is that ingredient present? × assumption it
  relies on × objective it optimizes × compute / label / human cost × expected trade-off × the
  benchmark that will verify the intended improvement.
- Tuned-simple-baseline result and the shared search configuration.
- Before/after full-battery table, per metric, including worst cell.
- Assumption test report.
- If abstaining: cost table, chosen risk-coverage point, coverage, residual risk, fallback path with
  its capacity and cost, and the owner; or a written "no validated action policy" naming which
  prerequisite was missing.
- Decision record with the reason, the comparison rule used (Pareto or constraint form), and the
  setting (original or stronger) the result belongs to.

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
- [`BM-04`](../../Benchmark/Trustworthy-ML-2023/BM-04-error-and-anomaly-detection.md) — whether the
  mitigation restored the system's ability to notice its own failures.
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
gradients construction with its oracle-selection caveat: §2.14-§2.14.1 (pp. 75-85). The sub-1 %
unbiased fraction in step 1 is the regime the source's own ρ sweep studies (§2.13.2, pp. 70-75),
reported here as an experimental condition rather than as a decision threshold. Retraining and
model-selection cadence as an engineering cost: §2.2.1-§2.2.2 (pp. 20-24), Definitions 2.9-2.11.
Recalibration as a cheap confidence fix: §4.8.3 (pp. 262-263). Cost table with abstention preferred
over an asymmetric error, and the confidence-threshold acceptance rule: §4.1.3 (pp. 223-228).
Ranking being sufficient for threshold filtering: §4.9.1 (pp. 263-264). "Fairly tuned ERM is not
worse", the untuned-baseline pathology and the weight-decay example: §5.2.2 (pp. 339-341). Shared
random-search budget: §5.2.3 (pp. 341-342). Toy-versus-real cost of validating complicated methods:
§5.2 (pp. 338-340). Extra supervision as the scalable direction and the information cap of a fixed
benchmark: §5.3-§5.3.5 (pp. 342-350). Admissibility table format and the escalation ladder are
repository conventions. Three further items are **synthesized** rather than quoted: the Pareto or
constraint form of the baseline comparison, since the source shows a fairly tuned simple method was
not worse *in one study* (§5.2.2, pp. 339-341), which licenses the reference row but not the rejection
of a candidate that wins a different declared axis; the five abstention prerequisites, which turn the
source's cost-table-and-threshold recipe (§4.1.3, pp. 223-228) into an admissibility test for the
fallback itself; and the caution that group or attribute labels are not domain labels, which follows
from the different roles §2.12.1 and §2.12.2 give them.
