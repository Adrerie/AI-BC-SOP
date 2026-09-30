# SOP-DL-01 — Specify the task, output distribution and cost function

**Stage:** define · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Turn a problem statement into an executable specification **before** anything is trained: which task
type is being solved, which performance measure defines success and what its target value is, which
experience the algorithm is allowed to use, which output representation the model emits, and which
cost function that representation determines.

The book makes this the first step of practical methodology: "确定目标——使用什么样的误差度量，并为
此误差度量指定目标值", followed immediately by building an end-to-end pipeline that can estimate that
metric (§11, p. 436). It also makes the point that the specification largely *derives* the rest:
declaring a model for p(y|x) automatically determines the cost function, so a bespoke cost rarely has
to be designed (§6.2.1.1, p. 203), and the whole algorithm is then an assembly of dataset, cost,
optimization procedure and model (§5.10, p. 181).

Out of scope: choosing model size or regularization (`SOP-DL-02`, `SOP-DL-03`), tuning
(`SOP-DL-05`), debugging (`SOP-DL-06`).

## 2. Inputs and assumptions

- A problem statement and the raw data (or a description of what can be collected).
- Knowledge of the deployment decision: what the system does with its output, whether it may abstain,
  and whether error types have different costs.
- A target value for the metric, or the information needed to set one (published benchmark results in
  an academic setting; safety, cost-effectiveness or consumer requirements in an application)
  (§11.1, p. 437).
- Assumption: the examples can be described as feature vectors or as a set of variable-length vectors
  (§5.1.3, p. 137). If neither holds, the representation problem must be solved before this SOP can be
  completed.

## 3. Procedure

1. **Declare the task type** using the book's list (§5.1.1, pp. 131–134): classification;
   classification with missing inputs; regression; transcription; machine translation; structured
   output; anomaly detection; synthesis and sampling; imputation of missing values; denoising;
   density or probability-mass-function estimation. The book states the list is illustrative rather
   than a strict taxonomy (§5.1.1, p. 134), so a deviation must be written down explicitly.
   Two declarations carry consequences:
   - *Classification with missing inputs* cannot be served by one classification function: with n
     input variables there are 2ⁿ possible missing-input subsets, each needing its own function. The
     book's efficient route is to learn the joint distribution over the relevant variables and
     marginalize out the missing ones (§5.1.1, p. 132).
   - *Density estimation* is the task type for which the usual measures are meaningless: accuracy,
     error rate and any 0-1 loss do not apply, and the measure must give every example a continuous
     score, most commonly the average log-probability over examples (§5.1.2, pp. 134–135).
2. **Declare the experience E** (§5.1.3, pp. 135–137): supervised, unsupervised, semi-supervised or
   multi-instance. Record that the boundary is not formal — the chain rule decomposes a joint p(x)
   into n conditional problems, so an "unsupervised" model can be trained as a sequence of supervised
   ones, and p(y|x) can be recovered from a learned joint p(x,y). Declare the dataset representation:
   a design matrix when every example has the same feature dimension, otherwise a set of
   variable-length vectors (the book points to §9.7 and Chapter 10 for the latter).
3. **Choose the performance measure P and its target value** (§11.1, pp. 436–439).
   a. Acknowledge the floor: absolute zero error is unattainable. Even with infinite training data and
      the true distribution recovered, **Bayes error** is the minimum achievable error rate, because
      the inputs may not contain complete information about the output, or the system may be
      intrinsically stochastic (§11.1, p. 437).
   b. Set the target: in academia, from previously published benchmark results; in an application,
      from what makes the product safe, cost-effective or attractive (§11.1, p. 437). Once the target
      error rate is fixed, the design is driven by how to reach it.
   c. Test whether the default measure is adequate. Accuracy (equivalently error rate, the expectation
      of 0-1 loss) is the default for classification, missing-input classification and transcription
      (§5.1.2, p. 134), but the book names three situations where it is not:
      - **Asymmetric costs.** In spam filtering, blocking a legitimate message is worse than letting a
        suspicious one through, so measure a weighted total cost rather than the error rate
        (§11.1, p. 438).
      - **Rare events.** For a condition affecting one person in a million, a detector that always
        reports "no disease" achieves 99.9999% accuracy. Use precision (fraction of reported positives
        that are correct) and recall (fraction of true events detected), the PR curve obtained by
        sweeping the decision threshold on the model's score, the F-score to collapse the curve to one
        number, or the area under the PR curve (§11.1, p. 438).
      - **Abstention.** When the system may decline to answer and a human can take over, the natural
        measure is **coverage** — the fraction of examples on which the system produces a response —
        traded against accuracy. A system can reach 100% accuracy by refusing everything and dropping
        coverage to 0%. The book's example target is human-level 98% transcription accuracy at 95%
        coverage (§11.1, pp. 438–439).
   d. Record that the reported metric is usually **not** the training cost (§11.1, p. 438), and that
      where the ideal measure is infeasible — as it often is for density estimation, because many of
      the best probability models represent distributions only implicitly and cannot evaluate the
      density at a point — a surrogate criterion or a good approximation of the ideal one must be
      designed and labelled as such (§5.1.2, p. 135).
