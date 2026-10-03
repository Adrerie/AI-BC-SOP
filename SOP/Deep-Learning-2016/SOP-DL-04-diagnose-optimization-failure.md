# SOP-DL-04 — Diagnose and repair optimization failure

**Stage:** optimize · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Separate **optimization failure** from statistical failure. Repair the failure with the smallest change that
works. The procedure is a loop, not a catalogue:

```text
verify objective → inspect symptom → probe → minimal repair → rerun → report
```

Learning is not pure optimization. That difference is why this SOP is a procedure of its own. The target is a
test-set measure P (§8.1, p. 298). P may itself be intractable. Training lowers a surrogate objective J(θ)
instead, and that improves P indirectly. The stopping rule therefore differs from the rule of pure
optimization. A pure optimizer stops when the gradient is small. A training algorithm stops on an
early-stopping criterion computed from the *true* loss (§8.1.2, pp. 299–300). At that point the surrogate's
gradient is still large. **A run that does not reach a critical point is not necessarily a failed run.**

Out of scope:

- whether training error is the problem at all (`SOP-DL-02`)
- regularization (`SOP-DL-03`)
- gradient verification, which must run first (`SOP-DL-06`)
- structural choices that change the optimization problem (`SOP-DL-07`)

The book's full method inventories are not reproduced here. Optimizer families, initialization schemes and
meta-strategies are compressed into the notes at §3.4. Their derivations are recorded as theory-only in
[`concept_reconstruction.md`](../../Validation/Deep-Learning-2016/concept_reconstruction.md) §4.

## 2. Inputs and assumptions

- The regime read from `SOP-DL-02`: training error above target is the trigger for this SOP.
- A **verified gradient implementation**. Nothing in this procedure is interpretable until the
  numerical-derivative check passes (§11.5, p. 452).
- Gradient instrumentation. The traces hold the per-step gradient norm, the activation histogram, the gradient
  histogram, and the ratio of update size to parameter size (`SOP-DL-06` step 6).
- The form of the objective (§8.1.1–§8.1.2; §6.2.1.1, p. 204). State whether a surrogate stands in for a
  non-differentiable target. State whether the objective is intractable, so that only a gradient estimate
  exists. State whether the objective is bounded below at all.
- The batch regime, and the hardware memory limit that constrains it (§8.1.3, p. 301).

## 3. Procedure

### 3.1 Verify the objective before blaming the optimizer (§8.1)

1. Confirm that the training loss is **instrumental, not terminal**. The target is the test-set measure P
   (§8.1, p. 298).
