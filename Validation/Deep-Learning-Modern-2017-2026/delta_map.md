# Delta map — Deep Learning modern update (2017–2026)

Every candidate delta is recorded in the form the plan mandates:

`2016 baseline → modern delta → source → destination → boundary`

Sources are cited by the keys defined in [`sources.md`](sources.md) §2.1. `UDL` citations use the form
`UDL §section, fol. N` (printed folio = PDF page − 14; see `sources.md` §1.1 for why the folio is
indicative and the section number is the stable part). 2016 citations use the form the 2016 package
already uses (`§section, p. N` = PDF page of that e-copy).

## Status taxonomy

| Status | Meaning |
| --- | --- |
| **A-extend** | Accepted; lands as a minimal extension to an existing Deep-Learning-2016 SOP or BC, carrying a modern-update provenance note. |
| **A-crosslink** | Accepted, but the capability is already owned by a Trustworthy-ML artifact. A pointer is added; nothing is duplicated. |
| **R** | Record-only. Method-specific, weakly supported, unsettled, or theoretical. Stays in this file and in no artifact. |
| **X** | Rejected. Reason stated. |

The plan's comparison rule is applied throughout: a topic name shared with an existing artifact is not
evidence of coverage, and a new model family is not evidence of a new capability. Conversely, a delta is
**not** accepted just because it is modern — it is accepted only when it changes a reusable research
workflow or an evaluable claim that an existing artifact already owns.

Net artifact decision: **no new SOP and no new BC.** Eleven existing SOP/BC artifacts receive modern extensions
(§6). This is a consequence of the per-item judgements below, not a target set in advance.

---

## 1. Scale and resources

### 1.1 Compute becomes a third declared axis — **A-extend**

- **2016 baseline.** `SOP-DL-02` §3.3–§3.5 reasons over two axes only — capacity and dataset size — and
  §3.5 decides whether to collect more data. Compute appears in the 2016 book only as a hyperparameter
  *search* budget (§11.4, p. 442). There is no allocation decision between model size and data at fixed
  compute, because the book never poses one.
- **Modern delta.** At a fixed compute budget there is an explicit allocation choice between parameters
  and training examples/tokens, and the choice is a first-class decision with a nameable assumption
  attached to it.
- **Source.** `SCALE` (power laws in N, D, C, each holding only under stated conditions); `CHINCHILLA`
  (equal-proportions scaling); `UDL` §20.1.1, fol. 403.
- **Destination.** `SOP-DL-02` §3.5 — add compute to the declared axes and require the allocation
  assumption to be recorded.
- **Boundary.** The SOP records *that* an allocation rule must be declared and under what conditions it
  was fitted. It does **not** adopt an exponent. See §1.2.

### 1.2 The allocation exponents, and the fact that they are contested — **R**

- **2016 baseline.** No counterpart; the 2016 book has no allocation law.
- **Modern delta.** `SCALE` fits N ∝ C^0.73 and D ∝ C^0.27 (α_N ≈ 0.076, α_D ≈ 0.095, α_Cmin ≈ 0.050) and
  concludes that optimal compute-efficiency means training very large models on relatively modest data
  and stopping well before convergence. `CHINCHILLA` fits a ≈ b ≈ 0.50 across three independent methods
  and concludes model size and tokens should be scaled equally, attributing the discrepancy to `SCALE`'s
  use of a fixed number of training tokens and learning-rate schedule for all models.
