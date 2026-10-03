# SOP-DL-01 — Specify the task, output distribution and cost function

**Stage:** define · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Turn a problem statement into an executable specification **before** you train anything. The specification
names:

- the task type
- the performance measure that defines success, and that measure's target value
- the experience that the algorithm may use
- the output representation that the model emits
- the cost function that the output representation determines

The book makes this specification the first step of practical methodology. The book's wording for that step is
"确定目标——使用什么样的误差度量，并为此误差度量指定目标值". That step is followed immediately by an end-to-end
pipeline that can estimate the metric (§11, p. 436).

The book also says that the specification largely *derives* the rest. Declaring a model for p(y|x)
automatically determines the cost function. You therefore rarely need to design a cost of your own
(§6.2.1.1, p. 203). The whole algorithm is then an assembly of dataset, cost, optimization procedure and
model (§5.10, p. 181).

Out of scope:

- `SOP-DL-02` and `SOP-DL-03` cover the choice of model size and of regularization
- `SOP-DL-05` covers the tuning of hyperparameters
- `SOP-DL-06` covers the debugging of the experiment

## 2. Inputs and assumptions

- A problem statement and the raw data. Or a description of the data you can collect.
- Knowledge of the deployment decision. State what the system does with its output, whether the system may
  abstain, and whether the error types have different costs.
- A target value for the metric, or the information needed to set one (published benchmark results in
  an academic setting; safety, cost-effectiveness or consumer requirements in an application)
  (§11.1, p. 437).
- The assumption that you can describe the examples as feature vectors, or as a set of variable-length
  vectors (§5.1.3, p. 137). If neither form holds, solve the representation problem before you finish this
  SOP.

## 3. Procedure

1. **Declare the task type** from the book's list (§5.1.1, pp. 131–134). The list names:

   - classification
   - classification with missing inputs
   - regression
   - transcription
   - machine translation
   - structured output
   - anomaly detection
   - synthesis and sampling
   - imputation of missing values
   - denoising
   - density or probability-mass-function estimation

   The book states that the list is illustrative rather than a strict taxonomy (§5.1.1, p. 134). Write down
   any deviation explicitly. Two declarations carry consequences:

   - *Classification with missing inputs* cannot come from one classification function. With n input
     variables, you have 2ⁿ possible subsets of missing inputs, and each subset needs its own function. The
     book's efficient route is to learn the joint distribution over the relevant variables. Then marginalize
     out the missing variables (§5.1.1, p. 132).
   - *Density estimation* is the task type where the usual measures are meaningless. Accuracy, error rate and
     any 0-1 loss do not apply. The measure must give every example a continuous score. Most often that score
     is the average log-probability over the examples (§5.1.2, pp. 134–135).
2. **Declare the experience E** (§5.1.3, pp. 135–137). Choose supervised, unsupervised, semi-supervised or
   multi-instance.

   Record that the boundary between these regimes is not formal. The chain rule decomposes a joint p(x) into
   n conditional problems. You can therefore train an "unsupervised" model as a sequence of supervised
   models. You can also recover p(y|x) from a learned joint p(x,y).

   Declare the dataset representation too. Use a design matrix when every example has the same feature
   dimension. Otherwise use a set of variable-length vectors. For the latter, the book points to §9.7 and
   Chapter 10.
