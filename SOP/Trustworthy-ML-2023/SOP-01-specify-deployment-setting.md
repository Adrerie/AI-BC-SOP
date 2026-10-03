# SOP-01 — Specify the deployment setting before training

**Stage:** define the problem · **Tier:** Core + Extended · **Concepts:** C1 setting declaration,
C2 generalization-type axis, C3 cue whitelist

Shared terms have one definition, in
[`SOP-08-report-evidence-and-validity-boundaries.md`](SOP-08-report-evidence-and-validity-boundaries.md).
This document defines only the terms that this procedure needs.

## 1. Purpose

Produce a written, checkable statement. The statement says what the experiment may know and what
the experiment claims to survive. Two results follow: (a) later numbers mean something, and (b)
any comparison with other work is between equal ingredients. Silent changes to the setting are the
single most common way a trustworthy-ML result becomes meaningless.

## 2. When to use

- Before the first training run of a project whose model faces data that differ from the training data.
  The difference may concern domain, cue correlation, adversarial pressure, or cost of error.
- When you adopt a published method, and you need to know whether its claim transfers to your case.
- When a reviewer, collaborator, or deployer asks "how do you know it generalizes?".
- Whenever you compare two methods that used different supervision, data, or compute.

A pure ID benchmark reproduction whose deployment claim is the benchmark itself does not need this
SOP. Record that decision.

## 3. Inputs / prerequisites

- Candidate task: input space, output space, decision to be automated.
- Available data inventory: which splits exist, which labels/attributes exist, their provenance,
  and their sizes.
- Knowledge (or an explicit guess) of the deployment stream: devices, sites, time span, users,
  weather/lighting, expected class mix.
- Resource limits: parameter budget, wall-clock, memory, annotation or human-review budget.
- The prior work you intend to compare against, with their settings written down.

## 4. Definitions needed for execution

- **Development** — the stage in which parameters are fitted *and* design choices are made.
  **Deployment** — the stage in which the frozen model meets a changing environment. Training is
  inside development. *Testing as reported in a paper is also inside development* unless you
  genuinely never look.
- **Setting** — the triple (development resources, deployment environment, time). Resources
  include data, labels, extra supervision, inductive bias, tooling, and human expertise.
- **Information rights** — the part of the setting that says what a method may look at. The rights
  cover labeled target-domain samples and unlabeled target-domain data. The rights also cover
  visual access to deployment data, test-time statistics, post-deployment updates, and few-shot
  target examples. A method may use only the rights its declared setting grants. Using more does
  not make the work invalid. Using more makes the work a **different setting**, and that setting
  then has its own comparison class and its own benchmark.
- **Test-batch right** — permission to consume the unlabeled test set *as a batch*. Adaptation
  against test statistics actually needs that permission. The test-batch right is not the same
  grant as access to unlabeled target data. Declare the test-batch right separately, because that
  right changes what a per-item claim can mean. The same objective, driven on one sample at a time,
  collapses toward a one-hot answer. The objective is undefined wherever nothing distinguishes an
  unexpected input from an ordinary one.
- **Generalization type** — pick which train→test difference you claim to survive: ID (same
  distribution, different samples), cross-domain (same task, different domain), cross-bias (different
  cue correlations), adversarial (worst-case samples). The list is not exhaustive. If your case falls
  outside the list, name the difference explicitly.
- **Cue** — a factor of variation in the data (color, shape, background, sensor artifact). Cues
  belong to the data, not to the model.
- **Causal (robust) cue / spurious (non-causal) cue** — a causal cue is one whose relation to the
  label is expected to hold in the deployment environment. A spurious cue is one that merely
  co-occurs during development.
- **ρ** — the fraction of *unbiased* (off-diagonal) development samples you allow yourself to use.
  State its direction explicitly: which population the fraction refers to, because this symbol is
  used inconsistently in the source literature.

## 5. Procedure

**Core**

1. Write the task statement: `X → Y`, decision owner, and what a wrong answer costs.
2. Write the deployment environment as a list of named variation axes (device, site, time,
   population, sensor, language, …). For each axis, mark whether development data cover that axis.
3. Attach a generalization type to **each result you intend to report**. Use ID, cross-domain,
   cross-bias, adversarial, or a type you name yourself. Record with each result the condition that
   result is measured under. A project may legitimately report several types. Domain shift,
   corruption, subgroup shift and adversarial stress are four questions. A project may answer all
   four, and that is not a contradiction. Do not blend heterogeneous conditions into one headline
   number unless the report states an aggregation rule that justifies the collapse.
