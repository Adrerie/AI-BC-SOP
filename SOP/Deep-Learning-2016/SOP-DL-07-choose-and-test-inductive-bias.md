# SOP-DL-07 — Choose an inductive bias by its assumption, then test the assumption

**Stage:** design · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Make an architecture choice reviewable. For every structural bias adopted, record four things — what it
**assumes** about the data-generating process, what it **buys**, what **breaks** when the assumption is
false, and what to **measure** to detect the violation — and then run the paired comparison that tests it.

This is not an architecture tutorial and not a chapter summary. The book itself licenses the framing:
convolution and pooling are **infinitely strong priors**, so data cannot override them, and "卷积和池化
可能导致欠拟合" — convolution and pooling may cause underfitting (§9.4, p. 366). It also licenses the
restricted comparison class: a convolutional model "只能以基准中的其他卷积模型作为比较的对象", because a
non-convolutional model can still learn after all pixels are permuted (§9.4, p. 366). And it refuses to
hand out architecture recipes: a new best structure was being published every few months or even weeks, so
at the time of writing it was hard to say which was best, and the ideal architecture "必须通过实验，观测
在验证集上的误差来找到" — must be found experimentally by observing validation error (§9 intro, p. 350;
§6.4, p. 223).

Out of scope: output units and cost (`SOP-DL-01`), capacity sizing (`SOP-DL-02`), regularization
(`SOP-DL-03`), optimization repair (`SOP-DL-04`).

## 2. Inputs and assumptions

- The task specification from `SOP-DL-01`, including whether the whole input is available before an output
  is required.
- Stated knowledge of the data's structure: is there a topology (image grid, sequence order)? Do the same
  statistics hold at every position? Which transformations leave the label unchanged? Is the target a
  composition of simpler functions?
- The ability to run **matched-capacity controls**, without which depth and sharing claims cannot be
  separated from parameter-count effects (§6.4, pp. 226–227).
- A validation metric and the search protocol of `SOP-DL-05`.
- The benchmark's **symmetry class**: permutation-invariant, or one in which the designer has embedded
  spatial knowledge (§9.4, pp. 366–367). Comparisons across the two classes are not meaningful.

## 3. Procedure

### 3.1 Let data structure select the model class, then declare it as a 2016 default

1. The book's baseline routing (§11.2, pp. 439–440): fixed-size vector input under supervision ⇒ fully
   connected feedforward network; input with a known topology (images) ⇒ convolutional network; sequence
   input or output ⇒ gated recurrent network. This routing is a book-era default and is recorded as such.

### 3.2 Fill in the bias register

For each bias under consideration, complete the four columns. The entries below are the book's own
mappings.

**Sparse interaction** (§9.2, p. 355)
- Assumes: outputs depend on a local neighbourhood, kernel size k ≪ m.
- Buys: parameters m × n → k × n; per-example time O(m × n) → O(k × n); statistical efficiency. Deeper
  units still touch most of the input indirectly, so complex interactions are built from sparse primitives
  (Fig. 9.4).
- Breaks: when the task requires merging information from distant positions in the input — then the
  convolutional prior "may simply be incorrect" (§9.4, p. 366).
- Measure: training-error floor against a dense control at matched capacity, on an ablation that requires a
  distant-position conjunction.

**Parameter sharing** (§9.2, pp. 358–360)
- Assumes: the same statistics hold at every position.
- Buys: storage reduced to k parameters (often orders of magnitude below m) and statistical efficiency —
  explicitly **not** a runtime saving, since the forward pass remains O(k × n). The book's worked arithmetic
  (a 2-tap edge detector on a 320 × 280 image: 267,960 flops versus more than 16 billion for a dense layer)
  is undercut by its own caveat that if only non-zero entries are stored, matrix multiplication and
  convolution require the same number of floating-point operations (§9.2, p. 360).
- Breaks: where positions carry different semantics — the book's own example is centred face crops, where
  upper units should look for eyebrows and lower units for a chin (§9.2, p. 360).
- Measure: the triad the book defines at equal adjacency — locally connected ("unshared convolution",
  §9.5, p. 371) versus tiled convolution (storage grows by a constant equal to the number of kernels,
  p. 374) versus convolution; and per-position bias versus per-channel bias, which slightly reduces
  statistical efficiency but lets the model correct for statistical differences across image positions
  (§9.5, p. 378) — read as edge-versus-centre accuracy under zero padding.

