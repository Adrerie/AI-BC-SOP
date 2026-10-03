# BC-DL-07 — Implementation-health instruments: is the number produced by the algorithm you think you ran?

**Tests:** whether a disappointing result is caused by the implementation rather than by the model or the
data · **Executed by:**
[`SOP-DL-06`](../../SOP/Deep-Learning-2016/SOP-DL-06-debug-deep-learning-experiment.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The book gives two reasons why watching the outputs cannot debug a machine-learning system. This benchmark
tests the instruments that get around those reasons (§11.5, p. 450):

1. **Expected behaviour is unknown in advance.** A classifier that reaches 5% test error may sit at the
   achievable optimum. The classifier may instead be badly suboptimal. The number alone does not say which
   case holds.
2. **Adaptive parts compensate for one another.** The book gives a worked example. An incorrectly implemented
   bias update ignores the gradient (`b ← b − α` instead of a gradient step). That update drives all biases
   negative during training. Even so, the weights can compensate adaptively, depending on the input
   distribution. So inspecting the model outputs does not reveal the bug.

The instruments below are therefore *self-referential*. Each creates a situation whose correct answer is known
in advance. Alternatively each checks one part of the implementation independently of the other parts
(§11.5, p. 450).

This benchmark tests four instruments:

- **I1 — tiny-dataset fit.** The reading is "Even a small model can fit a small enough dataset". Setting the
  output-layer bias alone can fit a classifier with one training example. An autoencoder must reproduce one example. A generative model must consistently generate one example. Failure of any of these
  tests is very likely a software bug. That bug prevents successful optimization on the training set. The
  test extends to a small number of examples (§11.5, p. 451).
- **I2 — back-prop vs numerical derivative.** Run this check whenever you implement gradients by hand. Run
  the check whenever you add a new operation to an autodifferentiation library. The book names an incorrect
  gradient expression as a common cause of failure (§11.5, p. 452).
- **I3 — activation and gradient histograms.** Read the pre-activation saturation, the dead units, and the
  gradient growth or decay across depth. Read the ratio of parameter-update magnitude to parameter magnitude
  (§11.5, p. 453).
- **I4 — per-step guarantee tests.** Many algorithms promise properties. One property is a non-increasing
  objective across iterations. Another is exactly-zero derivatives for certain variables at every step.
  Another is that all gradients are zero at convergence (§11.5, p. 453).

## 2. Data and comparison conditions

**I1.** Reduce a subset of the training data to one example, then to k examples. The book specifies three
problem shapes, and each needs its own pass criterion:

- classification: the classifier gives the correct label on the single example
- autoencoding: the autoencoder reproduces the single example
- generation: the generative model consistently generates the single example

The comparison condition is the model at its *production* size. The instrument's point is that capacity is
not the binding constraint at n = 1.

**I2.** Take any differentiable function in the stack. Evaluate the function at the current parameters. The
book fixes the conditions below:

- Use **centered differences**, for accuracy rather than one-sided differences.
- Choose the perturbation ε **large enough** that finite precision does not turn ε into rounding error.
- Test the scalar projection `f(x) = uᵀ g(v x)` with random vectors u and v, and **repeat over several
  draws**. A single projection can miss errors that are orthogonal to that projection. A full Jacobian for a
  vector-valued g would cost mn finite-difference evaluations.
- Where complex arithmetic is available, complex-step differentiation permits ε as small as 10⁻¹⁵⁰ with
  negligible error, because no cancellation occurs (Squire and Trapp, 1998, as cited).

**I3.** Collect the statistics after many training iterations. The book's suggested point is about one epoch.
Take the readings in three ways:

- For each activation family, take two readings. For rectifiers, record how often units switch off, and
  whether any unit is permanently off. For tanh units, record the mean absolute pre-activation as a
  saturation indicator.
- Across the depth of the network, record the gradient magnitude per layer.
- For each parameter group, record the update magnitude divided by the parameter magnitude. Note the
  sparse-data caveat. Training legitimately updates some parameters rarely. Do not score those parameters as
  stalled. Natural language is the book's example.

**I4.** Run one pass for each algorithm in the stack that makes a per-step promise. Set a tolerance parameter
in advance, because rounding means the promised conditions never hold exactly on a computer.

## 3. Baselines

- **I2's reference arm is the numerical derivative** (centered finite difference, or complex step where
  available) compared against the back-propagated value from the implementation under test.
- **I1's reference is the analytically known trivial solution.** For a single-example classifier the output
  bias alone suffices. So the pass criterion is not "good accuracy". It is whether "the loss can be driven to
  its floor at all".
- **I3's reference values are the book's cited targets** (Bottou, 2015, as cited) (§11.5, p. 453). An update
  of roughly **1% of the parameter magnitude** per minibatch step is healthy. **50%** and **0.001%** are the
  two named pathologies. **50%** is too fast, and **0.001%** is too slow.
- **I4's baseline is the algorithm's own stated guarantee.** There is no external reference.

## 4. Metrics

| Instrument | Metric | Pass reading |
| --- | --- | --- |
| I1 | Final training loss/error on 1 example, then on k examples | Reaches the floor for the shape (label correct / example reproduced / example generated) |
| I2 | Maximum and mean relative deviation between back-prop and numerical derivative; ε used; number of random projections | Deviation within the declared tolerance for every projection draw |
| I3 | Fraction of iterations a rectifier unit is off; count of permanently-off units; mean absolute pre-activation for tanh; gradient-magnitude ratio across depth; update-to-parameter ratio per group | No permanently-off units; gradient magnitude neither growing nor decaying monotonically across depth; update ratio near the ~1% order |
| I4 | Count of guarantee violations per run; tolerance used | Zero violations beyond tolerance |