4. Build the **cue whitelist**. For each named factor of variation, assign one of the statuses
   listed below:

   - `allowed-evidence`
   - `tolerated-if-unavoidable`
   - `forbidden-evidence`

   Add a one-line reason for each status. Anything not listed is undecided. List the undecided
   factors explicitly, rather than leaving those factors implicit.
5. Inventory supervision. Declare the **information rights** you claim:

   - task labels
   - group/attribute/domain labels
   - the unbiased-sample fraction ρ
   - target-domain samples (labeled / unlabeled / none)
   - visual access to deployment material
   - test-time statistics
   - post-deployment updates
   - the pretraining corpora
   - human review capacity

   Name the setting these rights belong to. The source catalogues ID generalization (§2.4.2),
   domain adaptation (§2.4.4), domain generalization (§2.4.5), and test-time training (§2.4.6). The
   source also catalogues domain- and task-incremental continual learning (§2.4.7, §2.4.11), and
   K-shot / meta-learning + K-shot (§2.4.9-§2.4.10). Or name your own setting and say so.
6. Record the resource envelope (compute, memory, wall-clock, annotation). State whether each
   compared method receives the same envelope.
7. Freeze the statement into a **setting block** (see §9). Before training, check the setting block
   against §6.

**Extended** — add when the result is published, reused across teams, or used for a risk-bearing
decision:

8. Write the *real-world scenario* sentence. That sentence is a concrete, believable instantiation
   of the setting. Name what in the scenario is hypothetical.
9. Enumerate the time behavior. State whether deployment is static, whether deployment drifts, and
   whether the label space changes. State whether retraining and model selection are part of the
   system, and give their cadence and cost.
10. Write the comparison class. List the specific prior works whose claims you consider comparable.
    For each such work, list the setting line you checked that work against. Move any work with more
    resources than you declared to a separate "stronger-setting" table.
11. Pre-register the decision policy applied later to test numbers (§5 step 2 and §7 of SOP-02).
    That makes the statement "we only looked once" verifiable rather than asserted.

## 6. Mandatory checks

Run all of the checks below. Each check is a stop-and-fix, not a warning.

- [ ] **Setting completeness**: the resources, the deployment distribution, and the time behavior
      are each written down. No field says "as usual", and no field is blank.
- [ ] **Claim-level typing**: every reported headline number names the generalization type. Each
      headline number also names the condition under which that number was measured. Several types
      in one project is normal. One number that blends several types is not normal, unless the
      report states an aggregation rule and justifies that rule.
- [ ] **Rights declaration**: every extra-resource ingredient the method consumes appears in the
      setting block as granted by the declared setting. The ingredients include target labels,
      unlabeled target data, batch-level test-time adaptation, visual access, test-time statistics,
      target-informed calibration, and post-deployment updates. If the declared setting does not
      grant an ingredient, either the setting changes or the ingredient goes.
- [ ] **Cue whitelist is a partition**: every named factor of variation has a status. The undecided
      list is empty, or the report explicitly accepts that list.
- [ ] **Supervision honesty**: the declared labels match the data actually present on disk. Count
      the group/attribute labels, and verify ρ by computing that fraction rather than by quoting the
      dataset paper.
- [ ] **Pretraining disclosure**: for every pretrained component, name the corpus. Record the
      relevant exposure separately: semantic or class exposure, exact or near-duplicate evaluation
      material, and benchmark-specific adaptation or fine-tuning. Do not collapse those exposure
      categories into one contamination label. Whether the resulting experiment is called
      "zero-shot" follows the explicit definition of the benchmark or study setting being used.
      This SOP does not impose a universal zero-shot definition.
- [ ] **Equal-ingredients check**: for each intended comparison, the other work's setting is
      recorded and the differences listed. Unequal resources ⇒ reclassify as a different setting.
- [ ] **Information-rights compliance**: development uses no deployment or target-domain information
      beyond the rights granted by the declared setting. Target-domain access is legitimate when the
      setting grants that access. Undeclared access is the integrity failure.

## 7. Decision or stop conditions

- **Stop and re-scope** if the claimed generalization type is cross-bias and neither attribute
  labels nor a nonzero ρ is available. With only a diagonal training set, the deployment cue is
  unidentifiable. The claim is then not testable, only arguable.
- **Re-declare the setting** as soon as the method consumes target-domain or deployment information
  that the declared setting does not grant. The consumed material may carry a label or not. A
  script, or an eye inspecting the data, may make the choice. The re-declaration records a change of
  problem, not a fault. The same work may be an entirely legitimate domain-adaptation,
  test-time-training or continual-learning project. The source is explicit on one point: once
  target-domain information is available, "we cannot call it a domain generalization setup
  anymore". The source adds that we must instead build a new setting with its own comparison class.
  What is not permitted is to keep the old setting's name and to quote its published results as the
  competition.