2. Confirm that you do not rely on pure empirical risk minimization. Empirical risk minimization easily leads
   to overfitting. It is often infeasible, because the losses we would like to use have no usable derivative
   (0-1 loss is the book's example) (§8.1.1, pp. 298–299).
3. Confirm that a **surrogate** is in use. Confirm that termination is on the **true** loss. Negative
   log-likelihood for 0-1 loss keeps extracting information after the training 0-1 loss reaches zero. The
   surrogate does this by widening margins. Stop on an early-stopping criterion before overfitting. Expect the
   surrogate's gradient to still be large at termination (§8.1.2, pp. 299–300).
4. Confirm that the batch regime is deliberate (§8.1.3, pp. 300–304):
   - Gradient-estimation error falls as 1/√n, so the return to larger batches is **sublinear**.
   - Memory scales with batch size, and is often the binding hardware limit. Powers of two run faster on GPUs.
     Very small batches waste multi-core hardware.
   - Minibatch noise acts as a regularizer. Generalization is usually best at batch size 1. The noise variance
     instead forces a small learning rate and many more steps. Second-order updates need much larger batches
     (~10,000) than first-order updates (~100).
   - Minibatches must be i.i.d. **Shuffle naturally ordered data.** If you do not shuffle, performance degrades
     greatly. One upfront shuffle, reused across epochs, is acceptable. Only the first pass over a fixed
     training set gives an unbiased estimate of the generalization gradient.

If any of steps 1–4 is wrong, fix that item. Then restart the loop. Most "optimizer" failures found at this
stage are objective failures or data-ordering failures.

### 3.2 Inspect the symptom (§8.2)

Read the symptom off the traces. Then list the candidate causes that the symptom admits. **A symptom never
selects one cause uniquely** (see §3.3).

| Symptom | Candidate causes the book names | Locator |
| --- | --- | --- |
| SGD "sticks": even very small steps *increase* the cost | Ill-conditioning — the curvature term gᵀHg exceeds the linear term; typically ‖g‖ barely shrinks while gᵀHg grows by more than an order of magnitude | §8.2.1, pp. 304–305 |
| Gradient norm **rising** | Not a symptom. The book's Fig. 8.1 shows ‖g‖ rising through a successful run | §8.2.1, p. 305 |
| Cost stalls, ‖g‖ never becomes tiny | Not a critical point. Excludes local minima and saddles | §8.2.2, p. 307 |
| Cost stalls, ‖g‖ becomes tiny | A critical point is involved — minimum, saddle or plateau. In high dimensions many non-minimum structures also have small gradients, so this does not confirm a minimum | §8.2.2, p. 307; §8.2.3, pp. 307–310 |
| Sudden large jump that destroys accumulated progress | A cliff, approached from above or below; common in recurrent costs where a factor per time step is multiplied over long sequences | §8.2.4, p. 310 |
| Long-range structure never learned | Vanishing/exploding gradients from repeated multiplication by a shared W (Wᵗ); eigenvalues >1 explode, <1 vanish | §8.2.5, pp. 310–311; §10.7, pp. 419–421 |
| Each step improves but the run wanders | Weak local–global correspondence: most training time is trajectory length, and networks typically never reach a critical point. Some losses have **no minimum** (NLL asymptotes). Failure can occur with no saddle and no minimum, simply because initialization landed on the wrong side of a hill | §8.2.7, pp. 312–314, Fig. 8.4 |
| Gradient is noisy or biased by construction | Inexact gradients — minibatches, or intractable objectives such as the Boltzmann-machine log-likelihood handled by contrastive divergence | §8.2.6, pp. 311–312 |

Two things that are **not** symptoms:

- **Local minima from symmetry and identifiability.** ReLU and maxout units give n!^m permutations, and give
  rescaling by α with 1/α. Both create countless minima of the same cost, and these are not the problem.
  Dangerous minima would be *high-cost* ones. Such minima are constructible for small networks. Their
  prevalence in real networks is unknown. The book-era conjecture is that most local minima have low cost in
  large enough networks (§8.2.2, pp. 306–307).
- **Theoretical impossibility results.** Such results exist (Blum and Rivest; Judd; Wolpert and MacReady, as
  cited). The book states that they usually do not affect practice. It also states that it is hard to tell
  whether a given problem lies in the hard class. Do not invoke an impossibility result as the explanation
  (§8.2.8, p. 314).

### 3.3 Probe

Run the probe that matches each surviving candidate. Use that probe only in the direction of inference it
actually licenses. [`BC-DL-05`](../../Benchmark/Deep-Learning-2016/BC-DL-05-optimization-diagnostic-probe-suite.md)
specifies the probes and their limits. A probe **supports or rules out** a candidate. It does not classify
uniquely.

- Ill-conditioning → record the per-step ‖g‖², the gᵀHg term, and their ratio. Count the steps where a smaller
  step increases the cost.
- Critical point → trace the gradient norm over the whole run. The trace excludes a critical point only.
- Cliff → read the update norm and the parameter displacement at the jump. Check for Inf or NaN.
- Vanishing or exploding gradient → take the per-step gradient-norm ratio across unfolded depth
  (`BC-DL-06`).
- Learning-rate bracket → run a sweep that spans the optimum at **fixed training time**. Include at least
  twice the best value. In the idealized quadratic case, a rate twice the optimum makes the training error
  *increase* (§11.4.1, p. 443, Fig. 11.1).
- Initialization → run the single-minibatch protocol in §3.4 **before** any training.
- Nothing fires → the failure is probably not an optimization pathology. Route to `SOP-DL-06`.

Record which candidates were **eliminated**, which were **corroborated**, and which remain undecided. Carry the
undecided set forward. That set determines how conservative the repair must be.

### 3.4 Minimal repair

Apply the **cheapest repair that is safe under every surviving candidate**. Change one thing at a time. The
steps below are ordered by cost and risk.

1. **Start with the learning rate.** The book names it the most important hyperparameter. It controls effective
   capacity non-monotonically. If the rate is too high, gradient descent can *increase* the training error. If
   the rate is too low, training stalls permanently at high cost (§11.4.1, pp. 443–444). SGD needs decay,
   because minibatch noise does not vanish at the minimum (§8.3.1, pp. 314–317).
2. **Clip** if a cliff or an explosion survived probing (§10.11.1, pp. 430–431). Clip elementwise, or clip the
   norm: when ‖g‖ > v, rescale g by v/‖g‖. Norm clipping preserves the direction. Elementwise clipping no
   longer aligns with the true gradient, but it remains a descent direction. The book's experiments show that
   both behave similarly. If the gradient is Inf or NaN, a random step of size v usually escapes. **The mean of
   norm-clipped minibatch gradients is a biased estimator.** The bias is an empirically useful heuristic,
   because the contributions of large-gradient examples vanish. **The book states no value of v.** Choose a
   value and report it.
3. **Add momentum** for ill-conditioning and gradient variance (§8.3.2, pp. 317–321). Newton-style fixes that
   work for convex ill-conditioning need major modification for networks. The book presents momentum as aimed at
   exactly this problem.
4. **Re-initialize** with the single-minibatch protocol below (§8.4, pp. 322–327). Do not switch initialization
   schemes on a theory-based criterion.
5. **Add batch normalization** when no single learning rate can be right across layers (§8.7.1, pp. 339–343).
   Each layer's gradient assumes that the other layers do not change, while all layers update at the same
   time. The higher-order cross-layer interactions can be exponentially large.
6. **Change the optimizer family** only after repairs 1–5. There is **no consensus**. The book states that the
   choice depends mainly on practitioner familiarity (§8.5.4, p. 332). Record the choice as a familiarity
   decision.

   > **Modern update (2017–2026) — the assumption behind the ordering, not the ordering itself.** The 2016 menu
   > puts the learning rate first and the optimizer family sixth. Its stated reason is that no consensus exists.
   > That reason stands, and the ordering is **not** changed here. One assumption behind the ordering has
   > changed. The modern anchor reports that Adam-family methods are **less sensitive to the initial learning
   > rate**. It reports that they need no complex learning-rate schedule. It reports that SGD is a special case
   > of Adam (β = 0, γ → 1). It reports that a *searched* Adam matches SGD and converges faster. It reports that
   > one named method switches from Adam to SGD partway through training.
   >
   > The operational consequence is narrow. Suppose the surviving symptom is learning-rate sensitivity, or a
   > stalling schedule rather than a pathology. Then an adaptive optimizer is a legitimate early move. Under an
   > adaptive optimizer, the "learning rate first" step costs less to satisfy. **No ranking is produced and none
   > is implied.** The choice remains problem-dependent. The 2016 package's rejection of an optimizer leaderboard
   > is reaffirmed, not reversed. The repair-ladder order is unchanged. Only the note attached to step 6 is new.
   >
   > *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §3.2. Source:
   > `UDL` §6.4, fol. 88–90.*
7. **Change the model to make it easier to optimize** (§8.7.5, pp. 347–348). This is the book's strongest
   meta-rule. Most gains over thirty years came from changing model families, not from changing optimizers.
   1980s momentum SGD is still a frontier algorithm. Use these levers:
   - Use activations that are differentiable almost everywhere and have a nonzero gradient over most of the
     domain. Avoid jagged, non-monotonic activations.
   - Use more-linear units (LSTM, ReLU, maxout over stacks of sigmoids). A linear path gives well-scaled
     Jacobian singular values, so gradients flow through many layers.
   - Add skip connections and linear connections. They shorten the path from input to output.
   - Add auxiliary heads on intermediate layers. A head injects large gradients into the low layers, and
     training discards it afterwards. This is an alternative to pretraining that permits single-stage joint
     training.
8. **Use continuation or curriculum** for a global-structure problem (§8.7.6, pp. 348–350). Continuation is a
   sequence of objectives of increasing difficulty. All the objectives share the same parameters, and each
   solution initializes the next objective. The classic form blurs or smooths the objective. The book no longer
   treats local minima as the main problem. Continuation still helps, because it eliminates flat regions and
   reduces the variance of the gradient estimate. Three failure modes are stated:
   - Too many intermediate objectives make the total cost high.
   - An NP-hard problem stays NP-hard.
   - Blurring may never convexify the problem. The blurred minimum may track a local minimum rather than a
     global one.
   Read curriculum learning as continuation. Weight simple examples more heavily, or sample them more heavily.
9. **Use supervised pretraining** when direct training is too hard (§8.7.4, pp. 344–347). Train a simpler or
   shallower model first. Then add complexity. Optionally follow it with joint fine-tuning. Greedy
   initialization greatly accelerates joint optimization. It also improves solution quality.
   `concept_reconstruction.md` §4.1 lists the named variants.
10. **Use the recurrent-specific repairs** (§10.11, §10.2.1). If the gradients **vanish**, clipping does not
    help. Use gating and self-loops. Or use an information-flow regularizer **combined with** clipping. The
    clipping is essential in that combination, because it preserves the RNN dynamics at the edge of exploding
    gradients. Expect the regularizer to underperform LSTM on redundant data such as language modelling. Note
    the structural limit. Robust memory storage requires living in the vanishing-gradient region. The cited
    result concerns the probability that SGD trains a vanilla RNN rapidly. That probability goes to zero once
    the required dependency span reaches 10 or 20 (§10.7, pp. 420–421). If training uses teacher forcing but
    deployment runs open-loop, train with a mixture of free-running inputs. Or use scheduled sampling (§10.2.1,
    pp. 401–402).
11. **Fix the numerics** whenever a symptom could be arithmetic rather than geometric (§4.1–§4.4). Compute
    softmax(z) with z = x − maxᵢ xᵢ, and implement a **dedicated stable log-softmax**. Do not compose log and
    softmax instead. The numerator of that composition can still underflow to −∞. The condition number is
    |λ_max|/|λ_min|, and it amplifies *pre-existing* input error. That is a property of the matrix, not of the
    algorithm (§4.2, p. 114). For a constrained problem, project the step back onto the feasible set. Or
    reparameterize the problem. The KKT conditions are **necessary but not sufficient** (§4.4, pp. 125–128).

**Repair menu at a glance.** Reach for the first row whose trigger matches a surviving candidate. The book's
full inventories for these options are not restated here. The inventories cover convergence conditions and
rates, and the adaptive-method mechanics. They cover the named initialization schemes, and
batch-normalization placement and its inference statistics. They are compressed in
[`concept_reconstruction.md`](../../Validation/Deep-Learning-2016/concept_reconstruction.md) §4.1.

| Option | Trigger | The one caveat that changes the decision | Locator |
| --- | --- | --- | --- |
| Learning-rate decay | Any SGD run | Decay is **required**: minibatch noise does not vanish at the minimum. Excess-error rates are O(1/√k) convex, O(1/k) strongly convex, but generalization cannot fall faster than O(1/√m) — a faster-converging optimizer may mean overfitting | §8.3.1, pp. 314–317 |
| Momentum | Ill-conditioning, gradient variance | Read α as 1/(1 − α): that multiple of plain GD is the effective maximum step | §8.3.2, pp. 317–321 |
| Nesterov momentum | Already using momentum | Evaluates the gradient after applying velocity. Improves O(1/k)→O(1/k²) in the **convex batch** case only; **no** stochastic rate gain — do not justify it by the convex rate | §8.3.3, pp. 321–322 |
| RMSProp / Adam | Per-parameter sensitivity that is roughly axis-aligned | AdaGrad's *cumulative* accumulation decays prematurely on deep networks; RMSProp uses an exponentially weighted moving average instead; Adam adds first-moment momentum plus bias correction of both moments | §8.5.1–§8.5.3, pp. 327–332 |
| Any optimizer, as a choice | After repairs 1–5 have failed | **No consensus.** The popular set is SGD, SGD+momentum, RMSProp, RMSProp+momentum, AdaDelta, Adam; the book states the choice depends mainly on practitioner familiarity. Record it as a familiarity decision | §8.5.4, p. 332 |
| Second-order methods | Almost never | Newton needs a positive-definite Hessian, is attracted to saddles, and costs O(k³); BFGS costs O(n²) memory. Conjugate gradient avoids the inverse and is reported reasonable, *better if preceded by a few SGD steps*; L-BFGS cuts storage to O(n) per step. Verdict: not worth it at scale | §8.6, pp. 332–339 |
| Coordinate descent | Variables split into nearly independent blocks, or one block is much cheaper | Sparse coding is the example: jointly non-convex but convex per block. Do **not** use when one variable strongly determines another's optimum | §8.7.2, pp. 343–344 |
| Polyak averaging | Trajectory oscillates across a valley | Strong guarantees for convex gradient descent; heuristic but effective for networks. Use exponentially decayed averaging when non-convex | §8.7.3, p. 344 |
| Re-initialization | Slow start, dead or saturating layers, vanishing/exploding at depth | The firm requirement is **symmetry breaking**; the **size** of the distribution matters far more than its shape (Gaussian vs uniform "does not seem to make much difference"). Use the single-minibatch protocol rather than trusting a named scheme | §8.4, pp. 322–327 |
| Batch normalization | No single learning rate can be right across layers | "Not really an optimization algorithm but an adaptive reparameterization"; the key step is backpropagating through the normalization. In a toy **linear** chain it makes lower layers harmless but *useless* — nonlinearity is what keeps them useful. Its regularization side effect is **not** in §8.7.1 of this translation; that remark is §11.2, p. 440 and belongs to `SOP-DL-03` | §8.7.1, pp. 339–343 |

**The single-minibatch initialization protocol** is cheap enough to run every time. The book recommends it
explicitly over theory-based criteria (§8.4, p. 325). Treat each layer's weight range as a hyperparameter.
Propagate **one minibatch** forward, and observe the activation magnitude and the standard deviation. Find the
first layer whose activations shrink unacceptably. Raise that layer's weights, and repeat. If learning is still
slow, do the same with the gradient magnitudes. Theory-based criteria fail for three reasons. The criterion may
be the wrong one. The property may not survive the start of learning. Faster optimization may cost
generalization. So the empirical optimum is roughly near the theoretical prediction, but not exactly equal to
it. Biases are usually zero. `concept_reconstruction.md` §4.1 lists the named exceptions and the named
initialization schemes.

### 3.5 Rerun

- Change **one** thing per rerun. Repair 1 and repair 3 together produce an uninterpretable result.
- Hold the split, the metric and the seed policy fixed (`SOP-DL-05`). A repair that works on one seed only is
  not a repair.
- Re-read the symptom table after each rerun. Do not assume that the same cause persists. Fixing a cliff can
  expose the ill-conditioning that the cliff masked.
- Stop when the declared training objective is adequate for the task. Stop when the current evidence no longer
  supports another repair. If a repair does not move the quantity it was meant to change, re-open the
  diagnosis at §3.2. Do not apply repairs mechanically.
- Do not chase convergence past the generalization floor. Generalization error cannot fall faster than
  O(1/√m). So a faster-converging optimizer may correspond to overfitting (§8.3.1, p. 317).

### 3.6 Report

See §5. The report is the artifact. No one can tell a repair from a lucky seed unless the record carries the
trace that motivated it.

## 4. Important failure modes

- **Reading a rising gradient norm as failure.** The book's successful run shows exactly that (§8.2.1, p. 305,
  Fig. 8.1).
