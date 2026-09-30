# SOP-DL-03 — Select and configure regularization

**Stage:** regularize · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Choose and configure the modifications to the learning algorithm that reduce **generalization** error
without reducing training error, and record why each one was chosen for this task.

The book's definition is the operative frame: regularization is any modification made to a learning
algorithm with the intention of reducing its generalization error but not its training error
(§5.2.2, p. 150, restated at §7, p. 253). Two consequences govern this SOP:

- Expressing a **preference** over functions is strictly more general than adding or removing members of
  the hypothesis space, because deleting a function is just an infinite preference against it (§5.2.2,
  p. 150). So the design space is not "which penalty term" but "which way of expressing a preference".
- There is **no best regularizer**. The no-free-lunch theorem implies no optimal form of regularization
  exists; one must be picked that suits the task, though the book's own position is that a very general
  regularizer may effectively solve a great many tasks (§5.2.2, p. 150).

In scope: §7.1–§7.5, §7.8–§7.14 and the §5.2.2 frame. Out of scope: semi-supervised and multi-task
sharing, which are covered by `SOP-DL-08`; capacity diagnosis, which decides *whether* to regularize at
all (`SOP-DL-02`); the search protocol that tunes coefficients (`SOP-DL-05`).

## 2. Inputs and assumptions

- A regime read from `SOP-DL-02`: the gap is the problem, not the training error. If training error is
  above target, regularization is the wrong lever (§11.4.1, p. 444).
- Validation material, because every choice here is scored on validation error, never on training error
  (§5.2.2, p. 150; §5.3, p. 151).
- Knowledge of the task's invariances and of which transformations preserve the label (§7.4, p. 265).
- A budget: several regularizers change the compute profile — dropout requires a larger model and more
  iterations (§7.12, pp. 289–290), bagging multiplies training cost (§7.11, p. 282).

## 3. Procedure

### 3.1 Set the target regime

1. Aim at the book's stated preference: **an appropriately regularized large model**, rather than a
   small model (§7, p. 254; §11.4.1, p. 444). The chapter's framing is a bias-variance move: go from the
   case where the model family contains the true process *and* many others, to the matched case, trading
   increased bias for reduced variance (§7, p. 253). Capacity increase raises variance and lowers bias;
   cross-validation is named as the most common way to judge that trade-off (§5.4.4, pp. 159–160).
2. Change one lever at a time while monitoring **both** training and test error, so each change can be
   read as a capacity change (§11.4.1, p. 444).

### 3.2 Parameter penalties and constraints (§7.1–§7.3)

3. Write the regularized objective as J̃(θ) = J(θ) + α Ω(θ) with α ∈ [0, ∞), where α = 0 means no
   regularization (§7.1, p. 254).
4. **Penalize weights, not biases.** Biases need far less data to fit than weights, and regularizing
   them can cause marked underfitting (§7.1, p. 254).
5. Use **one shared α across layers** to keep the search space small, unless per-layer tuning is
   affordable (§7.1, p. 255).
6. Choose Ω by what you want the solution to look like:
   - **L2** (weight decay; also called ridge regression or Tikhonov regularization) applies a constant-factor
     shrinkage to the weights before the ordinary gradient update at each step. It preserves directions of
     high Hessian curvature while components in low-curvature directions decay toward zero. In linear
     regression it adds α to the diagonal of the covariance matrix, whose diagonal entries are the
     per-feature variances, so high-variance features with low covariance to the target are shrunk — exact
     here because the cost is genuinely quadratic (§7.1.1, pp. 255–258). L2 **does not produce sparsity**
     (§7.1.2, p. 260). Prior reading: isotropic Gaussian (§7.1.2, p. 261).
   - **L1** contributes a constant-magnitude subgradient term using sign(w) — a constant shift rather than a
     linear scaling — and drives coordinates to **exactly zero** when α is large enough, which is why it
     performs feature selection (LASSO is L1 plus a linear model plus least squares). Its analysis assumes a
     diagonal Hessian, which is reasonable if inputs have been decorrelated, e.g. by PCA (§7.1.2,
     pp. 259–261). Prior reading: isotropic Laplace (§7.1.2, p. 261).
