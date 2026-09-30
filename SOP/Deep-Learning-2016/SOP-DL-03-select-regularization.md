# SOP-DL-03 — Select and configure regularization

**Stage:** regularize · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Choose and configure the modifications to the learning algorithm that are **intended** to reduce
generalization error, and record why each one was chosen for this task. Observed movement in training error
is evidence to report, not the criterion that decides whether something counted as regularization.

The book's definition is the operative frame: regularization is any modification made to a learning algorithm
with the intention of reducing its generalization error but not its training error (§5.2.2, p. 150, restated
at §7, p. 253). Two consequences govern this SOP:

- Expressing a **preference** over functions is strictly more general than adding or removing members of the
  hypothesis space, because deleting a function is just an infinite preference against it (§5.2.2, p. 150). So
  the design space is not "which penalty term" but "which way of expressing a preference".
- There is **no best regularizer**. The no-free-lunch theorem implies no optimal form of regularization
  exists; one must be picked that suits the task, though the book's own position is that a very general
  regularizer may effectively solve a great many tasks (§5.2.2, p. 150).

In scope: §7.1–§7.5, §7.8–§7.14 and the §5.2.2 frame. Out of scope: semi-supervised and multi-task sharing
(`SOP-DL-08`); capacity diagnosis, which decides *whether* to regularize at all (`SOP-DL-02`); the search
protocol that tunes coefficients (`SOP-DL-05`); the mechanism-level evaluation of each lever (`BC-DL-03`).
The book's per-mechanism derivations and variant catalogues are compressed in
[`concept_reconstruction.md`](../../Validation/Deep-Learning-2016/concept_reconstruction.md) §4.1(b) and are
not restated here.

## 2. Inputs and assumptions

- A regime read from `SOP-DL-02`: the gap is the problem, not the training error. If training error is above
  target, regularization is the wrong lever (§11.4.1, p. 444).
- Validation material, because every choice here is scored on validation error, never on training error
  (§5.2.2, p. 150; §5.3, p. 151).
- Knowledge of the task's invariances and of which transformations preserve the label (§7.4, p. 265).
- A budget: several regularizers change the compute profile — dropout requires a larger model and more
  iterations (§7.12, pp. 289–290), bagging multiplies training cost (§7.11, p. 282).

## 3. Procedure

### 3.1 Set the target regime

1. Aim at the book's stated preference: **an appropriately regularized large model**, rather than a small
   model (§7, p. 254; §11.4.1, p. 444). The framing is a bias-variance move: go from the case where the model
   family contains the true process *and* many others, to the matched case, trading increased bias for
   reduced variance (§7, p. 253). Capacity increase raises variance and lowers bias; cross-validation is
   named as the most common way to judge that trade-off (§5.4.4, pp. 159–160).
2. Change one lever at a time while monitoring **both** training and test error, so each change can be read as
   a capacity change (§11.4.1, p. 444).

### 3.2 Pick the lever from what is actually known about the task

Choose by which precondition holds, not by familiarity with the mechanism.

| If this holds | Use | Locator |
| --- | --- | --- |
| You want small weights and have no other information | L2 penalty (weight decay) | §7.1.1, pp. 255–258 |
| You want **feature selection** / exact zeros | L1 penalty, with inputs decorrelated | §7.1.2, pp. 259–261 |
| The admissible size k is **known directly** | Explicit constraint with reprojection, per-column norms | §7.2, pp. 261–263 |
| The problem is **under-determined** (singular XᵗX, or separable logistic regression) | Regularization as a well-posedness device | §7.3, pp. 263–264 |
| New (x, y) pairs can be fabricated cheaply and a label-preserving transform exists | Dataset augmentation | §7.4, pp. 264–265 |
| The task has known **infinitesimal** invariances and the model is not rectified | Tangent propagation | §7.14, pp. 294–296 |
| Two related models should have similar parameters | Parameter sharing / tying | §7.9, pp. 277–278 |
| You want the **activations** sparse rather than the weights | Activation L1 (or a named alternative) | §7.10, pp. 278–280 |
| Training cost is cheap to multiply and members decorrelate naturally | Bagging | §7.11, pp. 280–283 |
| You need one model with an implicit-ensemble effect | Dropout | §7.12, pp. 283–292 |
| Training time is the only lever you can afford to sweep | Early stopping — the cheapest, see §3.4 | §7.8, pp. 270–277 |
| Nothing else is available and the objective is differentiable | Inject noise (input or hidden units) | §7.5, pp. 265–267 |

