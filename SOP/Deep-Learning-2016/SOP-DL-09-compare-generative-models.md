# SOP-DL-09 — Compare generative models, and decide whether an intractable-likelihood number can be trusted

**Stage:** evaluate · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Produce a comparison between generative models that is not silently invalid. The book frames the problem
directly. Comparing one generative model with another is a difficult and subtle task. Usually one **cannot
actually evaluate the log-probability of data under the model. Only an approximation of that value exists.**
In that situation, the first obligation is to think through and to state clearly *what the reported number
measures* (§20.14, p. 715).

Several duties fall to this SOP:

- the declaration of the measured quantity
- the enforcement of identical preprocessing and of identical data-type handling
- sample-quality assessment, and the known blind spots of that assessment
- likelihood-based comparison, including the partition-function-ratio rule
- an audit of whatever estimator produced log Z
- the ELBO gap as a diagnostic, and the limit of that diagnostic
- MCMC trustworthiness (burn-in, mixing, importance-weight degeneracy, fresh-chain evaluation)

Out of scope:

- the choice of a generative family, or the training of one

The comparison in this SOP ranks no family. The book's own closing position is that the metric must match the
intended use. That position also holds that **all metrics currently in use still have serious flaws**
(§20.14, p. 717).

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

1. **State the intended use.** Some generative models are better at assigning high probability to most real
   points. Other models are better at avoiding high probability on unrealistic points. The book attributes
   that difference to a design choice, namely the divergence that the model minimizes. The choice is between the
   forward and the reverse KL divergence (the book refers to its Fig. 3.6, and to §3.13 信息论 where both are
   defined, pp. 105–109). Which model is "better" is a function of the use, so declare the use first
   (§20.14, p. 717).
2. **State what quantity the measurement reports, and whether the number is an estimate or a bound.** The
   book's worked case names two models. Model A is scored by a *stochastic estimate* of log-likelihood. Model B
   is scored by a *deterministic lower bound*. Suppose A scores higher. Then the question "which is better?"
   has no answer unless a method determines how loose B's bound is (§20.14, p. 715). Never let an estimate and
   a bound share one ranking axis without a report of the bound's looseness.
3. **Use the task-based escape hatch where the use is practical.** If the concern is practical performance,
   compare the models fairly on task-specific criteria. The book's example is anomaly detection. One such
   criterion ranks test cases and reports **precision and recall** (§20.14, p. 715). That comparison sidesteps
   incommensurable likelihoods entirely.

> **Modern update (2017–2026) — two additions to the declaration step.** Steps 1–3 are unchanged. The
> ambiguity in step 2's worked case remains. The first addition supplies a valid one-sided case.
>
> **3a. A lower bound from one family can legitimately outrank an exact likelihood from another.** Step 2
> cautions against one ranking. A higher stochastic estimate ranks above another model's lower bound only with
> further information. A valid lower bound for A can stand **above** B's exact log-likelihood. That case
> establishes a one-sided likelihood ordering on matched data and units. When A's bound falls below B's exact
> value, the ranking stays undecided. The modern families also invite confusion between training and
> evaluation.
>
> - The modern anchor discusses four generative families. **Normalizing flows are the only one that computes
>   the exact log-likelihood.** Test likelihood is ineffective for GANs. Test likelihood is expensive for
>   variational-autoencoder and diffusion models. Test likelihood is exact and efficient only for flows.
>
> - The footnote of that source supplies the case that trips the 2016 rule. The quote reads: "**The lower bound
>   on the likelihood for diffusion models can actually exceed the exact computation in normalizing flows, but
>   data generation is much slower.**" That ordering is a valid one-sided **likelihood** result on commensurate
>   data. The generation-cost asymmetry is a separate axis. Do not fold that asymmetry into the likelihood
>   conclusion. State both facts. Make any overall utility claim only from both.
>
> - Diffusion models train on an ELBO. Within that ELBO, "the decoder must do all the work since the encoder
>   has no parameters." A widely used training objective **drops the variational weighting** from that bound.
>   That objective down-weights the hard small-noise terms. The network then concentrates on the more difficult
>   large-noise ones. The same objective produces the best sample-quality score in its source's experiments.
>   **The training loss and the evaluation instrument are different things.** A model trained with that
>   simplified loss can still receive an evaluation under the standard variational bound. That evaluation
>   result is the number to put on a likelihood axis.
>
> Step 2 also requires three declarations. Identify the model family, the **training objective** and the
> **separate evaluation instrument** (exact likelihood, stochastic estimate or bound). State any valid
> one-sided comparison. Report the generation cost separately whenever the text claims overall practical
> utility.
>
> **3b. A conditional-generation use decomposes into nameable attribute axes.** Step 1 requires the declaration
> of the intended use. For text-conditioned generation, that use is not one axis. Declare **which
> attribute-rendering axes the evaluation scores**. The list holds colour, counting, spatial relation, and
> whatever else the use turns on. A model can satisfy an aggregate score while the model fails one named axis.
>
> Boundary on 3b: the modern anchor names a purpose-built evaluation set for exactly these axes. That set is
> cited here as an *example of the category* (`delta_map.md` §4.5). This SOP requires the declaration of those
> axes. This SOP requires no benchmark, and names none as mandatory.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §4.1, §4.5. Sources:
> `UDL` §14.3 fol. 272, §16.5.1 fol. 319 and fn. 2, §18.4.1 fol. 358, §18.6 fol. 371–372; `DDPM`; `FM`.*

