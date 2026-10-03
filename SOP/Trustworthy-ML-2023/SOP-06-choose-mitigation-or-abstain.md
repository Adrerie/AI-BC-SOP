# SOP-06 — Choose a mitigation, or choose to abstain

**Stage:** mitigate / decline · **Tier:** Core + Extended · **Concepts:** C13 admissibility,
C16 selective action, C8 quantity, C14 cost

## 1. Purpose

Select an intervention that is *admissible for the supervision you actually have*. Verify that the
intervention changed the failure you targeted, not the metric you watch. When no intervention is
admissible, convert the situation into a defensible abstention policy instead of a silent failure.

## 2. When to use

- After [`SOP-03`](SOP-03-diagnose-learned-evidence.md) identifies a dependence you cannot accept,
  or [`SOP-04`](SOP-04-measure-confidence-truthfulness.md) shows the confidence is not usable.
- Before committing to a method choice on the basis of published rankings.
- Whenever the marginal gain of a complicated method over a simple one is being argued.
- When the honest answer to the deployment question may be "decline to answer".

## 3. Inputs / prerequisites

- The setting block and the cue whitelist, the diagnosis verdicts, and the confidence battery.
- Label inventory: which group/attribute/domain labels exist, and the unbiased-sample fraction ρ.
- Retraining budget. A mitigation is a training-time intervention. Measure the budget for that
  intervention.
- An untouched evaluation configuration from
  [`SOP-02`](SOP-02-build-evaluation-splits-under-leakage-discipline.md) so before/after numbers are
  comparable.
- For abstention: the cost table of wrong actions (see §4).

## 4. Definitions needed for execution

- **Admissible mitigation** — an intervention whose required ingredients your setting grants.
  Admissibility, not popularity, decides the candidate list.
- **Resource-keyed scenarios** — the three supervision regimes the source distinguishes:
  - (S1) abundant biased samples plus a small amount of *labeled* unbiased samples
  - (S2) essentially no unbiased supervision and no bias labels. An assumption about which cue a
    limited model learns first must carry the weight in this regime.
  - (S3) a small *labeled sample from the deployment distribution*, available at decision time
- **Intentionally biased / myopic model** — a deliberately handicapped model (few epochs, small
  receptive field, single modality) used to expose which cue the easy solution is.
- **"Be different" supervision** — regularising the final model away from the biased one, via sample
  weighting or a representation-independence penalty.
- **Worst-group objective** — minimize the maximum loss over groups rather than the average loss. The
  objective trades average accuracy for the minimum cell.
- **Abstention / selective prediction** — declining to answer above a confidence or coverage
  constraint. The operating point, not the score, is the decision.
- **Cost table** — the expected-loss matrix over (predicted class × true class × abstain), which is
  what turns a confidence number into an action.

## 5. Procedure

**Core**

1. Enumerate candidate mitigations by admissibility. The list below is a set of **worked examples
   keyed to ingredients**, not a routing table. The same ingredient can admit several methods. Choose
   among those methods on the declared objective, on the assumptions each method needs, and on the
   costs. For every candidate, make these records in the admissibility table of §9. Record the required
   supervision, the assumption, and the objective that the method optimizes. Record the
   compute/label/human cost, the expected trade-off, and the benchmark that evaluates the intended
   improvement.
   - domain labels available → domain-adversarial alignment, off-diagonal up-weighting. *Group* or
     *attribute* labels are not domain labels. A worst-group objective needs the groups to be the
     units whose minimum risk you care about. Domain-adversarial alignment needs the labels to index
     distributions that you expect to shift. If your labels are one kind, do not spend that kind as
     the other kind.
   - group labels tied to a declared worst-cell objective → worst-group / distributionally-robust
     training. Accept the average-case cost that the source documents.
   - essentially no unbiased supervision, with the "easy cue first" assumption testable in your data
     → biased-model contrast ("be different") methods. The source studies that regime at very small
     unbiased fractions, at or below about 1 % in its ρ sweeps. Those numbers describe the
     *experimental regime* of those sweeps. They are not a threshold that decides when the family
     applies.
   - a labeled sample from the deployment distribution available at decision time → diverse-ensemble
     plus test-time selection. State the oracle-selection caveat with that result.
   - confidence is the problem, decisions are fine → post-hoc recalibration.
   - adversarial strategy space declared → adversarial training
     ([`SOP-05`](SOP-05-run-worst-case-stress-evaluation.md)).
   - nothing admissible → step 6. "Abstain" is itself admissible only if its prerequisites hold. If
     one prerequisite does not hold, the output is "no validated action policy".
2. Establish the **tuned simple baseline first**. Train the plainest admissible method with the same
   tuning budget as every candidate. Measure every candidate against this reference, not against a
   default-settings straw man. The reference is a necessary comparison point. The reference is not an
   automatic winner (see §7).