The book supplies no tolerance for I2, no k for I1, no saturation thresholds for I3 and no violation
tolerance for I4. The evaluator must fix each value and report each one. Do not infer any of these values
from the absence of a number in the source.

## 5. How to interpret failure

- **I1 fails** ⇒ a software bug prevents successful optimization on the training set. The book's reading is
  explicit. Do **not** attribute the result to underfitting or to insufficient capacity. Do not enlarge the
  model (§11.5, p. 451). Proceed to I2.
- **I2 fails** ⇒ an incorrect gradient expression is the cause. The book names that cause as common when you
  implement gradients, or when you extend an autodiff library (§11.5, p. 452).
- **I2 passes but I1 fails** ⇒ the defect is elsewhere in the training loop. Check the data routing, the loss
  reduction, the update rule, and the save/reload path. The book names one other cause of a
  low-train/high-test signature. A save-reload bug can mis-measure the test error. Test data that is
  preprocessed differently from training data can give the same mis-measurement (§11.5, p. 451).
- **I2 shows large deviation only for small ε** ⇒ rounding explains the deviation, and a gradient bug does
  not. That ε was too small (§11.5, p. 452).
- **I2 shows deviation that disappears when you draw more projections** ⇒ the first projection was nearly
  orthogonal to the error. The single-projection result was a false pass (§11.5, p. 452).
- **I3 shows permanently-off units or heavy saturation** ⇒ the cause is an activation, init or optimization
  problem. Route the case to `SOP-DL-04`. Rapidly growing or vanishing gradients through depth can block
  optimization (§11.5, p. 453).
- **I3 update ratio near 50%** ⇒ the steps are far too large. That reading is consistent with a learning rate
  above the optimum. At such a rate gradient descent can increase training error rather than decrease
  training error (§11.4.1, p. 443, Fig. 11.1). **Near 0.001%** ⇒ the parameters move too slowly to make
  progress in the budget.
- **I3 flags some parameters as stalled** ⇒ check data sparsity first. Under sparse inputs you expect some
  parameters to update rarely (§11.5, p. 453).
- **I4 violations within tolerance** ⇒ rounding explains the violations, and a defect does not. **Beyond
  tolerance** ⇒ the algorithm does not implement the property that the algorithm claims (§11.5, p. 453).
- **All four instruments pass and the metric is still bad** ⇒ the implementation is exonerated. The residual
  belongs to the model or to the data. Continue the routing in `SOP-DL-02` (train error high ⇒ capacity or
  data quality; gap high ⇒ regularization or more data, §11.3, pp. 440–442). Do not draw the converse
  conclusion. A healthy-looking output metric is **not** evidence of a healthy implementation, because
  adaptive parts compensate (§11.5, p. 450).

## 6. Validity limits and source traceability

- **I1 is a necessary-condition instrument.** A pass shows that optimization can succeed on a trivially
  fittable problem. A pass does not show that the implementation is correct at production scale.
- **I2's projection variant trades completeness for cost.** Finite differences yield one derivative at a
  time, so a full Jacobian costs mn evaluations. The random-projection test checks a scalar function instead,
  and can miss errors orthogonal to the projection. Repeating the test over several u and v *reduces* that
  probability, which is the book's own framing. The repetition does not eliminate the probability
  (§11.5, p. 452).
- **Complex-step differentiation requires complex arithmetic** to be available in the stack
  (§11.5, pp. 452–453).
- **The ~1% figure is a cited recommendation, not a derived bound** (Bottou, 2015, as cited). The book names
  50% and 0.001% as illustrative pathologies. Do not use the ~1% figure as a hard acceptance threshold,
  because the figure is an order-of-magnitude target.
- **I4 applies only to algorithms that make per-step promises.** The book's examples are the
  approximate-inference algorithms of Part III that solve optimization problems algebraically (§11.5, p. 453).
  An algorithm with no stated guarantee has nothing to test.
- **None of these instruments measures generalization.** The instruments localize cause. The fitting-regime
  read is a separate step (`SOP-DL-02`).

| Claim | Locator |
| --- | --- |
| Why ML systems are hard to debug; unknown expected behaviour; compensating adaptive parts and the bias-update example | §11.5, p. 450 |
| Design principle: create a situation with a known answer, or check parts independently | §11.5, p. 450 |
| Mis-evaluation as among the most destructive errors; visualize behaviour, not only metrics | §11.5, pp. 450–451 |
| Train/test error as a software detector; save-reload and preprocessing-mismatch causes; ambiguity when both are high | §11.5, p. 451 |
| Tiny-dataset fit: single-example classifier via output bias; autoencoder reproduction; consistent generation; extension to small datasets | §11.5, p. 451 |
| Gradient checking: centered differences, ε sizing, mn cost, random-projection test `uᵀg(vx)`, repeated draws, complex-step at 10⁻¹⁵⁰ | §11.5, pp. 452–453 |
| Histograms of activations and gradients; rectifier off-frequency; permanently-off units; tanh mean absolute pre-activation; gradient growth/decay across depth; ~1% update-to-parameter ratio; 50% and 0.001% pathologies; sparse-data caveat | §11.5, p. 453 |
| Guarantee tests with tolerance: non-increasing objective, zero derivatives per step, zero gradients at convergence | §11.5, p. 453 |
| Routing of the residual: data-quality branch when a larger model and tuned optimization still fail | §11.3, pp. 440–442 |
| Learning rate above optimum can increase training error | §11.4.1, p. 443, Fig. 11.1 |

**Historical boundary.** Bottou (2015) and Squire and Trapp (1998) are the book's own citations, and are
reported as such. The book states the four instruments as general practice. The four instruments are not tied
to any 2016 framework, library or hardware. This benchmark adds no framework-specific test. The sparse-data
example (natural language) is the book's own.