4. **Choose the output representation; the cost follows from it.** The book states the coupling
   directly: the choice of output representation determines the form of the cross-entropy, and most of
   the time the cost is simply the cross-entropy between the data distribution and the model
   distribution (§6.2.2, p. 205; §6.2.1, p. 202).
   | Target | Output unit | Cost | Why, per the book |
   | --- | --- | --- | --- |
   | Conditional mean of a real-valued y | linear (affine) units | maximum likelihood ≡ MSE | linear units do not saturate, so they are easy to optimize with gradient-based and other methods (§6.2.2.1, p. 206) |
   | Conditional median of y | linear units | mean absolute error | the calculus-of-variations result: minimizing MAE yields a function predicting the median, provided that function is in the class being optimized (§6.2.1.2, p. 205) |
   | Binary / two-class y | sigmoid unit on the logit z | negative log-likelihood, written as softplus((1−2y)z) | thresholding a linear unit is a valid distribution but gives zero gradient whenever z leaves the unit interval; the NLL form does not shrink the gradient when z has the wrong sign, so confidently-wrong predictions are corrected quickly (§6.2.2.2, pp. 206–208) |
   | n-way discrete y | softmax on unnormalized log-probabilities | negative log-likelihood | the log cancels the exp; the z_i term never saturates; the second term behaves like max_j z_j so the cost strongly penalizes the most active wrong prediction, and examples already ranked correctly contribute little (§6.2.2.3, pp. 209–210) |
   | Full p(y|x), incl. sequences and structured outputs | declare joint vs independent factorization | a proper log-likelihood | if any downstream decision uses p(y|x) — rejection thresholds in particular — an ad-hoc score is not a likelihood; see step 8 |
   If the target is a covariance or another constrained quantity, note the book's warning that a linear
   output layer cannot easily enforce positive-definiteness, so covariance needs a different
   parameterization (§6.2.2.1, p. 206).
