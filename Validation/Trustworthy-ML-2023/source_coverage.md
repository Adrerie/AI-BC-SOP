# Source Coverage Audit — *Trustworthy Machine Learning* (2023)

Plan 1 artifact. Produced before any SOP or Benchmark drafting (see Gate A at the end).

## Step 1 — Source record

| Field | Value |
|---|---|
| Primary source path | `D:\.Myfile\D1s1\学习路径方向\书\Trustworthy Machine Learning book 2023.pdf` |
| File type | PDF 1.5, 375 pages, produced by `pdfTeX-1.40.25` (LaTeX + hyperref) |
| Title / edition / year | *Trustworthy Machine Learning*, first edition, 2023 (document created 2023-10-11) |
| Authors | Bálint Mucsányi, Michael Kirchhof, Elisa Nguyen, Alexander Rubinstein, Seong Joon Oh (University of Tübingen / Tübingen AI Center) |
| Subject keywords in file | Machine Learning, Scalability, Trustworthiness, OOD Generalization, Explainability, Uncertainty, Evaluation |
| Text completeness | Full text: front matter, all 5 chapters, appendix, list of definitions, bibliography. Text layer is extractable (not scanned images), so the audit works on real body text. |
| Headings machine-readable? | **Not via bookmarks** — `doc.get_toc()` returns 0 entries, i.e. the PDF has no outline/named destinations. Headings were recovered from font metadata (size + weight) and cross-checked against the printed table of contents; see Step 2. |
| Secondary copies in workspace | Two unrelated PDFs (`TensorFlow深度学习`, `深度学习进阶：自然语言处理`) sit in the same folder; neither is a copy of this book, so no secondary source was needed to recover structure. |
| Pagination mapping | Printed book page = PDF page − 2 (verified: chapter 1 starts on PDF p.9 = book p.7 as listed in the printed TOC; every `Definition x.y` page in the printed *List of Definitions* reproduces under this mapping). |

## Step 2 — Structural universe as extracted

- 6 chapter headings (5 numbered chapters plus Appendix A) and 4 front/back-matter blocks
- 49 section headings (`x.y`)
- 188 subsection headings (`x.y.z`)
- **247 headings in total**, every one of them listed in the coverage table below with a disposition.

Extraction procedure (repeatable):

1. Attempt PDF outline first (`PyMuPDF.get_toc`) → 0 entries, so outline-based extraction is impossible.
2. Walk every page's text dictionary; keep every line whose maximum span size is one of the heading sizes and whose characters are ≥60 % bold/semibold. Observed heading sizes: 45.8 pt (chapter title), 19.9 pt (`Chapter N` banner), 14.3 pt (`x.y`), 12.0 pt (`x.y.z`). Body text is 10.0 pt.
3. Join a number line with the following title line(s) on the same page at the same size — the typesetter puts the heading number and the heading title in separate text runs, and some titles use `SemiBold` rather than `Bold`, which is why a naive bold-only filter loses 11 titles.
4. Cross-check the recovered `x.y` list against the printed table of contents (PDF pages 4–5) → 49 sections on both sides, no heading present in one source and missing in the other.
5. Validate numbering: within every section, subsection numbers are contiguous `1..n`; 6 sections (1.3, 2.10, 2.11, 3.13, 4.4, 4.7) legitimately have no subsections.

Two headings needed manual repair and are recorded here as source-fidelity notes, not silently fixed:

- `2.4.1` — the raw scan swallowed figure labels into the title (`Why are the learning settings important? MNIST MNIST-M SVHN SYN …`); the heading itself is *Why are the learning settings important?*
- `3.13` — the printed heading is *Applications of Attribution to Test Samples* while its body discusses training-sample attribution applications; the book's own numbering (`Definition 3.16`, §3.12.2) sits with training-data attribution. Recorded as a source inconsistency; the audit keeps the printed title.

## Step 3 — Where body reading was required

Reading was triggered by the Plan 1 criteria (vague title, method named without role, likely metric or protocol definition, assumptions/caveats that matter, unclear relation to other concepts, possible reusable procedure). Two reading modes are recorded per row:

- `direct` — read in the main audit pass: the deployment/evaluation setup cluster (2.3, 2.5), the uncertainty-metric cluster (4.4–4.10), the explainability-evaluation cluster (3.7–3.8), the evaluation-and-scalability chapter (5.1–5.3), plus the framing in 1.4 and 2.1–2.2 and the printed *List of Definitions*.
- `delegated` — read in bounded sub-passes over method catalogs whose headings name methods without stating their evaluation role: the domain-generalization / feature-selection cluster (2.6–2.14), the adversarial cluster (2.15.x), the attribution-method catalog (3.1–3.6, 3.9–3.13), and the uncertainty-estimator families (4.1–4.3, 4.11–4.14). Notes from these passes are integrated in the Body-reading notes section.
- `heading` — no body reading: content is navigation, an index, historical narrative, or a research agenda that cannot become a reusable procedure.

Body-read distribution: {'direct': 89, 'heading': 14, 'delegated': 144}.

## Step 4 — Normalized concept tags

Tags are assigned by methodological function, never copied from chapter names. The tag vocabulary used in the table:

| Tag | Meaning |
|---|---|
| `deployment-setting` | what the system faces after release: resources, environment, time |
| `dataset-splits / evaluation-integrity` | training / validation / test roles, who may look at what |
| `information-leakage` | deployment information reaching development, incl. leaderboard and pretraining |
| `distribution-shift / ood-generalization` | train≠test distributions and their sub-types |
| `generalization-type-taxonomy` | ID, cross-domain, cross-bias, adversarial |
| `spurious-correlation / underspecification / shortcut-bias` | wrong-cue families and their causes |
| `feature-selection / additional-supervision` | how to get the right cues, and what supervision that costs |
| `mitigation-method` | training-time interventions (Group DRO, DANN, ReBias, adversarial training, …) |
| `adversarial-robustness / threat-model / attack-protocol` | worst-case evaluation and its ingredients |
| `gradient-masking` | false robustness produced by the evaluation itself |
| `certified-robustness` | sound-but-loser bounds as an evaluation mode |
| `attribution / soundness / linearization` | explanation-by-attribution concepts |
| `explanation-evaluation / sanity-check / hitl-evaluation` | how to test an explanation method |
| `uncertainty / predictive / aleatoric / epistemic` | the three uncertainty quantities and their causes |
| `proper-scoring / calibration / ece / ranking-condition` | metric families for confidence truthfulness |
| `metric-gaming` | ways a metric can be satisfied without the property being present |
| `ood-detection / multiplicity-detection / error-detection` | proxy tasks that score non-predictive uncertainty |
| `selective-prediction` | abstention, human routing, active learning |
| `estimator-family / feature-distance` | how epistemic or aleatoric estimates are produced |
| `scalability / computational-cost / hyperparameter-tuning` | cost side of a trustworthy method |
| `benchmark-design / reporting / validity-boundary` | what a benchmark must state and where it stops |
| `repository-scope / background-motivation / history-narrative / research-agenda` | material that motivates but is not operationalized |

### Disposition policy

| Disposition | Rule used in this audit |
|---|---|
| `incorporate` | The heading carries a definition, protocol, metric, check, or failure mode that a reused procedure or benchmark must state. |
| `supporting` | Background, motivation, method detail, or evidence that shapes design decisions but is not itself operationalized into a step. |
| `redundant` | The heading restates material already audited elsewhere in the book; kept once, cross-linked. |
| `out-of-scope` | Navigation, index, historical narrative, author research agenda, legal context, or specialised showcase that has no reusable evaluation procedure behind it. |
| `needs-body-reading` | Left open deliberately; must be zero at Gate A. |

Where a subsection inherits its section's disposition the tag list ends with `inherited`; the decision was taken per section after body reading, not per chapter position.

## Coverage table

Source IDs are the book's own heading numbers (kept only for traceability), so source order is preserved here and deliberately abandoned in the artifact taxonomy. `Book p.` is the printed page.

