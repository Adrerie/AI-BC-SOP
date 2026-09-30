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
| Select and justify a regularizer | §5.2.2, §7.1–7.5, §7.8–7.14 | `SOP-DL-03`, `BC-DL-03` |
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
| `SOP-DL-04` | Training will not reach low error — verify objective → inspect symptom → probe → minimal repair → rerun → report | §8.1 objective framing; §8.2 pathology taxonomy; §8.3 SGD/momentum/Nesterov; §8.4 initialization and the single-minibatch protocol; §8.5 adaptive methods; §8.6 second-order verdicts; §8.7 meta-strategies; §10.11 clipping; §4.1–4.4 numerical hygiene |
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
- **Batch normalization** (§8.7.1). Kept as repair 5 and a menu row inside `SOP-DL-04` §3.4 rather than
  its own SOP; the book presents it as a meta-strategy, and its own caveat (it can lower generalization
  error, in which case dropout may be dropped) is preserved there.

## 3. Evaluable capabilities and failure modes

Eleven benchmark checks (BCs). Each names a capability or failure mode the book asserts, a
comparison condition that would falsify or confirm it, and a metric that is a quantity the book
itself defines. No threshold is invented; where the book gives no number, the BC says so and the
comparison is run as an ordering rather than a pass/fail gate.

BC identifiers are stable, not a sequence: `BC-DL-04` was withdrawn (see §3.1) and its number is
not reused.

| ID | Capability / failure mode under test | Comparison condition | Licensing material |
| --- | --- | --- | --- |
| `BC-DL-01` | Choosing the output unit and the cost function jointly; saturating units under the wrong loss fail to learn | Same data, same capacity, vary (output unit × loss); compare gradient magnitude and convergence | §6.2.1.1, §6.2.2.2 p. 209, §6.2.2.3 p. 211 |
| `BC-DL-02` | Capacity and data-size reasoning: the U-curve, and the train-size vs generalization-error curve | Sweep capacity at fixed data; sweep data at fixed capacity; read regime off both curves | §5.2, §5.2.2, Fig. 5.3, Fig. 5.4, §11.3, §11.4.1 |
| `BC-DL-03` | Whether each regularizer produces the mechanism-specific effect claimed (L1 exact zeros, L2 scaling, early stopping ≈ L2, bagging ν/k, dropout weight scaling); the two errors are reported separately and neither decides the arm | Mechanism-specific observables per regularizer at matched capacity | §7.1.1–7.1.2, §7.5.1, §7.8, §7.11, §7.12 |
| `BC-DL-05` | Whether the book's optimization **probes** are informative: each probe can support or rule out a diagnosis, and the remedies move the quantity the diagnosis names | Same architecture under deliberately induced pathologies; run the probe suite and check which diagnoses survive | §8.2.1–8.2.7 |
| `BC-DL-06` | Long-range dependency: depth in time makes gradients vanish or explode, and gating/clipping changes that | Unfolded depth sweep; measure per-step gradient norm ratio; gated vs ungated vs clipped | §8.2.5 pp. 310–311, §10.7, §10.9–10.11 |
| `BC-DL-07` | Implementation health instruments detect injected bugs | Inject known bugs (bias update sign, wrong back-prop, mismatched preprocessing, saved-model reload) and confirm each instrument fires | §11.5 pp. 450–453 |
| `BC-DL-08` | Inductive-bias assumptions are testable: shuffling pixels, breaking translation structure, changing padding, removing recurrence | Data permutations that preserve label statistics but destroy the structure the bias assumes | §9.2–9.5, §9.9 p. 383, §10.2, §10.10 |
| `BC-DL-09` | Search efficiency and resolvability: random search beats grid at equal budget; validation noise can hide real differences | Matched trial budgets; repeat-with-different-seeds to test whether two configurations are separable | §11.4.3, §11.4.4, §5.3.1, §5.3.2 |
| `BC-DL-10` | Sharing gains are conditional on the labeled-data budget and on genuine task relatedness | Multi-task / semi-supervised / transfer sweeps against labeled-sample count, with unrelated-task control | §7.6, §7.7, §15.1.1, §15.2 |
| `BC-DL-11` | Generative-evaluation integrity: likelihood, sample quality and mode coverage can disagree, and estimators have known bias directions | Same model compared by estimate vs bound vs sample-based instruments; check whether a reward-hacking model wins | §20.14, §18.7.1, §18.7.2, §19.4.4, §17.3–17.5 |
| `BC-DL-12` | Representation quality: the criteria the book names, each against a control appropriate to that criterion — PCA only for the linear / undercomplete-autoencoder comparisons | Per-criterion observables for §14, with the linear control restricted to where it is the right comparator | §14.1, §14.2, §14.5, §14.6, §14.7, §14.9, §13.5, §15.6 |

