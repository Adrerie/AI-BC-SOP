# BC-DL-10 — When does sharing pay? Gains from pretraining, transfer and unlabeled data as a function of labeled-data size

**Tests:** the book's dataset-size rule for unsupervised pretraining and the licensing conditions for
semi-supervised, multi-task and transfer gains · **Executed by:**
[`SOP-DL-08`](../../SOP/Deep-Learning-2016/SOP-DL-08-decide-what-to-share.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The central claim is a **conditional** one, and the claim is the book's own operational rule (§15.1.1, p. 540):

- On **large** labeled datasets, supervised regularization techniques — the book names dropout and batch
  normalization — reach human-level performance.
- On **medium** datasets, whose examples are CIFAR-10 and MNIST with roughly 5000 labeled samples per class,
  those supervised techniques **beat** unsupervised pretraining.
- On **very small** data, whose example is the splice dataset, **Bayesian** methods beat pretraining.

The benchmark also tests the supporting claims in the table below:

| # | Claim | Locator |
| --- | --- | --- |
| 1 | Unsupervised pretraining is helpful when the number of labeled samples is very small, and most helpful when unlabeled samples are very numerous | §15.1.1, p. 537 |
| 2 | The deeper the pretrained network, the greater the reduction in **both the mean and the variance** of test error | §15.1.1, p. 539 |
| 3 | Mechanism: pretrained networks consistently stop in a smaller region of function space, lowering estimator variance and hence overfitting risk | §15.1.1, pp. 538–539 |
| 4 | Pretraining does **not** reduce training error but reduces test error — it acts as a regularizer and as a form of parameter initialization | §15.1, p. 535 |
| 5 | Counter-evidence the book itself reports: in one cited study pretraining was on average slightly negative, though it helped markedly on some problems | §15.1.1, pp. 535–536 |
| 6 | Semi-supervised licensing: if p(x) is uniform, observing x gives no information about p(y|x); if x comes from a well-separated mixture with one component per class, modeling p(x) locates the components and **one labeled sample per class** suffices | §15.3, pp. 545–546 |
| 7 | Multi-task sharing improves generalization and generalization-error bounds through statistical strength, **only when** the assumption of a statistical relationship between tasks is reasonable | §7.7, p. 270 |
| 8 | Transfer helps when the shared features correspond to latent factors appearing across settings and the source setting is data-rich enough that the target needs very few samples; zero-shot transfer requires a task variable T that is a **generalizable representation, not a one-hot encoding** | §15.2, pp. 541, 543 |
| 9 | Dropout was ineffective below roughly 5000 samples in the cited comparison | §7.12, p. 290 |

## 2. Data and comparison conditions

- **Labeled-data ladder.** Use at least three regimes, one for each branch of the book's rule. The regimes
  are very small, medium and large. The medium regime is on the order of a few thousand labels per class.
  Obtain each regime by subsampling one corpus, so that every other factor stays fixed.
- **Technique arms** at each ladder point:
  - no extra information
  - Greedy layer-wise unsupervised pretraining per Algorithm 15.1. That algorithm pretrains each layer on the
    output of the previous layer, holds the lower layers fixed, and then applies joint supervised
    fine-tuning.
  - dropout
  - batch normalization
  - a Bayesian treatment
  - semi-supervised training that uses the unlabeled pool
  - multi-task training with a second task
  - transfer from a data-rich source task
- **Unlabeled-pool sweep.** For the semi-supervised arm and the pretraining arm, vary the number of unlabeled
  samples independently of the labeled count. Claim 1 makes the gain depend on both counts.
- **Depth sweep for the pretraining arm**, to test claim 2's "deeper ⇒ larger reduction in mean and variance".
- **p(x) structure conditions** for claim 6. Use one dataset whose class-conditional distributions form
  well-separated clusters. Use a second dataset, built or chosen so that p(x) carries little information
  about y.
- **Multi-task condition** for claim 7: a task pair with a plausible common factor pool, and a pair built to
  be unrelated.
- **Transfer condition** for claim 8. Use a data-rich source task and a data-poor target task that share
  input structure. Add a zero-shot arm. In that arm the task variable takes two representations: one-hot, and
  a generalizable representation.
- **Hyperparameter selection rule**: Select the pretraining hyperparameters by validation error in the
  **supervised** stage. That is the book's recommended practice (§15.1, p. 539). Run a separate arm that
  selects the pretraining hyperparameters in the unsupervised stage. Expect that arm to do worse.

## 3. Baselines

- At each ladder point, the **supervised-only** run with the book's mild-regularization default is the
  baseline that every sharing mechanism must beat.
- For pretraining, the matched fine-tuned-from-random-initialization run separates the initialization effect
  from the regularization effect.
- For semi-supervised, the same labeled data without the unlabeled pool.
- For multi-task, each task trained alone with the same total compute.
- For transfer, the target task trained from scratch on its own data.
- For the representation claims, use the linear control. An undercomplete autoencoder with a linear decoder and
  MSE recovers the PCA subspace. So any claim of learning beyond PCA must beat PCA at matched code dimension
  (§14.1, pp. 511–512; §13.5, p. 509).

## 4. Metrics

1. **Test error mean and variance** across seeds or folds — claim 2 is specifically about both quantities.
2. **Training error** alongside test error, to verify claim 4: pretraining should not lower training error.
3. **Region-of-function-space measure** for claim 3. Use the dispersion of the final parameter
   configurations, or the dispersion of predictions across seeds. That dispersion is the observable proxy for
   "consistently stopping in a smaller region".
4. **Gain versus labeled-data size**. Plot the series so that the crossover between the branches appears.
   Report which ladder points you used, rather than a fitted threshold.
5. **Gain versus unlabeled-pool size** for the semi-supervised and pretraining arms.
6. **Labels needed per class** in the separated-mixture condition, against claim 6's one-sample-per-class
   statement.
7. **Task-pair contrast** for claim 7. Take the multi-task gain on the related pair, and subtract the gain on
   the unrelated pair.
8. **Zero-shot transfer success** under one-hot versus generalizable task representations (claim 8).
9. **Cost**: pretraining adds a stage. The book notes two drawbacks of that two-stage design. No single knob
   controls the regularization strength, and hyperparameter feedback between the stages arrives late
   (§15.1, p. 539). Report the cost of both stages.

## 5. How to interpret failure

- **Pretraining loses at every ladder point** ⇒ that result agrees with the book's own verdict. The book
  states that fully-connected deep structures no longer need pretraining, and that most algorithms no longer
  use pretraining. The book names one exception: natural language processing. In that domain, words are
  one-hot vectors that carry no similarity, and huge unlabeled corpora exist (§15.1, p. 534; §15.1.1,
  p. 540). Report the domain.
- **Pretraining wins on the medium dataset** ⇒ check whether the supporting comparison predates current
  methods. The book states that the cited experiments predate ReLU units, dropout and batch normalization. The
  book also states that researchers know little about a combination of unsupervised pretraining with those
  methods (§15.1.1, p. 539). A win is evidence about that configuration, not a refutation of the size rule.
- **Pretraining lowers training error** ⇒ do not read that result as either confirmation or refutation
  standing alone. A lower training error is equally consistent with a different explanation. Pretraining may
  act as a capacity change, or as an optimization change, rather than as the regularizer the book describes
  (§15.1, p. 535). Report both errors separately. Before you attribute the gain, check the capacity
  confounders and the optimization confounders.
- **Semi-supervised gain appears on the uninformative-p(x) dataset** ⇒ the gain does not come from the
  unlabeled structure. Check for leakage between the unlabeled pool and the evaluation split.
- **Multi-task gain appears on the unrelated pair** ⇒ the gain comes from compute or from regularization, not
  from shared factors. The book makes that gain conditional on a reasonable statistical relationship
  (§7.7, p. 270).
- **Zero-shot transfer works with one-hot task variables** ⇒ that result contradicts claim 8. Verify that the
  evaluated tasks were in fact unseen. One-hot encodings carry no similarity information: the squared L2
  distance between any two distinct one-hot vectors is 2 (§15.1.1, p. 537).
- **Dropout helps below ~5000 samples** ⇒ that result differs from the cited comparison, where a Bayesian
  neural network won in that regime (§7.12, p. 290). Report the dataset and the Bayesian arm.
- **Any arm whose hyperparameters were selected in the unsupervised stage** cannot enter a comparison with the
  rest. Re-run that arm with supervised-stage selection (§15.1, p. 539).

## 6. Validity limits and source traceability

- The three branches are anchored to **named 2016-era datasets** (CIFAR-10, MNIST at roughly 5000 labels per
  class, and the splice dataset). Those datasets locate the regimes. Those datasets are not thresholds for
  reuse on other data.
- Claim 5 is part of the record: the book reports a cited study where pretraining was on average slightly
  negative. A null or negative result is therefore within the book's own expectations. Report such a result
  rather than discard that result.
- The book states Claim 3's mechanism as an interpretation of a cited visualization. The observable proxy in
  this benchmark (dispersion across seeds) is an evaluator's choice. That proxy is not a quantity the book
  names.
- Claims 6 and 7 are **licensing conditions**, not effect sizes. The book gives no numeric gain for
  semi-supervised learning or for multi-task learning. So no reader may infer a numeric gain.
- Claim 8's extremes (one-shot, zero-shot) carry extra requirements. Zero-shot needs an additional task
  variable, and a model that estimates p(y | x, T) (§15.2, p. 543).
- Nothing here licenses a general claim that unsupervised learning helps. The book records a domain
  asymmetry. Natural language processing benefits greatly. Computer vision shows no benefit at that time,
  except in semi-supervised settings with very few labels (§11.2, p. 440).

| Claim | Locator |
| --- | --- |
| Pretraining algorithm; freezing of lower layers; fine-tuning; historical role for fully-connected nets; regularizer-and-initialization function | §15.1, pp. 533–535, Algorithm 15.1 |
| Two-stage drawbacks; supervised-stage hyperparameter selection | §15.1, p. 539 |
| When pretraining helps; depth effect on mean and variance; smaller-region mechanism; slightly-negative cited study; predates ReLU/dropout/batch-norm caveat; the dataset-size rule | §15.1.1, pp. 535–540 |
| No-longer-necessary verdict; NLP exception with word embeddings | §15.1, p. 534; §15.1.1, p. 540 |
| Semi-supervised licensing; uniform-p(x) failure; separated-mixture success | §15.3, pp. 545–546 |
| Shared-parameter generative/discriminative trade-off | §7.6, p. 268 |
| Multi-task: soft constraint, shared vs task-specific parameters, statistical strength, conditional gain | §7.7, pp. 268–270 |
| Transfer vs domain adaptation vs concept drift; bottom- and top-shared factorizations; conditions; one-shot and zero-shot with a generalizable T; multimodal learning | §15.2, pp. 540–545 |
| One-hot distance 2 | §15.1.1, p. 537 |
| Dropout below ~5000 samples; Bayesian alternative | §7.12, p. 290 |
| Domain asymmetry in the first baseline | §11.2, p. 440 |
| Linear autoencoder recovers the PCA subspace | §14.1, pp. 511–512; §13.5, p. 509 |

**Historical boundary.** This benchmark is the most era-bound in the package, by design. The dataset-size rule
is one such 2016 statement. The 2011 transfer-learning competitions are another. There, the best result on
tasks with a few to a few dozen labels per class came from unsupervised pretraining. The named datasets and the
then-current verdicts are others (semi-supervised and multi-task gains real but assumption-dependent and hard
to predict; supervised pretraining on ImageNet as the popular successor in transfer learning). This benchmark
reports those statements as 2016 statements.

The conditional structure of the claims is general, and this package retains that structure. The structure is
that sharing pays only under stated assumptions about latent factors, about task relatedness and about the
label budget. No post-2016 pretraining paradigm is introduced. No modern self-supervised result is
substituted for the book's word-embedding example.
