# SOP-DL-07 — Choose an inductive bias by its assumption, then test the assumption

**Stage:** design · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Make an architecture choice reviewable. Record four things for every structural bias that you adopt:

- what the bias **assumes** about the data-generating process
- what the bias **buys**
- what **breaks** when the assumption is false
- what you **measure** to detect the violation

Then run the paired comparison that tests the assumption.

This SOP is not an architecture tutorial. This SOP is not a chapter summary. The book itself licenses the
framing. Convolution and pooling are **infinitely strong priors**, so data cannot override those priors.
The book's wording is "卷积和池化可能导致欠拟合" — convolution and pooling may cause underfitting (§9.4, p. 366).

The book also licenses the restricted comparison class. A convolutional model
"只能以基准中的其他卷积模型作为比较的对象", because a non-convolutional model can still learn after a
permutation of all the pixels (§9.4, p. 366).

The book also refuses to hand out architecture recipes. A new best structure appeared every few months or
even weeks. At the time of writing, no one could say which structure was best. The ideal architecture
"必须通过实验，观测在验证集上的误差来找到" — you must find that architecture experimentally, by
observing the validation error (§9 intro, p. 350; §6.4, p. 223).

Out of scope: output units and cost (`SOP-DL-01`), capacity sizing (`SOP-DL-02`), regularization
(`SOP-DL-03`), optimization repair (`SOP-DL-04`).

## 2. Inputs and assumptions

- The task specification from `SOP-DL-01`, including whether the whole input is available before an
  output is required.
- Stated knowledge of the data's structure. Ask whether there is a topology, such as an image grid or a
  sequence order. Ask whether the same statistics hold at every position. Ask which transformations
  leave the label unchanged. Ask whether the target is a composition of simpler functions.
- The ability to run **matched-capacity controls**. Without those controls, you cannot separate the
  depth claims and the sharing claims from parameter-count effects (§6.4, pp. 226–227).
- A validation metric and the search protocol of `SOP-DL-05`.
- The benchmark's **symmetry class**: permutation-invariant, or one in which the designer embeds spatial
  knowledge (§9.4, pp. 366–367). Comparisons across those two classes are not meaningful.

## 3. Procedure

### 3.1 Let data structure select the model class, then declare it as a 2016 default

1. Read the model class off the structure of the data. The book's baseline routing gives three arrows
   (§11.2, pp. 439–440):
   - fixed-size vector input under supervision ⇒ fully connected feedforward network
   - input with a known topology, such as images ⇒ convolutional network
   - sequence input or output ⇒ gated recurrent network

   That routing is a book-era default, and this file records that routing as such.

> **Modern update (2017–2026) — two of the three routing arrows are now conditional.** The 2016 routing
> is retained above as a book-era default. Two structural changes apply to that routing. Neither
> change adds a model family to this SOP.
>
> **Sequence input or output no longer implies recurrence.** A self-attention layer connects all
> positions with a constant number of sequentially executed operations. That layer dispenses with
> recurrence and convolutions entirely. Self-attention layers are faster than recurrent layers when the
> sequence length is smaller than the representation dimensionality. Shorter paths between any
> combination of positions make long-range dependencies easier to learn. The register gains an entry for
> that prior (§3.2 below). The *cost* side of that entry is a quadratic dependence on sequence length.
> That cost bounds the usable length in a different way than the recurrent gradient path did.
>
> **Known topology no longer implies convolution unconditionally.** Convolutional layers are equivariant
> to spatial translation. Those layers take the 2D structure of the image into account at every layer. In
> an attention-based network, that equivariance "must be learned" instead of being built in. The modern
> account is explicit about the strong convolutional inductive bias. That bias "can only be superseded by
> employing extremely large amounts of training data". The primary vision source states the same
> condition from the other side. Consider the low-bias architecture pre-trained on large data, then
> transferred to mid-sized or small benchmarks. That architecture attains excellent results with
> substantially fewer computational resources. Trained only on ImageNet-scale data, that architecture
> self-reports accuracies **below** comparable convolutional networks.
>
> The routing question therefore gains a precondition. Check that precondition before you follow either
> arrow. The question reads: **is there a large-scale pretraining source available for this input
> type?** If the answer is yes, a low-bias architecture is a live option, and its cost is compute. If the
> answer is no, the 2016 arrows hold, and their bias is what buys the data-efficiency.
>
> No architecture is specified, endorsed or ranked here. No transformer or vision-transformer entry is
> created. The plan governing this lineage forbids an architecture encyclopaedia. This SOP carries
> forward the 2016 package's rule that a model family is not a benchmark. What enters is the *prior*, and
> the *condition* under which a designer can give up that prior.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §2.1, §2.3, §2.6.
> Sources: `ATTN` (abstract, §4); `VIT` (abstract, introduction, conclusion); `UDL` §12.1–12.2 fol.
> 207–209, §12.9 fol. 227–228, §12.10 fol. 229–230.*

