# SOP-DL-04 — Diagnose and repair optimization failure

**Stage:** optimize · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Separate **optimization failure** from statistical failure, identify which of the book's named pathologies
is present from observable symptoms, and apply the repair the book attaches to it.

The framing that makes this a distinct procedure: learning is not pure optimization. We care about a
test-set performance measure P that may itself be intractable, and we improve it indirectly by lowering a
training objective J(θ) (§8.1, p. 298). Termination therefore differs from optimization: a pure optimizer
stops when the gradient is small, whereas a training algorithm stops on an early-stopping criterion
computed from the *true* loss, at a point where the surrogate's gradient is still large (§8.1.2,
pp. 299–300). A run that has not reached a critical point has not necessarily failed.

Out of scope: deciding whether the training error is even the problem (`SOP-DL-02`), regularization
(`SOP-DL-03`), verifying that gradients are computed correctly at all (`SOP-DL-06`, which must run first),
and structural choices that change the optimization problem (`SOP-DL-07`).

## 2. Inputs and assumptions

- The regime read from `SOP-DL-02`: training error above target is the trigger for this SOP.
- Gradient instrumentation: per-step gradient norm, activation and gradient histograms, and the
  update-to-parameter magnitude ratio (`SOP-DL-06` step 6).
- A verified gradient implementation. Nothing here is interpretable until the numerical-derivative check
  passes (§11.5, p. 452).
- The objective's form: is it a surrogate for a non-differentiable target? Is it intractable, so that only
  an estimate of the gradient exists? Is it bounded below at all? (§8.1.1–§8.1.2; §6.2.1.1, p. 204)
- The batch regime and the hardware memory limit (§8.1.3, p. 301).

## 3. Procedure

### 3.1 Set the objective correctly before blaming the optimizer (§8.1)

1. Treat training-loss minimization as instrumental, not terminal: the target is the test-set measure P
   (§8.1, p. 298).
2. Do not use pure empirical risk minimization. It easily leads to overfitting, and it is often infeasible
   because the losses we would like to use — 0-1 loss is the book's example — have no usable derivative.
   Deep learning therefore rarely uses pure ERM (§8.1.1, pp. 298–299).
3. Use a surrogate and stop on the true loss. A surrogate such as negative log-likelihood for 0-1 loss
   keeps extracting information after the training 0-1 loss has reached zero, by widening margins. Stop on
   an early-stopping criterion computed from the true loss, before overfitting; expect the surrogate's
   gradient to still be large at termination (§8.1.2, pp. 299–300).
4. Choose the batch regime deliberately (§8.1.3, pp. 300–304):
   - Gradient-estimation error falls as 1/√n, so returns to larger batches are **sublinear** — a hundred
     times the compute buys ten times less noise.
   - Batch-size factors the book lists: sublinear accuracy returns; very small batches waste multi-core
     hardware, with an absolute minimum below which time stops dropping; **memory consumption scales with
     batch size** when samples are processed in parallel, which is often the binding hardware limit; and
     powers of two run faster on GPUs.
   - Generalization warning: minibatch noise acts as a regularizer, and generalization error is usually
     best at batch size 1 — but the high gradient variance forces a small learning rate and many more
     steps, so total runtime blows up.
   - Second-order updates need much larger batches (around 10,000) than first-order ones (around 100),
     because an ill-conditioned Hessian amplifies gradient-estimation noise.
   - Minibatches must be drawn i.i.d.: shuffle naturally ordered data. One upfront shuffle reused across
     epochs is acceptable, but not shuffling greatly degrades performance. Only the first pass over a fixed
     training set gives an unbiased estimate of the generalization gradient.

### 3.2 Diagnose from symptoms (§8.2)

5. **Ill-conditioning** (§8.2.1, pp. 304–305). Symptom: SGD "sticks" — even very small steps *increase* the
   cost, because the curvature term gᵀHg in the second-order Taylor expansion exceeds the linear term.
   Diagnose by monitoring the squared gradient norm and gᵀHg: in many runs ‖g‖ does not shrink much while
   gᵀHg grows by more than an order of magnitude, and learning slows because the learning rate must shrink
   to compensate for the stronger curvature. Do **not** read a rising gradient norm as failure by itself —
   the book's Fig. 8.1 shows the gradient norm rising through a successful object-detection run. Newton-style
   fixes that work for convex ill-conditioning need major modification for networks; momentum is presented
   as aimed at exactly this problem (§8.3.2, Fig. 8.5, p. 318).
