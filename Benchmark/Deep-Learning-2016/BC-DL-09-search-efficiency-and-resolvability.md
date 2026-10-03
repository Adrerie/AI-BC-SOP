# BC-DL-09 — Search sample-efficiency, and whether the validation material can resolve the difference

**Tests:** random versus grid search efficiency, and the statistical resolvability that any such comparison
requires · **Executed by:**
[`SOP-DL-05`](../../SOP/Deep-Learning-2016/SOP-DL-05-run-model-selection-and-hyperparameter-search.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

Two claims are under test, and the second is the precondition for measuring the first.

**Search efficiency.** Random search is exponentially more efficient than grid search (Bergstra and Bengio,
2012, as cited) (§11.4.4, pp. 448–449, Fig. 11.2). The book claims that advantage under one condition:
several hyperparameters do not significantly affect the performance metric. Under that condition, random
search reduces validation error faster *per model run*.

The stated mechanism is the absence of wasted trials. Grid search sometimes produces identical results for
two values of one hyperparameter, because the other hyperparameters stay fixed across those two runs. Random
search instead gives the other hyperparameters different values, so random search performs two independent
explorations (§11.4.4, pp. 448–449).

The cost of grid search is O(n^m) for m hyperparameters with up to n values each. Grid search also
parallelizes with almost no inter-machine communication. That parallelism does not rescue the exponential
blowup (§11.4.3, pp. 447–448). Grid search is recommended only for 3 or fewer hyperparameters (§11.4.3,
p. 446).

**Resolvability.** A small validation set or test set makes the mean error statistically uncertain. A small
set therefore cannot tell algorithm A from algorithm B. That difficulty stops being a serious problem when
the dataset has on the order of 10⁵ or more samples (§5.3.1, p. 151).

Below that size, the book prescribes k-fold cross-validation (Algorithm 5.1). The book attaches a stated
caveat: **no unbiased estimator exists for the variance of the cross-validated average error** (Bengio and
Grandvalet, 2004, as cited).

The book also gives a working convention. A is declared better than B only when the two confidence intervals
do not intersect. Non-intersection means that A's error confidence interval lies below B's confidence interval
(§5.3.1, p. 152; §5.4.3, pp. 158–159).

Validation error itself **underestimates** generalization error, because validation data is used to fit the
hyperparameters (§5.3, p. 151).

The failure mode under test is the composite one. An evaluation reports a search-efficiency win that the
validation material cannot resolve.

## 2. Data and comparison conditions

- **Search space.** The space holds at least four hyperparameters, so that grid search falls outside its
  recommended range. Build the space so that **only some axes matter**. The book claims the exponential
  advantage under that condition (Fig. 11.2 illustrates a case where only one axis matters). The book states
  the marginal distributions. Use a Bernoulli or a categorical distribution for a binary or discrete knob.
  Use a uniform distribution on a log scale for a positive real knob.
- **Budget.** Use an identical number of model runs for both arms. The book states the efficiency claim per
  trial, not per unit of wall-clock. Report wall-clock separately. Grid search parallelizes with almost no
  communication, and random search does the same.
- **Arms.** Use the following arms:
  - Arm (1). Grid search over small finite value sets, spaced logarithmically. Apply the book's iterative
    refinement. If the best value lands on an edge of the grid, shift the grid. If the best value lands in the
    interior, refine the spacing.
  - Arm (2). Random search over the marginals. Repeat random search with marginals updated from the
    previous run.
  - Arm (3). Optionally, add a model-based arm, with the book's stated defect in view. Such algorithms
    extract no information until a full training run completes. A human, by contrast, can judge very early
    that a configuration is pathological (§11.4.5, p. 449).
- **Resolvability sweep.** Repeat the same comparison at several validation-set sizes, spanning the book's
  10⁵ point. Below that point, use k-fold cross-validation. That sweep measures the confidence-interval
  overlap rate as a function of validation-set size.
- **Honest final estimate.** After the search is frozen, take one test-set estimate per selected
  configuration. Record the number of test-set contacts (§5.3, p. 151).

## 3. Baselines

- Grid search is the baseline against which the per-trial progress of random search is measured.
- The book prescribes repetition for both methods. The random-search arm that repeats with updated marginals
  is then the baseline for single-pass random search.
- For resolvability, the reference is the pre-declared comparison rule (non-overlapping confidence intervals).
  Apply that rule identically at every validation-set size.
- A single-configuration run spends the search budget on more training steps instead. That run is the
  "no search" baseline. The baseline answers whether the search was worth the budget at all.

## 4. Metrics

1. **Best validation error found versus number of model runs** — the book's own framing of the efficiency
   claim (§11.4.4, p. 449).
2. **Fraction of wasted trials** is the share of grid-arm runs that repeat an earlier run's objective value.
   The duplication happens because the important axes repeat while the other axes stay fixed (§11.4.4,
   pp. 448–449).
3. **Trials required to reach a stated validation-error target**, per arm.
4. **Wall-clock per arm**, reported separately from trial count, with the parallelism actually used.
5. **Confidence-interval overlap rate** between the two arms' selected configurations. Report that rate as a
   function of validation-set size and of fold count.
6. **Standard error of the mean error** over the evaluation examples. Also report the 95% confidence interval
   built from that standard error (§5.4.3, pp. 158–159).
7. **Gap between validation error and the final test-set estimate**. The gap measures the optimism that the
   book attributes to selecting on validation data (§5.3, p. 151).
8. **Learning-rate sensitivity check**: the book names the learning rate as the most important hyperparameter.
   The effect of the learning rate on effective capacity is non-monotone. Report the search's behaviour on the
   learning-rate axis separately (§11.4.1, p. 443).

The book supplies the grid value sets used as examples. One set covers the learning rates, and holds
{0.1, 0.01, 10⁻³, 10⁻⁴, 10⁻⁵}. The other set covers hidden units, and holds {50, 100, 200, 500, 1000, 2000}.
The book also supplies the log-uniform sampling convention. For example, that convention draws hidden units
from a uniform distribution on the log interval between 50 and 2000. The book gives no trial budget, no fold
count and no target error. Those three values are evaluator choices.

## 5. How to interpret failure

- **Random search does not beat grid** ⇒ check the premise. The book claims the exponential advantage when
  several hyperparameters do not significantly affect the metric. If every axis matters, the mechanism that
  makes grid search wasteful is absent (§11.4.4, pp. 448–449, Fig. 11.2).
- **Grid wins at 3 or fewer axes** ⇒ that result is consistent with the book, which recommends grid search in
  exactly that regime (§11.4.3, p. 446).
- **The efficiency gap disappears under wall-clock accounting** ⇒ report both. The book's claim is per trial.
  The loose parallelism of grid search is a real advantage that the book grants (§11.4.3, p. 448).
- **Confidence intervals overlap at every size tested** ⇒ no claim about which search is better is licensed.
  That resolvability failure is the one the second half of this benchmark exists to catch (§5.3.1, p. 152).
- **Cross-validated comparison reported with an exact variance** ⇒ no exact variance is available. No
  unbiased estimator exists for the variance of the cross-validated average. The intervals are therefore
  conventional approximations (§5.3.1, p. 152).
- **The selected configuration's test error is much worse than its validation error** ⇒ the bias points in the
  expected direction. Validation error underestimates generalization error (§5.3, p. 151). Report the gap. Do
  not treat the validation number as the result.
- **A model-based arm consumes full runs on pathological configurations** ⇒ the book states that defect for
  every such arm. The prescribed mitigation is the variant that maintains several partially-run experiments.
  That variant freezes or unfreezes the experiments (§11.4.5, pp. 449–450).
- **The search keeps improving while the learning rate axis is unswept** ⇒ the search left out the most
  important knob. The book gives an instruction for that case. If you tune only one hyperparameter, tune the
  learning rate (§11.4.1, p. 443).

## 6. Validity limits and source traceability

- The exponential-efficiency claim is conditional on the presence of near-irrelevant axes. The claim is not a
  universal ordering of the two methods (§11.4.4, pp. 448–449).
- The comparison rule is a **convention**. The rule is adopted because no unbiased variance estimator exists
  for the cross-validated average. Overlapping intervals mean "not distinguishable", not "equal" (§5.3.1,
  p. 152).
- The 10⁵-sample resolvability point is a book-era rule of thumb, not a derived bound (§5.3.1, p. 151).
- The verdict on model-based hyperparameter optimization is a 2016 verdict. The book states an open question
  about Bayesian hyperparameter optimization. No one can clearly determine whether the method is a mature tool
  that gives better results, or one that does more with less. The book reports that the method sometimes
  performs like a human expert, and sometimes fails catastrophically. The book's conclusion is that the method
  deserves a trial on a given problem. The method is not yet mature or reliable (§11.4.5, p. 449). Nothing
  here reads as a current judgement on Bayesian optimization tooling.
- Repeated use of the same test set across years and attempts makes estimates optimistic. The same use makes
  benchmarks stale. The book's observation is that the field migrates to new benchmarks, usually larger and
  harder ones (§5.3, p. 151).

| Claim | Locator |
| --- | --- |
| Hyperparameters are not learned; capacity knobs cannot be fit on training data | §5.3, p. 150 |
| Validation carved from training data; 80/20 default; validation underestimates generalization error; benchmark staleness | §5.3, p. 151 |
| Small test sets cannot resolve A vs B; ~10⁵ samples; k-fold cross-validation and Algorithm 5.1; no unbiased variance estimator; non-overlapping-interval rule | §5.3.1, pp. 151–152 |
| Standard error of the mean, 95% confidence interval and the comparison rule | §5.4.3, pp. 158–159 |
| Grid search: ≤3 knobs, log-scale value sets, grid shifting and refinement, O(n^m), loose parallelism | §11.4.3, pp. 446–448, Fig. 11.2 |
| Random search: marginals, no discretization, no wasted trials, faster per-trial validation-error reduction, repeated runs | §11.4.4, pp. 448–449 |
| Model-based search: unavailable gradients, Bayesian surrogates, immaturity verdict, full-run defect, freeze/unfreeze variant | §11.4.5, pp. 449–450 |
| Learning rate as the most important hyperparameter; non-monotone effect on effective capacity | §11.4.1, p. 443 |

**Historical boundary.** Named tooling (Spearmint, TPE, SMAC) and the freeze/unfreeze multi-experiment scheme
are the 2016 state of the art, as the book reports that state. The immaturity verdict is dated accordingly.
The grid value sets, the 80/20 split and the ~10⁵-sample point are book-era conventions. Those conventions
serve as usable defaults, but are not derived values. No post-2016 search algorithm or tooling is introduced.