### 3.2 Fill in the bias register

For each bias under consideration, complete the four columns. The entries below are the book's own
mappings.

**Sparse interaction** (§9.2, p. 355)
- Assumes: the outputs depend on a local neighbourhood, and the kernel size k ≪ m.
- Buys: the parameter count falls from m × n to k × n. The time for one example falls from O(m × n) to
  O(k × n). The model gains statistical efficiency. Deeper units still touch most of the input
  indirectly. So the network builds complex interactions from sparse primitives (Fig. 9.4).
- Breaks: the task requires the merger of information from distant positions in the input. Then the
  convolutional prior "may simply be incorrect" (§9.4, p. 366).
- Measure: the floor of the training error, against a dense control at matched capacity. Run that
  comparison on an ablation which needs a conjunction of distant positions.

**Parameter sharing** (§9.2, pp. 358–360)
- Assumes: the same statistics hold at every position.
- Buys: storage falls to k parameters, often orders of magnitude below m. The model gains statistical
  efficiency. Parameter sharing is explicitly **not** a runtime saving, because the forward pass remains
  O(k × n). The book gives worked arithmetic. A 2-tap edge detector on a 320 × 280 image costs 267,960
  flops. A
  dense layer needs more than 16 billion flops for the same image. The book undercuts that figure with
  its own caveat. If only non-zero entries are stored, matrix multiplication and convolution need the
  same number of floating-point operations (§9.2, p. 360).
- Breaks: the positions carry different semantics. The book's own example is centred face crops. In
  those crops, the upper units should look for eyebrows, and the lower units should look for a chin
  (§9.2, p. 360).
- Measure: the triad that the book defines at equal adjacency. Run locally connected convolution, which
  the book calls "unshared convolution" (§9.5, p. 371). Run tiled convolution, whose storage grows by a
  constant equal to the number of kernels (p. 374). Run shared convolution. Then compare per-position
  bias with per-channel bias. That second choice slightly reduces statistical efficiency. That second
  choice still lets the model correct for statistical differences across image positions (§9.5, p. 378).
  Read that comparison as edge-versus-centre accuracy under zero padding.

**Equivariance** (§9.2, p. 360)
- Assumes: f(g(x)) = g(f(x)) for a translation g.
- Buys: a *where* representation. Convolution produces a two-dimensional map. That map indicates where a
  feature appears in the input. A delayed event yields the same representation later.
- Breaks: "卷积对其他的一些变换并不是天然等变的" — convolution is not naturally equivariant to other
  transformations, such as scaling or rotation. Those transformations require other mechanisms (§9.2,
  p. 360). Equivariance is also not invariance. The retained position is exactly what pooling later
  discards.
- Measure: shift the input by δ. Then verify that the output shifts by the same δ. For a group other
  than translation, the model must *learn* the equivariance. The model learns by replicating detectors
  over the group, and by pooling across channels (Fig. 9.9, p. 363, uses three filters for a rotated
  '5').

**Pooling invariance** (§9.3, pp. 362–364)
- Assumes: presence matters more than precise location.
- Buys: approximate invariance to small translations. Pooling leaves roughly k× fewer units for the next
  layer, which is a compute saving. When the next layer is fully connected, that reduction is also a
  statistical saving and a storage saving. Pooling gives fixed-size statistics from variable-size
  inputs.
- Breaks — stated as a caveat, and not an endorsement: "保存特征的具体位置却很重要" (§9.3, p. 362; the
  example is a corner defined by two edges). The book states that pooling all features
  "将会增大训练误差" when precise spatial information is required (§9.4, p. 366). Pooling complicates
  architectures that need a top-down pass, or an inverse pass. Boltzmann machines and autoencoders are
  such architectures (§9.3, p. 364).
- Measure: the **training** error with and without pooling. Record the localization accuracy as well.
  Consider mixed channels, where the network pools only some of the channels (Szegedy et al., 2014a,
  as cited; §9.4, p. 366).

