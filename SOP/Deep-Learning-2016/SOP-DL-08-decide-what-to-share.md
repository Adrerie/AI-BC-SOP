# SOP-DL-08 — Decide what to share: unlabeled data, tasks, stages and representations

**Stage:** leverage · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Decide whether to bring in information beyond the labeled training set of the current task. Decide under what
conditions that information pays. Five mechanisms are in scope. Each mechanism is licensed by a different
assumption:

| Mechanism | What is shared | Licensing assumption |
| --- | --- | --- |
| Semi-supervised | unlabeled samples from p(x) | y is, or is correlated with, a recoverable latent cause of x (§15.3, p. 545) |
| Multi-task | parameters across tasks | a pool of common factors explains input variation, each task using a subset (§7.7, pp. 268–270) |
| Transfer / domain adaptation | a representation or a trained model across settings | many factors explaining variation in the source setting are relevant to the target (§15.2, p. 541) |
| Pretraining (unsupervised or supervised) | parameters across training stages | the earlier stage places the parameters in a better region (§15.1, p. 535; §8.7.4) |
| Parameter sharing | weights across positions or components | a known domain invariance (§7.9, p. 278) — handled by `SOP-DL-07` |

The criteria for judging whether a learned representation is any good also belong here. Every mechanism above
is a claim about representations, so those criteria sit in this SOP's scope.

Out of scope:

- capacity and regularization decisions on the labeled data alone (`SOP-DL-02`, `SOP-DL-03`)
- supervised pretraining as an *optimization* device (`SOP-DL-04` §3.4, repair 9)
- structural bias (`SOP-DL-07`)

## 2. Inputs and assumptions

- The labeled-data budget for the target task, and the size of any unlabeled or source-task corpus. That
  budget, not taste, selects the branch (see §3.5).
- The task specification from `SOP-DL-01`. State whether the input semantics or the output semantics are what
  varies across settings.
- A validation metric that can detect a *generalization* change. The mechanisms here are regularizers.
  Unsupervised pretraining, for example, does not lower training error. Unsupervised pretraining lowers test
  error (§15.1, p. 535).
- The willingness to state, for each mechanism, the check that would falsify that mechanism's licensing
  assumption.

## 3. Procedure

### 3.1 Semi-supervised (§7.6, pp. 267–268; §15.3, pp. 545–549)

1. State what semi-supervised learning means in this setting. Unlabeled samples from p(x) and labeled samples
   from p(x, y) both enter the estimate of p(y|x). In deep learning, that usually means **learning a
   representation of the form h = f(x)**. Same-class samples then get similar representations. Samples that
   are tightly clustered in input space should map to similar representations. In many cases a **linear
   classifier in the new space** then generalizes well. The classic variant is PCA as a preprocessing step
   before classification (§7.6, p. 267).
2. **Check the licensing assumption before you spend compute** (§15.3, pp. 545–547). The features of the ideal
   representation correspond to the **latent causes** of the observed data. Modeling p(x) therefore yields a
   good representation for p(y|x) only under one condition. The variable y must be a **recoverable** latent
   cause, or tightly correlated with one. The argument has a causal-graph form. The real process is a directed
   graph, in which x has the latent h as its parent. By Bayes' rule, structure in p(x) therefore helps to
   learn p(y|x).
   - The argument **fails** when p(x) is uniform. Observing x then gives no information about p(y|x).
   - The argument **works** when x is drawn from a mixture. Each value of y then has one well-separated
     component, and modeling p(x) locates every component. **One labeled sample per class** suffices.
   - The learner does not know which factor y corresponds to. The brute-force solution, to capture all causes,
     is infeasible. Two practical strategies are stated. Use the unsupervised and the supervised signals
     jointly, or learn larger-scale purely unsupervised representations.
3. Watch the criterion for implicit saliency. A fixed criterion such as pixel-level MSE implicitly decides what
   counts as "important". That decision can miss small but task-relevant objects. The book's ping-pong-ball
   example is one such object. A learned saliency criterion is the alternative. The cited work uses a
   generative adversarial model as that criterion. Note also the asymmetry result. If x is the effect and y is
   the cause, modeling p(x|y) is robust to changes in p(y) (§15.3, pp. 547–549).