### 3.1 Evaluation candidates that were rejected or withdrawn

- **Architecture-family comparisons** (CNN vs RNN vs MLP vs autoencoder as such). The plan is
  explicit that an architecture name is not a benchmark. `BC-DL-08` tests the *assumption* the
  architecture encodes instead, which is a distinct evaluable claim.
- **Optimizer leaderboards** (Adam vs momentum SGD vs RMSProp). §8.5.4 states there is no consensus
  and that no single method dominates; a ranking would be an artifact of the chosen problem set, not
  a finding. What survives is the probe suite in `BC-DL-05`.
- **Adversarial linearity / the sign-of-gradient (FGSM-style) construction** — *withdrawn* as
  `BC-DL-04`. The book's demonstration is a single 2016-era figure (GoogLeNet on ImageNet,
  §7.13, pp. 292–293, Fig. 7.8) with no perturbation budget, no norm convention and no effect size
  for the claim that adversarial training helps the original i.i.d. test set. Turning it into a BC
  would have required inventing exactly those numbers. It is retained as a **2016 historical
  observation** in §5.1 and as brief context in `SOP-DL-03`; no current robustness metric is added
  and no later attack family is introduced.
- **Unique classification of an optimization pathology from its trace** — *reframed*, not dropped.
  Probes support or rule out diagnoses; they do not identify one pathology uniquely, because
  ill-conditioning, cliffs and flat regions co-occur and the same trace can admit several. `BC-DL-05`
  was rewritten accordingly as a diagnostic probe suite.
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
used inside `SOP-DL-03` §3.3 and `SOP-DL-04` §3.2–§3.4 but not operationalizable on their own. §4.5 the
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
learning, higher-order derivatives. This is the machinery that makes `SOP-DL-06` step 5 (comparing
back-prop against numerical derivatives) meaningful; the machinery itself has no SOP. §6.6
historical notes.

**Derivations behind methods that *are* operationalized (Ch. 7–8).** §7.2 the KKT/reprojection
derivation of penalties as constraints (the reprojection rule is used; the derivation is not).
§7.11 the normality assumption behind bagging and the exactness proof for the dropout-as-bagging
equivalence. §7.13 adversarial examples and the sign-of-gradient construction — retained only as a 2016
historical observation (§5.1) and as brief context in `SOP-DL-03` §3.3, since `BC-DL-04` was withdrawn
(§3.1). §7.14 tangent distance, tangent propagation and the manifold tangent classifier as
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

### 4.1 Method inventories moved out of the SOPs

The plan requires the SOPs to keep the executable decision path and to compress catalog-style method
inventories, historical menus, long derivations and era-specific recipes. This subsection holds the
inventories that were moved out, so that the decision path stays short without the source content being
lost. Everything here is **book-derived**, cited, and none of it is a current recommendation — see §5.

**(a) Optimization inventory — moved out of `SOP-DL-04`.**