- **Attributing a stall to a local minimum without the gradient trace.** If ‖g‖ never becomes tiny, no
  critical point is involved (§8.2.2, p. 307).
- **Treating a probe result as a classification.** Probes support or rule out. Several causes can survive one
  run (`BC-DL-05` §1).
- **Using unmodified Newton on a network.** Newton is attracted to saddles (§8.2.3, pp. 307–310).
- **Treating a non-converged run as a failed run.** Training algorithms are expected to terminate with the
  surrogate gradient still large (§8.1.2, p. 300). Networks typically never reach a critical point (§8.2.7,
  p. 312).
- **Expecting the minimum to exist.** Some losses have no minimum (§8.2.7, p. 313; §6.2.1.1, p. 204).
- **Chasing a faster-converging optimizer** past the O(1/√m) generalization floor (§8.3.1, p. 317).
- **Justifying Nesterov momentum by its convex rate**, which does not carry to the stochastic setting
  (§8.3.3, p. 322).
- **Presenting an optimizer choice as derived.** There is no consensus. The choice depends mainly on
  practitioner familiarity (§8.5.4, p. 332).
- **Second-order methods at scale.** Newton costs O(k³), and BFGS needs O(n²) memory (§8.6, pp. 335, 338).
- **Clipping to fix vanishing gradients.** Clipping does not help here (§10.11.2, p. 432).
- **Ignoring clipping's bias** when the estimator's unbiasedness matters (§10.11.1, p. 431).
- **Not shuffling naturally ordered data**, which greatly degrades performance (§8.1.3, p. 302).
- **Composing log with softmax** instead of implementing a stable log-softmax (§4.1, p. 114).
- **Blaming the shape of the initialization rather than its scale** (§8.4, pp. 323, 325).
- **Trusting a theoretical initialization criterion** without the single-minibatch activation and gradient check
  (§8.4, pp. 323, 325).