Three rules apply to every row:

- Write the regularized objective as J̃(θ) = J(θ) + α Ω(θ) with α ∈ [0, ∞), α = 0 meaning no regularization
  (§7.1, p. 254).
- **Penalize weights, not biases.** Biases need far less data to fit, and regularizing them can cause marked
  underfitting (§7.1, p. 254).
- Use **one shared α across layers** to keep the search space small, unless per-layer tuning is affordable
  (§7.1, p. 255).

### 3.3 Configure the chosen lever

One configuration rule per lever — the fact that changes a decision. Full mechanics, derivations and variant
catalogues are in `concept_reconstruction.md` §4.1(b).

- **L2 / weight decay.** Constant-factor shrinkage applied before each ordinary gradient step; preserves
  directions of high Hessian curvature while low-curvature components decay toward zero. **Produces no
  sparsity.** Exact in linear regression, where it adds α to the covariance diagonal so high-variance features
  with low covariance to the target are shrunk. Isotropic Gaussian prior (§7.1.1–7.1.2, pp. 255–261).
- **L1.** Constant-magnitude subgradient via sign(w) — a shift, not a scaling — driving coordinates to **exactly
  zero** once α is large enough, which is why it selects features. **Assumes a diagonal Hessian**, so
  decorrelate inputs first (e.g. by PCA). Isotropic Laplace prior (§7.1.2, pp. 259–261).
- **Constraint + reprojection.** Descent step on J, then project θ to the nearest feasible point. Avoids the
  dying units a penalty induces through non-convexity and the positive-feedback blowup at high learning rates.
  Constrain **per-column** norms, not the whole-matrix Frobenius norm. α and k move together monotonically,
  but α* does not reveal k (§7.2, pp. 261–263).
- **Well-posedness device.** αI added to a singular XᵗX; halts unbounded ‖w‖ growth in logistic regression on
  linearly separable data, where growth stops once the likelihood's slope equals the decay coefficient. The
  pseudoinverse solution is the α → 0 limit (§7.3, pp. 263–264).
- **Augmentation.** Easy for classification, hard for density estimation unless the density problem is
  already solved. Use label-preserving transforms (few-pixel translation, rotation, scaling). **Screen every
  transform for label destruction** — flip and 180° rotation confuse b with d and 6 with 9 in OCR; out-of-plane
  rotation is label-preserving but hard to realize. Input-noise and hidden-unit noise are augmentation at
  different abstraction levels. **Hold the scheme fixed across compared algorithms**, or the gain belongs to
  the transforms: generic operations such as Gaussian input noise count as part of the algorithm,
  domain-specific ones such as random cropping count as preprocessing — and judging proper control requires
  subjective judgement (§7.4, pp. 264–265).
- **Noise injection.** Generally far more powerful than shrinking parameters, especially on hidden units;
  small-variance input noise can equal a weight penalty for certain models. Weight noise is mainly for
  recurrent nets, and vanishes for simplified linear regression, where the induced term is
  parameter-independent (§7.5, pp. 265–267).
- **Label smoothing.** Soft values spread across the k outputs; standard cross-entropy applies unchanged.
  Stops the model chasing exact probabilities without harming correct classification (§7.5.1, p. 267).
- **Sharing / tying.** Soft penalty on ‖w⁽ᴬ⁾ − w⁽ᴮ⁾‖² or hard equality; prefer hard when memory matters, since
  only one parameter set is stored. Apply where a domain invariance is known — CNNs share across image
  positions because natural images are translation-invariant, reducing parameter count and allowing larger
  networks without more data (§7.9, §7.9.1, pp. 277–278).
- **Sparse representations.** Penalize *activations*, not parameters: Ω(h) = ‖h‖₁ with its own coefficient. The
  four named alternatives are catalogued in §4.1(b) (§7.10, pp. 278–280).
- **Bagging.** k bootstrap sets sampled with replacement at the original size, each retaining roughly
  two-thirds of the instances; average member outputs at inference. Expected squared error is ν with perfectly
  correlated member errors and ν/k uncorrelated. Neural nets already decorrelate through initialization,
  minibatch order, hyperparameter differences and nondeterminism, so members may share one dataset. **Do not
  report an ensemble as a single algorithm's benchmark result.** Boosting is *not* regularizing — it builds a
  higher-capacity ensemble. Ceiling is usually 5–10 networks (§7.11, pp. 280–283).
