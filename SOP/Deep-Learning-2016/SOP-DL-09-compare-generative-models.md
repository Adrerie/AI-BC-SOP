# SOP-DL-09 — Compare generative models, and decide whether an intractable-likelihood number can be trusted

**Stage:** evaluate · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Produce a comparison between generative models that is not silently invalid. The book frames the problem
directly: comparing one generative model with another is a difficult and subtle task, because usually the
log-probability of data under the model **cannot actually be evaluated — only an approximation of it can
be** — and in that situation the first obligation is to think through and communicate clearly *what is
being measured* (§20.14, p. 715).

This SOP owns: declaring the measured quantity; enforcing identical preprocessing and data-type
handling; sample-quality assessment and its known blind spots; likelihood-based comparison including the
partition-function-ratio rule; auditing whatever estimator produced log Z; the ELBO gap as a diagnostic
and its limit; and MCMC trustworthiness (burn-in, mixing, importance-weight degeneracy, fresh-chain
evaluation).

Out of scope: choosing or training a generative family. Nothing here ranks families; the book's own
closing position is that the metric must match the intended use and that **all metrics currently in use
still have serious flaws** (§20.14, p. 717).

## 2. Inputs and assumptions

- Two or more candidate models, and a **declared intended use** for the generative model. The metric must
  match the use (§20.14, p. 717).
- A test set with frozen preprocessing, plus an explicit declaration of the data type (real-valued or
  binary) and, if binary, of the exact binarization scheme (§20.14, p. 716).
- For likelihood-based comparison: either a tractable likelihood, or an estimator/bound for log Z
  (§18.7, pp. 624–625).
- A sampler, and the ability to look up nearest neighbours in the training set under Euclidean distance
  (§20.14, p. 716).
- For MCMC-based estimators: the ability to run **fresh chains from random initialization**, separately
  from any chain used during training (§18.2, p. 615).

## 3. Procedure

### 3.1 Declare before measuring

1. **State the intended use.** Some generative models are better at assigning high probability to most
   real points, others at avoiding high probability on unrealistic points; the book attributes the
   difference to whether the model is designed to minimize the forward or the reverse KL divergence
   (referring to its Fig. 3.6, and to §3.13 信息论 where both are defined, pp. 105–109). Which model is
   "better" is a function of the use, so the use is declared first (§20.14, p. 717).
2. **State what quantity is being measured, and whether it is an estimate or a bound.** The book's worked
   case: model A is scored by a *stochastic estimate* of log-likelihood and model B by a *deterministic
   lower bound*. If A scores higher, the question "which is better?" cannot be answered unless there is
   some way to determine how loose B's bound is (§20.14, p. 715). Estimates and bounds must never share a
   ranking axis without the bound's looseness being reported.
3. **Use the task-based escape hatch where the use is practical.** If the concern is practical
   performance — the book's example is anomaly detection — models can be compared fairly on
   task-specific criteria, e.g. ranking test cases and reporting **precision and recall** (§20.14,
   p. 715). This sidesteps incommensurable likelihoods entirely.