### 3.2 Make the comparison commensurable

4. **Freeze preprocessing across models.** Other areas of machine learning tolerate a per-algorithm change of
   preprocessing. When a study compares object-recognition accuracies, a slightly different preprocessing per
   algorithm is usually acceptable. Generative modelling does not tolerate that difference. Any change to the
   input data changes the distribution that the model must capture. Such a change fundamentally changes the
   task. The book's example: multiplying inputs by 0.1 artificially increases the probability tenfold
   (§20.14, p. 716).
5. **Enforce data-type comparability.** Compare a real-valued model only with real-valued models. Compare a
   binary model only with binary models. Otherwise the measured likelihoods are not in the same space. A
   binary model's log-likelihood is at most zero, while a real-valued log-density is unbounded above (§20.14,
   p. 716).
6. **Enforce identical binarization.** For a binary model, both sides must use exactly the same binarization.
   One scheme is a fixed threshold at 0.5. The other scheme is stochastic binarization. That scheme draws one
   sample per pixel. The same scheme uses the gray value as the probability of a 1. If the scheme is
   stochastic, pick one of two handling rules. First, binarize the whole dataset once. The book notes that
   researchers who share a single random binarization also share the resulting file. Results then do not differ
   by binarization draw. Second, re-draw at every training step, and evaluate over multiple samples. Each of
   these schemes produces **very different likelihood numbers** (§20.14, p. 716).

### 3.3 Assess samples, knowing what the assessment cannot see

7. **Inspect samples.** Ideal practice puts the inspection with naive experimental subjects, not with the
   researchers themselves. Those subjects do not know the provenance of the samples (Denton et al., 2015, as
   cited) (§20.14, p. 716).
8. **Assume the inspection is weak.** A very poor probability model may produce very good-looking samples
   (§20.14, p. 716).
9. **Run the nearest-neighbour test.** For some generated samples, display the Euclidean nearest neighbour of
   each sample in the training set. The book points to its Fig. 16.1. The test aims to detect a model that
   overfits the training set by merely reproducing training instances (§20.14, p. 716).
10. **Account for simultaneous over- and under-fitting.** The book's example is a model trained on dog and cat
    images. That model simply learns to reproduce the dog training images. That model clearly overfits, because
    it cannot produce images outside the training set. That model also underfits, because it assigns no
    probability to the cat images. Yet a human observer will judge every individual dog image high quality. In
    this simple case, an observer who inspects many samples easily notices the absence of cats. In a realistic
    setting the model may train on data with tens of thousands of modes. The model can then drop a few modes.
    Human observers cannot inspect or remember enough images to detect the missing variation (§20.14,
    pp. 716–717).

### 3.4 Compute likelihood, and check for reward hacking

11. **Compute test-set log-likelihood when that computation is feasible.** The precise reason for the step is
    that visual sample quality is not a reliable criterion (§20.14, p. 717).
