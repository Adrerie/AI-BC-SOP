# SOP-DL-06 — Debug a deep-learning experiment

**Stage:** localize · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Decide what produces a disappointing number. The cause may be the **algorithm**, the **data**, the
**implementation**, or the **evaluation itself**. Localize the cause before you change the model.

The book states why debugging is hard, and the whole procedure follows from those two reasons (§11.5,
p. 450):

1. You cannot know the expected behaviour in advance. That uncertainty is the point of using machine
   learning. A classifier may reach 5% test error and sit at the achievable optimum. The same
   classifier may instead be badly suboptimal. Nothing in the number alone says which case holds.
2. Models have multiple adaptive parts that compensate for one another. The book gives an example. An
   incorrectly implemented bias update ignores the gradient, and that update drives all biases negative
   during training. The weights then compensate adaptively, depending on the input distribution. So an
   inspection of the model outputs alone does not reveal the bug (§11.5, p. 450).

Every test below therefore has one of two designs. The test creates a situation whose correct answer you
know in advance. Or the test checks one part of the implementation independently of the other parts
(§11.5, p. 450).

Out of scope covers the choice of what to change once the cause is localized:

- capacity and data decisions, which go to
  [`SOP-DL-02`](SOP-DL-02-diagnose-fitting-regime-and-capacity.md)
- regularization, which goes to [`SOP-DL-03`](SOP-DL-03-select-regularization.md)
- optimization instability, which goes to [`SOP-DL-04`](SOP-DL-04-diagnose-optimization-failure.md)

## 2. Inputs and assumptions

- A system with a declared objective and metric (`SOP-DL-01`), and a current read of the training error
  and the test error.
- The ability to construct a **tiny subset** of the training data, down to a single example.
- Access to the internal quantities: the pre-activation values, the activations, the parameter
  gradients, and the parameter values.
- A finite-difference gradient checker, and optionally complex-step arithmetic.
- For each algorithm in the stack, the per-step guarantees that the algorithm claims (see step 7).

## 3. Procedure

The order below is the book's own. Steps 1–2 catch evaluation errors. Steps 3–4 catch implementation
errors. Steps 5–7 catch numerical errors and algorithmic errors. Only step 8 treats the residual as a
modelling problem.

1. **Visualize the model performing the task, not just its metric.** Look at the images where detections
   partially overlap. Listen to samples from a speech generation model. The book's warning is explicit:
   *mis-evaluating model performance may be among the most destructive errors* (§11.5, pp. 450–451).
   That mistake is easy to make in practice. A broken system looks healthy when you watch only
   quantitative measures such as accuracy or log-likelihood.
2. **Visualize the worst mistakes.** Most models emit a confidence-like quantity. In a softmax-output
   classifier, the probability assigned to the most likely class serves as that confidence estimate.
   Rank the examples by that confidence. Inspect the highest-confidence **errors**, and look in
   particular among the training examples that the model finds hard to fit. That inspection typically
   exposes problems in preprocessing or labelling, rather than problems in the model (§11.5, p. 451).
   The book notes that maximum-likelihood training tends to slightly overestimate the probability of
   correct predictions. The book also notes that low model probabilities rarely correspond to correct
   labels. So the ranking remains informative (§11.5, p. 451).

   Worked example (§11.6, pp. 454–455). In the street-view transcription system, the highest-confidence
   training errors were images whose crops were too tight. The crop cut off digits in those images. The
   address "1849" lost its first digit, and only "849" stayed visible. The fix was not to spend weeks
   improving the crop accuracy of the digit detector. The fix was to widen the crop box systematically,
   beyond the region that the detector predicted. That single change raised coverage by 10 percentage
   points.
3. **Read the two errors as a software detector** (§11.5, p. 451).
   - Low training error and high test error ⇒ either genuine overfitting **or a mis-measured test
     error**. The book names two causes of a mis-measured test error. A bug can corrupt the model when
     you save it and reload it for test evaluation. Or the preprocessing of the test data can differ
     from the preprocessing of the training data.
   - Both errors high ⇒ the reading is **ambiguous**, because an implementation bug and algorithmic
     underfitting are not yet distinguishable. Do not change the model. Continue to step 4.
4. **Fit a tiny dataset.** Even a small model should fit a small enough dataset. A classifier with a
   single training example can be fit by setting the output-layer bias alone. The book names the cases
   for that test. A classifier that cannot correctly label one example is very likely blocked by a
   software bug. An autoencoder that cannot reproduce one example is blocked by the same kind of bug. A
   generative model that cannot consistently generate one example is blocked in the same way. Each of
   those bugs prevents successful optimization on the training set. Extend the test to a small number of
   examples once the single-example case passes (§11.5, p. 451).
5. **Compare back-propagated derivatives with numerical derivatives.** Run this comparison whenever
   you implement gradients yourself. Run the comparison whenever you add an operation to an
   autodifferentiation library. An incorrect gradient expression is a common cause of failure (§11.5,
   p. 452).
   - Use finite differences. Prefer the **centered difference** for accuracy.
   - Choose the perturbation ε **large enough** that finite precision does not turn ε into rounding
     error (§11.5, p. 452).
   - Finite differences give one derivative at a time. So a test of the gradient, or of the Jacobian,
     of a vector-valued function g costs mn evaluations. The book gives a cheaper route. Test a scalar
     projection with the random vectors u and v, where the projection is `f(x) = uᵀ g(vx)`. A correct
     value of `f′(x)` requires a correct back-propagation through g. The function f has one input and
     one output, so one finite-difference run suffices. Repeat the test for several pairs of those
     vectors. A single projection can miss an error that stands orthogonal to that projection (§11.5,
     p. 452).
   - If complex arithmetic is available, use complex-step differentiation. That method estimates the
     gradient with negligible error. The ε can be as small as 10⁻¹⁵⁰ in practice. The method takes the
     difference across two points, rather than by cancellation (Squire and Trapp, 1998, as cited)
     (§11.5, pp. 452–453).
