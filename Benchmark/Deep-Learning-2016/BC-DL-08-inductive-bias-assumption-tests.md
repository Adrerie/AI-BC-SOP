# BC-DL-08 — Do the architectural priors hold, and does violating them cost what the book predicts?

**Tests:** the assumptions behind sparse interaction, parameter sharing, equivariance, pooling and depth ·
**Executed by:** [`SOP-DL-07`](../../SOP/Deep-Learning-2016/SOP-DL-07-choose-and-test-inductive-bias.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

Each structural bias encodes an assumption. This benchmark tests the assumptions and the costs the book
attaches to violating them.

| Arm | Claim under test | Locator |
| --- | --- | --- |
| a | Convolution is translation-**equivariant**: shifting the input shifts the output representation, which is what supplies a *where* representation | §9.2, p. 360 |
| b | Convolution is **not naturally equivariant** to other transformations such as scaling or rotation; equivariance to those groups must be learned by replicating detectors over the group and pooling across channels | §9.2, p. 360; Fig. 9.9, p. 363 |
| c | Pooling buys approximate invariance to small translations, but preserving the exact location of features matters in some domains, and pooling all features increases **training** error when precise spatial information is required | §9.3, p. 362; §9.4, p. 366 |
| d | Parameter sharing reduces storage and improves statistical efficiency but is **not** a runtime saving: if only non-zero entries are stored, matrix multiplication and convolution require the same number of floating-point operations | §9.2, p. 360 |
| e | Sharing breaks where positions carry different semantics — the book's example is centred face crops, where upper units should look for eyebrows and lower units for a chin | §9.2, p. 360 |
| f | Convolution and pooling are **infinitely strong priors**: data cannot override them, so they can cause underfitting; and a convolutional model can only be compared against other convolutional models in a benchmark, because a non-convolutional model can still learn after all pixels are permuted | §9.4, pp. 365–367 |
| g | Depth, not parameter count, carries the generalization benefit: adding parameters inside convolutional layers without adding depth has almost no effect, while shallow models overfit near 20 million parameters and deep models still perform well past 60 million | §6.4, pp. 226–227, Figs. 6.6–6.7 |
| h | Random convolution-and-pooling layers are already frequency-selective and translation-invariant, so architectures can be screened by training only the last layer | §9.9, p. 383 |
| i | The optimum for test accuracy in zero padding usually lies between valid and same convolution | §9.5, p. 371 |
| j | Activation choice cannot be predicted from theory, and publication bias means many unpublished activations match the popular ones | §6.3, pp. 216, 220–221 |

## 2. Data and comparison conditions

- **a**: a trained convolutional layer and inputs shifted by a known δ, with the output feature maps compared
  after the same shift. Boundary handling, stride and padding must be declared, since they are what can break
  exactness.
- **b**: the same layer under scaling and rotation, and a comparison against a network that replicates
  detectors over the transformation group and pools across channels.
- **c**: three pooling conditions — no pooling, pooling on all channels, and pooling on a subset of channels —
  on a task that requires precise spatial information (the book's example is a corner defined by two edges).
  Training error is the primary readout, since the book predicts the prior itself causes **underfitting**.
- **d**: convolution versus a dense layer versus a locally connected ("unshared convolution") layer versus a
  tiled convolution, all with the **same adjacency structure**, measuring parameter storage, floating-point
  operations and validation error. Per-position bias versus per-channel bias is measured as edge-versus-centre
  accuracy under zero padding.
- **e**: a dataset with position-dependent semantics (centred objects whose parts occupy predictable rows)
  versus one with translation-invariant statistics, under shared and unshared connectivity.
- **f**: a convolutional model and a non-convolutional model of comparable parameter count evaluated on the
  same benchmark, plus a **pixel-permuted** version of the benchmark. The benchmark's symmetry class must be
  declared before the comparison.
- **g**: a depth sweep at **matched parameter count**, with a width-only arm as the null condition.
- **h**: several candidate convolutional architectures ranked by training only the last layer on random or
  k-means features, then the ranking compared against full supervised training of each.
- **i**: a padding sweep between valid and same convolution.
- **j**: several activation functions, including at least one unconventional choice, compared on the same task.

> **Modern update (2017–2026) — one added comparison condition on arms a/b, and no new arm.** Arms a–j are
> the 2016 book's own tests and are unchanged. Arms a and b test whether a network has translation
> equivariance and whether other group equivariances must be learned by replicating detectors and pooling
> across channels. The modern material makes a distinction those arms can now be run with, using the same
> metric and the same baseline:
>
> - **a/b, added condition: given versus learned.** A convolutional layer is equivariant to spatial
>   translation at every layer and takes the 2D structure of the image into account by construction; in an
>   attention-based network that equivariance "**must be learned**". Run the existing equivariance-error
>   metric (metric 1) on both a model that has the prior built in and one that must acquire it, **at matched
>   data**, and report the data budget at which the comparison was made. The two are not comparable without
>   that budget, because the modern account is explicit about what closes the gap: the strong convolutional
>   inductive bias "can only be superseded by employing extremely large amounts of training data". The
>   primary vision source for this states the same condition from the other side — pre-trained on large data
>   and transferred to mid-sized or small benchmarks the low-bias architecture does very well at
>   substantially lower training cost, while trained only on ImageNet-scale data it self-reports accuracies
>   below comparable convolutional networks.
> - **Why this is a condition and not an arm.** It changes nothing about what is measured, what the baseline
>   is, or what counts as failure; it adds the second subject the equivariance claim is now made about. The
>   arm structure, the baseline set in §3 and the metrics in §4 are untouched.
> - **No architecture is specified.** Consistent with the plan governing this lineage and with the 2016
>   package's rule that a model family is not a benchmark, no transformer or vision-transformer entry is
>   created here. What is tested is the *prior* — whether equivariance is given or learned — which is exactly
>   the quantity arms a and b already measure.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §2.3. Sources: `UDL`
> §12.10 fol. 229–230; `VIT` (abstract, introduction, conclusion).*

## 3. Baselines

- Arm a/b: the identity transform (δ = 0) and, for b, a translation-only control.
- Arm c: the no-pooling network at matched parameter count.
- Arm d: the dense layer at the same input and output size, and the locally connected layer at the same
  adjacency — the book's own control triad.
- Arm f: the pixel-permuted benchmark is the control that separates "the prior helped" from "the benchmark
  rewards the prior".
- Arm g: the width-only arm.
- Arm h: full supervised training of each candidate.
- Arm j: the default piecewise-linear unit.

## 4. Metrics

1. **Equivariance error**: the distance between the shifted output and the output of the shifted input, as a
   function of δ (arm a), and under scaling and rotation (arm b).
2. **Training error and validation error** with and without pooling, plus localization accuracy (arm c).
3. **Parameter storage, floating-point operations and validation error** across the connectivity triad (arm d).
4. **Edge-versus-centre accuracy** for per-position versus per-channel bias (arm d).
5. **Validation error versus depth at matched parameter count**, and the parameter count at which the shallow
   arm begins to overfit (arm g).
6. **Rank correlation between the last-layer-only screening and full training** (arm h).
7. **Validation error versus padding amount** (arm i).
8. **Validation error per activation function**, reported with the publication-bias caveat (arm j).

The book supplies no tolerance for equivariance error, no parameter-count ladder and no screening-accuracy
threshold; those are evaluator choices.

## 5. How to interpret failure

- **Arm a fails** ⇒ the layer is not a pure convolution: pooling, stride, padding or boundary handling
  intervenes. Report which, since equivariance is a property of convolution alone (§9.2, p. 360).
- **Arm b fails for translation but holds for rotation** ⇒ the transformation group was learned by replication
  and channel pooling; that is the book's prescribed mechanism, not a contradiction (§9.2, p. 360; Fig. 9.9,
  p. 363).
- **Arm c: training error rises with pooling** ⇒ the infinite prior is wrong for this task, which is exactly
  the book's prediction; the remedy is to pool fewer channels or not at all (§9.4, p. 366).
- **Arm d shows a runtime saving from sharing** ⇒ the implementation is not exploiting sparsity in the dense
  arm, or it is comparing different adjacency structures; with only non-zeros stored the flops are the same
  (§9.2, p. 360).
- **Arm e shows no penalty for sharing on position-dependent data** ⇒ the position semantics were not actually
  position-dependent in this dataset; verify with the per-position bias arm.
- **Arm f: the convolutional model wins on the original benchmark and loses on the permuted one** ⇒ the
  benchmark embeds spatial knowledge and the comparison class was incommensurable. Declare the benchmark's
  symmetry class in the report (§9.4, pp. 366–367).
- **Arm g: width-only matches depth at equal parameter count** ⇒ the depth claim is not reproduced for this
  task; the book's own caveat is that we cannot guarantee the target function class has the property the
  expressivity results require (§6.4, p. 225).
- **Arm h: the screening ranking disagrees with full training** ⇒ the screening heuristic is invalid here; the
  book offers it as a heuristic and adds that the benefit of unsupervised or random feature learning remains
  unclear — regularization, or merely enabling larger architectures (§9.9, p. 383).
- **Arm j: an unconventional activation matches the default** ⇒ consistent with the book's publication-bias
  warning; a new unit matters only if it demonstrably improves (§6.3, pp. 220–221).

> **Modern update (2017–2026) — two interpretation rules, no change to any arm.** The bullets above stand.
> Two readings are added, both about how a result is *reported* rather than what is measured.
>
> - **Arms a/b, given-versus-learned condition.** Where the added condition in §2 was run, a large
>   equivariance error in the model that must **learn** the equivariance is not a failure of that model and is
>   not comparable to the same measurement on a model that has it built in — unless the data budget is
>   reported with it. The modern account states the gap closes only with extremely large amounts of training
>   data, so the informative quantity is *equivariance error as a function of data budget*, not either
>   endpoint alone. Report the budget at which the two were compared and say whether it is plausibly in the
>   regime where the gap should have closed.
> - **Arm g, the depth claim is contested in both directions.** Arm g's existing caveat — that we cannot
>   guarantee the target function class has the property the expressivity results require — is necessary but no
>   longer sufficient. The modern anchor's own verdict is that "the balance of evidence suggests that depth is
>   critical; even the shallowest networks with good image classification performance require >10 layers.
>   However, there is no definitive explanation for why", and it records substantial counter-evidence:
>   wider-shallower residual networks matching deeper ones; a 12-layer parallel-channel network; and the
>   finding that predominantly **shorter** paths of 5–17 layers drive performance in residual networks. The
>   depth-separation results are qualified by the finding that some cannot easily be fit in practice and that
>   there is "little evidence that the real-world functions that we are approximating have these pathological
>   properties". The direction that does support depth is distillation: shallow students could not replicate a
>   deeper teacher, and student performance increased with depth at a **constant parameter budget** — which is
>   arm g's own matched-parameter design, so it is the closest modern analogue this benchmark has.
>
>   Read an arm-g result as evidence about *this* task, *this* optimizer and *this* parameter ladder. Do not
>   report it as settling depth against width: the 2016 package already declined to make that a benchmark
>   claim, and the modern evidence does not overturn that decision — it confirms the question is open.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §2.3, §2.5. Sources:
> `UDL` §12.10 fol. 229–230, §20.6 fol. 418–419, §20.6.1–§20.6.2; `VIT`.*

## 6. Validity limits and source traceability

- Arm a's exactness holds for pure convolution; any stride, padding or pooling changes the statement.
- Arm f restricts the comparison class by construction: the book states a convolutional model can only be
  compared against other convolutional models in the benchmark, and that image benchmarks split into
  permutation-invariant ones and ones where the designer embedded spatial knowledge (§9.4, pp. 366–367).
  Results do not transfer across those two classes.
- Arm g's numbers (20 million, 60 million) come from one 2016-era study on address-photo digit transcription;
  they are an illustration of the matched-parameter-count method, not thresholds.
- Arm d's worked arithmetic (a 2-tap edge detector on a 320 × 280 image: 267,960 flops versus more than 16
  billion dense) is the book's own example and is undercut by its own non-zero-storage caveat; use it as a
  scale illustration only.