4. Implement the mechanism as **shared parameters**, not as two separate models. The generative model p(x) or
   p(x, y) shares parameters with the discriminative model p(y|x). The supervised criterion −log p(y|x) is
   traded against the generative criterion. The generative criterion expresses prior knowledge of a particular
   form about the solution to the supervised problem. Control the weight of that criterion in the total
   criterion. That control gives a better trade-off than purely generative or purely discriminative training.
   The weight is a hyperparameter. Send its selection to `SOP-DL-05` (§7.6, p. 268).

### 3.2 Multi-task (§7.7, pp. 268–270)

5. Read the mechanism. Merging examples from several tasks acts as a **soft constraint on the parameters**.
   Extra training samples push parameters toward values that generalize better. In the same way, a part of the
   model that several extra tasks share is constrained to good values. That shared part usually generalizes
   better, *if the sharing is reasonable*.
6. Structure the model as the common form does (Fig. 7.2). All tasks share the same input x. All tasks also
   share an intermediate representation h^(shared), which learns a common pool of factors. The upper layers
   hold the task-specific parameters. Those parameters generalize well only from the samples of their own
   task. The lower layers hold the generic parameters. Those parameters benefit from the pooled data of all
   tasks. In the unsupervised case, some top-level factors need not be associated with any output task at
   all.
7. Expect the gain through **statistical strength**. The number of samples per shared parameter increases
   against the single-task regime. That increase improves generalization, and it improves the
   generalization-error bounds. Apply the book's own condition. The gain happens **only when the assumption
   that some statistical relationship exists between the tasks is reasonable**. In other words, the tasks must
   genuinely share some parameters (§7.7, p. 270).

### 3.3 Transfer and domain adaptation (§15.2, pp. 540–545)

8. Classify the situation:
   - **Transfer learning**: the learner performs two or more *different* tasks. The assumption is that many of
     the factors explaining variation in the source distribution are relevant to the target. The usual case is
     the same input with a different output. The book's example is cat/dog recognition transferred to
     ant/wasp.
   - **Domain adaptation**: the task and the optimal input-to-output map are identical. Only the input
     distribution differs slightly. The book's example is sentiment classification trained on books, video and
     music, then applied to electronics. Denoising-autoencoder pretraining worked well there.
   - **Concept drift**: transfer over time.
9. Choose *what* to share from what varies. The default factorization is a **shared representation at the
   bottom plus task-specific parameters at the top**. The book reuses its multi-task figure for this choice.
   Sometimes the *output* semantics are the shared part instead. The book's example is speech. In speech,
   valid sentences appear at the output, while the inputs are speaker-specific. In that case, share the
   **top** layers and use task-specific **preprocessing** (§15.2, pp. 541–542).
10. Check the conditions under which transfer helps. The shared features must correspond to latent factors
    that appear across settings. The source setting must have abundant data, so the target needs very few
    samples (§15.2, p. 541). Three extremes are named, and each carries an extra requirement:
    - **One-shot learning** — a transfer task with only one labeled sample.
    - **Zero-shot / zero-data learning** — no labeled samples at all. Zero-shot learning requires an extra task
      variable T, and the model estimates p(y | x, T). **T must be a generalizable representation, not a
      one-hot encoding**. Word embeddings are the cited example (§15.2, p. 543).
    - **Multimodal learning** learns the two input mappings and their relation jointly (§15.2, pp. 544–545).