| Source ID | Heading | Level | Book p. | Initial concept tags | Body read? | Disposition |
|---|---|---|---:|---|---|---|
| FM-Contents | Contents | front/back matter | 1 | navigation | direct | out-of-scope |
| FM-Preface | Preface | front/back matter | 4 | repository-scope, reading-guide | heading | supporting |
| 1 | Introduction to Trustworthy Machine Learning | chapter | 7 | problem-definition, trustworthiness-framing | direct | incorporate |
| 1.1 | Scale is all we need? | section | 8 | problem-definition, background-motivation | direct | supporting |
| 1.1.1 | Are we done with ML? | subsection | 8 | background-motivation | heading | supporting |
| 1.2 | Key Limitations of ML | section | 9 | failure-analysis, cost-awareness, background-motivation | direct | supporting |
| 1.2.1 | ML often does not work. | subsection | 9 | failure-analysis | heading | supporting |
| 1.2.2 | ML has high operating costs. | subsection | 9 | cost-awareness, computational-cost | heading | supporting |
| 1.2.3 | ML is currently not trustworthy. | subsection | 10 | failure-analysis, trustworthiness-framing | heading | supporting |
| 1.3 | Topics of the Book | section | 10 | repository-scope | heading | out-of-scope |
| 1.4 | Trustworthiness: Transition from “What” to “How” | section | 11 | problem-definition, what-vs-how, causal-vs-spurious-cue | direct | incorporate |
| 1.4.1 | Why Solving “What” is Not Enough | subsection | 11 | causal-vs-spurious-cue, feature-selection, failure-analysis | direct | incorporate |
| 1.4.2 | Machine Learning 2.0 | subsection | 12 | what-vs-how, additional-supervision | direct | supporting |
| 2 | OOD Generalization | chapter | 14 | ood-generalization, distribution-shift | direct | incorporate |
| 2.1 | Introduction to OOD Generalization | section | 15 | problem-definition, task-definition | direct | supporting |
| 2.1.1 | Examples of Tasks | subsection | 16 | task-definition, benchmark-design | direct | incorporate |
| 2.1.2 | Generalization Types | subsection | 17 | generalization-type-taxonomy, distribution-shift | direct | incorporate |
| 2.2 | Why do we even care about OOD generalization? | section | 19 | deployment-consequence, cost-awareness | direct | supporting |
| 2.2.1 | Greater Levels of Automation | subsection | 22 | deployment-consequence | direct | supporting |
| 2.2.2 | Once we “solve” OOD generalization... | subsection | 24 | speculative-benefit | direct | out-of-scope |
| 2.3 | Formal Setup of OOD Generalization | section | 24 | dataset-splits, evaluation-integrity, deployment-setting | direct | incorporate |
| 2.3.1 | Stages of ML Systems | subsection | 24 | deployment-setting, problem-definition, resource-accounting | direct | incorporate |
| 2.3.2 | Dataset Splits in ML | subsection | 26 | dataset-splits, evaluation-integrity | direct | incorporate |
| 2.3.3 | Why Idealists Cannot Evaluate on the Test Set | subsection | 28 | evaluation-integrity, test-set-spoiling | direct | incorporate |
| 2.4 | Common Settings for OOD Generalization | section | 28 | distribution-shift, ood-generalization, deployment-setting | direct | incorporate |
| 2.4.1 | Why are the learning settings important? MNIST MNIST-M SVHN SYN Art Painting Cartoon Photo Sketch Artistic Clip Art Product Real World | subsection | 28 | domain-label, distribution-shift | direct | incorporate |
| 2.4.2 | ID generalization | subsection | 29 | id-generalization | direct | incorporate |
| 2.4.3 | Domain-Dependent OOD Generalization | subsection | 30 | distribution-shift, taxonomy-axis | direct | incorporate |
| 2.4.4 | Domain Adaptation | subsection | 30 | domain-adaptation, deployment-setting | direct | incorporate |
| 2.4.5 | Domain Generalization | subsection | 31 | domain-generalization, deployment-setting | direct | incorporate |
| 2.4.6 | Test-Time Training | subsection | 32 | test-time-adaptation, deployment-setting | heading | supporting |
| 2.4.7 | Domain-Incremental Continual Learning | subsection | 32 | continual-learning, deployment-setting | heading | supporting |
| 2.4.8 | Task-Dependent OOD Generalization | subsection | 33 | task-dependent-shift, taxonomy-axis | heading | supporting |
| 2.4.9 | K-Shot Learning | subsection | 34 | few-shot-learning | heading | supporting |
| 2.4.10 | Meta-Learning + K-Shot Learning | subsection | 34 | meta-learning, few-shot-learning | heading | supporting |
| 2.4.11 | Task-Incremental Continual Learning | subsection | 35 | continual-learning | heading | supporting |
| 2.5 | ML Dev as a Closed System of Information | section | 35 | information-leakage, evaluation-integrity | direct | incorporate |
| 2.5.1 | Information Leakage from Deployment | subsection | 36 | information-leakage, evaluation-integrity, benchmark-design | direct | incorporate |
| 2.5.2 | A Case Study on Information Leakage | subsection | 38 | information-leakage, ablation-study, failure-analysis | direct | incorporate |
| 2.5.3 | Solutions to Information Leakage | subsection | 39 | information-leakage, mitigation-protocol, benchmark-design | direct | incorporate |
| 2.6 | Domain Generalization Benchmarks | section | 40 | benchmark-design, domain-generalization | delegated | incorporate |
| 2.6.1 | Examples of Domain Generalization Benchmarks | subsection | 40 | benchmark-design, domain-generalization, dataset-review | delegated | incorporate |
| 2.7 | Domain Generalization Difficulties | section | 44 | spurious-correlation, underspecification, failure-analysis | delegated | incorporate |
| 2.7.1 | Ill-Defined Behavior and Spurious Correlations | subsection | 44 | ill-defined-behavior, spurious-correlation | delegated | incorporate |
| 2.8 | Cross-Bias Generalization | section | 45 | cross-bias-generalization, feature-selection, benchmark-design | delegated | incorporate |
| 2.8.1 | Why is cross-bias generalization still challenging? | subsection | 46 | cross-bias-generalization, failure-analysis | delegated | incorporate |
| 2.8.2 | The Feature Selection Problem | subsection | 46 | feature-selection, problem-definition | delegated | incorporate |
| 2.8.3 | Extra Information to Make Cross-Bias Generalization Possible | subsection | 48 | additional-supervision, mitigation-method | delegated | supporting |
| 2.8.4 | How to determine what cue our model learns to recognize? | subsection | 49 | diagnostic-procedure, cue-identification | delegated | incorporate |
| 2.9 | Shortcut (Simplicity) Bias | section | 49 | shortcut-bias, feature-selection, failure-analysis | delegated | incorporate |
| 2.9.1 | Examples of Shortcut Bias | subsection | 50 | shortcut-bias, failure-examples | delegated | supporting |
| 2.9.2 | Is the simplicity bias a bad thing? | subsection | 53 | shortcut-bias, background-theory | delegated | supporting |
| 2.10 | Identifying and Evaluating Misspecification | section | 55 | misspecification, failure-analysis, diagnostic-procedure | delegated | incorporate |
| 2.11 | Overview of Scenarios for Selecting the Right Features | section | 57 | feature-selection, mitigation-method, decision-rule | delegated | incorporate |
| 2.12 | Scenario 1 for Selecting the Right Features | section | 57 | mitigation-method, subgroup-robustness, feature-selection | delegated | incorporate |
| 2.12.1 | Group DRO | subsection | 59 | mitigation-method, subgroup-robustness, feature-selection, inherited | delegated | incorporate |
| 2.12.2 | Domain-Adversarial Training of Neural Networks (DANN) | subsection | 62 | mitigation-method, subgroup-robustness, feature-selection, inherited | delegated | incorporate |
| 2.13 | Scenario 2 for Selecting the Right Features | section | 65 | mitigation-method, feature-selection, failure-analysis | delegated | incorporate |
| 2.13.1 | Learning from Failure | subsection | 67 | mitigation-method, feature-selection, failure-analysis, inherited | delegated | incorporate |
| 2.13.2 | ReBias: Representational regularization | subsection | 70 | mitigation-method, feature-selection, failure-analysis, inherited | delegated | incorporate |
| 2.14 | Scenario 3 for Selecting the Right Features | section | 75 | mitigation-method, additional-supervision, feature-selection | delegated | incorporate |
| 2.14.1 | Predicting is not Understanding | subsection | 77 | mitigation-method, additional-supervision, feature-selection, inherited | delegated | incorporate |
| 2.15 | Adversarial OOD Generalization | section | 86 | adversarial-robustness, threat-model | delegated | incorporate |
| 2.15.1 | Formulation of a General Adversarial Environment | subsection | 87 | threat-model, problem-definition | delegated | incorporate |
| 2.15.2 | Fast Gradient Sign Method (FGSM) | subsection | 88 | attack-protocol, white-box-attack | delegated | incorporate |
| 2.15.3 | Projected Gradient Descent (PGD) | subsection | 89 | attack-protocol, baseline-requirement | delegated | incorporate |
| 2.15.4 | FGSM vs. PGD | subsection | 91 | attack-strength-ordering, evaluation-protocol | delegated | incorporate |
| 2.15.5 | Different Strategy Spaces for Adversarial Attacks | subsection | 92 | threat-model, strategy-space-alignment | delegated | incorporate |
| 2.15.6 | Optical Flow | subsection | 96 | attack-method-detail | delegated | supporting |
| 2.15.7 | Adversarial Flow-Based Perturbation | subsection | 96 | attack-method-detail | delegated | supporting |
| 2.15.8 | White-Box vs. Black-Box Attacks | subsection | 97 | white-box-vs-black-box, evaluation-protocol | delegated | incorporate |
| 2.15.9 | Black-Box Attack via a Substitute Model | subsection | 98 | black-box-attack, baseline-requirement | delegated | supporting |
| 2.15.10 | Black-Box Attack via a Zeroth-Order Attack | subsection | 99 | black-box-attack, query-cost-accounting | delegated | supporting |
| 2.15.11 | Defense against Attacks: Adversarial Training | subsection | 100 | defense, adversarial-training, cost-accounting | delegated | incorporate |
| 2.15.12 | Obfuscated Gradients: Breaking the defense Again! | subsection | 102 | gradient-masking, evaluation-integrity, failure-analysis | delegated | incorporate |
| 2.15.13 | Effectiveness of Adversarial Training | subsection | 107 | defense-effectiveness, transferability | delegated | incorporate |
| 2.15.14 | Barrage of Random Transforms (BaRT) | subsection | 108 | defense-method-detail | delegated | supporting |
| 2.15.15 | Certified defenses | subsection | 110 | certified-robustness, evaluation-protocol, validity-boundary | delegated | incorporate |
| 2.15.16 | History and Possible Future of Adversarial Robustness in ML | subsection | 113 | history-narrative | delegated | out-of-scope |
| 2.15.17 | Towards Less Pessimistic defenses | subsection | 114 | research-agenda | delegated | out-of-scope |
| 3 | Explainability | chapter | 115 | explainability, attribution | delegated | incorporate |
| 3.1 | Introduction | section | 116 | explainability, problem-definition | delegated | supporting |
| 3.1.1 | Ways to Control Undefined Behavior | subsection | 117 | undefined-behavior, control-strategies | delegated | incorporate |
| 3.1.2 | Explainability as a Base Tool for Many Applications | subsection | 118 | explainability-applications | delegated | supporting |
| 3.1.3 | Explainability as a Data Subject’s Right | subsection | 119 | legal-context | delegated | out-of-scope |
| 3.1.4 | When is an explanation needed? | subsection | 119 | applicability-criteria | delegated | incorporate |
| 3.1.5 | When is an explanation not needed? | subsection | 119 | applicability-criteria | delegated | incorporate |
| 3.2 | Human Explanations | section | 120 | explainability, background-theory | delegated | supporting |
| 3.2.1 | How do humans explain to each other? | subsection | 120 | explainability, background-theory, inherited | delegated | supporting |
| 3.3 | Properties of Good Explanations | section | 121 | explainability, quality-criteria | delegated | incorporate |
| 3.3.1 | What are good explanations? | subsection | 122 | quality-criteria, soundness | delegated | incorporate |
| 3.3.2 | Intrinsically Interpretable Models | subsection | 123 | intrinsically-interpretable-models | delegated | supporting |
| 3.4 | Taxonomies of Model Explainability | section | 124 | explainability, taxonomy, soundness | delegated | incorporate |
| 3.4.1 | Soundness-Explainability Trade-off | subsection | 126 | soundness-explainability-tradeoff | delegated | incorporate |
| 3.4.2 | Current Status of XAI Techniques | subsection | 127 | xai-landscape | delegated | supporting |
| 3.5 | Methods for Attribution to Test Features | section | 127 | attribution, method-family | delegated | supporting |
| 3.5.1 | What features to consider in attribution methods to test features? | subsection | 128 | feature-granularity, evaluation-design | delegated | incorporate |
| 3.5.2 | Intrinsically interpretable models support counterfactual evalua- tion by design. | subsection | 130 | attribution, method-family, inherited | delegated | supporting |
| 3.5.3 | Infinitesimal Counterfactual Evaluation in Neural Networks: Saliency Maps | subsection | 131 | attribution, method-family, inherited | delegated | supporting |
| 3.5.4 | SmoothGrad – Smoother Input Gradients | subsection | 136 | attribution, method-family, inherited | delegated | supporting |
| 3.5.5 | Integrated Gradients | subsection | 137 | attribution, method-family, inherited | delegated | supporting |
| 3.5.6 | Comparing Local and Global Perturbations – Two Ways of Measur- ing Contribution | subsection | 139 | attribution, method-family, inherited | delegated | supporting |
| 3.5.7 | Local = Global for (Sparse) Linear Models | subsection | 140 | attribution, method-family, inherited | delegated | supporting |
| 3.5.8 | Zintgraf et al.: Inpainting + Black-Box Computation | subsection | 141 | attribution, method-family, inherited | delegated | supporting |
| 3.5.9 | LIME: Fitting a Sparse Linear Model | subsection | 144 | attribution, method-family, inherited | delegated | supporting |
| 3.5.10 | SHAP (SHapley Additive exPlanations) | subsection | 146 | attribution, method-family, inherited | delegated | supporting |
| 3.5.11 | Defining a Missing Feature | subsection | 150 | attribution, method-family, inherited | delegated | supporting |
| 3.5.12 | Meaningful Perturbations | subsection | 151 | attribution, method-family, inherited | delegated | supporting |
| 3.5.13 | Testing with Concept Activation Vectors (TCAV) | subsection | 153 | attribution, method-family, inherited | delegated | supporting |
| 3.5.14 | Class Activation Maps (CAM) | subsection | 157 | attribution, method-family, inherited | delegated | supporting |
| 3.5.15 | Comparison of the two CAM implementations | subsection | 158 | attribution, method-family, inherited | delegated | supporting |
| 3.5.16 | Assumptions to Make CAM Work | subsection | 161 | attribution, method-family, inherited | delegated | supporting |
| 3.5.17 | Grad-CAM – Generalizing CAM to non-linear h | subsection | 163 | attribution, method-family, inherited | delegated | supporting |
| 3.5.18 | Remaining Weakness of CAM | subsection | 165 | attribution, method-family, inherited | delegated | supporting |
| 3.5.19 | Class Activation Latent Mapping (CALM) | subsection | 166 | attribution, method-family, inherited | delegated | supporting |
| 3.5.20 | Summary of Test Input Attribution Methods | subsection | 174 | method-summary, baseline-menu | delegated | incorporate |
| 3.6 | Explanations Linearize Models in Some Way | section | 174 | attribution, linearization, unifying-axis | delegated | incorporate |
| 3.6.1 | Input Gradient | subsection | 174 | attribution, linearization, unifying-axis, inherited | delegated | incorporate |
| 3.6.2 | Integrated Gradients | subsection | 175 | attribution, linearization, unifying-axis, inherited | delegated | incorporate |
| 3.6.3 | LIME | subsection | 175 | attribution, linearization, unifying-axis, inherited | delegated | incorporate |
| 3.6.4 | SHAP | subsection | 175 | attribution, linearization, unifying-axis, inherited | delegated | incorporate |
| 3.6.5 | TCAV | subsection | 175 | attribution, linearization, unifying-axis, inherited | delegated | incorporate |
| 3.6.6 | Different Types of Linearization | subsection | 176 | linearization-types, unifying-axis | delegated | incorporate |
| 3.7 | Evaluation of Explainability Methods | section | 177 | explanation-evaluation, soundness, benchmark-design | direct | incorporate |
| 3.7.1 | Why do we need empirical evaluation? | subsection | 178 | soundness-explainability-tradeoff, evaluation-rationale | direct | incorporate |
| 3.7.2 | Types of Empirical Evaluation | subsection | 178 | evaluation-taxonomy, functional-human-application | direct | incorporate |
| 3.7.3 | Soundness Evaluation Techniques | subsection | 179 | confirmation-bias, soundness, failure-analysis | direct | incorporate |
| 3.7.4 | Evaluation of Soundness of Explanations based on Necessary Con- ditions | subsection | 181 | necessary-condition-check, soundness | direct | incorporate |
| 3.7.5 | Sanity Checks for Saliency Maps | subsection | 182 | sanity-check, evaluation-protocol | direct | incorporate |
| 3.7.6 | Simulation of Inputs with GT Explanations | subsection | 185 | ground-truth-simulation, evaluation-protocol | direct | incorporate |
| 3.7.7 | Remove-and-Classify/Remove-and-Predict | subsection | 186 | remove-and-classify, metric-definition | direct | incorporate |
| 3.7.8 | Missingness Bias | subsection | 187 | missingness-bias, validity-boundary | direct | incorporate |
| 3.8 | Soundness is Not The End of the Story | section | 188 | explanation-evaluation, end-goal, hitl-evaluation | direct | incorporate |
| 3.8.1 | Various End Goals for Explainability | subsection | 189 | end-goal-definition, relevance-criterion | direct | incorporate |
| 3.8.2 | Human-in-the-Loop (HITL) Evaluation | subsection | 189 | hitl-evaluation, protocol | direct | incorporate |
| 3.9 | Towards Interactive Explanations | section | 193 | explainability, interactive-explanation | delegated | supporting |
| 3.9.1 | A Survey on Explanations | subsection | 193 | survey-interactive | delegated | supporting |
| 3.9.2 | Generating Counterfactual Explanations with Natural Language | subsection | 194 | method-detail-interactive | delegated | supporting |
| 3.9.3 | e-ViL | subsection | 194 | dataset-reference | delegated | supporting |
| 3.9.4 | Summary of Interactive Explanations | subsection | 194 | summary-interactive | delegated | redundant |
| 3.10 | Attribution to Model Parameters | section | 195 | attribution, model-parameters | delegated | supporting |
| 3.10.1 | Explanation of Model Parameters θ | subsection | 197 | attribution, model-parameters, inherited | delegated | supporting |
| 3.10.2 | More examples of turning parameters into samples | subsection | 198 | attribution, model-parameters, inherited | delegated | supporting |
| 3.10.3 | Criticism of feature visualization | subsection | 200 | attribution, model-parameters, inherited | delegated | supporting |
| 3.11 | Attribution to Training Samples | section | 201 | attribution, training-data-influence, data-debugging | delegated | supporting |
| 3.11.1 | Why attribute to training samples? | subsection | 201 | data-debugging-rationale | delegated | incorporate |
| 3.11.2 | Basic Counterfactual Question for Attribution to Training Data – Influence Functions | subsection | 201 | attribution, training-data-influence, data-debugging, inherited | delegated | supporting |
| 3.11.3 | LISSA | subsection | 207 | attribution, training-data-influence, data-debugging, inherited | delegated | supporting |
| 3.11.4 | Arnoldi | subsection | 208 | attribution, training-data-influence, data-debugging, inherited | delegated | supporting |
| 3.11.5 | LISSA vs. Arnoldi | subsection | 210 | attribution, training-data-influence, data-debugging, inherited | delegated | supporting |
| 3.11.6 | TracIn | subsection | 210 | attribution, training-data-influence, data-debugging, inherited | delegated | supporting |
| 3.11.7 | TracIn vs. IF | subsection | 213 | attribution, training-data-influence, data-debugging, inherited | delegated | supporting |
| 3.12 | Evaluation of Attribution to Test Samples | section | 214 | explanation-evaluation, ground-truth-proxy, data-debugging | delegated | incorporate |
| 3.12.1 | Comparison of Approximation Against GT Value | subsection | 214 | ground-truth-proxy, evaluation-protocol | delegated | incorporate |
| 3.12.2 | Focus on the End Goal: Mislabeled Training Data Detection | subsection | 215 | end-goal-evaluation, mislabeled-detection | delegated | incorporate |
| 3.13 | Applications of Attribution to Test Samples | section | 217 | attribution, application | delegated | supporting |
| 4 | Uncertainty | chapter | 220 | uncertainty, calibration | direct | incorporate |
| 4.1 | Introduction to Uncertainty Estimation | section | 221 | uncertainty, use-cases, selective-prediction | delegated | incorporate |
| 4.1.1 | Motivation | subsection | 221 | uncertainty-motivation | delegated | supporting |
| 4.1.2 | Uncertainty estimation is a critical building block for many sys- tems. | subsection | 222 | downstream-systems | delegated | supporting |
| 4.1.3 | Example Use Cases of Uncertainty Estimation | subsection | 223 | use-cases, selective-prediction, active-learning | delegated | incorporate |
| 4.2 | Types and Causes of Uncertainty | section | 228 | uncertainty, aleatoric, epistemic, predictive-uncertainty | direct | incorporate |
| 4.2.1 | Predictive Uncertainty | subsection | 228 | predictive-uncertainty, definition | direct | incorporate |
| 4.2.2 | Aleatoric Uncertainty | subsection | 229 | aleatoric-uncertainty, definition | direct | incorporate |
| 4.2.3 | Epistemic Uncertainty | subsection | 233 | epistemic-uncertainty, definition, data-manifold | delegated | incorporate |
| 4.2.4 | Epistemic vs. Aleatoric Uncertainty | subsection | 237 | uncertainty-decomposition, validity-boundary | direct | incorporate |
| 4.3 | Connection of Uncertainty Estimates to Earlier Chap- ters | section | 238 | uncertainty, cross-capability-link | delegated | supporting |
| 4.3.1 | Connection of Epistemic Uncertainty to OOD Generalization | subsection | 239 | epistemic-uncertainty, ood-detection | direct | incorporate |
| 4.3.2 | Connection of General Uncertainty Estimation to Explainability | subsection | 239 | uncertainty-explainability-link | delegated | supporting |
| 4.3.3 | Trustworthiness and Confidence Estimates | subsection | 240 | trustworthiness, confidence-truthfulness | direct | incorporate |
| 4.4 | Formats of Uncertainty | section | 240 | uncertainty, output-format, evaluation-design | direct | incorporate |
| 4.5 | Proper Scoring Rules | section | 242 | proper-scoring, calibration, metric-definition | direct | incorporate |
| 4.5.1 | Motivation: Binary Forecasting Task | subsection | 243 | proper-scoring-motivation | direct | supporting |
| 4.5.2 | The Log Probability is a Strictly Proper Scoring Rule | subsection | 244 | log-probability, metric-definition | direct | incorporate |
| 4.5.3 | The Brier Score is a Strictly Proper Scoring Rule | subsection | 245 | brier-score, metric-definition | direct | incorporate |
| 4.5.4 | Role of Proper Scoring Rules | subsection | 246 | proper-scoring-role | direct | incorporate |
| 4.5.5 | Binary Cross-Entropy for True Predictive Uncertainty | subsection | 246 | bce, max-prob-confidence, metric-definition | delegated | incorporate |
| 4.5.6 | Multi-Class Cross-Entropy (CE) for True Predictive Uncertainty | subsection | 248 | cross-entropy, metric-definition | direct | incorporate |
| 4.5.7 | Strictly Proper Scoring Rules can Behave Differently | subsection | 249 | objective-vs-metric, empirical-comparison | direct | incorporate |
| 4.5.8 | Multi-Class Brier Score | subsection | 250 | multi-class-brier, metric-definition | direct | incorporate |
| 4.5.9 | Empirical Evaluation of Predictive Uncertainties | subsection | 251 | metric-interpretation, evaluation-protocol | direct | incorporate |
| 4.6 | A New Notion of Calibration | section | 254 | calibration, ece, metric-gaming, evaluation-integrity | direct | incorporate |
| 4.6.1 | Evaluating Calibration | subsection | 254 | ece, calibration-procedure | direct | incorporate |
| 4.6.2 | Gaming the ECE Metric | subsection | 256 | metric-gaming, evaluation-integrity | direct | incorporate |
| 4.6.3 | Reliability Diagrams | subsection | 257 | reliability-diagram, reporting | direct | incorporate |
| 4.7 | Summary of Evaluation Tools for the Truthfulness of Confidence | section | 259 | metric-menu, consolidation | direct | redundant |
| 4.8 | Excourse: How well-calibrated are DNNs? | section | 259 | calibration, empirical-evidence, recalibration | direct | supporting |
| 4.8.1 | On Calibration of Modern Neural Networks | subsection | 259 | nll-accuracy-disconnect, failure-analysis | direct | incorporate |
| 4.8.2 | Modern Results on Model Calibration | subsection | 261 | architecture-dependence, empirical-evidence | direct | supporting |
| 4.8.3 | Easy Fix for Better ECE: Temperature Scaling | subsection | 262 | temperature-scaling, mitigation-protocol | direct | incorporate |
| 4.9 | Do we really need proper scoring? | section | 263 | ranking-condition, error-detection, metric-definition | direct | incorporate |
| 4.9.1 | Ranking Condition | subsection | 263 | ranking-condition, weak-calibration | direct | incorporate |
| 4.9.2 | Binary Detection Metrics | subsection | 264 | auroc, aupr, metric-definition, imbalance | direct | incorporate |
| 4.10 | c(x) as Non-Predictive Uncertainty | section | 266 | non-predictive-uncertainty, ood-detection, multiplicity-detection | direct | incorporate |
| 4.10.1 | c(x) as an OOD Detector | subsection | 267 | ood-detection-benchmark, epistemic-proxy | direct | incorporate |
| 4.10.2 | c(x) as a Multiplicity Detector | subsection | 267 | multiplicity-detection-benchmark, aleatoric-proxy | direct | incorporate |
| 4.10.3 | Summary of Evaluation Methods so far for Uncertainty | subsection | 267 | metric-menu, uncertainty-evaluation | direct | incorporate |
| 4.11 | Estimating Epistemic Uncertainty | section | 268 | epistemic-uncertainty, estimator-family | delegated | supporting |
| 4.11.1 | Space of Model Parameters θ | subsection | 268 | epistemic-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.11.2 | Approximate Posterior Distribution Families | subsection | 268 | epistemic-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.11.3 | Ensembling | subsection | 271 | epistemic-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.11.4 | Dropout | subsection | 273 | epistemic-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.11.5 | Evaluation of Ensembling and Dropout in Practice | subsection | 274 | ensembling-evaluation, empirical-verdict | delegated | incorporate |
| 4.11.6 | Training an Infinite Number of Models – Bayes By Backprop | subsection | 276 | epistemic-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.11.7 | Weight Space | subsection | 283 | epistemic-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.11.8 | Training a Curve of an Infinite Number of Models | subsection | 283 | epistemic-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.11.9 | Stochastic Weight Averaging | subsection | 288 | epistemic-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.11.10 | On the Principledness of Bayesian Approaches | subsection | 290 | bayesian-principledness, validity-boundary | delegated | incorporate |
| 4.12 | Non-Bayesian Approaches to Epistemic Uncertainty: Measuring Distances in the Feature Space | section | 291 | epistemic-uncertainty, feature-distance | delegated | supporting |
| 4.12.1 | Mahalanobis Distance | subsection | 291 | epistemic-uncertainty, feature-distance, inherited | delegated | supporting |
| 4.12.2 | Other types of distances than Mahalanobis: RBF kernel | subsection | 294 | epistemic-uncertainty, feature-distance, inherited | delegated | supporting |
| 4.12.3 | Summary of Modeling Epistemic Uncertainty | subsection | 297 | epistemic-method-summary | delegated | incorporate |
| 4.13 | Modeling Aleatoric Uncertainty | section | 298 | aleatoric-uncertainty, estimator-family | delegated | supporting |
| 4.13.1 | Roadmap to Representing Aleatoric Uncertainty | subsection | 298 | aleatoric-roadmap | delegated | supporting |
| 4.13.2 | Aleatoric Uncertainty In Classification | subsection | 298 | aleatoric-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.13.3 | Detour: Proper Scoring Rules for Aleatoric and Predictive Uncer- tainty | subsection | 303 | proper-scoring-for-aleatoric, metric-definition | delegated | incorporate |
| 4.13.4 | Aleatoric Uncertainty in Regression | subsection | 305 | aleatoric-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.13.5 | Using Proper Scoring Rules to Recover N(µ(x), σ2(x)I) | subsection | 307 | aleatoric-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.13.6 | Aleatoric Uncertainty for Complex Output: Multimodal Future Prediction | subsection | 309 | aleatoric-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.13.7 | Aleatoric Uncertainty for Complex Output: Image Inpainting | subsection | 310 | aleatoric-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.13.8 | Aleatoric Uncertainty for Complex Output: 2D to 3D | subsection | 310 | aleatoric-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.13.9 | Common Challenges in Aleatoric Uncertainty | subsection | 311 | aleatoric-challenges, failure-analysis | delegated | incorporate |
| 4.13.10 | MoGs with Fixed Variance for Aleatoric Uncertainty Estimation in Regression Problems | subsection | 312 | aleatoric-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.13.11 | K-Diverse Loss | subsection | 317 | aleatoric-uncertainty, estimator-family, inherited | delegated | supporting |
| 4.14 | Aleatoric Uncertainty in Representation Learning | section | 320 | representation-learning, aleatoric-uncertainty | delegated | supporting |
| 4.14.1 | Prelude: Representation Learning | subsection | 321 | representation-learning, aleatoric-uncertainty, inherited | delegated | supporting |
| 4.14.2 | Aleatoric Uncertainty in Representation (Learning) | subsection | 322 | representation-learning, aleatoric-uncertainty, inherited | delegated | supporting |
| 4.14.3 | Multimodal Joint Representations and Aleatoric Uncertainty | subsection | 328 | representation-learning, aleatoric-uncertainty, inherited | delegated | supporting |
| 4.14.4 | Theoretical Guarantees for Recovering P(Z \| X) | subsection | 330 | theoretical-guarantee, research-showcase | delegated | out-of-scope |
| 5 | Evaluation and Scalability | chapter | 332 | evaluation-design, scalability | direct | incorporate |
| 5.1 | Benchmarks and Evaluation | section | 333 | evaluation-integrity, benchmark-design, failure-analysis | direct | incorporate |
| 5.1.1 | Why do we do evaluation? | subsection | 333 | evaluation-purpose, upper-bound-check | direct | incorporate |
| 5.1.2 | What are the costs of wrong evaluation? | subsection | 333 | cost-of-wrong-evaluation, case-evidence | direct | incorporate |
| 5.1.3 | “Recipes” for Wrong Benchmark Evaluation | subsection | 335 | benchmark-failure-modes, evaluation-integrity | direct | incorporate |
| 5.2 | Scalability | section | 338 | scalability, computational-cost, hyperparameter-tuning | direct | incorporate |
| 5.2.1 | Possible Roadmap to Scaling Up TML | subsection | 339 | scaling-roadmap, toy-vs-real | direct | incorporate |
| 5.2.2 | Simple Wins | subsection | 339 | tuned-baseline, simple-wins | direct | incorporate |
| 5.2.3 | One Right Way to Tune Hyperparameters | subsection | 341 | hyperparameter-protocol, random-search | direct | incorporate |
| 5.3 | Transition from “What” to “How” | section | 342 | problem-definition, data-ingredients, repository-scope | direct | supporting |
| 5.3.1 | Our Vision | subsection | 342 | benchmark-vs-data-hunting | direct | supporting |
| 5.3.2 | Data as Compressed Human Knowledge | subsection | 343 | data-as-knowledge, research-agenda | direct | supporting |
| 5.3.3 | Interventional Data | subsection | 344 | interventional-data, research-agenda | direct | supporting |
| 5.3.4 | Introducing Additional Supervision | subsection | 348 | additional-supervision, research-agenda | direct | supporting |
| 5.3.5 | Method-centric vs. Dataset-centric Solutions | subsection | 349 | method-vs-dataset-centric, cost-reasoning | direct | incorporate |
| A | Calculus Refresher | chapter | 351 | calculus-formalism | heading | out-of-scope |
| FM-List | List of Definitions | front/back matter | 355 | definition-index | direct | incorporate |
| FM-Bibliography | Bibliography | front/back matter | 359 | citation-index | heading | out-of-scope |

