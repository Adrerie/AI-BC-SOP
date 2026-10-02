# BC-DL-11 — Generative-model comparison: is the measured quantity comparable, and does likelihood track sample quality?

**Tests:** the commensurability failures and the likelihood/sample-quality dissociation the book documents ·
**Executed by:** [`SOP-DL-09`](../../SOP/Deep-Learning-2016/SOP-DL-09-compare-generative-models.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The capability under test is **evaluation integrity for generative models**: whether a reported comparison is
measuring what it claims. The book's premise is that usually the log-probability of data under the model
cannot actually be evaluated — only an approximation of it can — so the first obligation is to think through
and communicate clearly what is being measured (§20.14, p. 715). Seven specific failure modes are tested:

| Arm | Claim under test | Locator |
| --- | --- | --- |
| a | A stochastic **estimate** and a deterministic **lower bound** cannot be ranked against each other: if model A's estimate exceeds model B's bound, "which is better?" is unanswerable unless the looseness of B's bound is known | §20.14, p. 715 |
| b | A compute-economical AIS run may fail to find several modes of the model distribution and **underestimate Z**, which **overestimates** the log-likelihood, so a high likelihood may reflect a bad estimator rather than a good model | §20.14, p. 715 |
| c | Preprocessing must be identical across models: any change to the inputs changes the distribution being captured and fundamentally changes the task — multiplying inputs by 0.1 artificially increases the probability tenfold | §20.14, p. 716 |
| d | Real-valued models may be compared only with real-valued models and binary with binary, because binary log-likelihood is at most zero while a real-valued log-density is unbounded above; and the three binarization schemes (fixed 0.5 threshold; one stochastic binarization of the whole dataset; re-sampling per training step) produce **very different likelihood numbers** | §20.14, p. 716 |
| e | Visual sample quality is not a reliable criterion: a very poor probability model can produce very good-looking samples; the nearest-neighbour test detects a model that merely copies training examples; and a model can simultaneously overfit and underfit while producing individually good samples, with dropped modes undetectable by human inspection at realistic mode counts | §20.14, pp. 716–717 |
| f | Likelihood can fail to measure anything we care about: a real-valued model can assign arbitrarily low variance to never-changing background pixels and earn arbitrarily high likelihood — reward hacking that exists in any real-valued maximum-likelihood problem and is especially severe where many output values need not be predicted | §20.14, p. 717 |
| g | A small ELBO gap at the **learned** θ certifies nothing about the variational family's adequacy: if the optimum θ* has a posterior too complex for the q-family, learning never reaches θ*, and a small gap at the found θ coexists with a large gap at θ* | §19.4.4, pp. 651–652 |

Two further integrity conditions are tested as part of the protocol:

| Arm | Claim | Locator |
| --- | --- | --- |
| h | A model trained with persistent chains must be evaluated on a **fresh chain initialized at a random point**; training-time negative-phase samples are influenced by recent model versions and would make the model appear to have more capacity than it actually has | §18.2, p. 615 |
| i | Importance sampling degenerates when the proposal is small where the target times the function is large: few samples carry significant weight, the estimate typically **underestimates**, and the failure is endemic in high dimensions | §17.2, pp. 595–596 |

## 2. Data and comparison conditions

- **Fixed corpus with declared data type.** One real-valued treatment and one binarized treatment of the same
  corpus, each with all three binarization schemes run separately (arm d). The book notes that researchers
  using a single random binarization share the resulting file so that results do not differ by binarization
  draw (§20.14, p. 716).
- **Model arms spanning likelihood regimes**: a model with a tractable likelihood; a model whose likelihood is
  available only as a lower bound (a latent-variable model trained on an ELBO); and a model scored by a
  stochastic estimate of log-likelihood (arm a).
- **Z-estimator arms**: AIS at a compute-economical setting and at a generous setting, to expose arm b's
  mode-dropping; and, where applicable, bridge sampling, which the book describes as more efficient than AIS
  when the divergence between proposal and target is moderate (§18.7.2, p. 631).
- **Preprocessing arms**: the identical model evaluated on inputs scaled by 0.1 and on unscaled inputs
  (arm c).
- **Sample-quality arms**: visual inspection by subjects who do not know the samples' provenance, versus
  inspection by the researchers; plus the nearest-neighbour test — for some generated samples, display their
  Euclidean nearest neighbour in the training set (arm e). Include a deliberately poor model that reproduces
  training examples, and a model that reproduces one mode well while assigning no probability to another
  (the book's dog-and-cat example).
- **Reward-hacking arm**: a real-valued model free to learn per-dimension variance on a corpus with
  near-constant regions (arm f).
- **Variational arm**: a latent-variable model where log p(v; θ) can be independently estimated, so the gap
  can be measured at the learned θ (arm g).
- **Persistent-chain arm**: a model trained with stochastic maximum likelihood or persistent contrastive
  divergence, evaluated both on training-time chains and on fresh randomly-initialized chains (arm h).
- **Importance-sampling arm**: proposals at several divergences from the target, with the variance of the
  importance weights recorded (arm i).

## 3. Baselines

- The tractable-likelihood model is the reference against which bound-based and estimate-based scores are
  declared incommensurable (arm a).
- The generous AIS setting is the reference against which the compute-economical setting is compared (arm b).
- The unscaled-input run is the reference for arm c.
- For arm d, each binarization scheme is its own reference; cross-scheme comparison is disallowed.
- For arm e, the training set itself is the nearest-neighbour reference.
- For arm h, the fresh-chain evaluation is the reference and the training-chain evaluation is the
  contamination being measured.

## 4. Metrics

1. **The declared measured quantity**: for every reported number, whether it is a point value, a stochastic
   estimate or a bound, and — for a bound — its looseness where known (§20.14, p. 715).
2. **Test log-likelihood**, with the Z estimator, its settings and its bias direction where known.
3. **log Z estimate and the variance of the importance weights** (§18.7, pp. 626–627; §17.2, pp. 595–596).
4. **Sample-quality instruments**: provenance-blind inspection outcome, and the nearest-neighbour distance
   distribution between generated samples and the training set (§20.14, p. 716).
5. **Per-dimension variance** in the reward-hacking arm, and the resulting likelihood, to expose the
   variance-collapse failure (§20.14, p. 717).
6. **ELBO, independently estimated log p(v; θ), and the gap** (§19.1, p. 635; §19.4.4, pp. 651–652).
7. **Task-based metrics where the intended use is practical**: ranking test cases and reporting precision and
   recall, which the book offers as the fair way to compare models when practical use is the concern
   (§20.14, p. 715).
8. **Chain diagnostics for arm h**: within-step negative-phase sample variance versus between-chain variance,
   which the book names as the heuristic symptom of chains that have not re-mixed (§18.2, p. 615).
9. **Mixing diagnostics for any MCMC-derived number**: the book states that mixing time is unknown a priori and
   that we typically cannot know whether a chain has mixed successfully; the prescribed substitutes are
   manual inspection of samples and measuring the correlation between successive samples (§17.3, p. 600).

The book gives no numeric thresholds here — no perplexity target, no nearest-neighbour distance bound, no
acceptable ELBO gap. None is invented; every threshold used must be declared by the evaluator.

> ### 4.M Modern-update metric block (2017–2026)
>
> Metrics 1–9 above are quantities the 2016 book names, and none was altered. This package's standing rule 5
> excludes post-2016 metrics from the 2016 text, and that exclusion still governs metrics 1–9. The rule is
> **scoped** here rather than broken: three later metrics now have an anchor-textbook source that states each
> one's failure modes, so they can be admitted on the same terms as the 2016 quantities — named by a source,
> with no invented threshold — provided they are never a bare ranking axis, which is what the rule was
> protecting against.
>
> Each entry below carries the failure modes its own source states. They are not optional commentary: a metric
> from this block reported without its failure modes is out of specification for this benchmark.
>
> 10. **Inception score** *(modern)* — a sample-quality score computed from a pretrained classifier's outputs
>     on generated samples. Its source states three failure modes, all of which must be reported alongside any
>     value: it is "only sensible for" datasets with the label structure of the ImageNet database; it is
>     "sensitive to the particular classification model; retraining this model can give quite different
>     numerical results"; and it "does not reward diversity within an object class; it returns a high value if
>     the model only generates one realistic example of each class". The third is a reward-hacking path of
>     exactly the kind metric 5 exists to expose, so the two must be read together.
> 11. **Fréchet inception distance** *(modern)* — a distance between the feature distributions of generated and
>     real samples. It is computed on the **deepest activations** of a pretrained classifier, so the comparison
>     is semantic and "any information discarded by the network does not contribute to the result". Report
>     which network and which layer produced the features: the number is indexed to that choice, and a
>     different classifier gives a different quantity.
> 12. **Manifold precision and recall** *(modern)* — a two-number decomposition obtained by approximating each
>     distribution's manifold with k-nearest-neighbour hyperspheres in classifier feature space. Its source
>     states the reason it exists: the Fréchet inception distance "is sensitive both to the realism of the
>     samples and their diversity but does not distinguish between these factors". Where a single distance is
>     used to make a claim about *either* realism or diversity, this pair is the instrument that separates
>     them, and the k used must be declared.
>
> Three rules govern this block, and they are what keep it inside the package's standing rules rather than
> around them:
>
> - **Every metric is a quantity a source names.** The anchor textbook defines all three and states each one's
>   limitations. Nothing here is introduced to fill a template field, which is the test standing rule 2 of this
>   package's README applies to the 2016 metrics.
> - **No threshold is invented.** As with metrics 1–9, the source supplies no acceptable value for any of the
>   three. Comparisons are **orderings**, and the absolute value comes from the run.
> - **Never a bare axis.** Metric 10's classifier sensitivity and metric 11's layer dependence make both
>   numbers indexed to a measurement setup, so a value reported without that setup is not a measurement. Where
>   tractable likelihood evaluation is available — the modern anchor identifies normalizing flows among its
>   four families (CNFs require numerical integration) — metric 2 remains primary and this block supplements it.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §4.4. Source: `UDL`
> §14.3, fol. 272–275 (citing Kynkäänniemi et al. 2019 for manifold precision and recall). The token `FID`
> does not occur in the chapters read; the metric is named there in full as "Fréchet inception distance", and
> that is the name used here (`sources.md` §2.5).*

## 5. How to interpret failure

- **Arm a: a stochastic estimate exceeds another model's lower bound** ⇒ the ranking remains uncertain
  unless the bound's looseness and estimator uncertainty are resolved. In the reverse case, a **valid lower
  bound above a comparable exact log-likelihood** establishes a one-sided likelihood ordering.
- **Arm b: the cheap AIS run gives a higher likelihood** ⇒ mode-dropping is the likely cause, since
  underestimating Z overestimates the likelihood; the high score is not evidence of a better model.
- **Arm c: likelihood changes under input rescaling** ⇒ expected, and the point of the arm: the two runs are
  not solving the same task.
- **Arm d: likelihoods differ across binarization schemes** ⇒ expected; cross-scheme comparison is
  meaningless, and a binary model must not be compared with a real-valued one at all.
- **Arm e: good-looking samples from a poor model** ⇒ the book's stated outcome; visual quality alone cannot
  rank models. If the nearest-neighbour distances are small, the model is copying training examples. If a
  mode is missing, note that human inspection cannot reliably detect dropped modes at realistic mode counts.
- **Arm f: likelihood rises while per-dimension variance on constant regions collapses** ⇒ reward hacking, not
  improvement. This is the book's argument that other evaluation methods are needed.
- **Arm g: small gap at the learned θ** ⇒ the audit is incomplete by construction; measuring the true damage
  would require the bound at the unreachable θ*, i.e. a better learning algorithm than the one being audited.
- **Arm h: training-chain evaluation looks better than fresh-chain** ⇒ the contamination the book predicts;
  report only the fresh-chain number.
- **Arm i: the estimate improves when the proposal moves closer to the target** ⇒ consistent with weight
  degeneracy; report the weight variance and the direction of the bias (toward underestimation).
- **Any arm where a pseudolikelihood-trained model is asked to sample or estimate density** ⇒ out of scope for
  that objective: the book states pseudolikelihood usually performs poorly for tasks needing the full joint,
  which includes sampling, while it can beat maximum likelihood for conditional-only tasks such as filling in
  a few missing values (§18.3, p. 618).

> **Modern update (2017–2026) — three interpretation rules, no change to any arm.** The bullets above stand,
> and no arm, baseline or comparison condition was added.
>
> - **Arm e's outcome now has a documented instance in the opposite direction.** Arm e tests the book's claim
>   that a very poor probability model may produce very good-looking samples. The modern literature supplies the
>   mirror case, from the first widely cited diffusion-model paper: state-of-the-art sample-quality scores
>   alongside the concession that "despite their sample quality, our models do not have competitive log
>   likelihoods compared to other likelihood-based models", explained by a coding argument — "more than half of
>   the lossless codelength describes imperceptible distortions". Its own numbers make the disagreement
>   concrete on one test set: a strong likelihood-based autoregressive baseline at 3.03 bits/dim, the diffusion
>   model's full variational bound at ≤3.70, and the simplified objective that produced the best sample-quality
>   score at ≤3.75 — the **model trained with** the simplified objective still receives a separately
>   evaluated standard variational NLL bound (`DDPM` §4.1, Table 1). The training objective, not that
>   likelihood-bound evaluation, is the quantity that deviates from the standard bound. So a
>   likelihood/sample-quality disagreement is **not by itself** evidence that either instrument failed. Arm e's
>   reading still requires the nearest-neighbour check and the dropped-mode caveat; the modern instance adds a
>   third possibility to distinguish — that the model is spending description length on detail no observer can
>   see, which is a property of the metric rather than a defect in the model.
> - **Which kind of disagreement is in play must be named.** Arm f's variance collapse is a defect: the
>   likelihood is earned dishonestly by assigning arbitrarily low variance to never-changing pixels. The
>   imperceptible-detail case is not a defect. Both produce a good likelihood-related number alongside a poor
>   sample judgement, or the reverse, and they are distinguishable only by running arm f's per-dimension
>   variance check. Report which was found.
> - **A family ranking taken from metric 10 or 11 is metric-indexed.** The modern anchor records that diffusion
>   models were shown to be quantitatively superior to GANs, and states the result **in terms of the Fréchet
>   inception distance**. That is the correct way to state it, and it is the worked modern instance of the
>   failure mode `SOP-DL-09` §4 already names — treating a metric disagreement as a model disagreement. A
>   ranking reported without its metric is not a result, and this benchmark does not rank families.
> - **A valid lower bound above an exact value supports a one-sided likelihood ordering.** Of the four
>   families the modern anchor discusses, flows admit tractable density evaluation (for CNFs, subject to
>   numerical solver error). Its footnote describes a diffusion lower bound exceeding a flow's exact
>   value while generation is slower. On matched data and units the ordering is informative about
>   likelihood; generation cost is a separate dimension in an overall utility comparison.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §4.1, §4.3, §4.6.
> Sources: `DDPM` (verbatim quotes in `sources.md` §2.3); `UDL` §16.5.1 fol. 319 and fn. 2, ch. 18 Notes fol.
> 369. `DDPM` §4.1, Table 1 was independently checked against the original arXiv HTML.*

## 6. Validity limits and source traceability

- **Estimates, bounds and exact likelihoods are not interchangeable**, but may describe the same quantity
  on identical data, preprocessing and units. A stochastic estimate above a lower bound is inconclusive;
  a valid lower bound above an exact likelihood supports a one-sided ordering. Binary likelihoods and
  real-valued densities remain incommensurable without a justified common measure. Where comparisons
  cannot be made, use task-based evaluation (§20.14, p. 715).
- **The book states no bound or bias result for AIS** other than the mode-dropping direction in arm b; it
  defers variance and efficiency analysis to the cited literature (§18.7.1, pp. 627–630). Any stronger
  statement about AIS bias is not supported here.
- **Mixing cannot be certified.** The book states that we typically cannot know whether a Markov chain has
  mixed successfully, and offers only heuristics (§17.3, p. 600). A "mixed" claim in any report is a heuristic
  judgement.
- **Perplexity is not used** in this benchmark: the book's generative-model evaluation section does not name
  it, and no metric is introduced that the source does not supply.
- The closing limitation must accompany every result: even restricted to their best-suited tasks, all metrics
  currently in use still have serious flaws, and designing new measurement techniques is itself one of the
  most important research topics in generative modelling (§20.14, p. 717). The metric must match the intended
  use, and some models are better at putting mass where real data is while others are better at avoiding mass
  where data is not — a difference the book traces to forward versus reverse KL (§20.14, p. 717; §3.13,
  pp. 105–109).

| Claim | Locator |
| --- | --- |
| Only an approximation of log-probability is usually available; declare what is measured; estimate-vs-bound case; task-based comparison with precision and recall; AIS mode-dropping inflates likelihood | §20.14, p. 715 |
| Preprocessing identity and the ×0.1 example; data-type comparability; binary log-likelihood ≤ 0 vs unbounded real log-density; three binarization schemes; sharing binarized files | §20.14, p. 716 |
| Provenance-blind inspection; very poor models can produce very good samples; nearest-neighbour test; simultaneous over- and under-fitting; dropped modes undetectable | §20.14, pp. 716–717 |
| Likelihood computed when feasible; background-variance reward hacking; cost toward −∞ in any real-valued MLE problem; need for other evaluation methods | §20.14, p. 717 |
| Metric must match intended use; forward vs reverse KL; all current metrics have serious flaws | §20.14, p. 717 |
| KL divergence and entropy | §3.13, pp. 105–109 |
| Z-ratio comparison rule; why Z must be estimated | §18.7, pp. 624–625 |
| Simple importance sampling for the Z ratio; degradation with large divergence; variance of importance weights | §18.7, pp. 626–627 |
| AIS construction and status; no bound or bias result stated | §18.7.1, pp. 627–630 |
| Bridge sampling; chained importance sampling; in-training Z tracking | §18.7.2, pp. 631–632 |
| Importance-sampling degeneracy and underestimation; biased variant asymptotically unbiased; MC confidence interval | §17.2, pp. 593–596; §17.1.2, p. 593 |
| MCMC burn-in, thinning, ~100 parallel chains, mixing unknowable, heuristic substitutes | §17.3, pp. 596–600 |
| Persistent-chain evaluation contamination; no formal re-mixing test; within- vs between-chain variance symptom | §18.2, p. 615 |
| Pseudolikelihood: definition, consistency, poor for full-joint tasks including sampling, incompatible with lower bounds | §18.3, pp. 616–619 |
| ELBO definition and lower-bound property; tightness iff q equals the posterior | §19.1, p. 635 |
| Gap at the learned θ certifies nothing about θ*; Dirac q makes the bound infinitely loose | §19.4.4, pp. 651–652; §19.3–19.4, pp. 637–638 |
| Importance-weighted autoencoder objective is a lower bound that tightens with more samples | §20.10.3, pp. 697–698 |

**Modern-update provenance.** Every row above is a 2016-book locator and none was altered. Three
modern-update blocks were added: the metric block §4.M (metrics 10–12 with their source-stated failure modes),
the interpretation rules in §5, and the scoped statement of this package's standing rule 5 in
[`Benchmark/Deep-Learning-2016/README.md`](README.md). They are sourced outside the 2016 book and recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§4.1, §4.3, §4.4, §4.6, with source keys defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1: `UDL` §14.3 fol. 272–275,
§16.5.1 fol. 319 and fn. 2, ch. 18 Notes fol. 369; `DDPM`. The claim under test, the arms, the comparison
conditions and the baselines are unchanged; **no arm was added**, and every threshold remains an evaluator
declaration.

**Historical boundary.** MNIST as the dominant generative benchmark, the practice of sharing binarized MNIST
files, ~100 parallel chains matched to minibatch size, and AIS as the standard partition-function estimator
since the cited 2008 work are book-era practices. The 2016 verdicts on specific families — variational
autoencoders as among the state of the art but producing somewhat blurry samples, the cited convolutional and
Laplacian-pyramid adversarial models on a bedroom/church dataset fooling human subjects 40% of the time,
moment-matching networks' disappointing samples without autoencoder composition, NADE described as recently
very successful — are recorded as period statements. No numeric likelihood or perplexity values are stated in
these sections, so none is invented here.

The closing clause of this note was amended by the modern update. It previously stated that no post-2016
evaluation metric is introduced; §4.M now introduces three, each named by the anchor textbook and each carrying
the failure modes that source states. The exclusion remains in force for the **2016 text and for metrics 1–9**,
and the two properties that made the rule necessary are preserved: every metric is a quantity a source names,
and no threshold is invented. What the rule was protecting against — a score introduced to fill a template
field, or a bare ranking axis — is still prohibited, now by §4.M's three governing rules rather than by
exclusion. Perplexity is still not used anywhere in this package, because no source in either lineage names it
as a generative-model metric.