6. **Local minima** (§8.2.2, pp. 306–307). Model identifiability and weight-space symmetry — n!^m
   permutations, and rescaling by α with 1/α for ReLU and maxout units — create countless equal-cost minima;
   these are not the problem. Dangerous minima would be *high-cost* ones: they can be constructed for small
   networks, whether they are common for real networks is an open question, and the conjecture at the time of
   writing is that for large enough networks most local minima have low cost. **Rule minima out empirically:
   plot the gradient norm over time. If it never shrinks to a tiny value, the failure is not a local minimum
   or any other critical point.** Limit: in high dimensions it is hard to prove that minima *are* the cause,
   because many non-minimum structures also have small gradients.
7. **Plateaus, saddles and flat regions** (§8.2.3, pp. 307–310). In high dimensions saddles vastly outnumber
   minima — for random functions the ratio grows exponentially in the dimension. Low-cost critical points are
   more likely to be minima, high-cost ones saddles, and very high-cost ones maxima. Gradients near a saddle
   are small; empirically SGD trajectories escape prominent saddles quickly. **Unmodified Newton is attracted
   to saddles**, which the book offers as the explanation for second-order methods' failure on neural
   networks; saddle-free Newton helps but does not scale. Constant-value plateaus, where gradient and Hessian
   are both zero, are a major problem for every numerical optimizer.
8. **Cliffs and gradient explosion** (§8.2.4, p. 310). Steep cliff regions arise from products of several
   large weights. A gradient step can catapult parameters far away and destroy accumulated progress, whether
   the cliff is approached from above or below. Remedy: heuristic gradient clipping (§10.11.1, step 32). The
   reasoning is that the gradient gives the best direction only within an infinitesimal region, so clipping
   intervenes to shrink the step when the proposed update is large. Cliffs are common in recurrent costs,
   where a factor per time step is multiplied over long sequences.
9. **Long-term dependencies** (§8.2.5, pp. 310–311). Repeated multiplication by a shared W gives Wᵗ;
   eigenvalues of magnitude greater than 1 explode, less than 1 vanish. Vanishing means no usable direction
   signal; explosion means unstable learning. In the power-method view, components orthogonal to the dominant
   eigenvector are discarded. Feedforward networks largely avoid this because each layer uses a *different*
   matrix. For the recurrent case the book adds a structural result that limits what any repair can achieve:
   the gradient magnitude of long-range interactions becomes exponentially small relative to short-range ones,
   and for an RNN to store memory robustly and resist small perturbations it **must** live in the
   vanishing-gradient region of parameter space (§10.7, pp. 419–421). Bengio et al. (1994b), as cited, found
   the probability of SGD successfully training a vanilla RNN rapidly goes to zero once the required
   dependency span reaches lengths of only 10 or 20 (§10.7, p. 421).
10. **Inexact gradients** (§8.2.6, pp. 311–312). The gradient or Hessian may be available only as a noisy or
    biased estimate — from minibatches, or from intractable objectives such as the Boltzmann-machine
    log-likelihood, handled by contrastive divergence. Remedy: choose surrogate losses that are easier to
    estimate; note that algorithms are designed to tolerate gradient defects.
11. **Weak correspondence between local and global structure** (§8.2.7, pp. 312–314). Each local step
    improves, yet the descent direction does not point toward distant low-cost regions. Most training time is
    trajectory length — long arcs around hills — and networks typically never reach any critical point. Some
    losses have no minimum at all: NLL asymptotes, and an exponential-type model drives its parameter toward
    infinity. Failure can occur with no saddle and no minimum present, simply because initialization landed on
    the wrong side of a hill (Fig. 8.4). **The book's prescribed response is to seek better initial points,
    in regions where local descent connects quickly to solutions, rather than to invent nonlocal update
    rules** (§8.2.7, p. 314).
12. **Theoretical limits are not an explanation** (§8.2.8, p. 314). Results showing that any optimization
    algorithm for neural networks has performance limits exist (Blum and Rivest; Judd; Wolpert and MacReady,
    as cited), but the book states these usually do not affect practice, and that it is hard to tell whether a
    given problem lies in the hard class. Do not invoke them.

### 3.3 Configure the first-order optimizer (§8.3, §8.5)