- **Invoking theoretical impossibility results** as an explanation for a practical failure (§8.2.8, p. 314).
- **Changing two repairs at once**, which makes the rerun uninterpretable (§3.5).

## 5. Outputs and reporting

- Keep the **loop record**. Record the outcome of each of steps 1–4, the symptom observed, and the probes run.
  Mark each candidate as eliminated, corroborated, or undecided.
- Record the symptom → diagnosis → remedy chain, with the trace that supported each diagnosis. For
  ill-conditioning, record the squared gradient norm and gᵀHg over time. To exclude critical points, record the
  gradient norm over time. Record the activation histograms and the gradient histograms. Record the ratio of
  update size to parameter size.
- Record one repair per rerun, with the rerun result and whether the symptom changed.
- Record the optimizer configuration. Name the algorithm, and the learning-rate schedule with ε₀, ε_τ and τ.
  Record the momentum coefficient and the implied 1/(1 − α). Record the adaptive-method constants, if you used
  any. Mark each value as a book-era default or as a searched value.
- Record the batch regime. Name the size, the shuffling policy and the memory headroom. State whether you
  probed the trade-off of generalization against runtime.
- Record the initialization. Name the scheme and the per-layer weight ranges. Give the result of the
  single-minibatch activation and gradient check. List every bias exception applied.