**Convolution and pooling as infinite priors** (§9.4, pp. 365–367)
- Assumes: zero probability mass on all weights outside a small, contiguous receptive field. Each weight
  also equals the weight of its neighbour, up to a shift. Pooling adds an infinite prior of invariance to
  a small translation, for every unit.
- Buys: large statistical efficiency when the assumption holds.
- Breaks: an infinite prior has a strength that data cannot override. So these priors can cause
  **underfitting** (§9.4, p. 366).
- Measure / validity limit: compare only against other convolutional models in the same benchmark
  (§9.4, p. 366). Declare whether the benchmark is permutation-invariant, or whether the benchmark embeds
  spatial knowledge. Under this prior, a convolutional network that runs as a fully connected network
  counts as an enormous waste of computation. That framing is interpretive only.

**Depth versus width** (§6.4, pp. 223, 225–227)
- Assumes: one hidden layer already suffices to fit the training set. So depth is a *statistical* choice.
  The choice is a prior that the target is a composition of simpler functions. That prior also allows a
  multi-step program, whose intermediate values may be counters or pointers, rather than variation
  factors.
- Buys: a deeper network usually needs fewer units per layer, and fewer parameters per layer. A deeper
  network often generalizes to the test set more easily.
- Breaks: deeper networks are usually harder to optimize (§6.4, p. 223). The expressivity-separation
  results carry one caveat. We cannot guarantee that the function class we want to learn has the required
  property (§6.4, p. 225).
- Measure: the validation error against depth, at **matched parameter count**. The book gives an explicit
  control (Fig. 6.7, pp. 226–227, on address-photo digit transcription). Adding parameters inside
  convolutional layers, without adding depth, has almost no effect on that task. Shallow models overfit
  near 20 million parameters. Deep models still perform well past 60 million.

**Hidden-unit choice** (§6.3, pp. 216–222)
- Assumes: near-linear behaviour optimizes better. The first derivative of ReLU is 1 where the unit is
  active, and the second derivative is 0 almost everywhere. The ReLU gradient direction is more useful
  than the direction of an activation that brings in second-order effects (§6.3, p. 217).
- Buys: ReLU is an excellent default. Initialize the ReLU bias around 0.1, so that units start active and
  pass derivative. Maxout learns the activation itself. Maxout approximates any convex function, and can
  give the next layer k× fewer weights. The redundancy of maxout resists catastrophic forgetting. An
  identity hidden layer factors W = V U. That factorization needs (n + p)q parameters instead of np, at
  the cost of a low-rank constraint.
- Breaks: ReLU cannot learn from an example that zeros its activation. Maxout has k weight vectors per
  unit, so maxout usually needs more regularization. That need falls away when the training set is large
  and k is small. Sigmoid and tanh saturate over most of their domain, so the book discourages sigmoid
  and tanh as feedforward hidden units. Those same units are **required** in recurrent networks, in probabilistic
  models and in some autoencoders. In those models, piecewise-linear activations are inadmissible. RBF
  units saturate to zero, and are hard to optimize. Softplus is smooth and does not saturate. Even so,
  softplus is empirically worse than ReLU, and is generally discouraged.
- Measure: measure empirically. The book states "还没有许多明确的指导性理论原则" — there are not many clear
  theoretical guiding principles. No one can predict the winner in advance. The loop runs intuition →
  build → validate (§6.3, p. 216). An isolated non-differentiability is acceptable. Training never reaches
  a minimum where the gradient is zero, and implementations return a one-sided derivative (§6.3,
  pp. 216–217).

**Recurrence and unfolding** (§10.1, pp. 393–396; §10.2.3, pp. 406–407)
- Assumes: stationarity. The value of p(next | current) does not depend on t.
- Buys: a fixed model size, whatever the sequence length. The model uses one shared transition function at
  every step. That sharing generalizes to unseen lengths. The sharing also needs far fewer training
  samples than a model without parameter sharing. A tabular joint would need k^τ parameters. The parameter
  count of the RNN is tunable independently of the length.
- Breaks: "循环网络为减少的参数数目付出的代价是优化参数可能变得困难" — the price of fewer parameters is that
  optimizing those parameters may become difficult (§10.2.3, p. 407). The hidden state is necessarily a
  lossy summary of the past (§10.1, p. 394).