12. **Check the variance-collapse failure.** A real-valued MNIST model can assign arbitrarily low variance to
    background pixels that never change. That model thereby earns arbitrarily high likelihood. The possibility
    of driving the cost toward −∞ exists in **any** real-valued maximum-likelihood problem. The possibility is
    especially severe for MNIST generation, because many output values need no prediction at all. The book
    draws the conclusion explicitly. That state of affairs strongly indicates that the field needs other ways
    to evaluate generative models (§20.14, p. 717).

> **Modern update (2017–2026) — the likelihood/sample-quality disagreement has a named mechanism.** Steps 8 and
> 11 stand. A very poor probability model may produce very good-looking samples. Compute the likelihood where
> the computation is feasible. The modern literature supplies the mirror case. The mirror case is a model with
> state-of-the-art sample quality. That model concedes uncompetitive log-likelihoods. The same literature
> explains the concession by spending lossless codelength on distortions that no observer can perceive. So the
> two instruments can move in opposite directions, for reasons that are **not** either instrument failing. The
> result figures of that source are in `delta_map.md` §4.3. This SOP does not restate those figures.
>
> The addition changes practice in three ways. The addition applies to steps 8 and 11, and does not replace
> those steps.
>
> - **Report which axis a number is on.** A bits-per-dim figure and a sample-quality score are not two
>   readings of one underlying quality. Report both numbers. Label each number. Never present one number as
>   evidence about the other.
>
> - **When the two instruments disagree, investigate rather than assign a cause from the scores alone.** Step
>   12's per-dimension variance check can reveal variance-collapse reward hacking. Imperceptible-detail
>   codelength is another documented explanation for weak likelihood despite good samples. The absence of
>   variance collapse does not by itself prove that the second explanation applies.
>
> - **The disagreement is not a licence to drop likelihood.** The flow-matching source reports bits/dim and a
>   sample-quality score jointly. That source disputes neither number. Nothing in this lineage's sources
>   declares bits-per-dim an inappropriate metric. This SOP searched for that stronger claim, and did **not
>   find** that claim in this lineage's sources.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §4.3, §4.2. Sources:
> `DDPM` (§3.4, §4.1 and Table 1; verbatim quotes in `sources.md` §2.3); `FM`.*

### 3.5 Compare through the partition function when the likelihood is intractable

13. **Use the ratio rule.** The estimate of Z matters exactly when one evaluates models, monitors training
    performance and compares models (§18.7, pp. 624–625). On an i.i.d. test set, model A beats model B when
    Σ log p̃(x; θ_A) − m log Z(θ_A) exceeds the same quantity for B. That form needs both partition functions.
    A rewrite needs only the **ratio** Z(θ_B)/Z(θ_A) (§18.7, p. 625). Report which form the work used.
14. **Choose the estimator by the size of D_KL(p₀ ‖ p₁).** Then audit that estimator. The estimate of Z matters
    exactly when one evaluates models, monitors training and compares models (§18.7, pp. 624–625). A simple
    importance-sampling estimate from a tractable proposal degrades as D_KL(p₀ ‖ p₁) grows. Few samples then
    carry significant weight, and the **variance of the importance weights** quantifies that loss. The book
    describes **annealed importance sampling (AIS)** as the most common method for undirected models. **Bridge
    sampling** is more efficient when D_KL(p₀ ‖ p₁) is moderate. AIS is too expensive for tracking Z *during*
    training. `concept_reconstruction.md` §4.1(d) catalogues the mechanics of each estimator, and the
    in-training tracking workaround. **The book states no upper/lower bound and no bias or consistency result
    for AIS.** The book defers the variance and the efficiency analysis to Neal (2001, as cited). The evaluator
    must therefore establish the bias direction, not assume that direction (§18.7.1–§18.7.2, pp. 626–632).
15. **Record the one bias direction the book does state.** A compute-economical AIS implementation may fail to
    find several modes of the model distribution, and therefore **underestimate Z**. That error
    **overestimates** the log-likelihood. The consequence is the trap this SOP exists to avoid. One cannot
    easily tell whether a high likelihood estimate reflects a good model or a bad AIS implementation (§20.14,
    p. 715).