7. When the admissible size k is known directly, prefer an **explicit constraint with reprojection**: take
   a descent step on J, then project θ to the nearest feasible point (§7.2, p. 262). Reprojection avoids
   the "dying units" that a penalty can induce through non-convexity, and prevents the positive-feedback
   blowup that occurs at high learning rates (§7.2, pp. 262–263). Constrain **per-column** weight-matrix
   norms rather than the whole-matrix Frobenius norm, and in practice always implement it by reprojection
   (§7.2, p. 263). α and k move together monotonically (larger α ⇒ smaller feasible region) but α* does
   not reveal k, and the relation depends on the form of J (§7.2, p. 262).
8. Use regularization as a **well-posedness device** when the problem is under-determined (§7.3,
   pp. 263–264): adding αI to a singular XᵗX; halting the unbounded growth of ‖w‖ in logistic regression on
   linearly separable data, where growth stops once the likelihood's slope equals the decay coefficient.
   The pseudoinverse solution is the α → 0 limit.

### 3.3 Data-side levers (§7.4–§7.5)

9. **Dataset augmentation.** First ask whether new (x, y) pairs can be fabricated cheaply: this is easy for
   classification and hard for density estimation, unless the density problem is already solved (§7.4,
   p. 264). Then:
   - use label-preserving transforms — translation by a few pixels in each direction (effective even with
     convolution and pooling), rotation, scaling (§7.4, p. 264);
   - **screen every transform for label destruction**: transforms that change the class must not be used.
     The book's counterexample is horizontal flip and 180° rotation for OCR, which confuse b with d and 6
     with 9. Out-of-plane rotation is label-preserving but hard to realize (§7.4, p. 265);
   - treat input-noise injection and hidden-unit noise as augmentation at different abstraction levels, and
     tune hidden-unit noise magnitude carefully (§7.4, p. 265);
   - **hold augmentation fixed across compared algorithms.** When comparing algorithm A to B, both must use
     the identical hand-designed augmentation scheme, otherwise an improvement may be attributable to the
     transforms rather than to the algorithm. The book's classification convention: generic operations such
     as Gaussian input noise count as part of the algorithm, while domain-specific operations such as random
     image cropping count as separate preprocessing. It concedes that judging whether an experiment is
     properly controlled requires subjective judgement (§7.4, p. 265).
10. **Noise robustness.** Injecting noise is generally far more powerful than shrinking parameters,
    especially when applied to hidden units; input noise with small variance can be equivalent to a weight
    penalty for certain models (§7.5, pp. 265–266). Weight noise pushes the solution toward regions robust
    to weight perturbation and is mainly used for recurrent nets; note that for simplified linear regression
    the induced term is parameter-independent and has no effect on the gradient, so the mechanism vanishes
    there (§7.5, pp. 266–267).
11. **Label smoothing.** Replace exact 0/1 targets with soft values spread across the k outputs; the
    standard cross-entropy applies unchanged. It stops the model from chasing exact probabilities without
    harming correct classification, and has been in use since the 1980s (§7.5.1, p. 267).

### 3.4 Early stopping (§7.8) — the algorithm, not just the idea

12. Recognize the signature: with a model large enough to overfit, training error falls steadily while
    validation error turns and rises again, forming an asymmetric U-shape. The book states this "almost
    certainly occurs" (illustrated on MNIST with a maxout network, Fig. 7.3) (§7.8, p. 270).
13. Run **Algorithm 7.1** (§7.8, pp. 272–273): fix the evaluation interval n in steps and the patience p;
    initialize the best validation error ν ← ∞; while j < p: run n training steps, evaluate the validation
    error; if it improved, reset j ← 0 and save both the parameters θ* and the step count i*; otherwise
    j ← j + 1. Return θ* and i*. **The book states no default for n or p** — both are choices to record.
14. Budget its two costs: periodic validation evaluation (parallelizable on a separate machine, CPU or GPU;
    or reduce cost with a smaller validation set or less frequent evaluation), and keeping a copy of the
    best parameters — negligible, since it can live in slower, larger storage (train in GPU memory, store
    the best parameters in main memory or on disk) because writes are rare and never read during training
    (§7.8, p. 271).
15. Note why it is the cheapest lever: training time is the **only** hyperparameter that lets many values be
    tried in a single run, and early stopping is unobtrusive — it needs almost no change to the base
    training procedure, the objective function or the set of allowed parameter values, so it does not
    disturb learning dynamics. Weight decay, by contrast, must not be set too high, or the network can fall
    into a bad local minimum corresponding to pathologically small weights (§7.8, p. 271). It can be used
    alone or combined with other regularizers; even with a regularized objective, the best generalization is
    rarely at a local minimum of the training objective (§7.8, p. 271).