- **Source.** `SCALE`, `CHINCHILLA`.
- **Destination.** None. Record-only.
- **Boundary.** Two sources in the plan's own list disagree on the quantity, and both self-report
  extrapolation uncertainty ("significant uncertainty extrapolating out many orders of magnitude"; "only
  two comparable training runs at large scale"; `SCALE`: "at present we do not have a solid theoretical
  understanding", trends "must eventually level off"). An artifact that printed either exponent would be
  printing an unsettled number. The plan directs unsettled items here.
- **What is retained.** The *existence and direction* of the disagreement is carried into §1.1 as the
  reason the allocation assumption must be declared rather than assumed. That part is robust.

### 1.3 The parameters-to-data ratio is not a well-defined quantity — **A-extend**

- **2016 baseline.** `SOP-DL-02` §3.2 classifies the fitting regime by comparing model capacity against
  dataset size; `BC-DL-02` tests the capacity curve and the training-set-size curve as if both axes were
  directly measurable.
- **Modern delta.** The ratio itself is ill-defined once augmentation and tokenization enter. `UDL`'s
  worked case: AlexNet had ~60M parameters trained on ~1M data points, but each training example was
  augmented with 2048 transformations; GPT-3 had 175B parameters trained on 300B tokens. "There is not a
  clear-cut case that either model was overparameterized."
- **Source.** `UDL` §20.1.1, fol. 403.
- **Destination.** `SOP-DL-02` §3.6 (interpret without over-claiming) and `BC-DL-02` §6 (validity limits).
- **Boundary.** This is a *measurement* caveat about an axis the 2016 artifacts already use, not a new
  axis. It does not license any conclusion about whether a given model is over- or under-parameterized.

### 1.4 Double descent removes the U-curve's right branch as a stopping rule — **A-extend**

- **2016 baseline.** `SOP-DL-02` §3.4 reasons with the U-curve: test error falls, reaches a minimum, then
  rises with further capacity, and the practitioner samples points on that curve. `BC-DL-02` tests whether
  the capacity curve actually has that shape.
- **Modern delta.** The curve can descend again. `UDL` distinguishes three regimes and reports a second
  descent beyond the interpolation threshold, and is explicit that the explanation is putative. It is also
  explicit that the phenomenon is **dataset-dependent** — present on MNIST with the original data, but
  emerging or becoming prominent with label noise, and on MNIST-1D and CIFAR-100. `UDL` §8.5, fol. 132
  states the operational consequence directly: "in the modern regime, there is no way to tell how much
  capacity should be added before the test error stops improving."
- **Source.** `UDL` §8.4, fol. 127–132 (citing Belkin et al. 2019 and Nakkiran et al. 2021); `UDL` §8.5,
  fol. 132.
- **Destination.** `SOP-DL-02` §3.4 (the U-curve reasoning step) and §3.6; `BC-DL-02` §5 (how to interpret
  failure) — the modern arm asks whether a second descent appears **on the data actually in use**, since
  that is what the source makes conditional.
- **Boundary.** No mechanism is asserted, because the source does not settle one. No threshold is supplied
  for where the interpolation point sits — it is a property of the run. The 2016 U-curve text is not
  rewritten; it is annotated as era-scoped.

### 1.5 Overparameterization is evidence-backed, not merely tolerated — **A-extend**

- **2016 baseline.** `SOP-DL-02` §3.3–§3.4 and `BC-DL-02` treat excess capacity as something to be
  regularized away, following the 2016 book's capacity/generalization framing.
- **Modern delta.** `UDL` §20.5, fol. 415–418 reports that "there are almost no examples of
  state-of-the-art test performance on complex datasets where the model has significantly fewer parameters
  than there were training data points", that pruning results still leave networks over-parameterized
  (Han et al. 2016 retaining 8% of VGG's weights, where VGG already has ~100× ImageNet's data count in
  parameters; Frankle & Carbin 2019 lottery tickets cutting VGG-19 by 98.5% on CIFAR-10 and ResNet-50 by
  80% on ImageNet — "these networks are still over-parameterized after pruning"), that "distillation has
  not yet provided convincing evidence that under-parameterized models can perform well", and concludes
  that "current evidence suggests that overparameterization is needed for generalization — at least for
  the size and complexity of datasets that are currently used". Bubeck & Sellke (2021): in D dimensions,
  smooth interpolation requires D times more parameters than mere interpolation.
- **Source.** `UDL` §20.5, fol. 415–418.
- **Destination.** `SOP-DL-02` §3.6; `BC-DL-02` §5–§6.
- **Boundary.** The source scopes this to current dataset sizes and complexities, and leaves open whether
  small models fundamentally cannot perform or training merely cannot find good solutions for them. The
  artifact carries that open question rather than resolving it.

### 1.6 Compute and resource reporting discipline — **A-crosslink**

- **2016 baseline.** The 2016 package reports search budget and run configuration but has no
  resource-reporting obligation of its own.
- **Modern delta.** Compute, hardware and allocation must be reported as evidence, not as background.
- **Source.** `SCALE`, `CHINCHILLA`, `VIT` (all state compute conditions as part of the claim).
- **Destination.** Cross-link to Trustworthy-ML `SOP-08` (report evidence and validity boundaries). No
  text duplicated into the Deep-Learning artifacts.
- **Boundary.** The Deep-Learning lineage owns *what to decide* about compute (§1.1); Trustworthy ML owns
  *how to report* it.

### 1.7 Architecture-variant and parameter-count specifics — **R**

- ImageGPT's 6.8B parameters at 64×64 with 9-bit colour quantization and 27.4% top-1 on ImageNet resized
  to 48×48; ViT-H/14 87.8% top-1 on ImageNet-1K under `MAE` pretraining; ViT 16×16 patches with supervised
  pretraining on 303M labeled images from 18,000 classes reaching 11.45% top-1 error; `FM`'s bits/dim at
  32×32, 64×64 and 128×128. **Source:** `UDL` §12.10, fol. 229–230; `MAE`; `FM`. **Destination:** none.
  **Boundary:** these are single-configuration results. The plan forbids an architecture encyclopaedia and
  forbids one artifact per method. The *structural* claims these numbers support are carried separately at
  §2.2 and §2.3.

### 1.8 Conditional hyperparameters change what a search sampler does — **A-extend**

- **2016 baseline.** `SOP-DL-05` and `BC-DL-09` treat the search space as a fixed product over named
  hyperparameters, and compare random against grid sampling at matched budget (§11.4.3–§11.4.4,
  pp. 443–447).
- **Modern delta.** `UDL` §8.5, fol. 133 splits hyperparameters into **discrete** and **conditional** ones
  and names architecture search as its own activity. A conditional hyperparameter is undefined unless its
  parent takes a particular value, so a plain product-space sampler assigns budget to points that do not
  exist and mis-counts the space it is searching.
- **Source.** `UDL` §8.5, fol. 133.
- **Destination.** `SOP-DL-05` §3 — declare which hyperparameters are conditional before sampling, and
  state how the sampler handles undefined branches.
- **Boundary.** No architecture-search method is endorsed. `SCALE`'s counterweight — architecture details
  such as width vs. depth "have minimal effects within a wide range" — is recorded here as a tension, with
  the note that it is a language-model result and is not generalized by this lineage.

---

## 2. Architecture — attention and the changed assumptions behind sequence and vision modeling

### 2.1 Sequence modeling need not be sequential — **A-extend**

- **2016 baseline.** `SOP-DL-07` §3.1 lets data structure select the model class and is already declared a
  2016 default: sequential data → recurrent network, spatial data → convolutional network. Long-range
  dependency is bounded by the recurrent path (`BC-DL-06`, §8.2.5, §10.7).
- **Modern delta.** A self-attention layer connects all positions with a constant number of sequentially
  executed operations, dispensing with recurrence and convolutions entirely; self-attention layers are
  faster than recurrent layers when the sequence length is smaller than the representation dimensionality;
  shorter paths between positions make long-range dependencies easier to learn.
- **Source.** `ATTN` (abstract and §4); `UDL` §12.1–12.2, fol. 207–209.
- **Destination.** `SOP-DL-07` §3.1 — the selection rule's era-binding is already declared there; the
  extension states what the modern rule adds. `BC-DL-06` §6 / Historical boundary — the 2016 structural
  limit is architecture-bound.
- **Boundary.** No transformer architecture is specified or endorsed. The delta is that *recurrence is not
  a precondition for sequence modeling*, which is what changes the 2016 selection step.

### 2.2 The conditions that motivate attention are a bias-register entry — **A-extend**

- **2016 baseline.** `SOP-DL-07` §3.2 maintains a bias register listing each prior an architecture encodes
  (sparse interaction, parameter sharing, equivariance, pooling, depth) with the data property that
  licenses it.
- **Modern delta.** `UDL` §12.1–12.2, fol. 207–209 states the motivating conditions in exactly the
  register's shape: very many input variables; similar statistics at every position; variable sequence
  length that cannot simply be resized; content-dependent long-range connections.
- **Source.** `UDL` §12.1–12.2, fol. 207–209.
- **Destination.** `SOP-DL-07` §3.2 — one new register row.
- **Boundary.** The register records the prior and the data property that licenses it. It does not rank
  architectures, consistent with the 2016 package's standing rule that a model family is not a benchmark.

### 2.3 A low-bias architecture can supersede a high-bias one, conditionally — **A-extend**

- **2016 baseline.** `SOP-DL-07` §3.1 and `BC-DL-08` treat convolutional equivariance as the prior that
  spatial data licenses, and the 2016 book's §9 case for convolutions is unconditional in practice.
- **Modern delta.** "Convolutional nets have a good inductive bias because each layer is equivariant to
  spatial translation, and takes into account the 2D structure of the image. However, this must be learned
  in a transformer network." Transformers eclipsed CNNs "partly because of the enormous scale … and the
  large amounts of data that can be used to pre-train", and — the load-bearing sentence — "**The strong
  inductive bias of convolutional networks can only be superseded by employing extremely large amounts of
  training data**." `VIT` states the same condition from the other side: pre-trained on large data and
  transferred to mid-sized or small benchmarks, ViT attains excellent results with substantially fewer
  computational resources, but on ImageNet-scale training only it self-reports accuracies below comparable
  ResNets.
- **Source.** `UDL` §12.10, fol. 229–230; `VIT` (abstract, introduction, conclusion).
- **Destination.** `SOP-DL-07` §3.1; `BC-DL-08` §2 — the equivariance arm gains a **given versus learned**
  comparison condition, which is the same test with one new arm, not a new benchmark.
- **Boundary.** The claim is conditional on pretraining scale in both sources. The unconditional form
  ("ViT beats CNNs") is rejected at §7.2.

### 2.4 Attention's cost is a different bound on the same axis — **A-extend**

- **2016 baseline.** `BC-DL-06` and `SOP-DL-07` treat the long-range-dependency limit as a gradient-path
  property of recurrence, with the spectral account predicting the learnable span (§8.2.5, pp. 310–311).
- **Modern delta.** Attention removes the recurrence-depth path but pays quadratic complexity in sequence
  length, which bounds the usable length instead; `UDL` lists the sparsification options as the response.
- **Source.** `UDL` §12.9, fol. 227–228; `ATTN` §4.
- **Destination.** `BC-DL-06` §6 and Historical boundary — a boundary note, not a new test arm.
- **Boundary.** No sparsification method is endorsed or compared; they are named as a category only. The
  2016 spectral account is left intact for recurrent models, which remain its scope.

### 2.5 Depth's role is contested in a way the 2016 package already declined to test — **R**

- **2016 baseline.** Depth-versus-width superiority was an explicitly **rejected** BC candidate in the 2016
  package, because the §6.4.2 20M→60M observation is matched-parameter and experiment-specific.
- **Modern delta.** `UDL` §20.6, fol. 418–419: residual connections and batch normalization allowed deeper
  training with commensurate gains; "the balance of evidence suggests that depth is critical; even the
  shallowest networks with good image classification performance require >10 layers. However, there is no
  definitive explanation for why." Counter-evidence recorded there: Zagoruyko & Komodakis (2016)
  wider-shallower ResNets; Goyal et al. (2021) a 12-layer parallel-channel network; **Veit et al. (2016)
  showing predominantly shorter paths of 5–17 layers drive performance in residual networks**. The
  depth-separation results (Eldan & Shamir 2016; Telgarsky 2016; Liang & Srikant 2016) are qualified by
  Nye & Saxe (2018), who found some cannot easily be fit in practice and "little evidence that the
  real-world functions that we are approximating have these pathological properties". Urban et al. (2017)
  distillation is the direction that does support depth: shallow students could not replicate a deeper
  teacher, and student performance increased with depth at constant parameter budget.
- **Source.** `UDL` §20.6, fol. 418–419; `UDL` ch. 11 summary, fol. 186 (residual blocks cause an
  exponential increase in activation magnitudes at initialization, compensated by batch normalization).
- **Destination.** `BC-DL-08` §5 — an interpretation note only, so that a depth arm's result is read
  against the counter-evidence rather than as a settled hierarchy.
- **Boundary.** Still no depth-versus-width benchmark. The 2016 rejection stands; this row records why the
  modern evidence does not overturn it.

### 2.6 Architecture variants as such — **X**

Rejected: Transformer and ViT entries of their own. The plan forbids a history of architectures and one
artifact per method, and the 2016 package's standing rule that a model family is not a benchmark is
carried forward into this lineage. Only the prior each architecture encodes enters, via §2.2–§2.3.

---

## 3. Training and adaptation

### 3.1 L2 regularization and weight decay are not the same lever under adaptive optimizers — **A-extend**

- **2016 baseline.** `SOP-DL-03` §3.2's lever table lists L2/weight decay as one regularization lever, and
  §3.3 configures it with a single coefficient. The 2016 book does not separate the two for adaptive
  methods.
- **Modern delta.** L2 and weight decay are equivalent for standard SGD when rescaled by the learning rate,
  but not for adaptive gradient algorithms: with L2 both the loss gradient and the λ·w gradient are
  normalized by their typical summed magnitudes, so weights with large historic gradient magnitudes are
  regularized less than they would be under weight decay. Decoupled weight decay regularizes all weights at
  the same rate λ, and decouples the optimal decay setting from the learning-rate setting. `UDL` states the
  same delta in one sentence: "for Adam, the learning rate α is different for each parameter, so L2
  regularization and weight decay differ. Loshchilov & Hutter (2019) present AdamW, which modifies Adam to
  implement weight decay correctly and show that this improves performance."
- **Source.** `ADAMW` (abstract, §2, Algorithm 2); `UDL` §9.1, fol. 156.
- **Destination.** `SOP-DL-03` §3.3 (configure the chosen lever).
- **Boundary.** No λ value is supplied — `ADAMW`'s λ_norm = 0.025 / 0.05 are batch-budget-normalized values
  from its own experiments, and its Appendix B.1 normalization is described by the paper itself as "merely
  one possibility informed by few experiments". The scheduling mechanism is cited as `SetScheduleMultiplier`
  η_t; the specific "multiply by η_t/η_init" form was **not verified verbatim** and is not used
  (`sources.md` §2.4). `ADAMW`'s Bayesian-filtering justification is explicitly theoretical and, in the
  paper's own words, "does not directly apply to practical adaptive gradient algorithms", so it is not
  carried as a mechanism claim.

### 3.2 The era-default optimizer ordering has changed — **A-extend**

- **2016 baseline.** `SOP-DL-03` §3.2 and `SOP-DL-04` §3.4 treat the optimizer as one lever among several,
  and the 2016 book's §8.5.4 explicitly reports no consensus — which is why the 2016 package rejected an
  optimizer leaderboard and why `BC-DL-05` was reframed as a diagnostic probe suite.
- **Modern delta.** Adam is less sensitive to the initial learning rate and "doesn't need complex learning
  rate schedules"; SGD is a special case of Adam (β = 0, γ → 1); Choi et al. (2019) found that a *searched*
  Adam matches SGD and converges faster; SWATS switches from Adam to SGD mid-training.
- **Source.** `UDL` §6.4, fol. 88–90.
- **Destination.** `SOP-DL-03` §3.2 and `SOP-DL-04` §3.4 — notes on the regularization lever and optimizer-repair menu; neither creates an optimizer ranking.
- **Boundary.** **No ranking is produced.** The delta is that the sensitivity-to-learning-rate assumption
  behind the 2016 ordering no longer holds; the choice remains problem-dependent, and the 2016 package's
  rejection of an optimizer leaderboard is reaffirmed rather than reversed. `SOP-DL-04`'s repair menu is not
  re-ordered.

### 3.3 Self-supervised pretraining replaces greedy layer-wise pretraining — **A-extend**

- **2016 baseline.** `SOP-DL-08` §3.4 records the 2016 verdict: greedy layer-wise unsupervised pretraining
  is no longer necessary to train fully-connected deep structures (§15.1, p. 534), most algorithms no longer
  use it, and the surviving case is NLP word embeddings (§15.1.1, p. 540). Where used, it is a regularizer
  and a form of initialization that reduces test but not training error, and the gain is confined to the
  low-label regime.
- **Modern delta.** The category that replaced it is **self-supervised learning**, absent as a category from
  the 2016 book. `UDL` §9.3.7, fol. 152–153 frames it as creating "free" labeled data to feed transfer
  learning, and splits it into generative (mask-and-predict) and contrastive (pairwise relatedness)
  families. The two structural mechanisms: masking a high proportion of the input — e.g. 75% — yields a
  nontrivial self-supervisory task, and an asymmetric encoder–decoder that shows the encoder only visible
  patches and uses a lightweight decoder **only during pretraining** gives 3× or more training
  acceleration (`MAE`); composition of multiple augmentations is crucial, and it is critical to compose
  cropping with color distortion or the model shortcuts through colour statistics (`SIMCLR`).
- **Source.** `UDL` §9.3.7, fol. 152–153; `UDL` §9.3.8, fol. 154; `MAE`; `SIMCLR`.
- **Destination.** `SOP-DL-08` §3.4 — the same research function (decide whether and how to pretrain), so a
  minimal extension rather than a new SOP.
- **Boundary.** The 2016 verdict is left standing as history; it was correct about the method it named.
  `MAE`'s rationale — images have heavy spatial redundancy, so sparse random masking suffices — is carried
  as the reason the masking ratio is high, but the language-model "vocabulary" analogy is paraphrase and is
  not quoted (`sources.md` §2.4). The specific 75% figure is `MAE`'s best configuration for its datasets
  (40–80% studied), not a universal constant, and is labelled as such.

### 3.4 Contrastive learning imposes a resource condition the 2016 workflow does not have — **A-extend**

- **2016 baseline.** `SOP-DL-08` §3.1 handles semi-supervised learning; `SOP-DL-02` §3.5 handles the
  labeled-data budget. Neither ties a representation-learning method's *quality* to batch size.
- **Modern delta.** Contrastive learning benefits from larger batch sizes and more training steps than
  supervised learning; batches of 256–8192 are reported, "a batch size of 8192 gives us 16382 negative
  examples per positive pair", and the best models were trained for 1000 epochs. The nonlinear projection
  head substantially improves the quality of the learned representation, and the representation **before**
  the head is what transfers. NT-Xent's normalization and temperature are load-bearing.
- **Source.** `SIMCLR`.
- **Destination.** `SOP-DL-08` §3.4 — as a resource precondition attached to the contrastive branch, and as
  the rule that the transferred representation is taken before the projection head.
- **Boundary.** The batch-size and epoch figures are one paper's configuration range, recorded as evidence
  that the resource axis is bound to the method, not as a recipe. No claim is made that larger batches
  always help.

### 3.5 Augmentation-composition failure is a spurious-cue failure — **A-crosslink**

- **2016 baseline.** The 2016 book treats data augmentation as a regularizer; `SOP-DL-03` §3.2 lists it as a
  lever, and `UDL` §9.3.8, fol. 154 states its aim as teaching the model "to be indifferent to these
  irrelevant data transformations".
- **Modern delta.** `SIMCLR`'s cropping-without-colour-distortion shortcut is a case where the *augmentation
  design itself* creates a spurious feature the model exploits. That is a capability the Trustworthy-ML
  lineage already owns.
- **Source.** `SIMCLR`; `UDL` §9.3.8, fol. 154.
- **Destination.** Cross-link to Trustworthy-ML `BM-02` (spurious cues) from `SOP-DL-08` §3.4. No
  duplicated detector or procedure.
- **Boundary.** The Deep-Learning side records the composition requirement; the Trustworthy-ML side owns the
  spurious-cue audit.

### 3.6 Parameter-efficient adaptation adds a third point to the share decision — **A-extend**

- **2016 baseline.** `SOP-DL-08` §3.3 offers two factorizations — shared representation at the bottom with
  task-specific parameters at the top, or shared top layers with task-specific preprocessing (§15.2,
  pp. 541–542) — and §3.4 fine-tunes all layers jointly after pretraining.
- **Modern delta.** A third option: freeze the base model entirely and adapt a low-rank increment on the
  attention weight matrices. Adapting both W_q and W_v gives the best result under a fixed parameter
  budget, and spreading a low rank across matrices beats concentrating it. There is no additional inference
  latency, because W = W₀ + BA is materialized before deployment. Many tasks are served from one frozen base
  by swapping the low-rank weights, cutting storage and task-switching overhead. Trainable parameters can be
  ~10,000× fewer than full fine-tuning of a 175B model, at ~3× lower GPU memory.
- **Source.** `LORA`.
- **Destination.** `SOP-DL-08` §3.3 — one new option in the existing decision, plus §3.8 (record the
  decision) so the choice is declared.
- **Boundary.** `LORA`'s quality claim is "on-par or better than fine-tuning" on RoBERTa, DeBERTa, GPT-2 and
  GPT-3 — the models it tested. No general ranking against full fine-tuning is implied, and the parameter
  and memory ratios are its own measurements. The 2016 conditions for transfer to help (§15.2, p. 541:
  shared latent factors across settings; abundant source data) are **not** displaced — they still govern
  whether any sharing pays.

### 3.7 Zero-shot transfer realizes the 2016 task-variable requirement, with named failure modes — **A-extend**

- **2016 baseline.** `SOP-DL-08` §3.4 step 10 names zero-shot / zero-data learning as an extreme requiring
  an extra task variable T with the model estimating p(y | x, T), and requires that **T be a generalizable
  representation, not a one-hot encoding** — word embeddings are the cited example (§15.2, p. 543).
- **Modern delta.** `CLIP` instantiates exactly that requirement with natural language as T, via a text
  encoder acting as a hypernetwork that generates the weights of a linear classifier from the text, with
  cosine similarities, a temperature and a softmax. Its limitations are the load-bearing part: "zero-shot
  CLIP is quite weak on several specialized, complex, or abstract tasks"; it "struggles with more abstract
  and systematic tasks such as counting the number of objects in an image"; it is near-random on distance
  estimation; it "still generalizes poorly to data that is truly out-of-distribution for it"; and it "is
  still limited to choosing from only those concepts in a given zero-shot classifier". Prompt templates and
  ensembling are worth roughly 5 points. Comparables that are usable: zero-shot CLIP "only approaches fully
  supervised performance on 5 datasets", wins on 16 of 27 against a supervised baseline, and underperforms
  by more than 10% on Flowers102 and FGVCAircraft.
- **Source.** `CLIP` (§2.3 of `sources.md` holds the verbatim limitation quotes).
- **Destination.** `SOP-DL-08` §3.4 step 10 — the requirement is confirmed, and the *closed label-set*
  constraint is added as its defining limit.
- **Boundary.** The claim that zero-shot evaluation amounts to "evaluating on a different task
  specification" was **not found in the source** and is not used (`sources.md` §2.4). The 5-dataset and
  16-of-27 comparables are `CLIP`'s own; they are recorded as evidence that the capability is
  dataset-dependent, not as a benchmark result.

### 3.8 Zero-shot prompt selection on a benchmark validation set is an evaluation-integrity failure — **A-crosslink**

- **2016 baseline.** `SOP-DL-08` §3.5 lets the labeled-data budget decide; `BC-DL-09` tests whether the
  validation material can resolve a difference (§5.3.1–§5.3.2). Neither anticipates a *prompt* being tuned
  on the target benchmark.
- **Modern delta.** `CLIP` states that using benchmark validation sets to select prompts "is unrealistic for
  true zero-shot scenarios". That is a leakage-and-integrity failure of a kind the Trustworthy-ML lineage
  already audits.
- **Source.** `CLIP` limitations section.
- **Destination.** Cross-link to Trustworthy-ML `BM-08` (evaluation-integrity audit), and to `BM-01`
  (distribution shift) for the truly-OOD limitation. Pointers added from `SOP-DL-08` §3.4; nothing
  duplicated.
- **Boundary.** The Deep-Learning artifacts record that the failure exists and where it is owned. They do
  not restate an audit procedure.

### 3.9 Implicit regularization via the modified gradient-descent objective — **R**

- `UDL` §9.2, fol. 141–143: L̃_GD = L + (α/4)‖∂L/∂ϕ‖², with an extra SGD term equal to the variance of the
  batch gradients; consequences are that full-batch GD generalizes better with larger step sizes, SGD
  generalizes better than GD, and smaller batches generally perform better. **Boundary:** `UDL` itself
  caveats that in the over-parameterized case these gradient terms are zero at the global minimum, and the
  derivation is theoretical. It changes no step in `SOP-DL-03` or `SOP-DL-04`. Record-only.

### 3.10 Early stopping's second reading — **R**

- `UDL` §9.3.1, fol. 145: early stopping can be read as moving back down the bias/variance trade-off curve
  **from the critical region**, and allows selecting among models without training multiple of them.
  **Boundary:** `SOP-DL-03` §3.4 already owns the early-stopping algorithm as a procedure; this is a
  mechanism refinement that changes no step. Record-only.

### 3.11 Neither L2 nor dropout is required to fit random labels — **R**

- `UDL` §20.2.2, fol. 404, citing Zhang et al. (2017a). **Boundary:** considered as an arm for `BC-DL-03`
  and left out — `BC-DL-03`'s claim is mechanism-conformance of the regularizers the 2016 book names, and
  adding a random-label-fitting arm would change the claim under test rather than extend it. Record-only.

### 3.12 Initialization schemes — **R**

- `UDL` §7.5, fol. 108–110: SeLU (Klambauer et al. 2017), layer-sequential unit variance (Mishkin & Matas
  2016 — already cited by the 2016 book), GradInit (Zhu et al. 2021). **Boundary:** method-specific, and
  the 2016 package already labels initialization scales as era defaults with their source. No structural
  delta. Record-only.

---

## 4. Generative modeling — diffusion and flow-based training and evaluation

### 4.1 A lower bound from one family can outrank an exact likelihood from another — **A-extend**

- **2016 baseline.** `SOP-DL-09` §3.1 requires declaring whether each reported number is a point estimate,
  a stochastic estimate or a bound, and forbids sharing a ranking axis between an estimate and a bound
  unless the bound's looseness is reported (§20.14, p. 715). The 2016 book's families are RBM/DBM, VAE,
  GAN, NADE and directed models.
- **Modern delta.** `UDL` §16.5.1, fol. 319 identifies flows as the tractable-likelihood family
  among the four it discusses (CNFs require numerical integration). Its footnote describes a diffusion
  likelihood lower bound exceeding a flow's exact value, while generation is slower. A **valid lower
  bound above a comparable exact log-likelihood** supports a one-sided likelihood ordering; the
  opposite ordering is inconclusive. Generation cost is a separate utility dimension.
- **Source.** `UDL` §16.5.1, fol. 319 and fn. 2; `UDL` §18.4.1, fol. 358; `DDPM` (weighted variational
  bound; `L_simple` drops the variational weighting and gives the best FID despite deviating from the
  bound).
- **Destination.** `SOP-DL-09` §3.1 — the declaration step gains the exact-versus-bound *across families*
  case, and the generation-cost asymmetry that must be reported alongside it.
- **Boundary.** The 2016 case (stochastic estimate above another model's bound) remains inconclusive.
  `L_simple` is a modified **training objective**, not the standard ELBO; its trained model can still be
  independently evaluated using the standard bound (`DDPM` §4.1, Table 1: NLL ≤3.75 bits/dim).
  Training objective and evaluation instrument must be reported separately.

### 4.2 Flow matching generalizes diffusion paths rather than replacing them — **A-extend**

- **2016 baseline.** `SOP-DL-09` §3.8 restricts claims to what the training objective actually supports,
  with a row per objective (pseudolikelihood, score matching, ratio matching, NCE).
- **Modern delta.** Flow matching is simulation-free **during training**, regressing vector fields of
  fixed conditional paths; it **subsumes diffusion paths** as instances. Sampling and CNF likelihood
  evaluation still require numerical ODE integration and have solver-dependent precision. FM on diffusion
  paths is described as a more stable alternative for training diffusion models. Optimal-transport paths are straighter, needing roughly 60% of the NFEs to
  reach the same error threshold. FM reports bits/dim **and** FID jointly.
- **Source.** `FM`.
- **Destination.** `SOP-DL-09` §3.8 — one row in the objective-capability table.
- **Boundary.** FM makes **no** claim that likelihood is an inappropriate metric and does not dispute
  bits/dim; any stronger statement would be unsupported (`sources.md` §2.2). `RF` is a **separate** work;
  no concurrency or derivation relationship between the two is asserted, because none was verified
  (`sources.md` §2.4).

### 4.3 Likelihood and sample quality can disagree, with a source-named mechanism — **A-extend**

- **2016 baseline.** `SOP-DL-09` §3.3 warns that a very poor probability model may produce very
  good-looking samples (§20.14, p. 716), and §3.4 warns of reward hacking through variance collapse on
  never-changing pixels. `BC-DL-11` tests exactly this integrity question.
- **Modern delta.** `DDPM` supplies the strongest citable instance: "Despite their sample quality, our
  models do not have competitive log likelihoods compared to other likelihood-based models", explained by
  "More than half of the lossless codelength describes imperceptible distortions". Its CIFAR-10 test
  bits/dim are 3.03 for Gated PixelCNN, ≤3.70 for the ELBO-trained model and ≤3.75 from a
  **separate standard-bound evaluation** of the `L_simple`-trained model; the latter achieves FID 3.17 / IS 9.46.
- **Source.** `DDPM` (verbatim quotes in `sources.md` §2.3).
- **Destination.** `BC-DL-11` §5 (how to interpret failure) and `SOP-DL-09` §3.3–§3.4.
- **Boundary.** Neither `DDPM` nor `FM` declares bits-per-dim an inappropriate metric; that stronger claim
  was searched for and **not found** (`sources.md` §2.2, cross-cutting answer). The delta strengthens
  `BC-DL-11`'s existing claim rather than replacing it. `DDPM` §4.1, Table 1 has now been verified
  against the primary paper's arXiv HTML.

### 4.4 The 2016 metric exclusion is scoped, and three metrics now have an anchor source — **A-extend**

- **2016 baseline.** `Benchmark/Deep-Learning-2016/README.md` standing rule 5: "No post-2016 metric (FID,
  Inception Score, perplexity-as-standard) appears anywhere in this package." `BC-DL-11` §4 consequently
  names only quantities the 2016 book defines.
- **Modern delta.** `UDL` §14.3, fol. 272–275 names all three as book quantities **with their failure modes
  attached**: test likelihood is ineffective for GANs, expensive for VAEs and diffusion, and exact and
  efficient only for flows; Inception Score is "only sensible for … the ImageNet database", is "sensitive to
  the particular classification model; retraining this model can give quite different numerical results",
  and "does not reward diversity within an object class; it returns a high value if the model only generates
  one realistic example of each class"; FID is computed on the deepest Inception activations so the
  comparison is semantic and "any information discarded by the network does not contribute to the result";
  manifold precision and recall exist precisely because "Fréchet inception distance is sensitive both to the
  realism of the samples and their diversity but does not distinguish between these factors", approximating
  the manifold with k-NN hyperspheres in classifier feature space (Kynkäänniemi et al. 2019).
- **Source.** `UDL` §14.3, fol. 272–275.
- **Destination.** `BC-DL-11` §4 — a clearly marked modern-update metric block carrying all three with their
  stated failure modes; `Benchmark/Deep-Learning-2016/README.md` standing rule 5 — scoped to the 2016 text.
- **Boundary.** The metrics enter **only** with their failure modes attached and **only** in a block marked
  as a modern update. They are never a bare ranking axis, which is what the 2016 rule was protecting. The
  word-boundary scan confirms `FID` does not occur as a token in the thirteen `UDL` chapters read
  (`sources.md` §2.5) — the metric is named in full as "Fréchet inception distance", so the block cites the
  name the source uses. No threshold is invented for any of the three.

### 4.5 Intended-use declaration gains a conditional-generation case — **A-extend**

- **2016 baseline.** `SOP-DL-09` §3.1 requires the intended use to be declared first, because "which model is
  better" is a function of the use (§20.14, p. 717), and offers the task-based escape hatch of precision
  and recall for practical uses such as anomaly detection.
- **Modern delta.** For text-conditioned generation the use decomposes into nameable attribute-rendering
  axes. `UDL` §18.6, fol. 371–372 records GLIDE and Dall·E 2 conditioned on CLIP embeddings, Imagen using
  LLM text embeddings, and DrawBench "designed to evaluate the ability of a model to render colors, numbers
  of objects, spatial relations, and other characteristics".
- **Source.** `UDL` §18.6, fol. 371–372.
- **Destination.** `SOP-DL-09` §3.1 — the declaration step gains the conditional case.
- **Boundary.** DrawBench is cited as an *example of the category*, not as a required instrument. The
  artifact requires that the axes be declared; it does not require a benchmark.

### 4.6 A family ranking that holds only under one metric — **A-extend**

- **2016 baseline.** `SOP-DL-09` §4 lists "treating a metric disagreement as a model disagreement" as a
  failure mode, following §20.14's forward-KL / reverse-KL point.
- **Modern delta.** `UDL`'s Notes (fol. 369) record that Dhariwal & Nichol (2021) "showed for the first time
  that images from diffusion models were quantitatively superior to GAN models **in terms of Fréchet
  Inception Distance**" — a worked instance of a family ranking that is metric-indexed, stated with its
  metric attached by the source itself.
- **Source.** `UDL` ch. 18 Notes, fol. 369.
- **Destination.** `BC-DL-11` §5 and `SOP-DL-09` §4 — as the modern worked example of the failure mode the
  2016 text already named.
- **Boundary.** This lineage does not rank diffusion against GANs. The sentence is carried *because* it is
  metric-indexed, as evidence for the existing failure mode.

### 4.7 Generative-model property taxonomy — **R**

- `UDL` §14.2, fol. 271–272 lists six desirable generative-model properties and, in Fig. 14.3, a matrix
  showing "no single model that satisfies all of these characteristics". **Boundary:** the *function* —
  declare which properties the intended use requires — is already owned by `SOP-DL-09` §3.1. Reproducing
  the matrix would be a model-family encyclopaedia entry, which the plan forbids. Record-only, with the
  pointer.

### 4.8 Implementation-level flow and diffusion details — **R**

- Diffusion's forward-process nomenclature is "the opposite nomenclature to normalizing flows" (`UDL` §18.2
  fn. 1, fol. 350); flows require every layer to be invertible (fol. 305); dequantization and GLOW sampling
  from the base density raised to a positive power (fol. 319–320). **Boundary:** implementation detail; no
  decision step changes. Record-only.