- Architecture rankings are unstable: a new best structure was published every few months or weeks, and at the
  time of writing it was hard to say which was best (§9 intro, p. 350). No arm here may be reported as a
  standing ranking.
- Arm j cannot be settled by theory: the book states there are not many clear guiding principles for hidden
  units and that the winner cannot be predicted in advance (§6.3, p. 216).

| Claim | Locator |
| --- | --- |
| Sparse interaction, parameter sharing, equivariance and the *where* representation; the flops caveat; the centred-face counterexample | §9.2, pp. 355–360, Fig. 9.4 |
| Learned equivariance by replication and channel pooling | §9.2, p. 360; Fig. 9.9, p. 363 |
| Pooling benefits; exact-location caveat; inverse-pass complication; mixed channels | §9.3, pp. 362–364 |
| Infinite-prior reading; underfitting risk; restricted comparison class; benchmark symmetry classes | §9.4, pp. 365–367 |
| Locally connected, tiled and grouped convolution; padding variants; per-position vs per-channel bias | §9.5, pp. 371–378 |
| Random and unsupervised feature screening; unclear benefit | §9.9, p. 383 |
| Depth as a statistical prior; harder to optimize; expressivity caveat; matched-parameter-count control and the 20M/60M observation | §6.4, pp. 223–227 |
| Hidden units: absence of guiding theory; publication-bias warning; admissibility split between feedforward and recurrent/probabilistic models | §6.3, pp. 216–222 |
| Architecture rankings unstable; no architecture-selection advice given | §9 intro, p. 350 |