*First-order schedules.* SGD's rate must decay because minibatch sampling noise does not vanish at the
minimum, whereas batch gradient descent can use a fixed rate; sufficient convergence conditions are
Σ εₖ = ∞ and Σ εₖ² < ∞ (§8.3.1, pp. 314–317). The practical schedule is a linear decay of εₖ to ε_τ over
τ iterations, constant afterwards. Tuning is described as more art than science: monitor the
objective-versus-time curve; take τ as roughly the iterations needed for a few hundred passes through the
training set; take ε_τ as about 1% of ε₀; choose ε₀ by inspecting the earliest iterations — pick a rate
*higher* than the one that looks best after about 100 iterations, but not so high that it causes severe
oscillation. Violent oscillation or a rising cost means too high; too low means slow training or a permanent
stall at high cost; mild oscillation is acceptable, especially with dropout. Per-step time is independent of
dataset size, and on very large datasets SGD may converge within tolerance before completing one pass.
Growing the minibatch during training trades the batch and stochastic advantages.

*Momentum.* The velocity is an exponentially decaying average of past gradients; momentum targets
ill-conditioning and gradient variance. α is read through 1/(1 − α), the effective maximum step multiple over
plain gradient descent, so α = 0.9 gives a terminal speed ten times plain GD; common values are 0.5, 0.9 and
0.99. α may be ramped up over time, but tuning α over time matters less than shrinking 1/(1 − α) (§8.3.2,
pp. 317–321, Fig. 8.5).

*Adaptive rates.* Motivation: the learning rate is among the hardest hyperparameters, the loss is highly
sensitive in some parameter directions and not others, and per-parameter adaptation makes sense if that
sensitivity is roughly axis-aligned. AdaGrad scales each parameter's rate inversely to the square root of the
*cumulative* sum of squared gradients — good convex theory, but on deep networks the accumulation causes
premature or excessive decay of the effective rate, and it works on some deep models and not others. RMSProp
replaces the accumulation with an exponentially weighted moving average, discarding distant history, which
behaves like AdaGrad re-initialized inside the local convex bowl; the book calls it effective and practical
and one of the methods practitioners commonly use. Adam adds momentum applied to the exponentially weighted
first-moment estimate of the raw gradient, plus bias correction of both moments — RMSProp lacks the
correction, so its second-moment estimate is heavily biased early — and is considered robust to
hyperparameter choice, though the learning rate sometimes needs changing from the recommended default of
0.001 (§8.5.1–§8.5.3, pp. 327–332). A broad comparison (Schaul et al., 2014, as cited) found the
adaptive-rate family quite robust but produced no standout winner; the popular set is SGD, SGD with momentum,
RMSProp, RMSProp with momentum, AdaDelta and Adam (§8.5.4, p. 332).

*Second-order methods.* Newton is valid only where the Hessian is positive definite; near a saddle it moves in
the wrong direction; it can be patched by adding α to the Hessian diagonal, but if α must be large enough to
offset negative curvature the method degenerates into gradient/α with steps smaller than well-tuned gradient
descent. Its fatal cost is a k × k inverse per iteration, O(k³) with k possibly in the millions, so only tiny
networks are feasible. Conjugate gradient avoids the inverse using conjugate directions, needs at most k line
searches in k dimensions for quadratics, and nonlinear CG needs occasional restarts; practitioners report it
reasonable for training networks and *better if preceded by a few SGD steps*, and minibatch versions have
succeeded. BFGS keeps a low-rank approximation of H⁻¹ and depends less on a precise line search, but costs
O(n²) memory and is unsuitable for million-parameter models; L-BFGS reduces storage to O(n) per step (§8.6,
pp. 332–339).