> **Modern update (2017–2026) — a third factorization, and the zero-shot requirement realized.** Steps 8–10
> stand. The conditions of step 10 stand with those steps. Shared features must correspond to latent factors
> appearing across settings, and the source setting must have abundant data. Nothing below displaces those
> conditions.
>
> **(a) Step 9 gains a third option: freeze the base and adapt a low-rank increment.** The increment sits on
> the attention weight matrices. The 2016 options were to share the bottom, or to share the top and fine-tune
> jointly. Three properties make the third option a distinct decision point, not a cheaper approximation of
> the other two.
>
> - For the source's attention-based models, adaptation of **both** the query and the value projections
>   performed well. A fixed rank budget, distributed across the matrices, also performed well. Treat the target
>   matrices and the rank allocation as choices to validate for the model in use. Those choices are not
>   universal settings.
>
> - If the increment is **merged into the weights before inference**, inference adds no adapter-specific
>   forward-pass operations. Verify the merging cost and the task-switching cost for the actual deployment.
>
> - One frozen base can serve many tasks by swapping increments. Step 9's question then changes. The old
>   question was "which layers does this task share?" The new question is **"how many tasks must one stored
>   base serve?"**
>
> **Boundary on (a):** the quality claim is "on-par or better than fine-tuning" on the model families its
> source tested. No general ranking against full fine-tuning is implied. The parameter ratios and the memory
> ratios are that source's own measurements, not transferable constants (see `delta_map.md` §3.6).
>
> **(b) Step 10's zero-shot requirement is realizable with natural language as T. Its defining limit is a
> closed label set.** The 2016 requirement — T must be a generalizable representation, not a one-hot encoding
> — is **confirmed, not relaxed**. Four conditions attach to the realized form:
>
> - The classifier closes over a fixed concept set. The capability is therefore a *selection* capability, not
>   open-ended prediction.
>
> - The classifier generalizes poorly to data that is truly out-of-distribution for the model. The classifier
>   is weak on specialized, abstract or systematic tasks. Counting objects is the named example.
>
> - Prompt templates and their ensembling materially move the reported number. Prompt construction is
>   therefore a declared decision, not a detail.
>
> - **Do not select prompts on the benchmark's own validation set**. The source calls that practice
>   unrealistic for true zero-shot scenarios.
>
> The verbatim limitation quotes and the cross-dataset comparables are evidence that the capability is strongly
> dataset-dependent. Those records live in
> [`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.3 and in `delta_map.md` §3.7.
> This SOP does not reproduce those records.
>
> **Cross-links — do not duplicate.** Trustworthy-ML audits prompt-selection integrity through
> [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md). Trustworthy-ML audits the
> truly-OOD limitation through
> [`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md).
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §3.6, §3.7, §3.8.
> Sources: `LORA`; `CLIP`.*

### 3.4 Pretraining across stages (§15.1, pp. 533–540)

11. **Read the book's verdict before investing.** Greedy layer-wise unsupervised pretraining is **no longer
    necessary** to train fully-connected deep structures (§15.1, p. 534). Most algorithms no longer use
    unsupervised pretraining. The exception is natural language processing. There, words are one-hot vectors
    that carry no similarity information. Huge unlabeled corpora also exist there, so word embeddings are still
    in use (§15.1.1, p. 540). Greedy layer-wise pretraining was historically the first method able to train
    fully-connected deep supervised networks. Before 2006, only convolutional and recurrent deep networks were
    thought trainable (§15.1, p. 534).
12. If a run uses unsupervised pretraining, know what that pretraining is. Unsupervised pretraining is
    **a regularizer and a form of parameter initialization**. Unsupervised pretraining does not reduce training
    error. It reduces test error (§15.1, p. 535). Run pretraining as Algorithm 15.1 specifies:
    - Stack the layers, and pretrain each layer on the output of the previous layer.
    - Train layer k while the lower layers stay fixed. The algorithm adds the higher layers, and does **not**
      readjust the lower layers.
    - Optionally fine-tune all the layers jointly, with a supervised learner (§15.1, p. 534).
13. Expect the gain only in the low-label regime. The book states two caveats.
    - The first caveat covers when pretraining helps. Pretraining helps when the labeled samples are very few,
      and helps most when the unlabeled samples are very numerous. The deeper the pretrained network, the
      greater the reduction of test error. That reduction applies to both the mean and the variance of test
      error. The reason is that pretrained networks consistently stop in a **smaller region of function
      space**.
    - The second caveat covers the evidence. In one cited study, chemical activity prediction, pretraining was
      on average slightly negative. That study still found a marked gain on some problems. Those experiments
      **predate ReLU units, dropout and batch normalization**. So little is known about the combination of
      pretraining with current methods (§15.1.1, pp. 535–540).
14. Handle the two-stage drawbacks explicitly. No single knob controls the regularization strength. The
    hyperparameter feedback is delayed between the stages. Select the pretraining hyperparameters by
    **validation error in the supervised stage** (§15.1, p. 539).