13. **SGD and its schedule** (§8.3.1, pp. 314–317). The learning rate must decay, because minibatch sampling
    noise does not vanish at the minimum — batch gradient descent, by contrast, can use a fixed rate.
    Sufficient convergence conditions: Σ εₖ = ∞ and Σ εₖ² < ∞. The practical schedule is a linear decay of εₖ
    to ε_τ over τ iterations, constant afterwards. Tuning is described as more art than science: monitor the
    objective-versus-time learning curve; take τ to be roughly the number of iterations needed for a few
    hundred passes through the training set; take ε_τ to be about 1% of ε₀; and choose ε₀ by inspecting the
    earliest iterations — pick a rate *higher* than the one that looks best after about 100 iterations, but
    not so high that it causes severe oscillation. Violent oscillation or a rising cost means too high; too
    low means slow training or a permanent stall at high cost; mild oscillation is acceptable, especially with
    dropout. Per-step time is independent of dataset size, and on very large datasets SGD may converge within
    tolerance before completing one pass. Excess-error rates are O(1/√k) in the convex case and O(1/k) in the
    strongly convex case; since the Cramér–Rao bound implies generalization error cannot fall faster than
    O(1/√m), hunting for a faster-converging optimizer may correspond to overfitting. Growing the minibatch
    during training trades the batch and stochastic advantages.
14. **Momentum** (§8.3.2, pp. 317–321). The velocity is an exponentially decaying average of past gradients;
    momentum targets ill-conditioning and gradient variance. Read α through 1/(1 − α): the effective maximum
    step is 1/(1 − α) times plain gradient descent, so α = 0.9 gives a terminal speed ten times plain GD.
    Common values are 0.5, 0.9 and 0.99. α may be ramped up over time, but tuning α over time matters less
    than shrinking 1/(1 − α).
15. **Nesterov momentum** (§8.3.3, pp. 321–322) is identical except that the gradient is evaluated *after*
    applying the current velocity. In the convex batch case it improves O(1/k) to O(1/k²); in the stochastic
    case there is **no** convergence-rate improvement. Do not justify it by the convex rate.
16. **Adaptive learning rates** (§8.5, pp. 327–332). Motivation: the learning rate is among the hardest
    hyperparameters, the loss is highly sensitive in some parameter directions and not others, and
    per-parameter adaptation makes sense if that sensitivity is roughly axis-aligned. AdaGrad scales each
    parameter's rate inversely to the square root of the *cumulative* sum of squared gradients — good convex
    theory, but on deep networks the accumulation causes premature or excessive decay of the effective rate,
    and it works on some deep models and not others. RMSProp replaces the accumulation with an exponentially
    weighted moving average, discarding distant history, which behaves like AdaGrad re-initialized inside the
    local convex bowl; the book calls it effective and practical and one of the methods practitioners commonly
    use. Adam adds momentum applied to the exponentially weighted first-moment estimate of the raw gradient,
    plus bias correction of both moments — RMSProp lacks the correction, so its second-moment estimate is
    heavily biased early — and is considered robust to hyperparameter choice, though the learning rate
    sometimes needs changing from the recommended default of 0.001.
17. **Choosing among them: there is no consensus** (§8.5.4, p. 332). A broad comparison (Schaul et al., 2014,
    as cited) found the adaptive-rate family quite robust but produced no standout winner. The popular set is
    SGD, SGD with momentum, RMSProp, RMSProp with momentum, AdaDelta and Adam, and the book states the choice
    depends mainly on the practitioner's familiarity for hyperparameter tuning. Record the choice as a
    familiarity decision, not a derived one.
18. **Second-order methods** (§8.6, pp. 332–339). Newton is valid only where the Hessian is positive
    definite; near a saddle it moves in the wrong direction; it can be patched by adding α to the Hessian
    diagonal, but if α must be large enough to offset negative curvature the method degenerates into
    gradient/α with steps smaller than well-tuned gradient descent. Its fatal cost is a k × k inverse per
    iteration, O(k³) with k possibly in the millions, so only tiny networks are feasible — the verdict is that
    it is not worth it at scale. Conjugate gradient avoids the inverse using conjugate directions, needs at
    most k line searches in k dimensions for quadratics, and nonlinear CG needs occasional restarts;
    practitioners report it reasonable for training networks and *better if preceded by a few SGD steps*, and
    minibatch versions have succeeded. BFGS keeps a low-rank approximation of H⁻¹ and depends less on a
    precise line search, but costs O(n²) memory and is unsuitable for million-parameter models; L-BFGS reduces
    storage to O(n) per step.