> **Modern update (2017–2026) — two additions to the declaration step.** Steps 1–3 are unchanged and the
> ambiguity in step 2's worked case remains; the first addition supplies a valid one-sided case.
>
> **3a. A lower bound from one family can legitimately outrank an exact likelihood from another.** Step 2
> cautions that a higher stochastic estimate cannot be ranked above another model's lower bound without
> further information. A valid lower bound for A **above** B's exact log-likelihood does establish a
> one-sided likelihood ordering on matched data and units; when A's bound falls below B's exact value, the
> ranking is undecided. The modern families also make it easy to confuse training with evaluation:
>
> - Of the four generative families the modern anchor discusses, **normalizing flows are the only one that
>   computes the exact log-likelihood.** Test likelihood is ineffective for GANs, expensive for
>   variational-autoencoder and diffusion models, and exact and efficient only for flows.
> - Its own footnote supplies the case that trips the 2016 rule: "**The lower bound on the likelihood for
>   diffusion models can actually exceed the exact computation in normalizing flows, but data generation is
>   much slower.**" That ordering is a valid one-sided **likelihood** result on commensurate data; the
>   generation-cost asymmetry is a separate axis and must not be folded into the likelihood conclusion. State
>   both, and make any overall utility claim only from both.
> - Diffusion models are trained on an ELBO in which "the decoder must do all the work since the encoder has
>   no parameters." A widely used training objective **drops the variational weighting** from that bound —
>   down-weighting the hard small-noise terms lets the network concentrate on the more difficult large-noise
>   ones — and produces the best sample-quality score in its source's experiments. **The training loss and the
>   evaluation instrument are different things**: a model trained with that simplified loss can still be
>   evaluated with the standard variational bound, and that evaluation result is the number to put on a
>   likelihood axis.
>
> Required of step 2: identify the model family, the **training objective** and the **separate evaluation
> instrument** (exact likelihood, stochastic estimate or bound). State any valid one-sided comparison and
> report generation cost separately when overall practical utility is discussed.
>
> **3b. A conditional-generation use decomposes into nameable attribute axes.** Step 1 requires the intended
> use to be declared. For text-conditioned generation the use is not one axis: declare **which
> attribute-rendering axes it will be judged on** — colour, counting, spatial relation, and whatever else the
> use turns on — because a model can satisfy an aggregate score while failing a named axis.
>
> Boundary on 3b: the modern anchor names a purpose-built evaluation set for exactly these axes, cited here as
> an *example of the category* (`delta_map.md` §4.5). This SOP requires the axes to be declared; it requires no
> benchmark, and none is named as mandatory.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §4.1, §4.5. Sources:
> `UDL` §14.3 fol. 272, §16.5.1 fol. 319 and fn. 2, §18.4.1 fol. 358, §18.6 fol. 371–372; `DDPM`; `FM`.*

### 3.2 Make the comparison commensurable

4. **Freeze preprocessing across models.** Other areas of machine learning tolerate per-algorithm
   preprocessing variation — when comparing object-recognition accuracies it is usually acceptable to
   preprocess input images slightly differently per algorithm. Generative modelling does not tolerate it:
   any change to the input data changes the distribution to be captured and fundamentally changes the
   task. The book's example: multiplying inputs by 0.1 artificially increases the probability tenfold
   (§20.14, p. 716).
5. **Enforce data-type comparability.** Real-valued models may be compared only with real-valued models,
   binary only with binary; otherwise the measured likelihoods are not in the same space, because a
   binary model's log-likelihood is at most zero while a real-valued log-density is unbounded above
   (§20.14, p. 716).
6. **Enforce identical binarization.** For binary models the two must use exactly the same binarization:
   a fixed threshold at 0.5, or stochastic binarization that draws a sample per pixel using the gray
   value as the probability of a 1. If stochastic, either binarize the whole dataset once — the book notes
   that researchers sharing a single random binarization share the resulting file so that results do not
   differ by binarization draw — or re-draw at every training step and evaluate over multiple samples.
   Each of these schemes produces **very different likelihood numbers** (§20.14, p. 716).

### 3.3 Assess samples, knowing what the assessment cannot see

7. **Inspect samples**, ideally not by the researchers themselves but by naive experimental subjects who
   do not know the provenance of the samples (Denton et al., 2015, as cited) (§20.14, p. 716).
8. **Assume the inspection is weak.** A very poor probability model may produce very good-looking
   samples (§20.14, p. 716).
9. **Run the nearest-neighbour test**: for some generated samples, display their Euclidean nearest
   neighbour in the training set (the book points to its Fig. 16.1). The test is aimed at detecting a
   model that overfits the training set by merely reproducing training instances (§20.14, p. 716).
10. **Account for simultaneous over- and under-fitting.** The book's example: a model trained on dog and
    cat images that simply learns to reproduce the dog training images is clearly overfitting (it cannot
    produce images outside the training set) and also underfitting (it assigns no probability to the cat
    images) — yet a human observer will judge every individual dog image high quality. In this simple case
    an observer who can inspect many samples easily notices the absence of cats; in realistic settings,
    with a generative model trained on data with tens of thousands of modes, the model can drop a few
    modes and human observers cannot easily inspect or remember enough images to detect the missing
    variation (§20.14, pp. 716–717).

