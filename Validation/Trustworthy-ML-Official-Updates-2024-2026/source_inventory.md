# Source inventory — official post-book TML material, 2024/25 and 2026

Source-audit record. Read on 2026-09-23. Nothing in this file was inferred from a
title: every row states what was actually opened, and anything that could not be opened is marked
`PARTIAL` or `NO` with the routes that were tried.

**Lineage.** The book *Trustworthy Machine Learning* (2023) is the material of an earlier edition of
the same course. The current official pages for the course live under the STAI group site
(`stai-lab.org/courses/…`), whose published source is the `S-T-A-I/s-t-a-i.github.io` repository; both
the rendered page and that source file were read. The group is now at KAIST AI, so the 2026 edition is
a KAIST AI course page rather than a Tübingen one — recorded below, with the Tübingen-side 2026 page
listed as not found rather than assumed.

**Reading method, because it affects what "accessed" means.** Course pages were read in full as text.
Lecture decks are Google Slides, publicly readable; they were read through the presentation's own text
export. That export drops anything drawn rather than typed, so every deck row below records which
formulas and figures were lost. Slide decks and notebook bodies are **not** committed here; only
extracted facts and short quoted phrases are.

## 1. Registry

| ID | Year | Institution | Material | Access |
|---|---|---|---|---|
| TML2425-PAGE | 2024/25 | U. Tübingen | Course page (overview, policies, grading, schedule, exercise links) | **FULL** |
| TML2425-L5 | 2024/25 | U. Tübingen | Lecture deck: OOD (Attacking LLMs) & Explainability (Definitions) | **FULL text**, formulas lost |
| TML2425-L1..L4,L6..L12 | 2024/25 | U. Tübingen | Eleven other lecture decks | **PARTIAL** (title + link only) |
| TML2425-VID | 2024/25 | U. Tübingen | Twelve lecture videos + recap videos (YouTube) | **PARTIAL** (link inventory; not watched) |
| TML2425-EX0 | 2024/25 | U. Tübingen | Exercise 0 notebook (Kaggle, `seongjoonoh/0-prelim`) | **NO** |
| TML2425-EX1 | 2024/25 | U. Tübingen | Exercise 1 — OOD (Kaggle, `johannestml/1-ood`) | **NO** (title + attached-dataset metadata only) |
| TML2425-EX2 | 2024/25 | U. Tübingen | Exercise 2 — XAI (Kaggle, `aktsonthalia/tml2425-exercise-2-xai-public`) | **NO** for the notebook body |
| TML2425-EX2-SCAFFOLD | 2024/25 | U. Tübingen | Tutor's public utility package `tml2425_xai` (GitHub) | **FULL** for the source files read |
| TML2425-EX3 | 2024/25 | U. Tübingen | Exercise 3 — Uncertainty (Kaggle, `lennartbramlage/3-uncertainty`) | **NO** |
| TML2324-PAGE | 2023/24 | U. Tübingen | Course page, used as the book-era historical control | **FULL** |
| TML26-PAGE | 2026 | KAIST AI | Course page (schedule, grading rubric, project topics, AI policy) | **FULL** |
| TML26-L4 | 2026 | KAIST AI | Deck: LLM Communication & Modularity | **FULL text**, formulas lost |
| TML26-L11 | 2026 | KAIST AI | Deck: Uncertainty for Foundational Models | **FULL text**, formulas lost |
| TML26-L12 | 2026 | KAIST AI | Deck: Security & Adversarial Robustness | **FULL text**, formulas lost |
| TML26-L13 | 2026 | KAIST AI | Deck: Privacy & Data Protection | **FULL text**, formulas lost |
| TML26-L6 | 2026 | KAIST AI | Deck: Attribution Methods | **FULL text**, formulas lost |
| TML26-L7 | 2026 | KAIST AI | Deck: Training Data Attribution | **FULL text**, formulas lost |
| TML26-L2,L3,L5,L8..L10 | 2026 | KAIST AI | Six other decks | **PARTIAL** (title + link only) |
| TML26-VID | 2026 | KAIST AI | Thirteen Drive-hosted session recordings | **PARTIAL** (link inventory; not watched) |
| TML26-PROJECT | 2026 | KAIST AI | Project brief: teams, compute, deliverables, five example topics | **FULL** (part of TML26-PAGE) |
| TML26-RUBRIC | 2026 | KAIST AI | Grading rubric: 4 components, 5-point scale, per-criterion anchors | **FULL** (part of TML26-PAGE) |