### 3.4 Initialize deliberately (§8.4, pp. 322–327)

19. Accept the stakes: the initial point can determine whether the algorithm converges at all, how fast, to
    what cost, and it can affect generalization; some initial points cause outright numerical failure. The
    book states that understanding here is primitive and that the strategies are simple heuristics.
20. The one firm requirement is to **break symmetry between units**: identical units receiving identical
    inputs would update identically. Random initialization from a high-entropy distribution is the cheap way;
    Gram–Schmidt orthogonalization is the expensive deterministic alternative. Biases and extra parameters
    (a conditional variance, for instance) are usually set to heuristically chosen constants — only weights
    are randomized.
21. Gaussian versus uniform "does not seem to make much difference" and has not been exhaustively studied;
    the **size** of the initial distribution, not its shape, has a large effect on optimization and
    generalization.
22. Know the scale trade-off. Large weights break symmetry better and prevent signal loss in forward and
    backward linear propagation; too large causes exploding values, chaos in recurrent networks (mitigable by
    gradient clipping), and saturating activations with zero gradients. Optimization wants weights large
    enough to propagate signal while regularization wants them small. Initializing at θ₀ acts like a Gaussian
    prior centered at θ₀ — early-stopped gradient descent is approximately weight decay toward the
    initialization (cf. §7.8).
23. Named schemes and their status: **normalized initialization** (Glorot and Bengio, 2010, as cited) samples
    from a range that compromises between equal activation variance and equal gradient variance per layer,
    derived under an assumption of a chain of linear matrix multiplications — real networks violate the
    assumption, but strategies derived for linear models often still work. **Orthogonal initialization with a
    per-nonlinearity gain g** (Saxe et al., 2013, as cited) makes iterations-to-convergence independent of
    depth *under the linear-chain model*; increasing g pushes the network into the regime where forward
    activation norms and backward gradient norms grow. Setting the gain correctly alone has been reported to
    suffice for training 1000-layer networks without orthogonal initialization (Sussillo, 2014, as cited),
    because activations and gradients then follow a norm-preserving random walk across layers, avoiding the
    shared-matrix vanishing and explosion of §8.2.5. **Sparse initialization** (Martens, 2010, as cited) gives
    each unit exactly k nonzero weights, keeping total input magnitude independent of m; its drawbacks are a
    strong prior on the large weights it keeps, slowness to shrink the wrong ones, and problems with maxout
    filters.
24. **Run the empirical initialization check** — the book's explicit protocol, and the cheapest diagnostic in
    this SOP. Treat each layer's weight range as a hyperparameter (searched randomly per §11.4 or by hand).
    Then observe activation magnitude and standard deviation on a **single minibatch** propagating forward;
    repeatedly find the first layer whose activations shrink unacceptably and raise that layer's weights,
    until initial activations are all reasonable. If learning is still slow, do the same with gradient
    magnitude and standard deviation. This uses one batch of feedback and is cheaper than validation-set
    hyperparameter search (formalized by Mishkin and Matas, 2015, as cited). Know why theory-based criteria
    fail in practice — the criterion may be the wrong one, the property may not be preserved once learning
    starts, or faster optimization may come at the cost of generalization — so the empirical optimum is
    roughly near, but not exactly equal to, the theoretical prediction.
25. **Biases**: zero is usually fine. Exceptions the book names: output-unit biases set to match output
    marginal statistics (solve softmax(b) = c for class marginals; likewise autoencoders and Boltzmann
    machines reproducing input marginals); avoiding initial saturation (a ReLU hidden bias of 0.1 instead of 0,
    which conflicts with walk-initialization schemes); and gating units, where the bias is set so the gate
    opens at initialization — the cited example is an LSTM forget-gate bias of 1. Variance or precision
    parameters can safely be initialized to 1, or set to the marginal variance of the training outputs.
    Learned initialization, unsupervised or cross-task supervised, can beat random initialization in
    convergence speed and sometimes in generalization.

### 3.5 Apply the meta-strategies (§8.7)