5. **Derive the cost by maximum likelihood wherever possible.** Most modern neural networks are
   trained by maximum likelihood: the cost is the negative log-likelihood, equivalently the
   cross-entropy between the training data and the model distribution. Terms that do not depend on θ
   may be dropped — dropping the Gaussian variance term is exactly how MSE is recovered
   (§6.2.1.1, p. 203; §5.5, p. 162). The stated advantage is that specifying p(y|x) *automatically*
   determines the cost, removing the burden of designing one per model (§6.2.1.1, p. 203).
   Two hazards must be checked at specification time:
   - **The cost may have no minimum.** For discrete outputs, most models cannot represent probability 0
     or 1 exactly and only approach them (logistic regression is the book's example); for real-valued
     outputs, a model that controls the density — for instance one that learns the variance of a
     Gaussian output — can assign extremely high density to the correct training targets and drive the
     cross-entropy toward −∞. The book names regularization (Chapter 7) as the family of remedies
     (§6.2.1.1, p. 204).
   - **Saturation.** A recurring theme is that the cost's gradient must be large enough and
     predictable enough to guide the learner, and that flat (saturating) functions destroy this. The
     log in NLL cancels the exp in saturating output units, which is why NLL avoids the problem;
     MSE and MAE do not, and combined with saturating output units they produce very small gradients —
     one reason cross-entropy is preferred even when the full distribution is not needed
     (§6.2.1.1, p. 203; §6.2.1.2, p. 205).
6. **Record the numerical form of the cost, not only its mathematical form.** The book's concrete
   instruction: implement NLL as a function of the pre-activation z rather than of σ(z), because σ can
   underflow to zero and log(0) is −∞ (§6.2.2.2, p. 209).
7. **Assemble the algorithm and declare every component** (§5.10, pp. 181–182). Nearly every
   deep-learning algorithm is a recipe of dataset + cost function + optimization procedure + model, and
   the components are substitutable largely independently. The cost normally contains at least one term
   performing statistical estimation — most commonly the negative log-likelihood, so that minimizing the
   cost performs maximum likelihood — and may contain additional terms such as regularizers. Once the
   model is nonlinear, closed-form optimization is generally unavailable and an iterative numerical
   procedure must be chosen. If the cost cannot be computed exactly but its gradient can be
   approximated, iterative optimization is still usable. Models whose cost has flat regions (the book's
   examples: decision trees, k-means) are not gradient-friendly and need special optimization.
8. **Decide the factorization of the output explicitly.** The book's worked example is instructive
   (§11.6, pp. 453–454): the first implementation of the street-view transcription system emitted n
   independent softmax units, one per character, each trained as an ordinary classifier, and defined
   p(y|x) ad hoc by multiplying the softmax outputs together. That was sufficient to train, but the
   rejection rule "refuse to transcribe when p(y|x) < t" needs a genuine log-likelihood, so the team
   developed an output layer and cost that compute one; this made the rejection mechanism effective.
   If your specification includes any threshold, ranking or abstention decision, the output must be a
   calibrated joint likelihood, not a product of independently trained parts.
9. **Hand over to the pipeline.** Fix the evaluation plan that matches P (test material kept separate
   from training material, §5.1.2, p. 135), state the numeric target from step 3, and build the
   end-to-end baseline as fast as possible (§11, p. 436). Fitting-regime diagnosis and the baseline
   recipe are `SOP-DL-02`; hyperparameter search over the specification's free choices is
   `SOP-DL-05`.

## 4. Important failure modes

- **Optimizing a measure that is not the deployment objective.** Error rate under asymmetric costs;
  accuracy on rare events; accuracy when abstention is permitted (§11.1, p. 438).
- **0-1 loss on a density-estimation task**, where it is meaningless (§5.1.2, p. 134).
- **Thresholded linear output for a probability**: valid distribution, zero gradient outside the
  interval, no learning signal (§6.2.2.2, p. 207).
- **Squared error with a softmax output**: the book states plainly that squared error is a poor loss for
  softmax units because it cannot train the model to change its output even when it makes a highly
  confident incorrect prediction (Bridle, 1990, as cited) (§6.2.2.3, p. 211).
- **MSE/MAE with saturating output units**: very small gradients (§6.2.1.2, p. 205).
- **Unbounded likelihood**: learned variance driving cross-entropy to −∞; unregularized MLE driving
  softmax outputs toward the empirical training ratios and beyond (§6.2.1.1, p. 204; §6.2.2.3, p. 210).
- **Ad-hoc composite scores used where a likelihood is required**, which silently breaks rejection and
  ranking decisions (§11.6, p. 454).
- **Designing a bespoke cost** where maximum likelihood would have derived it (§6.2.1.1, p. 203).
- **Omitting the target value.** Without a stated target error rate the design has nothing to be driven
  by, and later changes cannot be judged as improvements (§11.1, pp. 437, 439).

## 5. Outputs and reporting

A single specification block, reviewable on one page:

- Task type from the book's list, or the declared deviation; T / P / E in one line each.
- Output representation and the factorization decision (joint vs independent), with the reason.
- Cost function: mathematical form, which constant terms were dropped and why, the numerical form used
  in code (pre-activation vs probability), and whether the cost is bounded below.
- Regularization placeholder: which term will carry it, left to `SOP-DL-03`.
- Optimization procedure family, with the note that a nonlinear model rules out closed-form solutions.
- Metric, target value, and the Bayes-error acknowledgment; abstention/coverage policy if applicable.
- Split plan and the note that validation material comes from training data (`SOP-DL-05`).
- A design-decision log for the choices where the book offers alternatives rather than a rule:
  mean vs median target, joint vs factorized output, weighted cost vs error rate.

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
target) belong to a 2014-era production system and are examples, not targets. The book itself warns
that deep learning advances quickly and that better default algorithms may exist soon after
publication (§11.2, p. 439) — that caveat applies to every default named here. The task taxonomy, the
output-unit/cost couplings and the Bayes-error floor are stated as general results and are not
era-bound.