*Initialization schemes.* **Normalized initialization** (Glorot and Bengio, 2010, as cited) samples from a
range compromising between equal activation variance and equal gradient variance per layer, derived under an
assumption of a chain of linear matrix multiplications — real networks violate the assumption, but strategies
derived for linear models often still work. **Orthogonal initialization with a per-nonlinearity gain g** (Saxe
et al., 2013, as cited) makes iterations-to-convergence independent of depth *under the linear-chain model*;
increasing g pushes the network into the regime where forward activation norms and backward gradient norms
grow. Setting the gain correctly alone has been reported to suffice for training 1000-layer networks without
orthogonal initialization (Sussillo, 2014, as cited), because activations and gradients then follow a
norm-preserving random walk across layers, avoiding the shared-matrix vanishing and explosion of §8.2.5.
**Sparse initialization** (Martens, 2010, as cited) gives each unit exactly k nonzero weights, keeping total
input magnitude independent of m; its drawbacks are a strong prior on the large weights it keeps, slowness to
shrink the wrong ones, and problems with maxout filters. **Symmetry breaking** is the one firm requirement:
identical units receiving identical inputs would update identically; random initialization from a
high-entropy distribution is the cheap way, Gram–Schmidt orthogonalization the expensive deterministic
alternative. Gaussian versus uniform "does not seem to make much difference" and has not been exhaustively
studied. The scale trade-off: large weights break symmetry better and prevent signal loss in forward and
backward linear propagation; too large causes exploding values, chaos in recurrent networks (mitigable by
gradient clipping) and saturating activations with zero gradients. Optimization wants weights large enough to
propagate signal while regularization wants them small. Initializing at θ₀ acts like a Gaussian prior centered
at θ₀, so early-stopped gradient descent is approximately weight decay toward the initialization (cf. §7.8).
**Bias exceptions** to the usual zero: output-unit biases set to match output marginal statistics (solve
softmax(b) = c for class marginals; likewise autoencoders and Boltzmann machines reproducing input
marginals); avoiding initial saturation (a ReLU hidden bias of 0.1 instead of 0, which conflicts with
walk-initialization schemes); and gating units, where the bias is set so the gate opens at initialization —
the cited example is an LSTM forget-gate bias of 1. Variance or precision parameters can safely be
initialized to 1, or set to the marginal variance of the training outputs. Learned initialization,
unsupervised or cross-task supervised, can beat random initialization in convergence speed and sometimes in
generalization (§8.4, pp. 322–327).

*Batch normalization, full mechanism.* The diagnosis it addresses: in a deep composition each layer's
gradient assumes the other layers are fixed while all layers update simultaneously, and higher-order
cross-layer interactions can be exponentially large, which makes any single learning rate wrong and n-th-order
methods hopeless. Replace a layer's minibatch activation matrix H by H′ = (H − µ)/σ computed per unit over the
minibatch, and — the key innovation — **backpropagate through the normalization**, so gradient components that
would merely shift a unit's mean or standard deviation are cancelled. Prior approaches either penalized the
deviation or re-normalized after each step, and either under-normalize or waste time fighting the learner. For
inference, replace µ and σ with running averages collected during training, which enables single-sample
evaluation. Normalization alone reduces representational power, so use γH′ + β — the same function family with
better learning dynamics, and β directly controls the mean. Placement: normalize XW after the linear
transform, dropping the bias as redundant with β; for convolutional networks, normalize each feature map
across spatial positions jointly. Full decorrelation of units would be better but is too expensive, so BN
remains the most practical option so far (§8.7.1, pp. 339–343).

*Supervised pretraining variants.* Greedy supervised pretraining trains layer subsets stage-wise, each new
hidden layer as a shallow MLP on the previous layer's output, optionally followed by joint fine-tuning.
Variants the book names: growing an 11-layer network to 19 layers with random middle layers then training
jointly; using previous outputs together with the original inputs; transferring the first k layers from a
network pretrained on other subsets; and hint-based training, where a wide-shallow teacher trains a
narrow-deep student that must also regress the teacher's intermediate layers — without those hints the student
performs badly on both training and test data. It helps by guiding intermediate-layer learning, benefiting
optimization and generalization alike (§8.7.4, pp. 344–347).

**(b) Regularization inventory — moved out of `SOP-DL-03`.**

*Sparse-representation alternatives to activation L1* (§7.10, pp. 278–280): penalties derived from the
Student-t distribution; KL-divergence penalties for constraining elements to the unit interval; matching the
mean activation to a target vector (an all-0.01 target is the cited example); and a hard constraint on the
number of non-zeros solved by orthogonal matching pursuit (OMP-k), which is efficient when W is orthogonal.

