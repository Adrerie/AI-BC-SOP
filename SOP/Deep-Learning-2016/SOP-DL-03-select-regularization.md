# SOP-DL-03 — Select and configure regularization

**Stage:** regularize · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Choose and configure the modifications to the learning algorithm that are **intended** to reduce generalization
error. Record why you chose each modification for this task. Observed movement in training error is evidence to
report. That movement is not the criterion that decides whether something counted as regularization.

The book's definition is the operative frame. Regularization is any modification made to a learning algorithm.
The intention is to reduce the generalization error of the algorithm, but not its training error (§5.2.2,
p. 150, restated at §7, p. 253). Two consequences govern this SOP:

- Expressing a **preference** over functions is strictly more general than adding or removing members of the
  hypothesis space. The reason is that deleting a function is just an infinite preference against that function
  (§5.2.2, p. 150). So the design space is not "which penalty term". The design space is "which way of
  expressing a preference".
- There is **no best regularizer**. The no-free-lunch theorem implies that no optimal form of regularization
  exists. You must pick a regularizer that suits the task. The book's own position is that a very general
  regularizer may effectively solve a great many tasks (§5.2.2, p. 150).

In scope: §7.1–§7.5, §7.8–§7.14 and the §5.2.2 frame.

Out of scope:

- semi-supervised and multi-task sharing (`SOP-DL-08`)
- capacity diagnosis, which decides *whether* to regularize at all (`SOP-DL-02`)
- the search protocol that tunes the coefficients (`SOP-DL-05`)
- the mechanism-level evaluation of each lever (`BC-DL-03`)

The book's per-mechanism derivations and variant catalogues are not restated here. They are compressed in
[`concept_reconstruction.md`](../../Validation/Deep-Learning-2016/concept_reconstruction.md) §4.1(b).

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

1. Aim at the book's stated preference. The preference is **an appropriately regularized large model**, rather
   than a small model (§7, p. 254; §11.4.1, p. 444). The framing is a bias-variance move. Start from the case
   where the model family contains the true process *and* many other processes. Move from that case to the
   matched case. The move trades increased bias for reduced variance (§7, p. 253). A capacity increase raises
   variance and lowers bias. The book names cross-validation as the most common way to judge that trade-off
   (§5.4.4, pp. 159–160).
2. Change one lever at a time. Monitor **both** training error and test error. Each change then reads as a
   capacity change (§11.4.1, p. 444).

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

- Write the regularized objective as J̃(θ) = J(θ) + α Ω(θ) with α ∈ [0, ∞). In that form, α = 0 means no
  regularization (§7.1, p. 254).
- **Penalize weights, not biases.** Biases need far less data to fit. Regularizing the biases can cause marked
  underfitting (§7.1, p. 254).
- Use **one shared α across layers**, to keep the search space small. Do that unless per-layer tuning is
  affordable (§7.1, p. 255).

### 3.3 Configure the chosen lever

Each lever below carries one configuration rule, namely the fact that changes a decision. Full mechanics,
derivations and variant catalogues are in `concept_reconstruction.md` §4.1(b).

