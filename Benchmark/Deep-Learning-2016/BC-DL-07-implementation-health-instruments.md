# BC-DL-07 — Implementation-health instruments: is the number produced by the algorithm you think you ran?

**Tests:** whether a disappointing result is caused by the implementation rather than by the model or the
data · **Executed by:**
[`SOP-DL-06`](../../SOP/Deep-Learning-2016/SOP-DL-06-debug-deep-learning-experiment.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The book gives two reasons why a machine-learning system cannot be debugged by watching its outputs, and
this benchmark tests the instruments that get around them (§11.5, p. 450):

1. **Expected behaviour is unknown in advance.** A classifier reaching 5% test error may be at the
   achievable optimum or badly suboptimal; the number alone does not say which.
2. **Adaptive parts compensate for one another.** The book's worked example: an incorrectly implemented
   bias update that ignores the gradient (`b ← b − α` instead of a gradient step) drives all biases
   negative during training, yet the weights can adaptively compensate depending on the input
   distribution, so inspecting model outputs does not reveal the bug.

Consequently the instruments below are constructed to be *self-referential*: each creates a situation
whose correct answer is known in advance, or checks one part of the implementation independently of the
others (§11.5, p. 450).

Four instruments are tested:

- **I1 — tiny-dataset fit.** "Even a small model can fit a small enough dataset": a classifier with one
  training example can be fit by setting the output-layer bias alone; an autoencoder must reproduce one
  example; a generative model must consistently generate one example. Failure of any of these is very
  likely a software bug preventing successful optimization on the training set. The test extends to a
  small number of examples (§11.5, p. 451).
- **I2 — back-prop vs numerical derivative.** Required whenever gradients are implemented by hand or a new
  operation is added to an autodifferentiation library; an incorrect gradient expression is named as a
  common cause of failure (§11.5, p. 452).
- **I3 — activation and gradient histograms.** Pre-activation saturation, dead units, gradient growth or
  decay across depth, and the ratio of parameter-update magnitude to parameter magnitude (§11.5, p. 453).
- **I4 — per-step guarantee tests.** Many algorithms promise properties such as a non-increasing
  objective across iterations, exactly-zero derivatives for certain variables at every step, or all
  gradients zero at convergence (§11.5, p. 453).

## 2. Data and comparison conditions

**I1.** A subset of the training data reduced to one example, then to k examples. Three problem shapes
are specified by the book and each needs its own pass criterion: classification (correct label on the
single example), autoencoding (reproduction of the single example), generation (consistent generation of
the single example). The comparison condition is the model at its *production* size — the instrument's
point is that capacity is not the binding constraint at n = 1.

**I2.** Any differentiable function in the stack, evaluated at the current parameters. Conditions the
book fixes:
- use **centered differences** for accuracy rather than one-sided differences;
- choose the perturbation ε **large enough** that finite precision does not turn it into rounding error;
- for a vector-valued g whose full Jacobian would cost mn finite-difference evaluations, test the scalar
  projection `f(x) = uᵀ g(v x)` with random vectors u and v, and **repeat over several draws**, because a
  single projection can miss errors orthogonal to it;
- where complex arithmetic is available, complex-step differentiation permits ε as small as 10⁻¹⁵⁰ with
  negligible error, because no cancellation occurs (Squire and Trapp, 1998, as cited).

**I3.** Statistics collected after many training iterations — the book's suggested point is about one
epoch. Per activation family: for rectifiers, how often units switch off and whether any are permanently
off; for tanh units, the mean absolute pre-activation as a saturation indicator. Across depth: gradient
magnitude per layer. Per parameter group: update magnitude divided by parameter magnitude, with the
sparse-data caveat that some parameters are legitimately updated rarely (natural language is the book's
example) and must not be scored as stalled.

**I4.** One run per algorithm in the stack that makes a per-step promise, with a tolerance parameter set
in advance, because rounding means the promised conditions never hold exactly on a computer.

## 3. Baselines

- **I2's reference arm is the numerical derivative** (centered finite difference, or complex step where
  available) compared against the back-propagated value from the implementation under test.
- **I1's reference is the analytically known trivial solution**: for a single-example classifier the
  output bias alone suffices, so the pass criterion is not "good accuracy" but "the loss can be driven to
  its floor at all".
- **I3's reference values are the book's cited targets**: an update of roughly **1% of the parameter
  magnitude** per minibatch step is healthy, while **50%** and **0.001%** are the two named pathologies —
  too fast and too slow respectively (Bottou, 2015, as cited) (§11.5, p. 453).
- **I4's baseline is the algorithm's own stated guarantee**; there is no external reference.

## 4. Metrics