---

## 5. Inference-time compute

### 5.1 The protocol that *can* be stated — **R**

The plan admits this area "only if a reusable, source-bounded protocol can be stated". One can be, and it
is written out here so the work is not lost:

1. Declare the compute budget and the **matching axis** before comparing; `TTC`'s headline result is a
   FLOPs-matched evaluation, and an unmatched one is not comparable.
2. Report the base model's success rate on the target problems **as a precondition**: the benefit holds
   "on problems where a smaller base model attains somewhat non-trivial success rates".
3. Declare which axis is being scaled — sequential revision or parallel search — because the optimum
   depends on difficulty: beam search consistently outperforms best-of-N; easy questions benefit more from
   sequential revisions, while on difficult questions it is optimal to balance the two.
4. Do not treat pretraining compute saved as recoverable at test time: "Test-time and pretraining compute
   are not 1-to-1 exchangeable."
5. Account for difficulty estimation inside the budget: "assessing question difficulty requires applying a
   non-trivial amount of test-time compute itself".

- **2016 baseline.** None. The 2016 book has no test-time-compute concept; its nearest relative is the
  *search* budget in `SOP-DL-05` / `BC-DL-09`, which is a training-time quantity.
- **Modern delta.** The five steps above.
- **Source.** `TTC` (arXiv:2408.03314 v1, 2024-08-06), which the plan directs be kept "explicitly as a
  dated frontier result".