26. **Batch normalization** (§8.7.1, pp. 339–343). The diagnosis it addresses: in a deep composition, each
    layer's gradient assumes the other layers are fixed while all layers update simultaneously, and
    higher-order cross-layer interactions can be exponentially large, which makes any single learning rate
    wrong and n-th-order methods hopeless. The book describes BN as "not really an optimization algorithm but
    an adaptive reparameterization". Mechanism: replace a layer's minibatch activation matrix H by
    H′ = (H − µ)/σ computed per unit over the minibatch, and — the key innovation — **backpropagate through
    the normalization**, so gradient components that would merely shift a unit's mean or standard deviation
    are cancelled. Prior approaches either penalized the deviation or re-normalized after each step, and
    either under-normalize or waste time fighting the learner. For inference, replace µ and σ with running
    averages collected during training, which enables single-sample evaluation. Normalization alone reduces
    representational power, so use γH′ + β — the same function family with better learning dynamics, and β
    directly controls the mean. Placement: normalize XW after the linear transform, dropping the bias as
    redundant with β; for convolutional networks, normalize each feature map across spatial positions jointly.
    In a toy linear chain BN makes lower layers harmless but also *useless* — nonlinearity is what keeps them
    useful. Full decorrelation of units would be better but is too expensive, so BN remains the most practical
    option so far. Note on scope: a *regularization* side effect is not stated in §8.7.1 of this translation;
    the practitioner-level remark that batch normalization sometimes lowers generalization error, allowing
    dropout to be omitted, is in §11.2, p. 440.
27. **Coordinate descent** (§8.7.2, pp. 343–344): use when variables split into nearly independent blocks or
    one block is much cheaper to optimize — sparse coding is the example, jointly non-convex but convex in
    each block, so alternate. Do not use when one variable's value strongly determines another's optimum.
28. **Polyak averaging** (§8.7.3, p. 344): average the visited trajectory points. Strong guarantees exist for
    convex gradient descent; for networks it is heuristic but works well, on the rationale that crossings back
    and forth across a valley average out near the bottom. For non-convex problems use exponentially decayed
    averaging.
29. **Supervised pretraining** (§8.7.4, pp. 344–347): when direct training is too hard, train simpler or
    shallower models first, then complicate. Greedy supervised pretraining trains layer subsets stage-wise,
    each new hidden layer as a shallow MLP on the previous layer's output, optionally followed by joint
    fine-tuning; greedy initialization greatly accelerates joint optimization and improves solution quality.
    Variants the book names: growing an 11-layer network to 19 layers with random middle layers then training
    jointly; using previous outputs together with the original inputs; transferring the first k layers from a
    network pretrained on other subsets; and hint-based training, where a wide-shallow teacher trains a
    narrow-deep student that must also regress the teacher's intermediate layers — without those hints the
    student performs badly on both training and test data. It helps by guiding intermediate-layer learning,
    benefiting optimization and generalization alike.
30. **Design models that are easier to optimize** (§8.7.5, pp. 347–348) — the book's strongest meta-rule: most
    of the gains over thirty years came from changing model families, not optimizers, and 1980s momentum SGD
    is still a frontier algorithm in modern neural-network applications. Concretely: choose
    almost-everywhere-differentiable activations with nonzero gradient over most of the domain, avoiding
    jagged non-monotonic ones; prefer more-linear units (LSTM, ReLU, maxout over stacks of sigmoids), because
    linear paths give well-scaled Jacobian singular values, so gradients flow through many layers and give a
    clear direction even when the outputs are far from correct; use skip and linear connections to shorten the
    input-to-output path and mitigate vanishing; and use auxiliary heads on intermediate layers, which inject
    large gradients into low layers and are discarded after training — an alternative to pretraining that
    permits single-stage joint training.
31. **Continuation and curriculum** (§8.7.6, pp. 348–350): for global-structure problems, build a sequence of
    objectives of increasing difficulty sharing the same parameters, solve the easiest first, and let each
    solution initialize the next. The classic form blurs or smooths the objective, and some non-convex
    functions become approximately convex when blurred; the idea is related to simulated annealing. Three
    stated failure modes: too many intermediate objectives make the total cost high; an NP-hard problem stays
    NP-hard; and blurring may never convexify, or the blurred minimum may track a local rather than a global
    minimum. Even though local minima are no longer considered the main problem, continuation still helps by
    eliminating flat regions and reducing gradient-estimate variance. Curriculum learning (Bengio et al.,
    2009, as cited) is interpreted as continuation: increase the influence of simple samples by weighting them
    more heavily in the cost or sampling them more often, which makes earlier objectives easier;
    experimentally it produced better results on a large-scale neural language modelling task.

### 3.6 Recurrent-specific repairs (§10.11, §10.2.1)