16. **Recover the withheld training data** with one of the two second-round strategies:
    - *Algorithm 7.2*: reinitialize randomly and train on all data for i* steps. Open question the book
      flags: whether to match the number of parameter *updates* or the number of *passes*, since a larger
      training set makes more updates per pass (§7.8, pp. 273–274).
    - *Algorithm 7.3*: keep θ* and continue training on all data, monitoring the validation mean loss and
      stopping when it falls below the value at which early stopping terminated. Cheaper, but the book
      states it performs less well and may not terminate at all, because the earlier target may be
      unreachable (§7.8, pp. 273–274).
17. Understand the mechanism so the lever can be traded against weight decay: with learning rate ε and τ
    steps, ετ measures effective capacity, and 1/(ετ) plays the role of a weight-decay coefficient
    (Bishop, 1995a; Sjöberg and Ljung, 1995, as cited). For a simple linear model with quadratic error and
    plain gradient descent, initialized at the origin, with ε small and all Hessian eigenvalues small, τ acts
    inversely to the L2 coefficient — the equivalence holds at least under the quadratic approximation
    (§7.8, pp. 274–276). A consequence worth using: parameters in large-curvature directions are learned
    earlier than those in small-curvature directions. The practical advantage over weight decay is that
    **early stopping determines the right amount of regularization automatically**, whereas weight decay
    needs several training runs at different coefficients (§7.8, p. 277).

### 3.5 Algorithm-side levers (§7.9–§7.14)

18. **Parameter sharing / tying.** Where two related models should have similar parameters, either add a
    soft penalty on ‖w⁽ᴬ⁾ − w⁽ᴮ⁾‖² or impose the hard equality constraint; prefer hard sharing when memory
    matters, since only one parameter set is stored. Apply it where a domain invariance is known: CNNs share
    weights across image positions because natural images are translation-invariant, which reduces parameter
    count and allows larger networks without more data (§7.9, §7.9.1, pp. 277–278).
19. **Sparse representations.** Penalize *activations* rather than parameters: Ω(h) = ‖h‖₁ with its own
    coefficient. Alternatives the book names: Student-t-derived penalties, KL penalties for constraining
    elements to the unit interval, matching the mean activation to a target vector (an all-0.01 target is the
    cited example), or a hard constraint on the number of non-zeros solved by orthogonal matching pursuit
    (OMP-k), which is efficient when W is orthogonal (§7.10, pp. 278–280).
20. **Bagging and ensembling.** Build k bootstrap datasets by sampling with replacement at the original size
    (each retains roughly two-thirds of the original instances), train model i on dataset i, and average
    member outputs at inference. Expected squared error is ν when member errors are perfectly correlated and
    ν/k when uncorrelated (the derivation assumes multivariate normal errors with common variance and
    covariance). For neural networks, decorrelation already arises from random initialization, minibatch
    ordering, hyperparameter differences and nondeterminism, so members may share a single dataset.
    **Reporting rule:** model averaging is discouraged when benchmarking algorithms in a scientific paper,
    because any algorithm benefits at the cost of compute and storage. Note that Boosting is *not* a
    regularizing ensemble — it builds a higher-capacity one. Practical ceiling: usually only 5–10 networks
    can be ensembled (§7.11, pp. 280–283).