**Equivariance** (§9.2, p. 360)
- Assumes: f(g(x)) = g(f(x)) for translation g.
- Buys: a *where* representation — convolution produces a two-dimensional map indicating where a feature
  appears in the input, and a delayed event yields the same representation later.
- Breaks: "卷积对其他的一些变换并不是天然等变的" — convolution is not naturally equivariant to other
  transformations such as scaling or rotation, which require other mechanisms (§9.2, p. 360). Note also that
  equivariance is not invariance: retaining position is exactly what pooling later discards.
- Measure: shift the input by δ and verify the output shifts by δ. For groups other than translation,
  equivariance must be *learned* by replicating detectors over the group and pooling across channels
  (Fig. 9.9, p. 363, uses three filters for a rotated '5').

**Pooling invariance** (§9.3, pp. 362–364)
- Assumes: presence matters more than precise location.
- Buys: approximate invariance to small translations; roughly k× fewer units into the next layer, which is a
  compute saving and, when the next layer is fully connected, a statistical and storage saving; fixed-size
  statistics from variable-size inputs.
- Breaks — stated as a caveat, not an endorsement: "保存特征的具体位置却很重要" (§9.3, p. 362; the example is
  a corner defined by two edges). Pooling all features "将会增大训练误差" when precise spatial information is
  required (§9.4, p. 366). Pooling also complicates architectures that need a top-down or inverse pass, such
  as Boltzmann machines and autoencoders (§9.3, p. 364).
- Measure: **training** error with and without pooling, plus localization accuracy; consider mixed channels —
  pooling only some of them (Szegedy et al., 2014a, as cited; §9.4, p. 366).

**Convolution and pooling as infinite priors** (§9.4, pp. 365–367)
- Assumes: zero probability mass on all weights outside a small contiguous receptive field, and weights
  equal to their neighbours' up to shift; pooling is an infinite prior of per-unit small-translation
  invariance.
- Buys: large statistical efficiency when the assumption holds.
- Breaks: infinite strength means the data cannot override the prior, so these priors can cause
  **underfitting** (§9.4, p. 366).
- Measure / validity limit: only against other convolutional models in the same benchmark (§9.4, p. 366).
  Declare whether the benchmark is permutation-invariant or embeds spatial knowledge. Implementing a
  convolutional network as a fully connected network under this prior is described as an enormous waste of
  computation; the framing is interpretive only.

**Depth versus width** (§6.4, pp. 223, 225–227)
- Assumes: one hidden layer already suffices to fit the training set, so depth is a *statistical* choice —
  a prior that the target is a composition of simpler functions, or a multi-step program whose intermediates
  may be counters or pointers rather than variation factors.
- Buys: deeper networks usually need fewer units and fewer parameters per layer, and often generalize to the
  test set more easily.
- Breaks: deeper networks are usually harder to optimize (§6.4, p. 223); the expressivity-separation results
  carry the caveat that we cannot guarantee the function class we want to learn has the required property
  (§6.4, p. 225).
- Measure: validation error versus depth at **matched parameter count**. The book's explicit control
  (Fig. 6.7, pp. 226–227, on address-photo digit transcription) is that adding parameters inside
  convolutional layers without adding depth has almost no effect, while shallow models overfit near 20
  million parameters and deep models still perform well past 60 million.

**Hidden-unit choice** (§6.3, pp. 216–222)
- Assumes: near-linear behaviour optimizes better — ReLU's first derivative is 1 where active and its second
  derivative is 0 almost everywhere, so its gradient direction is more useful than that of activations
  introducing second-order effects (§6.3, p. 217).
- Buys: ReLU as an excellent default, with bias initialized around 0.1 so units start active and pass
  derivative; maxout, which learns the activation itself, approximates any convex function, can give the next
  layer k× fewer weights, and whose redundancy resists catastrophic forgetting; identity hidden layers,
  factoring W = V U for (n + p)q parameters instead of np at the cost of a low-rank constraint.
- Breaks: ReLU cannot learn from examples that zero its activation; maxout has k weight vectors per unit and
  so usually needs more regularization unless the training set is large and k small; sigmoid and tanh
  saturate over most of their domain and are discouraged as feedforward hidden units, yet are **required** in
  recurrent networks, probabilistic models and some autoencoders where piecewise-linear activations are
  inadmissible; RBF units saturate to zero and are hard to optimize; softplus is smooth and non-saturating
  yet empirically worse than ReLU and is generally discouraged.