32. **If gradients explode, clip** (§10.11.1, pp. 430–431). Two forms: clip the minibatch gradient
    **elementwise** before the update, or clip its **norm** — if ‖g‖ > v, rescale g by v/‖g‖. Clip at every
    step whose gradient exceeds the threshold v. Norm clipping preserves the exact gradient direction with a
    bounded update norm; elementwise clipping no longer aligns with the true gradient but remains a descent
    direction; experiments show both behave similarly. If the gradient is numerically Inf or NaN, taking a
    random step of size v usually escapes the unstable state. Know the bias: the mean of norm-clipped
    minibatch gradients is a **biased** estimator of the true gradient — the book calls it an empirically
    useful heuristic bias — because the contributions of large-gradient examples vanish. **No numeric value of
    v is stated**; it must be chosen and reported.
33. **If gradients vanish, clipping does not help** (§10.11.2, p. 432). Use gating and self-loops, or an
    information-flow regularizer (computed by treating the forward vector as constant) **combined with**
    clipping — clipping is essential in that combination because it preserves the RNN dynamics at the edge of
    exploding gradients. Expect the combination to underperform LSTM on redundant data such as language
    modelling. Remember the structural limit from step 9: robust memory storage requires living in the
    vanishing-gradient region (§10.7, p. 420).
34. **If the model is deployed open-loop after teacher forcing** (§10.2.1, pp. 401–402): train with a mixture
    of free-running inputs, or use scheduled sampling as a curriculum.

### 3.7 Numerical hygiene (§4.1–§4.4)

35. Underflow rounds a number to zero and then poisons later steps — division by zero, or log 0 giving −∞ or
    NaN; overflow gives ∞ and then NaN (§4.1, pp. 112–114). The mandatory softmax fix: compute softmax(z) with
    z = x − maxᵢ xᵢ, so the largest argument is 0, ruling out overflow, and the denominator contains a term
    equal to 1, ruling out division by zero. Numerator underflow can still make log softmax equal −∞, so
    implement a dedicated numerically stable log-softmax rather than composing log with softmax. Frameworks may
    detect and stabilize such expressions automatically.
36. Condition number is |λ_max| / |λ_min|; a large value means matrix inversion amplifies *pre-existing* input
    error — a property of the matrix, not of the algorithm (§4.2, p. 114).
37. At a critical point the gradient gives no direction; the types are local minimum, local maximum and
    saddle. When a function has many poor global minima or flat regions, we accept points that are very small
    but not minimal — zero gradients and plateaus jointly defeat purely local methods. Learning-rate options at
    this level: a small constant; the step that makes the directional derivative vanish; or a line search over
    candidates (§4.3, pp. 114–118).
38. The Hessian is the Jacobian of the gradient and is symmetric almost everywhere; the second-derivative test
    generalizes through eigenvalues — positive definite gives a local minimum, mixed signs a saddle, and a zero
    eigenvalue leaves the case indeterminate. The Hessian condition number measures curvature variation;
    ill-conditioning makes gradient descent zigzag and forces a step size small enough for the stiff direction,
    which is then too small to make progress in the flat direction. Newton is useful near minima and harmful
    near saddles unless the Hessian is positive definite. Lipschitz continuity gives only weak guarantees, and
    convex optimization's guarantees barely transfer to deep learning (§4.3.1, pp. 119–125).
39. For constrained problems: project the gradient-descent step or line search back onto the feasible set, or
    project the gradient onto the tangent space first; or reparameterize (a unit-norm x as [cos θ, sin θ]). The
    general machinery is the generalized Lagrangian with KKT multipliers and active or inactive inequality
    constraints; the KKT conditions are **necessary but not sufficient** for optimality (§4.4, pp. 125–128).

## 4. Important failure modes

- **Reading a rising gradient norm as failure.** The book's successful run shows exactly that (§8.2.1, p. 305,
  Fig. 8.1).
- **Attributing a stall to a local minimum without the gradient trace.** If ‖g‖ never becomes tiny, no
  critical point is involved (§8.2.2, p. 307).
- **Using unmodified Newton on a network**: it is attracted to saddles (§8.2.3, pp. 307–310).
- **Treating a non-converged run as a failed run.** Training algorithms are expected to terminate with the
  surrogate gradient still large (§8.1.2, p. 300), and networks typically never reach a critical point
  (§8.2.7, p. 312).