Canonical URLs. TML2425-PAGE `https://stai-lab.org/courses/tml_winter_2425/`; TML2324-PAGE
`https://stai-lab.org/courses/tml_winter_2324/`; TML26-PAGE
`https://stai-lab.org/courses/tml_spring_26/`. Deck URLs are the `docs.google.com/presentation/d/…`
links printed in each page's schedule table; the four 2026 decks and TML2425-L5 were read through that
schedule, so each is reachable from its page.

## 2. What each accessed source actually contains

### TML2425-PAGE — University of Tübingen, Winter Semester 2024/25

Lecturer Seong Joon Oh; tutors Johannes (OOD generalisation), Ankit (explainability), Lennart
(uncertainty). Thursdays, lecture plus a two-hour tutorial; two written exams with a use-the-best rule.

Relationship to the book, in the page's own words: "Last year's course materials are now a book", and
"The course materials are updated yearly to stay aligned with the latest research. The book will be
useful for the TML24/25 course. However, it won't cover new topics added to the course." This is the
explicit licence to treat later material as an update source and the explicit reason it is not book
content.

Schedule structure: three blocks — OOD generalisation (L2–L5), explainability (L5–L8), uncertainty
(L9–L11) — then L12 "Conclusion (Exam, Research at STAI, Project topics)". Exercises 1–3 are released
at L2, L5 and L9 with due dates 20.11.2024, 11.12.2024 and 30.01.2025, each introduced in a tutorial
and recapped in a later tutorial; the recap sessions have no linked slides or video on the page.

Concrete requirements the page states: Exercise 0 submission is the minimal requirement to sit the
exam; exam admission needs Exercise 0 **and** an average exercise score `E ≥ 60%`; top-up
`T = (E − 60%)/40% × 10%p`; final `S = min(100%, X + T)`; the exam pass needs `X ≥ 50%` independent of
exercise performance. Language-model use is permitted for exercises under four guidelines: transparency
about which models were used and which text or code was generated, rigorous verification, adding a
personal touch to reduce identical submissions, and "Don't use them as your primary source for
verification."

No per-exercise rubric, point weights or submission format appear on the page.

### TML2425-L5 — "OOD Generalisation (Attacking LLMs) & Explainability (Definitions)"

Two halves. The attack half teaches the suffix-optimisation family: the objective is the negative
log-likelihood of a desired target output minimised over suffix tokens, per-position gradients are taken
against all vocabulary tokens, top-k candidates are kept, then a greedy coordinate variant, then a
multi-model index `p` for transferability and a multi-prompt index `m` for universality. Named paper:
"Universal and Transferable Adversarial Attacks on Aligned Language Models" (arXiv 2023); "Obfuscated
Gradients Give a False Sense of Security" (ICML 2018) is used to invalidate naive defense claims.
Caveats stated: "Naive gradient descent doesn't work because the input is discrete"; "Since inputs are
discrete (only one-hot vectors allowed), there's mismatch"; "Playing cat & mouse game is a dead end";
"Defense against general adversary is ultimately impossible." Practitioner rules on the same deck:
serve the model black-box, keep parameters/dataset/architecture secret, content filtering, periodic
updates, "Maintain an internal red team."

The explainability half defines interpretable versus non-interpretable function classes, separates
interpretability from explainability, and imports a social-science account of what makes an explanation
acceptable to a human. Two rival evaluation regimes are named as opposites: "End-to-end evaluation. How
well does the XAI technique help practitioners achieve the end goal?" versus "Unit tests of general XAI
benefits. Modular evaluation." Faithfulness is stated as a requirement — the method "must cite the true
cause" — and efficiency is required to be measured over all additional resources, itemised as one-time
or per-case time, memory, storage and manpower. Caveats: "Evaluation is application- and
user-dependent. Lacks replicability"; "May not directly reflect the practical usefulness"; "Perfect
faithfulness mirrors complex model computations, often beyond human understanding"; "If they have to
wait too long for the explanation, they will not use it."

Formulas are drawn rather than typed and are absent from the text export; five "Examples" slides are
image-only.

### TML2324-PAGE — book-era control

