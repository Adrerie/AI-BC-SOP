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

> **Modern update (2017–2026) — a third factorization, and the zero-shot requirement realized.** Steps 8–10
> stand, including the conditions at step 10: shared features must correspond to latent factors appearing
> across settings, and the source setting must have abundant data. Nothing below displaces them. Two
> additions to the decision space:
>
> **(a) Step 9 gains a third option: freeze the base and adapt a low-rank increment.** The 2016 choice is
> between sharing the bottom or the top, with fine-tuning adjusting all layers jointly. The modern option
> freezes the pretrained base entirely and adapts a **low-rank increment on the attention weight matrices**.
> Its structural properties are what make it a distinct point in the decision rather than a cheaper
> approximation of one:
>
> - Adapting **both** the query and value projections gives the best result under a fixed parameter budget,
>   and spreading a low rank across several matrices beats concentrating it in one.
> - There is **no additional inference latency**, because the increment is materialized into the weights
>   (W = W₀ + BA) before deployment. A latency-sensitive deployment is therefore not a reason to reject it.
> - Many tasks are served from **one frozen base** by swapping the increments, which cuts storage and
>   task-switching overhead. This changes step 9's question from "which layers does this task share?" to
>   "how many tasks must one stored base serve?"
> - The scale of the change is what makes it a decision rather than a detail: trainable parameters can be
>   roughly 10,000× fewer than full fine-tuning of a 175B-parameter model, at roughly 3× lower GPU memory.
>
> **Boundary on (a):** the quality claim is "on-par or better than fine-tuning" on the four model families
> its source tested. No general ranking against full fine-tuning is implied, and the parameter and memory
> ratios are that source's own measurements, not transferable constants. Record which option was chosen and
> why in §3.8.
>
> **(b) Step 10's zero-shot requirement is now realizable, and its defining limit is a closed label set.**
> The 2016 text requires an extra task variable T that is **a generalizable representation, not a one-hot
> encoding**, citing word embeddings. Natural language has been used as exactly that T: a text encoder acts
> as a hypernetwork generating the weights of a linear classifier from the text, with cosine similarities, a
> temperature and a softmax. The requirement is confirmed, not relaxed. What must be added is the limit that
> comes with it, in the source's own words:
>
> - The model "is still limited to choosing from only those concepts in a given zero-shot classifier" — the
>   label set is closed by the classifier you construct, so this is a *selection* capability, not open-ended
>   prediction.
> - It "still generalizes poorly to data that is truly out-of-distribution for it".
> - It is "quite weak on several specialized, complex, or abstract tasks", "struggles with more abstract and
>   systematic tasks such as counting the number of objects in an image", and is near-random on distance
>   estimation.
> - Prompt templates and their ensembling are worth roughly five points, so the reported number depends on a
>   prompt-construction decision that must be declared.
> - Comparables that are usable, all from the same source: zero-shot performance "only approaches fully
>   supervised performance on 5 datasets"; it wins on 16 of 27 datasets against a supervised baseline; and it
>   underperforms by more than 10% on two named fine-grained benchmarks. Read these as evidence that the
>   capability is strongly dataset-dependent, not as a benchmark result.
>
> **Boundary on (b):** a sentence to the effect that zero-shot evaluation amounts to evaluating on a
> different task specification was searched for in the source and **not found**; it is not used anywhere in
> this lineage.
>
> **Cross-links — do not duplicate.** Two of the failures above are capabilities the Trustworthy-ML lineage
> already owns, and this SOP points at them instead of restating a procedure:
>
> - Selecting prompts on a **benchmark validation set** is described by the source itself as "unrealistic for
>   true zero-shot scenarios". That is an evaluation-integrity failure: see Trustworthy-ML
>   [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md).
> - The truly-out-of-distribution limitation is distribution shift: see Trustworthy-ML
>   [`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md).
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §3.6, §3.7, §3.8.
> Sources: `LORA`; `CLIP` (limitations section quoted verbatim in `sources.md` §2.3).*

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

> **Modern update (2017–2026) — the category that replaced greedy layer-wise pretraining.** Steps 11–14
> remain an accurate record of the 2016 verdict, which was correct about the method it named. What has
> changed is that the *category* the 2016 book closed is not the category now in use: **self-supervised
> learning** does not appear as a category in the 2016 book at all.
>
> 14a. **Recognize the category before applying step 11's verdict.** The modern framing is that
>      self-supervised learning creates "free" labeled data in order to feed transfer learning — the same
>      function step 11 assigns to unsupervised pretraining, by a different mechanism. It splits into two
>      families: **generative** (mask-and-predict) and **contrastive** (pairwise relatedness). Step 11's
>      "no longer necessary" verdict applies to greedy layer-wise pretraining of stacked layers; it is not
>      evidence about either family.
>
> 14b. **If the generative family is used, the masking ratio is the load-bearing choice.** Masking a *high*
>      proportion of the input — e.g. 75% — yields a nontrivial and meaningful self-supervisory task; ratios
>      from 40% to 80% were studied and 75% was best both for fine-tuning and for linear probing. The stated
>      rationale is that images are natural signals with heavy spatial redundancy, so sparse random masking
>      leaving a quarter visible suffices — a reason tied to the signal, not a universal constant. The
>      architecture is **asymmetric**: the encoder sees only the visible patches and receives no mask tokens,
>      while a lightweight decoder is used **only during pretraining** and discarded afterwards, which is what
>      produces a 3× or more training acceleration.
>
> 14c. **If the contrastive family is used, two conditions attach and both change the plan.**
>      - *Augmentation composition is not a free choice.* Composition of multiple augmentations is crucial to
>        defining the contrastive task, and it is critical to compose cropping **with** colour distortion —
>        cropping alone lets the model shortcut through colour statistics. The aim of augmentation in this
>        setting is to teach the model to be indifferent to irrelevant transformations, so an augmentation set
>        that leaves an exploitable cue defeats the objective. That failure is a spurious-cue failure and is
>        audited by Trustworthy-ML
>        [`BM-02`](../../Benchmark/Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md); this SOP records the
>        composition requirement and does not restate the audit.
>      - *The method carries a resource condition.* Contrastive learning benefits from **larger batch sizes
>        and more training steps** than supervised learning; batch sizes from 256 to 8192 are reported, a batch
>        of 8192 yields 16382 negative examples per positive pair, and the best models were trained for 1000
>        epochs. These are one source's configuration range, recorded as evidence that the resource axis is
>        bound to the method — not as a recipe, and not as a claim that larger batches always help. This
>        condition belongs in the compute declaration that
>        [`SOP-DL-02`](SOP-DL-02-diagnose-fitting-regime-and-capacity.md) §3.5 now requires.
>
> 14d. **Take the representation from before the projection head.** A nonlinear projection head substantially
>      improves the quality of the learned representation, but the representation that transfers is the one
>      **before** the head. Reading out the post-head representation is a category error, and the head is
>      discarded at transfer time. The loss's normalization and its temperature are load-bearing parts of the
>      objective, not tuning detail.
>
> 14e. **Step 13's low-label expectation survives, with its regime widened.** Step 13 confines the gain to the
>      low-label regime and notes the gain grows with pretraining depth. That reasoning is unchanged. What is
>      new is that the source of the pretraining signal is no longer limited by the availability of a
>      generative model that fits the data: the modern families manufacture their own supervision from
>      unlabeled data, which is why the step 11 verdict about *necessity* and the step 13 verdict about
>      *where the gain appears* can both hold at once.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §3.3, §3.4, §3.5.
> Sources: `UDL` §9.3.7 fol. 152–153 and §9.3.8 fol. 154; `MAE`; `SIMCLR`. `MAE`'s language-model
> "vocabulary" analogy is paraphrase rather than verbatim text and is not quoted (`sources.md` §2.4).*

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

> **Modern update (2017–2026) — three further items to record.** Step 24's list is unchanged; these are added
> to it where the corresponding modern option was available.
>
> - **Which factorization was chosen at §3.3 step 9**, now including the third option: shared bottom, shared
>   top with task-specific preprocessing, or a frozen base with a low-rank increment. If the third, also
>   record how many tasks the stored base must serve, since that is the question the option changes.
> - **For a zero-shot construction**: the label set the classifier closes over, the prompt templates used and
>   whether they were ensembled, and **which split the prompts were selected on** — selecting on a benchmark
>   validation set is an integrity failure owned by Trustworthy-ML
>   [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md).
> - **For a self-supervised pretraining stage**: the family (generative or contrastive), the masking ratio or
>   the augmentation composition, the batch size and step count actually used, and confirmation that the
>   transferred representation was taken **before** any projection head.
>
> *Delta: `delta_map.md` §3.3, §3.4, §3.6, §3.7.*

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

Modern-update failure modes (provenance in §3.3, §3.4 and §3.8 above):

- **Reading out the representation after the projection head.** The head improves the learned representation
  but is discarded at transfer time; the representation that transfers is the one before it (`delta_map.md`
  §3.4).
- **Composing augmentations that leave an exploitable cue** — cropping without colour distortion lets the
  model shortcut through colour statistics, defeating the stated aim of teaching indifference to irrelevant
  transformations. Audited by Trustworthy-ML `BM-02`, not here (`delta_map.md` §3.5).
- **Budgeting a contrastive run as if it had a supervised run's resource profile.** It benefits from larger
  batches and more training steps, so an under-budgeted run measures the budget, not the method
  (`delta_map.md` §3.4).
- **Treating a zero-shot classifier as open-ended prediction.** It selects among the concepts in the
  classifier that was constructed; the label set is closed by that construction (`delta_map.md` §3.7).
- **Selecting zero-shot prompts on a benchmark validation set**, which the source itself calls unrealistic
  for true zero-shot scenarios; an integrity failure owned by Trustworthy-ML `BM-08` (`delta_map.md` §3.8).
- **Rejecting a low-rank adaptation because of inference latency.** The increment is materialized into the
  weights before deployment, so there is no additional latency (`delta_map.md` §3.6).
- **Reading "on-par or better" as a general ranking** over full fine-tuning. The claim covers the four model
  families its source tested (`delta_map.md` §3.6).
- **Applying step 11's "no longer necessary" verdict to self-supervised pretraining.** That verdict is about
  greedy layer-wise pretraining of stacked layers; self-supervised learning is a different category and does
  not appear in the 2016 book as one (`delta_map.md` §3.3).

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
- **Modern update (2017–2026) — for transfer runs,** which of the three factorizations was chosen, now including a frozen
  base with a low-rank increment; if the third, the number of tasks the stored base must serve and
  confirmation that the increment was materialized before deployment.
- **Modern update (2017–2026) — for self-supervised pretraining runs,** the family (generative or contrastive), the
  masking ratio or the augmentation composition, the batch size and step count actually used, and
  confirmation that the transferred representation was taken before any projection head.
- **Modern update (2017–2026) — for zero-shot constructions,** the closed label set, the prompt templates and whether
  they were ensembled, and which split the prompts were selected on.
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

**Modern-update provenance.** Every row above is a 2016-book locator and none was altered. Four
modern-update blocks were added — at §3.3 step 10 (third factorization; zero-shot realized and its closed
label set), §3.4 step 14 (self-supervised pretraining as a category, with steps 14a–14e), §3.8 step 24
(three further items to record) — plus the matching entries in §4 and §5. They are sourced outside the 2016
book and recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§3.3, §3.4, §3.5, §3.6, §3.7, §3.8, with source keys defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1: `UDL` §9.3.7 fol. 152–153 and
§9.3.8 fol. 154; `MAE`; `SIMCLR`; `LORA`; `CLIP`. Three capabilities are **cross-linked rather than
restated**: spurious-cue audit → Trustworthy-ML
[`BM-02`](../../Benchmark/Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md); evaluation-integrity audit →
[`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md); distribution shift →
[`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md).

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
for judging a representation — are stated as general and are retained.

The closing sentence of this note was amended by the modern update. It previously stated that no post-2016
pretraining paradigm is introduced; that is no longer true of the file as a whole. The 2016 procedure above
still introduces none, but §3.4's steps 14a–14e add self-supervised pretraining as the category that replaced
greedy layer-wise pretraining, and §3.3 adds a frozen-base low-rank factorization and language-as-task-variable
zero-shot transfer. Each is marked in place as a modern update with its own sources, and the 2016 verdicts in
steps 11–13 are retained as history rather than rewritten — step 11's "no longer necessary" was correct about
the method it named.
