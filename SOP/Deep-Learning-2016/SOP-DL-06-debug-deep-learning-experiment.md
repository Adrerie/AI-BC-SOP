# SOP-DL-06 — Debug a deep-learning experiment

**Stage:** localize · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Decide whether a disappointing number is produced by the **algorithm**, by the **data**, by the
**implementation**, or by the **evaluation itself**, and localize it before changing the model.

The book states why this is hard, and the whole procedure follows from those two reasons (§11.5,
p. 450):

1. Expected behaviour cannot be known in advance — that is the point of using machine learning. A
   classifier reaching 5% test error may be at the achievable optimum or badly suboptimal, and
   nothing in the number alone says which.
2. Models have multiple adaptive parts that compensate for one another. The book's example: an
   incorrectly implemented bias update that ignores the gradient drives all biases negative during
   training, yet the weights can adaptively compensate depending on the input distribution, so
   inspecting model outputs alone does not reveal the bug (§11.5, p. 450).

Consequently every test below is designed either to create a situation whose correct answer is known
in advance, or to check one part of the implementation independently of the others (§11.5, p. 450).

Out of scope: choosing what to change once the cause is localized — capacity and data decisions go to
[`SOP-DL-02`](SOP-DL-02-diagnose-fitting-regime-and-capacity.md), regularization to
[`SOP-DL-03`](SOP-DL-03-select-regularization.md), optimization instability to
[`SOP-DL-04`](SOP-DL-04-diagnose-optimization-failure.md).

## 2. Inputs and assumptions

- A system with a declared objective and metric (`SOP-DL-01`) and a current read of training and test
  error.
- The ability to construct a **tiny subset** of the training data (down to a single example).
- Access to internal quantities: pre-activation values, activations, parameter gradients, parameter
  values.
- A finite-difference gradient checker, and optionally complex-step arithmetic.
- For each algorithm in the stack, the per-step guarantees it claims (see step 7).

## 3. Procedure

The order below is the book's own; steps 1–2 catch evaluation errors, 3–4 catch implementation errors,
5–7 catch numerical and algorithmic errors, and only step 8 treats the residual as a modelling
problem.

1. **Visualize the model performing the task, not just its metric.** Look at the images where
   detections partially overlap; listen to samples from a speech generation model. The book's warning
   is explicit: it is easy in practice to watch only quantitative measures such as accuracy or
   log-likelihood, and *mis-evaluating model performance may be among the most destructive errors*,
   because it makes a broken system look healthy (§11.5, pp. 450–451).
2. **Visualize the worst mistakes.** Most models emit a confidence-like quantity; for a
   softmax-output classifier the probability assigned to the most likely class serves as a confidence
   estimate. Rank examples by that confidence and inspect the highest-confidence **errors**, in
   particular among training examples the model finds hard to fit: this typically exposes problems in
   preprocessing or labelling rather than in the model (§11.5, p. 451). The book notes that
   maximum-likelihood training tends to slightly overestimate the probability of correct predictions,
   but that low model probabilities rarely correspond to correct labels, so the ranking remains
   informative (§11.5, p. 451).
   Worked example (§11.6, pp. 454–455): in the street-view transcription system the highest-confidence
   training errors turned out to be images cropped so tightly that digits were cut off — an address
   "1849" reduced to a visible "849". The fix was not to spend weeks improving the digit detector's
   crop accuracy but to systematically widen the crop box beyond the detector's predicted region;
   that single change raised coverage by 10 percentage points.
3. **Read the two errors as a software detector** (§11.5, p. 451).
   - Low training error, high test error ⇒ either genuine overfitting **or a mis-measured test
     error**. The two named causes of the latter: a bug when saving and reloading the trained model
     for test evaluation, or test data preprocessed differently from training data.
   - Both errors high ⇒ **ambiguous**: implementation bug and algorithmic underfitting are not yet
     distinguishable. Do not change the model; continue to step 4.
4. **Fit a tiny dataset.** Even a small model should fit a small enough dataset — a classifier with a
   single training example can be fit by setting the output-layer bias alone. The book's test set: a
   classifier that cannot correctly label one example, an autoencoder that cannot reproduce one
   example, or a generative model that cannot consistently generate one example is very likely
   blocked by a software bug that prevents successful optimization on the training set. Extend the
   test to a small number of examples once the single-example case passes (§11.5, p. 451).
5. **Compare back-propagated derivatives with numerical derivatives.** Required whenever you
   implement gradients yourself or add an operation to an autodifferentiation library — an incorrect
   gradient expression is a common cause of failure (§11.5, p. 452).
   - Use finite differences, and prefer the **centered difference** for accuracy.
   - Choose the perturbation ε **large enough** that finite precision does not turn it into rounding
     error (§11.5, p. 452).
   - Finite differences give one derivative at a time, so testing the gradient or Jacobian of a
     vector-valued function g costs mn evaluations. The book's cheaper route: test the scalar
     projection `f(x) = uᵀ g(vx)` with random vectors u and v — correct `f′(x)` requires correct
     back-propagation through g, but f has a single input and output so one finite-difference run
     suffices. Repeat over several draws of u and v, because a single projection can miss errors
     orthogonal to it (§11.5, p. 452).
   - If complex arithmetic is available, complex-step differentiation estimates the gradient with
     negligible error at ε as small as 10⁻¹⁵⁰, because the difference is taken across points rather
     than by cancellation (Squire and Trapp, 1998, as cited) (§11.5, pp. 452–453).