*Dropout mechanism generalizations* (§7.12, pp. 290–292): any μ-parameterized random modification works, not
just include/exclude. Gaussian multiplicative noise with E[μ²] = 1 was reported to outperform binary masks;
DropConnect and stochastic pooling are named variants. Choose modifications the network can learn to defend
against, and prefer families that permit fast approximate inference. Multiplicative hidden-unit noise beats
additive fixed-scale noise on rectified networks, because additive noise can be defeated simply by scaling
activations up. For linear regression, dropout is equivalent to L2 with per-feature coefficients set by
feature variance (Wager et al., 2013, as cited); the equivalence breaks for deep models (§7.12, p. 290).
Inference detail: the exact object is a renormalized geometric mean over exponentially many subnetworks; the
weight-scaling rule for inclusion probability 0.5 reduces to halving weights after training, or doubling unit
states during training, so that a unit's expected total input matches training time; up to 1000 Monte Carlo
samples were compared, with weight scaling winning overall but 20-sample MC winning for some models
(§7.12, pp. 286–289).

*Bagging derivation assumption* (§7.11, pp. 280–282): the ν → ν/k error decomposition assumes multivariate
normal member errors with common variance and covariance; the ν/k endpoint requires zero covariance, which is
an idealization.

*Early-stopping costs and era hardware habits* (§7.8, p. 271): the two costs are periodic validation
evaluation — parallelizable on a separate machine, CPU or GPU, or reducible with a smaller validation set or
less frequent evaluation — and keeping a copy of the best parameters, which is negligible because it can live
in slower, larger storage (train in GPU memory, store the best parameters in main memory or on disk), since
writes are rare and never read during training.

**(c) Sharing and representation inventory — moved out of `SOP-DL-08`.**

*The non-distributed contrast class* (§15.4, pp. 549–554): representations and methods that are **not**
distributed — one-hot and other symbolic encodings, k-means, k-nearest-neighbours, decision trees, Gaussian
and mixture-of-experts models, kernel machines with local kernels, and n-gram models. A nearest-neighbour
scheme with n samples distinguishes only n regions, against O(n^d) for n linear-threshold features with O(nd)
parameters.

*The book's list of general priors for discovering latent causes* (§15.6, pp. 556–558): smoothing (local
constancy); linearity; multiple explanatory factors; causal factors; depth, i.e. hierarchical organization of
factors; **factors shared across tasks**, where each output is tied to a subset of a common factor pool and
sharing p(h|x) shares statistical strength; manifold; natural clustering, with each connected manifold
receiving one class — which motivates tangent propagation, double backpropagation, the manifold-tangent
classifier and adversarial training; temporal and spatial coherence (slow feature analysis); sparsity; and
simplified factor dependencies (marginal independence, or linear/shallow-autoencoder dependencies).

*Regularized-autoencoder variants* (§14.2, pp. 512–516): **sparse** (reconstruction plus a sparsity penalty; a
Laplace prior corresponds to an L1 penalty; ReLU codes give true zeros), **denoising**, and
**derivative-penalty / contractive**. The denoising training procedure (§14.5, p. 518): sample x; sample a
corrupted x̃ from the corruption distribution; train to reconstruct x from x̃ by minimizing the decoder's
negative log-likelihood with h = f(x̃). Depth for a contractive autoencoder is obtained by stacking
single-layer contractive autoencoders, each trained to reconstruct the previous code (§14.7, pp. 527–530).