21. **Dropout.** Training recipe: for each minibatch, draw an independent binary inclusion mask per unit;
    the inclusion probability is a hyperparameter fixed before training and is not a function of the current
    parameters or of the input; masks are applied to input and hidden (non-output) units; then run the
    ordinary forward, backward and update steps. The book's typical values are **0.8 for input units and 0.5
    for hidden units** (§7.12, pp. 283–285).
    - *Inference*: the exact object is a renormalized geometric mean over exponentially many subnetworks.
      Use the **weight-scaling inference rule** — multiply each unit's outgoing weights by its inclusion
      probability, which for 0.5 reduces to halving weights after training (or doubling unit states during
      training) so that a unit's expected total input matches training time (§7.12, p. 287). Monte Carlo
      averaging needs only 10–20 masks for decent results, and up to 1000 samples were compared; the
      weight-scaling rule won that comparison, though 20-sample MC won for some models, so the best
      inference approximation is problem-dependent. Weight scaling is *exact* only for families without
      nonlinear hidden units (softmax regression, conditional-normal-output regression, deep networks with
      linear hidden units) and is merely an approximation for deep nonlinear models, with no theoretical
      accuracy analysis (§7.12, pp. 286–289).
    - *Cost*: dropout lowers effective capacity, so enlarge the model and budget more iterations; on very
      large datasets the regularization gain may not pay for the compute, and below roughly 5000 samples it
      lost to a Bayesian neural network in the cited experiment (§7.12, pp. 289–290).
    - *Generalization of the mechanism*: any μ-parameterized random modification works, not just
      include/exclude; Gaussian multiplicative noise with E[μ²] = 1 was reported to outperform binary masks;
      DropConnect and stochastic pooling are named variants. Choose modifications the network can learn to
      defend against, and prefer families that permit fast approximate inference (§7.12, pp. 290–292).
      Multiplicative hidden-unit noise beats additive fixed-scale noise on rectified networks, because
      additive noise can be defeated simply by scaling activations up (§7.12, p. 292).
    - *Interpretation test*: randomness is neither necessary nor sufficient. Fast dropout (analytic, less
      stochastic) and **Dropout Boosting** (identical noise masks, but trained to maximize training-set
      likelihood) show almost no regularization effect, which supports the bagging explanation over the
      noise-robustness explanation; bagging regularization requires members to be trained **independently**
      (§7.12, p. 290). For linear regression, dropout is equivalent to L2 with per-feature coefficients set
      by feature variance (Wager et al., 2013, as cited); the equivalence breaks for deep models (§7.12,
      p. 290).
22. **Adversarial training.** Probe for adversarial examples by optimizing the input; the demonstrated
    construction adds an imperceptibly small vector whose elements equal the **sign of the cost gradient
    with respect to the input** (illustrated with GoogLeNet on ImageNet, Fig. 7.8). A network with
    human-level accuracy on clean data can be driven to near-total error on such points, and the book's
    explanation is **excessive linearity**, not insufficient capacity: a linear function of many inputs
    changes very fast under a per-input perturbation, proportional to the weight norm. Purely linear models
    such as logistic regression cannot resist adversarial examples at all; only large function families can
    be pushed from near-linear to locally constant behaviour. Training on adversarially perturbed training
    samples reduces error on the **original i.i.d. test set** (§7.13, pp. 292–293). For unlabeled data, use
    **virtual adversarial examples**: take the model's own label at x, find x̃ where the predicted label
    changes, and train the classifier to assign x and x̃ the same label; this assumes distinct classes lie on
    separate manifolds and that small perturbations do not jump between them (§7.13, p. 294).
23. **Tangent propagation and the manifold tangent classifier.** Encode invariance knowledge as tangent
    directions ν⁽ⁱ⁾ derived from known transforms (translation, rotation, scaling) and add a penalty on the
    directional derivative of f along them, hyperparameter-scaled and summed over outputs (§7.14, p. 295).
    Choose between this analytic route and explicit augmentation knowingly: tangent propagation resists only
    **infinitesimal** perturbation while augmentation resists larger ones, and tangent propagation is hard on
    rectified-linear models — they can only shrink derivatives by turning units off or shrinking weights,
    unlike saturating sigmoid/tanh units — whereas augmentation works well with ReLU. To avoid
    hand-specifying tangents, estimate them with an autoencoder and apply the same penalty (the manifold
    tangent classifier) (§7.14, p. 296). The book's summary identities are useful for choosing: augmentation
    is non-infinitesimal tangent propagation, and adversarial training is non-infinitesimal double
    backpropagation (§7.14, p. 296).
24. **Semi-supervised and multi-task** are handled by `SOP-DL-08`; the one condition to carry here is that
    multi-task sharing produces a gain **only if** the shared-factor assumption is reasonable (§7.7,
    pp. 268–270).

## 4. Important failure modes

- **Regularizing biases**, which needs far less data to fit and can cause marked underfitting (§7.1, p. 254).
- **Expecting sparsity from L2** (§7.1.2, p. 260), or **applying the L1 diagonal-Hessian analysis to
  correlated inputs** without decorrelating first (§7.1.2, p. 259).
- **Weight decay set too high**, driving the network into a bad local minimum with pathologically small
  weights (§7.8, p. 271).
- **Penalty where a constraint was needed**: dying units and high-learning-rate positive-feedback blowup
  (§7.2, pp. 262–263).