> **Modern update (2017–2026) — the category that replaced greedy layer-wise pretraining.** Steps 11–14 are an
> accurate record of the 2016 verdict. That verdict was correct about the method that step 11 named.
> **Self-supervised learning** does not appear as a category in the 2016 book at all. The 2016 verdict
> therefore does not reach that category.
>
> 14a. **Do not apply step 11 to the wrong category.** Self-supervised learning manufactures supervision from
>      unlabeled data, in order to feed transfer learning. Self-supervised learning splits into the
>      **generative** (mask-and-predict) and the **contrastive** (pairwise relatedness) families. Step 11's
>      "no longer necessary" verdict is about greedy layer-wise pretraining of stacked layers. That verdict is
>      not evidence about either family. Measure transfer at the target label budget. Do not impose the 2016
>      low-label conclusion on modern methods.
>
> 14b. **For MAE-style masked-image pretraining**, test a high masking ratio. `MAE`'s source configuration used
>      ≈75% (see `delta_map.md` §3.3). Image redundancy can make a low-ratio reconstruction trivial. The MAE
>      design is asymmetric. The encoder receives only the visible patches. A lightweight decoder runs during
>      pretraining, and is not part of the transfer. Tune the ratio for the actual signal and the actual task.
>      That tuning is not a requirement for all generative self-supervised methods.
>
> 14c. **For SimCLR-style in-batch contrastive learning, check two design conditions.**
>    - *Test the augmentation composition.* In `SIMCLR`'s image setting, cropping without colour distortion
>      lets the model shortcut through colour statistics. Choose task-valid transformations. Audit
>      exploitable cues, rather than mandating that specific image recipe. The shortcut is a spurious-cue
>      failure. Trustworthy-ML
>      [`BM-02`](../../Benchmark/Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md) audits that failure.
>        This SOP records the composition requirement, and does not restate the audit.
>
>    - *The resource budget matters for this in-batch-negative design.* `SIMCLR` benefited from larger batches
>      and from more training steps than its supervised comparisons. Declare the batch, the negatives and the
>      training budget. Do not extrapolate that resource requirement to every contrastive method. Record
>      resources under [`SOP-DL-02`](SOP-DL-02-diagnose-fitting-regime-and-capacity.md) §3.5. The source's
>      values remain in `delta_map.md` §3.4.
>
> 14d. **For SimCLR, evaluate the pre-projection representation.** The nonlinear projection head of SimCLR
>      serves contrastive training. Read the transferred representation **before** that head. Record the
>      feature stage that you export. Report the loss normalization and the temperature when you reproduce
>      SimCLR. Other self-supervised architectures require their own readout choice.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §3.3, §3.4, §3.5.
> Sources: `UDL` §9.3.7; `MAE`; `SIMCLR`.*

### 3.5 Let the labeled-data budget decide

15. Apply the book's dataset-size rule. That rule is the operational core of this SOP (§15.1.1, p. 540):
    - **Large labeled datasets**: supervised regularization techniques reach human-level performance. The book
      names dropout and batch normalization. Unsupervised pretraining is not the lever here.
    - **Medium datasets**: those supervised techniques **beat** unsupervised pretraining. The book's examples
      are CIFAR-10 and MNIST, with roughly 5000 labeled samples per class.
    - **Very small data**: **Bayesian** methods beat pretraining. The book's example is the splice dataset.
    Carry the related threshold from `SOP-DL-03`. Dropout was ineffective below roughly 5000 samples in the
    cited comparison (§7.12, p. 290).
16. Note the domain asymmetry that the book records for the first baseline. Natural language processing
    benefits greatly from unsupervised techniques such as learned word embeddings. Computer vision showed no
    such benefit at the time, except in semi-supervised settings with very few labels. Include unsupervised
    learning in the first end-to-end baseline only where the domain deems it important. Otherwise try
    unsupervised learning first, when the initial baseline is found to overfit (§11.2, p. 440).

### 3.6 Understand why sharing works, and prefer distributed factors (§15.4, pp. 549–554)

17. Share at the level of **factors, not symbols**. The statistical advantage of that sharing is exponential.
    The count runs as follows. n features with k values describe kⁿ concepts. A distributed representation with
    n linear-threshold features assigns unique codes to O(n^d) input regions. That representation uses O(nd)
    parameters. A nearest-neighbour scheme with n samples distinguishes only n regions (§15.4, pp. 549–554).
    `concept_reconstruction.md` §4.1(c) lists the contrast class, which names the representations that are
    *not* distributed. The operative consequence is simple. The squared L2 distance between any two distinct
    one-hot vectors is 2. One-hot encodings therefore carry no similarity information (§15.1.1, p. 537). That
    missing information is why zero-shot transfer requires a generalizable T.
