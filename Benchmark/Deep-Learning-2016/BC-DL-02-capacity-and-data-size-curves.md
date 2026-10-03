# BC-DL-02 — Do the capacity and data-size curves behave as the fitting theory predicts?

**Tests:** whether the capacity and data-size curves behave as the book predicts · **Executed by:**
[`SOP-DL-02`](../../SOP/Deep-Learning-2016/SOP-DL-02-diagnose-fitting-regime-and-capacity.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The book's account of fitting makes six directional predictions. Two curves test the predictions. Unless a
researcher reproduces a prediction, a capacity story about the real model has no support. The reproduction
needs a setting where the optimum is computable.

1. **Training error decreases monotonically with capacity** (§5.2, p. 145). The decrease ends at the
   smallest achievable value, where the curve asymptotes.
2. **Generalization error is U-shaped in capacity** (§5.2, pp. 145–146, Fig. 5.3). Read the curve in three
   parts.
   - At the left end both errors are high. That part is the underfitting regime.
   - As capacity rises, training error falls while the gap widens.
   - Once the growth of the gap outpaces the fall in training error, the system is in the overfitting
     regime. That part lies past the optimal capacity.
3. **Expected generalization error never increases when training samples are added** (§5.2, p. 146).
4. **A fixed-capacity model below optimal capacity asymptotes above Bayes error** (§5.2, pp. 146–147,
   Fig. 5.4). **Training error can fall below Bayes error**, because the learner can memorize particular
   training examples. As the training set grows without bound, training error for any fixed-capacity model
   rises to at least Bayes error.
5. **Optimal capacity itself increases with training-set size** (§5.2, p. 147, Fig. 5.4). Optimal capacity
   stops increasing once the capacity suffices to capture the true complexity.
6. **Regularization traverses the same curve from the other side** (§5.2.2, pp. 149–150, Fig. 5.5). Take a
   high-capacity model. A very large weight-decay coefficient forces a constant function, which is
   underfitting. An appropriate coefficient recovers the true curvature. A coefficient approaching zero
   produces severe overfitting.

The failure mode under test is the *misdiagnosis* this machinery exists to prevent. A researcher calls a
result "overfitting" or "underfitting" without locating the result on the curve. The researcher then moves
the wrong lever.

## 2. Data and comparison conditions

The book supplies its own construction. Reproducing that construction is the cheapest way to make the
optimum computable (Fig. 5.4, p. 147):

- **Synthetic regression problem**. Generate y from a 5th-degree polynomial, with noise of appropriate
  magnitude. Generate a **single** test set. Then generate training sets of several different sizes.
- **Replication**. For each training-set size, generate 40 different training sets. Then draw 95%
  confidence-interval error bars. The book's figure reports exactly this design.
- The benchmark uses **two model arms**, both fitted in **closed form**. The first arm is a quadratic
  model, with fixed and deliberately insufficient capacity. The second arm chooses its polynomial degree by
  minimizing test error, and is the "optimal capacity" arm.
- **Overfitting reference arm** (Fig. 5.2, p. 144). Generate the training data by sampling x and computing
  y *deterministically* from a quadratic function. That construction is noiseless. Fit a 9th-degree
  polynomial whose parameter count exceeds the sample count. Solve the underdetermined normal equation with
  the Moore-Penrose pseudoinverse. The predicted pathology has three parts. The fitted function passes
  exactly through every training point. The fitted function has a deep valley between two data points, and
  the true function has no such valley. The fitted function grows sharply on the left, where the true
  function falls.
- **Regularization arm** (Fig. 5.5, pp. 149–150). This arm runs the same 9th-degree model at three
  settings of the weight-decay coefficient λ: very large, appropriate, and approaching zero.

Any report must state two conditions explicitly:

- The noiseless construction (Fig. 5.2) and the noisy construction (Fig. 5.4) are **different experiments**.
  Bayes error is zero in the noiseless construction and positive in the noisy construction. Claims 3–5 are
  meaningful only in the noisy construction.
- The degree-selection arm chooses its degree by minimizing **test** error. That choice makes the arm an
  **oracle upper bound**, not a deployable procedure, and the report must label the arm as such. The book's
  own rule is that test samples may not participate in model selection in any form (§5.3, p. 151). Report
  the arm as an upper-bound row. If a deployable arm is wanted, add one that selects degree on validation
  material.

Extension condition for deep models: claims 1–2 are what `SOP-DL-02` relies on when the SOP moves
architecture size. A second pass on the real model is required before the diagnosis is transferred. That
pass uses a capacity ladder by layers and units per layer, the same metric, and the same splits.

Report the two passes separately. The book warns that capacity bounds are rarely usable for deep learning.
The bounds are too loose, and effective capacity depends on the optimizer (§5.2, p. 145).

## 3. Baselines

| Arm | Role |
| --- | --- |
| Quadratic (closed form) | insufficient-capacity reference; predicted to asymptote above Bayes error |
| Degree selected on test error (closed form) | oracle optimal-capacity upper bound |
| Degree selected on validation error | deployable counterpart; its gap to the oracle measures the cost of honest model selection |
| 9th-degree, λ → 0 | maximum-capacity / overfitting reference |
| 9th-degree, λ very large | minimum-capacity / underfitting reference (constant function) |
| 9th-degree, λ appropriate | target: recovers the curvature despite excess representational capacity |
| Nearest-neighbour regression with tie averaging | non-parametric reference; predicted to reach the minimum possible training error on any regression dataset (§5.2, p. 146) |

## 4. Metrics

All are quantities the book itself uses:

1. **MSE on the training set** and **MSE on the test set**, per capacity point and per training-set size.
2. **The gap** (test MSE minus train MSE). The regime classification is made on this quantity (§5.2, p. 142).
3. **95% confidence-interval error bars** over the 40 training sets per size (Fig. 5.4's construction).
4. **Location of the minimum of the test-error curve** along the capacity ladder. That location is the
   empirical optimal capacity. Plot the location against training-set size, to test claim 5.
5. **Bayes error**, known by construction in the synthetic setting. Use the known Bayes error to test
   claim 4. Claim 4 predicts train MSE below the Bayes error, and fixed-capacity test MSE above the Bayes
   error.
6. For the overfitting arm, **the function's behaviour between and outside training points**. Take the
   valley depth between adjacent samples, and the growth at the domain edge. The book's diagnosis of the
   9th-degree fit concerns exactly these regions. The diagnosis does not concern training error, which is
   zero by construction (Fig. 5.2, p. 144).

The book gives no numeric threshold for "significant" curvature of the U. The book gives no capacity-ladder
spacing, and no minimum replication count beyond the 40 used in its own figure. Those items are the
evaluator's choices, and the evaluator must report the chosen values.

## 5. How to interpret failure

- **Test error monotone in capacity with no U** ⇒ the ladder did not span the transition. Many capacity
  knobs are discrete, so only a few points on the curve are reachable (§11.4.1, p. 443). Extend the range
  before you conclude that the account is wrong.
- **Training error not monotone decreasing** ⇒ the result is not a capacity result. Effective capacity is
  limited by the optimizer's ability to minimize the training cost. Representational capacity is not the
  only limit (§5.2, p. 144; §11.4.1, p. 442). Route the run to `SOP-DL-04`. In the closed-form arms, that
  outcome means a solver error, not a modelling finding.
- **Generalization error increasing with more training data** ⇒ the result is an assumption violation, not
  a capacity finding. The code breaks either the i.i.d. assumption or the shared data-generating
  distribution (§5.2, p. 142). Check the sampling code before anything else.
- **Insufficient-capacity arm reaching Bayes error** ⇒ the arm is not insufficient, and the construction is
  wrong. Claim 4 requires capacity below the optimal capacity.
- **Training error below Bayes error** ⇒ the outcome is expected and is not a defect. The cause is
  memorization (§5.2, p. 147).
- **Optimal capacity flat in training-set size** ⇒ either the true function is simpler than the ladder
  assumes. The alternative is that the ladder is too coarse to resolve the shift. The book predicts growth
  followed by saturation, not constancy (§5.2, p. 147).
- **Large λ recovering the true function while λ → 0 does not** ⇒ the run reproduces claim 6.
  Regularization, not capacity reduction, is the operative lever. The correct reading is that the
  preference over hypotheses controls the outcome, and not the size of the hypothesis space (§5.2.2,
  pp. 148–150).
- **Deep-model pass failing where the closed-form pass succeeded** ⇒ do not conclude that the theory is
  wrong. Capacity bounds are rarely applied to deep learning. The book gives the reasons: the bounds are
  too loose, and the capacity of a deep learning algorithm is hard to determine (§5.2, p. 145). The deep
  pass is evidence about the diagnosis, not about the bound.
- **No-free-lunch over-reading**: none of these results license a claim about algorithms averaged over all
  distributions. The theorem says every classification algorithm has the same error rate on unobserved
  points, under an average over all possible data-generating distributions. The theorem holds only under
  that averaging. The book's conclusion is to characterize the distributions that matter, rather than to
  abandon method choice (§5.2.1, pp. 147–148).

> **Modern update (2017–2026) — a rising right branch is no longer a confirmation by itself.** The first
> bullet above reads a monotone test error as evidence that the ladder did not span the transition. The
> claim under test reads a U as confirmation. Both readings remain correct for the 2016 account, and neither
> is withdrawn. A third reading is required before either conclusion is reported:
>
> - **A U that turns back down is not a failed replication.** The modern account distinguishes three
>   regimes. It reports a **second descent** beyond the interpolation threshold. Suppose the capacity ladder
>   spans that threshold and the error falls again. The report then names *which* regime boundary the run
>   crossed, rather than calling the U-curve falsified. **Predeclare** a ladder that covers the proposed
>   regimes, before you measure its held-out test curve. Any adaptive extension or capacity selection must
>   use development/validation data. A test-selected arm remains an explicitly labelled oracle (§2).
> - **The run must measure whether a second descent appears.** The measurement uses the data actually in
>   use. The source is explicit that the phenomenon is dataset-dependent. The phenomenon is present on MNIST
>   with the original labels. Under label noise, and on MNIST-1D and CIFAR-100, the phenomenon emerges or
>   becomes prominent. The second descent is therefore a property of this benchmark's data construction, not
>   a constant to import. A synthetic construction with no label noise is a legitimate case. That case may
>   show no second descent.
> - **This benchmark asserts no mechanism and computes no interpolation threshold.** The modern source
>   states its own explanation as putative. The location of the threshold is a property of the run. This
>   benchmark supplies neither.
> - **A flat or absent right branch is not evidence about parameter count.** That point stands apart from
>   the shape of the curve. The modern evidence concerns model size. State-of-the-art performance on complex
>   datasets almost never comes from models with significantly fewer parameters than training data points.
>   Pruned networks remain over-parameterized after pruning. Distillation provides no convincing evidence
>   that under-parameterized models perform well. One question stays open: whether small models
>   fundamentally cannot perform, or training merely cannot find good solutions for the small models. Read a
>   capacity-ladder result as a statement about *this* ladder and *this* optimizer, not about how many
>   parameters the problem needs.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §1.4, §1.5. Sources:
> `UDL` §8.4 fol. 127–132, §8.5 fol. 132, §20.5 fol. 415–418.*

## 6. Validity limits and source traceability

- The closed-form arms are **linear/polynomial regression**: the curves are demonstrated where the optimum
  is computable. Transferring the qualitative shape to deep non-convex models is an extrapolation, and the
  book itself limits how far capacity theory reaches (§5.2, p. 145).
- **Bayes error is known only by construction** in this benchmark. A real dataset exposes no Bayes error, so
  no evaluation can test claim 4 outside the synthetic setting.
- **VC dimension is not a metric in this benchmark.** The VC dimension is defined as the largest number of
  training points that a binary classifier can label arbitrarily. The VC dimension underwrites bounds in
  which the gap grows with capacity and shrinks with more samples. The book states that those bounds rarely
  apply to practical deep learning. The book gives the reasons: the bounds are too loose, and effective
  capacity depends on the optimizer (§5.2, pp. 144–145). This benchmark computes and reports no bound.
- The oracle arm is an **upper bound row** only (§5.3, p. 151).
- Results are conditional on the assumed data-generating family. The no-free-lunch theorem bounds any
  generalization beyond that family (§5.2.1, p. 148).
- This benchmark informs the data-size decision. The decision is a procedure: plot training-set size
  against generalization error, then extrapolate. Reason on a log scale, and double the sample count
  between experiments. The book expects that adding a small fraction of the current total changes little
  (§11.3, p. 441).

**Modern update (2017–2026) — one further validity limit (`delta_map.md` §1.3).** The capacity axis and the
data-size axis are each treated here as a single countable quantity. That treatment is what makes a curve
plottable. Under a modern construction that assumption can fail: once augmentation or tokenization enters,
"number of data points" is a choice rather than a measurement.

The modern anchor gives a worked case. The anchor describes a 60M-parameter network trained on ~1M examples.
That network applied 2048 transformations to each example. A 175B-parameter network was trained on 300B
tokens. The conclusion of the anchor is that "there is not a clear-cut case that either model was
overparameterized."

The arms of this benchmark are unaffected, because their synthetic constructions fix the training-set size
directly and apply no augmentation. Any transfer of these curve shapes to a real dataset must state **what
the run counts as a data point**. The choice is raw examples, augmented views, or tokens. The transfer must
not switch definitions between the capacity arm and the data-size arm. A curve whose two axes use different
counting conventions is not a curve.

| Claim | Locator |
| --- | --- |
| Training error, generalization error, the two success factors, underfitting/overfitting definitions | §5.2, pp. 141–142 |
| i.i.d. assumption, p_data, equality of expectations for a fixed model | §5.2, p. 142 |
| Capacity, hypothesis space, representational vs effective capacity | §5.2, pp. 143–144 |
| Polynomial ladder; 9th-degree overfitting with Moore-Penrose pseudoinverse; valley and edge behaviour | §5.2, pp. 143–144, Fig. 5.2 |
| Monotone training error; U-shaped generalization error; underfitting/optimal/overfitting regimes | §5.2, pp. 145–146, Fig. 5.3 |
| VC dimension and why bounds are rarely applied | §5.2, pp. 144–145 |
| Non-parametric models; nearest-neighbour regression with tie averaging; Bayes error; memorization below Bayes error | §5.2, p. 146 |
| Data-size construction: 5th-degree polynomial with noise, single test set, 40 training sets per size, 95% CI bars, closed-form quadratic vs test-error-selected degree; optimal capacity grows then saturates | §5.2, pp. 146–147, Fig. 5.4 |
| No free lunch and its scope | §5.2.1, pp. 147–148 |
| Regularization as a preference over hypotheses; weight decay λ; the three-λ demonstration | §5.2.2, pp. 148–150, Fig. 5.5 |
| Test data may not participate in model selection | §5.3, p. 151 |
| Effective capacity's three limits; discrete/bounded knobs sample few points | §11.4.1, pp. 442–443 |
| Log-scale data-size reasoning and doubling | §11.3, p. 441 |

**Modern-update provenance.** Every row above is a 2016-book locator, and no row was altered. The
modern-update block in §5 and the added validity limit in §6 are sourced outside the 2016 book. Both are
recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§1.3, §1.4, §1.5.

The source keys are defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1: `UDL` §8.4 fol. 127–132,
§8.5 fol. 132, §20.1.1 fol. 403, §20.5 fol. 415–418. The benchmark gained no new claim, arm, metric or
threshold. The claim under test, the comparison conditions, the baselines and the metrics are unchanged.

**Historical boundary.** Figures 5.2–5.5 are the book's own synthetic illustrations. Their constructions
(polynomial degrees, 40 replications, 95% intervals, closed-form fitting) are reproduced here as the
cheapest testbed. That reproduction is not a claim about how to evaluate deep models. Nothing in this
benchmark depends on 2016-era datasets, architectures or benchmark scores. The nearest-neighbour regression
arm is the book's example of a practical non-parametric model whose complexity tracks the training set
(§5.2, p. 146).

The **U-shape itself** is now partly era-scoped. The modern update added this sentence. The curve's left
branch and the underfitting/optimal/overfitting regime definitions are general. The expectation that
generalization error rises monotonically past the optimum is a 2016 default (see the modern-update block in
§5). The benchmark still tests the shape that the 2016 account predicts. What changed is that a different
shape is no longer automatically a falsification.
