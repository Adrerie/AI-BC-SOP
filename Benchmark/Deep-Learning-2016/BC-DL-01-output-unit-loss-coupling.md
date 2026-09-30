# BC-DL-01 — Does the cost still teach the model when it is confidently wrong?

**Tests:** the output-unit ↔ loss coupling · **Executed by:**
[`SOP-DL-01`](../../SOP/Deep-Learning-2016/SOP-DL-01-specify-task-output-and-cost.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The book makes a mechanism claim, not a preference claim: a loss that does not use a logarithm to
cancel the exponential inside the output unit loses its gradient exactly in the regime where the model
is confidently wrong.

- Squared error with a softmax output is stated to be a poor loss because it **cannot train the model to
  change its output even when the model makes a highly confident incorrect prediction** (Bridle, 1990,
  as cited) (§6.2.2.3, p. 211).
- Many objectives other than log-likelihood "do not work" with softmax: those that do not cancel the exp
  cause vanishing gradients when the exponent's argument is very negative; when softmax saturates
  (differences between inputs become extreme), softmax-based costs saturate too unless they can
  transform the saturated activation (§6.2.2.3, pp. 210–211).
- MSE and MAE "often perform poorly" with gradient-based optimization because saturating output units
  combined with these costs produce very small gradients — one reason cross-entropy is preferred even
  when the full p(y|x) is not needed (§6.2.1.2, p. 205).
- A **thresholded linear unit** used as a probability output defines a valid conditional distribution but
  cannot be trained efficiently by gradient descent: whenever the pre-activation leaves the unit
  interval, the gradient of the output with respect to the parameters is **zero**, and a zero gradient
  leaves the learner with no guidance (§6.2.2.2, p. 207).
- The positive counterpart: with a sigmoid output and maximum likelihood, the loss written as
  softplus((1−2y)z) saturates only when the model is already correct; when z has the wrong sign the
  softplus argument reduces to |z| and its derivative tends to sign(z), so **the gradient does not
  shrink even for extremely wrong z**, and gradient-based learning corrects wrong z quickly
  (§6.2.2.2, p. 208).
- Structural claim to be observed alongside: cross-entropy costs commonly have **no minimum** — for
  discrete outputs models can approach but not reach probabilities 0 and 1, and for real-valued outputs
  a model that controls the density (e.g. learns a Gaussian variance) can drive cross-entropy toward
  −∞ (§6.2.1.1, p. 204).

## 2. Data and comparison conditions

Same task, same data, same architecture, same initialization, same optimizer and learning rate, same
number of steps. The arms differ **only** in the (output unit, loss) pairing:

| Arm | Output unit | Loss | Book's prediction |
| --- | --- | --- | --- |
| A | softmax | negative log-likelihood | reference: learns, corrects confidently-wrong examples (§6.2.2.3, p. 210) |
| B | softmax | squared error | fails to change output on highly confident incorrect predictions (§6.2.2.3, p. 211) |
| C | sigmoid | NLL in softplus form, as a function of z | reference: gradient does not shrink when z has the wrong sign (§6.2.2.2, p. 208) |
| D | sigmoid | squared error | saturates with the unit; small gradients whether the answer is right or wrong (§6.2.2.2, p. 208) |
| E | thresholded linear | squared error | exactly zero gradient whenever the pre-activation leaves the unit interval (§6.2.2.2, p. 207) |
| F | linear | MSE, fixed variance | control: MLE ≡ MSE, non-saturating units, optimizes easily (§6.2.2.1, p. 206; §5.5.1, p. 163) |

Required condition, without which the test says nothing: the initial state must contain examples on
which the model is **confidently wrong** — large |z| with the wrong sign. The book's claim is about that
regime, so the evaluator must either construct it (initialize to produce large-margin errors) or train
partially until it occurs, and must measure the pre-update state before any remedy is applied.

Second required condition: one arm (F, or an A-variant) must learn a variance or otherwise control the
output density, so that the no-minimum behaviour of §6.2.1.1 can be observed rather than assumed.

Numerical-form condition: arm C must implement NLL as a function of the pre-activation z, not of σ(z),
because σ can underflow to zero and log(0) is −∞ (§6.2.2.2, p. 209). Running a variant that computes the
loss from σ(z) is a legitimate additional arm, and its divergence is a predicted implementation failure,
not a refutation of the coupling claim.

## 3. Baselines

- Arm A / C / F are the reference arms; the quantity of interest is the *relative* behaviour of B, D and
  E against them.
- No external or literature baseline is used: the comparison is internal and controlled, which is what
  makes the mechanism claim testable.
- A "no-learning-signal" floor is obtained from arm E, whose gradient is provably zero outside the unit
  interval; it marks the bottom of the scale against which B and D are read.

## 4. Metrics

The book names the mechanism (gradient size) and the outcome (whether the output changes), so the
metrics are those two, plus the cost trajectory:

1. **Output-layer gradient magnitude per example**, as a function of confidence |z| and of correctness.
   Report the smallest gradient observed on confidently-wrong examples per arm, and the ratio between
   the confidently-wrong and the just-wrong regime. Arms B, D and E are predicted to show vanishing (E:
   exactly zero) gradients as |z| grows with the wrong sign; arms A and C are predicted not to
   (§6.2.1.2, p. 205; §6.2.2.2, pp. 207–208; §6.2.2.3, pp. 210–211).
2. **Fraction of confidently-wrong examples whose predicted output changes** by more than a stated
   tolerance after k fixed steps. This is the direct reading of "cannot train the model to change its
   output" (§6.2.2.3, p. 211). Report k, the tolerance, and the per-arm fraction.
3. **Training error and cost versus steps** per arm, on a common step budget. Arms B, D and E are
   predicted to plateau while A, C and F descend.
4. **Cost-trajectory boundedness** for the density-controlling arm: whether the cost decreases without
   bound (predicted when a variance parameter is learned, §6.2.1.1, p. 204), reported separately from
   the error metrics so that divergence is not mistaken for learning.
5. **Softmax saturation indicator**: the spread between the largest and second-largest pre-activation on
   the confidently-wrong examples, since the book attributes saturation to extreme differences between
   inputs (§6.2.2.3, p. 211).

The book supplies no numeric threshold for "confidently wrong", no tolerance for "output changed", and
no step budget; the evaluator must fix all three and report them.

## 5. How to interpret failure

- **B / D / E show vanishing gradients and no output change while A / C correct the same examples** ⇒
  the book's coupling claim is reproduced. The defect is in the (unit, loss) pairing; neither the model
  family nor the data is implicated, and the fix is to change the pairing (§6.2.2, p. 205).
- **A or C also fail to correct confidently-wrong examples** ⇒ the pairing is not the cause. Route to
  `SOP-DL-06`: verify gradients numerically (step 5), verify the loss is computed from z rather than
  σ(z) (step 6 of the specification SOP), then check the learning rate — a wrong rate lowers effective
  capacity regardless of the model (`SOP-DL-02`, §11.4.1, p. 443).
- **E shows nonzero gradients** ⇒ the threshold is not actually saturating the unit, i.e. the arm was
  mis-constructed; the pre-activation never left the unit interval. Rebuild the condition rather than
  reporting a refutation.
- **Cost diverges to −∞ in a density-controlling arm while error also improves** ⇒ the predicted
  no-minimum behaviour (§6.2.1.1, p. 204). Not a bug; the remedy the book names is regularization, i.e.
  `SOP-DL-03`.
- **No arm shows the effect** ⇒ the confidently-wrong condition was not achieved (|z| too small). Report
  the measured |z| distribution and re-run; a null result obtained outside the saturating regime does not
  test the claim.

## 6. Validity limits and source traceability

Limits the book itself states or implies:

- The MSE ≡ MLE equivalence holds for a Gaussian output with **user-fixed variance**, after dropping
  terms that do not depend on θ, under i.i.d. samples (§5.5.1, p. 163; §6.2.1.1, p. 203).
- The conditional-statistic results (MSE ⇒ conditional mean, MAE ⇒ conditional median) require the
  target function to lie in the class being optimized and, for the mean result, training on infinitely
  many samples from the true data-generating distribution (§6.2.1.2, p. 205). A finite-sample violation
  is not a counterexample.
- The squared-error/softmax claim is cited to Bridle (1990) and concerns the **saturating** regime; a
  non-saturated regime is outside its scope (§6.2.2.3, pp. 210–211).
- Cross-entropy's lack of a minimum is stated for the models "often encountered in practice", not as a
  universal property (§6.2.1.1, p. 204).
- Everything here is a statement about the coupling of output representation to loss. It licenses no
  claim about final task accuracy on any particular dataset.

| Claim | Locator |
| --- | --- |
| Cost follows from the output representation; cross-entropy is the usual choice | §6.2.1, p. 202; §6.2.2, p. 205 |
| MLE derives the cost automatically; terms independent of θ may be dropped; Gaussian ⇒ MSE | §6.2.1.1, p. 203 |
| Cross-entropy often has no minimum; density control drives it to −∞; regularization is the remedy | §6.2.1.1, p. 204 |
| MSE ⇒ mean, MAE ⇒ median; both poor with saturating units; small gradients | §6.2.1.2, pp. 204–205 |
| Linear units non-saturating and easy to optimize; covariance needs another parameterization | §6.2.2.1, p. 206 |
| Thresholded linear output has zero gradient outside the interval; sigmoid + NLL as softplus; gradient does not shrink for wrong-sign z; implement NLL in z, not σ(z) | §6.2.2.2, pp. 206–209 |
| Softmax + NLL: log cancels exp, z_i term never saturates, second term ≈ max_j z_j, strongest penalty on the most active wrong prediction; unregularized MLE drives outputs to empirical ratios; squared error is a poor loss for softmax (Bridle, 1990); saturation from extreme input differences | §6.2.2.3, pp. 209–211 |
| Conditional maximum likelihood; linear regression as MLE with fixed variance | §5.5, §5.5.1, pp. 161–163 |
| Ad-hoc product of softmax outputs replaced by a proper log-likelihood once a rejection threshold was needed | §11.6, p. 454 |

**Historical boundary.** The output-unit menu (linear, sigmoid, softmax) is the book's 2016 menu and is
used here as the experimental object, not as a current recommendation. Bridle (1990) is a citation made
by the book. No arm depends on post-2016 architectures or losses, and none is added here.