Same three blocks, same exercise architecture, same language-model policy wording, same grading
arithmetic. Two differences that matter for version comparison: the adversarial content is titled
"OOD Generalisation (Adversarial attacks)" and "…(Adversarial defenses)" with no LLM session, and there
is no privacy or security part at all. Exercises are Google-Colab documents rather than Kaggle
notebooks, and a recap slide deck for Exercise 1 is linked. No project topics, no rubric: the assessment
is exam-based.

### TML26-PAGE / TML26-PROJECT / TML26-RUBRIC — KAIST AI, Spring Semester 2026

Subtitle: "Bridging the Communication Gap in Deploying General AI". The description frames the course as
three broken channels — human→AI (underspecification), AI→human (unexplainability and overconfidence),
environment (privacy leaks and security attacks). Lecturer Seong Joon Oh; four KAIST tutors; Fridays
online; thirteen content sessions plus proposal and final presentation sessions. Relationship to the
book: "Previous course materials are available as a book … the course materials are updated yearly to
stay aligned with the latest research, so it won't cover new topics."

Session list, since the shape is the evidence: L2 ML foundations & generalisation; L3 Underspecification
& Cues; **L4 LLM Communication & Modularity**; L5 Explanation & XAI; L6 Attribution Methods; L7 Training
Data Attribution; L9 Uncertainty Estimation; L10 Epistemic & Aleatoric Uncertainty; **L11 Uncertainty
for Foundational Models**; **L12 Security & Adversarial Robustness**; **L13 Privacy & Data Protection**.

The course is now project-assessed, not exam-assessed. Teams of three, 50 USD GCP voucher per student,
ICML 2026 LaTeX format, proposal 1–2 pages plus a 5-minute talk, final 4 pages excluding references plus
a 10-minute talk and Q&A, and a mandatory peer evaluation distributing 100 points across the team where
"Unequal splits will affect individual grades."

Rubric, which is the load-bearing part for this repository. Weights: proposal presentation 15%,
proposal report 15%, final presentation 35%, final report 35%. All criteria use a 5-point scale, equally
weighted within a component. The final-report criteria, quoted at the level that constrains behaviour:
experimental design asks "Are experiments well-designed with appropriate baselines? Are results presented
clearly (tables, figures, error bars where applicable)?" with the 1-anchor "Missing or poorly designed
experiments"; analysis asks the team to "interpret their results, discuss limitations, and reflect on
what worked and what did not" with the 5-anchor "Thoughtful analysis that goes beyond 'method X got
accuracy Y'"; technical depth asks "Are technical choices justified?"; writing quality requires figures
and tables to be captioned and referenced and penalises "AI slop". The proposal report must state
"model choice, data, metrics, and experimental design" and show related-work awareness where "A full
literature review is not expected, but awareness of the landscape is." Late work is not accepted and a
missed deadline is a zero.

What the rubric does **not** require anywhere: reproducibility artifacts, code hand-in, seed or variance
protocols, or statistical tests. That absence is a finding, not an oversight in this audit — it bounds
how far the rubric can be cited as an experimental-design standard.

The five example project topics, each with its own evaluation ask, models, datasets and cited papers:

1. **Test-time detection of prompt sensitivity.** The open question is stated as "whether we can detect
   *at test time* that a prediction is prompt-sensitive and flag it to the user, without access to
   ground truth. Propose and evaluate a detection method." CLIP ViT-B/32 and LLaVA-7B on a single T4;
   ImageNet/EuroSAT zero-shot; cites PARC (CVPR 2025) and WaffleCLIP (ICCV 2023).
2. **Surfacing knowledge conflicts in RAG.** Against work that "resolves parametric-contextual conflicts
   silently", the ask is "whether the system can instead *detect and surface* the conflict to the user,
   letting them decide. Build a conflict-detection pipeline and evaluate its precision." Llama 3.1 8B or
   Mistral 7B with a FAISS index; Natural Questions/TriviaQA "with synthetically altered retrieval
   passages"; cites FaithfulRAG (ACL 2025), AdaCAD (NAACL 2025), JuICE (ICML 2025).
3. **Mechanistic vs data attribution for the same failure.** "These perspectives are rarely compared.
   Pick a failure mode (e.g. hallucination, gender bias) and apply both attribution families to the same
   cases. Do they agree?" Cites Accountability Attribution (ICML 2025) and DDA (EMNLP 2024).