## Disposition summary

| Disposition | Headings |
|---|---:|
| `incorporate` | 132 |
| `supporting` | 104 |
| `redundant` | 2 |
| `out-of-scope` | 9 |
| `needs-body-reading` | 0 |
| **total** | **247** |

## Body-reading notes

Evidence gathered under Step 3, organised by reading cluster. Page numbers are printed book pages.
These notes are the raw material for the concept reconstruction that follows; nothing here is a
paraphrase of a heading, and every claim that later reaches an artifact is traceable to one of them.

### N1 — Deployment setting, splits and evaluation integrity (2.3, 2.5; read directly)

- Stage vocabulary is normative, not descriptive: *development* is where design choices are made
  (Def 2.14), *deployment* is where the model meets a changing environment (Def 2.15), and
  *testing* is "a lab setup designed to mimic the deployment scenario closely" (Def 2.17) which
  the book explicitly keeps **inside development** from the practice point of view (2.3.1, pp. 24-26).
- A *setting* (Def 2.18, p. 25) enumerates dev resources (datasets, labels, supervision, inductive
  bias, engineer skill), the deployment distribution, **and time**. Consequence the book draws:
  methods may only be compared when they are given the same setting; a method that consumes fewer
  dev resources cannot be compared fairly to one that consumes more (2.3.1, p. 25, "How to compare
  methods with different resources?").
- The three splits are distinguished by *what is optimised*, not by size (2.3.2, p. 26-27):
  training set → parameters, update cadence O(ms-s); validation set → hyperparameters and design
  choices, O(min-d); test set → "the methodology and overall approach through the shift of the
  field", O(months-y). For true OOD generalisation the validation set **must** come from the
  training domain(s), otherwise the target domain is being tuned on.
- 2.3.3 (p. 28) states the dilemma plainly: any decision taken from test results — including
  reading other people's test numbers — destroys the test set's meaning as a generalisation
  estimate; benchmarks are still necessary, so the achievable standard is "spoil the test set
  less", never "do not spoil it".
- Dev is modelled as a *closed system of information* (2.5, p. 35): dataset, annotation, inductive
  bias, knowledge. No new information may appear inside it, and "there is no change in the maximal
  generalization performance we can get out of this system". Note that information can also be
  *killed* (averaging, replacing measurements by summary statistics).
- Information leakage (Def 2.24, p. 36) is defined as deployment-stage information reaching dev,
  and is enumerated in four concrete patterns: (1) hyper-parameters chosen from labelled target
  samples; (2) chosen by *visually inspecting* target data ("still information leakage, just in a
  less automated way"); (3) training on target samples, labelled **or unlabelled** — which turns
  domain generalization into domain adaptation; (4) tuning to maximise publicly visible scores on
  a benchmark built from the target domain. Remedy named for (4): publish only a *ranking*, e.g. a
  hidden server (footnote 7, p. 36).
- Pretraining leakage (2.5.1, p. 37): a pretrained model imports the whole pretraining corpus into
  dev, so "zero-shot" claims must be audited against pretraining data (ImageNet-1K critique), while
  the book concedes zero-shotness may stop mattering at sufficient scale.
- Case study (2.5.2, p. 38): a published paper selects its "Feature Drop Strategy"
  hyper-parameter by the *average left-out-domain accuracy* — a full leave-one-out ablation on the
  test domains. Stated takeaway: ablation studies (Def 2.25) are safe for ID generalisation and
  dangerous for OOD generalisation, and such choices also overfit the *specific benchmark* (PACS).
- Partial solutions (2.5.3, p. 39): make hyper-parameter selection part of the learning problem and
  *specify* it when proposing a method; tune on the other domains and use the held-out domain's
  test set once per project ("a good rule of thumb might be to use it once per paper"); refresh or
  stream benchmarks and fall back on significance tests (clinical-trial analogy) instead of a
  frozen comparable test set; or noise the reported accuracy with a Laplace mechanism
  (differential-privacy evaluation).

### N2 — Generalisation-type axes and the cue problem (1.4, 2.1.2, 2.4, 2.7-2.9; direct + delegated)

- Def 2.8 *Generalization Types* (p. 18) is a 3-column axis table, not a list: ID (same
  distribution, different samples), Cross-Domain (same task, different domain), Cross-Bias
  (different cue correlations), Adversarial (worst-case test samples) — and the book flags the list
  as non-exhaustive.
- Def 2.7 ID/OOD and Def 2.5 environment/domain fix the vocabulary; Def 2.6 cue/feature/attribute
  are "characteristics of the dataset", explicitly **independent of the model** (p. 18).
- Settings taxonomy (2.4, pp. 28-35) separates *domain-dependent* (domain adaptation, domain
  generalization, test-time training, domain-incremental CL) from *task-dependent* OOD (K-shot,
  meta-learning + K-shot, task-incremental CL). The distinction is resource-based: which labels and
  how many are available, and from where.
- Def 2.27 *Spurious correlation* (p. 45): co-occurrence of cues/features/labels "which happens in
  the development stage but not in the deployment stage". Def 2.28 *Underspecification* (p. 46):
  several cues each reach 100 % training accuracy, so the data cannot say which the model will
  pick; picking the wrong one is a misspecification. Stated precondition: a very high-capacity
  network that can fit every cue.
- Def 2.29 *Shortcut (simplicity) bias* (p. 49): a preference for "simpler" cues, ordered
  Color > Scale > Shape > Orientation independent of architecture and training algorithm, explained
  through the Kolmogorov complexity of a cue approximated by the minimal parameter count needed to
  memorise the cue-labelled training set (formula on p. 50).
- Cross-bias impossibility (2.8.2, p. 47): on a diagonal dataset the perfectly aligned cues
  contradict each other, so a single model cannot use them all; if the deployment cue is unknown,
  "cross-bias generalization is not solvable" and reported success implies a hidden ingredient,
  i.e. leakage.
- Feasibility routes (2.8.3, p. 48): route 1 — a fraction ρ ∈ [0,1] of unbiased dev samples **plus
  bias/attribute labels** (Def 2.30); ρ is "part of the setting" and must be reported, task becomes
  arbitrarily hard as ρ → 0 and impossible at ρ = 0. Route 2 — grant labelled (or unlabelled) target
  samples plus per-sample domain identity, which *changes the setting* to domain adaptation or
  test-time training and therefore breaks comparability with prior DG work.
- 2.7.1 (p. 44) names the first difficulty as *ill-defined behavior on novel domains*: "It works in
  practice, but there are no rigorous theories as to why", remedy being calibrated epistemic
  uncertainty — an explicit hand-off from OOD generalization to uncertainty evaluation.

### N3 — Misspecification diagnostics and mitigation scenarios (2.10-2.14; delegated)

- Two executable diagnostics, both requiring a *disentangled* test set with task labels:
  1. **Cue-by-cue accuracy** (2.8.4, p. 49): re-label an off-diagonal test set under each candidate
     cue and compute accuracy per labelling; the signature of a learned cue is high accuracy under
     its own labelling and near-chance under all others.
  2. **Counterfactual evaluation** (2.10, p. 55-56), two strategies — *alter the task cue* (drop in
     performance is required; no drop ⇒ misspecified) and *alter the bias cue* (a drop is the
     failure signal and additionally identifies the bias). Instantiate with object removal +
     inpainting, silhouette/edge or style-transfer stimuli, or human text edits. Stated caveat:
     "Different papers do it differently" — no fixed significance threshold exists.
- Scenario frame (2.11-2.14, p. 57-77) is a **decision table keyed by available resources**, which
  is exactly the shape our SOP needs: Scenario 1 = abundant biased + ≤1 % unbiased training samples
  *with* bias labels → Group DRO / re-weighting / DANN; Scenario 2 = no bias labels → assume bias is
  the first cue a generic or myopic model learns → Learning from Failure, ReBias ("be different"
  supervision, Def 2.31/2.32); Scenario 3 = labelled test samples at deployment → train a diverse
  ensemble and select or adapt at test time.
- Group DRO (2.12.1, p. 59-61): min over θ of the *max over groups* of expected loss, with the
  empirical risk over the mixture class Q = {Σ q_g P_g}; Algorithm 1 gives the exponential-weights
  update on group sampler q. Recommended grouping when off-diagonal samples are scarce: on-diagonal
  vs off-diagonal, called "a more stable choice". Metric consequence stated by the book: Group DRO
  loses average accuracy but wins **worst-group accuracy**, where ERM "usually breaks down
  completely" under notable imbalance.
- DANN (2.12.2, p. 62-65): adversarial bias-head objective E = task loss − λ(bias loss on both
  labelled and unlabelled points) with the saddle point over (θ_f, θ_y) vs θ_d; two label
  encodings are given (bias attribute as domain, or biased-vs-unbiased as domain 1/2). The book's
  own reproduction of the source paper's tables is used to show *no significant difference* against
  NN/SVM on sentiment transfer, and large gains on the standard adaptation pairs.
- Learning from Failure (2.13.1, p. 67-70): generalized cross-entropy
  L_GCE = (1 − p_y^q)/q to build the biased model, then sample weights
  W(x) = L_CE(f_B) / (L_CE(f_B) + L_CE(f_D)); Algorithm 2 alternates both. Documented failure case:
  when task and bias roles are swapped (bias = digit, task = colour) LfF fails, and lower unbiased
  fractions increase its relative effect.
- ReBias (2.13.2, p. 70-75): HSIC-based independence between the final and a myopic biased model
  (BagNet-3 with a small receptive field), minimax form min_f max_g L(f) − L(g) + λ·HSIC, with the
  book noting the update-schedule sensitivity (n = 1 officially). Evaluation is explicitly
  **two test sets**: biased and unbiased, over several ρ values.
- "Predicting is not Understanding" (2.14.1, p. 77-85): diversity enforced on **input gradients**
  (L_indep = cos² of the two input gradients) plus an on-manifold projection loss trained through a
  VAE, because two models can be orthogonal off-manifold and identical on-manifold. The book labels
  its own evaluation as *test-time oracle model selection*, i.e. an upper bound, not an achievable
  protocol result (p. 82).
- Benchmark-design rules collected in this cluster: declare which regime a benchmark measures when
  it mixes DG and subpopulation shift (WILDS); a benchmark keyed to one model implementation
  (ImageNet-A ↔ one ResNet-50 build) is implementation-dependent; ImageNet-O's meaningful readout is
  confidence on unforeseen classes, not top-1 accuracy; oracle / train-on-target rows must be
  labelled as upper bounds; equal hyper-parameter tuning budget across compared methods (p. 64).

### N4 — Adversarial evaluation as a worst-case protocol (2.15; delegated)

- A threat model is *three named parts and no fewer* (2.15.1, p. 87-88): adversarial goal
  (Def 2.37), strategy space (Def 2.38), knowledge (Def 2.39), against a "Devil" (Def 2.36);
  "If one of them left unspecified, we are missing critical ingredients."
- Worst-case framing (2.15, p. 86): the alternative to guessing the deployment distribution is to
  prepare for the worst, which yields a lower bound **only inside the pre-set strategy space** and
  "can also lead to unrealistically pessimistic solutions".
- Attack objectives: FGSM x + ε·sgn(∇_x L(θ,x,y)) with ε bounding the L∞ magnitude (p. 89); PGD as
  constrained maximisation of the loss with projection onto the ε-ball, step size α, T iterations,
  convergence checked via ‖x_{t+1} − x_t‖₂ ≤ 1e−5 (p. 90-91). Strength ordering FGSM < PGD is
  explicit, with the reason: a single gradient step "does not even find local optima in general",
  and PGD is non-convex so "no guarantee for the globally optimal solution, even within a small
  ε-ball" — hence attack strength depends on the optimiser used.
- ε policy (2.15.4, p. 91-92): keep it small, and *fix it across studies* because results are
  compared against previous attacks and defenses.
- Reporting template (Table 2.8, p. 103): one row per defense with columns Defense / Dataset /
  **distance, norm-qualified** / Accuracy, plus footnoted semantics for "defense combined with
  adversarial training" and " theoretically 0 % accuracy in principle, nonzero only because of
  imperfections". Curves over ε or adversary strength, and matrices of train-condition ×
  test-condition, are used rather than single numbers (Fig. 2.58, 2.60, 2.63).
- Obfuscated gradients (Def 2.44, 2.15.12, pp. 102-107) is the cluster's core integrity lesson:
  three mechanisms (shattering, stochasticity, exploding/vanishing), the headline evidence that
  7 of 9 ICLR'18 defenses did not actually work, and the decisive statement that "the model being
  safe is not equivalent to no gradient-based algorithm being able to find an attack". The
  symptom to look for: naive PGD reports high robust accuracy because the gradient path is broken.
  The prescribed progression: attack the *joint* defence pipeline through differentiable
  transforms, use a straight-through estimator for quantising transforms (Def 2.46), and average
  gradients over randomised transforms (expectation-over-transformation identity, p. 107) because
  single randomised gradients are "simply too noisy".
- Defense cost ledger (2.15.11, p. 101-102): adversarial training needs T + 1 forward/backward
  passes per batch plus more epochs and often more capacity, but **no inference overhead**; it does
  not introduce obfuscated gradients, yet leaves "no guarantees" that the ε-ball is attack-free.
  BaRT (2.15.14) is explicitly *not* post-hoc: transforms are applied both at training and inference.
- Black-box evaluation must account for access and queries (2.15.8-2.15.10, p. 98-99): substitute
  models (Def 2.43) borrow assumed architecture/size/optimizer; zeroth-order gradients cost
  ~120 001 API calls for one 200×200 gradient and require logits or probabilities, not the predicted
  label.
- Certified evaluation (2.15.15, p. 110-113) replaces "no attack found" with "no attack exists in
  B_ε(x)", through a relaxation chain from the empirical robust loss to an SDP bound; the book's
  own limits: a post-hoc certificate "might be arbitrarily loose", cross-entropy training inflates
  the certified quantity without tightening the bound (hence joint regularised training), and the
  concrete result is binary-classification, two-layer-network only — "theoretically meaningful but
  not yet in practice".
- Excluded from incorporation: 2.15.16 (2014-2019 timeline and the authors' "cat-and-mouse dead
  end" position) and 2.15.17 (manifesto on less pessimistic defenses) are argument, not procedure.

### N5 — Explainability: attribution catalog, trade-off, and its evaluation (3.1-3.6 delegated; 3.7-3.8 direct; 3.9-3.13 delegated)

- Vocabulary is deliberately narrow: an explanation is "an answer to a why-question" (Def 3.1),
  interpretability is about a human *understanding the cause* (Def 3.2), explainability is the same
  degree **after receiving an explanation** (Def 3.3), and a justification (Def 3.4) "is good but
  does not necessarily … explain the actual decision-making process … also not necessarily sound".
  Attribution (Def 3.5) chooses among exactly three targets: input features, training samples, model
  parameters — this is the axis our SOP taxonomy reuses, and it is orthogonal to intrinsic/post-hoc,
  global/local, and local-vs-global perturbation (3.4, 3.5.6, 3.6.6).
- Soundness is defined model-internally, so "no attribution method that presents significantly
  simpler reasoning can be perfectly sound" (3.5.3, p. 135). The *soundness–explainability
  trade-off* (3.4.1, p. 126) is stated as a frontier: the DNN itself is sound and uninterpretable, a
  sparse global linearization is interpretable and cannot be sound, and no method may be declared
  perfect "by design" — which is the stated reason empirical evaluation is mandatory (3.7.1, p. 178).
  A second, orthogonal trade-off is interpretability vs *accuracy* (3.5.19, p. 172-173, CALM changes
  the model and loses accuracy).
- Method catalog (3.5.x, 3.10, 3.11) is incorporated as a **baseline menu with assumption lists**,
  not as procedures: input gradient (infinitesimal, non-sparse, arbitrary normalisation), SmoothGrad
  (noise-averaged, less local, more interpretable), Integrated Gradients (completeness axiom,
  baseline-sensitive), LIME (locally faithful surrogate, unstable/not continuous in the input), SHAP
  (unique under strong monotonicity + completeness — axioms the book declines to treat as
  necessities), Meaningful Perturbations, TCAV (needs concept data and linear separability of the
  concept in a chosen layer), CAM/Grad-CAM (assumes translational equivariance and unjustified
  upscaling, breaks for ViT), CALM (respects accepted axioms but costs accuracy), influence
  functions / LISSA / Arnoldi / TracIn (IF assumes convexity and twice differentiability that deep
  nets violate; TracIn trades the Hessian for checkpoints and memory).
- The evaluation cluster (3.7, read directly) is the reusable part, in increasing strength order:
  1. *Qualitative inspection* is rejected as evidence: it is confirmation bias (Def 3.13, p. 179),
     because judges look only at x and y and never at f, and no ground-truth explanation exists in
     general (chicken-and-egg, p. 181).
  2. *Necessary conditions* (3.7.4, p. 181): an explanation must depend on f; the strict version
     (randomly initialised model ⇒ informationless map) is called "probably a way too strong
     necessary condition", the relaxed version being that attribution maps must change visibly when
     the model changes.
  3. *Sanity checks* (3.7.5, pp. 182-185): cascading randomisation (randomise weights top-down and
     watch the map change) and label randomisation (a model trained on random labels must not yield
     informative maps), scored quantitatively by rank correlation between true- and random-label
     attributions. Book's verdicts: Guided Backprop and Guided Grad-CAM fail as edge detectors;
     Gradient⊙Input and Integrated Gradients are unconvincing; Grad-CAM and SmoothGrad pass.
     Explicit warning: this "seemingly simple sanity check already conflicts with the theoretically
     justified completeness axioms".
  4. *Simulated inputs with known ground truth* (3.7.6, pp. 185-186): images with a caption whose
     agreement noise p is controlled by the experimenter, so the correct attribution is known by
     construction (at p = 0 the caption must dominate; at p = 1 it must not be used).
  5. *Remove-and-Classify* (Def 3.14, 3.7.7, pp. 186-187): rank features by attribution, remove in
     that order, measure the accuracy drop relative to random erasing, summarise by AUC (lower
     better); four variants exist (most/least important first, occlude/inpaint-in, single/batched)
     and some papers average them. *Missingness bias* (3.7.8, p. 188) is the validity boundary:
     replacing pixels by the dataset mean (usually grey) can **add** information — the ResNet-50
     example predicts "crossword" from the masking pattern — so the occlusion operator is a
     hyper-parameter, ViT is far less susceptible, and "remove-and-classify is not the perfect
     soundness evaluation metric. However, it is the most popular and one of the best".
- Evaluation types are a cost/validity axis, not alternatives (3.7.2, pp. 178-179): functionally-grounded
  (proxy tasks, cheap, but "as explainability is necessarily human-grounded, such evaluations should
  only be considered **in addition to** human-grounded studies"), human-grounded, application-
  grounded. End goals (3.8.1, p. 189) are debugging, understanding (can humans *predict* the
  model's behaviour?), and trust/approach acceptance; soundness addresses only an intermediate step,
  and there is a named absence: "we have yet to see a successful use case of XAI for model
  debugging". HITL evaluation (Def 3.15) is therefore unavoidable.
- Training-data attribution is evaluated by its **end goal**, not its proxy (3.12, p. 214-217):
  approximation-vs-retraining accuracy is one axis; the second is self-influence (Def 3.16) for
  mislabelled-training-sample detection, scored with AUROC/AP — with the book's own caveat that the
  benchmark is imperfectly aligned with the quantity the method approximates, so an approximate
  method can beat the "exact" one, and that it assumes few mislabels and no systematic mislabelling.

### N6 — Uncertainty: quantities, formats, metrics (4.1-4.4, 4.5-4.10; direct unless noted)

- Three quantities, kept on separate axes: predictive uncertainty is *the model's* probability of
  being right, c(x) = P(L = 1) (Def 4.1, p. 228); aleatoric is entropy of the true P(Y | X = x) and
  is irreducible (Def 4.2, p. 229); epistemic is multiplicity of plausible models given the data,
  reducible by more supervision in underexplored regions (Def 4.3, p. 234, with Def 4.4-4.7 on
  misspecification, function space, effective function space and the data manifold). The book
  refuses the naive additive story: "the decompositions are not this straightforward and require many
  assumptions", and disentangling predictive into the two sources "is an open research topic"
  (4.2.4, p. 238).
- Format determines the evaluation (4.4, p. 240-242): scalar c(x) ∈ [0,1] (probability of
  correctness, hence any scalar may be treated as a probability); vector c(x) ∈ R^d (per-evidence
  confidence — which attribute the model lacks); matrix + vector, probabilistic embeddings
  P(z | x) = N(µ_θ(x), Σ_θ(x)) with Σ representing aleatoric uncertainty in the embedding; and a
  "disentangled" pair c(x) = c_al(x) + c_ep(x) where c_al is the average learned variance and c_ep
  the variance of ensemble means, with the footnote that these only *approximate* the true
  quantities and "their faithfulness is subject to evaluation".
- Strict propriety is the mechanism that makes an estimate truthful (Def 4.8, p. 243): P is one of
  the maximisers / the unique maximiser of E_P S(Q, Y). Instantiations with formulas in the text:
  log probability S = y log q + (1−y) log(1−q) (4.5.2, p. 245, proved strictly proper), Brier
  S = −(q − y)² (4.5.3, p. 246), BCE for max-prob c(x) = max(f(x), 1−f(x)) (Def 4.9, 4.5.5,
  p. 246-247), multi-class CE as a lower bound of the log-probability score (4.5.6, p. 248), and
  the multi-class Brier score with its analogous lower-bound claim (4.5.8, p. 251).
- "Not all strictly proper scoring rules are equally good training objectives" (4.5.7, pp. 249-250) —
  demonstrated by a tuned comparison where the max-prob formulation reaches 54 % on CIFAR-10 against
  67 % for NLL training, on a noisier loss surface. Numerical optimisation, not just the metric, is
  part of the evaluation design.
- Metric interpretation limits are stated for each family (4.5.9, p. 253-254): NLL/Brier have no
  knowable floor because the true aleatoric term is unknown; they mix accuracy and calibration
  (which is why "larger LLMs have lower perplexity" cannot be read as better uncertainty); and
  because the Bayes predictor is a maximiser of both predictive and aleatoric scores, proper scoring
  says nothing about epistemic uncertainty.
- Calibration is the interpretable but gameable alternative (4.6): perfect calibration
  P(Ŷ = Y | C = c) = c (Def 4.11), model calibration as an integral of the deviation (Def 4.12),
  ECE as its binned approximation (Def 4.13) with a 5-step practical recipe (typically M = 10 bins,
  bin-weighted mean of |acc(B_m) − conf(B_m)|), MCE as the worst-bin variant for high-risk use
  (Def 4.14), and the reliability diagram (Def 4.15) which reveals the sign of miscalibration and
  the MCE but not the ECE because bin weights are invisible. Two named integrity failures: **gaming
  ECE** by emitting the constant c = P(Ŷ = Y), which needs no labelled validation data at all and
  yields ECE = 0 while per-sample c(x) is arbitrarily wrong; and **bin-count dependence**
  ("Using twenty bins gives us a different score than using ten"), with the book observing that
  papers are inconsistent (15 bins in the table it reproduces) and recommending finer bins near
  90-100 %.
- Empirical calibration evidence (4.8): modern networks can overfit NLL while accuracy keeps
  improving — "the network learns better classification accuracy at the expense of well-modelled
  probabilities" (4.8.1, pp. 259-261) — calibration varies by architecture family (4.8.2, pp. 261-262), and
  temperature scaling f(x;T) = softmax(g(x)/T) with T chosen by grid search on a validation set to
  minimise ECE is the cheap fix (4.8.3, p. 263, 8-10 % → sub-2 % ECE). The protocol detail that
  matters for benchmark integrity: T is fitted on **validation** data, never on the test set.
- The ranking condition (4.9.1, pp. 263-264) is the weaker requirement — preserve the order of
  P(L = 1 | x) — which is "sufficient for many applications, such as when we filter out too-uncertain
  examples via a threshold", and is equivalent to calibration up to an unknown monotone g. It turns
  evaluation into a binary detection problem of L from feature c (4.9.2, pp. 264-266): TP/FP/FN/TN sets,
  precision/recall curves, AUPR-Success and AUPR-Error, ROC and AUROC, with the imbalance rule
  recorded verbatim in both directions — random-detector AUPR = P(L = 1), so AUPR "lacks the
  resolution" under severe imbalance, hence "AUROC the recommended metric over AUPR, especially on
  unbalanced datasets"; and the AP corner case (undefined precision at empty thresholds) resurfaces
  in 5.1.3 as a reason to share one metric implementation.
- Non-predictive uncertainty gets its own benchmarks (4.10, pp. 266-268): the *same* confidence score
  may be scored as an OOD detector (Y = "outside the training distribution", epistemic proxy) or as a
  multiplicity detector (Y = "several true answers", aleatoric proxy), each with AUPR/AUROC, and the
  book repeatedly warns that these quantities are "not perfectly aligned" with predictive
  uncertainty. 4.10.3 consolidates the metric menu: proper scoring, calibration metrics, ranking.

### N7 — Uncertainty estimators and scalability (4.1-4.3, 4.11-4.14 delegated; 5.1-5.3 direct)

- Use cases set the *contract*, and the contract is what makes a benchmark necessary: every module
  must emit prediction **and** uncertainty (4.1.2, p. 222); abstention is preferred under asymmetric
  cost (Table 4.1, p. 224: predict-healthy-when-diseased costs 10 vs 0.5 to abstain); scores must be
  comparable across candidates for pruning (objectness, p. 227); open-set recognition without an
  explicit "I don't know" class relies on calibrated uncertainty and "will likely produce worse
  results" than the supervised variant (p. 225). The three questions an uncertainty explanation must
  answer are listed (4.3.2, p. 239): how uncertain, due to which factor, and what extra data would
  help.
- Epistemic estimators (4.11-4.12) are evaluated with an explicit verdict per family, and the
  verdicts are the reusable part: MC dropout "does not really work" and plateaus below ensembling
  (4.11.5, p. 275); ensembling scales cost linearly in M and "does not scale nicely" while
  implicitly treating the initialisation scheme as the prior; BBB's diagonal Gaussian posterior fails
  when the true posterior is elongated and reverse KL "squishes" it, and is "not a better solution
  than the ensemble method" (4.11.6, p. 281-282); SWAG-Diag is "sadly very similar to SGD" on the
  reliability diagram, so the cheap variant buys scale, not quality (4.11.9, p. 290); Mahalanobis and
  DUQ-style feature distances beat max-prob on OOD detection but "conflate OOD with high aleatoric
  ambiguity" and must not be generalised from one dataset pair (4.12.1-4.12.2, p. 292-296).
  4.11.10 (p. 290) states the principledness bar as two assumptions — a sensible prior and a
  posterior inside the chosen family — neither verifiable in deep networks.
- Aleatoric modeling (4.13) reduces to a two-ingredient recipe (4.13.1, p. 298): output the
  parameters of the predictive distribution, and train with a proper scoring rule for it.
  Heteroscedastic Gaussian NLL, (1/2σ̂²)‖y − µ̂‖² + (d/2)log σ̂², is recommended for regression with
  the precondition of enough data and limited capacity, because the log-variance term "prevents the
  model from saying that every sample is hard" (4.13.5, p. 307-308). A transfer result with a hard
  boundary: any strictly proper aleatoric rule is also strictly proper for max-prob predictive
  uncertainty, but the converse holds **only in the binary case** (4.13.3, p. 303-305, with explicit
  3-class counterexamples). Mixture-of-Gaussians with fixed variance needs a stop-gradient in the
  expert weighting and a catch-up term to stop experts collapsing onto a constant (4.13.10-4.13.11,
  p. 314-317). 4.13.9 (p. 311) records the difficulty of multimodal, high-dimensional aleatoric
  estimation as a single explicit paragraph.
- 4.14 (probabilistic embeddings, p. 320-331) is a research showcase, not a procedure — the book's
  own honesty flag is decisive: "we now have **no guarantee of propriety**", evaluation is
  qualitative (variance grows with corruption), and the recovery theorem needs vMF posteriors,
  uniform marginals and M → ∞. Only the corruption-based ambiguity protocol and its seen/unseen
  class split are worth carrying over.
- Scalability and evaluation discipline (5.1-5.3, read directly) supply the benchmark-integrity
  backbone:
  - Purpose of evaluation is a *1-D ranking* of methods, checked against human performance or a
    theoretical upper bound; exceeding an upper bound forces an explanation — evaluation bug, flawed
    bound, or a different set of ingredients (5.1.1, p. 333).
  - Cost of wrong evaluation is quantified as wasted effort (4+ years in deep metric learning),
    opportunity cost, and practitioners mis-selecting methods (5.1.2, pp. 333-335), with a named list
    of eight "evaluation scandals" across CV/NLP.
  - 5.1.3 (pp. 335-338) enumerates the failure modes as a checklist: per-paper metric
    implementations (with the AP-empty-bin corner case) → use one shared evaluation library or
    server; confounding factors (different backbones while claiming a loss-function gain); hiding
    extra resources, i.e. reporting accuracy without latency/compute; train-test contamination
    (>50 % answer overlap reported for Natural Questions/TriviaQA/WebQuestions, with models scoring
    0 % on the non-overlapping subset); and missing validation sets, where ImageNet's "validation"
    set *is* the de-facto test set and re-collected second versions (ImageNet v2, CIFAR v2) show a
    systematic drop below the identity line — evidence of accumulated test-set overfitting.
  - Practical pointers (5.1.3, pp. 335-338): before trusting a field's benchmark, look for a fair
    re-evaluation paper; if none exists, either produce one, or trust it only because the task and
    its ingredients are simple, or stay sceptical.
  - Simple wins (5.2.2, pp. 339-341): fairly tuned ERM — "the simplest method — is not worse at all"
    — and the untuned-baseline pathology, where an unoptimised default (learning rate 0.1, weight
    decay 1e−4) is reported as the baseline; weight decay is singled out as routinely omitted and
    decisive.
  - 5.2.3 (pp. 341-342): the tuning protocol the book endorses is random search over per-parameter
    *sensible exponential ranges* with a **fixed sample budget shared by all compared methods**,
    justified because only a few hyper-parameters matter; stated preconditions are approximate
    unimodality and independence, and the fallback for wiggly regions is Bayesian optimisation.
  - Toy vs real trade-off (5.2, p. 338-340): toy datasets buy rich per-sample labels (task label plus
    domain/bias attributes), speed and controlled ablation; large-scale data costs days-to-weeks per
    validation and loses factor analysis, so scaled-up methods must be simple. This is the source of
    our "report the data regime, do not transfer a ranking between regimes" rule.
  - Method-centric vs dataset-centric solutions (5.3.5, p. 349-350): a fixed benchmark imposes an
    information cap, so scaling complicated methods fails; adding supervision (the "How", Z) is the
    way to raise the cap. 5.3.1 (pp. 342-343) also states that letting competitors use extra
    ingredients is no longer a benchmark — "It is unfair" — which is the cleanest source statement of
    the equal-ingredients rule.

### Fidelity flags (recorded, not silently repaired)

1. **`ρ` semantics conflict inside §2.13.2.** The caption of Table 2.5 (p. 74) says ρ is the fraction
   of *unbiased* samples, while the reproduced numbers behave as if ρ were the fraction of *biased*
   samples (vanilla biased accuracy 100 % and unbiased accuracy ≈ chance at ρ = 0.999). Any artifact
   that uses ρ must define it explicitly and not inherit the book's symbol.
2. **PGD has no numerical recipe in this source.** §2.15.3 names the knobs (α, T, projection,
   clipping, a ‖x_{t+1} − x_t‖₂ ≤ 1e−5 stopping test) but gives no default values, margin rule, or
   restart count. Our benchmarks therefore require "report the attack configuration" rather than
   prescribing numbers we would be inventing.
3. **The certified-defense result is scope-limited.** The bound chain in §2.15.15 is demonstrated for
   binary classification with a two-layer network; the book itself says it is "theoretically
   meaningful but not yet in practice".
4. **`3.13` heading/content mismatch** (applications of attribution to *test* samples, body about
   training samples) — kept as printed, flagged in the table.
5. **ECE bin count is not fixed by the source** (10 typical, 15 in the reproduced table); we record
   it as a required disclosure, not a constant.
6. **Calibration literature is contradictory by design**: 4.8.1 (older models better calibrated) vs
   4.8.2 (modern families better calibrated). The audit treats this as evidence for "report
   architecture family and recalibration status", not as a single claim.

### N8 — Metric and definition inventory (source-grounded backbone)

| Quantity to be measured | Metric as the source defines it | Formula / recipe | Source |
|---|---|---|---|
| Truthfulness of a probability report | Strictly proper scoring rule | `arg max_Q E_P S(Q,Y) = P` uniquely | Def 4.8, 4.5.1 p. 243 |
| Predictive uncertainty (binary) | Log probability / BCE | `S = y log q + (1−y) log(1−q)`; `L = −log f(x)` if y=1 else `−log(1−f(x))` | 4.5.2 p. 245; Def 4.9 p. 246 |
| Predictive uncertainty (binary) | Brier score | `S(q,y) = −(q−y)²` | 4.5.3 p. 246 |
| Predictive uncertainty (multi-class) | NLL / CE (lower bound of the max-prob score), perplexity as its exponentiation | `L_NLL = −(1/N)Σ log f_{y_i}(x_i)`; `L_Ppl = 2^{−(1/N)Σ log₂ f_{y_i}(x_i)}` | 4.5.6 p. 248; 4.5.9 p. 253 |
| Predictive uncertainty (multi-class) | Multi-class Brier | `S = −(1−f_y)² − Σ_{k≠y} f_k²` | 4.5.8 p. 251 |
| Group-wise correctness | Worst-group accuracy vs average accuracy | max-group risk objective `min_θ max_g E_{P_g}[ℓ]` | 2.12.1 p. 59-61 |
| Calibration | ECE | `Σ_m (\|B_m\|/n)\|acc(B_m) − conf(B_m)\|`, M bins, 5-step recipe | Def 4.13, 4.6.1 p. 255 |
| Calibration, worst bin | MCE | `max_m \|acc(B_m) − conf(B_m)\|` | Def 4.14 p. 256 |
| Calibration, signed picture | Reliability diagram (+ confidence histogram mandatory) | binned `acc(B_m)` vs `conf(B_m)−acc(B_m)` barplot | Def 4.15, 4.6.3 p. 257 |
| Ranking of correctness by confidence | AUROC (preferred), AUPR-Success / AUPR-Error | `TP/FP/FN/TN(t)` sets; `AUROC = P(c > c&#39; \| L=1, L&#39;=0)`; random AUPR = `P(L=1)`, random AUROC = 0.5 | 4.9.2 pp. 264-266 |
| Epistemic quality (proxy) | OOD-detection AUROC/AUPR of `1−c(x)` | binary task `Y = 1[x outside training distribution]` | 4.10.1 p. 267 |
| Aleatoric quality (proxy) | Multiplicity / corruption detection AUROC/AUPR | binary task `Y = 1[several true labels for x]` | 4.10.2 p. 267 |
| Aleatoric recovery (regression) | Heteroscedastic Gaussian NLL | `(1/2σ̂²)‖y−µ̂‖² + (d/2) log σ̂² + C` | 4.13.5 p. 307 |
| Robustness to perturbation | Accuracy under attack at a norm-qualified ε; sweep over ε | `max_{‖δ‖_p ≤ ε, x+δ∈[0,1]} L(f(x+δ),y)` | 2.15.3 p. 90; Table 2.8 p. 103 |
| Robustness, sound claim | Certified robust accuracy | bound chain `Ã(A(x)) ≤ Ã(x) + ε‖∇Ã‖₁ ≤ … ≤ Ã_SDP(x)` | 2.15.15 p. 111 |
| Explanation dependence on the model | Sanity-check rank correlation (label & weight randomisation) | Kendall-type rank correlation of maps, true vs random labels | 3.7.5 pp. 182-185 |
| Explanation soundness (ordering) | Remove-and-Classify relative accuracy drop, AUC lower-better | iterative occlusion in attribution rank vs random erasing | Def 3.14, 3.7.7 p. 186 |
| Explanation usefulness to humans | HITL / application-grounded task performance | human accuracy or behaviour change with vs without the explanation | Def 3.15, 3.8.2 p. 189 |
| Training-data attribution usefulness | Self-influence mislabel detection | AUROC / AP over self-influence scores | Def 3.16, 3.12.2 p. 216 |
| Calibration repair | Temperature scaling | `f(x;T) = softmax(g(x)/T)`, T grid-searched on validation to minimise ECE | 4.8.3 pp. 262-263 |

## Gate A — Source Coverage

| Condition | Result | Evidence |
|---|---|---|
| Complete available heading hierarchy captured | PASS | 247 headings recovered from font metadata; 49/49 sections agree with the printed TOC |
| Every heading has a disposition | PASS | 0 rows left at `needs-body-reading` |
| Ambiguous / methodologically important headings checked against body text | PASS | 89 direct + 144 delegated body reads out of 247 headings |
| No SOP or Benchmark drafting started before this gate | PASS | `SOP/Trustworthy-ML-2023/` and `Benchmark/Trustworthy-ML-2023/` do not exist while this file is produced |