### 3.4 Compute likelihood, and check for reward hacking

11. **Compute test-set log-likelihood when it is computationally feasible**, precisely because visual
    sample quality is not a reliable criterion (§20.14, p. 717).
12. **Check the variance-collapse failure.** A real-valued MNIST model can assign arbitrarily low
    variance to background pixels that never change and thereby earn arbitrarily high likelihood. The
    possibility of driving the cost toward −∞ exists in **any** real-valued maximum-likelihood problem,
    and is especially severe for MNIST generation because many output values need not be predicted at
    all. The book draws the conclusion explicitly: this strongly indicates that other ways of evaluating
    generative models need to be developed (§20.14, p. 717).

> **Modern update (2017–2026) — the likelihood/sample-quality disagreement has a named mechanism.** Steps 8
> and 11 stand: a very poor probability model may produce very good-looking samples, so compute the likelihood
> where it is feasible. The modern literature supplies the mirror case — a model with state-of-the-art sample
> quality that concedes uncompetitive log-likelihoods, and explains it by spending lossless codelength on
> distortions no observer can perceive. So the two instruments can move in opposite directions for reasons that
> are **not** either instrument failing. Its result figures are in `delta_map.md` §4.3, not restated here.
>
> What this changes in practice, as an addition to steps 8 and 11 rather than a replacement:
>
> - **Report which axis a number is on.** A bits-per-dim figure and a sample-quality score are not two
>   readings of one underlying quality. Report both, label each, and never present one as evidence about the
>   other.
> - **When they disagree, name which kind of disagreement it is before adjudicating.** Step 12's variance
>   collapse is a likelihood number earned dishonestly — a defect. Imperceptible-detail codelength is a
>   likelihood number honestly uncompetitive — a property of the metric. The two look identical from the
>   direction of the numbers, and step 12's per-dimension variance check is what separates them.
> - **The disagreement is not a licence to drop likelihood.** The flow-matching source reports bits/dim and a
>   sample-quality score jointly and disputes neither. Nothing in this lineage's sources declares bits-per-dim
>   an inappropriate metric; that stronger claim was searched for and **not found**.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §4.3, §4.2. Sources:
> `DDPM` (§3.4, §4.1 and Table 1; verbatim quotes in `sources.md` §2.3); `FM`.*

### 3.5 Compare through the partition function when the likelihood is intractable

13. **Use the ratio rule.** Estimating Z matters exactly when evaluating models, monitoring training
    performance and comparing models (§18.7, pp. 624–625). On an i.i.d. test set, model A beats model B
    when Σ log p̃(x; θ_A) − m log Z(θ_A) exceeds the same quantity for B; this requires both partition
    functions, but can be rewritten so that only the **ratio** Z(θ_B)/Z(θ_A) is needed (§18.7, p. 625).
    Report which form was used.
14. **Choose the estimator by the size of D_KL(p₀ ‖ p₁) and audit it.** Estimating Z matters exactly when
    evaluating models, monitoring training and comparing models (§18.7, pp. 624–625). Simple importance
    sampling from a tractable proposal degrades as D_KL(p₀ ‖ p₁) grows — few samples carry significant weight,
    quantified by the **variance of the importance weights**. **Annealed importance sampling (AIS)** is
    described as the most common method for undirected models; **bridge sampling** is more efficient when
    D_KL(p₀ ‖ p₁) is moderate; AIS is too expensive for tracking Z *during* training. The mechanics of each
    estimator, and the in-training tracking workaround, are catalogued in `concept_reconstruction.md` §4.1(d).
    **The book states no upper/lower bound and no bias or consistency result for AIS**, deferring variance and
    efficiency analysis to Neal (2001, as cited) — so the bias direction must be established by the evaluator,
    not assumed (§18.7.1–§18.7.2, pp. 626–632).
15. **Record the one bias direction the book does state.** A compute-economical AIS implementation may
    fail to find several modes of the model distribution and therefore **underestimate Z**, which
    **overestimates** the log-likelihood. The consequence is the trap this SOP exists to avoid: it becomes
    hard to tell whether a high likelihood estimate reflects a good model or a bad AIS implementation
    (§20.14, p. 715).