- Measure: empirically, because "还没有许多明确的指导性理论原则" — there are not many clear theoretical
  guiding principles, and the winner cannot be predicted in advance; the loop is intuition → build →
  validate (§6.3, p. 216). Isolated non-differentiability is acceptable, because training never reaches a
  gradient-zero minimum and implementations return a one-sided derivative (§6.3, pp. 216–217).

**Recurrence and unfolding** (§10.1, pp. 393–396; §10.2.3, pp. 406–407)
- Assumes: stationarity — p(next | current) does not depend on t.
- Buys: fixed model size regardless of sequence length, and one shared transition function at every step,
  which generalizes to unseen lengths and needs far fewer training samples than a model without parameter
  sharing; a tabular joint would need k^τ parameters, whereas the RNN's count is tunable independently of
  length.
- Breaks: "循环网络为减少的参数数目付出的代价是优化参数可能变得困难" — the price of fewer parameters is that
  optimizing them may become difficult (§10.2.3, p. 407); and the hidden state is necessarily a lossy summary
  of the past (§10.1, p. 394).
- Measure: hold out at longer τ than trained; per-position error; comparison against a variant conditioned on
  t. The book's remedy for non-stationarity is to feed t as an extra input, at the cost of having to
  extrapolate to unseen t (§10.2.3, p. 407).

**Which part of a recurrent network to make deep** (§10.5, pp. 415–417)
- Allocate capacity across all three blocks (input→hidden, hidden→hidden, hidden→output), but prefer
  **shallow state-to-state transforms**, because depth there lengthens the shortest path between t and t + 1
  — a one-hidden-layer MLP doubles it. If depth there is needed, add hidden-to-hidden skip connections. The
  book describes the evidence as strongly suggestive rather than proven.
- Measure: validation error per allocation, and the shortest-path length between consecutive time steps.

**Gating** (§10.10, pp. 425–429)
- Assumes: paths through time must have derivatives that neither vanish nor explode, and the correct time
  constant is input-dependent.
- Buys: the self-loop, described as LSTM's core contribution — a path on which the gradient persists; making
  that weight context-dependent means the time constant is itself a model output, so the accumulation scale
  changes per sequence even with fixed parameters; it generalizes leaky units from a constant to per-step
  weights and adds a learned reset of state after use.
- Breaks / ablation: variants of LSTM and GRU have difficulty clearly beating both original architectures
  simultaneously across tasks; the critical factor turns out to be the **forget gate**, and a +1 bias on it
  makes LSTM as robust as the best variants explored (§10.10.2, p. 429).
- Measure: maximum learnable dependency span, demonstrated first on artificial long-dependency datasets and
  then on real tasks (§10.10.1, p. 428).

**Encoder–decoder bottleneck** (§10.4, pp. 413–415)
- Assumes: a fixed-size context vector C can summarize the input.
- Buys: decoupling of input and output lengths, with encoder and decoder hidden sizes not required to match.
- Breaks: "维度太小而难以适当地概括一个长序列" — C's dimensionality is too small to adequately summarize a
  long sequence, observed in machine translation (§10.4, p. 415).
- Measure: task quality against input length. The stated fix is a variable-length C with attention tying C's
  elements to output elements (§10.4, p. 415).

**Bidirectionality** (§10.3, pp. 410–413)
- Assumes: the entire sequence is observable before outputs are needed — backward connections are legitimate
  only in that case.
- Buys: outputs depending on past and future while remaining most sensitive to x(t), without a fixed window,
  unlike feedforward or convolutional networks and look-ahead-buffer RNNs. The motivating case is
  coarticulation, where a phoneme's correct interpretation depends on several future phonemes or words.
- Breaks: invalid for online or causal generation — the networks earlier in the chapter are all described as
  having a causal structure; and RNNs applied to images cost more than convolutional networks, though they
  permit long-range lateral interaction within a feature map (§10.3, p. 413).
- Measure: whether deployment permits full-sequence observation; error versus look-ahead budget against a
  causal baseline.

**Recursive (tree) structure** (§10.6, pp. 417–419)
- A chain of length τ has depth τ, while a balanced binary tree has depth O(log τ). Measure the learnable
  span against a chain at equal τ. The book states that how best to construct the tree is explicitly
  unresolved.

**Explicit memory** (§10.12, pp. 432–435)
- Measure task success against a plain RNN and an LSTM on the same task; failure implies addressing, not
  capacity, is the bottleneck. Integer addressing is hard to optimize, soft (softmax) addressing keeps the
  model differentiable, and stochastic hard addressing is harder to train.

### 3.3 Test before trusting