- **L2 / weight decay.** The method applies a constant-factor shrinkage before each ordinary gradient step.
  That shrinkage preserves the directions of high Hessian curvature. The low-curvature components decay toward
  zero. **The penalty produces no sparsity.** The result is exact for linear regression. There the penalty adds
  α to the diagonal of the covariance matrix. Features with high variance and low covariance to the target then
  shrink. The prior reading is an isotropic Gaussian prior (§7.1.1–7.1.2, pp. 255–261).

  > **Modern update (2017–2026) — under an adaptive optimizer these are two different levers, and the table
  > row above conflates them.** For standard SGD, L2 regularization and weight decay are equivalent, once you
  > rescale them by the learning rate. That equivalence does **not** hold for adaptive gradient algorithms.
  > Take the mechanism. Under L2, the λ·w term joins the loss gradient. The optimizer then normalizes both
  > terms by their typical summed magnitudes. Weights with large historic parameter and gradient magnitudes end
  > up **regularized less** than under weight decay. Decoupled weight decay instead regularizes every weight at
  > the same rate λ. A second benefit is separate, and also useful. Decoupling frees the optimal decay setting
  > from the learning-rate setting. Under L2, by contrast, the best λ is tightly coupled to α. The anchor
  > textbook states the same delta in one sentence. For Adam, the learning rate differs per parameter. L2
  > regularization and weight decay therefore differ under Adam. AdamW modifies Adam, and that change
  > implements weight decay correctly.
  >
  > In practice the change is **which knob you turn and what that knob is coupled to**. Before you configure
  > this lever, record which of the two forms the implementation actually performs. One form adds λ·w to the
  > gradient. The other shrinks θ by a factor at each step. Under an adaptive optimizer those two are not
  > interchangeable, so a swept λ means different things under each form. Suppose a learning-rate schedule runs
  > together with decoupled decay. Then also record the schedule of the decay relative to the learning rate.
  > The source supplies a schedule-multiplier mechanism for exactly that need. The source also supplies a
  > batch-budget normalization. That source itself describes the normalization as "merely one possibility
  > informed by few experiments."
  >
  > **No λ value is supplied here.** The published λ_norm values are batch-budget-normalized results. Those
  > results come from that source's own experiments, and are not transferable defaults. The justification
  > offered for decoupling is Bayesian filtering. That justification is explicitly theoretical. In the source's
  > own words it "does not directly apply to practical adaptive gradient algorithms". So this SOP does not
  > carry that justification as a mechanism claim.
  >
  > *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §3.1. Sources:
  > `ADAMW` (abstract, §2, Algorithm 2); `UDL` §9.1, fol. 156.*
- **L1.** The subgradient has constant magnitude, given by sign(w). That subgradient is a shift, not a
  scaling. The shift drives coordinates to **exactly zero**, once α is large enough. That behaviour is why L1
  selects features. **The analysis assumes a diagonal Hessian**, so decorrelate the inputs first, for example
  by PCA. The prior reading is an isotropic Laplace prior (§7.1.2, pp. 259–261).
- **Constraint + reprojection.** Take a descent step on J. Then project θ to the nearest feasible point. That
  route avoids the dying units that a penalty induces through non-convexity. The route also avoids the
  positive-feedback blowup at high learning rates. Constrain the **per-column** norms, not the Frobenius norm of
  the whole matrix. α and k move together monotonically. But α* does not reveal k (§7.2, pp. 261–263).
- **Well-posedness device.** Add αI to a singular XᵗX. That step halts the unbounded growth of ‖w‖ in logistic
  regression on linearly separable data. The growth stops once the slope of the likelihood equals the decay
  coefficient. The pseudoinverse solution is the α → 0 limit (§7.3, pp. 263–264).
- **Augmentation.** Augmentation is easy for classification. Augmentation is hard for density estimation,
  unless the density problem is already solved. Use label-preserving transforms, such as a few-pixel
  translation, rotation, or scaling. **Screen every transform for label destruction.** In OCR, a flip and a
  180° rotation confuse b with d, and 6 with 9. An out-of-plane rotation is label-preserving, but is hard to
  realize. Input noise and hidden-unit noise are augmentation at different levels of abstraction. **Hold the
  scheme fixed across the algorithms you compare.** Otherwise the gain belongs to the transforms, not to the
  algorithm. Judge the control as follows. Generic operations count as part of the algorithm. Gaussian input
  noise is one such operation. Domain-specific operations count as preprocessing. Random cropping is one such
  operation. The book adds that judging proper control requires a subjective judgement (§7.4, pp. 264–265).
- **Noise injection.** Noise injection is generally far more powerful than parameter shrinkage. The gap is
  largest on hidden units. For certain models, small-variance input noise can equal a weight penalty. Weight
  noise is mainly for recurrent nets. For simplified linear regression, that weight noise vanishes. The
  induced term in that case is parameter-independent (§7.5, pp. 265–267).
- **Label smoothing.** Spread the soft values across the k outputs. Standard cross-entropy then applies
  unchanged. That step stops the model from chasing exact probabilities, and does not harm correct
  classification (§7.5.1, p. 267).
- **Sharing / tying.** Use a soft penalty on ‖w⁽ᴬ⁾ − w⁽ᴮ⁾‖², or use hard equality. Prefer the hard form when
  memory matters, because training then stores only one parameter set. Apply sharing where the domain gives a
  known invariance. CNNs share across image positions, because natural images are translation-invariant. That
  sharing reduces the parameter count, and allows larger networks without more data (§7.9, §7.9.1,
  pp. 277–278).