4. **Confidence under distribution shift.** "Methods like BaseCal and EAGLE improve calibration on
   in-distribution data. Less is known about how confidence estimates degrade under distribution shift
   or across multi-turn conversations. Evaluate existing calibration methods on shifted inputs and
   propose a detection strategy." Notes the cost explicitly: sampling methods "need ~20-50 forward
   passes per input; budget for this". Cites IB-EDL (ICLR 2025), Multicalibration (ICML 2024).
5. **Paper reproduction.** "Verify the claims, test on a different model or dataset, and report where
   the results hold and where they break. Choose a paper whose experiments fit the compute budget."

AI policy penalises "Hallucinated or factually incorrect outputs", "Unsound or fabricated citations",
plagiarised material and AI slop; "Inability to explain your own work will be treated as evidence of
academic misconduct."

### TML26-L4 — "LLM Communication & Modularity"

Frames a modular-versus-monolithic spectrum along four design axes — what is decomposed, when, how
tightly coupled, and who does it — with RAG, tool use, LoRA and MoE as the named method families.
Underspecification is split into three layers and reduced by prompting, dialogue or structured context.
Evaluation content is thin: "Test entropy of prediction is related to error rate / OODness"; MoE load
balancing is "Optimal when marginal router prob is uniform"; "Programmatic checks on intermediate steps
to control the quality"; voting means "Running the same task multiple times to get diverse outputs". No
metric, dataset or baseline is named. Caveats worth carrying: "The problem is ill-posed without 'OOD'
signal", "Entropy minimisation for a single sample results in one-hot prediction", "TENT requires
availability of a batch of test samples", "Modularity is a design overlay, not a fundamental
decomposition", and that natural language is "rich but ambiguous & uncompressed". One cited arXiv
identifier is forward-dated and could not be resolved; it is recorded as unread rather than smoothed
over.

### TML26-L6 / TML26-L7 — "Attribution Methods" and "Training Data Attribution"