- **Expecting the minimum to exist.** Some losses have no minimum (§8.2.7, p. 313; §6.2.1.1, p. 204).
- **Chasing a faster-converging optimizer** past the O(1/√m) generalization floor, which may correspond to
  overfitting (§8.3.1, p. 317).
- **Justifying Nesterov momentum by its convex rate**, which does not carry to the stochastic setting
  (§8.3.3, p. 322).
- **Presenting an optimizer choice as derived.** There is no consensus; the book says the choice depends
  mainly on practitioner familiarity (§8.5.4, p. 332).
- **Second-order methods at scale**: O(k³) for Newton, O(n²) memory for BFGS (§8.6, pp. 335, 338).
- **Clipping to fix vanishing gradients** — it does not help (§10.11.2, p. 432).
- **Ignoring clipping's bias** when the estimator's unbiasedness matters (§10.11.1, p. 431).
- **Not shuffling naturally ordered data**, which greatly degrades performance (§8.1.3, p. 302).
- **Composing log with softmax** instead of implementing a stable log-softmax (§4.1, p. 114).
- **Blaming initialization shape rather than scale**, or trusting a theoretical initialization criterion
  without the single-minibatch activation and gradient check (§8.4, pp. 323, 325).
- **Invoking theoretical impossibility results** as an explanation for a practical failure (§8.2.8, p. 314).

## 5. Outputs and reporting

- The symptom → diagnosis → remedy chain, with the trace that supported each diagnosis: squared gradient norm
  and gᵀHg over time for ill-conditioning; gradient norm over time to exclude critical points; activation and
  gradient histograms; the update-to-parameter ratio.
- Optimizer configuration: algorithm, learning-rate schedule with ε₀, ε_τ and τ, momentum coefficient and the
  implied 1/(1 − α), and the adaptive-method constants if used — each recorded as a book-era default or as a
  searched value.
- Batch regime: size, shuffling policy, memory headroom, and whether the generalization-versus-runtime
  trade-off was probed.
- Initialization record: scheme, per-layer weight ranges, the single-minibatch activation and gradient check
  result, and every bias exception applied.
- Meta-strategies applied and why: batch normalization placement and inference statistics, averaging,
  pretraining or hints, continuation or curriculum, and any structural change made to ease optimization.
- Clipping record if used: form (norm or elementwise), threshold v, how often it triggered, and the bias
  caveat.
- An explicit statement of what the book does not fix and that was therefore chosen: v, τ and ε_τ in any
  setting other than the book's rule of thumb, the number of continuation stages, and the optimizer family.

## 6. Source traceability