16. **If the estimator is importance sampling, measure its degeneracy.** When the proposal q is small
    where p·f is large, the variance explodes; such samples are rarely drawn, so the estimate typically
    **underestimates** the target rather than being offset by overestimates, and the book calls this
    endemic in high dimensions (§17.2, pp. 595–596). Report the estimator's variance and the number of
    samples carrying significant weight. Where an unbiased estimator is not required, biased importance
    sampling needs no normalized p or q and is biased but asymptotically unbiased (§17.2, p. 595). Also
    report the Monte Carlo confidence interval built the book's way: empirical mean and variance of
    f(x⁽ⁱ⁾), variance divided by n, approximately normal by the central limit theorem (§17.1.2, p. 593).

### 3.6 Report the variational bound and its gap honestly

17. For latent-variable models trained on a bound, report the **ELBO** and the gap to an independently
    estimated log p(v; θ). L(v, θ, q) = log p(v; θ) − D_KL(q(h|v) ‖ p(h|v; θ)) is a lower bound on
    log p(v), tight if and only if q = p(h|v); inference maximizes L over q and learning maximizes over
    θ; any q gives a valid bound, and a restricted q family or lazy optimization yields looser bounds more
    cheaply (§19.1, p. 635). The importance-weighted autoencoder objective is likewise a lower bound that
    tightens as the number of samples grows (§20.10.3, pp. 697–698).
18. **Attach the book's limitation to every gap you report.** After training, one can estimate
    log p(v; θ) — for example by AIS — and find the gap to L is small, but this certifies accuracy only at
    the **learned** θ. The deeper failure is undetectable this way: if the optimum θ* has a posterior too
    complex for the q-family, learning never reaches θ*, and a small gap at the found θ coexists with
    L(θ*) ≪ log p(θ*). Measuring the true damage would require L(v, θ*, q), i.e. a better learning
    algorithm than the one being audited (§19.4.4, pp. 651–652). Note also that a MAP/Dirac q makes the
    bound infinitely loose (differential entropy → −∞) unless noise is added (§19.3–19.4, pp. 637–638).

### 3.7 Establish whether any MCMC-derived number can be trusted

19. **Burn in, then handle correlation.** Run the chain until equilibrium (磨合); post-equilibrium samples are
    correlated, so either thin by returning every n-th sample or run parallel chains — the book notes
    deep-learning practice uses around 100 chains, comparable to the minibatch size (§17.3, pp. 599–600).
20. **Do not claim mixing.** Mixing time is unknown a priori: theory says the second-largest eigenvalue of the
    transition matrix determines it, but that matrix is exponentially large and inaccessible, and the book
    states plainly that we typically cannot know whether a Markov chain has mixed successfully. Its prescribed
    substitutes are heuristics — run the chain for a crudely sufficient time, then manually inspect samples or
    measure the correlation between successive samples. Report which heuristic was used and what it showed.
    The remedy menu for chains that do not mix (Gibbs/block Gibbs, block updates, tempering and its limitation,
    depth helping mode-hopping) and the symptom picture are in `concept_reconstruction.md` §4.1(d)
    (§§17.3–17.5.2, pp. 596–605).
21. **If the model was trained with persistent chains (SML/PCD), evaluate on a fresh chain initialized at a
    random point.** Training-time negative-phase samples are influenced by recent versions of the model and
    would make the model appear to have more capacity than it actually has. There is no formal test for
    whether chains re-mix between gradient steps; the heuristic symptom is within-step negative-phase sample
    variance exceeding between-chain variance — the book's example is an MNIST model that samples only 7s,
    then only 9s (§18.2, p. 615).

### 3.8 Restrict claims to what the training objective actually supports

22. Read the objective off this table and state the restriction in the report. The mechanics behind each row
    are catalogued in `concept_reconstruction.md` §4.1(d).