16. **If the estimator is importance sampling, measure the degeneracy of that estimator.** When the proposal q
    is small where p·f is large, the variance explodes. The sampler draws such samples rarely. The estimate
    therefore typically **underestimates** the target, with no offset from overestimates. The book calls that
    failure endemic in high dimensions (§17.2, pp. 595–596). Report the variance of the estimator, and the
    number of samples that carry significant weight. Where the work needs no unbiased estimator, a biased
    importance-sampling estimator needs no normalized p or q. That estimator is biased, but is asymptotically
    unbiased (§17.2, p. 595). Also report the confidence interval of the Monte Carlo estimate, built the book's
    way. That interval uses:
    - the empirical mean and the variance of f(x⁽ⁱ⁾)
    - the variance divided by n
    - an approximate normal form, from the central limit theorem (§17.1.2, p. 593)

### 3.6 Report the variational bound and its gap honestly

17. For a latent-variable model trained on a bound, report the **ELBO**. Also report the gap between the ELBO
    and an independently estimated log p(v; θ). The quantity L(v, θ, q) = log p(v; θ) − D_KL(q(h|v) ‖
    p(h|v; θ)) is a lower bound on log p(v). The bound is tight if and only if q = p(h|v). Inference maximizes
    L over q, and learning maximizes L over θ. Any q gives a valid bound. A restricted q family, or lazy
    optimization, yields looser bounds more cheaply (§19.1, p. 635). The importance-weighted autoencoder
    objective is likewise a lower bound. That bound tightens as the number of samples grows (§20.10.3,
    pp. 697–698).
18. **Attach the book's limitation to every gap you report.** After training, one can estimate log p(v; θ), for
    example by AIS. That estimate may show a small gap to L. The small gap certifies accuracy only at the
    **learned** θ. A deeper failure stays undetectable in that way. If the optimum θ* has a posterior too
    complex for the q-family, learning never reaches θ*. Then a small gap at the found θ coexists with
    L(θ*) ≪ log p(θ*). A measurement of the true damage would require L(v, θ*, q). That measurement needs a
    better learning algorithm than the algorithm under audit (§19.4.4, pp. 651–652). Note also that a
    MAP/Dirac q makes the bound infinitely loose (differential entropy → −∞), unless the method adds noise
    (§19.3–19.4, pp. 637–638).

### 3.7 Establish whether any MCMC-derived number can be trusted

19. **Burn in, then handle correlation.** Run the chain until equilibrium (磨合). The samples after equilibrium
    are correlated. Thin the sample set by returning every n-th sample. Or run parallel chains. The book notes
    that deep-learning practice uses around 100 chains, comparable to the minibatch size (§17.3,
    pp. 599–600).
20. **Do not claim mixing.** The mixing time is unknown a priori. Theory says that the second-largest
    eigenvalue of the transition matrix determines the mixing time. That matrix is exponentially large and out
    of reach. The book states plainly that one typically cannot know whether a Markov chain mixes
    successfully. The prescribed substitutes are heuristics. Run the chain for a crudely sufficient time. Then
    inspect the samples by hand, or measure the correlation between successive samples. Report which heuristic
    the work used, and what that heuristic showed. `concept_reconstruction.md` §4.1(d) holds the remedy menu
    for chains that do not mix (Gibbs/block Gibbs, block updates, tempering and its limitation, depth helping
    mode-hopping). That section also holds the symptom picture (§§17.3–17.5.2, pp. 596–605).
21. **If training used persistent chains (SML/PCD), evaluate on a fresh chain, started at a random point.**
    Recent versions of the model influence the training-time negative-phase samples. Those samples would make
    the model appear to have more capacity than the model actually has. No formal test exists for whether
    chains re-mix between gradient steps. The heuristic symptom is a within-step negative-phase sample variance
    that exceeds the between-chain variance. The book's example is an MNIST model that samples only 7s, then
    only 9s (§18.2, p. 615).

### 3.8 Restrict claims to what the training objective actually supports

22. Read the objective off this table. Then state the restriction in the report.
    `concept_reconstruction.md` §4.1(d) catalogues the mechanics behind each row.

