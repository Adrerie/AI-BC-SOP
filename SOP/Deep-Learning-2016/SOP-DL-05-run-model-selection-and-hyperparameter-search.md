# SOP-DL-05 — Run model selection and hyperparameter search

**Stage:** select · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Own the protocol by which hyperparameters and design choices are selected, so that a reported number
can be attributed to the method rather than to search noise, to an under-resolved validation set, or
to decisions taken from test data.

In scope: what counts as a hyperparameter; construction and sizing of validation material; the
comparison rule between two candidate algorithms; the manual → automatic escalation; grid, random
and model-based search and when each is legitimate.

Out of scope: what each individual knob does to the model (see
[`SOP-DL-02`](SOP-DL-02-diagnose-fitting-regime-and-capacity.md) for capacity,
[`SOP-DL-03`](SOP-DL-03-select-regularization.md) for regularizers,
[`SOP-DL-04`](SOP-DL-04-diagnose-optimization-failure.md) for optimization settings) and the choice of
metric being searched over (see
[`SOP-DL-01`](SOP-DL-01-specify-task-output-and-cost.md)).

## 2. Inputs and assumptions

- A single scalar search objective defined on validation material, inherited from the task
  specification. Multiple objectives must be collapsed into one number *before* the search, not
  during it.
- A training corpus from which validation material is carved. The book requires this: test samples
  "不能用于验证集" — test data may not participate in model selection in any form, so the validation
  set is always built out of the training data (§5.3, p. 151).
- A budget: number of trials, wall-clock, memory. Manual search is explicitly framed as minimizing
  generalization error *subject to* runtime and memory constraints (§11.4.1, p. 442).
- A hyperparameter list annotated with type (numeric / discrete / binary / bounded) and with the
  direction in which it moves effective capacity (Table 11.1, p. 445).
- Assumption: repeated runs at the same setting are comparable. If they are not, seed variance must
  be measured first, otherwise the search will select noise.

## 3. Procedure

1. **Classify every knob.** A quantity that the learning algorithm itself should learn must not be
   turned into a hyperparameter merely because it is hard to optimize; more often it must be a
   hyperparameter because it *cannot* be learned on the training set — this is true of every
   capacity-controlling knob, since fitting it on training data drives it to maximum capacity and
   overfits (§5.3, p. 150). Mark each knob as capacity-increasing, capacity-decreasing, or
   non-monotone. The learning rate is non-monotone: effective capacity is highest when the learning
   rate is right, and degrades when it is either too large or too small (§11.4.1, p. 443, Fig. 11.1).
2. **Freeze the validation material before searching.** The book's stated default is 80% of the
   training data for parameter learning and 20% for validation (§5.3, p. 151). Record that validation
   error is *not* an estimate of generalization error: because validation data is used to fit
   hyperparameters, it systematically underestimates generalization error. The honest estimate comes
   from the test set only after all hyperparameter optimization is finished (§5.3, p. 151).
3. **Check whether the validation material can resolve the differences you care about.** A small
   validation/test set makes the mean error statistically uncertain, so it cannot tell algorithm A
   from algorithm B; the book states this stops being a serious problem when the dataset has on the
   order of 10^5 or more samples (§5.3.1, p. 151). Below that, use k-fold cross-validation
   (Algorithm 5.1, p. 152): split into k disjoint subsets, train on the other k−1, evaluate on the
   i-th, and average over the k folds. Return the per-example error vector, not just the mean, so a
   confidence interval can be formed.
4. **Fix the comparison rule before running anything.** There is no unbiased estimator of the
   variance of the cross-validated average error (Bengio and Grandvalet, 2004, as cited in Algorithm
   5.1). The book's working convention: declare A better than B **only when A's error confidence
   interval lies below B's and the two intervals do not intersect** (§5.3.1, p. 152). Overlapping
   intervals mean "not distinguishable", not "equal".
