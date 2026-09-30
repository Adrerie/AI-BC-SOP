# SOP-DL-08 — Decide what to share: unlabeled data, tasks, stages and representations

**Stage:** leverage · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Decide whether to bring in information beyond the labeled training set of the current task, and under what
conditions that information pays. Five mechanisms are in scope, and each is licensed by a different
assumption:

| Mechanism | What is shared | Licensing assumption |
| --- | --- | --- |
| Semi-supervised | unlabeled samples from p(x) | y is, or is correlated with, a recoverable latent cause of x (§15.3, p. 545) |
| Multi-task | parameters across tasks | a pool of common factors explains input variation, each task using a subset (§7.7, pp. 268–270) |
| Transfer / domain adaptation | a representation or a trained model across settings | many factors explaining variation in the source setting are relevant to the target (§15.2, p. 541) |
| Pretraining (unsupervised or supervised) | parameters across training stages | the earlier stage places the parameters in a better region (§15.1, p. 535; §8.7.4) |
| Parameter sharing | weights across positions or components | a known domain invariance (§7.9, p. 278) — handled by `SOP-DL-07` |

This SOP also owns the criteria for judging whether a learned representation is any good, because every
mechanism above is a claim about representations.

Out of scope: capacity and regularization decisions on the labeled data alone (`SOP-DL-02`, `SOP-DL-03`),
supervised pretraining as an *optimization* device (`SOP-DL-04` §3.4, repair 9), and structural bias
(`SOP-DL-07`).

## 2. Inputs and assumptions

- The labeled-data budget for the target task, and the size of any unlabeled or source-task corpus. This
  budget, not taste, selects the branch (see §3.5).
- The task specification from `SOP-DL-01`, including whether the input or the output semantics are what
  varies across settings.
- A validation metric capable of detecting a *generalization* change, since the mechanisms here are
  regularizers: unsupervised pretraining, for instance, does not lower training error but lowers test error
  (§15.1, p. 535).
- Willingness to state, for each mechanism, the check that would falsify its licensing assumption.

## 3. Procedure

### 3.1 Semi-supervised (§7.6, pp. 267–268; §15.3, pp. 545–549)

1. State what it means in this setting: unlabeled samples from p(x) and labeled samples from p(x, y) are both
   used to estimate p(y|x). In deep learning this usually means **learning a representation h = f(x)** such
   that same-class samples get similar representations; samples tightly clustered in input space should map to
   similar representations, and in many cases a **linear classifier in the new space** then generalizes well.
   The classic variant is PCA as a preprocessing step before classification (§7.6, p. 267).
2. **Check the licensing assumption before spending compute** (§15.3, pp. 545–547). The ideal representation's
   features correspond to the **latent causes** of the observed data, so modeling p(x) yields a good
   representation for p(y|x) only if y is, or is tightly correlated with, a **recoverable** latent cause. The
   causal-graph form of the argument: the real process is a directed graph with the latent h as a parent of x,
   so by Bayes' rule structure in p(x) helps learn p(y|x).
   - It **fails** when p(x) is uniform — observing x then gives no information about p(y|x).
   - It **works** when x is drawn from a mixture with one well-separated component per value of y — modeling
     p(x) locates each component and **one labeled sample per class** suffices.
   - The learner does not know which factor y corresponds to, and the brute-force solution of capturing all
     causes is infeasible. Two practical strategies are stated: use unsupervised and supervised signals
     jointly, or learn larger-scale purely unsupervised representations.