- **Sparse representations.** Penalize the *activations*, not the parameters. Use Ω(h) = ‖h‖₁, with a
  coefficient of its own. §4.1(b) catalogues the four named alternatives (§7.10, pp. 278–280).
- **Bagging.** Draw k sets by bootstrap sampling, with replacement, at the size of the original set. Each
  bootstrap set keeps roughly two-thirds of the instances. Average the member outputs at inference. The
  expected squared error
  is ν when the member errors are perfectly correlated. That error is ν/k when the member errors are
  uncorrelated. Neural nets already decorrelate their members. The sources of that decorrelation are
  initialization, minibatch order, hyperparameter differences and nondeterminism. So the members may share one
  dataset. **Do not report an ensemble as a single algorithm's benchmark result.** Boosting is *not*
  regularizing, because boosting builds an ensemble of higher capacity. The usual ceiling is 5–10 networks
  (§7.11, pp. 280–283).
- **Dropout.** For each minibatch, draw one independent binary inclusion mask per unit. Fix that probability
  before training. The probability is not a function of the parameters, and not a function of the input. The
  masks apply to the input units and the hidden units, not to the output units. At inference, use the
  **weight-scaling rule**. That rule multiplies each unit's outgoing weights by the inclusion probability of
  that unit. Monte Carlo needs only 10–20 masks, and the best number of masks is problem-dependent. Weight
  scaling is *exact* only for model families **without nonlinear hidden units**. Enlarge the model, and add
  iterations, because dropout lowers effective capacity. *Interpretation test.* Randomness is neither necessary
  nor sufficient for the regularization effect. Fast dropout and **Dropout Boosting** show almost no
  regularization effect. That result supports the bagging explanation over the noise robustness explanation.
  Bagging requires members trained **independently** (§7.12, pp. 283–290).
- **Tangent propagation.** Penalize the directional derivative of f, along tangents ν⁽ⁱ⁾ that come from known
  transforms. The penalty resists only an **infinitesimal** perturbation. The penalty is also hard on
  rectified-linear models. Such a model can shrink its derivatives only by turning units off, or by shrinking
  weights. Augmentation works well with ReLU. Estimate the tangents with an autoencoder, for the manifold
  tangent classifier. The book states two identities. Augmentation is non-infinitesimal tangent propagation.
  Adversarial training is non-infinitesimal double backpropagation (§7.14, pp. 294–296).
- **Adversarial training — brief context only.** The book describes one result. A clean-accurate network can
  reach near-total error under an imperceptible perturbation. That perturbation equals the elementwise **sign
  of the cost gradient with respect to the input**. The book attributes the failure to **excessive linearity**,
  not to insufficient capacity. Training on such samples reduces error on the **original i.i.d. test set**, and
  the book reports that gain (§7.13, pp. 292–294). This SOP keeps the item as a 2016 observation, and as the
  third term in §7.14's identity. Adversarial training is **not** an active benchmark here. The book supplies
  no perturbation budget, no norm convention and no effect size. So a run of that benchmark would require
  invented values. `concept_reconstruction.md` §5.1 holds the full record.
- **Semi-supervised and multi-task** belong to `SOP-DL-08`. One condition carries into this SOP. Multi-task
  sharing gains **only if** the shared-factor assumption is reasonable (§7.7, pp. 268–270).

### 3.4 Early stopping (§7.8) — the algorithm, not just the idea

Early stopping is its own stage here. The book calls early stopping the most commonly used form of
regularization in deep learning. Early stopping also has an explicit algorithm.

3. Recognize the signature. Take a model large enough to overfit. The training error then falls steadily. The
   validation error turns, and rises again. The validation curve forms an asymmetric U-shape. The book states
   that this pattern "almost certainly occurs". Fig. 7.3 illustrates the pattern on MNIST with a maxout
   network (§7.8, p. 270).
4. Run **Algorithm 7.1** (§7.8, pp. 272–273). Fix the evaluation interval n in steps, and the patience p.
   Initialize the best validation error ν ← ∞. Then repeat the loop while j < p. In each pass, run n training
   steps, and evaluate the validation error. If the validation error improved, reset j ← 0, and save both the
   parameters θ* and the step count i*. Otherwise set j ← j + 1. At the end, return θ* and i*. **The book
   states no default for n or p**, so record both choices.

   The algorithm has two costs. The first cost is the periodic validation evaluation. That work is
   parallelizable on a separate machine. It is also reducible, with a smaller validation set or less frequent
   evaluation. The second cost is a stored copy of the best parameters, and that copy is negligible. The copy
   can live in slower, larger storage. Writes are rare, and training never reads the copy (§7.8, p. 271).