6. **Monitor histograms of activations and gradients** after many iterations, e.g. one epoch
   (§11.5, p. 453).
   - Pre-activation statistics show whether units saturate and how often. For rectifiers: how often do
     they switch off, and are any units permanently off? For tanh units: the mean absolute
     pre-activation indicates the degree of saturation.
   - Rapid growth or rapid decay of gradients through depth can block optimization.
   - Compare **parameter-gradient magnitude to parameter magnitude**. The book's cited target (Bottou,
     2015) is that a parameter should move by roughly **1% of its own magnitude** in one minibatch
     update — not 50%, and not 0.001% (which moves too slowly).
   - Some parameters may move at a healthy step size while others stall. When the data is sparse
     (natural language is the book's example), some parameters are updated rarely; keep that in mind
     before calling them stalled.
7. **Test the algorithm's own guarantees.** Many deep-learning algorithms promise per-step properties:
   the objective value does not increase across iterations, certain variables have exactly zero
   derivative at every step, all gradients are zero at convergence. Test each promise. Include a
   tolerance parameter, because rounding means these conditions never hold exactly on a computer
   (§11.5, p. 453).
8. **Route the residual.** Only now treat what remains as a modelling or data problem, using the
   book's branch (§11.3, pp. 440–442):
   - Training error too high, and a larger model plus carefully tuned optimization still fails ⇒
     suspect the **training data**: it may be too noisy, or it may not contain the inputs needed to
     predict the output. The prescribed response is to restart with cleaner data or richer features —
     not another architecture change.
   - Training error acceptable but the train/test gap unacceptable ⇒ regularization or more data; see
     `SOP-DL-03` and §11.3.
   - Optimization unstable or stalled ⇒ `SOP-DL-04`.
9. **Prefer the practical fix over the ambitious one when both are open.** The street-view team could
   have improved the detector's cropping accuracy over weeks and instead widened the crop box
   (§11.6, p. 455). Record which alternative was rejected and why, so the decision is reviewable.

## 4. Important failure modes

- **Watching metrics instead of behaviour.** The most destructive error class, because a
  mis-evaluated system reports healthy numbers (§11.5, p. 451).
- **Reading a mis-measured test error as overfitting.** Save/reload bugs and train/test preprocessing
  mismatches produce exactly the low-train/high-test signature (§11.5, p. 451).
- **Changing the model while "both errors high" is still ambiguous.** Without the tiny-dataset test,
  an implementation bug is absorbed into a capacity story (§11.5, p. 451).
- **Gradient bugs masked by compensation.** Other adaptive parameters hide an incorrect update rule,
  so output inspection cannot find it; only independent per-part checks can (§11.5, p. 450).
- **Gradient-check artifacts.** ε too small ⇒ rounding error read as a gradient bug; a single random
  projection ⇒ errors orthogonal to the projection go undetected (§11.5, p. 452).
- **Misjudging sparse-data parameters as stalled** (§11.5, p. 453).
- **Testing guarantees without tolerance**, so rounding produces spurious failures (§11.5, p. 453).
- **Fixing the wrong component.** The book's example fixes the data pipeline (crop box), not the
  detector, and gains 10 coverage points (§11.6, p. 455).

## 5. Outputs and reporting

- A debug log that maps each observed symptom → the test that localized it → the change made, in that
  order, so a later reader can see that localization preceded intervention.
- Tiny-dataset fit result: number of examples used, final training error, pass/fail.
- Gradient-check result: method (centered finite difference / complex step), ε used, number of random
  projections, maximum deviation observed.
- Activation and gradient summary: saturation statistics, dead-unit count, gradient magnitude trend
  across depth, and the update-to-parameter ratio per parameter group.
- Guarantee tests with their tolerances and outcomes.
- A closing attribution of the residual to one of: evaluation, implementation, data, capacity,
  optimization. If it cannot be attributed, say so — that is a finding, not a gap to paper over.

## 6. Source traceability

| Claim or step | Locator |
| --- | --- |
| Why ML systems are hard to debug: unknown expected behaviour; compensating adaptive parts (bias-update example) | §11.5, p. 450 |
| Visualize model behaviour; mis-evaluation as among the most destructive errors | §11.5, pp. 450–451 |
| Visualize worst mistakes; confidence from softmax; MLE slightly overestimates correct-class probability; preprocessing/labelling diagnosis | §11.5, p. 451 |
| Train/test error as software detector; save-reload and preprocessing-mismatch causes; ambiguity when both are high | §11.5, p. 451 |
| Fit a tiny dataset; single-example classifier, autoencoder, generative model | §11.5, p. 451 |
| Finite differences, centered difference, ε sizing, random-projection test, complex-step differentiation | §11.5, pp. 452–453 |
| Histograms of activations and gradients; saturation; gradient growth/decay; ~1% update-to-parameter ratio; sparse-data caveat | §11.5, p. 453 |
| Testing algorithmic guarantees with tolerance | §11.5, p. 453 |
| Data-quality branch when a larger model and tuned optimization still fail | §11.3, pp. 440–442 |
| Street-view transcription case: coverage at 98% precision target, highest-confidence training errors, crop widening, +10 coverage points | §11.6, pp. 453–455 |

**Historical boundary.** The running example is the street-view address transcription system
(Goodfellow et al., 2014d, as cited), a 2014-era production system; its numbers (98% human-level
precision, 95% coverage target, +10 coverage points) are properties of that system and dataset, not
transferable thresholds. The Bottou (2015) 1% update rule and the Squire and Trapp (1998) complex-step
trick are cited by the book and are recorded here as the book records them. The tests themselves —
tiny-dataset fit, gradient checking, activation/gradient monitoring, guarantee testing — are stated as
general practice and are not tied to any 2016 framework.