3. Re-run the *whole* evaluation battery on the mitigated model with the configuration unchanged.
   Include the task metrics, the worst-group view, the confidence battery, and the diagnosis of
   `SOP-03`. A mitigation reported only through the metric that the mitigation targets is not tested.
4. Record side effects explicitly:
   - the average-accuracy cost of a worst-group objective
   - the coverage loss from abstention
   - the inference overhead
   - the added hyper-parameters
   - the label cost incurred to obtain the mitigation's supervision
5. Test the assumption that the mitigation rests on. Report the result of that test as pass/fail. For
   contrast-style methods, check that the handicapped model really learned the cue you call the bias.
   If you swap the roles and the method degrades, name the assumption as the failure. Do not blame an
   unlucky baseline.
6. Treat the **abstention branch** as a policy, not as a default. Abstention is available only when
   each item below has its own established evidence. If one item is missing, the honest output is "no
   validated action policy". That output is not the same act as abstaining. The items are:
   - An informative selection signal exists. Its ranking or calibration is validated on permitted
     material for this use (`SOP-04`, `BM-03`).
   - A risk-coverage or cost-coverage relation is *measured* over the deployment distribution, and not
     assumed from the ID subset.
   - The operating point is chosen on that curve against the cost table, and not on a raw score
     threshold.
   - A fallback path exists and has capacity. The capacity can be human review, a re-ask for better
     input, or a safe state. Name the cost of that fallback and its owner.
   - The coverage you accept is stated. The residual risk at that coverage is stated.
7. Decide on the outcome. Record which of these four outcomes applies:
   - **mitigated-and-verified**
   - **abstain above coverage X**, with the five items above satisfied
   - **no admissible mitigation**
   - **no validated action policy**
   Record the reasons for the last two outcomes. Those reasons make a refusal to act distinguishable
   from an untested intention to act.

**Extended** — add for publication-grade or safety-relevant work:

8. Add a ladder of escalating interventions. The ladder is re-weight → align → relabel/add supervision
   → change the setting. Stop at the first intervention that meets the requirement. Justify each
   promotion by a measured failure of the previous intervention.
9. Cost the extra supervision explicitly where that supervision is the only route. Acquiring attribute
   labels or unbiased samples is a *setting change*. The comparison class changes with that change.
10. Add a robustness-to-ρ study. Repeat the mitigation at several unbiased fractions. Report the
    fraction at which the mitigation stops working. That report is the honest form of the question
    "how much supervision did this need?".
11. Add a re-deployment clause. State what monitoring cadence the residual failure rate implies, and
    what retraining cadence that rate implies. Constant retraining is the normal industry response to
    drift.

## 6. Mandatory checks

- [ ] **Admissibility audit**: every candidate's required ingredient is present in the setting block.
      No candidate relies on data that you do not have.
- [ ] **Equal tuning budget** between the simple baseline and every candidate, with the search space
      and sample count reported.
- [ ] **Setting-drift check**: if the mitigation used target-domain information, reclassify the result
      to that stronger setting. Do not compare that result against the original class.
- [ ] **Full-battery re-evaluation** after mitigation, with the pre-mitigation configuration restored.
- [ ] **Assumption test recorded** for every method that depends on one (easy-cue-first, myopia,
      posterior family, separability).
- [ ] **Cost parity**: added compute, memory, label and human cost are reported next to the gain.
- [ ] **Abstention prerequisites all present**. If one prerequisite is missing, record the result as
      "no validated action policy", not as an abstention policy. The four prerequisites are:

    - an informative score, validated for this use
    - a measured risk-coverage or cost-coverage relation
    - an operating point chosen from that relation against the cost table
    - a fallback path with named capacity, cost and owner
- [ ] **Abstention operating point justified by the cost table**, not by a convention such as 0.9.

## 7. Decision or stop conditions

- **Stop: no admissible mitigation** if the setting grants neither bias labels, nor unbiased samples,
  nor deployment labels. Four outputs are defensible there:
  - a validated abstention (step 6)
  - a change of setting, with its cost
  - an explicit statement that available resources do not remove the dependence
  - "no validated action policy", when even abstention lacks its prerequisites
- **Do not reject a candidate merely because that candidate loses to the tuned simple baseline on
  average accuracy.** The baseline is a required reference and an efficiency check. The baseline is not
  an automatic winner. A candidate is admissible to keep if the candidate improves one axis that the
  declared objective requires. Those axes are worst-group risk, calibration, robustness, coverage at
  risk, compute, memory, latency, and annotation cost. Keeping such a candidate means a stated
  trade-off elsewhere. When objectives conflict, compare the candidates by Pareto domination, or by
  the constraint form "meets the requirement at least cost". Record which comparison rule you used.
  Drop a candidate that is dominated on every declared axis and that costs more.
- **Stop and go back to `SOP-01`** if the mitigation succeeded by changing what the task means
  (for example by exploiting an attribute label that the deployment will not provide).