*The linear factor model baseline family* (§13, pp. 497–509), to be kept in view whenever a representation is
claimed to be richer than a linear factor model: factor analysis (Gaussian prior, conditionally independent
inputs, diagonal noise); probabilistic PCA (isotropic variance, reducing to PCA as the noise goes to zero);
ICA (separates *independent*, not merely uncorrelated, signals, and requires a non-Gaussian prior for
identifiability — with a Gaussian prior the mixing matrix is not identifiable); slow feature analysis (a
slowness penalty between consecutive time steps, closed-form, under zero-mean, unit-variance and decorrelation
constraints); and sparse coding (a non-parametric encoder obtained by optimization, alternating between the
code and the dictionary; it has no encoder generalization error, and was reported to generalize better than a
linear-sigmoid autoencoder, and better still with very few labels per class, §13.4, p. 507).

**(d) Generative-evaluation inventory — moved out of `SOP-DL-09`.**

*Partition-function estimators, mechanics* (§18.7, pp. 624–632). **Simple importance sampling** from a
tractable proposal p₀ with known Z₀: the expectation is independent of the proposal q but the variance is not,
the optimal q* ∝ p|f| is infeasible, and the estimator degrades as D_KL(p₀ ‖ p₁) grows because few samples
carry significant weight — quantified by the variance of the importance weights, maximal when the weights are
highly dispersed. Where an unbiased estimator is not required, biased importance sampling needs no normalized
p or q and is biased but asymptotically unbiased; when q is small where p·f is large the variance explodes,
such samples are rarely drawn, so the estimate typically **underestimates** the target rather than being
offset by overestimates — the book calls this endemic in high dimensions (§17.2, pp. 593–596). The Monte Carlo
confidence interval is built as: empirical mean and variance of f(x⁽ⁱ⁾), variance divided by n, approximately
normal by the central limit theorem (§17.1.2, p. 593). **Annealed importance sampling (AIS)**, popularized for
RBMs and DBNs by Salakhutdinov and Murray (2008, as cited): a chain of geometric-mean intermediate
distributions between p₀ and p₁, MCMC transitions (Metropolis–Hastings or Gibbs) preserving each, per-sample
weights accumulated in log space, and the ratio estimated as the mean of the weights; its validity is argued
by recasting AIS as simple importance sampling on an extended state space. **Bridge sampling** uses a single
bridge distribution p*; the optimal bridge is the harmonic mixture of p₀ and p₁ weighted by r = Z₁/Z₀, found
by iterating from a rough r; more efficient than AIS when D_KL(p₀ ‖ p₁) is moderate. **Chained importance
sampling** (Neal, 2005, as cited) bridges AIS's intermediate distributions to improve the estimate. AIS is too
expensive for tracking Z *during* training; the book cites Desjardins et al. (2011) combining bridge sampling,
short-run AIS and parallel tempering to track an RBM's Z during training with lower variance (§18.7.2,
pp. 631–632).