| Training objective | What it licenses | What it forbids | Locator |
| --- | --- | --- | --- |
| Pseudolikelihood | Conditional-only tasks such as filling in a few missing values, where it can beat MLE | **Any joint-distribution claim** — density estimation *and sampling* usually perform poorly. Also incompatible with lower-bound approximations, because p̃ sits in a denominator, so a lower bound there yields only an upper bound on the objective and maximizing an upper bound is not meaningful | §18.3, pp. 616–619 |
| Score matching / ratio matching / denoising score matching | A consistent fit **without** Z | Discrete data (it needs derivatives with respect to x); models that admit only lower bounds. The book notes it is used for pretraining the first hidden layer | §18.4–§18.5, pp. 619–621 |
| Noise-contrastive estimation | An **asymptotically consistent** estimator of the original density problem, via binary classification of data against easy noise samples | Treating the learned log p_model as a valid distribution before the extra parameter c ≈ −log Z has converged. Efficiency drops with many random variables, because once basic marginals are learned the classifier rejects nearly all noise samples and learning slows | §18.6, pp. 621–624 |
| Maximum likelihood with intractable Z | Likelihood comparison **only through the Z ratio rule** at step 13, with the estimator's bias direction reported | Reading a high likelihood as a good model when the estimator underestimates Z | §18.7, pp. 624–625; §20.14, p. 715 |
| (Generalized) denoising autoencoder, no sampler | Samples from a Markov chain: corrupt x → x̃, encode h = f(x̃), decode to p(x′|h), sample x′. If the autoencoder is a consistent estimator of the true conditional, the chain's stationary distribution is an implicit consistent estimator of the data distribution; the injected noise level controls mixing and smoothing | Conditional sampling without **clamping** the observed units and without the transition operator satisfying **detailed balance**. The back-propagation-through-training variant (multiple stochastic encode-decode steps from training samples) is equivalent for the stationary distribution but empirically removes spurious modes better | §20.11, pp. 709–712 |

**Modern update (2017–2026) — three added rows.** The five rows above are the 2016 book's objectives and are
unchanged, and step 22's instruction is unchanged: read the objective off the table and state the restriction.
Three modern entries (two diffusion training objectives and flow matching) are added in the same shape and
marked as modern rows so they cannot be mistaken for book entries.

| Training objective | What it licenses | What it forbids | Source |
| --- | --- | --- | --- |
| **Diffusion ELBO** *(modern row)* — a weighted variational bound whose weighting is derived from a connection between diffusion models and denoising score matching; equivalently multi-scale score estimation, with sampling resembling annealed Langevin dynamics | A **lower bound** on the data log-likelihood, and samples. Because "the decoder must do all the work since the encoder has no parameters", the bound is the only likelihood-like quantity available | Reading the bound as an exact likelihood, or comparing it against one without §3.1 step 3a's declaration. A diffusion bound **above** a flow's exact computation is a valid one-sided likelihood ordering on commensurate data — but it says nothing about generation cost, which is a separate axis and must not be inferred from it | `UDL` §18.4.1 fol. 358, §16.5.1 fol. 319 and fn. 2; `DDPM` |
| **Simplified diffusion training (`L_simple`)** *(modern row)* — removes standard ELBO term weighting during training | Better sample quality in `DDPM`'s experiments; its trained model can **separately** be evaluated using the standard variational bound (NLL ≤3.75 bits/dim in Table 1) | Reporting `L_simple` itself as a likelihood bound, or claiming `L_simple` training prevents valid likelihood-bound evaluation | `DDPM` §3.4, §4.1, Table 1 |
| **Flow matching** *(modern row)* — simulation-free training of continuous normalizing flows by regressing vector fields of fixed conditional paths | Samples and tractable CNF log-density evaluation via ODE integration, **subject to numerical solver/trace-estimation error**; report bits/dim and sample-quality metrics jointly | Confusing simulation-free training with ODE-free evaluation/sampling, or treating numerically evaluated likelihood as error-free closed-form likelihood. Flow matching subsumes diffusion paths; it does not replace diffusion models | `FM` |

