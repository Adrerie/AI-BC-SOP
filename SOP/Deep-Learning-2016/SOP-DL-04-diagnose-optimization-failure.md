# SOP-DL-04 — Diagnose and repair optimization failure

**Stage:** optimize · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Separate **optimization failure** from statistical failure and repair it with the smallest change that works.
The procedure is a loop, not a catalogue:

```text
verify objective → inspect symptom → probe → minimal repair → rerun → report
```

Framing that makes this a distinct procedure: learning is not pure optimization. The target is a test-set
measure P that may itself be intractable, improved indirectly by lowering a training objective J(θ) (§8.1,
p. 298). Termination therefore differs from optimization — a pure optimizer stops when the gradient is small,
whereas a training algorithm stops on an early-stopping criterion computed from the *true* loss, at a point
where the surrogate's gradient is still large (§8.1.2, pp. 299–300). **A run that has not reached a critical
point has not necessarily failed.**

Out of scope: whether training error is the problem at all (`SOP-DL-02`), regularization (`SOP-DL-03`),
verifying that gradients are computed correctly (`SOP-DL-06`, which must run first), and structural choices
that change the optimization problem (`SOP-DL-07`). The book's full method inventories — optimizer families,
initialization schemes, meta-strategies — are compressed into the notes at §3.4 and are not reproduced here;
their derivations are recorded as theory-only in
[`concept_reconstruction.md`](../../Validation/Deep-Learning-2016/concept_reconstruction.md) §4.

## 2. Inputs and assumptions

- The regime read from `SOP-DL-02`: training error above target is the trigger for this SOP.
- A **verified gradient implementation**. Nothing here is interpretable until the numerical-derivative check
  passes (§11.5, p. 452).
- Gradient instrumentation: per-step gradient norm, activation and gradient histograms, and the
  update-to-parameter magnitude ratio (`SOP-DL-06` step 6).
- The objective's form: surrogate for a non-differentiable target? intractable, so only a gradient estimate
  exists? bounded below at all? (§8.1.1–§8.1.2; §6.2.1.1, p. 204)
- The batch regime and the hardware memory limit (§8.1.3, p. 301).

## 3. Procedure

### 3.1 Verify the objective before blaming the optimizer (§8.1)

1. Confirm the training loss is **instrumental, not terminal**: the target is the test-set measure P (§8.1,
   p. 298).
2. Confirm you are not doing pure empirical risk minimization. It easily leads to overfitting and is often
   infeasible, because the losses we would like to use — 0-1 loss is the book's example — have no usable
   derivative (§8.1.1, pp. 298–299).
3. Confirm a **surrogate** is in use and that termination is on the **true** loss. Negative log-likelihood for
   0-1 loss keeps extracting information after training 0-1 loss reaches zero, by widening margins; stop on an
   early-stopping criterion before overfitting and expect the surrogate's gradient to still be large at
   termination (§8.1.2, pp. 299–300).
4. Confirm the batch regime is deliberate (§8.1.3, pp. 300–304):
   - Gradient-estimation error falls as 1/√n, so returns to larger batches are **sublinear**.
   - Memory scales with batch size and is often the binding hardware limit; powers of two run faster on GPUs;
     very small batches waste multi-core hardware.
   - Minibatch noise acts as a regularizer — generalization is usually best at batch size 1, but the variance
     forces a small rate and many more steps. Second-order updates need much larger batches (~10,000) than
     first-order (~100).
   - Minibatches must be i.i.d.: **shuffle naturally ordered data**. Not shuffling greatly degrades
     performance; one upfront shuffle reused across epochs is acceptable, and only the first pass over a fixed
     training set gives an unbiased estimate of the generalization gradient.

If any of 1–4 is wrong, fix it and restart the loop. Most "optimizer" failures found at this stage are
objective or data-ordering failures.

### 3.2 Inspect the symptom (§8.2)