*MCMC non-mixing: remedies and symptoms* (§§17.4–17.5.2, pp. 601–605). Options: Gibbs or block Gibbs
(Metropolis–Hastings is rarely used for undirected models in deep learning); grouping highly dependent
variables and updating blocks jointly, which is often intractable; and tempering — sampling at inverse
temperature β < 1, tempered transitions (Neal, 1994) and parallel tempering (Iba, 2001) — with the verdict
that tempering is limited because transitions must be very slow near critical temperatures. Depth may help:
deeper stacked RBM/autoencoder top-layer marginals are more uniform, easing mode-hopping, but exploiting this
remains to be explored. Symptom picture: consecutive Gibbs samples from an MNIST DBM are nearly identical —
non-mixing at the semantic scale (the book's Fig. 17.2); ancestral samples from a GAN are independent, so no
mixing problem arises there.

*Objective mechanics* (§18.3–§18.6, §20.11). **Pseudolikelihood** replaces the chain-rule conditional
p(x_i | x_{<i}) with p(x_i | x_{−i}) computed as a ratio in which Z cancels, costing k × n evaluations instead
of kⁿ; maximizing it is asymptotically consistent (Mase, 1995, as cited), but finite-sample behaviour can
differ from maximum likelihood. **Score matching** minimizes the expected squared difference between model and
data scores. **(Generalized) denoising autoencoder sampling**: each chain step corrupts the current state x by
sampling x̃ from the corruption distribution, encodes h = f(x̃), decodes to obtain the parameters of the
reconstruction distribution p(x′|h), and samples the next state x′ from it; if the autoencoder is a consistent
estimator of the true conditional, the chain's stationary distribution is an implicit consistent estimator of
the data distribution (Bengio et al., 2013c/2014, as cited). For conditional sampling, **clamp** the observed
units and resample only the free ones, with the condition that the transition operator satisfy **detailed
balance** (Alain et al., 2015, as cited). The back-propagation-through-training variant replaces one-shot
encode-decode with multiple stochastic encode-decode steps initialized at training samples, penalizing the
final (or all) reconstructions: k steps are equivalent to one step for the stationary distribution but
empirically remove spurious modes better (§20.11, pp. 709–712). A related drawback of the wake-sleep algorithm
is that its inference network only ever sees model-typical v (§19.5.1, pp. 653–654).

## 5. Historical boundary register

The book is a 2016 source. Everything below was **recorded as historical** in the artifacts rather
than written as a current default. Each entry names where it appears so the boundary is checkable.

### 5.1 Era defaults presented as recommendations

- **The §11.2 baseline recipe** — ReLU/Leaky ReLU/PReLU/maxout units, momentum SGD with decay or
  Adam, early stopping, dropout, mild regularization unless the training set exceeds tens of
  millions of samples, and "use batch normalization as soon as optimization seems problematic."
  Recorded in `SOP-DL-02` §3.1 and `SOP-DL-04` §3.4 with the book's own caveat quoted: deep
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
- **Adversarial examples and the sign-of-gradient (FGSM-style) construction** (§7.13,
  pp. 292–294). Kept as a **2016 historical observation**, not as an active benchmark — `BC-DL-04`
  was withdrawn for this reason (§3.1). What the book states, recorded with its period scope:
  a network can be indistinguishable from correct on clean data and still be driven to near-total
  error by an imperceptible perturbation, demonstrated with GoogLeNet on ImageNet (Fig. 7.8); the
  construction is the elementwise **sign of the cost gradient with respect to the input**; the named
  cause is **excessive linearity** rather than insufficient capacity, with purely linear models such
  as logistic regression unable to resist at all and only large function families pushable toward
  locally constant behaviour; the named remedy is training on adversarially perturbed samples, which
  the book reports as reducing error on the **original i.i.d. test set**, plus *virtual* adversarial
  examples for unlabeled data under the stated assumption that distinct classes lie on separate
  manifolds. §7.14 (p. 296) frames this structurally: augmentation is non-infinitesimal tangent
  propagation, adversarial training is non-infinitesimal double backpropagation. The book supplies
  **no perturbation budget, no norm convention and no effect size**, which is precisely why this
  cannot be run as a BC without inventing numbers. Security implications are placed outside the
  chapter's scope (§7.13, p. 293) and are not evaluated anywhere in this package. Later attack
  families and later robustness metrics are not introduced.

  > **Modern update (2017–2026) — the named *cause* has been superseded; this entry is otherwise
  > unchanged.** The 2016 account above is retained verbatim as a period statement, and the withdrawal of
  > `BC-DL-04` is unaffected by what follows. The modern anchor textbook records a different explanation as
  > the current best one: adversarial examples "aren't due to a lack of robustness to data from outside the
  > training data manifold. Instead, they are exploiting a source of information that is in the training
  > distribution but which has a small norm and is imperceptible to humans" (attributing the result to
  > Ilyas et al., 2019).
  >
  > Why this matters for the historical entry rather than for a benchmark: the 2016 cause and the 2016
  > remedy are linked. Excessive linearity implies that pushing a network toward locally constant behaviour
  > — which is what training on perturbed samples does — addresses the mechanism. Under the modern account
  > the exploited information is *inside* the training distribution, so the remedy is not aimed at the cause
  > in the way the 2016 text implies. That is a further reason the 2016 prescription cannot simply be
  > reinstated as an active claim, and it is recorded here so the historical entry is not read as a
  > currently valid causal account.
  >
  > **No adversarial artifact is created in the modern-update lineage, and none is created here.**
  > Adversarial robustness evaluated under a declared threat model is a capability the Trustworthy-ML
  > package already owns: see
  > [`BM-05`](../../Benchmark/Trustworthy-ML-2023/BM-05-adversarial-robustness.md). This entry points there
  > rather than restating any procedure, per the plan governing that lineage.
  >
  > *Delta: [`delta_map.md`](../Deep-Learning-Modern-2017-2026/delta_map.md) §7.1. Source: `UDL` §20.4,
  > fol. 415.*

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