- **Dropout.** Per minibatch, draw an independent binary inclusion mask per unit; the probability is fixed
  before training and is not a function of the parameters or the input; masks apply to input and hidden
  (non-output) units. At inference use the **weight-scaling rule** (multiply each unit's outgoing weights by
  its inclusion probability); Monte Carlo needs only 10–20 masks and the best approximation is
  problem-dependent. Weight scaling is *exact* only for families **without nonlinear hidden units**. Enlarge
  the model and add iterations, since dropout lowers effective capacity. *Interpretation test:* randomness is
  neither necessary nor sufficient — fast dropout and **Dropout Boosting** show almost no regularization
  effect, supporting the bagging explanation over noise robustness, and bagging requires members trained
  **independently** (§7.12, pp. 283–290).
- **Tangent propagation.** Penalize the directional derivative of f along tangents ν⁽ⁱ⁾ derived from known
  transforms. Resists only **infinitesimal** perturbation, and is hard on rectified-linear models, which can
  only shrink derivatives by turning units off or shrinking weights; augmentation works well with ReLU.
  Estimate tangents with an autoencoder for the manifold tangent classifier. The book's identities:
  augmentation is non-infinitesimal tangent propagation, adversarial training is non-infinitesimal double
  backpropagation (§7.14, pp. 294–296).
- **Adversarial training — brief context only.** The book describes driving a clean-accurate network to
  near-total error with an imperceptible perturbation equal to the elementwise **sign of the cost gradient
  with respect to the input**, attributes it to **excessive linearity** rather than insufficient capacity, and
  reports that training on such samples reduces error on the **original i.i.d. test set** (§7.13,
  pp. 292–294). Retained as a 2016 observation and as the third term in §7.14's identity. It is **not** an
  active benchmark here: the book supplies no perturbation budget, no norm convention and no effect size, so
  running it would require inventing them. Full record in `concept_reconstruction.md` §5.1.
- **Semi-supervised and multi-task** belong to `SOP-DL-08`; the one condition to carry here is that multi-task
  sharing gains **only if** the shared-factor assumption is reasonable (§7.7, pp. 268–270).

### 3.4 Early stopping (§7.8) — the algorithm, not just the idea

Kept as its own stage because the book calls it the most commonly used form of regularization in deep
learning and because it has an explicit algorithm.

3. Recognize the signature: with a model large enough to overfit, training error falls steadily while
   validation error turns and rises again, forming an asymmetric U-shape — the book states this "almost
   certainly occurs" (illustrated on MNIST with a maxout network, Fig. 7.3) (§7.8, p. 270).
4. Run **Algorithm 7.1** (§7.8, pp. 272–273): fix the evaluation interval n in steps and the patience p;
   initialize the best validation error ν ← ∞; while j < p: run n training steps, evaluate the validation
   error; if it improved, reset j ← 0 and save both the parameters θ* and the step count i*; otherwise
   j ← j + 1. Return θ* and i*. **The book states no default for n or p** — both are choices to record. Its
   two costs are periodic validation evaluation (parallelizable on a separate machine, or reducible with a
   smaller validation set or less frequent evaluation) and keeping a copy of the best parameters (negligible —
   it can live in slower, larger storage, since writes are rare and never read during training) (§7.8, p. 271).
5. Prefer it when the search budget is tight: training time is the **only** hyperparameter that lets many
   values be tried in a single run, and early stopping is unobtrusive — it needs almost no change to the base
   training procedure, the objective or the set of allowed parameter values, so it does not disturb learning
   dynamics. Weight decay, by contrast, must not be set too high, or the network can fall into a bad local
   minimum corresponding to pathologically small weights. It can be used alone or combined; even with a
   regularized objective, the best generalization is rarely at a local minimum of the training objective
   (§7.8, p. 271).
6. **Recover the withheld training data** with one of two second-round strategies: *Algorithm 7.2* —
   reinitialize randomly and train on all data for i* steps, with the book flagging the open question of
   whether to match the number of parameter *updates* or the number of *passes*, since a larger training set
   makes more updates per pass; or *Algorithm 7.3* — keep θ* and continue training on all data, stopping when
   the validation mean loss falls below the value at which early stopping terminated, which is cheaper but
   performs less well and may not terminate at all, because the earlier target may be unreachable (§7.8,
   pp. 273–274).