| Instrument | Metric | Pass reading |
| --- | --- | --- |
| I1 | Final training loss/error on 1 example, then on k examples | Reaches the floor for the shape (label correct / example reproduced / example generated) |
| I2 | Maximum and mean relative deviation between back-prop and numerical derivative; ε used; number of random projections | Deviation within the declared tolerance for every projection draw |
| I3 | Fraction of iterations a rectifier unit is off; count of permanently-off units; mean absolute pre-activation for tanh; gradient-magnitude ratio across depth; update-to-parameter ratio per group | No permanently-off units; gradient magnitude neither growing nor decaying monotonically across depth; update ratio near the ~1% order |
| I4 | Count of guarantee violations per run; tolerance used | Zero violations beyond tolerance |

The book supplies no tolerance for I2, no k for I1, no saturation thresholds for I3 and no violation
tolerance for I4. Each must be fixed and reported by the evaluator; none may be inferred from the
absence of a number in the source.

## 5. How to interpret failure

- **I1 fails** ⇒ a software bug is preventing successful optimization on the training set; the book's
  reading is explicit. Do **not** attribute the result to underfitting or to insufficient capacity, and
  do not enlarge the model (§11.5, p. 451). Proceed to I2.
- **I2 fails** ⇒ an incorrect gradient expression — the named common cause when implementing gradients or
  extending an autodiff library (§11.5, p. 452).
- **I2 passes but I1 fails** ⇒ the defect is elsewhere in the training loop: data routing, loss
  reduction, the update rule, or the save/reload path. The book's other named cause of a
  low-train/high-test signature is a mis-measured test error from a save-reload bug or from test data
  preprocessed differently from training data (§11.5, p. 451).
- **I2 shows large deviation only for small ε** ⇒ rounding error, not a gradient bug: ε was too small
  (§11.5, p. 452).
- **I2 shows deviation that disappears when more projections are drawn** ⇒ the first projection was
  nearly orthogonal to the error; the single-projection result was a false pass (§11.5, p. 452).
- **I3 shows permanently-off units or heavy saturation** ⇒ an activation/init/optimization problem;
  route to `SOP-DL-04`, since rapidly growing or vanishing gradients through depth can block
  optimization (§11.5, p. 453).
- **I3 update ratio near 50%** ⇒ steps are far too large; consistent with a learning rate above the
  optimum, where gradient descent can increase rather than decrease training error (§11.4.1, p. 443,
  Fig. 11.1). **Near 0.001%** ⇒ parameters move too slowly to make progress in the budget.
- **I3 flags some parameters as stalled** ⇒ check data sparsity first; rarely-updated parameters are
  expected under sparse inputs (§11.5, p. 453).
- **I4 violations within tolerance** ⇒ rounding, not a defect. **Beyond tolerance** ⇒ the algorithm is
  not implementing the property it claims (§11.5, p. 453).
- **All four instruments pass and the metric is still bad** ⇒ the implementation is exonerated; the
  residual belongs to the model or the data, and routing continues in `SOP-DL-02` (train error high ⇒
  capacity or data quality; gap high ⇒ regularization or more data, §11.3, pp. 440–442). Note the
  converse is not licensed: a healthy-looking output metric is **not** evidence of a healthy
  implementation, because adaptive parts compensate (§11.5, p. 450).

## 6. Validity limits and source traceability

- **I1 is a necessary-condition instrument.** Passing it shows that optimization can succeed on a
  trivially fittable problem; it does not show the implementation is correct at production scale.
- **I2's projection variant trades completeness for cost.** Finite differences yield one derivative at a
  time, so a full Jacobian costs mn evaluations; the random-projection test checks a scalar function
  instead and can miss errors orthogonal to the projection. Repeating over several u and v *reduces*
  that probability — the book's own framing — without eliminating it (§11.5, p. 452).
- **Complex-step differentiation requires complex arithmetic** to be available in the stack
  (§11.5, pp. 452–453).
- **The ~1% figure is a cited recommendation, not a derived bound** (Bottou, 2015, as cited); 50% and
  0.001% are illustrative pathologies. It is an order-of-magnitude target and must not be used as a hard
  acceptance threshold.
- **I4 applies only to algorithms that make per-step promises.** The book's examples are the
  approximate-inference algorithms of Part III that solve optimization problems algebraically
  (§11.5, p. 453); an algorithm with no stated guarantee has nothing to test.
- **None of these instruments measures generalization.** They localize cause; the fitting-regime read is
  a separate step (`SOP-DL-02`).

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

**Historical boundary.** Bottou (2015) and Squire and Trapp (1998) are citations made by the book and are
reported as such. The four instruments are stated as general practice and are not tied to any 2016
framework, library or hardware; no framework-specific test is added here. The sparse-data example
(natural language) is the book's own.
