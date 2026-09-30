# Concept reconstruction — *Deep Learning* (Goodfellow, Bengio & Courville, 2016)

Single working record for the `Deep-Learning-2016` package. It answers four questions the plan asks
of this source: which reusable research **workflows** the book supports, which **evaluable
capabilities and failure modes** it supports, which major parts are **theory only** and therefore
correctly have no artifact, and where a **2016 implementation detail** is historical rather than a
current general rule.

Source identification, pagination convention and extraction method: [`SOURCE.md`](SOURCE.md).
Citations below use `§section` (stable across both editions) with a PDF page added where the claim
is load-bearing for an artifact.

## 1. Reconstruction principle

The package is reconstructed **by research function, not by chapter**. Chapter 11 (practical
methodology) is the spine: it names a design loop — set the metric, build an end-to-end baseline,
locate the bottleneck, then make incremental changes (§11, p. 436). The rest of the book supplies
the content that each step of that loop needs. Artifacts are therefore shaped like the questions a
researcher actually has to answer, and a single chapter is routinely split across several artifacts
while several chapters feed one artifact.

Mapping used throughout:

| Research function | Book material | Artifact |
| --- | --- | --- |
| Specify the task, the metric and the output distribution | §5.1, §6.2.1, §6.2.2, §5.10, §11.1, §11.6 | `SOP-DL-01`, `BC-DL-01` |
| Diagnose the fitting regime and move effective capacity | §5.2, §11.2, §11.3, §11.4.1 | `SOP-DL-02`, `BC-DL-02` |
| Select and justify a regularizer | §5.2.2, §7.1–7.5, §7.8–7.14 | `SOP-DL-03`, `BC-DL-03`, `BC-DL-04` |
| Diagnose optimization failure | §8.1–8.7, §10.11, §4.1–4.4 | `SOP-DL-04`, `BC-DL-05`, `BC-DL-06` |
| Run model selection and hyperparameter search | §5.3, §5.3.1, §11.4 | `SOP-DL-05`, `BC-DL-09` |
| Debug an experiment | §11.5, §4.1, §8.4 | `SOP-DL-06`, `BC-DL-07` |
| Choose and test an architectural inductive bias | §6.4.2, §9, §10 | `SOP-DL-07`, `BC-DL-08` |
| Decide what to share across tasks, domains and layers | §7.6, §7.7, §7.9, §14.1–14.9, §15 | `SOP-DL-08`, `BC-DL-10`, `BC-DL-12` |
| Compare generative models honestly | §17, §18, §19.4, §20.11, §20.14 | `SOP-DL-09`, `BC-DL-11` |

## 2. Reusable research workflows the book supports

Nine workflows survived the "is this genuinely reusable?" test. Each is a decision procedure with
stated inputs, a branch structure and a reporting obligation — not a summary of a method family.