- **Destination.** None. Record-only.
- **Boundary — why this is not an artifact.** Four reasons, in order of weight. (i) It rests on a **single**
  dated source with no independent replication in the plan's list. (ii) That source self-reports narrowness:
  "across the board these schemes provided small gains on hard problems", and on the hardest problems more
  pretraining compute would have been better. (iii) Its benchmark list and exact base-model naming are only
  **partially verified** (`sources.md` §2.4), so the scope of the claim cannot be pinned down precisely
  enough to write an artifact against. (iv) Step 1 — compute matching and resource reporting — is already
  owned (§1.1 and §1.6), so what would genuinely be new is only the sequential-versus-parallel allocation,
  which is model- and task-specific. The plan directs weakly supported or unsettled items to this file.
- **Promotion trigger.** A second independent source establishing the sequential/parallel allocation, or
  reproduction of the frontier result across model families, would make step 3 artifact-worthy. Recorded so
  the deferral is a decision with an exit condition rather than an omission.

### 5.2 A test-time-compute SOP or BC of its own — **X**

Rejected on the grounds at §5.1. Creating one would rest a whole artifact on a single 2024 preprint with
self-reported small gains and a partially unverified evaluation scope — precisely the shape the plan
excludes.

---

## 6. Destination summary

| Artifact | Deltas landing | Kind of change |
| --- | --- | --- |
| `SOP-DL-02` §3.4, §3.5, §3.6 | §1.1, §1.3, §1.4, §1.5 | Compute as a third axis; ratio ill-defined; U-curve right branch era-scoped; overparameterization evidence |
| `SOP-DL-03` §3.2, §3.3 | §3.1, §3.2 | L2 ≠ weight decay under adaptive optimizers; optimizer-ordering note, no ranking |
| `SOP-DL-04` §3.4 | §3.2 | Adaptive-optimizer sensitivity note; no optimizer ranking or repair-menu reorder |
| `SOP-DL-05` §3 | §1.8 | Conditional hyperparameters declared before sampling |
| `SOP-DL-07` §3.1, §3.2 | §2.1, §2.2, §2.3 | Attention prior in the bias register; conditional supersession of the convolutional prior |
| `SOP-DL-08` §3.3, §3.4, §3.8 | §3.3, §3.4, §3.6, §3.7 | Self-supervised pretraining; contrastive resource condition; low-rank adaptation as a third share option; zero-shot closed label set |
| `SOP-DL-09` §3.1, §3.3, §3.4, §3.8, §4 | §4.1, §4.2, §4.3, §4.5, §4.6 | Exact-versus-bound across families; FM row; likelihood/sample-quality disagreement; conditional-generation use; metric-indexed ranking |
| `BC-DL-02` §5, §6 | §1.3, §1.4, §1.5 | Second descent on the data in use; ratio caveat; overparameterization reading |
| `BC-DL-06` §6 + Historical boundary | §2.1, §2.4 | Structural limit is architecture-bound; quadratic cost replaces recurrence depth |
| `BC-DL-08` §2, §5 | §2.3, §2.5 | Equivariance given-versus-learned arm; depth counter-evidence in interpretation |
| `BC-DL-11` §4, §5 | §4.3, §4.4, §4.6 | Modern metric block with failure modes attached; likelihood/sample-quality instance; metric-indexed ranking |
| `Validation/Deep-Learning-2016/concept_reconstruction.md` §5.1 | §7.1 | Pointer to the revised adversarial explanation |
| `Benchmark/Deep-Learning-2016/README.md` rule 5 | §4.4 | Exclusion scoped to the 2016 text |
| `SOP/Deep-Learning-2016/README.md` rule 4 | §6 note | "No post-2016 material" scoped to the 2016 text, with a pointer to this lineage |