- Measure: hold out at a longer τ than the τ used in training. Record the error at each position. Compare
  the model against a variant that conditions on the time index. The book's remedy for non-stationarity is
  to feed t as an extra input. That remedy costs the need to extrapolate to values of t never seen in
  training (§10.2.3, p. 407).

**Which part of a recurrent network to make deep** (§10.5, pp. 415–417)
- Allocate capacity across all three blocks: input→hidden, hidden→hidden, and hidden→output. Prefer
  **shallow state-to-state transforms**. Depth in the state path lengthens the shortest path between t and
  t + 1. One hidden layer in that path doubles the length. If you need depth there, add hidden-to-hidden
  skip connections. The book describes the evidence as strongly suggestive, and not proven.
- Measure: the validation error per allocation, and the length of the shortest path between consecutive
  time steps.

**Gating** (§10.10, pp. 425–429)
- Assumes: a path through time must have a derivative that neither vanishes nor explodes. The correct time
  constant also depends on the input.
- Buys: the self-loop, which the book describes as LSTM's core contribution. That loop is a path on which
  the gradient persists. Make the self-loop weight context-dependent, and the time constant becomes itself
  a model output. The scale of accumulation then changes per sequence, even with fixed parameters. Gating
  generalizes leaky units from a constant weight to per-step weights. Gating also adds a learned reset of
  the state after use.
- Breaks / ablation: variants of LSTM and GRU have difficulty clearly beating both original architectures
  across tasks at the same time. The critical factor turns out to be the **forget gate**. A +1 bias on
  that gate makes LSTM as robust as the best variants explored (§10.10.2, p. 429).
- Measure: the largest dependency span that the model can learn. The book demonstrates this first on
  artificial long-dependency datasets, and then on real tasks (§10.10.1, p. 428).

**Encoder–decoder bottleneck** (§10.4, pp. 413–415)
- Assumes: a context vector C of fixed size can summarize the input.
- Buys: the input length and the output length come apart. The encoder and the decoder need not match in
  hidden size.
- Breaks: "维度太小而难以适当地概括一个长序列" — the dimensionality of C is too small to summarize a long
  sequence adequately. The book observed the bottleneck in machine translation (§10.4, p. 415).
- Measure: the task quality against the input length. The stated fix is a C of variable length. That fix
  uses attention, which ties the elements of C to the output elements (§10.4, p. 415).

**Bidirectionality** (§10.3, pp. 410–413)
- Assumes: you can observe the entire sequence before the outputs are needed. Backward connections are
  legitimate only in that case.
- Buys: the outputs depend on the past and on the future, and stay most sensitive to x(t). No fixed window
  is needed, unlike a feedforward network, a convolutional network, or a look-ahead-buffer RNN. The
  motivating case is coarticulation. In coarticulation, the correct reading of a phoneme depends on
  several future phonemes or words.
- Breaks: the network is invalid for online generation, or for causal generation. The book describes the
  networks earlier in the chapter as all having a causal structure. An RNN applied to images also costs
  more than a convolutional network. That RNN does permit long-range lateral interaction inside a feature
  map (§10.3, p. 413).
- Measure: check whether deployment permits the observation of the whole sequence. Then compare the error
  against a causal baseline, at each look-ahead budget.

**Recursive (tree) structure** (§10.6, pp. 417–419)
- A chain of length τ has depth τ. A balanced binary tree has depth O(log τ). Measure the span that the
  model can learn, against a chain at the same τ. The book leaves the best way to construct the tree
  explicitly unresolved.

**Explicit memory** (§10.12, pp. 432–435)
- Measure the task success against a plain RNN, and against an LSTM on the same task. A failure implies
  that addressing, and not capacity, is the bottleneck. Integer addressing is hard to optimize. Soft
  (softmax) addressing keeps the model differentiable. Stochastic hard addressing is harder to train.