18. Use the regularization reading. A strong representation, used with a weak (linear) classifier, is itself a
    strong regularizer. The VC dimension of deep linear-threshold networks is only O(w log w) in the number of
    weights. That reading is checkable, not merely asserted. Hidden units in networks trained on ImageNet and
    Places are interpretable. Directions in a face-generating model separate gender from eyeglasses (§15.4,
    pp. 554–555). Treat both findings as observational evidence for the existence of distributed factors, not
    as a metric.
19. Treat depth as a sharing lever with an exponential payoff. Some functions that a depth-k network can
    represent need exponentially many units at depth 2. The same holds at depth k − 1. The result extends to
    sum-product networks, and to families of convolutional-network circuits (§15.5, pp. 555–556). Pair that
    treatment with the matched-parameter-count discipline of `SOP-DL-07`.
20. When you choose what to share, use the book's list of general priors for discovering latent causes (§15.6,
    pp. 556–558). `concept_reconstruction.md` §4.1(c) holds the full list. Three priors most often decide a
    sharing question:
    - **factors shared across tasks**: each output ties to a subset of a common factor pool. The sharing of
      p(h|x) therefore shares statistical strength.
    - **natural clustering**: each connected manifold receives one class. That clustering motivates tangent
      propagation, double backpropagation, the manifold-tangent classifier and adversarial training.
    - **smoothness / local constancy**.

### 3.7 Judge whether the representation is actually good (§14)

21. Do not accept reconstruction error alone. With a linear decoder and MSE, an undercomplete autoencoder
    simply recovers the **PCA subspace**. If the capacity is too large, the autoencoder learns the **identity**
    and captures nothing (§14.1, pp. 511–512). The code must reflect the distinctive statistical structure of
    the training set. The code must not act as an identity function (§14.2, p. 512).
22. Apply the criteria that the book actually gives, **each against its own appropriate control**.
    `BC-DL-12` §3 holds the per-criterion baseline table.
    - **Linear / undercomplete regime only**: a learned code in *that* regime must beat PCA at matched
      dimension (§13.5, p. 509; §14.1, pp. 511–512). The minimization of reconstruction error, with a linear
      encoder and a linear decoder, yields tied and orthonormal weights. Those weights span the principal
      eigenvectors of the covariance. The theorem covers only that configuration. It is **not** a universal
      yardstick for nonlinear manifold, contractive, counting or encoding claims.
    - **Manifold criterion**: judge that criterion against the orthogonal-direction response of the same
      encoder. A good code is sensitive only along manifold-tangent directions, and insensitive to the
      orthogonal ones. Reconstruction pulls one way, and the constraint pulls the other way (§14.6,
      pp. 523–524).
    - **Contractive criterion**: judge that criterion against the spectrum of the untrained encoder. The
      penalty is the squared Frobenius norm of the encoder Jacobian. A Jacobian is contractive when ‖Jx‖ ≤ 1
      for every unit x. After training, **most singular values are below 1**. The directions of the largest
      singular values correspond to the learned tangent directions. In the small-Gaussian-noise limit, the
      denoising reconstruction error equals the contractive penalty. **Tie the decoder weights to the
      transpose of the encoder**. Otherwise the degenerate small-constant solution appears (§14.7,
      pp. 527–530).
    - **Downstream utility**: judge that criterion against PCA-based codes and against raw inputs. That is the
      book's own comparison. Semantic hashing places semantically related samples close together. The cited
      30-unit bottleneck achieves lower reconstruction error than 30-dimensional PCA. The same bottleneck gives
      more interpretable and better class-separated codes (§14.9, p. 531).
23. Choose the regularized-autoencoder variant by what that variant penalizes: sparse, denoising, or
    derivative-penalty/contractive. `concept_reconstruction.md` §4.1(c) holds the catalogues (§13,
    pp. 497–509; §14.2, pp. 512–516; §14.5, p. 518). The catalogue covers the variant menu, the denoising
    training procedure, and the baseline family of linear-factor models. That family holds factor analysis,
    probabilistic PCA, ICA and its identifiability requirement, slow feature analysis, and sparse coding.

### 3.8 Record the decision

24. For each adopted or rejected mechanism, record the following:

    - the licensing assumption
    - the check performed on that assumption
    - the trade-off coefficient searched
    - the representation-quality criteria used beyond reconstruction error
    - the labeled-data branch that selected the mechanism
    - the observation that would falsify that choice