| Training objective | What it licenses | What it forbids | Locator |
| --- | --- | --- | --- |
| Pseudolikelihood | Conditional-only tasks such as filling in a few missing values, where it can beat MLE | **Any joint-distribution claim** — density estimation *and sampling* usually perform poorly. Also incompatible with lower-bound approximations, because p̃ sits in a denominator, so a lower bound there yields only an upper bound on the objective and maximizing an upper bound is not meaningful | §18.3, pp. 616–619 |
| Score matching / ratio matching / denoising score matching | A consistent fit **without** Z | Discrete data (it needs derivatives with respect to x); models that admit only lower bounds. The book notes it is used for pretraining the first hidden layer | §18.4–§18.5, pp. 619–621 |
| Noise-contrastive estimation | An **asymptotically consistent** estimator of the original density problem, via binary classification of data against easy noise samples | Treating the learned log p_model as a valid distribution before the extra parameter c ≈ −log Z has converged. Efficiency drops with many random variables, because once basic marginals are learned the classifier rejects nearly all noise samples and learning slows | §18.6, pp. 621–624 |
| Maximum likelihood with intractable Z | Likelihood comparison **only through the Z ratio rule** at step 13, with the estimator's bias direction reported | Reading a high likelihood as a good model when the estimator underestimates Z | §18.7, pp. 624–625; §20.14, p. 715 |
| (Generalized) denoising autoencoder, no sampler | Samples from a Markov chain: corrupt x → x̃, encode h = f(x̃), decode to p(x′|h), sample x′. If the autoencoder is a consistent estimator of the true conditional, the chain's stationary distribution is an implicit consistent estimator of the data distribution; the injected noise level controls mixing and smoothing | Conditional sampling without **clamping** the observed units and without the transition operator satisfying **detailed balance**. The back-propagation-through-training variant (multiple stochastic encode-decode steps from training samples) is equivalent for the stationary distribution but empirically removes spurious modes better | §20.11, pp. 709–712 |

**Modern update (2017–2026) — three added rows.** The five rows above are the 2016 book's objectives, and are
unchanged. Step 22's instruction is unchanged. Read the objective off the table, and state the restriction.
Three modern entries are added in the same shape. Those entries cover two diffusion training objectives and
flow matching. Each entry carries a modern-row mark, so no reader can mistake a modern row for a book row.

| Training objective | What it licenses | What it forbids | Source |
| --- | --- | --- | --- |
| **Diffusion ELBO** *(modern row)* — a weighted variational bound whose weighting is derived from a connection between diffusion models and denoising score matching; equivalently multi-scale score estimation, with sampling resembling annealed Langevin dynamics | A **lower bound** on the data log-likelihood, and samples. Because "the decoder must do all the work since the encoder has no parameters", the bound is the only likelihood-like quantity available | Reading the bound as an exact likelihood, or comparing it against one without §3.1 step 3a's declaration. A diffusion bound **above** a flow's exact computation is a valid one-sided likelihood ordering on commensurate data — but it says nothing about generation cost, which is a separate axis and must not be inferred from it | `UDL` §18.4.1 fol. 358, §16.5.1 fol. 319 and fn. 2; `DDPM` |
| **Simplified diffusion training (`L_simple`)** *(modern row)* — removes standard ELBO term weighting during training | Better sample quality in `DDPM`'s experiments; its trained model can **separately** be evaluated using the standard variational bound (NLL ≤3.75 bits/dim in Table 1) | Reporting `L_simple` itself as a likelihood bound, or claiming `L_simple` training prevents valid likelihood-bound evaluation | `DDPM` §3.4, §4.1, Table 1 |
| **Flow matching** *(modern row)* — simulation-free training of continuous normalizing flows by regressing vector fields of fixed conditional paths | Samples and tractable CNF log-density evaluation via ODE integration, **subject to numerical solver/trace-estimation error**; report bits/dim and sample-quality metrics jointly | Confusing simulation-free training with ODE-free evaluation/sampling, or treating numerically evaluated likelihood as error-free closed-form likelihood. Flow matching subsumes diffusion paths; it does not replace diffusion models | `FM` |

Boundaries on the modern rows: every layer of a normalizing flow must be invertible. That invertibility buys
the exact likelihood, and is also the constraint that shapes the architecture. The diffusion and the flow
literatures use **opposite nomenclature** for the direction of the forward process. Check a quoted direction
against its own source. `FM`'s straight-path relative is a separate, concurrent-line work on rectified
transport. This SOP does **not** fold that work into the flow-matching row. No one verified a concurrency or a
derivation relationship between the two works. This SOP therefore cites the two works as distinct works.

*Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §4.1, §4.2, §4.8.
Sources: `UDL` §16.5.1 fol. 319 and fn. 2, §18.2 fn. 1 fol. 350, §18.4.1 fol. 358, fol. 305; `DDPM`; `FM`;
`RF`.*


## 4. Important failure modes

- **Ranking an estimate against a bound** without knowledge of the bound's looseness (§20.14, p. 715).
- **Comparing across data types or binarization schemes**. That comparison puts the likelihoods in different
  spaces (§20.14, p. 716).
- **Per-model preprocessing**. That preprocessing changes the target distribution and the task (§20.14,
  p. 716).
- **Reading a high likelihood as a good model** when the Z estimator underestimates Z (§20.14, p. 715).
- **Reward hacking via variance collapse** on never-changing pixels (§20.14, p. 717).
- **Trusting visual quality.** Very poor models can produce very good samples. At realistic mode counts, human
  inspection cannot detect dropped modes (§20.14, pp. 716–717).
- **Skipping the nearest-neighbour test**, and shipping a model that only copies training examples (§20.14,
  p. 716).
- **Reporting a small ELBO gap as evidence that the variational family is adequate** (§19.4.4,
  pp. 651–652).
- **Evaluating a persistent-chain model with training-time samples**. Those samples inflate the apparent
  capacity (§18.2, p. 615).
- **Assuming a chain mixed** because the chain ran long. No formal test exists (§17.3, p. 600).
- **Reading an importance-sampling estimate as accurate** when the proposal is far from the target. The bias
  direction goes toward underestimation, and the failure is endemic in high dimensions (§17.2,
  pp. 595–596).
- **Claiming sampling or density-estimation capability from a pseudolikelihood-trained model** (§18.3,
  p. 618).
- **Treating a metric disagreement as a model disagreement.** The two models were designed for forward-KL and
  reverse-KL behaviour respectively (§20.14, p. 717).

Modern-update failure modes (rules in §3.1, §3.4 and §3.8 above):

- **Reading a family ranking off a metric-indexed result.** The modern worked case reports that
  diffusion-model images were quantitatively superior to GAN images. The source of that report states the
  result **in terms of one specific sample-quality metric**. That is the same error as the 2016
  forward/reverse-KL item above, but a different cause. Here the ranking holds only under the named metric. A
  ranking that does not name its metric is not a result (`delta_map.md` §4.6).
- **Discarding a valid diffusion lower bound that lands above a comparable flow likelihood.** Such a bound
  supports a one-sided likelihood conclusion. Generation cost is a separate axis. No one infers that cost from
  the likelihood result (`delta_map.md` §4.1).
- **Placing an `L_simple` training-loss value on a likelihood axis.** That value is not an ELBO. A separately
  computed standard bound can nevertheless evaluate the trained model (`delta_map.md` §4.1).
- **Confusing the axes of likelihood and sample quality, or assigning a cause from their disagreement alone.**
  Step 12's per-dimension variance check can identify one failure mode. That check cannot by itself establish
  that imperceptible-detail codelength is the alternative explanation (`delta_map.md` §4.3).
- **Declaring an aggregate use for a conditional generator**, without naming the attribute axes that the
  evaluation scores. A model then passes in aggregate, while the model fails counting, colour or spatial
  relation (`delta_map.md` §4.5).
- **Treating flow matching as a replacement for diffusion**, or treating its simulation-free *training* as
  simulation-free *evaluation* (`delta_map.md` §4.2).

## 5. Outputs and reporting

- Keep the **measured-quantity declaration**: intended use, quantity, and whether each reported number is a
  point estimate, a stochastic estimate or a bound. Give the looseness of a bound where that is known.
- Keep the **comparability record**: preprocessing (identical across models, stated), data type, binarization
  scheme, and the shared binarized file where the work used one.
- Keep the **sample-quality record**: who inspected the samples, and whether those inspectors knew the
  provenance. Record the nearest-neighbour test result. State explicitly the modes that inspection cannot
  detect.
- Keep the **likelihood record**. Record the numbers, the estimator and the settings of the estimator. Record
  the bias direction where that direction is known. Record the ratio-rule form used for cross-model
  comparison.