> **Modern update (2017–2026) — one added register row.** The entries above are the 2016 book's own
> mappings, and those entries are unchanged. The modern anchor states the motivating conditions for
> content-based connection in exactly this register's four-column shape. One row is therefore added in
> that shape. The rest of the register keeps the book's own wording.
>
> **Content-based all-to-all connection (attention)** — *modern row, not a 2016-book entry*.
>
> Assumes: the task presents very many input variables. The task shows **similar statistics at every
> position**. The sequence length varies, and one cannot simply resize that length to a fixed input. The
> connections between distant positions carry a relevance that is **content-dependent**, and not fixed by
> the architecture.
>
> Buys: a path between any two positions, in a constant number of sequentially executed operations. That
> path is what makes long-range dependencies easier to learn. Self-attention layers are faster than
> recurrent layers when the sequence length is smaller than the representation dimensionality. The model
> is also more parallelizable, and that needs significantly less time to train.
>
> Breaks: the cost grows **quadratically** with the sequence length, and that growth bounds the usable
> length. The new limit sits on the same axis that the recurrent entries above treat. That limit is a
> different bound, and not the absence of a bound. The named category of response is to make the
> connection pattern sparser. No specific sparsifying scheme is endorsed here. The prior is also
> *low*-bias in the spatial case. Convolution has translation equivariance at every layer, and an
> attention model must learn that equivariance instead. That is why only extremely large amounts of
> training data can supersede the low-bias prior.
>
> Measure: use the same two instruments that the recurrent entries already define. Those instruments are
> the **maximum learnable dependency span**, and the error at each position. Read both against the
> quadratic cost, at the length actually used. Add the equivariance test that the **Equivariance** row
> above already specifies. That test shifts the input by δ, then verifies that the output shifts by δ.
> Run that test as a *learned*-versus-*given* contrast. Run the test on a model that must learn the
> equivariance. Run the test on a model that has the equivariance built in, at matched data. Then report
> which of those regimes the data budget puts you in.
>
> The depth-versus-width row above is **not** amended. The modern evidence on depth is genuinely
> contested. Consider the evidence that runs against a simple depth story. That evidence includes wider
> and shallower residual networks. That evidence includes a 12-layer parallel-channel network. That
> evidence also includes the finding that predominantly shorter paths of 5–17 layers drive performance in
> residual networks. Other evidence runs for that story. The distillation experiments report that student
> performance increased with depth, at a constant parameter budget. The modern anchor gives its own
> verdict: "the balance of evidence suggests that depth is critical. Even the shallowest networks with
> good image classification performance require >10 layers. However, there is no definitive explanation
> for why." The 2016 package already declined to make depth-versus-width a benchmark, and that decision
> stands. `delta_map.md` §2.5 records the counter-evidence. A reader then interprets a depth result
> against that evidence, and not as a settled hierarchy.
>
> *Delta: `delta_map.md` §2.2, §2.4, §2.5. Sources: `ATTN` (abstract, §4); `UDL` §12.1–12.2 fol. 207–209,
> §12.9 fol. 227–228, §12.10 fol. 229–230, §20.6 fol. 418–419, ch. 11 summary fol. 186.*

### 3.3 Test before trusting

2. Run the paired comparison that the book defines for every bias that you adopt. Report **which
   assumption** that comparison tested. Use these pairs:
   - dense versus sparse, at matched capacity
   - locally connected versus tiled versus shared, at equal adjacency
   - pooled versus unpooled, and partially pooled
   - shallow versus deep, at matched parameter count
   - chain versus tree, at equal τ
   - causal versus bidirectional, under the same look-ahead budget
   - fixed-size C versus length-varying C, across input lengths
3. **Screen architectures cheaply before paying for full training** (§9.9, p. 383): random
   convolution-and-pooling layers are already frequency-selective and translation-invariant, so evaluating
   several candidate convolutional architectures by training only the last layer, picking the best, and then
   training fully is a legitimate screening procedure. Carry the book's caveat: the benefit of unsupervised
   feature pretraining remains unclear — regularization, or merely enabling larger architectures.
4. **Sweep the zero padding** rather than assuming a padding value (§9.5, p. 371). The optimum for test
   accuracy usually lies between valid and same convolution.
5. **Declare the benchmark's symmetry class** before reporting any comparison (§9.4, pp. 366–367).
6. **Do not expect rankings to be stable** (§9 intro, p. 350). Record the date of any architecture claim.

## 4. Important failure modes

- **Adopting a prior whose assumption fails**, and reading the resulting underfitting as insufficient
  capacity. More data cannot fix the infinite-prior case (§9.4, p. 366).
- **Comparing across symmetry classes**: a convolutional model against non-convolutional models on a
  permutation-invariant benchmark (§9.4, pp. 366–367).
- **Pooling every channel** when precise spatial information is required (§9.3, p. 362; §9.4, p. 366).
- **Claiming a runtime saving from parameter sharing**, which saves storage and sample complexity, not
  flops (§9.2, p. 360).