- **Proceed with a weaker claim** if you cannot describe the deployment environment. Fall back to
  "ID performance plus declared stress tests", and record the missing knowledge as a limitation.
- **Escalate to the Extended tier** if a decision with asymmetric error cost depends on the model.

## 8. Common methodological failures

- You write the setting *after* the results, so that the claim matches whatever the numbers
  survived.
- You report one accuracy for a mixture of cross-domain and cross-bias shifts.
- You treat a benchmark name as a setting. The dataset is the same, the supervision differs, and
  the result is not comparable.
- You keep a domain-generalization label after the work uses target-domain data. The source's own
  scenarios call that a different setting. Training on unlabeled target samples "is performing
  domain adaptation, not domain generalization". So the fix is to rename the setting, not to hide
  the data.
- You leave "forbidden cues" implicit. Nothing in standard training stops the model from using
  those cues.
- You count engineer expertise and pretraining data as free. You then compare against methods that
  had neither.
- Silent ρ drift: the sample count that was 2 % unbiased at project start becomes 20 % once
  convenient data are added.
- You use "zero-shot" without stating the benchmark or study definition, and without stating the
  model's pretraining exposure.

## 9. Required outputs

- `setting-block.md` (or a YAML front-matter file) with these fields:

  - `task`
  - `deployment_axes[]`
  - `generalization_type`
  - `cue_whitelist{factor→status}`
  - `supervision{labels, ρ, target_samples, pretraining[]}`
  - `resource_envelope`
  - `time_behavior`
  - `comparison_class[]`, with the per-entry checked setting differences

- A one-paragraph real-world scenario statement (Extended).
- The undecided-cue list, accepted or resolved.

## 10. Minimum reporting requirements

Reproduce the setting block verbatim in any report or paper. In the first paragraph, state the
generalization type claimed, which extra supervision you used, and any ingredient your comparison
class did not have. If ρ appears, give its numeric value and its direction.

## 11. Links to relevant Benchmarks

- [`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md) —
  consumes the declared generalization type and domain axes.
- [`BM-02`](../../Benchmark/Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md) — consumes the
  cue whitelist and ρ.
- [`BM-05`](../../Benchmark/Trustworthy-ML-2023/BM-05-adversarial-robustness.md) — consumes the
  adversarial branch of the type axis.
- [`BM-07`](../../Benchmark/Trustworthy-ML-2023/BM-07-selective-prediction-under-cost.md) —
  consumes the cost statement.
- [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md) — audits the
  setting block itself.
- [`BM-09`](../../Benchmark/Trustworthy-ML-2023/BM-09-disclosure-of-training-data-and-context.md) —
  consumes the information-rights block. The declared setting grants here what an attack may query,
  and at which access level. That grant must exist before this benchmark runs.

## 12. Source traceability

- Vocabulary for setting, development, deployment, training, testing, setting-resources and
  real-world-scenario: §2.3.1 (Definitions 2.14-2.19, book pp. 24-25).
- Supervision-keyed learning settings: §2.4.2-§2.4.11 (pp. 29-35).
- Equal-resources rule: §2.3.1, "How to compare methods with different resources?" (p. 25) and
  §5.3.1 (pp. 342-343).
- Information leakage as an influx into a closed development system (Definition 2.24): §2.5.1 (p. 36).
- The instruction that once target-domain information is available, "we cannot call it a domain
  generalization setup anymore": §2.5.1 (p. 36).
- The same instruction requires a new setting, benchmark and comparison class: §2.5.1 (p. 36).
- Scenarios 1-4 — labeled tuning, unlabeled tuning, visual inspection, and choosing hyper-parameters
  against published scores: §2.5.1 (pp. 36-37).
- The admission that evaluation on a new domain necessarily uses target-domain data: §2.5.1
  (pp. 36-37).
- The admission that the definition of domain generalization "may need to shift ... into something
  that allows some validation in the target domain (like domain adaptation)": §2.5.1 (pp. 36-37).
- Generalization types: §2.1.2, Definition 2.8 (p. 18).
- Cue/feature/attribute and ID/OOD: §2.1.2, Definitions 2.5-2.7 (p. 18).
- Causal vs spurious cues: §1.4.1 (pp. 11-12).
- Unidentifiability of the deployment cue on a diagonal set: §2.8.2 (p. 47).
- Pretraining leakage and the limits of zero-shot claims at scale: §2.5.1 (p. 37).
- ρ as part of the setting: §2.8.3 (p. 48), with the direction ambiguity noted at §2.13.2
  Table 2.5 (p. 74).

Core/Extended tiering, the checklist format, file layout and the "pre-register the decision policy"
step are repository conventions.
