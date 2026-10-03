# SOP-DL-05 — Run model selection and hyperparameter search

**Stage:** select · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Own the protocol that selects hyperparameters and design choices. That protocol lets you attribute a
reported number to the method. Without the protocol, the number comes instead from search noise, from an
under-resolved validation set, or from decisions taken from test data.

In scope:

- what counts as a hyperparameter
- the construction and the sizing of validation material
- the comparison rule between two candidate algorithms
- the escalation from manual search to automatic search
- grid search, random search and model-based search, and the case in which each is legitimate

Out of scope: what each individual knob does to the model (see
[`SOP-DL-02`](SOP-DL-02-diagnose-fitting-regime-and-capacity.md) for capacity,
[`SOP-DL-03`](SOP-DL-03-select-regularization.md) for regularizers,
[`SOP-DL-04`](SOP-DL-04-diagnose-optimization-failure.md) for optimization settings) and the choice of
metric being searched over (see
[`SOP-DL-01`](SOP-DL-01-specify-task-output-and-cost.md)).

## 2. Inputs and assumptions

- A single scalar search objective, defined on validation material, and inherited from the task
  specification. You must collapse multiple objectives into one number *before* the search. Do not
  collapse them during the search.
- A training corpus from which you carve the validation material. The book requires that carving. The
  book's rule for test data is "不能用于验证集" — test data may not take part in model selection in any form
  (§5.3, p. 151). So the validation set always comes out of the training data.
- A budget: the number of trials, the wall-clock time, and the memory. The book explicitly frames manual
  search as the minimization of generalization error *subject to* runtime and memory constraints
  (§11.4.1, p. 442).
- A hyperparameter list. Annotate each entry with its type (numeric / discrete / binary / bounded), and
  with the direction in which that hyperparameter moves effective capacity (Table 11.1, p. 445).
- An assumption: repeated runs at the same setting are comparable. If those runs are not comparable,
  measure the seed variance first. Otherwise the search selects noise.

## 3. Procedure

1. **Classify every knob.** The learning algorithm itself should learn some quantities. Do not turn
   such a quantity into a hyperparameter only because the quantity is hard to optimize. More often a
   quantity must be a hyperparameter for the opposite reason. The algorithm *cannot* learn that
   quantity on the training set (§5.3, p. 150). Every capacity-controlling knob has that property.
   Fitting the knob on training data pushes capacity to its maximum, and that overfits. Mark each knob
   as capacity-increasing, capacity-decreasing, or non-monotone. The learning rate is non-monotone.
   Effective capacity is highest when the learning rate is right. Effective capacity degrades when the
   rate is too large. Effective capacity also degrades when the rate is too small (§11.4.1, p. 443,
   Fig. 11.1).

   > **Modern update (2017–2026) — add a fourth classification: *conditional*.** Step 1's three
   > categories describe what a knob does to capacity. The modern anchor adds an orthogonal property,
   > and that property changes what a sampler does. Hyperparameters divide into **discrete** and
   > **conditional** ones. The modern anchor names the search over the architecture itself as a
   > distinct activity.
   >
   > A conditional hyperparameter is one that is **undefined unless its parent takes a particular
   > value**. The number of units in a layer is one example, where the layer exists only under one
   > parent value. A coefficient for a regularizer that the configuration may switch off is another.
   > Mark each knob as conditional or not. For each conditional knob, name the parent and the parent
   > value that makes that knob defined.
   >
   > This note changes the arithmetic of step 7, not the advice of step 7. Both samplers in step 7
   > assume that the space is a product over the knobs. Under a conditional space, that assumption
   > fails in three ways. The O(n^m) count for the grid is wrong, because a combination in an undefined
   > branch does not exist. Such a trial is a wasted trial. Or the sampler coerces the trial into a
   > default, and that default is then an unrecorded decision. The random-search argument still matters.
   > That argument says that the important knob gets a distinct value in nearly every trial. A draw that
   > lands in an undefined branch dilutes that argument. Between random-search runs, the book has you
   > update the marginals. Those marginals cover a space whose effective dimensionality varies from
   > trial to trial.
   >
   > The required step is small. That step is the only step added here. **Declare the conditional
   > structure before sampling.** Then state how the sampler handles an undefined branch. The two
   > options are to skip the trial, or to impute a named default. Report that named default as part of
   > the configuration. Report the number of trials actually evaluated. Do not report the nominal
   > product size in place of that number.
   >
   > No architecture-search method is endorsed here. No such method is added to the search-algorithm
   > menu in step 7. This note records one tension rather than resolving that tension. A scaling-law
   > source in this lineage's list reports a finding about architecture details. The finding is that
   > width versus depth "have minimal effects within a wide range". That finding would make an
   > architecture search low-yield. The finding covers a language model, and this file does not
   > generalize the finding here.
   >
   > *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §1.8. Sources:
   > `UDL` §8.5, fol. 133; `SCALE` (for the recorded tension).*