2. For every bias adopted, run the paired comparison the book defines and report **which assumption** it
   tested: dense versus sparse at matched capacity; locally connected versus tiled versus shared at equal
   adjacency; pooled versus unpooled (and partially pooled); shallow versus deep at matched parameter count;
   chain versus tree at equal τ; causal versus bidirectional under the same look-ahead budget; fixed-size C
   versus length-varying C across input lengths.
3. **Screen architectures cheaply before paying for full training** (§9.9, p. 383): random
   convolution-and-pooling layers are already frequency-selective and translation-invariant, so evaluating
   several candidate convolutional architectures by training only the last layer, picking the best, and then
   training fully is a legitimate screening procedure. Carry the book's caveat: the benefit of unsupervised
   feature pretraining remains unclear — regularization, or merely enabling larger architectures.
4. **Sweep zero padding** rather than assuming it (§9.5, p. 371): the optimum for test accuracy usually lies
   between valid and same convolution.
5. **Declare the benchmark's symmetry class** before reporting any comparison (§9.4, pp. 366–367).
6. **Do not expect rankings to be stable** (§9 intro, p. 350). Record the date of any architecture claim.

## 4. Important failure modes

- **Adopting a prior whose assumption fails** and reading the resulting underfitting as insufficient
  capacity — the infinite-prior case cannot be fixed by more data (§9.4, p. 366).
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
- **Choosing an activation on theoretical grounds**; the book states there are no clear guiding principles
  and the winner cannot be predicted in advance (§6.3, p. 216).
- **Reporting a new activation as an advance** without heeding the publication-bias warning: many unpublished
  activations match the popular ones, and the authors' own MNIST run reached below 1% error with an
  unconventional activation (§6.3, pp. 220–221).
- **Using saturating units where piecewise-linear ones are admissible**, or piecewise-linear units where they
  are not — recurrent networks, probabilistic models and some autoencoders require the former (§6.3, p. 220).
- **Optimizing parameters in a shared-weight recurrent model as if the reduced parameter count were free**;
  the book names the difficulty explicitly (§10.2.3, p. 407).

## 5. Outputs and reporting

- The **bias register**: one row per adopted bias with assumes / buys / breaks / measure, each column
  sourced.
- The paired comparisons actually run, with their matched-capacity controls and the assumption each tested.
- The benchmark symmetry-class declaration.
- The depth-versus-width sweep at matched parameter count, with the validation-error criterion.
- The screening procedure used (last-layer-only ranking, if applied) and its caveat.
- A date stamp on every architecture claim, since rankings move faster than the source can record.
- Anything left to `SOP-DL-05` because it is a hyperparameter rather than a structural choice (padding
  amount, number of maxout pieces, hidden sizes per block).

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

**Historical boundary.** Treated as book-era and labelled wherever used: the §11.2 model-class routing and
unit menu; the verdict that gated RNNs were the most effective sequence models in practice at the time of
writing, with LSTM then GRU (§10.10, pp. 425, 428); explicit memory and neural Turing machines as the
frontier for tasks RNNs and LSTMs cannot learn (§10.12, p. 434); unsupervised or patch-wise feature learning
being popular roughly 2007–2013 while "today most convolutional networks are trained in a purely supervised
way" (§9.9, p. 383); the named component menus (Leaky ReLU, PReLU, maxout, softplus, hard tanh, RBF, mixture
density networks; locally connected, tiled, grouped and strided convolution; valid/same/full padding; ESNs
and reservoir computing; leaky units and clockwork-style update frequencies; peephole connections; memory
networks and neural Turing machines); the MNIST sub-1% result with an unconventional activation; the
address-photo digit transcription study behind Fig. 6.7; the ImageNet result credited with starting current
commercial interest (§9.11, p. 390); the AT&T check-reading and Microsoft OCR deployments (§9.11, p. 390);
framework-specific practices such as symbol-to-number differentiation in Torch and Caffe versus
symbol-to-symbol in Theano and TensorFlow (§6.5.5, p. 238). Two general lessons survive the era and are
retained: the book's verdict that core ideas were unchanged since the 1980s, with the gains attributed mainly
to larger datasets and networks, and only two algorithmic changes credited — cross-entropy replacing MSE,
which greatly improved models with sigmoid and softmax outputs, and piecewise-linear units replacing sigmoid
(§6.6, pp. 249–251); and the observation that designing a model that is easy to optimize is usually easier
than designing a more powerful optimizer (§10.11, pp. 429–430). No post-2016 architecture is introduced.