Cross-links added, nothing duplicated:

| From | To | Owned capability |
| --- | --- | --- |
| `SOP-DL-02` §3.5 | Trustworthy-ML `SOP-08` | Reporting evidence and validity boundaries, incl. compute |
| `SOP-DL-08` §3.4 | Trustworthy-ML `BM-02` | Spurious-cue audit (augmentation-shortcut case) |
| `SOP-DL-08` §3.4 | Trustworthy-ML `BM-08` | Evaluation-integrity audit (prompt selection on a benchmark validation set) |
| `SOP-DL-08` §3.4 | Trustworthy-ML `BM-01` | Distribution shift (truly-OOD zero-shot limitation) |
| `concept_reconstruction.md` §5.1 | Trustworthy-ML `BM-05` | Adversarial robustness under a declared threat model |

## 7. Rejected and cross-lineage items

### 7.1 The revised adversarial-example explanation — **A-crosslink**

- **2016 baseline.** The 2016 book attributes adversarial examples to excessive linearity and prescribes
  adversarial training (§7.13). In the previous phase this was **withdrawn as an active claim**: `BC-DL-04`
  was deleted and the account was demoted to a 2016 historical record in `concept_reconstruction.md` §5.1.
- **Modern delta.** "The best current explanation is that adversarial examples aren't due to a lack of
  robustness to data from outside the training data manifold. Instead, they are exploiting a source of
  information that is in the training distribution but which has a small norm and is imperceptible to humans
  (Ilyas et al., 2019)."