- **Label-destroying augmentation** — the OCR flip/180° case (§7.4, p. 265).
- **Comparing algorithms under different augmentation schemes**, which attributes the transforms' gain to
  the algorithm (§7.4, p. 265).
- **Additive noise on rectified networks**, defeated by scaling activations up (§7.12, p. 292).
- **Dropout without compensating**: model not enlarged, iterations not increased, or applied where there
  are fewer than about 5000 samples (§7.12, pp. 289–290).
- **Forgetting the weight-scaling inference rule**, so inference-time inputs do not match training-time
  expectations (§7.12, p. 287).
- **Explaining dropout by noise robustness** rather than by bagging; the Dropout Boosting control shows
  noise alone does not regularize, and bagging requires independently trained members (§7.12, p. 290).
- **Reporting an ensemble as a single algorithm's benchmark result** (§7.11, p. 282).
- **Early stopping without a validation set**, or without recovering the withheld data afterwards (§7.8,
  pp. 271–274).
- **Tangent propagation with rectified units** (§7.14, p. 296).
- **Treating any of these as universally best** — the no-free-lunch argument rules it out (§5.2.2, p. 150).

## 5. Outputs and reporting

- Regularization block: mechanism, coefficient(s), where applied (weights not biases; which layers share
  α), and the validation metric used to select it.
- The task-specific reason for each mechanism, since no regularizer is universally best.
- Augmentation scheme with the label-safety screen recorded transform by transform, the
  generic-vs-domain-specific classification, and the statement that all compared algorithms used the
  identical scheme.
- Early stopping configuration: n, p, the monitored statistic, which second-round strategy was used
  (Algorithm 7.2 or 7.3), and whether ετ was traded against a weight-decay coefficient.
- Dropout configuration: inclusion probabilities per layer, model-size and iteration compensation, and the
  inference rule used (weight scaling vs Monte Carlo with a stated sample count).
- Ensemble disclosure: number of members, how they were decorrelated, and an explicit note if a benchmark
  number includes averaging.
- Adversarial training settings if used: how the perturbation was constructed and whether labeled or
  virtual adversarial examples were used.
- The quantities the book leaves open and that must therefore be declared: α per mechanism, n and p for
  early stopping, the number of ensemble members, the sparsity target, and the tangent set.

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
| Adversarial examples: sign-of-gradient perturbation, GoogLeNet/ImageNet demonstration, excessive linearity as the cause, linear models cannot resist, adversarial training improves i.i.d. test error, virtual adversarial examples and its manifold assumption | §7.13, pp. 292–294 |
| Tangent propagation, manifold tangent classifier, infinitesimal-only resistance, ReLU incompatibility, augmentation and adversarial training as non-infinitesimal forms | §7.14, pp. 294–296 |
| Multi-task gain conditional on the shared-factor assumption | §7.7, pp. 268–270 |

**Historical boundary.** Reported as book-era rather than current defaults: the typical dropout inclusion
probabilities (0.8 input / 0.5 hidden); the 5–10 network ensembling ceiling with the ILSVRC six-model
example; the Alternative Splicing dataset (fewer than 5000 samples) where a Bayesian neural network beat
dropout; the MNIST maxout learning curve of Fig. 7.3; the GoogLeNet-on-ImageNet adversarial demonstration;
label smoothing's history since the 1980s; the hardware habits around early stopping (validation evaluation
on a separate machine, best parameters stored on disk); and the two state-of-field claims that "dropout
remains the most widely used implicit ensemble method" and that early stopping is "the most commonly used
form of regularization in deep learning". The book also records the 2006–2012 belief that feedforward
networks would not perform well, and its reversal (§7, p. 252) — a reminder that the field's verdicts in
this chapter are dated. The mechanisms themselves (penalties, constraints, augmentation, early stopping,
sharing, sparsity, bagging, dropout, adversarial training, tangent methods) are stated as general and are
not era-bound.

**Formula caveat.** Display equations in this copy are images rather than text (see `SOURCE.md`), so the
exact algebraic condition for the early-stopping ↔ L2 equivalence and the exact label-smoothing target
values are not recoverable from the extracted text. Both are cited here at prose level only, which is how
the book states the relationship in words: τ acts inversely to the L2 coefficient, and 1/(ετ) plays the role
of the weight-decay coefficient, under a quadratic approximation with small ε and small eigenvalues.