- Record the meta-strategies you applied, and why. Include batch-normalization placement and its inference
  statistics. Include averaging, pretraining or hints, and continuation or curriculum. Include any structural
  change made to ease optimization.
- If you clipped, record the form of the clipping (norm or elementwise) and the threshold v. Record how often
  clipping triggered. Record the bias caveat.
- State what the book does not fix, and what you chose instead. Cover v, τ and ε_τ in any setting other than
  the book's rule of thumb. Cover the number of continuation stages. Cover the optimizer family.

## 6. Source traceability

| Claim or step | Locator |
| --- | --- |
| Learning vs pure optimization; the intractable test measure P | §8.1, p. 298 |
| ERM leads to overfitting and is often infeasible; surrogate losses; termination with a large surrogate gradient | §8.1.1–§8.1.2, pp. 298–300 |
| Batch vs minibatch: 1/√n error decay, memory scaling, powers of two, batch-1 generalization, second-order batch sizes, i.i.d. shuffling, unbiasedness of the first pass | §8.1.3, pp. 300–304 |
| Ill-conditioning: sticking, gᵀHg vs ‖g‖², rising gradient norm in a successful run | §8.2.1, pp. 304–305, Fig. 8.1 |
| Local minima: symmetry and identifiability, high-cost minima open question, gradient-norm exclusion test | §8.2.2, pp. 306–307 |
| Saddles dominate in high dimensions; SGD escapes; Newton is attracted; constant plateaus | §8.2.3, pp. 307–310, Fig. 8.2 |
| Cliffs and explosion; clipping as the remedy; cliffs common in recurrent costs | §8.2.4, p. 310 |
| Long-term dependencies; Wᵗ; power-method view; feedforward nets use different matrices | §8.2.5, pp. 310–311 |
| Recurrent long-range gradients exponentially small; robust memory requires the vanishing region; span-10/20 result | §10.7, pp. 419–421 |
| Inexact gradients; surrogate choice | §8.2.6, pp. 311–312 |
| Weak local–global correspondence; trajectory length; no minimum; wrong side of the hill; better initial points prescribed | §8.2.7, pp. 312–314, Fig. 8.4 |
| Theoretical limits and their practical irrelevance | §8.2.8, p. 314 |
| SGD schedule, decay conditions, τ and ε_τ rules, oscillation diagnosis, excess-error rates, Cramér–Rao floor | §8.3.1, pp. 314–317 |
| Momentum, 1/(1 − α) reading, common α values | §8.3.2, pp. 317–321, Fig. 8.5 |
| Nesterov momentum and its convex-only rate gain | §8.3.3, pp. 321–322 |
| AdaGrad accumulation problem; RMSProp moving average and verdict; Adam moments and bias correction | §8.5.1–§8.5.3, pp. 327–332 |
| No consensus; popular set; choice by familiarity | §8.5.4, p. 332 |
| Newton, conjugate gradient, BFGS and L-BFGS verdicts | §8.6, pp. 332–339 |
| Batch normalization: diagnosis, reparameterization framing, mechanism, backprop through normalization, inference statistics, γ and β, placement, linear-chain caveat | §8.7.1, pp. 339–343 |
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
| Learning rate as the most important hyperparameter; too high can increase training error; too low stalls | §11.4.1, pp. 443–444, Fig. 11.1 |