5. **Search by hand first.** Adjust one knob at a time while monitoring **both** training error and
   test error, so that each change can be read as a capacity change rather than as an unexplained
   score change (§11.4.1, p. 444). The objective of manual tuning is to match *effective* capacity to
   task complexity; effective capacity is limited by three things — representational capacity, the
   learning algorithm's ability to minimize the training cost, and the degree to which the cost
   function and training procedure regularize the model (§11.4.1, p. 442). If there is time for only
   one knob, tune the learning rate (§11.4.1, p. 443).
   - Training error above target ⇒ only a capacity increase can help; add layers or hidden units
     (accepting the compute cost) if no regularization is in use and the optimizer is known to work
     (§11.4.1, p. 444).
   - Test error above target while training error is low ⇒ the objective is to shrink the
     train/test gap without letting training error rise faster than the gap falls; change
     regularization knobs (Dropout, weight decay). The book's stated expectation is that the best
     results come from large models that are well regularized (§11.4.1, p. 444).
   - Respect bounded knobs: weight decay has a floor at zero, so if the model *underfits* at
     λ = 0 you cannot reach the overfitting side by moving λ, and "regularization does not help" is
     the wrong conclusion — the knob can only reduce capacity (§11.4.1, p. 443).
6. **Escalate to automatic search only when a good starting point does not exist.** Manual tuning
   works well when the practitioner has months or years of experience on similar problems and
   architectures, or can borrow known-good settings from a similar well-studied task; where those
   starting points are unavailable, automatic search finds suitable hyperparameters at higher
   computational cost and lower domain-knowledge cost (§11.4.2, p. 446). Hyperparameter optimization
   algorithms have their own secondary hyperparameters (the search ranges), but the book notes these
   transfer well across problems (§11.4.2, p. 446).
7. **Choose the search algorithm by dimensionality.**
   - **Grid search** when there are 3 or fewer hyperparameters: pick a small finite value set per
     knob, take the Cartesian product, train each combination, keep the configuration with the lowest
     validation error (§11.4.3, p. 446). Space ordered numeric values on a **logarithmic scale** —
     the book's own examples are learning rates {0.1, 0.01, 10⁻³, 10⁻⁴, 10⁻⁵} and hidden-unit counts
     {50, 100, 200, 500, 1000, 2000} (§11.4.3, p. 447). Iterate the grid: if the best value sits on an
     edge, the range was mis-estimated and should be shifted (e.g. {-1,0,1} → {1,2,3}); if it sits
     inside, refine the spacing (e.g. {-1,0,1} → {-0.1,0,0.1}) (§11.4.3, p. 447). Cost is O(n^m) for m
     knobs with n values; it parallelizes with almost no inter-machine communication, which does not
     rescue the exponential blowup (§11.4.3, p. 448).
   - **Random search** beyond that, or whenever the space is wide: define a marginal distribution per
     hyperparameter — Bernoulli or categorical for binary/discrete knobs, uniform on a log scale for
     positive real knobs — and sample the joint (§11.4.4, p. 448). No discretization is needed, so a
     larger space costs nothing extra. When only a few knobs matter, random search is exponentially
     more efficient than grid search, because grid search wastes trials on equivalent experiments
     (the important knob repeats values while the others are held fixed) whereas random search gives
     the important knob a distinct value in nearly every trial; Bergstra and Bengio (2012), as cited,
     found random search reduces validation error faster per trial (§11.4.4, pp. 448–449, Fig. 11.2).
     Repeat random search runs, updating the marginals from the previous run's results (§11.4.4,
     p. 448).
   - **Model-based optimization** is an option, not a default. The gradient of validation error with
     respect to hyperparameters is usually unavailable — because of compute and storage cost, or
     because the objective is genuinely non-differentiable in discrete knobs (§11.4.5, p. 449).
     Surrogate approaches model validation error with Bayesian regression and trade exploration
     (high-uncertainty regions) against exploitation (known-good regions); the book names Spearmint,
     TPE and SMAC (§11.4.5, p. 449). Its own verdict is that the approach is **not yet mature or
     reliable** — sometimes expert-like, sometimes catastrophically wrong on particular problems —
     and that most such algorithms share a defect: they must complete a full training run before they
     can extract any information, whereas a human practitioner can spot a pathological setting very
     early (§11.4.5, p. 449). If used, prefer the variant that maintains several partially-run
     experiments and freezes or unfreezes them as information accumulates (Swersky et al., 2014, as
     cited) (§11.4.5, pp. 449–450).
8. **Close the search.** Re-estimate generalization error once, on untouched test material, after all
   hyperparameter decisions are frozen. Record how many trials contacted the validation material and
   how many contacted the test material.