- Keep the **variational record**: the ELBO, the independently estimated log p(v; θ), the gap, and the §19.4.4
  limitation attached to that gap.
- Keep the **MCMC record**: the burn-in length, the thinning interval, and the chain count. Also record the
  mixing heuristic that the work applied, and what that heuristic showed. Also record the fresh-chain statement
  for persistent-chain models.
- Keep the **objective-capability statement**: what the training objective licenses (joint density, conditional
  only, samples) and what that objective does not license.
- Keep the **standing limitation**. Even restricted to their best-suited tasks, all metrics currently in use
  have serious flaws. The design of new measurement techniques is itself a top research topic in generative
  modelling (§20.14, p. 717). Any conclusion is provisional on that fact.

The modern update adds the items below to the report (`delta_map.md` §4.1, §4.3, §4.5):

- In the **measured-quantity declaration**, name the model family, its **training objective** and the
  **separate evaluation instrument**. A model trained with `L_simple` may still receive a valid ELBO
  evaluation.
- Where one family's bound meets another family's exact value, report the **generation cost** of each model on
  its own axis. A valid one-sided likelihood ordering licenses no inference about that cost. A claim of overall
  utility does require that cost.
- In the **likelihood record**, state **which axis each number is on**. Where likelihood and sample quality
  disagree, also state which diagnostic checks ran, and which explanations remain supported. Where variance
  collapse or imperceptible-detail codelength applies, include that explanation.
- For a conditional generator, name the **attribute-rendering axes** that the declared use scores.
- Report any family ranking, and name **the metric that indexes the ranking** in the same sentence.

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

**Modern-update provenance.** Every row above is a 2016-book locator, and none was altered. The modern update
adds three blocks, along with the matching entries in §4 and §5:

- §3.1 steps 3a and 3b
- §3.4 step 12
- three added rows, plus their boundaries, in §3.8's objective-capability table

The detailed evidence, the verbatim source quotations and the sources' own result figures do **not** appear
here. Those records live in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§4.1, §4.2, §4.3, §4.5, §4.6 and §4.8. The same records also live in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.2–§2.4.

The source keys sit with those records. One key is `UDL` §14.3, §16.5.1 and fn. 2, §18.2 fn. 1, §18.4.1, §18.6
and ch. 18 Notes. The other keys are `DDPM`, `FM` and `RF`.

The sample-quality metric block lives in
[`BC-DL-11`](../../Benchmark/Deep-Learning-2016/BC-DL-11-generative-evaluation-integrity.md) §4.M. That block
belongs there, because that file owns metrics in this package.

**Historical boundary.** The items below are treated as book-era, and are reported as such:

- MNIST as the dominant generative benchmark, and the practice of sharing binarized MNIST files
- ~100 parallel chains, matched to the minibatch size
- Gibbs step counts (naive ≈100, CD 1–20, SML 1 for RBMs and 5–50 for DBMs)
- AIS as the standard partition-function estimator since Salakhutdinov and Murray (2008)
- the 2016 verdicts on specific families (VAE samples "somewhat blurry", DCGAN/LAPGAN on LSUN with LAPGAN
  fooling human subjects 40% of the time, moment-matching networks' disappointing samples without
  autoencoder composition, NADE described as recently very successful, DBNs beating kernelized SVMs on MNIST)

No numeric likelihood value and no perplexity value appears in these sections, so this SOP invents none.
**Perplexity is not used as a metric in this package, because the book's generative-model evaluation section
does not name it**.

The modern update amended the closing sentence of this note. That sentence previously stated that no post-2016
evaluation metric enters the file. That claim remains true of the 2016 procedure and of this SOP. **This SOP
adds no metric**, because `BC-DL-11` owns metrics in this package.

The modern update adds these items to this SOP:

- a family-exactness status
- a training-objective restriction
- an attribute-axis declaration
- a generation-cost asymmetry

Each item is a *declaration* requirement of the kind §3.1 already imposed. None of these items is a score.
`BC-DL-11` §4.M holds the metric block itself, and the scoping of the 2016 exclusion rule that permits that
block. `Benchmark/Deep-Learning-2016/README.md` standing rule 6 holds the same scoping.