**Historical boundary.** These values are recorded as book-era defaults, not as current ones:

- ε_τ ≈ 1% of ε₀, with τ ≈ a few hundred passes
- momentum α ∈ {0.5, 0.9, 0.99}
- AdaGrad δ ≈ 10⁻⁷
- RMSProp δ = 10⁻⁶
- Adam step size 0.001, with ρ₁ = 0.9, ρ₂ = 0.999 and δ = 10⁻⁸
- batch-normalization δ ≈ 10⁻⁸
- conjugate-gradient restart period k = 5
- batch sizes as powers of two in 32–256, with 16 for large models
- ~100-sample batches for first-order methods, against ~10,000 for second-order methods
- ReLU hidden bias 0.1
- LSTM forget-gate bias 1

These verdicts were current at publication, and are reported as such:

- RMSProp stood among the most-used methods.
- There was no optimizer consensus. The choice went by familiarity.
- 1980s momentum SGD was still a frontier algorithm.
- For LSTMs, plain SGD displaced second-order methods, even without momentum. The general lesson was that
  designing an easy-to-optimize model is usually easier than designing a more powerful optimizer (§10.11,
  pp. 429–430).
- AdaGrad's premature decay was found empirically on deep networks.

These examples are era-specific:

- the Fig. 8.1 object-detection gradient trace
- the remark that prominent saddles were visualized around 2012, before SGD trained very large models
- the Bengio et al. (1994b) span result
- the 11-layer-to-19-layer growth example
- the 1000-layer feedforward result
- Theano's automatic stabilization of unstable expressions
- delta-bar-delta being full-batch only
- shuffle-once-and-reuse as standard practice for very large datasets

Nothing after 2016 is introduced into the 2016 procedure. There is no warmup schedule, no scaling-law argument
and no AdamW mechanics. Where the book states no numeric value, none is invented here. That covers the clipping
threshold v and the patience in initialization sweeps.

**Modern-update provenance.** The modern update adds one annotated exception: the block attached to §3.4 step 6.
The block records that the learning-rate-sensitivity assumption behind the repair ordering no longer holds as
stated. The block changes no step and produces no ranking. Its source lies outside the 2016 book. It is
recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§3.2. The source key `UDL` §6.4, fol. 88–90 is defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1. The 2016 text of step 6 is
unchanged, and so is the repair-menu row that it belongs to.

**Formula caveat.** Display equations are images in this copy (see `SOURCE.md`). Four of them are cited here at
prose level. The list holds the exact normalized initialization range, the exact clipping inequality, the exact
learning-rate schedule and the exact second-order Taylor terms. That is how the book states those items in
words.