- **Assuming equivariance beyond translation** (§9.2, p. 360).
- **Adding depth without matching parameter count**, and crediting depth for a parameter effect (§6.4,
  pp. 226–227).
- **Deepening the state-to-state transform** in a recurrent network, lengthening the shortest path between
  consecutive time steps (§10.5, pp. 415–417).
- **Using a bidirectional network where deployment is causal** (§10.3, pp. 410–411).
- **Keeping a fixed-size context vector** as sequence length grows (§10.4, p. 415).
- **Choosing an activation on theoretical grounds.** The book states that no clear guiding principles
  exist. No one can predict the winner in advance (§6.3, p. 216).
- **Reporting a new activation as an advance**, without heeding the publication-bias warning. Many
  unpublished activations match the popular ones. The authors' own MNIST run reached below 1% error with
  an unconventional activation (§6.3, pp. 220–221).
- **Using saturating units where piecewise-linear ones are admissible**, or piecewise-linear units where
  saturating ones are not. Recurrent networks, probabilistic models and some autoencoders require the
  former (§6.3, p. 220).
- **Optimizing parameters in a shared-weight recurrent model as if the reduced parameter count were
  free.** The book names that difficulty explicitly (§10.2.3, p. 407).

## 5. Outputs and reporting

- Keep the **bias register**: one row per adopted bias, with the columns assumes / buys / breaks /
  measure. Source each column.
- Record the paired comparisons that you actually ran, with their matched-capacity controls, and the
  assumption that each comparison tested.
- Record the declaration of the benchmark's symmetry class.
- Record the depth-versus-width sweep at matched parameter count, with the validation-error criterion.
- Record the screening procedure that you used, and the caveat of that procedure. The screening option is
  the last-layer-only ranking, when you use that ranking.
- Date-stamp every architecture claim, because rankings move faster than the source can record.
- Record anything that you leave to `SOP-DL-05`, because the item is a hyperparameter rather than a
  structural choice. Those items are the padding amount, the number of maxout pieces, and the hidden
  sizes per block.

The modern update adds the items below to the report (`delta_map.md` §2.2, §2.3):

- Report the **pretraining-scale precondition** that you checked at §3.1 step 1. State whether a
  large-scale pretraining source exists for that input type. State, in turn, whether a low-bias
  architecture was a live option at all.
- In the register, mark the modern row as such. That mark lets a reader tell the 2016 book's own mappings
  from the added row.
- For any equivariance claim, state whether the architecture had the equivariance **built in or learned**.
  State the data budget under which you ran the comparison. Without that budget, the two comparisons are
  not comparable.

## 6. Source traceability

| Claim or step | Locator |
| --- | --- |
| Model class from data structure (book-era default) | §11.2, pp. 439–440 |
| Sparse interaction: parameter, time and statistical savings; deeper units still see most of the input | §9.2, p. 355, Fig. 9.4 |
| Parameter sharing: storage not runtime; worked flops and its own caveat; centred-face counterexample | §9.2, pp. 358–360 |
| Locally connected vs tiled vs shared convolution; per-position vs per-channel bias | §9.5, pp. 371, 374, 378 |
| Equivariance: the where-representation; not naturally equivariant to scale or rotation; learned equivariance by replication and channel pooling | §9.2, p. 360; Fig. 9.9, p. 363 |
| Pooling: what it buys; exact-location caveat; training-error increase when spatial precision is needed; inverse-pass complication; mixed channels | §9.3, pp. 362–364; §9.4, p. 366 |
| Infinite-prior reading; underfitting risk; restricted comparison class; permutation-invariant vs spatial-knowledge benchmarks | §9.4, pp. 365–367 |
| Depth as a statistical prior; harder to optimize; expressivity caveat; matched-parameter-count control and the 20M/60M observation | §6.4, pp. 223, 225–227, Figs. 6.6–6.7 |
| Architecture must be found experimentally on validation error | §6.4, p. 223 |
| Hidden units: ReLU derivative argument and default status; bias ≈ 0.1; maxout; identity layers; ReLU dead-example failure; maxout regularization need; sigmoid/tanh admissibility split; RBF and softplus verdicts; absence of guiding theory; publication-bias warning; isolated non-differentiability acceptable | §6.3, pp. 216–222 |
| Recurrence: stationarity, shared transition function, sample-efficiency, k^τ tabular contrast, lossy state, optimization price, t-conditioning remedy | §10.1, pp. 393–396; §10.2.3, pp. 406–407 |
| Which recurrent block to deepen; shortest-path argument; skip connections | §10.5, pp. 415–417 |
| Gating: self-loop as core contribution, context-dependent time constant, generalization of leaky units, learned reset; forget-gate ablation and +1 bias | §10.10, pp. 425–429 |
| Encoder–decoder: length decoupling; bottleneck deficiency; variable-length C with attention | §10.4, pp. 413–415 |
| Bidirectionality: full-sequence requirement, coarticulation motivation, causal invalidity, image cost | §10.3, pp. 410–413 |
| Recursive nets: O(log τ) depth; unresolved tree construction | §10.6, pp. 417–419 |
| Explicit memory: addressing as the bottleneck; soft vs hard addressing | §10.12, pp. 432–435 |
| Cheap architecture screening with random convolution/pooling layers; unclear benefit of unsupervised features | §9.9, p. 383 |
| Zero padding optimum between valid and same | §9.5, p. 371 |
| Architecture rankings unstable; no architecture-selection advice given | §9 intro, p. 350 |