| Claim or step | Locator |
| --- | --- |
| Learning vs pure optimization; the intractable test measure P | §8.1, p. 298 |
| ERM leads to overfitting and is often infeasible; surrogate losses; termination with a large surrogate gradient | §8.1.1–§8.1.2, pp. 298–300 |
| Batch vs minibatch: 1/√n error decay, memory scaling, powers of two, batch-1 generalization, second-order batch sizes, i.i.d. shuffling, unbiasedness of the first pass | §8.1.3, pp. 300–304 |
| Ill-conditioning: sticking, gᵀHg vs ‖g‖², rising gradient norm in a successful run | §8.2.1, pp. 304–305, Fig. 8.1 |
| Local minima: symmetry and identifiability, high-cost minima open question, gradient-norm test | §8.2.2, pp. 306–307 |
| Saddles dominate in high dimensions; SGD escapes; Newton is attracted; constant plateaus | §8.2.3, pp. 307–310, Fig. 8.2 |
| Cliffs and explosion; clipping as the remedy; cliffs common in recurrent costs | §8.2.4, p. 310 |
| Long-term dependencies; Wᵗ; power-method view; feedforward nets use different matrices | §8.2.5, pp. 310–311 |
| Recurrent long-range gradients exponentially small; robust memory requires the vanishing region; span-10/20 result | §10.7, pp. 419–421 |
| Inexact gradients; surrogate choice | §8.2.6, pp. 311–312 |
| Weak local–global correspondence; trajectory length; no minimum; wrong side of the hill; better initial points prescribed | §8.2.7, pp. 312–314, Fig. 8.4 |
| Theoretical limits and their practical irrelevance | §8.2.8, p. 314 |
| SGD schedule, decay conditions, τ and ε_τ rules, oscillation diagnosis, excess-error rates, Cramér–Rao floor, growing minibatches | §8.3.1, pp. 314–317 |
| Momentum, 1/(1 − α) reading, common α values, ramping | §8.3.2, pp. 317–321, Fig. 8.5 |
| Nesterov momentum and its convex-only rate gain | §8.3.3, pp. 321–322 |
| AdaGrad accumulation problem; RMSProp moving average and verdict; Adam moments and bias correction | §8.5.1–§8.5.3, pp. 327–332 |
| No consensus; popular set; choice by familiarity | §8.5.4, p. 332 |
| Newton, conjugate gradient, BFGS and L-BFGS verdicts | §8.6, pp. 332–339 |
| Batch normalization: diagnosis, reparameterization framing, mechanism, backprop through normalization, inference statistics, γ and β, placement, linear-chain caveat, most practical so far | §8.7.1, pp. 339–343 |
| Batch normalization sometimes lowers generalization error, allowing dropout to be omitted | §11.2, p. 440 |
| Coordinate descent; Polyak averaging | §8.7.2–§8.7.3, pp. 343–344 |
| Supervised pretraining and its variants; hints from a teacher | §8.7.4, pp. 344–347 |
| Designing for optimization: model families over optimizers, activation differentiability, more-linear units, skip connections, auxiliary heads | §8.7.5, pp. 347–348 |
| Continuation and curriculum, with three failure modes | §8.7.6, pp. 348–350 |
| Gradient clipping: forms, threshold rule, Inf/NaN escape, bias caveat | §10.11.1, pp. 430–431 |
| Vanishing gradients: clipping does not help; information-flow regularizer with clipping; weaker than LSTM on redundant data | §10.11.2, p. 432 |
| Teacher forcing and open-loop deployment | §10.2.1, pp. 401–402 |
| Underflow/overflow, stable softmax, stable log-softmax | §4.1, pp. 112–114 |
| Condition number | §4.2, p. 114 |
| Critical points, plateaus, learning-rate options | §4.3, pp. 114–118 |
| Jacobian/Hessian, second-derivative test, ill-conditioning zigzag, Newton near saddles, weak transfer of convex guarantees | §4.3.1, pp. 119–125 |
| Constrained optimization, projection, reparameterization, KKT necessary but not sufficient | §4.4, pp. 125–128 |
| Initialization: symmetry breaking, shape vs scale, scale trade-offs, prior interpretation, normalized/orthogonal/sparse schemes, the single-minibatch activation and gradient protocol, why theory-based criteria fail, bias exceptions, learned initialization | §8.4, pp. 322–327 |

**Historical boundary.** Recorded as book-era defaults, not current ones: ε_τ ≈ 1% of ε₀ with τ ≈ a few
hundred passes; momentum α ∈ {0.5, 0.9, 0.99}; AdaGrad δ ≈ 10⁻⁷; RMSProp δ = 10⁻⁶; Adam step size 0.001 with
ρ₁ = 0.9, ρ₂ = 0.999, δ = 10⁻⁸; batch-normalization δ ≈ 10⁻⁸; conjugate-gradient restart period k = 5; batch
sizes as powers of two in 32–256 with 16 for large models; ~100-sample batches for first-order versus
~10,000 for second-order methods; ReLU hidden bias 0.1; LSTM forget-gate bias 1. Then-current verdicts,
reported as such: RMSProp among the most-used methods; no optimizer consensus, choose by familiarity; 1980s
momentum SGD still a frontier algorithm; for LSTMs plain SGD (even without momentum) displacing second-order
methods, with the general lesson that designing an easy-to-optimize model is usually easier than designing a
more powerful optimizer (§10.11, pp. 429–430); AdaGrad's premature decay found empirically on deep networks.
Era-specific examples: the Fig. 8.1 object-detection gradient trace; the remark that prominent saddles were
visualized around 2012, before SGD trained very large models; the Bengio et al. (1994b) span result; the
11-layer-to-19-layer growth example; the 1000-layer feedforward result; Theano's automatic stabilization of
unstable expressions; delta-bar-delta being full-batch only; shuffle-once-and-reuse as standard practice for
very large datasets. Nothing post-2016 is introduced — no AdamW, no warmup schedule, no scaling-law
argument — and where the book states no numeric value (the clipping threshold v, the patience in
initialization sweeps) none is invented here.

**Formula caveat.** Display equations are images in this copy (see `SOURCE.md`), so the exact normalized
initialization range, the exact clipping inequality and the exact learning-rate schedule are cited here at
prose level, which is how the book states them in words.