5. Prefer early stopping when the search budget is tight. Training time is the **only** hyperparameter that
   allows many values in a single run. Early stopping is also unobtrusive. Early stopping needs almost no
   change to the base training procedure. It changes neither the objective nor the set of allowed parameter
   values, so it does not disturb the learning dynamics. Weight decay, by contrast, must not be too high. Too
   high a weight decay can leave the network in a bad local minimum. That minimum corresponds to pathologically
   small weights. Use early stopping alone, or in combination. Even with a regularized objective, the best
   generalization is rarely at a local minimum of the training objective (§7.8, p. 271).
6. **Recover the withheld training data** with one of two second-round strategies.
   - *Algorithm 7.2*: reinitialize at random, and train on all the data for i* steps. The book flags one open
     question here. Match either the number of parameter *updates*, or the number of *passes*. A larger
     training set makes more updates per pass, so the two counts do not coincide.
   - *Algorithm 7.3*: keep θ*, and continue training on all the data. Stop when the validation mean loss falls
     below the value where early stopping terminated. That route is cheaper, but performs less well. The route
     may also never terminate, because the earlier target may be unreachable (§7.8, pp. 273–274).
7. Understand the mechanism, so that you can trade the lever against weight decay. Take a learning rate ε and
   τ steps. Then ετ measures effective capacity, and 1/(ετ) plays the role of a weight-decay coefficient. Now
   take a simple linear model with quadratic error, and plain gradient descent from the origin. Let ε be small,
   and let all the Hessian eigenvalues be small. Then τ acts inversely to the L2 coefficient, at least under
   the quadratic approximation. One usable consequence follows. The model learns parameters in large-curvature
   directions earlier than parameters in small-curvature directions. The practical advantage over weight decay
   is that **early stopping determines the right amount of regularization automatically**. Weight decay, by
   contrast, needs several runs at different coefficients (§7.8, pp. 274–277).

### 3.5 Validate and record

8. Score every candidate on **validation** error, never on training error (§5.2.2, p. 150; §5.3, p. 151).
9. Report training error and generalization error **separately** for each lever. If both errors improve, note
   that fact. Then check the capacity and optimization confounders (`SOP-DL-02`, `SOP-DL-04`) before you
   attribute the gain to regularization. `BC-DL-03` judges the lever by its mechanism observable.
10. Declare every quantity the book leaves open:
    - α per mechanism
    - n and p for early stopping
    - the number of ensemble members
    - the sparsity target
    - the tangent set

## 4. Important failure modes

- **Regularizing biases**, which need far less data to fit. Bias regularization can cause marked underfitting
  (§7.1, p. 254).
- **Expecting sparsity from L2** (§7.1.2, p. 260), or **applying the L1 diagonal-Hessian analysis to
  correlated inputs** without decorrelating the inputs first (§7.1.2, p. 259).
- **Weight decay set too high**, which drives the network into a bad local minimum of pathologically small
  weights (§7.8, p. 271).
- **Penalty where a constraint was needed**: dying units and high-learning-rate positive-feedback blowup
  (§7.2, pp. 262–263).
- **Label-destroying augmentation** — the OCR flip/180° case (§7.4, p. 265).
- **Comparing algorithms under different augmentation schemes**, which attributes the gain of the transforms to
  the algorithm (§7.4, p. 265).
- **Additive noise on rectified networks**, defeated by scaling activations up (§7.12, p. 292).
- **Dropout without compensating.** The model is not enlarged, or the iterations are not increased. Or dropout
  is applied where there are fewer than about 5000 samples (§7.12, pp. 289–290).
- **Forgetting the weight-scaling inference rule.** The inference-time inputs then do not match the
  training-time expectations (§7.12, p. 287).
- **Assuming weight scaling is exact for a deep nonlinear model.** The scaling is exact only for families
  without nonlinear hidden units (§7.12, pp. 286–289).
- **Explaining dropout by noise robustness** rather than by bagging. The Dropout Boosting control shows that
  noise alone does not regularize. Bagging also requires independently trained members (§7.12, p. 290).