Nothing post-2016 was added to the **2016 text** of this package: no Transformer or attention mechanisms, no
AdamW or modern optimizer defaults, no learning-rate warmup/cosine schedules, no batch-size–LR
scaling rules, no scaling laws, no FID / Inception Score / perplexity-as-standard, no modern
leaderboards, no diffusion models, no large-pretrained-model or foundation-model transfer, no
current best practices for mixed precision or distributed training. Where a 2016 statement is now
known to be incomplete, the artifact marks it **historical** and stops there rather than updating
the source. A future source-update cycle may add later material; this cycle may not.

> **Modern update (2017–2026) — that future cycle has now run, and this section is scoped accordingly.**
> The paragraph above remains an accurate description of the 2016 procedure and of every 2016 citation in
> this package, none of which was altered. It is no longer an accurate description of the files as they now
> stand, because the sanctioned update lineage has added later material — inside blocks explicitly marked
> *Modern update (2017–2026)*, each carrying its own source line and a pointer to the delta record.
>
> The lineage's own records are the authority on what was and was not imported:
> [`sources.md`](../Deep-Learning-Modern-2017-2026/sources.md) for source identity, access and version, and
> [`delta_map.md`](../Deep-Learning-Modern-2017-2026/delta_map.md) for every candidate delta with its
> `2016 baseline → modern delta → source → destination → boundary` record and its status.
>
> Three of this section's exclusions were **not** lifted, and remain in force:
>
> - **No modern leaderboard and no family ranking.** Optimizer leaderboards are still rejected, and the
>   changed learning-rate-sensitivity assumption is recorded without producing a ranking (`SOP-DL-04` §3.4
>   step 6). Generative families are still not ranked; the one modern family-ranking statement carried is
>   carried *because* its source states it in terms of a single named metric (`BC-DL-11` §5).
> - **No architecture encyclopaedia.** No Transformer, vision-transformer or diffusion architecture entry,
>   variant catalogue or model-family BC was created. What entered is a *prior* in `SOP-DL-07`'s existing
>   bias register and a *precondition* on its model-class routing.
> - **No unsettled number.** Contested quantities — above all the compute-allocation exponents, where the
>   two sources in the lineage's own list disagree — are recorded in `delta_map.md` and imported nowhere.
>
> Two exclusions were **scoped rather than lifted**. Perplexity is still not used anywhere, because no
> source in either lineage names it as a generative-model metric. And the post-2016-metric exclusion now
> applies to the 2016 text and to `BC-DL-11` metrics 1–9 only: §4.M of that BC admits three later scores,
> each named by the anchor textbook and each carrying that source's stated failure modes, under the standing
> rules that every metric is a quantity a source names and that no threshold is invented.
>
> One item the 2016 package withdrew has been given a further reason to stay withdrawn. `BC-DL-04`'s
> adversarial-linearity claim was withdrawn because the book supplies no perturbation budget, norm
> convention or effect size. The modern account also supersedes the *cause* the 2016 remedy was aimed at,
> which is recorded at §5.1 above; robustness under a declared threat model is owned by Trustworthy-ML
> [`BM-05`](../../Benchmark/Trustworthy-ML-2023/BM-05-adversarial-robustness.md) and is not duplicated here.
>
> *Delta: `delta_map.md` §4.4, §6, §7.1, §7.2. Sources: as recorded per item in `delta_map.md`.*

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
