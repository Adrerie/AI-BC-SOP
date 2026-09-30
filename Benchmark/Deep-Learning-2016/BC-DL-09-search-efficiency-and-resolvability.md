# BC-DL-09 — Search sample-efficiency, and whether the validation material can resolve the difference

**Tests:** random versus grid search efficiency, and the statistical resolvability that any such comparison
requires · **Executed by:**
[`SOP-DL-05`](../../SOP/Deep-Learning-2016/SOP-DL-05-run-model-selection-and-hyperparameter-search.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

Two claims, the second being the precondition for measuring the first.

**Search efficiency.** Random search is exponentially more efficient than grid search when several
hyperparameters do not significantly affect the performance metric, and it reduces validation error faster
*per model run* (Bergstra and Bengio, 2012, as cited) (§11.4.4, pp. 448–449, Fig. 11.2). The stated mechanism
is the absence of wasted trials: grid search sometimes produces identical results for two values of one
hyperparameter because the other hyperparameters are held fixed across those two runs, whereas random search
gives the other hyperparameters different values and so performs two independent explorations (§11.4.4,
pp. 448–449). Grid search's cost is O(n^m) for m hyperparameters with up to n values each; it parallelizes with
almost no inter-machine communication, which does not rescue the exponential blowup (§11.4.3, pp. 447–448).
Grid search is recommended only for 3 or fewer hyperparameters (§11.4.3, p. 446).

**Resolvability.** A small validation or test set makes the mean error statistically uncertain, so it cannot
tell algorithm A from algorithm B; this stops being a serious problem when the dataset has on the order of
10⁵ or more samples (§5.3.1, p. 151). Below that, k-fold cross-validation is prescribed (Algorithm 5.1), with
the stated caveat that **no unbiased estimator exists for the variance of the cross-validated average error**
(Bengio and Grandvalet, 2004, as cited), and the working convention that A is declared better than B only when
A's error confidence interval lies below B's and the two do not intersect (§5.3.1, p. 152; §5.4.3,
pp. 158–159). Validation error itself **underestimates** generalization error, because validation data is used
to fit the hyperparameters (§5.3, p. 151).

The failure mode under test is the composite one: reporting a search-efficiency win that the validation
material was never able to resolve.

## 2. Data and comparison conditions

- **Search space.** At least four hyperparameters, so that grid search is outside its recommended range, and
  constructed so that **only some axes matter** — this is the condition under which the exponential advantage
  is claimed (Fig. 11.2 illustrates a case where only one axis matters). Marginal distributions per the book:
  Bernoulli or categorical for binary and discrete knobs, uniform on a log scale for positive real knobs.
- **Budget.** Identical number of model runs for both arms — the book's efficiency claim is stated per trial,
  not per unit of wall-clock. Report wall-clock separately, since grid parallelizes with almost no
  communication and random search does too.
- **Arms.** (1) grid search over small finite value sets spaced logarithmically, with the book's iterative
  refinement (if the best value lands on an edge, shift the grid; if interior, refine the spacing);
  (2) random search over the marginals, repeated with marginals updated from the previous run;
  (3) optionally a model-based arm, with the book's stated defect in view: such algorithms must complete a
  full training run before extracting any information, whereas a human can judge very early that a
  configuration is pathological (§11.4.5, p. 449).
- **Resolvability sweep.** The same comparison repeated at several validation-set sizes spanning the book's
  10⁵ point, and with k-fold cross-validation below it, so that the confidence-interval overlap rate is
  measured as a function of size.
- **Honest final estimate.** After the search is frozen, one test-set estimate per selected configuration,
  with the number of test-set contacts recorded (§5.3, p. 151).

## 3. Baselines

- Grid search is the baseline against which random search's per-trial progress is measured.
- The random-search arm that repeats with updated marginals is the baseline against which single-pass random
  search is measured, since the book prescribes repetition for both methods.
- For resolvability, the reference is the pre-declared comparison rule (non-overlapping confidence intervals),
  applied identically at every validation-set size.
- A single-configuration run with the search budget spent on more training steps is the "no search" baseline,
  which answers whether searching was worth the budget at all.

## 4. Metrics

1. **Best validation error found versus number of model runs** — the book's own framing of the efficiency
   claim (§11.4.4, p. 449).
2. **Fraction of wasted trials**: in the grid arm, the proportion of runs whose objective value duplicates an
   earlier run's because the important axes repeated while the others were held fixed (§11.4.4, pp. 448–449).
3. **Trials required to reach a stated validation-error target**, per arm.
4. **Wall-clock per arm**, reported separately from trial count, with the parallelism actually used.
5. **Confidence-interval overlap rate** between the two arms' selected configurations, as a function of
   validation-set size and fold count.
6. **Standard error of the mean error** over evaluation examples, and the 95% confidence interval built from
   it (§5.4.3, pp. 158–159).
7. **Gap between validation error and the final test-set estimate**, which measures the optimism the book
   attributes to selecting on validation data (§5.3, p. 151).
8. **Learning-rate sensitivity check**: since the learning rate is named as the most important
   hyperparameter, and one whose effective-capacity effect is non-monotone, report the search's behaviour on
   that axis separately (§11.4.1, p. 443).

The book supplies the grid value sets it uses as examples (learning rates {0.1, 0.01, 10⁻³, 10⁻⁴, 10⁻⁵};
hidden units {50, 100, 200, 500, 1000, 2000}) and the log-uniform sampling convention (for example hidden units
from a uniform draw on the log interval between 50 and 2000), but no trial budget, no fold count and no target
error; those are evaluator choices.

## 5. How to interpret failure

- **Random search does not beat grid** ⇒ check the premise: the exponential advantage is claimed when several
  hyperparameters do not significantly affect the metric. If every axis matters, the mechanism that makes grid
  wasteful is absent (§11.4.4, pp. 448–449, Fig. 11.2).
- **Grid wins at 3 or fewer axes** ⇒ consistent with the book, which recommends grid search in exactly that
  regime (§11.4.3, p. 446).
- **The efficiency gap disappears under wall-clock accounting** ⇒ report both; the book's claim is per trial,
  and grid's loose parallelism is a real advantage it grants (§11.4.3, p. 448).
- **Confidence intervals overlap at every size tested** ⇒ no claim about which search is better is licensed;
  this is the resolvability failure the second half of this benchmark exists to catch (§5.3.1, p. 152).
- **Cross-validated comparison reported with an exact variance** ⇒ not available: there is no unbiased
  estimator of the variance of the cross-validated average, so intervals are conventional approximations
  (§5.3.1, p. 152).
- **The selected configuration's test error is much worse than its validation error** ⇒ expected direction of
  bias, since validation error underestimates generalization error (§5.3, p. 151); report the gap rather than
  treating the validation number as the result.
- **A model-based arm consumes full runs on pathological configurations** ⇒ the book's stated shared defect;
  the prescribed mitigation is the variant that maintains several partially-run experiments and freezes or
  unfreezes them (§11.4.5, pp. 449–450).
- **The search keeps improving while the learning rate axis is unswept** ⇒ the most important knob was left
  out; the book's instruction is that if only one hyperparameter can be tuned, it should be the learning rate
  (§11.4.1, p. 443).

## 6. Validity limits and source traceability

- The exponential-efficiency claim is conditional on the presence of near-irrelevant axes; it is not a
  universal ordering of the two methods (§11.4.4, pp. 448–449).
- The comparison rule is a **convention**, adopted because no unbiased variance estimator exists for the
  cross-validated average; overlapping intervals mean "not distinguishable", not "equal" (§5.3.1, p. 152).
- The 10⁵-sample resolvability point is a book-era rule of thumb, not a derived bound (§5.3.1, p. 151).
- The verdict on model-based hyperparameter optimization is a 2016 verdict: the book states it cannot be
  clearly determined whether Bayesian hyperparameter optimization is a mature tool that yields better results
  or does more with less, that it sometimes performs like a human expert and sometimes fails catastrophically,
  and that it is worth trying on a given problem but not yet mature or reliable (§11.4.5, p. 449). Nothing here
  should be read as a current judgement on Bayesian optimization tooling.
- Repeated use of the same test set across years and attempts makes estimates optimistic and benchmarks
  stale; the book's observation is that the field migrates to new, usually larger and harder benchmarks
  (§5.3, p. 151).

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
are the 2016 state of the art as the book reports it; the immaturity verdict is dated accordingly. The grid
value sets, the 80/20 split and the ~10⁵-sample point are book-era conventions, usable as defaults but not
derived. No post-2016 search algorithm or tooling is introduced.