Read the symptom off the traces, then take the candidate causes it admits. **A symptom never selects one
cause uniquely** — see §3.3.

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

- **Local minima from symmetry and identifiability.** n!^m permutations and rescaling by α with 1/α for ReLU
  and maxout units create countless equal-cost minima; these are not the problem. Dangerous minima would be
  *high-cost* ones — constructible for small networks, of unknown prevalence for real networks, with the
  book-era conjecture that for large enough networks most local minima have low cost (§8.2.2, pp. 306–307).
- **Theoretical impossibility results.** Such results exist (Blum and Rivest; Judd; Wolpert and MacReady, as
  cited), but the book states they usually do not affect practice and that it is hard to tell whether a given
  problem lies in the hard class. Do not invoke them (§8.2.8, p. 314).

### 3.3 Probe

Run the probe that matches each surviving candidate, in the direction of inference the probe actually
licenses. The probes and their limits are specified in
[`BC-DL-05`](../../Benchmark/Deep-Learning-2016/BC-DL-05-optimization-diagnostic-probe-suite.md): they
**support or rule out**, they do not classify uniquely.

- Ill-conditioning → per-step ‖g‖² and gᵀHg and their ratio; count steps where a smaller step increases cost.
- Critical point → gradient-norm trace over the whole run (exclusion only).
- Cliff → update norm and parameter displacement at the jump; check for Inf/NaN.
- Vanishing/exploding → per-step gradient-norm ratio across unfolded depth (`BC-DL-06`).
- Learning-rate bracket → sweep spanning the optimum at **fixed training time**, including at least twice the
  best value; in the idealized quadratic case a rate twice the optimum makes training error *increase*
  (§11.4.1, p. 443, Fig. 11.1).
- Initialization → the single-minibatch protocol in §3.4, run **before** any training.
- Nothing fires → the failure is probably not an optimization pathology. Route to `SOP-DL-06`.

Record which candidates were **eliminated**, which were **corroborated**, and which remain undecided. Carry
the undecided set forward; it determines how conservative the repair must be.

### 3.4 Minimal repair

Apply the **cheapest repair that is safe under every surviving candidate**, one change at a time. Ordered by
cost and risk:

1. **Learning rate first** — named the most important hyperparameter, and it controls effective capacity
   non-monotonically: too high and gradient descent can *increase* training error, too low and training stalls
   permanently at high cost (§11.4.1, pp. 443–444). SGD needs decay because minibatch noise does not vanish at
   the minimum (§8.3.1, pp. 314–317).
2. **Clip** if a cliff or explosion survived probing (§10.11.1, pp. 430–431). Elementwise, or norm clipping
   (‖g‖ > v ⇒ rescale by v/‖g‖): norm preserves direction, elementwise no longer aligns with the true gradient
   but remains a descent direction, and experiments show both behave similarly. If the gradient is Inf or NaN,
   a random step of size v usually escapes. **The mean of norm-clipped minibatch gradients is a biased
   estimator** — an empirically useful heuristic bias, because large-gradient examples' contributions vanish.
   **The book states no value of v**; choose and report it.
3. **Momentum** for ill-conditioning and gradient variance (§8.3.2, pp. 317–321). Newton-style fixes that work
   for convex ill-conditioning need major modification for networks; momentum is presented as aimed at exactly
   this problem.
4. **Re-initialize** with the single-minibatch protocol below, not by switching schemes on theory (§8.4,
   pp. 322–327).
5. **Batch normalization** when no single learning rate can be right across layers (§8.7.1, pp. 339–343): each
   layer's gradient assumes the others are fixed while all update simultaneously, and higher-order cross-layer
   interactions can be exponentially large.
6. **Change the optimizer family** only after 1–5. There is **no consensus**, and the book states the choice
   depends mainly on practitioner familiarity (§8.5.4, p. 332). Record it as a familiarity decision.