6. **Monitor histograms of activations and gradients** after many iterations, for example one epoch
   (§11.5, p. 453).
   - Pre-activation statistics show whether units saturate, and how often that saturation happens. For
     rectifiers, ask how often a rectifier switches off. Ask whether any rectifier stays permanently
     off. For tanh units, the mean absolute pre-activation indicates the degree of saturation.
   - Rapid growth or rapid decay of gradients through depth can block optimization.
   - Compare **parameter-gradient magnitude to parameter magnitude**. The book cites a target from
     Bottou (2015). A parameter should move by roughly **1% of its own magnitude** in one minibatch
     update. A move of 50% is too large. A move of 0.001% moves the parameter too slowly.
   - Some parameters may move at a healthy step size while other parameters stall. When the data is
     sparse, some parameters are updated rarely. Natural language is the book's example of sparse data.
     Keep that fact in mind before you call such a parameter stalled.
7. **Test the algorithm's own guarantees.** Many deep-learning algorithms promise per-step properties:
   - the objective value does not increase across iterations
   - certain variables have exactly zero derivative at every step
   - all gradients are zero at convergence

   Test each promise. Include a tolerance parameter, because rounding means that these conditions never
   hold exactly on a computer (§11.5, p. 453).
8. **Route the residual.** Only now treat what remains as a modelling problem or a data problem. Use the
   book's branch (§11.3, pp. 440–442):
   - Training error too high, and a larger model plus carefully tuned optimization still fails ⇒ suspect
     the **training data**. The training data may be too noisy. The training data may not contain the
     inputs needed to predict the output. The prescribed response is to restart with cleaner data, or
     with richer features. Do not answer with another architecture change.
   - Training error acceptable but the train/test gap unacceptable ⇒ the residual is a regularization
     problem or a data problem. See `SOP-DL-03` and §11.3.
   - Optimization unstable or stalled ⇒ route the case to `SOP-DL-04`.
9. **Prefer the practical fix over the ambitious one when both are open.** The street-view team had two
   options open. One option was to improve the crop accuracy of the detector, over weeks. The team
   rejected that option and widened the crop box instead (§11.6, p. 455). Record which alternative was
   rejected, and record the reason for the rejection. That record makes the decision reviewable.

## 4. Important failure modes

- **Watching metrics instead of behaviour.** That is the most destructive error class, because a
  mis-evaluated system reports healthy numbers (§11.5, p. 451).
- **Reading a mis-measured test error as overfitting.** Save/reload bugs and train/test preprocessing
  mismatches produce exactly the low-train/high-test signature (§11.5, p. 451).
- **Changing the model while "both errors high" is still ambiguous.** Without the tiny-dataset test,
  an implementation bug is absorbed into a capacity story (§11.5, p. 451).
- **Gradient bugs masked by compensation.** Other adaptive parameters hide an incorrect update rule. So
  an inspection of the model outputs cannot find that bug. Only an independent check of each part can
  find the bug (§11.5, p. 450).
- **Gradient-check artifacts.** If ε is too small, rounding error looks like a gradient bug. If you use
  one random projection only, an error orthogonal to that projection goes undetected (§11.5, p. 452).
- **Misjudging sparse-data parameters as stalled** (§11.5, p. 453).
- **Testing guarantees without tolerance**, so rounding produces spurious failures (§11.5, p. 453).
- **Fixing the wrong component.** The book's example fixes the data pipeline (crop box), not the
  detector, and gains 10 coverage points (§11.6, p. 455).

## 5. Outputs and reporting

- Keep a debug log. The log maps each observed symptom → the test that localized that symptom → the
  change that you made, in that order. That order shows a later reader that localization came before the
  intervention.
- Record the tiny-dataset fit result: the number of examples used, the final training error, and whether
  the run passed or failed.
- Record the gradient-check result: the method (centered finite difference / complex step), the ε used,
  the number of random projections, and the maximum deviation observed.
- Record the activation and gradient summary. The summary holds the saturation statistics and the
  dead-unit count. The summary also holds the trend of gradient magnitude across depth, and the
  update-to-parameter ratio for each parameter group.
- Record the guarantee tests, with their tolerances and outcomes.
- Close with a statement that attributes the residual to one of these sources: evaluation,
  implementation, data, capacity, optimization. If you cannot attribute the residual to one of those
  sources, say so. That unattributed residual is a finding, and not a gap to paper over.

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

**Historical boundary.** The running example is the street-view system for address transcription
(Goodfellow et al., 2014d, as cited), a production system from 2014. The numbers of that system are 98%
human-level precision, a 95% coverage target, and +10 coverage points. Those numbers are properties of
that system and of that dataset. Those numbers are not transferable thresholds.

The book cites the 1% update rule of Bottou (2015), and the complex-step trick of Squire and Trapp
(1998). This file records both as the book records them. The tests themselves cover the tiny-dataset
fit, the gradient check, the monitoring of activations and gradients, and the guarantee test. The book
states those tests as general practice, and ties those tests to no 2016 framework.
