# BC-DL-05 — Optimization diagnostic probe suite: do the probes support or rule out a diagnosis, and do the remedies move the diagnosed quantity?

**Tests:** whether each probe supports or rules out what the probe claims, and whether the remedy moves the
diagnosed quantity · **Executed by:**
[`SOP-DL-04`](../../SOP/Deep-Learning-2016/SOP-DL-04-diagnose-optimization-failure.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The book offers a set of diagnostic probes, each attached to a candidate cause and a remedy. The capability
under test is **whether each probe carries the evidential weight the book gives it**. That weight is the
power to *rule out* what the probe claims to rule out, and to *support* what the probe claims to support. The
test also asks whether the remedy then moves the implicated quantity.

**What this benchmark does not claim.** A trace does **not** uniquely identify a pathology.

Ill-conditioning, cliffs, plateaus and saddles co-occur in the same run. One ‖g‖ trajectory is compatible
with several of those pathologies. The book itself leaves first-order behaviour near saddles unclear
(§8.2.3, p. 309). The book also records that whether high-cost local minima are common for real networks was
open (§8.2.2, pp. 306–307).

The suite therefore scores **elimination plus corroboration**, not classification. A probe result either
removes a diagnosis from consideration, or adds support to a diagnosis that is already live. The report
states which diagnoses remain undecided.

Each arm below is written with its inference direction made explicit.

| Arm | Probe and the inference it licenses | Locator |
| --- | --- | --- |
| a | **Ill-conditioning.** SGD "sticks" — even very small steps increase the cost, because the curvature term gᵀHg exceeds the linear term. In many runs ‖g‖ does not shrink much while gᵀHg grows by more than an order of magnitude. *Supports* ill-conditioning; does not exclude a cliff or a too-large rate | §8.2.1, pp. 304–305 |
| b | **Gradient norm is not a failure indicator.** A *rising* gradient norm is compatible with successful training. *Rules out* "‖g‖ rising" as evidence of failure — a negative control on the most commonly misused trace | §8.2.1, p. 305, Fig. 8.1 |
| c | **Critical-point exclusion.** Plot the gradient norm over time; if it never shrinks to a tiny value, the failure is not a local minimum or any other critical point. *Rules out* only; a tiny gradient does not confirm a minimum, because in high dimensions many non-minimum structures also have small gradients | §8.2.2, p. 307 |
| d | **Saddle behaviour.** Saddles dominate in high dimensions; SGD trajectories escape prominent saddles quickly, while **unmodified Newton is attracted to them**. *Supports* a saddle diagnosis when escape is observed and Newton is not used; the dominance argument is about random function ensembles, not this network | §8.2.3, pp. 307–310 |
| e | **Cliff detection.** A gradient step can catapult parameters far away and destroy accumulated progress, whether approached from above or below; clipping bounds the step. *Supports* a cliff when a single step produces the displacement; also the arm that tests the remedy | §8.2.4, p. 310; §10.11.1, pp. 430–431 |
| f | **Learning-rate bracket.** A rate above the optimum can make gradient descent *increase* training error — in the idealized quadratic case when the rate is twice the optimal value. *Rules out* "the rate is too small" when error rises with the rate; the quadratic prediction is idealized and need not transfer | §11.4.1, p. 443, Fig. 11.1 |
| g | **Initialization scale, on a single minibatch.** Propagate forward, find the first layer whose activations shrink unacceptably, raise its weights, repeat; if learning is still slow, do the same with gradient magnitudes. *Supports* an initialization diagnosis; the book warns a theory-based criterion may be the wrong one or may trade generalization for speed | §8.4, p. 325 |
| h | **Batch normalization as remedy probe.** Makes lower-layer updates nearly harmless, permits one learning rate across layers, and enables single-sample inference via running averages; in a purely linear chain it makes lower layers *useless* rather than merely harmless. Tests the remedy and its stated failure condition | §8.7.1, pp. 339–343 |
| i | **Batch-size trade-off.** Generalization error is usually best at batch size 1, but the high gradient variance forces a small learning rate and many more steps; second-order updates need much larger batches (~10,000) than first-order (~100). Tests whether the gradient-variance mechanism is the operative one | §8.1.3, pp. 301–302 |

## 2. Data and comparison conditions

- **a / b**: the same model and data run to success and run into a stalled state, with per-step ‖g‖² and gᵀHg
  recorded. Arm b additionally requires a *successful* run whose gradient norm rises, to test that the
  indicator is not a failure signal by itself.
- **c**: a run stalled at high cost, with the gradient-norm trace over the whole run. The comparison is between
  the "critical point" hypothesis and the observed trace.
- **d**: a constructed or selected objective with a prominent high-cost saddle, run under first-order SGD and
  under unmodified Newton from comparable initializations.
- **e**: use a model whose cost surface contains a cliff region. The book notes that cliffs are common in
  recurrent costs, where a factor per time step is multiplied over long sequences. Run the model with and
  without clipping. Run the model under both clipping forms. Norm clipping preserves the direction.
  Elementwise clipping does not preserve the direction, but remains a descent direction.
- **f**: a learning-rate sweep spanning the optimum, including at least twice the optimal value, with training
  error recorded at **fixed training time** (the book's figure is drawn for fixed training time).
- **g**: a deep network at initialization only, with per-layer activation magnitude and standard deviation
  measured on one minibatch, before any training. Then the same measurement after applying the raise-and-repeat
  protocol.
- **h**: use the same deep network with and without batch normalization, plus a purely linear chain as the
  control. In that control the lower layers should become useless. Run inference both with minibatch
  statistics and with the training-time running averages.
- **i**: run a batch-size sweep. Include batch size 1, a power of two in the book's typical range, and a
  large batch. Match wall-clock as well as step counts. Add a second-order arm if one is available.

## 3. Baselines

- Arm a/b/c: a run known to succeed on the same model and data.
- Arm d: SGD is the reference against which Newton's behaviour at the saddle is read.
- Arm e: the unclipped run is the baseline. The two clipping forms are compared against each other, because
  the book reports that both forms behave similarly.
- Arm f: the empirically best learning rate at the same fixed training time.
- Arm g: the theoretically derived initialization range, which the book says the empirical optimum is roughly
  near but not exactly equal to.
- Arm h: the same network without batch normalization, at a single global learning rate.
- Arm i: the largest batch that fits in memory at matched wall-clock.

## 4. Metrics

1. Record the per-step values of ‖g‖² and gᵀHg, and their ratio over time (arms a, b, c).
2. Record the cost change per step. Count the steps where a smaller step *increases* the cost (arm a).
3. Record the trajectory behaviour near the critical region. State whether the run escapes, and the
   iteration count to escape (arm d).
4. Record the update norm, the parameter displacement from the pre-cliff point, and whether training recovers
   (arm e). Also record the bias the book names. The mean of the norm-clipped minibatch gradients is a biased
   estimator of the true gradient. That bias arises because the contributions of large-gradient examples
   vanish.
5. Record training error versus learning rate at fixed training time, and the incidence of oscillation
   (arm f).
6. Record the per-layer activation mean and standard deviation at initialization on one minibatch. Record the
   per-layer gradient magnitude and standard deviation (arm g).
7. Compare the run with and without batch normalization. Record the iterations to a target cost, and the
   sensitivity to the single global learning rate. Also record the agreement between minibatch-statistic
   inference and running-average inference (arm h).
8. Record generalization error and total wall-clock versus batch size (arm i).
9. **Record the per-arm verdict in the arm's own inference direction.** For each probe, state whether the
   probe *ruled out* a diagnosis, *supported* a diagnosis, or was *uninformative*. End with the set of
   diagnoses still live. A suite run that ends with one diagnosis is a report of elimination, not of
   identification.

The book states no numeric threshold for "sticks", and no tolerance for the gᵀHg growth ratio. The book
states no clipping threshold v, and no batch-size optimum. Those items are evaluator choices, and the
evaluator must report the chosen values.

## 5. How to interpret failure

- **Two or more arms point at different pathologies** is the expected outcome, not a broken suite. Report both
  and prefer the remedy that is safe under either — the book's own repair menu (clipping, momentum, batch
  normalization, a smaller rate) overlaps across causes for exactly this reason.
- **Arm a reproduces but the remedy does not help** ⇒ the evidence supports the diagnosis, and the repair is
  wrong for this model. The book notes that Newton-style fixes for convex ill-conditioning need major
  modification for networks. The book presents momentum as aimed at exactly this problem.
- **Arm b: a rising gradient norm in a failing run** ⇒ the gradient norm is not the discriminator. Use the
  gᵀHg ratio instead. That is the point of the arm.
- **Arm c: gradient norm becomes tiny** ⇒ a critical point *is* involved. The tiny gradient does not
  establish that the point is a minimum. The book states that in high dimensions many non-minimum structures
  also have small gradients. The test therefore only excludes. The test does not confirm.
- **Arm d: SGD does not escape the saddle** ⇒ the escape claim is empirical, not proven. The book describes
  first-order behaviour near saddles as still unclear. Report the geometry rather than a refutation.
- **Arm e: clipping does not prevent the loss of progress** ⇒ check whether the threshold v is large relative
  to the cliff's scale. Also check the numerical state of the gradient. If the gradient is Inf or NaN, the
  book's remedy is a random step of size v, to escape the unstable state.
- **Arm f: training error does not rise above twice the optimal rate** ⇒ the idealized quadratic prediction
  need not hold for this objective. The book calls the too-small-rate stall effect poorly understood. The
  book also states that the stall effect does not occur for a convex loss. So asymmetry between the two
  directions is expected.
- **Arm g: raising the offending layer's weights does not improve learning** ⇒ the book's own explanation
  applies. A theory-based criterion may be the wrong one. Learning may not preserve the criterion once
  training starts. Faster optimization may instead cost generalization. Report the validation error, not only
  the activation statistics.
- **Arm h: lower layers become useless rather than harmless** ⇒ the control is the purely linear chain, where
  the book predicts exactly this. Nonlinearity is what keeps the lower layers useful.
- **Arm i: batch size 1 generalizes best but is impractical** ⇒ that is the book's stated trade-off, not a
  contradiction. Report both generalization error and wall-clock.
- **Every arm uninformative** ⇒ the failure is probably not an optimization pathology at all. Route to
  `SOP-DL-06` (implementation health) before re-running the suite, since a mis-implemented gradient produces
  traces that no pathology taxonomy explains.

## 6. Validity limits and source traceability

- **No probe identifies a pathology uniquely.** The suite licenses elimination and corroboration only. The
  book itself hedges on saddle behaviour under first-order methods. The book hedges on the prevalence of
  high-cost local minima, and on the too-small-rate stall. Each corresponding arm inherits that hedge. No
  arm with an inherited hedge can report a settled diagnosis.
- Arm d's saddle-dominance argument is about **random function ensembles**: for random functions the ratio of
  saddles to minima grows exponentially with dimension. The argument is not a statement about any particular
  trained network. The book records that whether high-cost local minima are common for real networks was an
  open question. The book also carries the conjecture that for large enough networks most local minima have
  low cost (§8.2.2–8.2.3, pp. 306–309).
- Arm f's "twice the optimal rate" prediction is stated for an **idealized quadratic** case (§11.4.1, p. 443).
- Arm g's protocol uses one minibatch of feedback, and is cheaper than validation-set search. The protocol
  diagnoses initialization only. The protocol says nothing about generalization at the chosen scale.
- Arm h: §8.7.1 of this translation makes no claim that batch normalization also lowers *generalization*
  error. The practitioner-level remark appears in §11.2, p. 440, and belongs to `BC-DL-03`, not here.
- Arm i's batch-size figures (32–256 as powers of two, 16 for large models, ~100 first-order versus ~10,000
  second-order) are book-era hardware guidance, not derived optima.
- None of these arms measures generalization directly, except arm i. The rest diagnose optimization. A
  pathology correctly identified and correctly repaired still requires `SOP-DL-02` to confirm the fitting
  regime.
- Display equations are images in this copy. So the exact clipping inequality, the exact Taylor-expansion
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

**Historical boundary.** The Fig. 8.1 trace comes from a 2016-era object-detection convolutional network. The
book notes the visualization of prominent saddles around 2012, before SGD was used to train very large
models.

The batch-size figures, the momentum and adaptive-method constants and the optimizer menu are book-era. So is
the verdict that there is no consensus among optimizers, and that the choice depends mainly on practitioner
familiarity (§8.5.4, p. 332). No post-2016 optimizer, schedule or hardware argument is introduced.