> **Modern update (2017–2026) — three further items to record.** Step 24's list is unchanged. Some modern
> options at §3.3 or §3.4 carry extra reporting items. Where such an option was available, add the §5 items for
> that case to the record.
>
> - the factorization chosen. For a frozen base, record how many tasks that base must serve.
>
> - the self-supervised family, with its masking ratio or its augmentation composition, and with its resource
>   budget.
>
> - for a zero-shot construction, the closed label set, with the split that the prompts were selected on.
>
> *Delta: `delta_map.md` §3.3, §3.4, §3.6, §3.7.*

## 4. Important failure modes

- **Using unlabeled data when p(x) carries no information about p(y|x)** — the uniform-p(x) case (§15.3,
  pp. 545–546).
- **Multi-task sharing without a genuine statistical relationship** between the tasks. The gain is conditional
  on that assumption (§7.7, p. 270).
- **One-hot task variables in a zero-shot setting**. Those variables carry no similarity information, so the
  model generalizes to no unseen task (§15.2, p. 543; §15.1.1, p. 537).
- **Unsupervised pretraining on a large labeled dataset**, where the supervised regularizers already reach the
  target (§15.1.1, p. 540).
- **Selecting the pretraining hyperparameters in the unsupervised stage**, instead of by the supervised-stage
  validation error (§15.1, p. 539).
- **Judging a representation by reconstruction error alone**. That error gives an identity function, or an exact
  equivalence to PCA under a linear decoder (§14.1, pp. 511–512; §13.5, p. 509).
- **An untied decoder in a contractive autoencoder**. That decoder produces the degenerate small-constant
  solution (§14.7, p. 530).
- **Sharing the wrong end of the network**. Suppose the output semantics are the shared part, and the inputs
  are what vary. Then the top layers take the sharing, and the preprocessing becomes task-specific. That is
  the opposite of the default (§15.2, pp. 541–542).
- **Assuming transfer helps when the source setting is not data-rich** relative to the target (§15.2, p. 541).
- **Treating pretraining's benefit as established for current methods**. The supporting experiments predate ReLU
  units, dropout and batch normalization. Little is known about the combination with current methods, and the
  book says so (§15.1.1, p. 539).
- **Reading a fixed reconstruction criterion as task-neutral**. That criterion embeds a saliency judgement, and
  can miss small task-relevant structure (§15.3, pp. 547–548).

Modern-update failure modes (rules in §3.3 and §3.4 above; delta references given per item):

- **Applying step 11's "no longer necessary" verdict to self-supervised pretraining.** That verdict is about
  greedy layer-wise pretraining of stacked layers. Self-supervised learning is a different category, and does
  not appear in the 2016 book as one (`delta_map.md` §3.3).
- **Reading out the representation after the projection head.** The projection head is discarded at transfer
  time (`delta_map.md` §3.4).
- **Composing augmentations that leave an exploitable cue.** Cropping without colour distortion invites a
  colour-statistics shortcut, and that shortcut defeats the objective (`delta_map.md` §3.5).
- **Budgeting a contrastive run as if that run had a supervised run's resource profile.** The result then
  measures the budget rather than the method (`delta_map.md` §3.4).
- **Treating a zero-shot classifier as open-ended prediction.** The classifier that was constructed closes the
  label set (`delta_map.md` §3.7).
- **Selecting zero-shot prompts on a benchmark validation set.** Trustworthy-ML `BM-08` owns that integrity
  failure. This SOP does not evaluate it (`delta_map.md` §3.8).
- **Rejecting low-rank adaptation without checking its deployment mode.** Merging an increment into the weights
  can eliminate adapter-specific forward-pass overhead. Unmerged adapters and task switching have
  implementation-dependent costs (`delta_map.md` §3.6).

## 5. Outputs and reporting

- Keep the **sharing decision record**. That record holds the mechanism, the licensing assumption, the check run
  on that assumption, and the falsification condition.
- Record the labeled-data budget, and the branch that budget selected (large / medium / very small). Record the
  technique that branch favours.
- For semi-supervised runs: record the generative-criterion weight that you searched, and the value chosen for
  that weight.
- For multi-task runs: record the split between the shared lower parameters and the task-specific upper
  parameters. Record the evidence that the tasks share factors.
- For transfer runs: record the source setting and the target setting. Record the shared part, namely the bottom
  representation, the top layers, or a trained model. Record the data-abundance condition.
