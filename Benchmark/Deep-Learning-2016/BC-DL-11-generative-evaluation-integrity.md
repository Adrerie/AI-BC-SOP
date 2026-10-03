# BC-DL-11 — Generative-model comparison: is the measured quantity comparable, and does likelihood track sample quality?

**Tests:** the commensurability failures and the likelihood/sample-quality dissociation the book documents ·
**Executed by:** [`SOP-DL-09`](../../SOP/Deep-Learning-2016/SOP-DL-09-compare-generative-models.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The capability under test is **evaluation integrity for generative models**. The question is whether a reported
comparison measures the quantity that the report names. The book's premise is that we usually cannot evaluate
the log-probability of data under the model exactly. Only an approximation of that log-probability is
available. The first obligation is therefore to think through what a report measures, and to say so clearly
(§20.14, p. 715). Seven specific failure modes are tested:

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

- **Fixed corpus with declared data type.** Use one real-valued treatment and one binarized treatment of the
  same corpus. Run all three binarization schemes separately (arm d). The book notes that researchers using a
  single random binarization share the resulting file, so that results do not differ by binarization draw
  (§20.14, p. 716).
- **Model arms spanning likelihood regimes** — use these three arms:
  - a model with a tractable likelihood
  - a model whose likelihood is available only as a lower bound, namely a latent-variable model trained on an
    ELBO
  - a model scored by a stochastic estimate of log-likelihood (arm a)
- **Z-estimator arms**: run AIS at a compute-economical setting, and at a generous setting. That pair exposes
  the mode-dropping of arm b. Where applicable, also use bridge sampling. The book describes bridge sampling
  as more efficient than AIS when the divergence between the proposal and the target is moderate (§18.7.2,
  p. 631).
- **Preprocessing arms**: evaluate the identical model on inputs scaled by 0.1, and on unscaled inputs
  (arm c).
- **Sample-quality arms**: use these instruments, and include a deliberately poor model that reproduces
  training examples. Also include a model that reproduces one mode well, and that assigns no probability to
  another mode (the book's dog-and-cat example).
  - visual inspection by subjects who do not know the provenance of the samples
  - inspection by the researchers
  - the nearest-neighbour test: for some generated samples, display the Euclidean nearest neighbour of each
    such sample in the training set (arm e)
- **Reward-hacking arm**: a real-valued model that is free to learn the per-dimension variance, on a corpus
  with near-constant regions (arm f).
- **Variational arm**: a latent-variable model for which one can estimate log p(v; θ) independently. Measure
  the gap at the learned θ (arm g).
- **Persistent-chain arm**: a model trained with stochastic maximum likelihood, or with persistent contrastive
  divergence. Evaluate that model both on training-time chains and on fresh randomly-initialized chains
  (arm h).
- **Importance-sampling arm**: use proposals at several divergences from the target, with a record of the
  variance of the importance weights (arm i).

## 3. Baselines

- The tractable-likelihood model is the reference. Against that reference, a bound-based score and an
  estimate-based score are incommensurable (arm a).
- The generous AIS setting is the reference for the compute-economical setting (arm b).
- The unscaled-input run is the reference for arm c.
- For arm d, each binarization scheme is its own reference. A cross-scheme comparison is not allowed.
- For arm e, the training set itself is the nearest-neighbour reference.
- For arm h, the fresh-chain evaluation is the reference. The training-chain evaluation carries the
  contamination that this benchmark measures.

## 4. Metrics

1. **The declared measured quantity**: for every reported number, state the kind of that number. The kinds
   are a point value, a stochastic estimate, and a bound. For a bound, state the looseness where that is
   known (§20.14, p. 715).
2. **Test log-likelihood**, with the Z estimator, its settings and its bias direction where known.
3. **log Z estimate and the variance of the importance weights** (§18.7, pp. 626–627; §17.2, pp. 595–596).
4. **Sample-quality instruments**: the outcome of the provenance-blind inspection. Also the distribution of
   nearest-neighbour distances between generated samples and the training set (§20.14, p. 716).
5. **Per-dimension variance** in the reward-hacking arm, and the resulting likelihood, to expose the
   variance-collapse failure (§20.14, p. 717).
6. Report the **ELBO, independently estimated log p(v; θ), and the gap** between the two quantities (§19.1,
   p. 635; §19.4.4, pp. 651–652).
7. **Task-based metrics where the intended use is practical**: rank the test cases. Report precision and
   recall for that ranking. The book offers those metrics as the fair way to compare models, when practical
   use is the concern (§20.14, p. 715).
8. **Chain diagnostics for arm h**: the within-step negative-phase sample variance, against the between-chain
   variance. The book names that pair as the heuristic symptom of chains that fail to re-mix (§18.2, p. 615).
9. **Mixing diagnostics for any MCMC-derived number**: the book states that the mixing time is unknown a
   priori. The book also states that we typically cannot know whether a chain mixed successfully. The
   prescribed substitutes are manual inspection of the samples, and the correlation between successive samples
   (§17.3, p. 600).

The book gives no numeric thresholds here: no perplexity target, no nearest-neighbour distance bound, no
acceptable ELBO gap. So this package invents none. The evaluator must declare every threshold that the run
uses.

> ### 4.M Modern-update metric block (2017–2026)
>
> Metrics 1–9 above are quantities that the 2016 book names. None of those nine changed here. The standing
> rule 6 of this package excludes post-2016 metrics from the 2016 text. That exclusion still governs metrics
> 1–9. Here the rule is **scoped**, not broken. Three later metrics now have an anchor-textbook source. That
> source states the failure modes of each one. So those three may enter on the same terms as the 2016
> quantities. Those terms are a source that names the metric, and a threshold that no source supplies. No
> metric in this block may serve as a bare ranking axis. The rule exists to prohibit exactly that.
>
> Each entry below carries the failure modes that its own source states. A metric from this block, reported
> without its failure modes, is out of specification here. Those modes are not optional commentary.
>
> 10. **Inception score** *(modern)* — a sample-quality score. The score reads the outputs of a pretrained
>     classifier on generated samples. Its source states three failure modes. A report must give all three
>     alongside any value. The first claim covers the datasets to which the score applies ("only sensible
>     for" datasets with the label structure of the ImageNet database). The second claim covers the scoring
>     model ("sensitive to the particular classification model; retraining this model can give quite different
>     numerical results"). The third claim covers diversity within a class ("does not reward diversity within
>     an object class; it returns a high value if the model only generates one realistic example of each
>     class"). That third claim is a reward-hacking path, and metric 5 exists to expose that path. Read both
>     metrics together.
> 11. **Fréchet inception distance** *(modern)* — a distance between two feature distributions. Those
>     distributions are of the generated samples and the real samples. A pretrained classifier supplies the
>     **deepest activations**, and the score reads those activations, so the comparison is semantic. The source
>     gives the consequence ("any information discarded by the network does not contribute to the result").
>     Report the feature network, the layer **and real-data reference split**. A measurement setup indexes the
>     number to all three items, and `DDPM` §4.1 demonstrates the point. That section reports FID 3.17 against
>     training data, but 5.24 against the test set. Values computed with different reference splits must not
>     enter a comparison as though the evaluation were identical. The reference split is part of the value.
> 12. **Manifold precision and recall** *(modern)* — a two-number decomposition. The pair approximates each
>     distribution's manifold with k-nearest-neighbour hyperspheres, in the feature space of a classifier. The
>     source states the reason for the pair: the Fréchet inception distance ("is sensitive both to the realism
>     of the samples and their diversity but does not distinguish between these factors"). Where one distance
>     supports a claim about *either* realism or diversity, this pair separates the two. Declare the k that the
>     run used.
>
> Three rules keep this block inside the package's standing rules.
>
> - **Every metric is a quantity a source names.** The anchor textbook defines all three, and states the
>   limitations of each one. Standing rule 2 of this package's README applies that same test to metrics 1–9.
>   Nothing here fills a template field.
> - **No threshold is invented.** As with metrics 1–9, the source supplies no acceptable value for any of the
>   three. Comparisons are **orderings**, and the absolute value comes from the run.
> - **Never a bare axis.** Metric 10 depends on the classifier, and metric 11 depends on the layer. A
>   measurement setup therefore indexes both numbers. A value without that setup is not a measurement. The
>   modern anchor identifies normalizing flows among its four families, and CNFs require numerical
>   integration. Where a tractable likelihood evaluation exists, metric 2 stays primary. This block then only
>   supplements metric 2.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §4.4. Source: `UDL`
> §14.3, fol. 272–275 (citing Kynkäänniemi et al. 2019 for manifold precision and recall). The token `FID`
> does not occur in the chapters read; the metric is named there in full as "Fréchet inception distance", and
> that is the name used here (`sources.md` §2.5).*

## 5. How to interpret failure

- **Arm a: a stochastic estimate exceeds another model's lower bound** ⇒ the ranking remains uncertain. That
  ranking becomes firm only when the looseness of the bound and the uncertainty of the estimator are both
  known. In the reverse case, a **valid lower bound above a comparable exact log-likelihood** establishes a
  one-sided likelihood ordering.
- **Arm b: the cheap AIS run gives a higher likelihood** ⇒ mode-dropping is the likely cause. An estimate that
  underestimates Z overestimates the likelihood. The high score is therefore not evidence of a better model.
- **Arm c: likelihood changes under input rescaling** ⇒ the result is expected. That expectation is the point
  of the arm. The two runs do not solve the same task.
- **Arm d: likelihoods differ across binarization schemes** ⇒ that result is expected. A cross-scheme
  comparison is meaningless. No one may compare a binary model with a real-valued model at all.
- **Arm e: good-looking samples from a poor model** ⇒ that is the book's stated outcome. Visual quality alone
  cannot rank models. If the nearest-neighbour distances are small, the model copies training examples. If a
  mode is missing, note that human inspection cannot reliably detect dropped modes at realistic mode counts.
- **Arm f: likelihood rises while per-dimension variance on constant regions collapses** ⇒ that is reward
  hacking, not improvement. That case is the book's argument that other evaluation methods are needed.
- **Arm g: small gap at the learned θ** ⇒ the audit is incomplete by construction. A measurement of the true
  damage would need the bound at the unreachable θ*. That need implies a better learning algorithm than the
  algorithm under audit.
- **Arm h: training-chain evaluation looks better than fresh-chain** ⇒ that result is the contamination the
  book predicts. Report only the fresh-chain number.
- **Arm i: the estimate improves when the proposal moves closer to the target** ⇒ that pattern agrees with
  weight degeneracy. Report the weight variance, and report the direction of the bias, which is toward
  underestimation.
- **Any arm where a pseudolikelihood-trained model is asked to sample or estimate density** ⇒ out of scope for
  that objective. The book states that pseudolikelihood usually performs poorly for tasks that need the full
  joint, and that need includes sampling. The book also states that pseudolikelihood can beat maximum
  likelihood for conditional-only tasks, such as filling in a few missing values (§18.3, p. 618).

> **Modern update (2017–2026) — three interpretation rules, no change to any arm.** The bullets above stand.
> No arm, baseline or comparison condition was added.
>
> - **Arm e's outcome now has a documented instance in the opposite direction.** Arm e tests the book's claim
>   that a very poor probability model may produce very good-looking samples. The first widely cited
>   diffusion-model paper supplies the mirror case. That paper reports state-of-the-art sample-quality scores,
>   alongside a concession about log likelihood ("despite their sample quality, our models do not have
>   competitive log likelihoods compared to other likelihood-based models"). A coding argument explains the
>   concession: "more than half of the lossless codelength describes imperceptible distortions". The paper's
>   own numbers make the disagreement concrete on one test set. A strong likelihood-based autoregressive
>   baseline reaches 3.03 bits/dim. The diffusion model's full variational bound sits at ≤3.70. The simplified
>   objective that produced the best sample-quality score sits at ≤3.75. Even so, the **model trained with**
>   the simplified objective still receives a separately evaluated standard variational NLL bound (`DDPM` §4.1,
>   Table 1). The quantity that deviates from the standard bound is the training objective, and not that
>   likelihood-bound evaluation. So a likelihood/sample-quality disagreement is **not by itself** evidence that
>   either instrument failed. Arm e's reading still requires the nearest-neighbour check and the dropped-mode
>   caveat. The modern instance adds a third possibility to distinguish. The model may spend description length
>   on detail that no observer can see. That is a property of the metric. No defect in the model explains that
>   property.
> - **Which kind of disagreement is in play must be named.** Arm f's variance collapse is a defect. That model
>   earns the likelihood dishonestly, by the assignment of an arbitrarily low variance to pixels that never
>   change. The imperceptible-detail case is not a defect. Both cases produce a good likelihood-related number
>   alongside a poor sample judgement, or the reverse. Only arm f's per-dimension variance check tells the two
>   cases apart. Report which kind that check found.
> - **A family ranking taken from metric 10 or 11 is metric-indexed.** The modern anchor reports the
>   quantitative superiority of diffusion models over GANs. The anchor states that result **in terms of the
>   Fréchet inception distance**. That phrasing is the correct way to state the result. The result is also the
>   worked modern instance of the failure mode that `SOP-DL-09` §4 already names. That failure mode is a metric
>   disagreement read as a model disagreement. A ranking reported without its metric is not a result. This
>   benchmark does not rank families.
> - **A valid lower bound above an exact value supports a one-sided likelihood ordering.** The modern anchor
>   discusses four families. Of those families, flows admit tractable density evaluation. For CNFs, that
>   evaluation is subject to numerical solver error. The anchor's footnote describes a diffusion lower bound
>   that exceeds a flow's exact value, while generation runs slower. On matched data and units, that ordering
>   is informative about likelihood. Generation cost is a separate dimension in an overall utility comparison.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §4.1, §4.3, §4.6.
> Sources: `DDPM` (verbatim quotes in `sources.md` §2.3); `UDL` §16.5.1 fol. 319 and fn. 2, ch. 18 Notes fol.
> 369. `DDPM` §4.1, Table 1 was independently checked against the original arXiv HTML.*

## 6. Validity limits and source traceability

- **Estimates, bounds and exact likelihoods are not interchangeable**, yet all three may describe the same
  quantity on identical data, identical preprocessing and identical units. A stochastic estimate above a lower
  bound is inconclusive. A valid lower bound above an exact likelihood supports a one-sided ordering. Binary
  likelihoods and real-valued densities remain incommensurable without a justified common measure. Where no
  comparison is available, use task-based evaluation (§20.14, p. 715).
- **The book states no bound or bias result for AIS** other than the mode-dropping direction in arm b. The
  book defers the variance and efficiency analysis to the cited literature (§18.7.1, pp. 627–630). This
  package supports no stronger statement about AIS bias.
- **Mixing cannot be certified.** The book states that we typically cannot know whether a Markov chain mixed
  successfully, and offers only heuristics (§17.3, p. 600). A "mixed" claim in any report is a heuristic
  judgement.
- **Perplexity is not used** in this benchmark. The generative-model evaluation section of the book does not
  name perplexity. No metric enters this benchmark unless the source supplies that metric.
- The closing limitation must accompany every result. Even on their best-suited tasks, all metrics currently in
  use still have serious flaws. The book makes the design of new measurement techniques itself one of the most
  important research topics in generative modelling (§20.14, p. 717). The metric must match the intended use.
  Some models are better at the placement of mass where real data is. Other models are stronger on the
  avoidance of mass where data is not. The book traces that difference to forward versus reverse KL (§20.14,
  p. 717; §3.13, pp. 105–109).

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

**Modern-update provenance.** Every row above is a 2016-book locator, and none was altered. This chapter adds
two modern-update blocks. One is the metric block §4.M, which carries metrics 10–12 with their source-stated
failure modes. The other is the set of interpretation rules in §5. This benchmark scopes the package's standing
rule 6 in [`Benchmark/Deep-Learning-2016/README.md`](README.md).

Both blocks draw on sources outside the 2016 book, and
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§4.1, §4.3, §4.4, §4.6 records both.

[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1 defines the source keys
(`UDL` §14.3 fol. 272–275, §16.5.1 fol. 319 and fn. 2, ch. 18 Notes fol. 369; `DDPM`).

The record keeps the claim under test, the arms, the comparison conditions and the baselines unchanged, and
**no arm was added**. Every threshold remains an evaluator declaration.

**Historical boundary.** These practices are book-era:

- MNIST as the dominant generative benchmark
- the practice of sharing binarized MNIST files
- ~100 parallel chains, matched to the minibatch size
- AIS as the standard partition-function estimator, since the cited 2008 work

These 2016 verdicts on specific families are recorded as period statements:

- The book places variational autoencoders among the state of the art, but notes somewhat blurry samples.
- The cited convolutional and Laplacian-pyramid adversarial models, on a bedroom/church dataset, fool human
  subjects 40% of the time.
- Moment-matching networks give disappointing samples without autoencoder composition.
- The book describes NADE as recently very successful.

No numeric likelihood or perplexity value appears in these sections, so this package invents none.

The modern update amended the closing clause of this note. That clause previously stated that no post-2016
evaluation metric enters the 2016 text. §4.M now introduces three such metrics. The anchor textbook names each
one, and each one carries the failure modes that source states.

The exclusion remains in force for the **2016 text and for metrics 1–9**. The two properties that made that
rule necessary still hold: every metric is a quantity a source names, and the block invents no threshold. The
rule existed to prohibit a score that fills a template field, or a bare ranking axis. §4.M's three governing
rules still prohibit both, in place of the exclusion. No source in either lineage names perplexity as a
generative-model metric, so this package still uses perplexity nowhere.