Boundaries on the modern rows. Every layer of a normalizing flow must be invertible, which is what buys the
exact likelihood and is also the constraint that shapes the architecture; the diffusion and flow literatures
use **opposite nomenclature** for the direction of the forward process, so a quoted direction must be checked
against its own source; and `FM`'s straight-path relative, a separate concurrent-line work on rectified
transport, is **not** folded into the flow-matching row — no concurrency or derivation relationship between
the two was verified, so they are cited as distinct works.

*Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §4.1, §4.2, §4.8.
Sources: `UDL` §16.5.1 fol. 319 and fn. 2, §18.2 fn. 1 fol. 350, §18.4.1 fol. 358, fol. 305; `DDPM`; `FM`;
`RF`.*


## 4. Important failure modes

- **Ranking an estimate against a bound** without knowing the bound's looseness (§20.14, p. 715).
- **Comparing across data types or binarization schemes**, which puts the likelihoods in different spaces
  (§20.14, p. 716).
- **Per-model preprocessing**, which changes the target distribution and the task (§20.14, p. 716).
- **Reading a high likelihood as a good model** when the Z estimator underestimates Z (§20.14, p. 715).
- **Reward hacking via variance collapse** on never-changing pixels (§20.14, p. 717).
- **Trusting visual quality**: very poor models can produce very good samples, and dropped modes are
  undetectable by human inspection at realistic mode counts (§20.14, pp. 716–717).
- **Skipping the nearest-neighbour test** and shipping a model that only copies training examples
  (§20.14, p. 716).
- **Reporting a small ELBO gap as evidence that the variational family is adequate** (§19.4.4,
  pp. 651–652).
- **Evaluating a persistent-chain model with training-time samples**, which inflates apparent capacity
  (§18.2, p. 615).
- **Assuming a chain mixed** because it ran long; no formal test exists (§17.3, p. 600).
- **Reading an importance-sampling estimate as accurate** when the proposal is far from the target; the
  bias direction is toward underestimation and the failure is endemic in high dimensions (§17.2,
  pp. 595–596).
- **Claiming sampling or density-estimation capability from a pseudolikelihood-trained model** (§18.3,
  p. 618).
- **Treating a metric disagreement as a model disagreement** when the two models were designed for
  forward-KL and reverse-KL behaviour respectively (§20.14, p. 717).

Modern-update failure modes (rules in §3.1, §3.4 and §3.8 above):

- **Reading a family ranking off a metric-indexed result.** The modern worked case is the report that
  diffusion-model images were quantitatively superior to GAN images, stated by its own source **in terms of one
  specific sample-quality metric**. Same error as the 2016 forward/reverse-KL item above, different cause: here
  the ranking holds only under the named metric. A ranking that does not name its metric is not a result
  (`delta_map.md` §4.6).
- **Discarding a valid diffusion lower bound that lands above a comparable flow likelihood.** It supports a
  one-sided likelihood conclusion; generation cost is a separate axis and is not inferred from it
  (`delta_map.md` §4.1).
- **Placing an `L_simple` training-loss value on a likelihood axis.** It is not an ELBO; the trained model may
  nevertheless be evaluated with a separately computed standard bound (`delta_map.md` §4.1).
- **Confusing the axis of a likelihood/sample-quality disagreement.** Presenting one instrument's number as
  evidence about the other, or reading every disagreement as a defect — variance collapse is a defect,
  imperceptible-detail codelength is a property of the metric, and step 12's per-dimension variance check is
  what tells them apart (`delta_map.md` §4.3).
- **Declaring an aggregate use for a conditional generator** without naming the attribute axes it will be
  judged on, so a model passes in aggregate while failing counting, colour or spatial relation
  (`delta_map.md` §4.5).
- **Treating flow matching as a replacement for diffusion**, or its simulation-free *training* as
  simulation-free *evaluation* (`delta_map.md` §4.2).

## 5. Outputs and reporting

