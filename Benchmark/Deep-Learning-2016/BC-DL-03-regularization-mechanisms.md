# BC-DL-03 — Do regularizers work through the mechanisms the book claims?

**Tests:** whether each regularizer produces the mechanism-specific effect the book claims, with training and
generalization error reported separately · **Executed by:**
[`SOP-DL-03`](../../SOP/Deep-Learning-2016/SOP-DL-03-select-regularization.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The book's definition is quoted for orientation: regularization is any modification to a learning algorithm
intended to reduce its **generalization** error but **not its training error** (§5.2.2, p. 150; §7, p. 253).
This benchmark does **not** turn that definition into a classifier. Whether training error happened to move in
a single run conflates regularization with capacity and optimization effects, so the two errors are reported
separately and the verdict rests on the mechanism-specific observable for each arm. Eight mechanism claims are
tested as sub-arms:

| Arm | Claim | Locator |
| --- | --- | --- |
| a | Early stopping is equivalent to L2 regularization in a stated regime: with learning rate ε and τ steps, ετ measures effective capacity and 1/(ετ) plays the role of the weight-decay coefficient; for a simple linear model with quadratic error and plain gradient descent from the origin, with ε small and all Hessian eigenvalues small, τ acts inversely to the L2 coefficient, at least under the quadratic approximation | §7.8, pp. 274–276 |
| b | With a model of sufficient representational capacity, training error falls steadily while validation error turns and rises, forming an asymmetric U — the book says this almost certainly occurs | §7.8, p. 270, Fig. 7.3 |
| c | The weight-scaling inference rule (multiply each unit's outgoing weights by its inclusion probability) approximates the intractable geometric mean over subnetworks; it is **exact** only for families without nonlinear hidden units, and Monte Carlo averaging with 10–20 masks gives decent results, with 20-sample MC winning for some models | §7.12, pp. 286–289 |
| d | Randomness is neither necessary nor sufficient: fast dropout (analytic, less stochastic) still works, and **Dropout Boosting** — identical noise masks but trained to maximize training-set likelihood — shows almost no regularization, which supports the bagging explanation over noise robustness; bagging requires members trained independently | §7.12, p. 290 |
| e | L1 drives coordinates to **exactly zero** when the coefficient is large enough and therefore performs feature selection; L2 does not produce sparsity. The L1 analysis assumes a diagonal Hessian, reasonable if inputs are decorrelated | §7.1.2, pp. 259–261 |
| f | Augmentation must preserve the label: transforms that change the class must not be used; horizontal flip and 180° rotation are the named counterexamples for OCR, confusing b with d and 6 with 9 | §7.4, p. 265 |
| g | Bagging reduces expected squared error from ν (perfectly correlated member errors) to ν/k (uncorrelated); for neural networks decorrelation already arises from random initialization, minibatch order, hyperparameter differences and nondeterminism, so members may share one dataset | §7.11, pp. 280–282 |
| h | A norm penalty can induce dying units and, at high learning rates, positive-feedback blowup; an explicit constraint implemented by reprojection avoids both | §7.2, pp. 262–263 |

## 2. Data and comparison conditions

- **Common condition for every arm**: training error and generalization error are measured **separately**, on
  a fixed split built per `SOP-DL-05`. Neither number alone decides the arm; the mechanism observable does.
  When both improve, record it and check for optimization or capacity effects before attributing the gain to
  regularization.
- **a**: two model classes — the book's stated regime (simple linear model, quadratic error, plain gradient
  descent, parameters initialized at the origin, small ε, small Hessian eigenvalues), and a deep nonlinear
  model to locate where the equivalence breaks. Sweep matched pairs of (ε, τ) against λ and compare the
  resulting weight vectors, not only the test error.
- **b**: a model with enough representational capacity to overfit, monitored over steps. The book's
  illustration is MNIST with a maxout network.
- **c**: one dropout-trained model evaluated three ways — weight scaling, Monte Carlo over 10–20 masks, Monte
  Carlo over up to 1000 masks — and run on both an exactness-family model (softmax regression,
  conditional-normal-output regression, or a deep network with linear hidden units) and a deep nonlinear
  model.
- **d**: three arms — standard dropout; fast dropout; Dropout Boosting. Dropout Boosting uses the identical
  noise masks but trains the ensemble to maximize likelihood on the training set.
- **e**: the same model under L1 and under L2, sweeping the coefficient, with inputs decorrelated (for
  example by PCA) so that the diagonal-Hessian assumption behind the L1 analysis is met; also run without
  decorrelation to observe the difference.
- **f**: an OCR-like dataset with and without horizontal flip and 180° rotation in the augmentation set, all
  other transforms held identical.
- **g**: k members with their pairwise error covariance measured; for neural networks, members trained on the
  same dataset with different random initializations and minibatch orders.
- **h**: a norm penalty arm and a projected-constraint arm at matched feasible size, run at a high learning
  rate.

## 3. Baselines

- The unregularized model (coefficient 0, no dropout, no early stopping, no augmentation) is the reference
  for the gap in every arm.
- Arm a's reference is the matched weight-decay run; arm c's reference is Monte Carlo averaging; arm d's
  reference is standard dropout; arm h's reference is the penalty at the same feasible size.
- For arm f, the reference is the identical pipeline with only label-preserving transforms.

## 4. Metrics

1. Training error and generalization error, reported separately, plus the gap (§5.2, p. 142).
2. Validation error versus training step, for the U-shape (arm b).
3. Final weight vector norm and direction, for the early-stopping ↔ L2 correspondence (arm a).
4. Fraction of weights exactly equal to zero (arm e).
5. Classification accuracy under each inference rule (arms c, d).
6. Test error with and without the contested transform (arm f).
7. Ensemble expected squared error against ν and ν/k, with the measured member-error covariance (arm g).
8. Count of near-dead units and incidence of overflow or NaN at high learning rate (arm h).
9. Cost profile: dropout requires a larger model and more iterations, and the book notes that on very large
   datasets the gain may not pay for the compute, while below roughly 5000 samples it lost to a Bayesian
   neural network (§7.12, pp. 289–290). Report dataset size alongside any dropout result.

## 5. How to interpret failure

- **Both errors improving together** is not a failed arm and not proof of regularization. Note it, then check
  the two confounders the book separates out: a capacity change (route to `SOP-DL-02`) and an optimization
  change — a modified objective or step rule can simply reach a better minimum (route to `SOP-DL-04`). Only
  after both are ruled out does the generalization gain belong to the regularizer, and even then the arm is
  decided by its own mechanism observable, not by the direction of the training-error movement.
- **Arm a diverging on the deep model** is expected, not a refutation: the equivalence is established only for
  the stated linear/quadratic/origin/small-ε/small-eigenvalue regime. Report where it broke.
- **Arm b showing no U** means the model is not large enough to overfit; increase capacity before concluding
  that early stopping is unnecessary.
- **Arm c: MC beating weight scaling** matches the book's own report that 20-sample MC won for some models —
  the best inference approximation is problem-dependent, and weight scaling is exact only for the named
  families, with no theoretical accuracy analysis for deep nonlinear models.
- **Arm d: Dropout Boosting regularizing** would contradict the bagging explanation; the book reports almost no
  regularization effect for it. If fast dropout matches standard dropout, that is consistent with randomness
  not being necessary.
- **Arm e: L2 producing exact zeros or L1 producing none** ⇒ check the coefficient (L1 needs it large enough)
  and check whether inputs were decorrelated.
- **Arm f: test error rising with a new transform** ⇒ the transform destroyed labels; remove it.
- **Arm g: ensemble error ≈ best member** ⇒ member errors are highly correlated (covariance near ν), so the
  averaging buys nothing; investigate whether the members were really trained independently.
- **Arm h: dying units or blowup under the penalty** ⇒ switch to reprojection, per the book's preference for
  explicit constraints at high learning rates.
- **Reporting an ensemble as a single algorithm's benchmark result** is disallowed: model averaging is
  discouraged when benchmarking algorithms for a scientific paper, because any algorithm benefits at the cost
  of compute and storage (§7.11, p. 282).

## 6. Validity limits and source traceability

- The exact algebraic condition for arm a is a display equation, which is an image in this copy and therefore
  not recoverable from the text layer (see `SOURCE.md`). The claim is cited at prose level only.
- Arm g's error decomposition assumes multivariate normal member errors with common variance and covariance;
  the ν/k endpoint requires zero covariance, which is an idealization.
- Arm c's exactness list is limited to families **without nonlinear hidden units**; for deep nonlinear models
  weight scaling is an approximation with no theoretical accuracy analysis.
- Arm e's L1 analysis requires a diagonal Hessian.
- Arm f and the wider question of whether an experiment is properly controlled both require subjective
  judgement, which the book states explicitly (§7.4, p. 265).
- The book gives **no** defaults for the early-stopping evaluation interval n or patience p, no numeric
  penalty coefficients, no ensemble size beyond the practical ceiling of 5–10 networks, and no sparsity
  target. Any value used here is the evaluator's choice and must be reported.
- Bias is penalized separately from weight: biases need far less data to fit and regularizing them can cause
  marked underfitting (§7.1, p. 254), so no arm should regularize biases without stating why.

| Claim | Locator |
| --- | --- |
| Definition of regularization | §5.2.2, p. 150; §7, p. 253 |
| Learning-curve U-shape; Algorithm 7.1 with interval n and patience p | §7.8, pp. 270–273 |
| ετ as effective capacity; 1/(ετ) as the weight-decay analogue; quadratic-approximation equivalence; automatic determination of the regularization amount | §7.8, pp. 274–277 |
| Dropout masks and inclusion probabilities; weight-scaling inference rule; exactness families; MC sample counts | §7.12, pp. 283–289 |
| Capacity compensation and dataset-size limits | §7.12, pp. 289–290 |
| Fast dropout and Dropout Boosting; bagging requires independent members; linear-regression L2 equivalence | §7.12, p. 290 |
| L2 mechanics and absence of sparsity; L1 exact zeros, feature selection, diagonal-Hessian assumption; prior readings | §7.1.1–§7.1.2, pp. 255–261 |
| Augmentation label safety and the OCR counterexample; benchmark control | §7.4, pp. 264–265 |
| Bagging bootstrap construction, error decomposition, decorrelation in neural nets, benchmark reporting rule, Boosting is not regularizing | §7.11, pp. 280–283 |
| Penalty versus reprojection; dying units; high-learning-rate blowup; per-column norms | §7.2, pp. 261–263 |
| Penalize weights not biases | §7.1, p. 254 |

**Historical boundary.** Book-era and reported as such: the typical dropout inclusion probabilities (0.8 for
input units, 0.5 for hidden units); the 5–10 network ensembling ceiling; the MNIST maxout learning curve of
Fig. 7.3; the Alternative Splicing dataset with fewer than 5000 samples where a Bayesian neural network beat
dropout; fast dropout having produced no significant improvement on large problems at the time of writing;
label smoothing in use since the 1980s; and the two state-of-field claims that dropout remains the most widely
used implicit ensemble method and that early stopping is the most commonly used form of regularization in deep
learning. The mechanisms under test are stated as general.