2. **Freeze the validation material before searching.** The book's stated default puts 80% of the
   training data into parameter learning, and 20% into validation (§5.3, p. 151). Record that
   validation error is *not* an estimate of generalization error. The validation data fits the
   hyperparameters, so validation error systematically underestimates generalization error. The honest
   estimate comes from the test set. Take that estimate only after you finish all hyperparameter
   optimization (§5.3, p. 151).
3. **Check whether the validation material can resolve the differences you care about.** A small
   validation/test set makes the mean error statistically uncertain. That set cannot tell algorithm A
   from algorithm B. The book gives the size at which that problem stops being serious. The size is on
   the order of 10^5 or more samples (§5.3.1, p. 151). Below that size, use k-fold cross-validation
   (Algorithm 5.1, p. 152). Run the cross-validation in four parts:
   - Split the data into k disjoint subsets.
   - Train on the other k−1 subsets.
   - Evaluate on the i-th subset.
   - Average the errors over the k folds.
   Return the per-example error vector, and not only the mean. You need that vector to form a confidence
   interval.
4. **Fix the comparison rule before running anything.** No unbiased estimator exists for the variance
   of the cross-validated average error (Bengio and Grandvalet, 2004, as cited in Algorithm 5.1). The
   book states a working convention (§5.3.1, p. 152). Declare A better than B **only when A's error
   confidence interval lies below B's**. **The two intervals must not intersect.** Overlapping
   intervals mean "not distinguishable", and not "equal".
5. **Search by hand first.** Adjust one knob at a time. Monitor **both** training error and test error
   while you make the change. Each change then reads as a capacity change, and not as an unexplained
   score change (§11.4.1, p. 444). The objective of manual tuning is to match *effective* capacity to
   task complexity. Three things limit effective capacity (§11.4.1, p. 442):
   - the representational capacity of the model
   - the ability of the learning algorithm to minimize the training cost
   - the degree to which the cost function and the training procedure regularize the model

   If there is time for only one knob, tune the learning rate (§11.4.1, p. 443). Work through these
   cases:
   - Training error above target ⇒ only a capacity increase can help. If no regularization is in use,
     and you know that the optimizer works, add layers or hidden units (accepting the compute cost)
     (§11.4.1, p. 444).
   - Test error above target, while training error is low ⇒ the objective is to shrink the train/test
     gap. Do not let training error rise faster than that gap falls. Change the regularization knobs
     (Dropout, weight decay). The book states that the best results come from large models that are
     well regularized (§11.4.1, p. 444).
   - Respect bounded knobs. Weight decay has a floor at zero. If the model *underfits* at λ = 0, you
     cannot reach the overfitting side by moving λ. The knob can only reduce capacity. So
     "regularization does not help" is the wrong conclusion (§11.4.1, p. 443).
6. **Escalate to automatic search only when a good starting point does not exist.** Manual tuning works
   well in two cases. In the first case the practitioner has months or years of experience on similar
   problems and architectures. In the second case the practitioner can borrow known-good settings from a
   similar well-studied task. Where those starting points are unavailable, automatic search finds
   suitable hyperparameters. The exchange is higher computational cost for lower domain-knowledge cost
   (§11.4.2, p. 446). Hyperparameter optimization algorithms have their own secondary hyperparameters,
   namely the search ranges. The book notes that those secondary hyperparameters transfer well across
   problems (§11.4.2, p. 446).
