# BC-DL-01 — Does the cost still teach the model when it is confidently wrong?

**Tests:** the coupling of the output unit to the loss · **Executed by:**
[`SOP-DL-01`](../../SOP/Deep-Learning-2016/SOP-DL-01-specify-task-output-and-cost.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The book makes a mechanism claim, not a preference claim. A loss that does not use a logarithm to cancel
the exponential inside the output unit loses its gradient. The gradient vanishes exactly in the regime
where the model is confidently wrong.

- Squared error with a softmax output is stated to be a poor loss (Bridle, 1990, as cited)
  (§6.2.2.3, p. 211). The reason is that the loss **cannot train the model to change its output even
  when the model makes a highly confident incorrect prediction**.
- Many objectives other than log-likelihood "do not work" with softmax. An objective that does not cancel
  the exp causes vanishing gradients when the exponent's argument is very negative. Softmax saturates when
  the differences between inputs become extreme. A softmax-based cost then saturates too, unless the cost
  can transform the saturated activation (§6.2.2.3, pp. 210–211).
- MSE and MAE "often perform poorly" with gradient-based optimization (§6.2.1.2, p. 205). A saturating
  output unit combined with these costs produces very small gradients. That is one reason cross-entropy is
  preferred, even when the full p(y|x) is not needed.
- A **thresholded linear unit** used as a probability output defines a valid conditional distribution.
  Gradient descent cannot train such a unit efficiently. Whenever the pre-activation leaves the unit
  interval, the gradient of the output with respect to the parameters is **zero**. A zero gradient leaves
  the learner with no guidance (§6.2.2.2, p. 207).
- The positive counterpart is a sigmoid output trained by maximum likelihood. The loss is then written as
  softplus((1−2y)z), and that form saturates only when the model is already correct. When z has the wrong
  sign, the softplus argument reduces to |z|, and the derivative tends to sign(z). So **the gradient does
  not shrink even for extremely wrong z**, and gradient-based learning corrects a wrong z quickly
  (§6.2.2.2, p. 208).
- A structural claim stands alongside the coupling claims. Cross-entropy costs commonly have **no
  minimum**. For discrete outputs, a model can approach the probabilities 0 and 1. The model cannot reach
  either value. For real-valued outputs, a model that controls the density (e.g. learns a Gaussian
  variance) can drive cross-entropy toward −∞ (§6.2.1.1, p. 204).

## 2. Data and comparison conditions

Every arm uses the same task, data, architecture, initialization, optimizer, learning rate and number of
steps. The arms differ **only** in the (output unit, loss) pairing:

| Arm | Output unit | Loss | Book's prediction |
| --- | --- | --- | --- |
| A | softmax | negative log-likelihood | reference: learns, corrects confidently-wrong examples (§6.2.2.3, p. 210) |
| B | softmax | squared error | fails to change output on highly confident incorrect predictions (§6.2.2.3, p. 211) |
| C | sigmoid | NLL in softplus form, as a function of z | reference: gradient does not shrink when z has the wrong sign (§6.2.2.2, p. 208) |
| D | sigmoid | squared error | saturates with the unit; small gradients whether the answer is right or wrong (§6.2.2.2, p. 208) |
| E | thresholded linear | squared error | exactly zero gradient whenever the pre-activation leaves the unit interval (§6.2.2.2, p. 207) |
| F | linear | MSE, fixed variance | control: MLE ≡ MSE, non-saturating units, optimizes easily (§6.2.2.1, p. 206; §5.5.1, p. 163) |

Required condition, without which the test says nothing: the initial state must contain examples on
which the model is **confidently wrong**. Such an example has large |z| with the wrong sign. The book's
claim concerns that regime. The evaluator must construct that regime, by initializing the model to produce
large-margin errors, or must train partially until the regime occurs. The evaluator must measure the
pre-update state before any remedy is applied.

The second required condition: one arm (F, or an A-variant) must learn a variance or otherwise control the
output density. The run then observes the no-minimum behaviour of §6.2.1.1, instead of assuming that
behaviour.

Numerical-form condition: arm C must implement NLL as a function of the pre-activation z, not of σ(z). σ
can underflow to zero, and log(0) is −∞ (§6.2.2.2, p. 209). A variant that computes the loss from σ(z) is
a legitimate additional arm. The divergence of that variant is a predicted implementation failure, not a
refutation of the coupling claim.

## 3. Baselines

- Arms A, C and F are the reference arms. The quantity of interest is the *relative* behaviour of arms B,
  D and E against those references.
- The benchmark uses no external or literature baseline. The comparison is internal and controlled. That
  is what makes the mechanism claim testable.
- Arm E gives the "no-learning-signal" floor. The gradient of arm E is provably zero outside the unit
  interval. That floor marks the bottom of the scale against which arms B and D are read.

## 4. Metrics

The book names the mechanism and the outcome. The mechanism is gradient size, and the outcome is whether
the output changes. The metrics are those two, plus the cost trajectory:

1. **Report the output-layer gradient magnitude per example**, as a function of confidence |z| and of
   correctness. Report the smallest gradient on confidently-wrong examples, per arm. Report the ratio
   between the confidently-wrong regime and the just-wrong regime. The book predicts that arms B, D and E
   show vanishing (E: exactly zero) gradients as |z| grows with the wrong sign. The book predicts that
   arms A and C do not (§6.2.1.2, p. 205; §6.2.2.2, pp. 207–208; §6.2.2.3, pp. 210–211).
2. **Measure the fraction of confidently-wrong examples whose predicted output changes** after k fixed
   steps. State the change as a move beyond a stated tolerance. This metric is the direct reading of
   "cannot train the model to change its output" (§6.2.2.3, p. 211). Report k, the tolerance, and the
   per-arm fraction.
3. **Plot training error and cost versus steps** for each arm, on a common step budget. The book predicts
   that arms B, D and E plateau while arms A, C and F descend.
4. **Report the boundedness of the cost trajectory** for the density-controlling arm. State whether the
   cost decreases without bound (predicted when a variance parameter is learned, §6.2.1.1, p. 204). Report
   that result separately from the error metrics, so that divergence is not mistaken for learning.
5. **Record the softmax saturation indicator**. The indicator is the spread between the largest and
   second-largest pre-activation on the confidently-wrong examples. The book attributes saturation to
   extreme differences between inputs (§6.2.2.3, p. 211).

The book supplies no numeric threshold for "confidently wrong", no tolerance for "output changed", and no
step budget. The evaluator must fix all three and report the chosen values.

## 5. How to interpret failure

- **B / D / E show vanishing gradients and no output change while A / C correct the same examples** ⇒ that
  reproduces the book's coupling claim. The defect lies in the (unit, loss) pairing. Neither the model
  family nor the data is implicated, and the fix is to change the pairing (§6.2.2, p. 205).
- **A or C also fail to correct confidently-wrong examples** ⇒ the pairing is not the cause. Route the run
  to `SOP-DL-06`. First verify the gradients numerically (step 5). Then verify that the implementation
  computes the loss from z rather than from σ(z) (step 6 of the specification SOP). Then check the
  learning rate. A wrong rate lowers effective capacity regardless of the model (`SOP-DL-02`, §11.4.1, p. 443).
- **E shows nonzero gradients** ⇒ the threshold does not actually saturate the unit, i.e. the arm was
  mis-constructed. The pre-activation never left the unit interval. Rebuild the condition rather than
  reporting a refutation.
- **Cost diverges to −∞ in a density-controlling arm while error also improves** ⇒ the run shows the
  predicted no-minimum behaviour (§6.2.1.1, p. 204). That divergence is not a bug. The remedy the book
  names is regularization, i.e. `SOP-DL-03`.
- **No arm shows the effect** ⇒ the run did not reach the confidently-wrong condition (|z| too small).
  Report the measured |z| distribution, then re-run the arms. A null result obtained outside the
  saturating regime does not test the claim.

## 6. Validity limits and source traceability

Limits the book itself states or implies:

- The MSE ≡ MLE result holds for a Gaussian output with **user-fixed variance**. The result assumes i.i.d.
  samples, and drops the terms that do not depend on θ (§5.5.1, p. 163; §6.2.1.1, p. 203).
- The conditional-statistic results are MSE ⇒ conditional mean and MAE ⇒ conditional median. Both require
  the target function to lie in the class being optimized. The mean result also requires training on
  infinitely many samples from the true data-generating distribution (§6.2.1.2, p. 205). A finite-sample
  violation is not a counterexample.
- The book cites the squared-error/softmax claim to Bridle (1990). The claim concerns the **saturating**
  regime, and a non-saturated regime is outside its scope (§6.2.2.3, pp. 210–211).
- Cross-entropy's lack of a minimum is stated for the models "often encountered in practice", not as a
  universal property (§6.2.1.1, p. 204).
- Everything in this benchmark is a statement about the coupling of output representation to loss. That
  claim licenses no statement about final task accuracy on any particular dataset.

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