Read specifically to test whether cross-attribution-family agreement is taught. It is not: neither deck
contains the words agree, disagree, compare, cross-family or consistency in an evaluative sense. What
they do contain is book-era material — integrated-gradients style baseline axioms ("Pixel-wise
contributions for x must sum up to the difference between the current model output f(x) and some baseline
output f(x0)", "How to set the baseline x0?"), a perfect-faithfulness case, TDA evaluation criteria
including "One could measure correlation to generate a scalar metric" with Pearson and Spearman named,
"Leave-many-out evaluation for greater stability", and the influence-function/TracIn line of methods
("TracIn sums over training iterations (checkpoints) and does not use Hessian-based distortion of
metric"). These are the same evaluation problems `SOP-07` and `BM-06` already own, so the decks function
here as confirmation of coverage rather than as a source of new protocol.

### TML26-L11 — "Uncertainty for Foundational Models"

The deck's thesis is that the epistemic/aleatoric decomposition does not survive contact with practice.
It states the desired identity for predictive, aleatoric and epistemic uncertainty, then makes the
disentanglement check an empirical one: "Suppose AU and EU estimators were truly disentangled. Then a
method designed for one should not be predictive of the other", reported over "19 UQ methods x 14
aggregators / 13 tasks / ImageNet-1k and CIFAR-10", with the failure measured as rank correlation
("≥ 0.78", and "On CIFAR-10, 11/12 methods exceed 0.88"). For LLMs it names a comparison
("llama-3.1-8B-Instruct, on five datasets, evaluated with AUROC and AUARC" — AUARC is never defined in
the text), groups methods into verbalised, latent and consistency families, notes the sampling cost
("Expensive: M forward passes per query"), and anchors ambiguity detection against chance ("57% times
(Chance: 50%)"). Procedure statements: "Decide the downstream task first. Pick the estimator second";
"Validate calibration on the actual downstream metric"; "Be honest about what 'uncertainty' means in
your setting"; and an access-level split, black-box for semantic clustering/consistency/verbalised,
white-box for latent. Caveats: "There is no universal uncertainty estimator", "A method that wins on OOD
detection often loses on aleatoric alignment", "Confounded by length", "The decomposition formulas
themselves are the failure mode, not the dataset", "The dichotomy collapses under interaction",
"Corpus disagreement, stylistic variation, and genuine indeterminacy are indistinguishable in the
estimate", and for multi-agent systems "Even if individual agents do report UQ, orchestrator fails to
process it."

### TML26-L12 — "Security & Adversarial Robustness"

The deck that formalises the threat model: three declared components — adversarial goal, strategy space,
knowledge — where the goal is either "making model misbehave (security)" or "leaking information
(privacy)". It gives the knowledge ladder from nothing, to task, to architecture, to rough
training-data information, to actual training samples, to input-output pairs; the ε budget ("It
determines the L-inf norm of the attack"); the strength ordering "PGD is generally much stronger than
FGSM"; the plausibility question "Do such adversaries exist in the real world?"; and the transfer
requirement "In transfer attack, one must generalise across models, rather than across data". The
guarantee caveat is explicit: "The guarantee is only within the pre-set space of possible environments",
plus "Optimisation problem for adversary is non-convex. No guarantee for the optimal solution, even
within an epsilon ball (it's not tiny in a high-dim space)", "Strength of the attack depends a lot on the
optimisation algorithm", and "Problem with Lp ball: it is not aligned with human's perception". LLM
attacks appear as prompt-structure attacks, jailbreaking and the same suffix-optimisation thread taught
in 2024/25, plus indirect prompt injection motivated by a named production incident. The
practice mandates repeat the 2024/25 list (black-box serving, secret details, content filtering,
periodic updates, internal red team).

### TML26-L13 — "Privacy & Data Protection"

A privacy evaluation family with its own targets and units, which is why it cannot be folded into the
robustness benchmark. Training-data privacy: memorisation and its scaling ("with: model size, sequence
repetition, prompt length. Approximately log-linear in each"), the poem-attack extraction result,
membership inference defined as "Given (x, y) and a model f, decide: was (x, y) in the training set?",
the shadow-model baseline, and the negative result "On modern LLMs, sentence-level MIA barely beats
chance" with the aggregation rule "The right unit of analysis is the corpus" ("Sentence ≈ chance;
collection ≫ chance"). Differentially private training with its utility cost ("At meaningful ε (say
ε ≤ 8), accuracy drops substantially") and composition ("Composes across steps via the moments
accountant"). Contextual privacy: Nissenbaum's contextual integrity, ConfAIde, and the finding that "The
'private thinker' assumption is wrong" because "Final answer respects the norm; CoT does not", with the
leakage gap measured between chain-of-thought and final answer and the warning that "Model still passes
standard safety and utility benchmarks … The failure is invisible to the evaluation stack." Model-side
privacy: extraction bounded by the API surface ("Extraction is bounded by what the API exposes, not what
the model contains"), visual attribute leakage ("A picture leaks a portfolio of attributes, not a single
bit"), and a model-stealing/fingerprinting procedure: "Deploy → register fingerprint → audit suspected
copies → confirm theft. One-time setup, repeated audit." Cost reporting is part of the protocol: query
counts and money ("$200 queries to gpt-3.5-turbo, extracted 10,000 unique training examples").

## 3. Exercise recovery, and why two of three are `NO`

The plan asks that exercise content be recovered rather than titled. Routes tried, in the order the plan
gives, per the audit that produced this record: the Kaggle notebook page (the viewer crashes and the
content RPC returns a reCAPTCHA challenge page), the Kaggle REST kernel endpoints (400/401 unauthenticated;
`download`/`raw`/`archive` 404), the raw HTML and three Wayback snapshots plus a CDX wildcard per author
(shell pages only, no cells), the course schedule's recap sessions (unlinked live sessions; the 2024/25
YouTube playlist holds twelve lecture videos and no exercise recap artifact exists for this edition), and
a GitHub search for the tutor's code (a hit only for Exercise 2).

What is therefore known and not known:

- **Exercise 1 (OOD)** — `NO`. Known: released at L2, due 20.11.2024, author Johannes, and the page
  metadata shows the notebook attaches an MNIST dataset. Nothing else about task, methods, baselines,
  metrics, ablations, questions or reporting is retrievable, so nothing is asserted.
- **Exercise 2 (XAI)** — `NO` for the notebook body, but the tutor's public scaffold
  (`aktsonthalia/tml2425_xai`, MIT, README empty) is `FULL` for the source files read. It ships a
  CUB-200-2011 dataset class, a `load_cub_test()` helper with a fixed manual seed and center crop, a
  `model_accuracy()` helper, an attribution-overlay viewer described as "attribution explanation
  overlayed to the image it's explaining", a deliberately dummy explanation — a "centered Gaussian
  heatmap" labelled "The dummy feature attribution explanation is a centered gaussian map" — and two
  configurable architectures (a MNIST-shaped LeNet with an ablatable `remove_layer`, and a hand-written
  ResNet-50 with optional pretrained weights). The dummy attribution is the one exercise-level fact with
  protocol content: the scaffold gives students a known-useless explanation to compare against. The
  instructions, required methods, metrics and questions remain unrecovered.
- **Exercise 3 (Uncertainty)** — `NO`. Known: released at L9, due 30.01.2025, author Lennart, page
  metadata lists an attached dataset named "miscellaneous". No scaffold found.

Consequence recorded up front: no candidate delta in this cycle may rest on the body of an exercise. The
2023/24 edition's Colab exercises and its linked Exercise-1 recap deck are a possible future route, but
that is book-era material and could not license a post-2023 delta anyway.

## 4. Version comparison

| Material family | 2023/24 (book era) | 2024/25 | 2026 |
|---|---|---|---|
| OOD generalisation, cues, domain generalisation | present | present | present (L2–L3) |
| Adversarial examples, FGSM/PGD, transfer, universal | present as "Adversarial attacks/defenses" | present | present, now inside a named "Privacy & Security" part with a formal threat model |
| LLM-specific attacks (suffix optimisation, jailbreak) | absent | **new** (L5) | present (L12), with indirect prompt injection as an environment attack |
| Explainability: definitions, feature attribution, training-data attribution | present | present | present (L5–L7), plus L4 modularity framing |
| Uncertainty: definitions, evaluation, epistemic/aleatoric, factorisation | present | present | present (L9–L10) plus **new** L11 "Uncertainty for Foundational Models" |
| Privacy and data protection as taught content | absent | absent | **new** (L13) |
| Model stealing, fingerprinting, watermark auditing | absent | absent | **new** (L13) |
| Project course with published rubric | absent (exam-based) | absent (exam-based; L12 mentions project topics) | **new**: proposal + final report/presentation, 5-point anchored rubric, peer evaluation |
| Example project topics naming detection-at-test-time tasks | absent | absent | **new** (five topics) |
| Exercise delivery vehicle | Colab + recap deck | Kaggle notebooks | not applicable (project replaces exercises) |
| Language-model use policy | present | present (four guidelines) | present, stricter penalties, plus "inability to explain your own work" as misconduct |

The 2024/25 edition is therefore a small delta on the book — one LLM-attack session and one new
explanation-definition framing — while 2026 is where the sizeable additions sit: a privacy/security
part, a foundational-model uncertainty session, and a project assessment layer with an explicit rubric.

## 5. Access limitations

- Kaggle notebook bodies for Exercises 0–3: blocked by bot protection at both the viewer and the API;
  Wayback holds shells only. Recorded as `NO`, not reconstructed.
- Sixteen of the twenty-two lecture decks were not opened: the eleven remaining 2024/25 decks and the six
  remaining 2026 decks are `PARTIAL` (title and link only). Anything they might contain is out of scope
  for this cycle and is not claimed.
- All videos (2024/25 YouTube, 2026 Drive) were not watched: `PARTIAL`.
- Text-export losses, deck-wide: drawn formulas and image-only slides are missing from the four 2026
  decks and TML2425-L5, and in two cases three citations are packed onto one tab-joined line so which
  paper backs which bullet is unreadable. Where this record quotes a formula-adjacent statement it says
  the formula itself was not seen.
- No Tübingen-side 2026 TML page was found; the STAI site lists `tml_spring_26` under KAIST AI only.
  Candidate hosts probed and the book site's sitemap returned nothing usable, so this is recorded as not
  found rather than as "the course moved".
- One cited arXiv identifier in TML26-L4 is forward-dated and unresolvable; treated as unread.
- A similarly named course from another institution with membership-inference and watermark-forgery
  leaderboard assignments surfaced during searching. Nothing connects it to this lineage; it is excluded
  and none of its content is used.
- AUARC, named as an evaluation metric in TML26-L11, is never defined in the deck text. It is therefore
  not usable as a metric in this repository without an external primary source.

## 6. Candidate deltas raised by this inventory

IDs are used by `delta_map.md` and `decision_log.md`. Listing a candidate here is not a recommendation;
each carries the source that raised it and nothing more.

| ID | Candidate | Raised by |
|---|---|---|
| CD-01 | Threat model as three declared components (goal, strategy space, knowledge ladder) plus a stated ε budget | TML26-L12 |
| CD-02 | LLM/generative-model attack evaluation: suffix optimisation on target NLL, transferability across models, universality across prompts | TML2425-L5, TML26-L12 |
| CD-03 | Indirect prompt injection as an environment-level attack, motivated by a production incident | TML26-L12 |
| CD-04 | Transfer must generalise across models rather than across data, with the shift named per model pair | TML26-L12 |
| CD-05 | Test-time detection of prompt sensitivity without ground truth | TML26-PROJECT topic 1, TML26-L11 |
| CD-06 | RAG parametric–contextual conflict detection and surfacing, evaluated as detector precision | TML26-PROJECT topic 2 |
| CD-07 | Agreement between mechanistic and training-data attribution families on the same failure cases | TML26-PROJECT topic 3 only — TML26-L4/L6/L7 were read for this and do not teach it |
| CD-08 | Empirical disentanglement check for epistemic/aleatoric estimators via cross-prediction rank correlation | TML26-L11 |
| CD-09 | Confidence and calibration degradation under shift and across turns, with method families split by access level and sampling cost | TML26-L11, TML26-PROJECT topic 4 |
| CD-10 | Training-data privacy evaluation: membership inference against a chance anchor, corpus-level unit of analysis, memorisation scaling | TML26-L13 |
| CD-11 | Contextual-norm compliance of intermediate reasoning, measured as a leak gap between chain-of-thought and final answer | TML26-L13 |
| CD-12 | Differentially private training reported as an ε-versus-utility curve with cross-step composition | TML26-L13 |
| CD-13 | Model extraction and fingerprint-audit procedure: deploy, register, audit, confirm | TML26-L13 |
| CD-14 | Reproduction as claim-boundary mapping: re-test on a different model or dataset and report where the result holds, weakens or breaks | TML26-PROJECT topic 5 |
| CD-15 | Rubric-level experimental-design expectations: appropriate baselines, error bars where applicable, limitation analysis, justified choices, interpretation beyond a single accuracy | TML26-RUBRIC |
| CD-16 | Explanation efficiency as an itemised resource cost (one-time versus per-case time, memory, storage, manpower) and end-to-end versus modular evaluation as rival regimes | TML2425-L5 |
| CD-17 | Test-time adaptation preconditions as information-rights requirements (a batch of test samples; single-sample entropy minimisation collapses to one-hot) | TML26-L4 |
| CD-18 | Underspecification re-expressed in three layers for language-mediated task specification, with modularity design axes | TML26-L4 |
| CD-19 | Multi-agent uncertainty propagation failure: an orchestrator that does not process valid per-agent uncertainty | TML26-L11 |
| CD-20 | Generated-work disclosure: name the models used and which text or code was generated; do not use a model as the primary verification source | TML2425-PAGE, TML26-PAGE |
| CD-21 | Exercise-level protocol content (task, baselines, metrics, required ablations, reporting) for OOD, XAI and uncertainty | TML2425-EX1/EX2/EX3 |

## 7. Gate U1 self-check

| Requirement | Result |
|---|---|
| Every Tier A item has an inventory row | **PASS** — all six Tier A families are represented, including the 2023/24 control and the project/rubric material. |
| Access status recorded per row | **PASS** — FULL / PARTIAL / NO per row, with the reason. |
| Enough extracted detail to support or reject a delta, or an explicit "insufficient evidence" | **PASS** — six decks and three pages carry field-level detail; CD-21 is recorded as insufficient evidence rather than reconstructed. |
| No content attributed to a source that was not read | **PASS** — the eleven unopened 2024/25 decks, eight unopened 2026 decks and all videos are credited with title and link only; export losses and one unresolvable citation are named in §5. |
| Post-2023 material kept distinct from the 2023 book | **PASS** — the two pages' own "updated yearly … won't cover new topics" wording is quoted, and the version table separates what is new in 2024/25 and 2026 from what the book-era edition already taught. |