7. **Choose the search algorithm by dimensionality.**
   - **Grid search** is the choice when there are 3 or fewer hyperparameters. Pick a small finite set of
     values for each knob. Take the Cartesian product of those sets. Train each combination, and keep
     the configuration with the lowest validation error (§11.4.3, p. 446). Order the numeric values on a
     **logarithmic scale**. The book's own examples give the learning rates {0.1, 0.01, 10⁻³, 10⁻⁴,
     10⁻⁵}, and the hidden-unit counts {50, 100, 200, 500, 1000, 2000} (§11.4.3, p. 447). Iterate the
     grid. Suppose the best value sits on an edge of the range. That position means the estimate of the
     range was wrong, so shift the range (for example {-1,0,1} → {1,2,3}). If the best value sits
     inside the range, refine the spacing (for example {-1,0,1} → {-0.1,0,0.1}) (§11.4.3, p. 447). The
     cost is O(n^m) for m knobs with n values. Grid search parallelizes with almost no inter-machine
     communication. That parallelism does not rescue the exponential blowup (§11.4.3, p. 448).
   - **Random search** is the choice beyond that dimension, or whenever the space is wide. Define a
     marginal distribution for each hyperparameter, and sample the joint distribution (§11.4.4,
     p. 448). Use a Bernoulli or a categorical distribution for a binary or discrete knob. Use a
     uniform distribution on a log scale for a positive real knob. No discretization is needed, so a
     larger space costs nothing extra. When only a few knobs matter, random search is exponentially more
     efficient than grid search. Grid search wastes trials on equivalent experiments, because the
     important knob repeats values while the other knobs stay fixed. Random search gives the important
     knob a distinct value in nearly every trial. Bergstra and Bengio (2012), as cited, report that
     random search reduces validation error faster per trial (§11.4.4, pp. 448–449, Fig. 11.2). Repeat
     the random-search runs. Update the marginals from the results of the previous run (§11.4.4,
     p. 448).
   - **Model-based optimization** is an option, and not a default. The gradient of the validation error
     with respect to the hyperparameters is usually unavailable (§11.4.5, p. 449). One reason is the
     compute and storage cost. Another reason is that the objective is genuinely non-differentiable in
     discrete knobs. Surrogate approaches model the validation error with Bayesian regression. Those
     approaches trade exploration against exploitation. Exploration targets the high-uncertainty
     regions. Exploitation targets the known-good regions. The book names Spearmint, TPE and SMAC
     (§11.4.5, p. 449). The book's own verdict is that the approach is **not yet mature or reliable**.
     The approach is sometimes expert-like. The approach is sometimes catastrophically wrong on a
     particular problem. Most such algorithms share one defect. An algorithm must complete a full
     training run before the algorithm extracts any information from that run. A human practitioner can
     spot a pathological setting very early (§11.4.5, p. 449). If you use model-based optimization,
     prefer one variant (Swersky et al., 2014, as cited) (§11.4.5, pp. 449–450). That variant maintains
     several partially-run experiments. The variant freezes or unfreezes an experiment as information
     accumulates.
8. **Close the search.** Re-estimate generalization error once, on untouched test material. Take that
   estimate only after you freeze every hyperparameter decision. Record how many trials contacted the
   validation material, and how many trials contacted the test material.
9. **Mark stale numbers.** Some benchmarks reuse the same test set across years and across many
   attempts. That reuse makes the resulting estimate optimistic, and the benchmark goes stale. The
   book's observation is that the field responds by moving to new benchmarks (§5.3, p. 151). The new
   benchmarks are usually larger and harder. State which of your numbers inherit a stale benchmark.

## 4. Important failure modes

- **Selecting on test data.** Any decision taken from test results destroys the meaning of the test set
  as a generalization estimate (§5.3, p. 151). That destruction includes the choice among the final
  candidates by test score.
- **Learning a capacity hyperparameter on the training set.** The model always moves such a
  hyperparameter to maximum capacity, and the model overfits (§5.3, p. 150). That is why capacity knobs
  are hyperparameters.
