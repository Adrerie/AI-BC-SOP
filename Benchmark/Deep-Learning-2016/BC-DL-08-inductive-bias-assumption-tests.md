# BC-DL-08 — Do the architectural priors hold, and does violating them cost what the book predicts?

**Tests:** the assumptions behind sparse interaction, parameter sharing, equivariance, pooling and depth ·
**Executed by:** [`SOP-DL-07`](../../SOP/Deep-Learning-2016/SOP-DL-07-choose-and-test-inductive-bias.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

Each structural bias encodes an assumption. This benchmark tests those assumptions, and the costs the book
attaches to breaking an assumption.

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

- **a**: Run a trained convolutional layer on inputs shifted by a known δ, and compare the output feature
  maps after the same shift. Declare the boundary handling, the stride and the padding, because each can
  break exactness.
- **b**: Run the same layer under scaling and rotation. Compare the layer against a network that replicates
  detectors over the transformation group and pools across channels.
- **c**: Run three pooling conditions on a task that requires precise spatial information. The conditions are
  no pooling, pooling on all channels, and pooling on a subset of channels. The book's example of such a task
  is a corner defined by two edges. Training error is the primary readout, because the book predicts that the
  prior itself causes **underfitting**.
- **d**: Compare four connectivities: convolution, a dense layer, a locally connected ("unshared convolution")
  layer, and a tiled convolution. Build all four with the **same adjacency structure**. Measure parameter
  storage, floating-point operations and validation error. Compare per-position bias with per-channel bias, as
  edge-versus-centre accuracy under zero padding.
- **e**: Compare a dataset with position-dependent semantics, where centred objects have parts that occupy
  predictable rows, against a dataset with translation-invariant statistics. Run each dataset under shared
  connectivity and under unshared connectivity.
- **f**: Evaluate a convolutional model and a non-convolutional model of comparable parameter count on the
  same benchmark. Add a **pixel-permuted** version of the benchmark. Declare the benchmark's symmetry class
  before the comparison.
- **g**: Run a depth sweep at **matched parameter count**. Use a width-only arm as the null condition.
- **h**: Rank several candidate convolutional architectures by training only the last layer on random or
  k-means features. Then compare that ranking against full supervised training of each architecture.
- **i**: Run a padding sweep between valid and same convolution.
- **j**: Compare several activation functions on the same task, including at least one unconventional choice.

> **Modern update (2017–2026) — one added comparison condition on arms a/b, and no new arm.** Arms a–j are
> the 2016 book's own tests and are unchanged. Arms a and b test whether a network has translation
> equivariance. The arms also test whether the network must learn other group equivariances by replicating
> detectors and pooling across channels. The modern material adds a distinction that arms a and b can now
> use. The metric and the baseline stay the same:
>
> - **a/b, added condition: given versus learned.** A convolutional layer is equivariant to spatial
>   translation at every layer. Such a layer takes the 2D structure of the image into account by
>   construction. In an attention-based network that equivariance "**must be learned**". Run the existing
>   equivariance-error metric (metric 1) on two models. One model has the prior built in, and the other model
>   must acquire the prior. Run the two models **at matched data**. The two measurements are not comparable
>   unless you report the data budget with both. The modern account is explicit about what closes the gap. The
>   account states that the strong convolutional inductive bias "can only be superseded by employing extremely
>   large amounts of training data". So the informative quantity is *equivariance error as a function of data
>   budget*, not either endpoint alone. The primary vision source states the same condition from the other
>   side. That source reports the low-bias architecture with pre-training on large data. On transfer to
>   mid-sized or small benchmarks, the architecture does very well at substantially lower training cost. On
>   ImageNet-scale data only, the same architecture self-reports accuracies below comparable convolutional
>   networks. Say whether the data budget of a comparison is plausibly in the regime where the gap should
>   close. Report that budget with the result.
> - **Why this is a condition and not an arm.** The condition changes nothing about what is measured, about
>   the baseline, or about what counts as failure. The condition adds a second subject. Arms a and b now make
>   the equivariance claim about that second subject. The arm structure, the baseline set in §3 and the
>   metrics in §4 are untouched.
> - **No architecture is specified.** The plan governing this lineage says that a model family is not a
>   benchmark. The 2016 package says the same. So this benchmark creates no transformer entry, and no
>   vision-transformer entry. The quantity under test is the *prior*: whether equivariance is given or
>   learned. Arms a and b already measure exactly that quantity.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §2.3. Sources: `UDL`
> §12.10 fol. 229–230; `VIT` (abstract, introduction, conclusion).*

## 3. Baselines

- Arms a/b use the identity transform (δ = 0). Arm b also uses a translation-only control.
- Arm c uses the no-pooling network at matched parameter count.
- Arm d uses the dense layer at the same input and output size, and the locally connected layer at the same
  adjacency. These arms form the book's own control triad.
- Arm f: the pixel-permuted benchmark is the control that separates "the prior helped" from "the benchmark
  rewards the prior".
- Arm g uses the width-only arm.
- Arm h uses full supervised training of each candidate.
- Arm j uses the default piecewise-linear unit.

## 4. Metrics

1. Measure the **equivariance error**, the distance between the shifted output and the output of the shifted
   input. Take the distance as a function of δ (arm a). Take the distance also under scaling and rotation
   (arm b).
2. Measure **training error and validation error** with pooling and without pooling. Also record
   localization accuracy (arm c).
3. Measure **parameter storage, floating-point operations and validation error** across the connectivity
   triad (arm d).
4. Take **edge-versus-centre accuracy** for per-position bias versus per-channel bias (arm d).
5. Record **validation error versus depth at matched parameter count**. Also record the parameter count at
   which the shallow arm begins to overfit (arm g).
6. Record the **rank correlation between the last-layer-only screening and full training** (arm h).
7. Record **validation error versus padding amount** (arm i).
8. Record **validation error per activation function** (arm j). Report the result with the publication-bias
   caveat.

The book supplies no tolerance for equivariance error, no parameter-count ladder and no screening-accuracy
threshold. Each of the three is an evaluator choice.

## 5. How to interpret failure

- **Arm a fails** ⇒ the layer is not a pure convolution. Pooling, stride, padding or boundary handling
  intervenes. Report which one intervenes, because equivariance is a property of convolution alone (§9.2,
  p. 360).
- **Arm b fails for translation but holds for rotation** ⇒ the network learned the transformation group by
  replication and channel pooling. The result is the book's prescribed mechanism, not a contradiction (§9.2,
  p. 360; Fig. 9.9, p. 363).