3. **Choose the performance measure P and its target value** (§11.1, pp. 436–439).
   a. Acknowledge the floor. Absolute zero error is unattainable. **Bayes error** is the minimum achievable
      error rate. The inputs may not contain complete information about the output, or the system may be
      intrinsically stochastic (§11.1, p. 437). The floor stands even with infinite training data, and even
      with the true distribution recovered.
   b. Set the target value (§11.1, p. 437). In academia, use previously published benchmark results. In an
      application, use what makes the product safe, cost-effective or attractive. Once you fix the target
      error rate, the task of reaching that rate drives the design.
   c. Test whether the default measure is adequate. Accuracy is the default measure for classification,
      missing-input classification and transcription (§5.1.2, p. 134). Error rate is the same quantity, and
      both are the expectation of 0-1 loss. The book names three situations where accuracy is not adequate:
      - **Asymmetric costs.** In spam filtering, blocking a legitimate message is worse than letting
        a suspicious message through. Measure a weighted total cost rather than the error rate
        (§11.1, p. 438).
      - **Rare events.** Suppose a condition affects one person in a million. A detector that always reports
        "no disease" then reaches 99.9999% accuracy. Use one of the following measures instead
        (§11.1, p. 438):
        - precision, the fraction of reported positives that are correct
        - recall, the fraction of true events that the detector finds
        - the PR curve, from a sweep of the decision threshold on the model's score
        - the F-score, which collapses the PR curve to one number
        - the area under the PR curve
      - **Abstention.** Suppose the system may decline to answer, and a human can take over. The natural
        measure is then **coverage**, the fraction of examples where the system gives a response. Trade that
        coverage against accuracy. A system can reach 100% accuracy by refusing every example, and such
        behaviour drops coverage to 0%. The book's example target is human-level 98% transcription accuracy
        at 95% coverage (§11.1, pp. 438–439).
   d. Record that the reported metric is usually **not** the training cost (§11.1, p. 438). The ideal
      measure is often infeasible, and density estimation is the usual case. Many of the best probability
      models represent a distribution only implicitly. They cannot evaluate the density at a point. Where
      the ideal measure is infeasible, design a surrogate criterion, or a good approximation of the ideal
      one. Label that choice as such (§5.1.2, p. 135).
4. **Choose the output representation.** The cost follows from that choice. The book states the coupling
   directly: the output representation determines the form of the cross-entropy (§6.2.2, p. 205; §6.2.1,
   p. 202). Most of the time the cost is simply the cross-entropy between the data distribution and the model
   distribution.
   | Target | Output unit | Cost | Why, per the book |
   | --- | --- | --- | --- |
   | Conditional mean of a real-valued y | linear (affine) units | maximum likelihood ≡ MSE | linear units do not saturate, so they are easy to optimize with gradient-based and other methods (§6.2.2.1, p. 206) |
   | Conditional median of y | linear units | mean absolute error | the calculus-of-variations result: minimizing MAE yields a function predicting the median, provided that function is in the class being optimized (§6.2.1.2, p. 205) |
   | Binary / two-class y | sigmoid unit on the logit z | negative log-likelihood, written as softplus((1−2y)z) | thresholding a linear unit is a valid distribution but gives zero gradient whenever z leaves the unit interval; the NLL form does not shrink the gradient when z has the wrong sign, so confidently-wrong predictions are corrected quickly (§6.2.2.2, pp. 206–208) |
   | n-way discrete y | softmax on unnormalized log-probabilities | negative log-likelihood | the log cancels the exp; the z_i term never saturates; the second term behaves like max_j z_j so the cost strongly penalizes the most active wrong prediction, and examples already ranked correctly contribute little (§6.2.2.3, pp. 209–210) |
   | Full p(y|x), incl. sequences and structured outputs | declare joint vs independent factorization | a proper log-likelihood | if any downstream decision uses p(y|x) — rejection thresholds in particular — an ad-hoc score is not a likelihood; see step 8 |
   If the target is a covariance or another constrained quantity, note the book's warning. A linear output
   layer cannot easily enforce positive-definiteness. Covariance therefore needs a different parameterization
   (§6.2.2.1, p. 206).