**Modern-update provenance.** Every row above is a 2016-book locator, and no row was altered. Two
modern-update blocks were added. The first is the conditional routing note at §3.1 step 1. The second is
one added register row, *Content-based all-to-all connection*, at the end of §3.2, together with the
matching §5 reporting lines. Those blocks are sourced outside the 2016 book. Both are recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§2.1–§2.5.

The source keys are defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1. The keys are:

- `ATTN` (abstract, §4)
- `VIT` (abstract, introduction, conclusion)
- `UDL` §12.1–12.2 fol. 207–209, §12.9 fol. 227–228, §12.10 fol. 229–230, §20.6 fol. 418–419, ch. 11
  summary fol. 186

The added register row carries the label *modern row, not a 2016-book entry* in place. That label stops a
reader from confusing the added row with the book's own mapping.

**Historical boundary.** Treat the entries below as book-era. Add that label wherever an entry appears:

- the §11.2 model-class routing, and the unit menu that goes with that routing
- the verdict that gated RNNs were the most effective sequence models in practice at the time of writing,
  with LSTM then GRU (§10.10, pp. 425, 428)
- explicit memory and neural Turing machines as the frontier for the tasks that RNNs and LSTMs cannot
  learn (§10.12, p. 434)
- unsupervised or patch-wise feature learning, popular roughly 2007–2013, while "today most convolutional
  networks are trained in a purely supervised way" (§9.9, p. 383)
- the named activation menu: Leaky ReLU, PReLU, maxout, softplus, hard tanh, RBF, and mixture density
  networks
- the named convolution menu: locally connected, tiled, grouped and strided convolution, and the
  valid/same/full padding choices
- the named recurrent menus: ESNs and reservoir computing, leaky units and clockwork-style update
  frequencies, and peephole connections
- memory networks and neural Turing machines
- the MNIST sub-1% result with an unconventional activation
- the study of address-photo digit transcription behind Fig. 6.7
- the ImageNet result credited with starting current commercial interest (§9.11, p. 390)
- the AT&T check-reading and Microsoft OCR deployments (§9.11, p. 390)
- framework-specific practices, such as symbol-to-number differentiation in Torch and Caffe, against
  symbol-to-symbol in Theano and TensorFlow (§6.5.5, p. 238)

Two general lessons survive the era, and this file keeps both. The first lesson is the book's verdict that
the core ideas did not change since the 1980s. The book attributes the gains mainly to larger datasets and
larger networks. The book credits only two algorithmic changes.

One algorithmic change is cross-entropy in place of MSE. That change greatly improved models with sigmoid
and softmax outputs. The other change is piecewise-linear units in place of sigmoid (§6.6, pp. 249–251).
The second lesson is the observation that designing a model that is easy to optimize is usually easier than
designing a more powerful optimizer (§10.11, pp. 429–430).

No architecture after 2016 is described in the 2016 procedure. The modern update adds **one prior and one
precondition**, and not an architecture. The prior is the content-based all-to-all connection, in the §3.2
register. The precondition is the pretraining-scale condition on the routing of §3.1.

Both additions are marked in place. Neither comes with a model specification, a variant catalogue or a
ranking. The plan governing this lineage forbids an architecture encyclopaedia. This SOP carries forward
the 2016 rule that a model family is not a benchmark.