| ID | Workflow question it answers | Licensing material |
| --- | --- | --- |
| `SOP-DL-01` | What exactly am I predicting, on what metric, with what output parameterization and cost? | §5.1.1 task taxonomy; §5.1.2/§11.1 metric choice, Bayes floor, asymmetric error costs, precision/recall/PR/F-score, coverage; §6.2.2.1–3 output units; §6.2.1.1 MLE→cost and the no-minimum hazard; §5.10 assembly recipe |
| `SOP-DL-02` | Am I underfitting or overfitting, and which capacity knob do I move? | §11.2 baseline recipe; §5.2 regime classification and Bayes error; §11.4.1 representational vs effective capacity and its three limits; Table 11.1 knob directions; §11.3 collect-more-data decision |
| `SOP-DL-03` | Given the regime, which regularization mechanism fits the failure and the data? | §5.2.2 definition; §7.1–7.3 penalties and constraints; §7.4 augmentation discipline; §7.5 noise robustness and label smoothing; §7.8 early stopping; §7.9–7.14 sharing, sparsity, bagging, dropout, adversarial training, tangent methods |
| `SOP-DL-04` | Training will not reach low error — which pathology is it, and what is the minimal repair? | §8.1 objective framing; §8.2 pathology taxonomy; §8.3 SGD/momentum/Nesterov; §8.4 initialization and the single-minibatch protocol; §8.5 adaptive methods; §8.6 second-order verdicts; §8.7 meta-strategies; §10.11 clipping; §4.1–4.4 numerical hygiene |
| `SOP-DL-05` | How do I choose hyperparameters and split data so the comparison is resolvable? | §5.3 validation sets; §5.3.1 cross-validation and benchmark staleness; §11.4.1 manual branches; §11.4.3 grid; §11.4.4 random search; §11.4.5 model-based search and its full-run defect |
| `SOP-DL-06` | Is this a real result or an implementation bug? | §11.5 in full (the two reasons debugging is hard, and the nine checks in the book's own order); §4.1 stable softmax/NLL forms; §8.4 gradient-magnitude expectations |
| `SOP-DL-07` | Which inductive bias does my data license, what does it buy, and how would I know it broke? | §6.4.2 depth vs width; §9.2 sparse interaction/parameter sharing/equivariance; §9.3 pooling; §9.4 infinite prior; §9.5 variants and padding; §9.9 cheap feature screening; §10.2–10.10 recurrence, unfolding, gating, encoder–decoder, bidirectionality; §10.6 recursion; §10.12 external memory |
| `SOP-DL-08` | Should I share parameters across tasks, domains, labeled/unlabeled data or layers? | §7.6/§15.3 semi-supervised; §7.7 multi-task; §15.2 transfer, domain adaptation, one-shot, zero-shot; §15.1 greedy pretraining and the book's own obsolescence verdict; §15.4 distributed representations; §15.6 prior list; §14 representation-quality criteria; §13.5 PCA control |
| `SOP-DL-09` | How do I compare two generative models without fooling myself? | §20.14 the four-way comparison problem; §18.7/§18.7.1/§18.7.2 partition-function estimation; §19.4.4 ELBO limitation; §17.3–17.5 MCMC trust conditions; §18.3–18.6 objective restrictions; §20.11 sampling from autoencoders |

Workflow order and dependencies are recorded in [`SOP/Deep-Learning-2016/README.md`](../../SOP/Deep-Learning-2016/README.md).
Two dependency rules the book itself forces: `SOP-DL-06` runs **before** any regime diagnosis when
the numbers are surprising (a mis-measured test error masquerades as overfitting, §11.5, p. 451),
and `SOP-DL-01` fixes the metric before `SOP-DL-05` chooses anything (the error metric guides all
subsequent work, §11.1, p. 437).

### 2.1 Procedures in the book that were deliberately **not** promoted to SOPs

These are procedures, but promoting them would produce chapter-shaped artifacts or would
operationalize a 2016 implementation choice as a current rule:

- **Greedy layer-wise unsupervised pretraining** (§15.1, Algorithm 15.1). A real procedure, but the
  book states it is no longer needed for most problems and survives only in the low-labeled-data
  regime (§15.1.1). Recorded as a **branch** inside `SOP-DL-08` with the book's own obsolescence
  verdict attached, not as a standalone SOP.
- **How to train an RBM / DBM / DBN** (§20.2.2, §20.3, §20.4.3–20.4.5). Model-family recipes tied to
  one 2016-era family. The reusable content is the *evaluation* discipline, which is `SOP-DL-09`;
  the positive/negative-phase mechanics stay in §4 below.
- **Vision preprocessing and dataset augmentation defaults** (§12.2.1, §12.2.2). The general
  augmentation discipline (only transformations the label is invariant to; keep a clean benchmark
  control) is already in `SOP-DL-03` via §7.4. The era-specific pixel statistics and contrast
  normalizations are historical, not a workflow.
- **Domain pipelines** (§12.3 speech recognition, §12.4 NLP incl. n-gram interpolation and
  high-dimensional output tricks, §12.5.1 recommendation systems). These are application surveys.
  The one transferable decision — whether to model the output sequence jointly or factorize it into
  independent per-position softmaxes — is folded into `SOP-DL-01` §7 from the street-view example
  (§11.6, p. 454).
- **Large-scale systems engineering** (§12.1.1–12.1.6: fast CPU, GPU, distributed training, model
  compression, dynamic structure, dedicated hardware). Real practice, but hardware-bound and the
  fastest-decaying material in the book.
- **Batch normalization** (§8.7.1). Kept as a repair inside `SOP-DL-04` §8.7 rather than its own
  SOP; the book presents it as a meta-strategy, and its own caveat (it can lower generalization
  error, in which case dropout may be dropped) is preserved there.

## 3. Evaluable capabilities and failure modes

Twelve benchmark checks (BCs). Each names a capability or failure mode the book asserts, a
comparison condition that would falsify or confirm it, and a metric that is a quantity the book
itself defines. No threshold is invented; where the book gives no number, the BC says so and the
comparison is run as an ordering rather than a pass/fail gate.

| ID | Capability / failure mode under test | Comparison condition | Licensing material |
| --- | --- | --- | --- |
| `BC-DL-01` | Choosing the output unit and the cost function jointly; saturating units under the wrong loss fail to learn | Same data, same capacity, vary (output unit × loss); compare gradient magnitude and convergence | §6.2.1.1, §6.2.2.2 p. 209, §6.2.2.3 p. 211 |
| `BC-DL-02` | Capacity and data-size reasoning: the U-curve, and the train-size vs generalization-error curve | Sweep capacity at fixed data; sweep data at fixed capacity; read regime off both curves | §5.2, §5.2.2, Fig. 5.3, Fig. 5.4, §11.3, §11.4.1 |
| `BC-DL-03` | Whether each regularizer acts by the mechanism claimed (L1 exact zeros, L2 scaling, early stopping ≈ L2, label smoothing, bagging, dropout weight scaling) | Mechanism-specific observables per regularizer at matched capacity | §7.1.1–7.1.2, §7.5.1, §7.8, §7.11, §7.12 |
| `BC-DL-04` | Adversarial examples arise from linear behaviour in high dimension, and adversarial training buys robustness | Sign-of-gradient perturbation at fixed ε; adversarially trained vs plain; measure accuracy drop and recovery | §7.13 |
| `BC-DL-05` | Optimization pathologies are **separable**: ill-conditioning, cliffs, saddles/plateaus, inexact gradients each leave a distinct trace | Same architecture under deliberately induced pathologies; classify from gradient/Hessian-conditioning traces and loss geometry | §8.2.1–8.2.7 |
| `BC-DL-06` | Long-range dependency: depth in time makes gradients vanish or explode, and gating/clipping changes that | Unfolded depth sweep; measure per-step gradient norm ratio; gated vs ungated vs clipped | §8.2.5 pp. 310–311, §10.7, §10.9–10.11 |
| `BC-DL-07` | Implementation health instruments detect injected bugs | Inject known bugs (bias update sign, wrong back-prop, mismatched preprocessing, saved-model reload) and confirm each instrument fires | §11.5 pp. 450–453 |
| `BC-DL-08` | Inductive-bias assumptions are testable: shuffling pixels, breaking translation structure, changing padding, removing recurrence | Data permutations that preserve label statistics but destroy the structure the bias assumes | §9.2–9.5, §9.9 p. 383, §10.2, §10.10 |
| `BC-DL-09` | Search efficiency and resolvability: random search beats grid at equal budget; validation noise can hide real differences | Matched trial budgets; repeat-with-different-seeds to test whether two configurations are separable | §11.4.3, §11.4.4, §5.3.1, §5.3.2 |
| `BC-DL-10` | Sharing gains are conditional on the labeled-data budget and on genuine task relatedness | Multi-task / semi-supervised / transfer sweeps against labeled-sample count, with unrelated-task control | §7.6, §7.7, §15.1.1, §15.2 |
| `BC-DL-11` | Generative-evaluation integrity: likelihood, sample quality and mode coverage can disagree, and estimators have known bias directions | Same model compared by estimate vs bound vs sample-based instruments; check whether a reward-hacking model wins | §20.14, §18.7.1, §18.7.2, §19.4.4, §17.3–17.5 |
| `BC-DL-12` | Representation quality: the criteria the book names, measured against a PCA control | Disentanglement / smoothness / sparsity / factorization observables per §14, with linear-baseline control | §14.1, §14.2, §14.5, §14.6, §14.7, §14.9, §13.5, §15.6 |

### 3.1 Evaluation candidates that were rejected

- **Architecture-family comparisons** (CNN vs RNN vs MLP vs autoencoder as such). The plan is
  explicit that an architecture name is not a benchmark. `BC-DL-08` tests the *assumption* the
  architecture encodes instead, which is a distinct evaluable claim.
- **Optimizer leaderboards** (Adam vs momentum SGD vs RMSProp). §8.5.4 states there is no consensus
  and that no single method dominates; a ranking would be an artifact of the chosen problem set, not
  a finding. The reusable claim is pathology separability, which is `BC-DL-05`.
- **Generative-model sample-quality scores.** Any metric the book does not name would be invented.
  `BC-DL-11` therefore evaluates the *evaluation instruments* the book does name (Z-ratio
  comparison, nearest-neighbour test, dropped-mode blindness, AIS bias direction, ELBO gap).
- **Depth-vs-width superiority.** §6.4.2 reports an observation (a network with 20M parameters can
  need 60M at fixed depth) under matched-parameter conditions specific to that experiment; it is
  recorded in `SOP-DL-07` as a design argument, and as a historical example, not as a standalone BC.

## 4. Theory-only material — no SOP or BC

These parts are load-bearing for *understanding* the artifacts above but yield no reusable procedure
and no evaluable claim of their own. They stay recorded here, per the plan.

**Mathematical and numerical toolkit (Ch. 2–4).** All of Ch. 2 (linear algebra, eigendecomposition,
SVD, pseudo-inverse, trace, determinant, the PCA worked example §2.12). Ch. 3 in full except the
function properties used by output units (§3.10 sigmoid/softplus identities) and §3.13 information
theory as the source of cross-entropy; §3.14 is a forward reference to Ch. 16. §4.3.1 Jacobian and
Hessian and the second-derivative test, and §4.4 constrained optimization and the KKT conditions —
used inside `SOP-DL-03` §7.2 and `SOP-DL-04` §8.2 but not operationalizable on their own. §4.5 the
linear least-squares worked example.

**Statistical foundations, derivation side (Ch. 5).** §5.1.4 the linear-regression example;
§5.2.1 the no-free-lunch theorem (its scope limits *are* used in `SOP-DL-02` §5, but the theorem
itself is not a procedure); §5.4.1–5.4.3 point estimation, bias, variance; §5.4.4 the bias–variance
decomposition of MSE; §5.4.5 consistency; §5.5.1 the conditional-log-likelihood ≡ MSE derivation;
§5.5.2 properties of MLE; §5.6 Bayesian statistics and §5.6.1 MAP; §5.7 the supervised-algorithm survey (incl. §5.7.2 SVM);
§5.8 the unsupervised-algorithm survey incl. §5.8.1 PCA and §5.8.2 k-means;
§5.9 SGD as an algorithm; §5.11.1 curse of dimensionality, §5.11.2 local constancy and smoothing
regularizers, §5.11.3 manifold learning and the manifold hypothesis — these motivate the tangent
methods and the representation criteria but are not themselves evaluable here.

**Network formalism (Ch. 6).** §6.1 the XOR example — a teaching device for why depth and
non-linearity matter. §6.4.1 universal approximation, the depth-separation results and the Barron
bounds: they license "capacity can be bought by depth or by width" in `SOP-DL-07` but give no
runnable test. §6.3 hidden-unit catalogue as such (the *choice* consequences are in `SOP-DL-01`
and `SOP-DL-04`; the taxonomy is reference material). §6.5 back-propagation and all of its
subsections §6.5.1–6.5.10 — computation graphs, chain rule, the full-connected MLP derivation,
symbol-to-symbol derivatives, generalized back-prop, complications, differentiation outside deep
learning, higher-order derivatives. This is the machinery that makes `SOP-DL-06` step 4 (comparing
back-prop against numerical derivatives) meaningful; the machinery itself has no SOP. §6.6
historical notes.

**Derivations behind methods that *are* operationalized (Ch. 7–8).** §7.2 the KKT/reprojection
derivation of penalties as constraints (the reprojection rule is used; the derivation is not).
§7.11 the normality assumption behind bagging and the exactness proof for the dropout-as-bagging
equivalence. §7.14 tangent distance, tangent propagation and the manifold tangent classifier as
mathematical constructions (their practical role is one line in `SOP-DL-03`). §8.2.8 the
theoretical limits of optimization — important for interpreting `BC-DL-05`, not testable by it.
§8.3.1–8.3.3 convergence-rate derivations and the dynamical-systems/physics analogy for momentum.
§8.6.1–8.6.3 the Newton, conjugate-gradient and BFGS derivations; only the verdicts (second-order
methods are rarely worth it in deep learning) enter `SOP-DL-04`.

**Sequence-model formalism (Ch. 10).** §10.1 unrolling computation graphs and §10.2 the RNN
gradient derivation; §10.2.1 teacher forcing; §10.2.2 the recursive gradient equation; §10.2.3
RNNs as directed graphical models and the conditional-independence bookkeeping; §10.2.4
context-based sequence modelling; §10.8 echo state networks and the echo state property. The
*decisions* (which recurrent block to deepen, whether to gate, whether to go bidirectional,
whether to add external memory) are in `SOP-DL-07`; the derivations are not.

**Linear factor models (Ch. 13)** as a family: §13.1 probabilistic PCA and factor analysis,
§13.2 ICA, §13.3 slow feature analysis, §13.4 sparse coding. Only §13.5 (PCA as the linear
manifold-projection control) is used, inside `BC-DL-12` as the linear baseline.

**Autoencoder mathematics (Ch. 14).** §14.3 representational capacity, layer size and depth for
autoencoders; §14.4 stochastic encoders and decoders; §14.5 the denoising autoencoder derivation
incl. §14.5.1 score estimation; §14.6 the manifold-learning view; §14.8 predicted sparse
decomposition. The *criteria* for representation quality (§14.1, §14.2, §14.7, §14.9) are
operationalized in `SOP-DL-08` and `BC-DL-12`; the derivations are not.

**Representation-learning theory (Ch. 15).** §15.3 the causal/semi-supervised argument in its
formal form (the practical licensing rule is in `SOP-DL-08`); §15.4 distributed representations
and the geometry of the exponential-gain argument; §15.5 exponential gains from depth as a
complexity-theoretic statement.

**Graphical-model formalism (Ch. 16) in its entirety.** §16.1 why unstructured modelling is hard;
§16.2 graph notation, directed and undirected models, partition functions, energy-based models,
separation and d-separation, moralization, factor graphs; §16.3 sampling from graphical models;
§16.4 advantages of structured modelling; §16.5 learning dependencies; §16.6 inference and
approximate inference; §16.7 deep-learning approaches and §16.7.1 the RBM instance. This chapter
is notation and factorization theory. It is what makes the partition-function problem in `SOP-DL-09`
intelligible; nothing in it is a workflow or an evaluation.

**Monte Carlo machinery (Ch. 17).** §17.1 why sampling is needed and the Monte Carlo foundations;
§17.2 importance sampling and its degeneracy analysis; §17.3 MCMC; §17.4 Gibbs sampling; §17.5 the
mixing-between-modes problem, §17.5.1 tempering and §17.5.2 the depth-helps-mixing argument. The
*trust conditions* (burn-in, thinning, ~100 chains, mixing being unknowable in practice, the
fresh-chain rule for persistent chains) are in `SOP-DL-09`; the Perron–Frobenius / ergodicity
material behind them is not.

**Parameter estimation for undirected models (Ch. 18).** §18.1 the log-likelihood gradient and the
positive/negative phase; §18.2 stochastic maximum likelihood and contrastive divergence; §18.7
partition-function estimation and its proof structure. The *estimator-selection rules* (IS
degeneracy, AIS and its stated mode-dropping bias direction, bridge sampling) enter `SOP-DL-09`;
the derivations do not.

**Approximate inference (Ch. 19).** §19.1 inference as optimization; §19.2 EM; §19.3 MAP inference
and sparse coding; §19.4.1 discrete latent variables; §19.4.2 the calculus of variations; §19.4.3
continuous latent variables and the ELBO derivation; §19.5 learned approximate inference,
§19.5.1 the wake-sleep algorithm, §19.5.2 other forms. Only §19.4.4 (learning and inference
interacting, and the resulting limitation of comparing models by ELBO) is operationalized, in
`SOP-DL-09` and `BC-DL-11`.

**Boltzmann-machine and generative-family catalogue (Ch. 20).** §20.1–20.8 the BM, RBM, DBN, DBM
(incl. mean-field inference and uniform-field inference), real-valued and convolutional BMs, BMs
for structured/sequence output, and other BMs; §20.9 back-propagation through stochastic
operations; §20.10 the directed generative network catalogue (sigmoid belief networks,
differentiable generator networks, VAE, GAN, generative moment matching networks, convolutional
generative networks, and the autoregressive family MADE/RNN-NADE/NADE); §20.12 generative
stochastic networks; §20.13 other generative schemes; §20.15 conclusions. Only §20.11 (sampling
from autoencoders, incl. clamping/conditioning and the annealing/backtracking training procedure)
and §20.14 (evaluating generative models) are operationalized.

**Applications survey (Ch. 12)** as described in §2.1 above: §12.1.1–12.1.6, §12.2.1–12.2.2,
§12.3, §12.4.1–12.4.6, §12.5.1–12.5.2.

**Front matter and Ch. 1** (introduction, history, the "who is this book for" framing): context
only. The 中文版推荐语 and 译者序 are paratext of this edition and are not citable as claims of the
work — see `SOURCE.md`.

## 5. Historical boundary register

The book is a 2016 source. Everything below was **recorded as historical** in the artifacts rather
than written as a current default. Each entry names where it appears so the boundary is checkable.

### 5.1 Era defaults presented as recommendations

- **The §11.2 baseline recipe** — ReLU/Leaky ReLU/PReLU/maxout units, momentum SGD with decay or
  Adam, early stopping, dropout, mild regularization unless the training set exceeds tens of
  millions of samples, and "use batch normalization as soon as optimization seems problematic."
  Recorded in `SOP-DL-02` §3.1 and `SOP-DL-04` §8.7 with the book's own caveat quoted: deep
  learning progresses quickly and better defaults were likely to appear soon after publication.
- **Greedy layer-wise unsupervised pretraining** (§15.1, Algorithm 15.1) as the standard way to
  initialize deep nets. The book already declares it largely obsolete outside low-data regimes;
  `SOP-DL-08` §15.1 carries that verdict forward rather than recommending the procedure.
- **Weight initialization rules of thumb** (§8.4): initialize with roughly unit variance then scale
  by 1/√fan-in, with the Glorot-style variant; the single-minibatch activation/gradient diagnostic
  is preserved as a *method* because it is era-independent, while the specific target values are
  flagged as 2016 conventions.
- **Dropout rates** (§7.12): ~0.8 retention at the input, ~0.5 at hidden layers, and the
  test-time weight-scaling rule. Kept in `SOP-DL-03` and `BC-DL-03` as the book's stated defaults,
  not as universal constants.
- **Bagging ensemble size / sampling fraction** (§7.11): the ~2/3-of-training-examples behaviour.
  Historical, cited as the source of the claim.
- **§12.1 systems practice**: fast CPU/GPU implementations, large-scale distributed training, model
  compression, dynamic structure, dedicated hardware. Not operationalized at all; recorded as the
  fastest-decaying part of the book.
- **§12.4 NLP stack**: n-gram language models and their interpolation with neural models (§12.4.4),
  the high-dimensional-output problem and its 2016 solutions (§12.4.3), neural machine translation
  as of §12.4.5, and §12.4.6's own "historical outlook." Surveyed at section level only.
- **§10.12 external memory** as an emerging mechanism; **§10.8 echo state networks**;
  **§10.9 leaky units and multi-timescale strategies** — recorded in `SOP-DL-07` as options the book
  considered, with no claim that they are current practice.
- **§18.7.1 annealed importance sampling** as the reference partition-function estimator, and
  **§18.7.2 bridge sampling** — used in `SOP-DL-09` as the book's instruments, with AIS's stated
  bias direction preserved.

### 5.2 Numeric constants and observations that are era-specific

The 20M→60M parameter observation attached to the depth/width trade-off (§6.4.2, Fig. 6.7); the
labeled-data budget landmarks used to branch the sharing decision (~5000 labels per class for
CIFAR-10 and MNIST in the §15.1.1 discussion); the street-view coverage/precision targets of 95%
coverage at 98% human-level precision (§11.1, §11.6); the ~1% parameter-update-to-parameter
magnitude rule attributed to Bottou (§11.5, p. 453); the complex-step differentiation ε = 10⁻¹⁵⁰
(§11.5, p. 453). All are recorded with attribution. Only the Bottou ratio rule and the complex-step
ε are presented as usable today, and in both cases the artifact says why (they are numerical
properties, not benchmark results).

### 5.3 Named tooling, verdicts and benchmarks

- **No-consensus verdicts preserved as verdicts, not as findings**: §8.5.4 (no optimizer dominates),
  §8.6 (second-order methods rarely pay off), §11.4.5 (Bayesian hyperparameter optimization "not
  yet mature or reliable", sometimes expert-like, sometimes catastrophic).
- **Benchmark staleness** (§5.3.2) and the era benchmark set (MNIST, CIFAR-10, SVHN, ImageNet, and
  the street-view house-number task). BCs that use these say so and treat them as *carriers* of a
  comparison condition, not as current leaderboards.
- **Software/hardware framework references** in Ch. 8 and Ch. 12 are cited only where a claim depends
  on them.

### 5.4 What was deliberately not imported

Nothing post-2016 was added anywhere in this package: no Transformer or attention mechanisms, no
AdamW or modern optimizer defaults, no learning-rate warmup/cosine schedules, no batch-size–LR
scaling rules, no scaling laws, no FID / Inception Score / perplexity-as-standard, no modern
leaderboards, no diffusion models, no large-pretrained-model or foundation-model transfer, no
current best practices for mixed precision or distributed training. Where a 2016 statement is now
known to be incomplete, the artifact marks it **historical** and stops there rather than updating
the source. A future source-update cycle may add later material; this cycle may not.

**Terminology boundary.** This local copy is Simplified Chinese only, so no verbatim English
quotations are possible and translated terminology is used throughout. One drift is worth flagging
because it affects citation reading: the book's own footnote (Ch. 11 front matter, p. 436) advises
against abbreviating 递归神经网络 (recursive neural network) as "RNN", to keep it distinct from
循环神经网络 (recurrent neural network). `SOP-DL-07` keeps that distinction and says which of the
two a claim is about.

## 6. Traceability caveats

- **Display equations are images, not text.** In this e-copy the numbered display equations are
  raster images embedded in the page, so text extraction returns surrounding prose with the formula
  missing. Verified by per-page image counts (e.g. PDF p. 275 → 7 images, p. 276 → 13, p. 442 → 0).
  Documented in `SOURCE.md`. Consequently, claims that in the print edition rest on a displayed
  equation are cited here at the **prose** level, and `SOP-DL-03`, `SOP-DL-04`, `BC-DL-03` and
  `BC-DL-12` each carry an explicit "Formula caveat" block saying which statement is prose-supported
  only. Nothing in this package asserts a formula that could not be read from the local file.
- **Pagination.** PDF page numbers are 1-based positions in the local file, not printed folios; the
  structural map in `SOURCE.md` gives the chapter↔page spans so any citation can be re-located.
- **No invented thresholds.** Every metric in every BC is a quantity the book names, or an ordering
  comparison where the book gives no number. Every SOP step points at a section. This was checked
  once, in the finishing pass, and is not re-litigated per artifact.
