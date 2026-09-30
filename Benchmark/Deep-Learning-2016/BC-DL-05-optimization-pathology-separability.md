# BC-DL-05 — Can optimization pathologies be distinguished from traces, and do the remedies move the diagnosed quantity?

**Tests:** whether the book's symptom → cause → remedy mappings are separable in practice · **Executed by:**
[`SOP-DL-04`](../../SOP/Deep-Learning-2016/SOP-DL-04-diagnose-optimization-failure.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The book gives a diagnostic taxonomy in which each pathology has a distinct observable signature and a
distinct remedy. The capability under test is **separability**: can a researcher, given only training traces,
identify which pathology is present; and does the prescribed remedy change the quantity the diagnosis
implicated?

| Arm | Claim under test | Locator |
| --- | --- | --- |
| a | Ill-conditioning signature: SGD "sticks" — even very small steps increase the cost, because the curvature term gᵀHg exceeds the linear term. In many runs ‖g‖ does not shrink much while gᵀHg grows by more than an order of magnitude | §8.2.1, pp. 304–305 |
| b | A **rising** gradient norm is compatible with successful training, so gradient norm alone is not a failure indicator | §8.2.1, p. 305, Fig. 8.1 |
| c | Local-minima exclusion test: plot the gradient norm over time; if it never shrinks to a tiny value, the failure is not a local minimum or any other critical point | §8.2.2, p. 307 |
| d | Saddles dominate in high dimensions; SGD trajectories escape prominent saddles quickly, while **unmodified Newton is attracted to them** | §8.2.3, pp. 307–310 |
| e | Cliffs: a gradient step can catapult parameters far away and destroy accumulated progress, whether approached from above or below; clipping bounds the step | §8.2.4, p. 310; §10.11.1, pp. 430–431 |
| f | A learning rate above the optimum can make gradient descent *increase* training error — in the idealized quadratic case when the rate is twice the optimal value | §11.4.1, p. 443, Fig. 11.1 |
| g | Initialization scale is diagnosable on a **single minibatch**: propagate forward, find the first layer whose activations shrink unacceptably, raise its weights, repeat; if learning is still slow, do the same with gradient magnitudes | §8.4, p. 325 |
| h | Batch normalization makes lower-layer updates nearly harmless, permits one learning rate across layers, and enables single-sample inference via running averages; in a purely linear chain it makes lower layers *useless* rather than merely harmless | §8.7.1, pp. 339–343 |
| i | Batch size trades generalization against runtime: generalization error is usually best at batch size 1, but the high gradient variance forces a small learning rate and many more steps; second-order updates need much larger batches (~10,000) than first-order (~100) | §8.1.3, pp. 301–302 |

## 2. Data and comparison conditions

- **a / b**: the same model and data run to success and run into a stalled state, with per-step ‖g‖² and gᵀHg
  recorded. Arm b additionally requires a *successful* run whose gradient norm rises, to test that the
  indicator is not a failure signal by itself.
- **c**: a run stalled at high cost, with the gradient-norm trace over the whole run. The comparison is between
  the "critical point" hypothesis and the observed trace.
- **d**: a constructed or selected objective with a prominent high-cost saddle, run under first-order SGD and
  under unmodified Newton from comparable initializations.
- **e**: a model whose cost surface contains a cliff region — the book notes cliffs are common in recurrent
  costs, where a factor per time step is multiplied over long sequences — run with and without clipping, and
  under both clipping forms (norm clipping, which preserves direction, and elementwise clipping, which does not
  but remains a descent direction).
- **f**: a learning-rate sweep spanning the optimum, including at least twice the optimal value, with training
  error recorded at **fixed training time** (the book's figure is drawn for fixed training time).
- **g**: a deep network at initialization only, with per-layer activation magnitude and standard deviation
  measured on one minibatch, before any training. Then the same measurement after applying the raise-and-repeat
  protocol.
- **h**: the same deep network with and without batch normalization, plus a purely linear chain as the control
  in which lower layers should become useless. Inference must be run both with minibatch statistics and with
  the training-time running averages.
- **i**: a batch-size sweep including 1, a power of two in the book's typical range, and a large batch, with
  matched wall-clock as well as matched step counts, and a second-order arm if one is available.

## 3. Baselines

- Arm a/b/c: a run known to succeed on the same model and data.
- Arm d: SGD is the reference against which Newton's behaviour at the saddle is read.
- Arm e: the unclipped run is the baseline; the two clipping forms are compared against each other, since the
  book reports they behave similarly.
- Arm f: the empirically best learning rate at the same fixed training time.
- Arm g: the theoretically derived initialization range, which the book says the empirical optimum is roughly
  near but not exactly equal to.
- Arm h: the same network without batch normalization, at a single global learning rate.
- Arm i: the largest batch that fits in memory at matched wall-clock.

## 4. Metrics

1. ‖g‖² and gᵀHg per step, and their ratio over time (arms a, b, c).
2. Cost change per step, including the count of steps where a smaller step *increases* the cost (arm a).
3. Trajectory behaviour near the critical region: whether the run escapes, and the iteration count to escape
   (arm d).
4. Update norm, parameter displacement from the pre-cliff point, and whether training recovers (arm e); plus
   the bias the book names — the mean of norm-clipped minibatch gradients is a biased estimator of the true
   gradient, because large-gradient examples' contributions vanish.
5. Training error versus learning rate at fixed training time, and the incidence of oscillation (arm f).
6. Per-layer activation mean and standard deviation at initialization on one minibatch; per-layer gradient
   magnitude and standard deviation (arm g).
7. With and without batch normalization: iterations to a target cost, sensitivity to the single global
   learning rate, and agreement between minibatch-statistic inference and running-average inference (arm h).
8. Generalization error and total wall-clock versus batch size (arm i).

The book states no numeric threshold for "sticks", no tolerance for the gᵀHg growth ratio, no clipping
threshold v, and no batch-size optimum; those are evaluator choices and must be reported.

## 5. How to interpret failure

- **Arm a reproduces but the remedy does not help** ⇒ the diagnosis is right and the repair is wrong for this
  model; the book notes that Newton-style fixes for convex ill-conditioning need major modification for
  networks, and presents momentum as aimed at exactly this problem.
- **Arm b: a rising gradient norm in a failing run** ⇒ gradient norm is not the discriminator; use the gᵀHg
  ratio instead. This is the point of the arm.
- **Arm c: gradient norm becomes tiny** ⇒ a critical point *is* involved, but this does not establish that it
  is a minimum; the book states that in high dimensions many non-minimum structures also have small
  gradients, so the test only excludes, it does not confirm.
- **Arm d: SGD does not escape the saddle** ⇒ the escape claim is empirical, not proven; the book describes
  first-order behaviour near saddles as still unclear, so report the geometry rather than a refutation.
- **Arm e: clipping does not prevent the loss of progress** ⇒ check whether the threshold v is large relative
  to the cliff's scale, and whether the gradient was numerically Inf or NaN, in which case the book's remedy
  is a random step of size v to escape the unstable state.
- **Arm f: training error does not rise above twice the optimal rate** ⇒ the idealized quadratic prediction
  need not hold for this objective; the book states the too-small-rate stall effect is poorly understood and
  does not occur for a convex loss, so asymmetry between the two directions is expected.
- **Arm g: raising the offending layer's weights does not improve learning** ⇒ the book's own explanation
  applies: a theory-based criterion may be the wrong one, may not be preserved once learning starts, or may
  trade generalization for optimization speed. Report the validation error, not only the activation
  statistics.
- **Arm h: lower layers become useless rather than harmless** ⇒ the control is the purely linear chain, where
  the book predicts exactly this; nonlinearity is what keeps lower layers useful.
- **Arm i: batch size 1 generalizes best but is impractical** ⇒ that is the book's stated trade-off, not a
  contradiction; report both generalization error and wall-clock.

## 6. Validity limits and source traceability

- Arm d's saddle-dominance argument is about **random function ensembles**: for random functions the ratio of
  saddles to minima grows exponentially with dimension. It is not a statement about any particular trained
  network, and the book records that whether high-cost local minima are common for real networks was an open
  question, with the conjecture that for large enough networks most local minima have low cost (§8.2.2–8.2.3,
  pp. 306–309).
- Arm f's "twice the optimal rate" prediction is stated for an **idealized quadratic** case (§11.4.1, p. 443).
- Arm g's protocol uses one minibatch of feedback and is cheaper than validation-set search, but it diagnoses
  initialization only; it says nothing about generalization at the chosen scale.
- Arm h: the claim that batch normalization also lowers *generalization* error is not made in §8.7.1 of this
  translation; the practitioner-level remark appears in §11.2, p. 440, and belongs to `BC-DL-03`, not here.
- Arm i's batch-size figures (32–256 as powers of two, 16 for large models, ~100 first-order versus ~10,000
  second-order) are book-era hardware guidance, not derived optima.
- None of these arms measures generalization directly except arm i; the rest diagnose optimization. A
  pathology correctly identified and correctly repaired still requires `SOP-DL-02` to confirm the fitting
  regime.
- Display equations are images in this copy, so the exact clipping inequality, the exact Taylor-expansion
  terms and the exact initialization range are cited at prose level.

| Claim | Locator |
| --- | --- |
| Ill-conditioning: sticking, gᵀHg versus ‖g‖², order-of-magnitude growth, rising gradient norm in a successful run | §8.2.1, pp. 304–305, Fig. 8.1 |
| Local minima: symmetry and identifiability, high-cost minima open question, gradient-norm exclusion test | §8.2.2, pp. 306–307 |
| Saddles dominate; SGD escapes; Newton attracted; constant plateaus defeat all optimizers | §8.2.3, pp. 307–310, Fig. 8.2 |
| Cliffs and explosion; clipping as remedy; cliffs common in recurrent costs | §8.2.4, p. 310 |
| Clipping forms, threshold rule, Inf/NaN escape, bias of the clipped estimator | §10.11.1, pp. 430–431 |
| Learning rate above optimum can increase training error; U-shaped training error in the rate | §11.4.1, p. 443, Fig. 11.1 |
| Initialization: symmetry breaking, scale over shape, the single-minibatch activation and gradient protocol, why theory-based criteria fail | §8.4, pp. 322–327 |
| Batch normalization: diagnosis, reparameterization framing, mechanism, backprop through normalization, running averages for inference, γ and β, linear-chain caveat | §8.7.1, pp. 339–343 |
| Batch normalization sometimes lowers generalization error | §11.2, p. 440 |
| Batch size: 1/√n error decay, memory scaling, powers of two, batch-1 generalization, second-order batch sizes, shuffling | §8.1.3, pp. 300–304 |

**Historical boundary.** The Fig. 8.1 trace comes from a 2016-era object-detection convolutional network; the
book notes that prominent saddles were visualized around 2012, before SGD was used to train very large models.
The batch-size figures, the momentum and adaptive-method constants and the optimizer menu are book-era, as is
the verdict that there is no consensus among optimizers and that the choice depends mainly on practitioner
familiarity (§8.5.4, p. 332). No post-2016 optimizer, schedule or hardware argument is introduced.