- **Source.** `UDL` §20.4, fol. 415.
- **Destination.** A pointer from `concept_reconstruction.md` §5.1 to Trustworthy-ML `BM-05`. **No new
  adversarial artifact is created in this lineage.**
- **Boundary.** The modern account reframes the *cause*, which is why the 2016 remedy cannot be reinstated
  as stated. Robustness evaluation under a declared threat model is owned by Trustworthy ML; this lineage
  only records that the 2016 explanation has been superseded and where the current capability lives.

### 7.2 Rejected outright

| Candidate | Why rejected |
| --- | --- |
| "ViT beats CNNs" as an unconditional delta | Both sources state the claim conditionally on pretraining scale; `VIT` self-reports underperformance versus ResNets at ImageNet scale. The unconditional form is false on its own source. §2.3 carries the conditional form. |
| A Transformer or ViT artifact of its own | Plan forbids a history of architectures and one artifact per method; the 2016 rule that a model family is not a benchmark is carried forward. §2.6. |
| An optimizer leaderboard or ranking | The 2016 package rejected this because §8.5.4 reports no consensus, and `BC-DL-05` was reframed as a probe suite for that reason. §3.2 records the changed sensitivity assumption without producing a ranking. |
| A compute-allocation benchmark | Would test contested exponents (§1.2) rather than a source-named quantity, so it fails the standing rule that every metric is a quantity a source names. |
| A test-time-compute SOP or BC | §5.1–§5.2: single dated frontier result, self-reported small gains, partially unverified evaluation scope. |
| Any delta sourced to `DLFC` | No access (`sources.md` §1.2). Recorded as a standing prohibition, not an oversight. |
| FID / Inception Score as a bare replacement metric axis | They enter only as anchor-named quantities with their stated failure modes attached (§4.4). The 2016 exclusion rule was protecting against exactly the bare-axis use, and that protection is kept. |
| `RF` presented as concurrent with or derived from `FM` | Relationship unverified (`sources.md` §2.4). Cited as distinct works. |
| Publication venues not stated in the arXiv record | `ATTN`'s NeurIPS 2017 and `DDPM`'s NeurIPS 2020 status are not arXiv-stated and are never used as citation elements (`sources.md` §2.1, §2.4). |

## 8. Provenance convention applied

Per the plan: any modified file carries a short modern-update provenance note pointing at the relevant
delta and source; wholly new artifacts list their modern sources directly. In practice:

- Each extension block in a 2016 artifact opens with **Modern update (2017–2026)** and closes with a
  source line naming the `delta_map.md` row and the source keys.
- 2016 text is annotated, never rewritten. Where a 2016 statement is now era-scoped, the annotation says
  so and the original sentence and its 2016 citation remain in place.
- `sources.md` and this file list their modern sources directly, as the plan requires for new artifacts.
- No 2016 citation was altered. The 2016 package's citation convention (`§section, p. N` = PDF page) is
  unchanged; `UDL` uses its own convention (`§section, fol. N`) recorded in `sources.md` §1.1.