- **Arm c: training error rises with pooling** ⇒ the infinite prior is wrong for this task. The rise is
  exactly the book's prediction. The remedy is to pool fewer channels, or to pool no channels at all (§9.4,
  p. 366).
- **Arm d shows a runtime saving from sharing** ⇒ the implementation does not exploit sparsity in the dense
  arm. Or the comparison uses different adjacency structures. If only non-zeros are stored, the flops are the
  same (§9.2, p. 360).
- **Arm e shows no penalty for sharing on position-dependent data** ⇒ the position semantics in the dataset
  were not actually position-dependent. Verify the dataset with the per-position bias arm.
- **Arm f: the convolutional model wins on the original benchmark and loses on the permuted version** ⇒ the
  benchmark embeds spatial knowledge. The comparison class was incommensurable. Declare the benchmark's
  symmetry class in the report (§9.4, pp. 366–367).
- **Arm g: width-only matches depth at equal parameter count** ⇒ the test does not reproduce the depth claim
  for this task. The book's own caveat applies. We cannot guarantee that the target function class has the
  property the expressivity results require (§6.4, p. 225).
- **Arm h: the screening ranking disagrees with full training** ⇒ the screening heuristic is invalid here. The
  book offers the ranking as a heuristic. The book adds that the benefit of unsupervised or random feature
  learning remains unclear. The unclear benefit is either regularization, or merely the enabling of larger
  architectures (§9.9, p. 383).
- **Arm j: an unconventional activation matches the default** ⇒ the result is consistent with the book's
  publication-bias warning. A new unit matters only if the unit demonstrably improves (§6.3, pp. 220–221).