- The **measured-quantity declaration**: intended use, quantity, and whether each reported number is a
  point estimate, a stochastic estimate or a bound (with the bound's looseness where known).
- The **comparability record**: preprocessing (identical across models, stated), data type, binarization
  scheme, and the shared binarized file if one was used.
- The **sample-quality record**: who inspected the samples and whether they knew provenance, the
  nearest-neighbour test result, and an explicit statement about modes that inspection cannot detect.
- The **likelihood record**: numbers, estimator, estimator settings, the bias direction if known, and the
  ratio-rule form used for cross-model comparison.
- The **variational record**: ELBO, independently estimated log p(v; θ), the gap, and the §19.4.4
  limitation attached to it.
- The **MCMC record**: burn-in length, thinning interval, chain count, which mixing heuristic was applied
  and what it showed, and the fresh-chain statement for persistent-chain models.
- The **objective-capability statement**: what the training objective licenses (joint density, conditional
  only, samples) and what it does not.
- The **standing limitation**: even restricted to their best-suited tasks, all metrics currently in use
  have serious flaws, and designing new measurement techniques is itself a top research topic in
  generative modelling (§20.14, p. 717). Any conclusion is provisional on that.

Modern-update additions to the report (`delta_map.md` §4.1, §4.3, §4.5):

- In the **measured-quantity declaration**, the model family, its **training objective** and the **separate
  evaluation instrument** — a model trained with `L_simple` may still receive a valid ELBO evaluation.
- Where a bound is compared against an exact value from a different family, the **generation cost** of each
  model reported as a separate axis — a valid one-sided likelihood ordering does not license any inference
  about it, and an overall utility claim does require it.
- In the **likelihood record**, an explicit statement of **which axis each number is on**, and — where
  likelihood and sample quality disagree — which of the two explanations is in play: variance collapse
  (a defect) or imperceptible-detail codelength (a property of the metric).
- For a conditional generator, the **attribute-rendering axes** the declared use will be judged on.
- Any family ranking reported, with the **metric it is indexed to** named in the same sentence.

## 6. Source traceability

| Claim or step | Locator |
| --- | --- |
| Comparison is difficult and subtle; only an approximation of log-probability is available; declare what is measured; estimate-vs-bound case; task-based comparison with precision and recall; AIS mode-dropping underestimates Z and inflates likelihood | §20.14, p. 715 |
| Preprocessing must be identical; ×0.1 raises probability tenfold; data-type comparability; binary log-likelihood ≤ 0 vs unbounded real-valued log-density; three binarization schemes give very different likelihoods; sharing binarized files | §20.14, p. 716 |
| Visual inspection by naive subjects (Denton et al., 2015); very poor models can produce very good samples; nearest-neighbour test (Fig. 16.1); simultaneous over- and under-fitting; dropped modes undetectable at scale | §20.14, pp. 716–717 |
| Likelihood computed when feasible; MNIST background-variance reward hacking; cost toward −∞ in any real-valued MLE problem; need for other evaluation methods | §20.14, p. 717 |
| Metric must match intended use; forward vs reverse KL (Fig. 3.6); all current metrics have serious flaws (Theis et al., 2015) | §20.14, p. 717 |
| KL divergence and entropy definitions | §3.13 信息论, pp. 105–109 |
| Why Z must be estimated (evaluation, monitoring, comparison); the ratio comparison rule | §18.7, pp. 624–625 |
| Simple importance sampling for the Z ratio; degradation with large D_KL(p₀‖p₁); variance of importance weights | §18.7, pp. 626–627 |
| AIS: intermediate distributions, MCMC transitions, log-space weights, validity via extended state space, most common method for undirected models, no bound/bias result stated | §18.7.1, pp. 627–630 |
| Bridge sampling, optimal harmonic-mixture bridge, chained importance sampling, in-training Z tracking (Desjardins et al., 2011) | §18.7.2, pp. 631–632 |
| MC estimator basics: unbiasedness, law of large numbers, variance/n, normal approximation and confidence interval | §17.1.2, pp. 591–593 |
| Importance sampling: q-independence of the expectation, q-sensitivity of the variance, optimal q* ∝ p|f| infeasible, biased variant asymptotically unbiased, underestimation endemic in high dimensions | §17.2, pp. 593–596 |
| MCMC: transition operator and stationary distribution, burn-in, correlated samples, thinning, ~100 parallel chains, mixing time inaccessible, "we typically cannot know", manual inspection and successive-sample correlation | §17.3, pp. 596–600 |
| Non-mixing remedies: Gibbs/block Gibbs, block updates, tempering and its limitation, depth helping mode-hopping; nearly identical consecutive DBM samples (Fig. 17.2); GAN ancestral samples independent | §§17.4–17.5.2, pp. 601–605 |
| CD/SML training; fresh-chain evaluation requirement; no formal re-mixing test; within- vs between-chain variance symptom | §18.2, pp. 608–616 (warning at p. 615) |
| Pseudolikelihood definition and cost, asymptotic consistency (Mase, 1995), poor for full-joint tasks incl. sampling, better for conditional tasks, incompatible with lower bounds | §18.3, pp. 616–619 |
| Score/ratio matching: what they estimate, discrete-data and lower-bound incompatibility, first-hidden-layer use | §18.4, pp. 619–621 |
| NCE: binary-classification reformulation, asymptotic consistency, c ≈ −log Z caveat, efficiency loss with many variables, self-contrast | §18.6, pp. 621–624 |
| ELBO definition, lower-bound property, tightness iff q = p(h|v), restricted q ⇒ looser bound; importance-weighted variant tightens with more samples | §19.1, p. 635; §20.10.3, pp. 697–698 |
| Gap-at-learned-θ certifies nothing about θ*; measuring the damage needs a better learner; Dirac q makes the bound infinitely loose | §19.4.4, pp. 651–652; §19.3–19.4, pp. 637–638 |
| Wake-sleep drawback: inference net only sees model-typical v | §19.5.1, pp. 653–654 |
| Sampling from autoencoders: Markov-chain procedure, consistency argument, noise level controls mixing, clamping and detailed balance (Alain et al., 2015), back-propagation through training | §20.11, pp. 709–712 |

**Modern-update provenance.** Every row above is a 2016-book locator and none was altered. Three
modern-update blocks were added — §3.1 steps 3a and 3b, §3.4 step 12, and three added rows plus their
boundaries in §3.8's objective-capability table — along with the matching entries in §4 and §5. Detailed
evidence, verbatim source quotations and the sources' own result figures are **not** reproduced here; they are
recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§4.1, §4.2, §4.3, §4.5, §4.6, §4.8 and in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.2–§2.4. Source keys: `UDL`
§14.3, §16.5.1 and fn. 2, §18.2 fn. 1, §18.4.1, §18.6, ch. 18 Notes; `DDPM`; `FM`; `RF`. The sample-quality
metric block lives in
[`BC-DL-11`](../../Benchmark/Deep-Learning-2016/BC-DL-11-generative-evaluation-integrity.md) §4.M, because
that is where metrics are owned in this package.

**Historical boundary.** Treated as book-era and reported as such: MNIST as the dominant generative
benchmark and the practice of sharing binarized MNIST files; ~100 parallel chains matched to minibatch
size; Gibbs step counts (naive ≈100, CD 1–20, SML 1 for RBMs and 5–50 for DBMs); AIS as the standard
partition-function estimator since Salakhutdinov and Murray (2008); the 2016 verdicts on specific families
(VAE samples "somewhat blurry", DCGAN/LAPGAN on LSUN with LAPGAN fooling human subjects 40% of the time,
moment-matching networks' disappointing samples without autoencoder composition, NADE described as
recently very successful, DBNs beating kernelized SVMs on MNIST). No numeric likelihood or perplexity
values are stated in these sections, so none is invented here; **perplexity is not used as a metric in
this package because the book's generative-model evaluation section does not name it**.

The closing sentence of this note was amended by the modern update. It previously stated that no post-2016
evaluation metric is introduced. That remains true of the 2016 procedure and of this SOP: **no metric is
added here**, because metrics are owned by `BC-DL-11` in this package. What the modern update adds to this SOP
is a family-exactness status, a training-objective restriction, an attribute-axis declaration and a
generation-cost asymmetry — all of them *declaration* requirements of the kind §3.1 already imposed, and none
of them a score. The metric block itself, and the scoping of the 2016 exclusion rule that permits it, are in
`BC-DL-11` §4.M and in `Benchmark/Deep-Learning-2016/README.md` standing rule 6.