7. Understand the mechanism so the lever can be traded against weight decay: with learning rate ε and τ steps,
   ετ measures effective capacity and 1/(ετ) plays the role of a weight-decay coefficient. For a simple linear
   model with quadratic error and plain gradient descent from the origin, with ε small and all Hessian
   eigenvalues small, τ acts inversely to the L2 coefficient — at least under the quadratic approximation. A
   usable consequence: parameters in large-curvature directions are learned earlier than those in
   small-curvature directions. The practical advantage over weight decay is that **early stopping determines
   the right amount of regularization automatically**, whereas weight decay needs several runs at different
   coefficients (§7.8, pp. 274–277).

### 3.5 Validate and record

8. Score every candidate on **validation** error, never training error (§5.2.2, p. 150; §5.3, p. 151).
9. Report training and generalization error **separately** for each lever. If both improve, note it and check
   the capacity and optimization confounders (`SOP-DL-02`, `SOP-DL-04`) before attributing the gain to
   regularization; the lever is judged by its mechanism observable, per `BC-DL-03`.
10. Declare every quantity the book leaves open: α per mechanism, n and p for early stopping, the number of
    ensemble members, the sparsity target, and the tangent set.

## 4. Important failure modes

- **Regularizing biases**, which need far less data to fit and can cause marked underfitting (§7.1, p. 254).
- **Expecting sparsity from L2** (§7.1.2, p. 260), or **applying the L1 diagonal-Hessian analysis to
  correlated inputs** without decorrelating first (§7.1.2, p. 259).
- **Weight decay set too high**, driving the network into a bad local minimum with pathologically small
  weights (§7.8, p. 271).
- **Penalty where a constraint was needed**: dying units and high-learning-rate positive-feedback blowup
  (§7.2, pp. 262–263).
- **Label-destroying augmentation** — the OCR flip/180° case (§7.4, p. 265).
- **Comparing algorithms under different augmentation schemes**, which attributes the transforms' gain to the
  algorithm (§7.4, p. 265).
- **Additive noise on rectified networks**, defeated by scaling activations up (§7.12, p. 292).
- **Dropout without compensating**: model not enlarged, iterations not increased, or applied where there are
  fewer than about 5000 samples (§7.12, pp. 289–290).
- **Forgetting the weight-scaling inference rule**, so inference-time inputs do not match training-time
  expectations (§7.12, p. 287).
- **Assuming weight scaling is exact for a deep nonlinear model** — it is exact only for families without
  nonlinear hidden units (§7.12, pp. 286–289).
- **Explaining dropout by noise robustness** rather than by bagging; the Dropout Boosting control shows noise
  alone does not regularize, and bagging requires independently trained members (§7.12, p. 290).
- **Reporting an ensemble as a single algorithm's benchmark result** (§7.11, p. 282).
- **Early stopping without a validation set**, or without recovering the withheld data afterwards (§7.8,
  pp. 271–274).
- **Tangent propagation with rectified units** (§7.14, p. 296).
- **Classifying a lever by whether training error moved.** Report both errors; a lever that lowers both may be
  acting through capacity or optimization, and one that lowers neither may still be doing its job on the
  mechanism observable (§5.2.2, p. 150; `BC-DL-03`).
- **Treating any of these as universally best** — the no-free-lunch argument rules it out (§5.2.2, p. 150).

## 5. Outputs and reporting

- Regularization block: mechanism, coefficient(s), where applied (weights not biases; which layers share α),
  and the validation metric used to select it.
- The task-specific reason for each mechanism, since no regularizer is universally best.
- Training and generalization error reported separately per lever, with any joint improvement flagged and the
  capacity/optimization confounders addressed.
- Augmentation scheme with the label-safety screen recorded transform by transform, the
  generic-vs-domain-specific classification, and the statement that all compared algorithms used the
  identical scheme.
- Early stopping configuration: n, p, the monitored statistic, which second-round strategy was used
  (Algorithm 7.2 or 7.3), and whether ετ was traded against a weight-decay coefficient.
- Dropout configuration: inclusion probabilities per layer, model-size and iteration compensation, and the
  inference rule used (weight scaling vs Monte Carlo with a stated sample count).
- Ensemble disclosure: number of members, how they were decorrelated, and an explicit note if a benchmark
  number includes averaging.
- The quantities the book leaves open and that must therefore be declared: α per mechanism, n and p for early
  stopping, the number of ensemble members, the sparsity target, and the tangent set.

## 6. Source traceability