- **Escalate to the abstention branch** when the residual worst-cell risk exceeds the tolerated risk
  even after mitigation. Escalate only to *validated* abstention. If the prerequisites in step 6 do
  not hold, report the absence of a validated action policy instead.

## 8. Common methodological failures

- The evaluation beats an untuned baseline. The delta is then published as the method's contribution.
- The tuning of the mitigation's hyper-parameters silently uses target-domain information.
- The report gives only the improved cell, and hides the average-accuracy cost.
- A worst-group objective is treated as strictly better than average-risk training.
- A contrast method is applied in a domain where its "easy cue first" assumption was never checked.
- The abstention threshold is chosen by habit. The resulting coverage is then presented as capability.
- "Abstain" is treated as the inherently safe default when no validated selection signal and no
  staffed fallback exist. That treatment converts an unmeasured policy into the appearance of one.
- The routing decision uses a numeric regime taken from a single source experiment, as though that
  regime were a general admissibility threshold.
- A candidate that improves the axis the objective requires is discarded, because that candidate loses
  the average-accuracy comparison.
- A method is adopted whose extra supervision nobody can afford to collect at scale.

## 9. Required outputs

- Admissibility table. One entry per candidate, with these fields:
  - candidate
  - required supervision
  - whether that ingredient is present
  - assumption the method relies on
  - objective the method optimizes
  - compute / label / human cost
  - expected trade-off
  - the benchmark that will verify the intended improvement
- Tuned-simple-baseline result and the shared search configuration.
- Before/after full-battery table, per metric, including worst cell.
- Assumption test report.
- If abstaining: cost table, chosen risk-coverage point, coverage, residual risk, fallback path with
  its capacity and cost, and the owner. Or a written "no validated action policy" that names the
  missing prerequisite.
- Decision record with the reason, the comparison rule used (Pareto or constraint form), and the
  setting (original or stronger) the result belongs to.

## 10. Minimum reporting requirements

State each of these items:

- which supervision the mitigation consumed
- the tuning budget that each compared method received
- the average *and* worst-cell results before and after
- the assumption you tested, and the outcome of that test
- the added cost in compute and labels

If a stronger setting was used, name that setting. Keep that setting in a separate table from the
results of the original setting.

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

- Scenario-keyed admissibility and the up-weight-off-diagonal option: §2.11-§2.12 (pp. 57-59).
- Worst-group objective, its algorithm and the average-versus-worst-group trade-off: §2.12.1,
  Definition 2.30 (pp. 59-61).
- Domain-adversarial objective and its label encodings, and the reproduced "no significant difference"
  comparison: §2.12.2 (pp. 62-65).
- Missing-bias-label regime, intentionally biased and myopic model definitions, "be different"
  supervision: §2.13, Definitions 2.31-2.33 (pp. 65-66, 74-75).
- Contrast methods' documented failure when task and bias roles are swapped: §2.13.1 (pp. 67-70).
- Dual biased/unbiased evaluation sets and the ρ sweep: §2.13.2 (pp. 70-75).
- Deployment-label regime, test-time selection, and the diversity-by-orthogonal gradients construction
  with its oracle-selection caveat: §2.14-§2.14.1 (pp. 75-85).
- The sub-1 % unbiased fraction in step 1 is the regime the source's own ρ sweep studies
  (§2.13.2, pp. 70-75). That fraction is reported here as an experimental condition, and not as a
  decision threshold.
- Retraining and model-selection cadence as an engineering cost: §2.2.1-§2.2.2 (pp. 20-24),
  Definitions 2.9-2.11.
- Recalibration as a cheap confidence fix: §4.8.3 (pp. 262-263).
- Cost table with abstention preferred over an asymmetric error, and the confidence-threshold
  acceptance rule: §4.1.3 (pp. 223-228).
- The sufficiency of ranking for threshold filtering: §4.9.1 (pp. 263-264).
- "Fairly tuned ERM is not worse", the untuned-baseline pathology and the weight-decay example:
  §5.2.2 (pp. 339-341).
- Shared random-search budget: §5.2.3 (pp. 341-342).
- Toy-versus-real cost of validating complicated methods: §5.2 (pp. 338-340).
- Extra supervision as the scalable direction and the information cap of a fixed benchmark:
  §5.3-§5.3.5 (pp. 342-350).
- The admissibility table format and the escalation ladder are repository conventions.

Three further items are **synthesized** rather than quoted:

- the Pareto or constraint form of the baseline comparison. The source shows that a fairly tuned
  simple method was not worse *in one study* (§5.2.2, pp. 339-341). That result licenses the reference
  row. It does not license the rejection of a candidate that wins a different declared axis.
- the five abstention prerequisites, which turn the source's cost-table-and-threshold recipe
  (§4.1.3, pp. 223-228) into an admissibility test for the fallback itself.
- the caution that group or attribute labels are not domain labels. §2.12.1 and §2.12.2 give those two
  label kinds different roles, and that difference is where the caution comes from.