**Modern-update provenance.** Every row above is a 2016-book locator and none was altered. Two
modern-update blocks were added: the given-versus-learned comparison condition on arms a/b in §2, and the two
interpretation rules in §5. They are sourced outside the 2016 book and recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§2.3 and §2.5, with source keys defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1: `UDL` §12.10 fol. 229–230 and
§20.6 fol. 418–419; `VIT`. The claim under test, the arm list, the baselines in §3 and the metrics in §4 are
unchanged: no arm was added, and no metric was introduced that a source does not name.

**Historical boundary.** The 20M/60M observation comes from address-photo digit transcription work cited by
the book; the named component menus (Leaky ReLU, PReLU, maxout, softplus, hard tanh, RBF; locally connected,
tiled, grouped and strided convolution; valid/same/full padding as MATLAB terminology) and the deployment
examples (AT&T check reading, Microsoft OCR and handwriting) are book-era. The 2016 verdict that most
convolutional networks are by then trained in a purely supervised way, after unsupervised or patch-wise feature
learning was popular roughly 2007–2013, is recorded as a period statement (§9.9, p. 383).

The closing sentence of this note was amended by the modern update. It previously stated that no post-2016
architecture is introduced. That remains true in substance and is now stated precisely: **no architecture is
introduced**, post-2016 or otherwise. What §2's added condition and §5's added rules introduce is a *prior*
and its acquisition cost — whether translation equivariance is given at every layer or must be learned, and
what data budget that difference requires. Consistent with the plan governing this lineage, and with the
standing rule in this package's README that a model family is not a benchmark, no architecture entry, variant
catalogue or family ranking is created here.