- **Reporting validation error as generalization error.** Validation error is biased low because
  validation data fits the hyperparameters (§5.3, p. 151).
- **Under-resolved comparison.** A practitioner claims that A beats B on a validation set or a test set
  too small to resolve the difference. A practitioner also treats cross-validated confidence intervals
  as exact, when no unbiased variance estimator exists (§5.3.1, pp. 151–152).
- **Grid search beyond its dimension.** Beyond that dimension, grid search gives an exponential trial
  count. The trials also repeat equivalent experiments (§11.4.3–11.4.4, pp. 448–449).
- **Misreading a bounded knob.** A practitioner concludes that regularization cannot help. The search
  moved weight decay only in the capacity-reducing direction, from a model that already underfits
  (§11.4.1, p. 443).
- **Attributing an optimization failure to capacity.** A wrong learning rate lowers effective capacity
  whatever the size of the model, so "add units" does not fix the optimization failure (§11.4.1, p. 443,
  Fig. 11.1).
- **Paying for full runs in model-based search.** Model-based search spends a complete training run on a
  setting that a human would abandon early (§11.4.5, p. 449).

The next failure mode comes from the modern update. The block at step 1 carries its provenance.

- **Sampling a conditional space as if the space were a product.** A trial lands in an undefined branch.
  That trial is wasted, or the sampler silently coerces the trial into an unrecorded default. So the
  reported trial count, and the effective dimensionality of the search, both misdescribe the space that
  you searched (`delta_map.md` §1.8).

## 5. Outputs and reporting

- Keep the hyperparameter table. The table lists the name, the type, the capacity direction, the search
  distribution or the grid, and the chosen value. The table also states whether you set the knob by hand
  or by search.
- **Modern update (2017–2026):** Mark each knob in that table as **conditional or not**. For each
  conditional knob, name the parent and the parent value under which the knob is defined. Report the
  number of trials **actually evaluated** alongside the nominal product size. Report how the sampler
  handled an undefined branch. The branch is either skipped, or filled with a named default, and that
  named default then forms part of the configuration. See step 1.
- Record the validation protocol. The record names the split sizes or the fold count, and the comparison
  rule that you declared before the search.
- Keep the search log. The log holds the number of trials, the objective value per trial, and which
  split each trial touched.
- Report one final test-set estimate, with the number of test-set contacts and the dates of those
  contacts.
- State which quantities the book does not fix, and which you therefore chose and must defend. The list
  covers the fold count k and the grid resolution. The list also covers the split of the search budget
  between exploration and refinement, and the confidence level used in the comparison rule. The book
  supplies a threshold for the 80/20 default, and for the ~10⁵-sample resolvability point. The book also
  supplies thresholds for the ≤3-knob grid limit, for the log-scale spacing convention, and for the
  non-overlapping-interval comparison rule. No other threshold comes from the book.

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

**Modern-update provenance.** Every row above is a 2016-book locator, and no row was altered. The
modern-update block at step 1 covers conditional hyperparameters, and the matching entries in §4 and §5
cover the same material. That block and those entries are sourced outside the 2016 book. The entries are
recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§1.8.

The source keys are defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1. The keys are `UDL` §8.5,
fol. 133, and `SCALE` for the recorded tension. No architecture-search method was added to the menu of
step 7.

**Historical boundary.** Spearmint, TPE, SMAC and the Swersky et al. (2014) freeze/unfreeze scheme are
the 2016 state of the art. The book reports those methods as the state of the art of 2016. The
judgement that Bayesian hyperparameter optimization is immature and unreliable is a 2016 judgement.
That judgement is recorded here as such, and not as a standing rule.

The 80/20 split, the ~10⁵-sample resolvability point and the ≤3-knob grid limit are book-era rules of
thumb. Those rules are usable defaults, and not derived bounds. The ≤3-knob grid limit counts *nominal*
knobs. Under the conditional-space classification added at step 1, a different count governs the limit.
That count is the effective dimensionality of the defined region, and that count may be smaller.