7. **Change the model to make it easier to optimize** (§8.7.5, pp. 347–348) — the book's strongest meta-rule:
   most gains over thirty years came from changing model families, not optimizers, and 1980s momentum SGD is
   still a frontier algorithm. Levers: almost-everywhere-differentiable activations with nonzero gradient over
   most of the domain, avoiding jagged non-monotonic ones; more-linear units (LSTM, ReLU, maxout over stacks of
   sigmoids), because linear paths give well-scaled Jacobian singular values so gradients flow through many
   layers; skip and linear connections to shorten the input-to-output path; auxiliary heads on intermediate
   layers, which inject large gradients into low layers and are discarded after training — an alternative to
   pretraining that permits single-stage joint training.
8. **Continuation or curriculum** for global-structure problems (§8.7.6, pp. 348–350): a sequence of objectives
   of increasing difficulty sharing the same parameters, each solution initializing the next; the classic form
   blurs or smooths the objective. Even though local minima are no longer considered the main problem,
   continuation still helps by eliminating flat regions and reducing gradient-estimate variance. Three stated
   failure modes: too many intermediate objectives make the total cost high; an NP-hard problem stays NP-hard;
   blurring may never convexify, or the blurred minimum may track a local rather than a global one. Curriculum
   learning is read as continuation — weight or sample simple examples more heavily.
9. **Supervised pretraining** when direct training is too hard (§8.7.4, pp. 344–347): train simpler or shallower
   models first, then complicate, optionally followed by joint fine-tuning. Greedy initialization greatly
   accelerates joint optimization and improves solution quality. The named variants are listed in
   `concept_reconstruction.md` §4.1.
10. **Recurrent-specific** (§10.11, §10.2.1): if gradients **vanish**, clipping does not help — use gating and
    self-loops, or an information-flow regularizer **combined with** clipping, which is essential in that
    combination because it preserves the RNN dynamics at the edge of exploding gradients; expect it to
    underperform LSTM on redundant data such as language modelling. Structural limit: robust memory storage
    requires living in the vanishing-gradient region, and the cited result is that SGD's probability of
    training a vanilla RNN rapidly goes to zero once the required dependency span reaches 10 or 20 (§10.7,
    pp. 420–421). If the model is deployed open-loop after teacher forcing, train with a mixture of
    free-running inputs or use scheduled sampling (§10.2.1, pp. 401–402).
11. **Fix numerics** whenever a symptom could be arithmetic rather than geometric (§4.1–§4.4): compute
    softmax(z) with z = x − maxᵢ xᵢ, and implement a **dedicated stable log-softmax** rather than composing
    log with softmax, because numerator underflow can still give −∞. Condition number is |λ_max|/|λ_min| and
    amplifies *pre-existing* input error — a property of the matrix, not of the algorithm (§4.2, p. 114). For
    constrained problems, project the step back onto the feasible set or reparameterize; KKT conditions are
    **necessary but not sufficient** (§4.4, pp. 125–128).

**Repair menu at a glance.** Reach for the first row whose trigger matches a surviving candidate. The book's
full inventories for these options — convergence conditions and rates, the adaptive-method mechanics, the
named initialization schemes, batch-normalization placement and inference statistics — are compressed in
[`concept_reconstruction.md`](../../Validation/Deep-Learning-2016/concept_reconstruction.md) §4.1 and are not
restated here.

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

**The single-minibatch initialization protocol** is cheap enough to run every time and is the book's explicit
recommendation over theory-based criteria (§8.4, p. 325): treat each layer's weight range as a hyperparameter,
observe activation magnitude and standard deviation on **one minibatch** propagating forward, repeatedly find
the first layer whose activations shrink unacceptably and raise that layer's weights, then do the same with
gradient magnitudes if learning is still slow. Theory-based criteria fail because the criterion may be the
wrong one, the property may not survive the start of learning, or faster optimization may cost generalization
— so the empirical optimum is roughly near, but not exactly equal to, the theoretical prediction. Biases are
usually zero; the named exceptions and the named initialization schemes are listed in
`concept_reconstruction.md` §4.1.