- **Reporting an ensemble as a single algorithm's benchmark result** (§7.11, p. 282).
- **Early stopping without a validation set**, or without recovering the withheld data afterwards (§7.8,
  pp. 271–274).
- **Tangent propagation with rectified units** (§7.14, p. 296).
- **Classifying a lever by whether training error moved.** Report both errors. A lever that lowers both errors
  may work through capacity or through optimization. A lever that lowers neither error may still do its job on
  the mechanism observable (§5.2.2, p. 150; `BC-DL-03`).
- **Treating any of these levers as universally best.** The no-free-lunch argument rules out a universal
  choice (§5.2.2, p. 150).

## 5. Outputs and reporting

- The regularization block: mechanism, coefficient(s), and where the mechanism applies (weights not biases, and
  which layers share α). Name the validation metric used to select the mechanism.
- The task-specific reason for each mechanism, since no regularizer is universally best.
- Training error and generalization error reported **separately** for each lever. Flag any joint improvement,
  and address the capacity and optimization confounders.
- The augmentation scheme, with the label-safety screen recorded transform by transform. Give the
  generic-versus-domain-specific classification. State that all the compared algorithms used the identical
  scheme.
- Early stopping configuration: n, p, the monitored statistic, which second-round strategy was used
  (Algorithm 7.2 or 7.3), and whether ετ was traded against a weight-decay coefficient.
- Dropout configuration: inclusion probabilities per layer, model-size and iteration compensation, and the
  inference rule used (weight scaling vs Monte Carlo with a stated sample count).
- Ensemble disclosure: the number of members, and how the members were decorrelated. Add an explicit note if a
  benchmark number includes averaging.
- The quantities the book leaves open, and that you must therefore declare. Declare each one:
  - α per mechanism
  - n and p for early stopping
  - the number of ensemble members
  - the sparsity target
  - the tangent set
- **Modern update (2017–2026):** when the optimizer is adaptive and a shrinkage penalty is in use, declare
  **which** of the two forms the implementation applied. One form is an L2 term added to the gradient. The
  other is decoupled weight decay applied to the parameters. If you use decoupled decay, also record how the
  decay schedule moves against the learning-rate schedule. See the modern-update block in §3.3.

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

**Modern-update provenance.** Every row above is a 2016-book locator, and none was altered. One modern-update
block was added, inside §3.3's L2 / weight-decay entry. §5 carries the matching reporting line. The block is
sourced outside the 2016 book, and is recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§3.1.

The source keys are defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1. The keys are `ADAMW`
(abstract, §2, Algorithm 2) and `UDL` §9.1, fol. 156.

**Historical boundary.** The following are reported as book-era defaults, not as current ones:

- the typical dropout inclusion probabilities (0.8 input / 0.5 hidden)
- the ceiling of 5–10 networks per ensemble, with the ILSVRC six-model example
- the Alternative Splicing dataset (fewer than 5000 samples), where a Bayesian neural network beat dropout
- the MNIST maxout learning curve of Fig. 7.3
- the GoogLeNet-on-ImageNet adversarial demonstration
- the history of label smoothing since the 1980s
- the hardware habits around early stopping, which put validation evaluation on a separate machine, and stored
  the best parameters on disk
- the state-of-field claim that "dropout remains the most widely used implicit ensemble method"
- the state-of-field claim that early stopping is "the most commonly used form of regularization in deep
  learning"

The book also records the 2006–2012 belief that feedforward networks would not perform well. The book records
the reversal of that belief (§7, p. 252). That record is a reminder that the field's verdicts in this chapter
are dated.

The mechanisms themselves are stated as general, and are not era-bound. The list of mechanisms covers
penalties, constraints, augmentation, early stopping, sharing, sparsity, bagging, dropout and tangent methods.
Adversarial training is carried as a 2016 observation, not as a current robustness recipe.

**Formula caveat.** Display equations in this copy are images rather than text (see `SOURCE.md`). Two items are
therefore not recoverable from the extracted text. The first is the exact algebraic condition for the
early-stopping ↔ L2 equivalence. The second is the exact label-smoothing target values. Both are cited here at
prose level only.

The book itself states that relationship in words. The book says that τ acts inversely to the L2
coefficient, and that 1/(ετ) plays the role of the weight-decay coefficient. Both statements hold under a
quadratic approximation, with small ε and small eigenvalues.