| Claim or step | Locator |
| --- | --- |
| Regularization defined as reducing generalization but not training error; preference more general than hypothesis-space editing; no best regularizer | §5.2.2, pp. 148–150 |
| Bias-variance move; "appropriately regularized large model"; CV as the usual way to judge the trade-off; capacity ↑ ⇒ variance ↑, bias ↓ | §7, pp. 253–254; §5.4.4, pp. 159–160; §11.4.1, p. 444 |
| J̃ = J + αΩ; penalize weights not biases; shared α across layers | §7.1, pp. 254–255 |
| L2 mechanics, curvature-eigendirection behaviour, linear-regression diagonal, no sparsity; L1 subgradient, exact zeros, feature selection, LASSO, diagonal-Hessian assumption; Gaussian/Laplace prior readings | §7.1.1–§7.1.2, pp. 255–261 |
| Constraint + reprojection; dying units; high-LR blowup; per-column norms; α–k monotonicity | §7.2, pp. 261–263 |
| Under-determined problems; XᵗX + αI; logistic regression on separable data; pseudoinverse as α→0 limit | §7.3, pp. 263–264 |
| Augmentation: cheapness by task, label-preserving transforms, OCR counterexample, out-of-plane rotation, noise as augmentation, benchmark control and the generic/domain-specific convention | §7.4, pp. 264–265 |
| Noise robustness; input noise vs parameter shrinkage; weight noise and its vanishing in linear regression; label smoothing | §7.5, §7.5.1, pp. 265–267 |
| Learning-curve U-shape; Algorithm 7.1 with n and p; costs and their mitigation; unobtrusiveness vs weight decay; Algorithms 7.2 and 7.3; ετ ↔ weight decay equivalence and its assumptions; large-curvature directions learned first; automatic regularization amount | §7.8, pp. 270–277 |
| Parameter sharing soft vs hard; memory advantage; CNN translation invariance | §7.9, §7.9.1, pp. 277–278 |
| Sparse representations: activation L1, Student-t, KL, mean-activation target, OMP-k | §7.10, pp. 278–280 |
| Bagging: bootstrap with replacement, ~2/3 retention, error decomposition ν vs ν/k, decorrelation in neural nets, benchmark reporting rule, Boosting is not regularizing, 5–10 member ceiling | §7.11, pp. 280–283 |
| Dropout: masks, inclusion probabilities 0.8/0.5, weight-scaling inference rule, exactness families, MC sample counts, capacity compensation, dataset-size limits, μ-parameterized variants, multiplicative vs additive noise, fast dropout and Dropout Boosting, linear-regression L2 equivalence | §7.12, pp. 283–292 |
| Adversarial examples as a 2016 observation: sign-of-gradient perturbation, GoogLeNet/ImageNet demonstration, excessive linearity as the cause, adversarial training improves i.i.d. test error, virtual adversarial examples and its manifold assumption | §7.13, pp. 292–294 |
| Tangent propagation, manifold tangent classifier, infinitesimal-only resistance, ReLU incompatibility, augmentation and adversarial training as non-infinitesimal forms | §7.14, pp. 294–296 |
| Multi-task gain conditional on the shared-factor assumption | §7.7, pp. 268–270 |

**Historical boundary.** Reported as book-era rather than current defaults: the typical dropout inclusion
probabilities (0.8 input / 0.5 hidden); the 5–10 network ensembling ceiling with the ILSVRC six-model example;
the Alternative Splicing dataset (fewer than 5000 samples) where a Bayesian neural network beat dropout; the
MNIST maxout learning curve of Fig. 7.3; the GoogLeNet-on-ImageNet adversarial demonstration; label
smoothing's history since the 1980s; the hardware habits around early stopping (validation evaluation on a
separate machine, best parameters stored on disk); and the two state-of-field claims that "dropout remains the
most widely used implicit ensemble method" and that early stopping is "the most commonly used form of
regularization in deep learning". The book also records the 2006–2012 belief that feedforward networks would
not perform well, and its reversal (§7, p. 252) — a reminder that the field's verdicts in this chapter are
dated. The mechanisms themselves (penalties, constraints, augmentation, early stopping, sharing, sparsity,
bagging, dropout, tangent methods) are stated as general and are not era-bound; adversarial training is
carried as a 2016 observation, not as a current robustness recipe.

**Formula caveat.** Display equations in this copy are images rather than text (see `SOURCE.md`), so the exact
algebraic condition for the early-stopping ↔ L2 equivalence and the exact label-smoothing target values are
not recoverable from the extracted text. Both are cited here at prose level only, which is how the book states
the relationship in words: τ acts inversely to the L2 coefficient, and 1/(ετ) plays the role of the
weight-decay coefficient, under a quadratic approximation with small ε and small eigenvalues.