9. **Mark stale numbers.** When the same test set has been reused across years and across many
   attempts, the resulting estimate becomes optimistic and the benchmark goes stale; the book's
   observation is that the field responds by moving to new, usually larger and harder benchmarks
   (§5.3, p. 151). State which of your numbers inherit a stale benchmark.

## 4. Important failure modes

- **Selecting on test data.** Any decision taken from test results destroys the test set's meaning as
  a generalization estimate (§5.3, p. 151). This includes choosing among final candidates by test
  score.
- **Learning a capacity hyperparameter on the training set.** It will always move to maximum
  capacity and overfit; this is why capacity knobs are hyperparameters (§5.3, p. 150).
- **Reporting validation error as generalization error.** Validation error is biased low because
  validation data fits the hyperparameters (§5.3, p. 151).
- **Under-resolved comparison.** Claiming A beats B on a validation or test set too small to resolve
  the difference; or treating cross-validated confidence intervals as exact when no unbiased variance
  estimator exists (§5.3.1, pp. 151–152).
- **Grid search beyond its dimension.** Exponential trial count, plus repeated equivalent
  experiments (§11.4.3–11.4.4, pp. 448–449).
- **Misreading a bounded knob.** Concluding that regularization cannot help because weight decay was
  only ever moved in the capacity-reducing direction from an already-underfitting model (§11.4.1,
  p. 443).
- **Attributing an optimization failure to capacity.** A wrong learning rate lowers effective
  capacity whatever the model size, so "add units" does not fix it (§11.4.1, p. 443, Fig. 11.1).
- **Paying for full runs in model-based search.** Complete training runs are consumed on settings a
  human would have abandoned early (§11.4.5, p. 449).

## 5. Outputs and reporting

- Hyperparameter table: name, type, capacity direction, search distribution or grid, chosen value,
  and whether it was set by hand or by search.
- Validation protocol: split sizes or fold count, and the pre-declared comparison rule.
- Search log: number of trials, objective per trial, and which split each trial touched.
- One final test-set estimate, with the number and dates of test-set contacts.
- An explicit statement of which quantities the book does not fix and which you therefore chose and
  must defend: fold count k, grid resolution, search-budget split between exploration and refinement,
  and the confidence level used in the comparison rule. The book supplies thresholds only for the
  80/20 default, the ~10⁵-sample resolvability point, the ≤3-knob grid limit, the log-scale spacing
  convention and the non-overlapping-interval comparison rule.

## 6. Source traceability

| Claim or step | Locator |
| --- | --- |
| Hyperparameters are not learned; capacity knobs cannot be fit on training data | §5.3, p. 150 |
| Validation set carved from training data; 80/20 default; validation underestimates generalization error; benchmark staleness | §5.3, p. 151 |
| Small test sets cannot resolve A vs B; ~10⁵ samples; k-fold cross-validation and Algorithm 5.1; no unbiased variance estimator; non-overlapping confidence-interval rule | §5.3.1, pp. 151–152 |
| Manual tuning objective; three limits on effective capacity; monitor train and test error; capacity vs gap branches; bounded knobs; learning rate as the single most important knob | §11.4.1, pp. 442–445, Table 11.1, Fig. 11.1 |
| When automatic search is justified; secondary hyperparameters transfer | §11.4.2, p. 446 |
| Grid search: ≤3 knobs, log-scale value sets, grid shifting and refinement, O(n^m), trivial parallelism | §11.4.3, pp. 446–448, Fig. 11.2 |
| Random search: marginals, no discretization, no wasted trials, faster validation-error reduction per trial, repeated runs | §11.4.4, pp. 448–449 |
| Model-based search: unavailable gradients, Bayesian surrogates, Spearmint/TPE/SMAC, immaturity verdict, full-run defect, freeze/unfreeze variant | §11.4.5, pp. 449–450 |

**Historical boundary.** Spearmint, TPE, SMAC and the Swersky et al. (2014) freeze/unfreeze scheme are
the 2016 state of the art as the book reports it; the judgement that Bayesian hyperparameter
optimization is immature and unreliable is a 2016 judgement and is recorded here as such, not as a
standing rule. The 80/20 split, the ~10⁵-sample resolvability point and the ≤3-knob grid limit are
book-era rules of thumb: usable defaults, not derived bounds.