> **Modern update (2017–2026) — two interpretation rules, no change to any arm.** The bullets above stand. The
> modern update adds two readings. Both readings are about how a result is *reported*, not about what is
> measured.
>
> - **Arms a/b, given-versus-learned condition.** Where you ran the added condition in §2, use the reading
>   below. A large equivariance error in the model that must **learn** the equivariance is not a failure of
>   that model. That error is not comparable to the same measurement on a model that has the prior built in.
>   The two measurements are not comparable unless you report the data budget with both. The modern account
>   states that the gap closes only with extremely large amounts of training data. So the informative quantity
>   is *equivariance error as a function of data budget*, not either endpoint alone. Say whether the data
>   budget of a comparison is plausibly in the regime where the gap should close. Report that budget with
>   the result.
> - **Arm g, the depth claim is contested in both directions.** Arm g carries an existing caveat. The caveat
>   is that we cannot guarantee the target function class has the property the expressivity results require.
>   That caveat is necessary, but no longer sufficient. The modern anchor gives its own verdict on depth. "the
>   balance of evidence suggests that depth is critical; even the shallowest networks with good image
>   classification performance require >10 layers. However, there is no definitive explanation for why" — that
>   is the anchor's verdict. The anchor also records substantial counter-evidence. Wider and shallower
>   residual networks match deeper networks. A 12-layer parallel-channel network is the second piece of
>   counter-evidence. The third is the finding that predominantly **shorter** paths of 5–17 layers drive
>   performance in residual networks. The depth-separation results carry a qualification. Some of those
>   results cannot easily be fit in practice. The anchor also states that there is "little evidence that the
>   real-world functions that we are approximating have these pathological properties". One direction does
>   support depth: distillation. Shallow students could not replicate a deeper teacher. Student performance
>   increased with depth at a **constant parameter budget**. Distillation matches arm g's own
>   matched-parameter design. So distillation is the closest modern analogue this benchmark has.
>
>   Read an arm-g result as evidence about *this* task, *this* optimizer and *this* parameter ladder. Do not
>   report an arm-g result as settling depth against width. The 2016 package already declined to make that a
>   benchmark claim. The modern evidence does not overturn that decision. That evidence confirms the question
>   is open.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §2.3, §2.5. Sources:
> `UDL` §12.10 fol. 229–230, §20.6 fol. 418–419, §20.6.1–§20.6.2; `VIT`.*

## 6. Validity limits and source traceability

- Arm a's exactness holds for pure convolution. Any stride, padding or pooling changes the statement.
- Arm f restricts the comparison class by construction. The book states that you can compare a convolutional
  model in a benchmark only against other convolutional models. The book also states that image benchmarks
  split into two kinds: permutation-invariant ones, and ones where the designer embedded spatial knowledge
  (§9.4, pp. 366–367). Results do not transfer across those two classes.
- Arm g's numbers (20 million, 60 million) come from one 2016-era study on address-photo digit transcription.
  The numbers are an illustration of the matched-parameter-count method, not thresholds.
- Arm d's worked arithmetic is the book's own example. The example is a 2-tap edge detector on a 320 × 280
  image: 267,960 flops versus more than 16 billion dense. The book's own non-zero-storage caveat undercuts
  that example. Use the example as a scale illustration only.
- Architecture rankings are unstable. A new best structure was published every few months or weeks. At the
  time of writing the book, the field could hardly say which structure was best (§9 intro, p. 350). Report no
  arm here as a standing ranking.
- Theory cannot settle arm j. The book states that there are not many clear guiding principles for hidden
  units. The book also states that no one can predict the winner in advance (§6.3, p. 216).

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

**Modern-update provenance.** Every row above is a 2016-book locator, and none was altered. Two
modern-update blocks were added. The first is the given-versus-learned comparison condition on arms a/b in §2.
The second block holds the two interpretation rules in §5. The two blocks are sourced outside the 2016 book.
The blocks are recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§2.3 and §2.5. The source keys are defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1: `UDL` §12.10 fol. 229–230 and
§20.6 fol. 418–419, and `VIT`. The claim under test, the arm list, the baselines in §3 and the metrics in §4
are unchanged. No arm was added, and no metric was introduced that a source does not name.

**Historical boundary.** The 20M/60M observation comes from a study of digit transcription on address
photographs, cited by the book. The named component menus are book-era: the activations (Leaky ReLU, PReLU,
maxout, softplus, hard tanh, RBF), the convolution variants (locally connected, tiled, grouped and strided
convolution), and the padding names (valid/same/full padding as MATLAB terminology). The deployment examples
(AT&T check reading, Microsoft OCR and handwriting) are book-era too.

The 2016 verdict is recorded as a period statement (§9.9, p. 383). The verdict is that purely supervised
training was by then the norm for most convolutional networks. Before that verdict, unsupervised or
patch-wise feature learning was popular roughly 2007–2013.

The modern update amended the closing sentence of this note. That sentence previously said that this benchmark
introduces no post-2016 architecture. The statement remains true in substance, and is now stated precisely:
**no architecture is introduced**, post-2016 or otherwise.

§2's added condition and §5's added rules introduce a *prior* and its acquisition cost. The first part is
whether translation equivariance is given at every layer, or must be learned. The second part is what data
budget that difference requires. The plan governing this lineage says that a model family is not a benchmark.
The standing rule in this package's README says the same. So this benchmark creates no architecture entry, no
variant catalogue and no family ranking.
