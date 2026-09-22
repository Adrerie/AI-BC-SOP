# SOP-01 — Specify the deployment setting before training

**Stage:** define the problem · **Tier:** Core + Extended · **Concepts:** C1 setting declaration,
C2 generalization-type axis, C3 cue whitelist

Shared terms are defined once in
[`SOP-08-report-evidence-and-validity-boundaries.md`](SOP-08-report-evidence-and-validity-boundaries.md);
this document defines only what is needed to execute this procedure.

## 1. Purpose

Produce a written, checkable statement of what the experiment is allowed to know and what it
claims to survive, so that (a) later numbers mean something, and (b) any comparison with other
work is between equal ingredients. Changing the setting silently is the single most common way a
trustworthy-ML result becomes meaningless.

## 2. When to use

- Before the first training run of any project whose model will face data that differ from the
  training data in domain, cue correlation, adversarial pressure, or cost of error.
- When adopting a published method and needing to know whether its claim transfers to your case.
- When a reviewer, collaborator, or deployer asks "how do you know it generalizes?".
- Whenever you are about to compare two methods that used different supervision, data, or compute.

Not required for a pure ID benchmark reproduction where the deployment claim is the benchmark
itself — but record that decision.

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
  inside development; *testing as reported in a paper is also inside development* unless you
  genuinely never look.
- **Setting** — the triple (development resources, deployment environment, time). Resources
  include data, labels, extra supervision, inductive bias, tooling, and human expertise.
- **Information rights** — the part of the setting that says what a method is allowed to look at:
  labeled target-domain samples, unlabelled target-domain data, visual access to deployment data,
  test-time statistics, post-deployment updates, few-shot target examples. A method may use only the
  rights its declared setting grants. Using more does not make the work invalid; it makes it a
  **different setting**, which then has its own comparison class and its own benchmark.
- **Generalization type** — pick which train→test difference you are claiming to survive:
  ID (same distribution, different samples), cross-domain (same task, different domain),
  cross-bias (different cue correlations), adversarial (worst-case samples). The list is not
  exhaustive; if your case is outside it, name the difference explicitly.
- **Cue** — a factor of variation in the data (color, shape, background, sensor artifact). Cues
  belong to the data, not to the model.
- **Causal (robust) cue / spurious (non-causal) cue** — a cue whose relation to the label is
  expected to hold in the deployment environment versus one that merely co-occurs during
  development.
- **ρ** — the fraction of *unbiased* (off-diagonal) development samples you will allow yourself to
  use. State its direction explicitly: which population the fraction refers to, because this symbol
  is used inconsistently in the source literature.

## 5. Procedure

**Core**

1. Write the task statement: `X → Y`, decision owner, and what a wrong answer costs.
2. Write the deployment environment as a list of named variation axes (device, site, time,
   population, sensor, language, …) and mark, for each, whether development data cover it.
3. Attach a generalization type (ID / cross-domain / cross-bias / adversarial / other-name-it) to
   **each result you intend to report**, together with the condition that result is measured under.
   A project may legitimately report several types — domain shift, corruption, subgroup shift and
   adversarial stress are four questions, and answering all four is not a contradiction. What is not
   permitted is blending heterogeneous conditions into one headline number without stating an
   aggregation rule that justifies the collapse.
4. Build the **cue whitelist**: for each named factor of variation, mark it
   `allowed-evidence`, `tolerated-if-unavoidable`, or `forbidden-evidence`, with a one-line
   reason. Anything not listed is undecided — list the undecided ones explicitly rather than
   leaving them implicit.
5. Inventory supervision and declare the **information rights** you are claiming: task labels,
   group/attribute/domain labels, unbiased-sample fraction ρ, target-domain samples (labeled /
   unlabelled / none), visual access to deployment material, test-time statistics, post-deployment
   updates, pretraining corpora, human review capacity. Name the setting these rights belong to — the
   source catalogues ID generalization (§2.4.2), domain adaptation (§2.4.4), domain generalization
   (§2.4.5), test-time training (§2.4.6), domain- and task-incremental continual learning (§2.4.7,
   §2.4.11), and K-shot / meta-learning + K-shot (§2.4.9-§2.4.10) — or name your own and say so.
6. Record the resource envelope (compute, memory, wall-clock, annotation) and whether each compared
   method will receive the same envelope.
7. Freeze this into a **setting block** (see §9) and check it against §6 before training.

**Extended** — add when the result will be published, reused across teams, or used for a
risk-bearing decision:

8. Write the *real-world scenario* sentence: a concrete, believable instantiation of the setting,
   and name what in it is hypothetical.
9. Enumerate the time behavior: is deployment static, drifting, or does the label space change?
   Is retraining/model selection part of the system, and at what cadence and cost?
10. Write the comparison class: list the specific prior works whose claims you consider
    comparable, and for each, the setting line you checked it against. Anything with more
    resources than you declared is moved to a separate "stronger-setting" table.
11. Pre-register the decision policy that will later be applied to test numbers (§6 step 5 of
    SOP-02), so that "we only looked once" is verifiable rather than asserted.

## 6. Mandatory checks

Run all of these; each is a stop-and-fix, not a warning.

- [ ] **Setting completeness**: resources, deployment distribution, and time are each written down;
      no field says "as usual" or is blank.
- [ ] **Claim-level typing**: every reported headline number names the generalization type and the
      condition it was measured under. Several types in one project is normal; one number that blends
      them is not, unless the aggregation rule is stated and justified.