3. Watch the criterion for implicit saliency: a fixed criterion such as pixel-level MSE implicitly decides what
   counts as "important" and can miss small but task-relevant objects (the book's ping-pong-ball example); a
   learned saliency criterion — a generative adversarial model in the cited work — is the alternative. Note
   also the asymmetry result: if x is the effect and y the cause, modeling p(x|y) is robust to changes in
   p(y) (§15.3, pp. 547–549).
4. Implement it as **shared parameters**, not as two separate models: the generative model p(x) or p(x, y)
   shares parameters with the discriminative model p(y|x), and the supervised criterion −log p(y|x) is traded
   against the generative criterion. The generative criterion expresses prior knowledge of a particular form
   about the solution to the supervised problem; controlling its weight in the total criterion gives a better
   trade-off than purely generative or purely discriminative training. That weight is a hyperparameter and
   goes to `SOP-DL-05` (§7.6, p. 268).

### 3.2 Multi-task (§7.7, pp. 268–270)

5. Mechanism: merging examples from several tasks acts as a **soft constraint on the parameters**. Just as
   extra training samples push parameters toward values that generalize better, a part of the model shared by
   several extra tasks is constrained to good values — *if the sharing is reasonable* — and usually generalizes
   better.
6. Structure the model as the common form does (Fig. 7.2): tasks share the same input x and an intermediate
   representation h^(shared) that learns a common pool of factors, with task-specific parameters in the upper
   layers, which generalize well only from their own task's samples, and generic parameters in the lower
   layers, which benefit from the pooled data of all tasks. In the unsupervised case some top-level factors
   need not be associated with any output task at all.
7. Expect the gain through **statistical strength** — the number of samples per shared parameter increases
   relative to the single-task regime, improving generalization and generalization-error bounds — and apply the
   book's own condition: this happens **only when the assumption that some statistical relationship exists
   between the tasks is reasonable**, i.e. only when some parameters can genuinely be shared (§7.7, p. 270).

### 3.3 Transfer and domain adaptation (§15.2, pp. 540–545)

8. Classify the situation:
   - **Transfer learning**: the learner performs two or more *different* tasks, assuming that many of the
     factors explaining variation in the source distribution are relevant to the target — typically the same
     input with a different output (the book's example: cat/dog recognition transferred to ant/wasp).
   - **Domain adaptation**: the task and the optimal input-to-output map are identical, but the input
     distribution differs slightly (the book's example: sentiment classification trained on books, video and
     music applied to electronics, where denoising-autoencoder pretraining worked well).
   - **Concept drift**: transfer over time.
9. Choose *what* to share from what varies. The default factorization is a **shared representation at the
   bottom plus task-specific parameters at the top** (the book reuses its multi-task figure for this). When
   the *output* semantics are what is shared instead — the book's example is speech, where valid sentences
   appear at the output while inputs are speaker-specific — share the **top** layers and use task-specific
   **preprocessing** (§15.2, pp. 541–542).
10. Check the conditions under which transfer helps: the shared features must correspond to latent factors
    that appear across settings, and the source setting must have abundant data so that the target needs very
    few samples (§15.2, p. 541). The extremes are named and carry extra requirements:
    - **One-shot learning** — a transfer task with only one labeled sample.
    - **Zero-shot / zero-data learning** — no labeled samples at all; this requires an extra task variable T
      with the model estimating p(y | x, T), and **T must be a generalizable representation, not a one-hot
      encoding** — word embeddings are the cited example (§15.2, p. 543).
    - **Multimodal learning** learns the two input mappings and their relation jointly (§15.2, pp. 544–545).

### 3.4 Pretraining across stages (§15.1, pp. 533–540)

11. **Read the book's verdict before investing.** Greedy layer-wise unsupervised pretraining is **no longer
    necessary** to train fully-connected deep structures (§15.1, p. 534), and most algorithms no longer use
    unsupervised pretraining — except in natural language processing, where words are one-hot vectors carrying
    no similarity information and huge unlabeled corpora exist, so word embeddings are still in use (§15.1.1,
    p. 540). Historically it was the first method able to train fully-connected deep supervised networks;
    before 2006 only convolutional and recurrent deep networks were thought trainable (§15.1, p. 534).
12. If it is used, know what it is: **a regularizer and a form of parameter initialization** — it does not
    reduce training error but reduces test error (§15.1, p. 535). Run it as Algorithm 15.1 specifies: stack
    layers so each is pretrained on the previous layer's output, train layer k while holding the lower layers
    fixed (lower layers are **not** readjusted when higher layers are added), then optionally fine-tune all
    layers jointly with a supervised learner (§15.1, p. 534).
13. Expect the gain only in the low-label regime, and know the two stated caveats: it helps when labeled
    samples are very small and most when unlabeled samples are very numerous, and the deeper the pretrained
    network the greater the reduction in both the mean and the variance of test error, because pretrained
    networks consistently stop in a **smaller region of function space**. But in one cited study (chemical
    activity prediction) pretraining was on average slightly negative even though it helped markedly on some
    problems, and those experiments **predate ReLU units, dropout and batch normalization**, so little is known
    about combining it with current methods (§15.1.1, pp. 535–540).
14. Handle the two-stage drawbacks explicitly: there is no single knob controlling regularization strength,
    and hyperparameter feedback is delayed between stages. Select pretraining hyperparameters by **validation
    error in the supervised stage** (§15.1, p. 539).

### 3.5 Let the labeled-data budget decide

15. Apply the book's dataset-size rule, which is the operational core of this SOP (§15.1.1, p. 540):
    - **Large labeled datasets**: supervised regularization techniques (the book names dropout and batch
      normalization) reach human-level performance; unsupervised pretraining is not the lever.
    - **Medium datasets** — the book's examples are CIFAR-10 and MNIST, with roughly 5000 labeled samples per
      class: those supervised techniques **beat** unsupervised pretraining.
    - **Very small data** — the book's example is the splice dataset: **Bayesian** methods beat pretraining.
    Carry the related threshold from `SOP-DL-03`: dropout was ineffective below roughly 5000 samples in the
    cited comparison (§7.12, p. 290).
16. Note the domain asymmetry the book records for the first baseline: natural language processing benefits
    greatly from unsupervised techniques such as learned word embeddings, while computer vision showed no
    benefit at the time except in semi-supervised settings with very few labels; include unsupervised learning
    in the first end-to-end baseline only where the domain deems it important, otherwise try it first when the
    initial baseline is found to overfit (§11.2, p. 440).

### 3.6 Understand why sharing works, and prefer distributed factors (§15.4, pp. 549–554)

17. Share at the level of **factors, not symbols**, because the statistical advantage is exponential: n
    features with k values describe kⁿ concepts, and a distributed representation with n linear-threshold
    features assigns unique codes to O(n^d) input regions using O(nd) parameters, whereas a
    nearest-neighbour scheme with n samples distinguishes only n regions (§15.4, pp. 549–554). The contrast
    class — which representations are *not* distributed — is listed in `concept_reconstruction.md` §4.1(c);
    the operative consequence is that the squared L2 distance between any two distinct one-hot vectors is 2, so
    one-hot encodings carry no similarity information (§15.1.1, p. 537), which is why zero-shot transfer
    requires a generalizable T.
18. Use the regularization reading: a strong representation with a weak (linear) classifier is itself a strong
    regularizer, and the VC dimension of deep linear-threshold networks is only O(w log w) in the number of
    weights. This is checkable, not merely asserted — hidden units in networks trained on ImageNet and Places
    are interpretable, and directions in a face-generating model separate gender from eyeglasses (§15.4,
    pp. 554–555). Treat both as observational evidence for the existence of distributed factors, not as a
    metric.
19. Treat depth as a sharing lever with an exponential payoff: some functions representable by a depth-k
    network require exponentially many units at depth 2 or k − 1; the result extends to sum-product networks
    and to families of convolutional-network circuits (§15.5, pp. 555–556). Pair this with the
    matched-parameter-count discipline of `SOP-DL-07`.
20. When choosing what to share, use the book's list of general priors for discovering latent causes
    (§15.6, pp. 556–558). The full list is in `concept_reconstruction.md` §4.1(c); the three that most often
    decide a sharing question are **factors shared across tasks** (each output tied to a subset of a common
    factor pool, so sharing p(h|x) shares statistical strength), **natural clustering** (each connected
    manifold receiving one class — which motivates tangent propagation, double backpropagation, the
    manifold-tangent classifier and adversarial training), and **smoothness / local constancy**.

### 3.7 Judge whether the representation is actually good (§14)

21. Do not accept reconstruction error alone. With a linear decoder and MSE, an undercomplete autoencoder
    simply recovers the **PCA subspace**; and if capacity is too large the autoencoder learns the **identity**
    and captures nothing (§14.1, pp. 511–512). The code must reflect the training set's distinctive
    statistical structure rather than acting as an identity function (§14.2, p. 512).
22. Apply the criteria the book actually gives, **each against its own appropriate control** — see
    `BC-DL-12` §3 for the per-criterion baseline table:
    - **Linear / undercomplete regime only**: minimizing reconstruction error with a linear encoder and
      decoder yields tied, orthonormal weights spanning the principal eigenvectors of the covariance, so a
      learned code in *that* regime must beat PCA at matched dimension (§13.5, p. 509; §14.1, pp. 511–512).
      This is a theorem about a specific configuration — it is **not** a universal yardstick for nonlinear
      manifold, contractive, counting or encoding claims.
    - **Manifold criterion**, judged against the orthogonal-direction response of the same encoder: sensitive
      only along manifold-tangent directions, insensitive to orthogonal ones, with reconstruction pulling one
      way and the constraint the other (§14.6, pp. 523–524).
    - **Contractive criterion**, judged against the untrained encoder's spectrum: the penalty is the squared
      Frobenius norm of the encoder Jacobian, a Jacobian is contractive when ‖Jx‖ ≤ 1 for all unit x, after
      training **most singular values are below 1**, and the largest-singular-value directions correspond to
      the learned tangent directions. In the small-Gaussian-noise limit, denoising reconstruction error equals
      the contractive penalty. **Tie the decoder weights to the transpose of the encoder**, otherwise the
      degenerate small-constant solution appears (§14.7, pp. 527–530).
    - **Downstream utility**, judged against PCA-based codes and raw inputs — the book's own comparison:
      semantic hashing places semantically related samples close together, and the cited 30-unit bottleneck
      achieves lower reconstruction error than 30-dimensional PCA *and* more interpretable, better
      class-separated codes (§14.9, p. 531).
23. Choose the regularized-autoencoder variant by what it penalizes — sparse, denoising, or
    derivative-penalty/contractive. The variant menu, the denoising training procedure and the linear-factor
    model baseline family (factor analysis, probabilistic PCA, ICA and its identifiability requirement, slow
    feature analysis, sparse coding) are catalogued in `concept_reconstruction.md` §4.1(c) (§13,
    pp. 497–509; §14.2, pp. 512–516; §14.5, p. 518).

### 3.8 Record the decision

24. For each mechanism adopted or rejected, record: the licensing assumption, the check performed on it, the
    trade-off coefficient searched, the representation-quality criteria used beyond reconstruction error, the
    labeled-data branch that selected it, and the observation that would falsify the choice.

## 4. Important failure modes

- **Using unlabeled data when p(x) carries no information about p(y|x)** — the uniform-p(x) case (§15.3,
  pp. 545–546).
- **Multi-task sharing without a genuine statistical relationship** between tasks; the gain is conditional on
  that assumption (§7.7, p. 270).
- **One-hot task variables in a zero-shot setting**: no similarity information, so no generalization to unseen
  tasks (§15.2, p. 543; §15.1.1, p. 537).
- **Unsupervised pretraining on a large labeled dataset**, where supervised regularizers already reach the
  target (§15.1.1, p. 540).
- **Selecting pretraining hyperparameters in the unsupervised stage** instead of by supervised-stage
  validation error (§15.1, p. 539).
- **Judging a representation by reconstruction error alone**: an identity function, or exact equivalence to
  PCA under a linear decoder (§14.1, pp. 511–512; §13.5, p. 509).
- **Untied decoder in a contractive autoencoder**, producing the degenerate small-constant solution (§14.7,
  p. 530).
- **Sharing the wrong end of the network**: when output semantics are shared and inputs are what vary, the
  top must be shared and preprocessing made task-specific — the opposite of the default (§15.2,
  pp. 541–542).
- **Assuming transfer helps when the source setting is not data-rich** relative to the target (§15.2, p. 541).
- **Treating pretraining's benefit as established for current methods**: the supporting experiments predate
  ReLU units, dropout and batch normalization, and the book says little is known about the combination
  (§15.1.1, p. 539).
- **Reading a fixed reconstruction criterion as task-neutral**: it embeds a saliency judgement and can miss
  small task-relevant structure (§15.3, pp. 547–548).

## 5. Outputs and reporting

- The sharing decision record: mechanism, licensing assumption, the check run on it, and the falsification
  condition.
- The labeled-data budget and the branch it selected (large / medium / very small), with the technique that
  branch favours.
- For semi-supervised runs: the generative-criterion weight searched and the value chosen.
- For multi-task runs: the split between shared lower parameters and task-specific upper parameters, and the
  evidence that the tasks share factors.
- For transfer runs: source and target settings, what was shared (bottom representation, top layers, or a
  trained model), and the data-abundance condition.
- For pretraining runs: the stacking procedure, whether lower layers were frozen, the fine-tuning step, and
  the supervised-stage validation error used to select pretraining hyperparameters.
- The representation-quality report: reconstruction error **plus** the control appropriate to each criterion
  claimed — the PCA control only for linear / undercomplete-autoencoder comparisons, the orthogonal-direction
  response for the manifold criterion, the untrained Jacobian spectrum for the contractive criterion, and
  PCA-based codes and raw inputs for downstream utility (`BC-DL-12` §3).
- Anything the book leaves open and that was therefore chosen: the generative-criterion weight, the number of
  pretrained layers, the code dimension, the sparsity target, and the contraction penalty weight.

## 6. Source traceability

| Claim or step | Locator |
| --- | --- |
| Semi-supervised as representation learning; clustering clue; linear classifier in the new space; PCA preprocessing | §7.6, p. 267 |
| Shared-parameter generative/discriminative model; trade-off of criteria; better than purely generative or discriminative | §7.6, p. 268 |
| Multi-task as a soft constraint; shared vs task-specific parameters; common factor pool; statistical strength and generalization bounds; the conditional nature of the gain | §7.7, pp. 268–270, Fig. 7.2 |
| Transfer vs domain adaptation vs concept drift; bottom-shared and top-shared factorizations; conditions for transfer to help; one-shot, zero-shot and the requirement that T be generalizable; multimodal learning | §15.2, pp. 540–545 |
| Semi-supervised causal licensing; uniform-p(x) failure; separated-mixture success with one label per class; causal graph with h as parent of x; recoverability check and infeasibility of capturing all causes; two practical strategies; fixed-criterion saliency warning; cause/effect asymmetry | §15.3, pp. 545–549 |
| Greedy layer-wise pretraining algorithm; freezing of lower layers; fine-tuning; historical role for fully-connected nets; regularizer-and-initialization function | §15.1, pp. 533–535, Algorithm 15.1 |
| Two-stage drawbacks and supervised-stage hyperparameter selection | §15.1, p. 539 |
| When pretraining helps; depth effect on mean and variance of test error; smaller-region-of-function-space mechanism; the slightly-negative cited study; predates ReLU/dropout/batch-norm caveat; dataset-size rule (large / CIFAR-10 and MNIST ≈5000 per class / splice) | §15.1.1, pp. 535–540 |
| Distributed representations: kⁿ concepts, O(n^d) regions with O(nd) parameters, contrast class, strong-representation-plus-linear-classifier regularization, VC dimension O(w log w), interpretability evidence | §15.4, pp. 549–555 |
| One-hot distance 2 | §15.1.1, p. 537 |
| Exponential gains from depth | §15.5, pp. 555–556 |
| Prior list for discovering latent causes | §15.6, pp. 556–558 |
| Autoencoder capacity: undercomplete, PCA recovery, identity failure; code must reflect distinctive statistics | §14.1–§14.2, pp. 511–512 |
| Regularized autoencoder variants; denoising training procedure | §14.2, §14.5, pp. 512–518 |
| Manifold criterion for a good code | §14.6, pp. 523–524 |
| Contractive autoencoder: squared Frobenius norm of the encoder Jacobian, contractiveness condition, singular values below 1, tangent directions, DAE equivalence in the small-noise limit, stacking, tied decoder | §14.7, pp. 527–530 |
| Downstream utility and semantic hashing; 30-unit bottleneck vs 30-d PCA | §14.9, p. 531 |
| Linear factor model baselines: factor analysis, probabilistic PCA, ICA identifiability, SFA, sparse coding; linear autoencoder ⇒ PCA | §13, pp. 497–509 |
| Dropout ineffective below roughly 5000 samples | §7.12, p. 290 |
| Domain asymmetry in the first baseline (NLP vs vision) | §11.2, p. 440 |
| Supervised pretraining as an optimization device | §8.7.4, pp. 344–347 |

**Historical boundary.** This SOP contains the most era-bound material in the package, and the book marks it
itself. Treated as historical: greedy layer-wise unsupervised pretraining as the trigger of the 2006 revival
and its present obsolescence except for NLP word embeddings (§15.1, p. 534; §15.1.1, p. 540); the 2011
transfer-learning competitions won by unsupervised pretraining on target tasks with a few to a few dozen
labels per class (§15.1.1, p. 537); the named datasets (CIFAR-10, MNIST with about 5000 labels per class, the
splice dataset, ImageNet, Places, QMUL Multiview Face); the cited architectures and experiments (RBM and deep
autoencoder stacks with a 30-unit bottleneck, discriminative RBMs and ladder networks as single-stage
semi-supervised methods, predictive generative networks, the face-generating model, ImageNet/Places
interpretability, contractive-autoencoder tangent visualization on a CIFAR-10 dog); and the then-current
verdicts that semi-supervised and multi-task gains are real but assumption-dependent and hard to predict, and
that supervised ImageNet pretraining had become the popular successor in transfer learning (§15.2, p. 540).
The general mechanisms — what licenses semi-supervised learning, why multi-task sharing adds statistical
strength, what transfer requires, the exponential advantage of distributed representations, and the criteria
for judging a representation — are stated as general and are retained. No post-2016 pretraining paradigm is
introduced.