### 3.5 Rerun

- Change **one** thing per rerun. Repair 1 and repair 3 together produce an uninterpretable result.
- Hold the split, the metric and the seed policy fixed (`SOP-DL-05`); a repair that only works on one seed is
  not a repair.
- Re-read the symptom table after each rerun rather than assuming the same cause persists: fixing a cliff can
  expose ill-conditioning that the cliff was masking.
- Stop the loop when training error meets target, or when two consecutive repairs produce no change — the
  second case means the diagnosis was wrong, so return to §3.2 rather than adding a third repair.
- Do not chase convergence past the generalization floor: since generalization error cannot fall faster than
  O(1/√m), a faster-converging optimizer may correspond to overfitting (§8.3.1, p. 317).

### 3.6 Report

See §5. The report is the artifact: a repair that is not recorded with the trace that motivated it cannot be
distinguished from a lucky seed.

## 4. Important failure modes

- **Reading a rising gradient norm as failure** — the book's successful run shows exactly that (§8.2.1,
  p. 305, Fig. 8.1).
- **Attributing a stall to a local minimum without the gradient trace.** If ‖g‖ never becomes tiny, no
  critical point is involved (§8.2.2, p. 307).
- **Treating a probe result as a classification.** Probes support or rule out; several causes can survive one
  run (`BC-DL-05` §1).
- **Using unmodified Newton on a network**: it is attracted to saddles (§8.2.3, pp. 307–310).
- **Treating a non-converged run as a failed run.** Training algorithms are expected to terminate with the
  surrogate gradient still large (§8.1.2, p. 300), and networks typically never reach a critical point
  (§8.2.7, p. 312).
- **Expecting the minimum to exist.** Some losses have no minimum (§8.2.7, p. 313; §6.2.1.1, p. 204).
- **Chasing a faster-converging optimizer** past the O(1/√m) generalization floor (§8.3.1, p. 317).
- **Justifying Nesterov momentum by its convex rate**, which does not carry to the stochastic setting
  (§8.3.3, p. 322).
- **Presenting an optimizer choice as derived.** There is no consensus; the choice depends mainly on
  practitioner familiarity (§8.5.4, p. 332).
- **Second-order methods at scale**: O(k³) for Newton, O(n²) memory for BFGS (§8.6, pp. 335, 338).
- **Clipping to fix vanishing gradients** — it does not help (§10.11.2, p. 432).
- **Ignoring clipping's bias** when the estimator's unbiasedness matters (§10.11.1, p. 431).
- **Not shuffling naturally ordered data**, which greatly degrades performance (§8.1.3, p. 302).
- **Composing log with softmax** instead of implementing a stable log-softmax (§4.1, p. 114).
- **Blaming initialization shape rather than scale**, or trusting a theoretical initialization criterion
  without the single-minibatch activation and gradient check (§8.4, pp. 323, 325).
- **Invoking theoretical impossibility results** as an explanation for a practical failure (§8.2.8, p. 314).
- **Changing two repairs at once**, which makes the rerun uninterpretable (§3.5).

## 5. Outputs and reporting

- The **loop record**: objective verified (steps 1–4 outcomes), symptom observed, probes run, which candidates
  were eliminated / corroborated / left undecided.
- The symptom → diagnosis → remedy chain with the trace that supported each diagnosis: squared gradient norm
  and gᵀHg over time for ill-conditioning; gradient norm over time to exclude critical points; activation and
  gradient histograms; the update-to-parameter ratio.
- One repair per rerun, with the rerun result and whether the symptom changed.
- Optimizer configuration: algorithm, learning-rate schedule with ε₀, ε_τ and τ, momentum coefficient and the
  implied 1/(1 − α), and adaptive-method constants if used — each recorded as a book-era default or as a
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
initialization range, the exact clipping inequality, the exact learning-rate schedule and the exact
second-order Taylor terms are cited here at prose level, which is how the book states them in words.