5. **Derive the cost by maximum likelihood wherever possible.** Most modern neural networks train by maximum
   likelihood. The cost is the negative log-likelihood. That log-likelihood is equivalently the cross-entropy
   between the training data and the model distribution. You may drop terms that do not depend on θ. Dropping
   the Gaussian variance term is exactly how you recover MSE (§6.2.1.1, p. 203; §5.5, p. 162). The stated
   advantage is that
   a declared model for p(y|x) determines the cost *automatically* (§6.2.1.1, p. 203). That removes the burden
   of designing one cost per model. Check two hazards at specification time:

   - **The cost may have no minimum.** For discrete outputs, most models cannot represent probability 0 or 1
     exactly. Those models only approach those values. Logistic regression is the book's example. For
     real-valued outputs, a model that controls the density can cause the same failure. The book's instance is
     a model that learns the variance of a Gaussian output. Such a model can assign extremely high density to
     the correct training targets. It can drive the cross-entropy toward −∞. The book names regularization
     (Chapter 7) as the family of remedies (§6.2.1.1, p. 204).
   - **Saturation.** The book repeats one theme here. The cost's gradient must be large enough, and
     predictable enough, to guide the learner. Flat, saturating functions destroy that property. The log in
     NLL cancels the exp in saturating output units. That cancellation is why NLL avoids the problem. MSE and
     MAE give no such cancellation. With saturating output units, MSE and MAE give very small gradients. One
     reason to prefer cross-entropy is exactly that, even when you do not need the full distribution
     (§6.2.1.1, p. 203; §6.2.1.2, p. 205).
6. **Record the numerical form of the cost, not only its mathematical form.** The book gives the instruction
   concretely. Implement NLL as a function of the pre-activation z, not of σ(z). The value of σ can underflow
   to zero, and log(0) is −∞ (§6.2.2.2, p. 209).
7. **Assemble the algorithm from its parts** (§5.10, pp. 181–182). Declare every component you used. Nearly
   every deep-learning algorithm is a recipe of dataset + cost function + optimization procedure + model. You
   can substitute each component largely on its own. The cost normally contains at least one term that
   performs statistical estimation. Most often that term is the negative log-likelihood, so minimizing the
   cost performs maximum likelihood. The cost may also contain extra terms, such as regularizers. Once the
   model is nonlinear, closed-form optimization is generally unavailable. Choose an iterative numerical
   procedure instead. If you cannot compute the cost exactly but you can approximate its gradient, iterative
   optimization is still usable. Some models have a cost with flat regions. Decision trees and k-means are the
   book's examples. Those models are not gradient-friendly, and they need special optimization.
8. **Decide the factorization of the output explicitly.** The book's worked example is instructive
   (§11.6, pp. 453–454). The first implementation of the street-view transcription system emitted n
   independent softmax units, one per character. Each unit trained as an ordinary classifier. That
   implementation defined p(y|x) ad hoc, by multiplying the softmax outputs together. The choice was
   sufficient for training. The rejection rule "refuse to transcribe when p(y|x) < t" needs a genuine
   log-likelihood. So the team built an output layer and a cost that compute one. That change made the
   rejection mechanism effective. If your specification includes a threshold, a ranking or an abstention
   decision, the output must be a calibrated joint likelihood. Do not use a product of independently trained
   parts.
9. **Hand over to the pipeline.** Fix the evaluation plan that matches P. Keep the test material separate
   from the training material (§5.1.2, p. 135). State the numeric target you set in step 3. Build the
   end-to-end baseline as fast as possible (§11, p. 436). The fitting-regime diagnosis and the baseline recipe
   are `SOP-DL-02`. The hyperparameter search over the specification's free choices is `SOP-DL-05`.

## 4. Important failure modes

- **Optimizing a measure that is not the deployment objective.** The book's cases are error rate under
  asymmetric costs, accuracy on a rare event, and accuracy when the system permits abstention
  (§11.1, p. 438).
- **0-1 loss on a density-estimation task**, where the loss is meaningless (§5.1.2, p. 134).
- **Thresholded linear output for a probability.** The thresholded unit is a valid distribution. Its gradient
  is zero outside the interval, so training gets no learning signal (§6.2.2.2, p. 207).
- **Squared error with a softmax output.** The book states plainly that squared error is a poor loss for
  softmax units. Squared error cannot train the model to change its output, even when the model makes a
  highly confident incorrect prediction (Bridle, 1990, as cited) (§6.2.2.3, p. 211).