- [ ] **Rights declaration**: every extra-resource ingredient the method consumes — target labels,
      unlabelled target data, visual access, test-time statistics, target-informed calibration,
      post-deployment updates — appears in the setting block as granted by the declared setting. If it
      is not granted, either the setting changes or the ingredient goes.
- [ ] **Cue whitelist is a partition**: every named factor of variation has a status; the
      undecided list is empty or explicitly accepted.
- [ ] **Supervision honesty**: the declared labels match the data actually present on disk (count
      group/attribute labels; verify ρ by computing it, not by quoting the dataset paper).
- [ ] **Pretraining disclosure**: for every pretrained component, name the corpus and record which
      exposure level applies — (i) no task-specific examples and no adaptation; (ii) class-name or
      semantic exposure during pretraining only; (iii) exact or near-duplicate evaluation material
      present; (iv) benchmark-specific fine-tuning. Report the level. "Zero-shot" may be used only for
      level (i), and only where the benchmark defines the term; semantic exposure is not
      contamination, and duplicate exposure is a different problem from fine-tuning on the benchmark,
      so the two must not be reported as one another.
- [ ] **Equal-ingredients check**: for each intended comparison, the other work's setting is
      recorded and the differences listed. Unequal resources ⇒ reclassify as a different setting.
- [ ] **Deployment fiction preserved**: nothing from the deployment stream (labels, images, logs,
      scores) has entered the development folder or the notebook history.

## 7. Decision or stop conditions

- **Stop and re-scope** if the claimed generalization type is cross-bias and neither attribute
  labels nor a nonzero ρ is available: with only a diagonal training set the deployment cue is
  unidentifiable, so the claim is not testable, only arguable.
- **Re-declare the setting** as soon as the method consumes target-domain or deployment information
  the declared setting does not grant — labeled or unlabelled, chosen by a script or by an eye
  inspecting the data. This records a change of problem, not a fault: the same work may be an entirely
  legitimate domain-adaptation, test-time-training or continual-learning project, and the source is
  explicit that once target-domain information is available "we cannot call it a domain generalization
  setup anymore" and must instead build a new setting with its own comparison class. What is not
  permitted is keeping the old setting's name and quoting its published results as the competition.
- **Proceed with a weaker claim** if the deployment environment cannot be described: fall back to
  "ID performance plus declared stress tests", and record the missing knowledge as a limitation.
- **Escalate to the Extended tier** if a decision with asymmetric error cost depends on the model.

## 8. Common methodological failures

- Writing the setting *after* the results, so that the claim matches whatever the numbers survived.
- Reporting one accuracy for a mixture of cross-domain and cross-bias shifts.
- Treating a benchmark name as a setting: same dataset, different supervision, incomparable result.
- Keeping a domain-generalization label after using target-domain data. The source's own scenarios
  call that a different setting — training on unlabelled target samples "is performing domain
  adaptation, not domain generalization" — so the fix is to rename the setting, not to hide the data.
- Leaving "forbidden cues" implicit — nothing in standard training stops the model using them.
- Counting engineer expertise and pretraining data as free, then comparing against methods that had
  neither.
- Silent ρ drift: the sample count that was 2 % unbiased at project start becomes 20 % once
  convenient data are added.
- Claiming zero-shot status while the pretraining corpus contains the target classes.

## 9. Required outputs

- `setting-block.md` (or a YAML front-matter file) with the fields:
  `task`, `deployment_axes[]`, `generalization_type`, `cue_whitelist{factor→status}`,
  `supervision{labels, ρ, target_samples, pretraining[]}`, `resource_envelope`,
  `time_behavior`, `comparison_class[]` with the per-entry checked setting differences.
- A one-paragraph real-world scenario statement (Extended).
- The undecided-cue list, accepted or resolved.

## 10. Minimum reporting requirements

Reproduce the setting block verbatim in any report or paper, and state in the first paragraph:
the generalization type claimed, which extra supervision was used, and any ingredient your
comparison class did not have. If ρ appears, give its numeric value and its direction.

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

## 12. Source traceability

Setting, development, deployment, training, testing, setting-resources and real-world-scenario
vocabulary: §2.3.1 (Definitions 2.14-2.19, book pp. 24-25). Supervision-keyed learning settings:
§2.4.2-§2.4.11 (pp. 29-35). Equal-resources rule: §2.3.1, "How to compare methods with different
resources?" (p. 25) and §5.3.1 (pp. 342-343). Information leakage as an influx into a closed
development system (Definition 2.24), and the instruction that once the target-domain information is
available "we cannot call it a domain generalization setup anymore" but must set up a new setting,
benchmark and comparison class: §2.5.1 (p. 36). Scenarios 1-4 — labelled tuning, unlabelled tuning,
visual inspection, and choosing hyper-parameters against published scores — together with the
admission that evaluating on a new domain necessarily uses target-domain data and that the definition
of domain generalization "may need to shift ... into something that allows some validation in the
target domain (like domain adaptation)": §2.5.1 (pp. 36-37). Generalization types: §2.1.2,
Definition 2.8 (p. 18).
Cue/feature/attribute and ID/OOD: §2.1.2, Definitions 2.5-2.7 (p. 18). Causal vs spurious cues:
§1.4.1 (pp. 11-12). Unidentifiability of the deployment cue on a diagonal set: §2.8.2 (p. 47).
Pretraining leakage and the limits of zero-shot claims at scale: §2.5.1 (p. 37). ρ as part of the
setting: §2.8.3 (p. 48), with the direction ambiguity noted at §2.13.2 Table 2.5 (p. 74).
Core/Extended tiering, the checklist format, file layout and the "pre-register the decision policy"
step are repository conventions.