- **Modern update (2017–2026) — three additional reporting lines.**
  - *Transfer runs:* record which factorization was chosen. For a frozen base with a low-rank increment, record
    the number of served tasks. Record the state of the increment at inference, merged or unmerged, and the
    relevant latency or task-switching costs.
  - *Self-supervised pretraining runs:* record the family (generative or contrastive), and the masking ratio or
    the augmentation composition. Record the batch size and the step count actually used. Confirm that the
    transferred representation came from before any projection head.
  - *Zero-shot constructions:* record the closed label set. Record the prompt templates, and whether those
    templates were ensembled. Record **which split the prompts were selected on**. Selecting prompts on a
    benchmark validation set is an integrity failure owned by Trustworthy-ML
    [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md).
- For pretraining runs: record the stacking procedure, and whether the lower layers stayed frozen. Record the
  fine-tuning step, and the supervised-stage validation error used to select the pretraining hyperparameters.
- Keep the **representation-quality report**. Report the reconstruction error **plus** the control appropriate to
  each criterion claimed. The PCA control applies only to linear / undercomplete-autoencoder comparisons. The
  orthogonal-direction response applies to the manifold criterion. The untrained Jacobian spectrum applies to
  the contractive criterion. PCA-based codes and raw inputs apply to downstream utility (`BC-DL-12` §3).
- Record anything the book leaves open, and that you therefore chose:

  - the generative-criterion weight
  - the number of pretrained layers
  - the code dimension
  - the sparsity target
  - the contraction penalty weight

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

**Modern-update provenance.** Every row above is a 2016-book locator, and none was altered. The modern update
adds three blocks, plus the matching entries in §4 and §5:

- §3.3 step 10 — the third factorization, the realized zero-shot case, and its closed label set
- §3.4 step 14 — self-supervised pretraining as a category, with steps 14a–14d
- §3.8 step 24 — a pointer to the §5 reporting lines

The detailed evidence, the verbatim source quotations and the sources' own result figures are **not**
reproduced here. Those records live in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§3.3, §3.4, §3.5, §3.6, §3.7 and §3.8. They also live in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.2–§2.4. Source keys: `UDL` §9.3.7
and §9.3.8, `MAE`, `SIMCLR`, `LORA` and `CLIP`. Three capabilities are **cross-linked rather than restated**:

- the spurious-cue audit → Trustworthy-ML
  [`BM-02`](../../Benchmark/Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md)
- the evaluation-integrity audit →
  [`BM-08`](../../Benchmark/Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md)
- distribution shift →
  [`BM-01`](../../Benchmark/Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md)

**Historical boundary.** This SOP contains the most era-bound material in the package. The book marks that
material itself. Treated as historical:

- greedy layer-wise unsupervised pretraining as the trigger of the 2006 revival, and its present obsolescence
  except for NLP word embeddings (§15.1, p. 534; §15.1.1, p. 540)
- the 2011 transfer-learning competitions won by unsupervised pretraining on target tasks, with a few to a few
  dozen labels per class (§15.1.1, p. 537)
- the named datasets (CIFAR-10, MNIST with about 5000 labels per class, the splice dataset, ImageNet, Places,
  QMUL Multiview Face)
- the cited architectures and experiments (RBM and deep autoencoder stacks with a 30-unit bottleneck,
  discriminative RBMs and ladder networks as single-stage semi-supervised methods, predictive generative
  networks, the face-generating model, ImageNet/Places interpretability, contractive-autoencoder tangent
  visualization on a CIFAR-10 dog)
- the then-current verdicts. Semi-supervised and multi-task gains are real, but are assumption-dependent and
  hard to predict. Supervised ImageNet pretraining became the popular successor in transfer learning
  (§15.2, p. 540).

The general mechanisms are stated as general, and are retained:

- what licenses semi-supervised learning
- why multi-task sharing adds statistical strength
- what transfer requires
- the exponential advantage of distributed representations
- the criteria for judging a representation

The modern update amended the closing sentence of this note. That sentence previously stated that no post-2016
pretraining paradigm enters the procedure. That statement is no longer true of the file as a whole. The 2016
procedure above still introduces none.

Steps 14a–14d of §3.4 add self-supervised pretraining, as the category that replaced greedy layer-wise
pretraining. §3.3 adds a frozen-base low-rank factorization, and adds language-as-task-variable zero-shot
transfer. Each modern update is marked in place, with its own sources. The 2016 verdicts in steps 11–13 are
retained as history, not rewritten. Step 11's "no longer necessary" verdict was correct about the method named
in step 11.