- **MSE/MAE with saturating output units.** That pairing gives very small gradients (§6.2.1.2, p. 205).
- **Unbounded likelihood.** A learned variance can drive the cross-entropy toward −∞. Unregularized MLE can
  drive softmax outputs past the empirical training ratios (§6.2.1.1, p. 204; §6.2.2.3, p. 210).
- **Ad-hoc composite scores used where a likelihood is required.** A composite score breaks the rejection and
  ranking decisions silently (§11.6, p. 454).
- **Designing a bespoke cost** where maximum likelihood would derive that cost instead (§6.2.1.1, p. 203).
- **Omitting the target value.** Without a stated target error rate, nothing drives the design. You cannot
  judge later changes as improvements (§11.1, pp. 437, 439).

## 5. Outputs and reporting

A single specification block, reviewable on one page:

- Task type from the book's list, or the declared deviation. Give T, P and E in one line each.
- Output representation and the factorization decision (joint vs independent), with the reason.
- The cost function: its mathematical form, and which constant terms were dropped, with the reason. Also
  report the numerical form that the code uses (pre-activation vs probability), and whether the cost is
  bounded below.
- The regularization placeholder, which is the term that will carry the regularization. Leave that choice to
  `SOP-DL-03`.
- Optimization procedure family, with the note that a nonlinear model rules out closed-form solutions.
- The metric, the target value, and the Bayes-error acknowledgment. If the system can abstain, add the
  coverage policy.
- Split plan and the note that validation material comes from training data (`SOP-DL-05`).
- A design-decision log for the choices where the book offers alternatives rather than a rule. Cover mean vs
  median target, joint vs factorized output, and weighted cost vs error rate.

## 6. Source traceability

| Claim or step | Locator |
| --- | --- |
| Task taxonomy (11 task types); missing-input classification needs the joint distribution; list is illustrative | §5.1.1, pp. 131–134 |
| Performance measure P; accuracy/error rate as expected 0-1 loss; density estimation needs a continuous score (average log-probability); surrogate criteria when the ideal measure is infeasible; test data separate from training data | §5.1.2, pp. 134–135 |
| Experience E; supervised/unsupervised boundary is fuzzy; chain-rule decomposition; design matrix vs variable-length sets | §5.1.3, pp. 135–137 |
| Maximum likelihood and cross-entropy equivalence; KL view; MSE as cross-entropy with a Gaussian model; conditional log-likelihood | §5.5, §5.5.1, pp. 161–163 |
| Algorithm = dataset + cost + optimization + model; substitutable components; NLL as the standard estimation term; nonlinear ⇒ iterative; flat-region costs need special optimization | §5.10, pp. 181–182 |
| Non-convexity ⇒ no convergence guarantee, sensitivity to initialization | §6.2, pp. 201–202 |
| Cost choice; MLE for the conditional distribution; cost may have no minimum; gradient must be large and predictable; saturation | §6.2.1, §6.2.1.1, pp. 202–204 |
| Conditional statistics: MSE ⇒ mean, MAE ⇒ median; both perform poorly with saturating output units | §6.2.1.2, pp. 204–205 |
| Output units couple to cost; linear units for Gaussian; sigmoid for Bernoulli incl. softplus form and the z-not-σ(z) implementation rule; softmax for Multinoulli incl. the squared-error warning | §6.2.2, §6.2.2.1–6.2.2.3, pp. 205–211 |
| Practical methodology step 1 (fix the metric and its target); Bayes error floor; asymmetric costs; precision/recall/PR/F-score; coverage and abstention; metric ≠ training cost | §11.1, pp. 436–439 |
| Worked example: independent softmax units, ad-hoc product score, replacement by a proper log-likelihood for rejection | §11.6, pp. 453–454 |

**Historical boundary.** The street-view transcription numbers (98% human-level accuracy, 95% coverage
target) belong to a 2014-era production system. Those numbers are examples, not targets. The book itself
warns that deep learning advances quickly. Better default algorithms may exist soon after publication
(§11.2, p. 439), and that caveat applies to every default named here. The task taxonomy, the
output-unit/cost couplings and the Bayes-error floor are stated as general results and are not era-bound.
