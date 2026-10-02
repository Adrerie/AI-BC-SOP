# SOP-DL-02 — Diagnose the fitting regime and set effective capacity

**Stage:** diagnose · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Read two numbers — training error and the train/test gap — classify the fitting regime, and move
**effective capacity** in the direction the regime requires. This SOP also owns the first-baseline
recipe, the "collect more data?" decision, and the interpretation frame that keeps those two decisions
from being over-claimed.

In scope: §5.2 (capacity, over/underfitting, Bayes error, no free lunch), §11.2 (default baselines),
§11.3 (more data), §11.4.1 (the U-curve and the three limits on effective capacity).

Out of scope: which regularizer to apply once the gap is the problem (`SOP-DL-03`), repairing an
optimizer that cannot reach low training error (`SOP-DL-04`), the search protocol that moves several
knobs at once (`SOP-DL-05`), and verifying that the errors are measured correctly at all
(`SOP-DL-06`, which must run first when the numbers are surprising).

## 2. Inputs and assumptions

- The specification from `SOP-DL-01`: task type, metric, target value.
- A trained system with **both** a training error and an honest generalization error estimate. The
  book's frame requires it: generalization error is the expected error on new inputs, estimated on a
  test set carved out of the training data (§5.2, p. 141).
- The i.i.d. assumption: train and test examples are independent and drawn from the same
  data-generating distribution p_data. The book is explicit that if train and test data are collected
  arbitrarily, very little can be concluded (§5.2, p. 142).
- A capacity lever that can actually be moved (architecture size, regularization strength, learning
  rate) and the budget to retrain.

## 3. Procedure

### 3.1 Establish the baseline before interpreting any number (§11.2, p. 439)

1. Decide whether deep learning is needed at all: if choosing a few linear weights correctly might
   solve the problem, start from a simple statistical model such as logistic regression. For
   "AI-complete" problems — the book names object recognition, speech recognition, machine
   translation — starting from a suitable deep model works better.
2. Choose the model class from the **structure of the data**: fixed-size vector input under supervision
   ⇒ fully connected feedforward network; input with known topology (images are the example) ⇒
   convolutional network; sequence input or output ⇒ gated recurrent network (LSTM or GRU).
3. Start with piecewise-linear units: ReLU or its extensions (Leaky ReLU, PReLU, maxout).
4. Optimizer: SGD with a decayed learning rate and momentum is a reasonable choice — the popular decay
   forms named are linear decay to a fixed minimum, exponential decay, or dividing the learning rate by
   2–10× whenever validation error stalls, and these behave differently across problems. Adam is
   described as another very reasonable choice.
5. Batch normalization has a significant effect on optimization performance, especially for
   convolutional networks and networks with sigmoid nonlinearities. It is reasonable to omit it from
   the first baseline, but it should be used immediately once optimization appears problematic.
6. Regularization from the start: unless the training set contains tens of millions of examples or
   more, the project should include some mild regularization from the beginning. Early stopping is
   widely used. Dropout is easy to implement and compatible with many models and training algorithms.
   Batch normalization sometimes also lowers generalization error, in which case Dropout may be omitted
   because the statistics used for normalization are themselves noisy estimates.
7. If the task resembles a widely studied one, copy the model and algorithms known to perform well on
   it — possibly even a trained model. The book's example is reusing features from convolutional
   networks trained on ImageNet for other computer-vision tasks (Girshick et al., 2015, as cited).
8. Unsupervised learning in the first baseline is domain-dependent: natural language processing
   benefits greatly from unsupervised techniques such as learned word embeddings, whereas in computer
   vision unsupervised learning brought no benefit at the time except in semi-supervised settings with
   very few labels (Kingma et al., 2014; Rasmus et al., 2015, as cited). Include it in the first
   end-to-end baseline only where it is considered important for the application's environment;
   otherwise try it first when the initial baseline is found to overfit.

### 3.2 Classify the regime (§5.2, pp. 141–142)

9. Report training error and generalization error separately, and the **gap** between them. The two
   factors that determine success are exactly these: lowering training error, and shrinking the gap.
   - **Underfitting** — the model cannot obtain a sufficiently low error on the training set.
   - **Overfitting** — the gap between training error and test error is too large.
   For a *fixed* model, the expected training error equals the expected test error, because both
   expectations use the same data-generating process; the inequality arises only because parameters are
   selected to minimize training error after the training set has been sampled (§5.2, p. 142). Do not
   therefore treat a nonzero gap as anomalous — treat its size as the quantity to manage.

### 3.3 Know which capacity you are moving (§5.2, p. 144; §11.4.1, p. 442)

10. Distinguish **representational capacity** (the functions the model family allows when parameters are
    adjusted to lower the training objective) from **effective capacity** (what the learning algorithm
    can actually reach). Effective capacity can be smaller, because finding the best function in the
    family is a hard optimization problem and the learner typically settles for a function that greatly
    reduces training error.
11. Effective capacity is limited by three things (§11.4.1, p. 442): the model's representational
    capacity; the learning algorithm's ability to minimize the training cost successfully; and the degree
    to which the cost function and training procedure regularize the model. Practical consequence: a
    model with plenty of representational capacity can still underfit, either because the optimizer
    cannot find a suitable function or because a regularizer excludes it. Capacity levers therefore
    come in three families — architecture (layers, units per layer), optimization (learning rate first),
    regularization (`SOP-DL-03`) — and the diagnosis must say which family is binding.
12. Use the book's direction table (Table 11.1, p. 445) when moving a knob: number of hidden units
    (capacity increases with them; nearly every operation's time and memory cost rises too);
    learning rate (**capacity is maximized at the optimal value** — a wrong rate, too high or too low,
    yields a low-effective-capacity model through optimization failure); convolution kernel width
    (increases parameters; wider kernels shrink the output size unless implicit zero padding
    compensates, which would reduce capacity); implicit zero padding (preserves larger representations,
    at higher time and memory cost); weight-decay coefficient (capacity increases as it is *lowered*,
    since parameters are freer to grow); Dropout rate (capacity increases as the rate is *lowered*,
    since units cooperate more to fit the training set).

### 3.4 Reason with the U-curve, and sample points on it (§5.2, pp. 145–146, Fig. 5.3; §11.4.1, pp. 442–443)

13. As capacity rises, training error decreases monotonically until it asymptotes at the smallest
    achievable value. Generalization error is **U-shaped** in capacity: at the left end both errors are
    high (underfitting regime); as capacity increases, training error falls but the gap widens; once the
    growth of the gap outpaces the fall in training error, the system is in the overfitting regime, past
    the optimal capacity. The best point combines a moderate training error with a moderate gap.
14. Expect to *sample* the curve rather than solve for its minimum. Many capacity knobs are discrete
    (units per layer, number of linear pieces in a maxout unit), so only a few points on the curve are
    reachable; binary knobs give two points; bounded knobs give only part of the curve — weight decay
    has a floor at zero, so if the model underfits at λ = 0 the overfitting side cannot be reached by
    moving λ at all.
15. Apply the two branches (§11.4.1, p. 444):
    - **Training error above target** ⇒ only a capacity increase can help. If no regularization is in
      use and the optimizer is known to be working, add layers or hidden units, accepting the compute
      cost.
    - **Test error above target while training error is low** ⇒ test error is the sum of training error
      and the gap, so the target is to shrink the gap without letting training error rise faster than
      the gap falls. Change regularization knobs to reduce effective capacity (add Dropout or weight
      decay). The book's stated expectation: the best performance usually comes from a large model that
      is well regularized.
16. Record the brute-force option when resources allow it: keep increasing model capacity and training
    set size until the problem is solved. This raises training and inference cost and is feasible only
    with sufficient resources; in principle it can fail because optimization becomes harder, but the
    book observes that for many problems optimization does not turn out to be a significant obstacle,
    provided a suitable model was chosen (§11.4.1, pp. 445–446).

> **Modern update (2017–2026) — the right branch of the U-curve is era-scoped.** Steps 13–16 remain the
> procedure, but the assumption that generalization error keeps rising once capacity passes the optimum no
> longer holds in general. The modern account distinguishes three regimes and reports a **second descent**
> beyond the interpolation threshold, and it is explicit that the explanation is putative rather than
> settled. It is also explicit that the phenomenon is **dataset-dependent**: it appears on MNIST with the
> original labels, but emerges or becomes prominent under label noise and on MNIST-1D and CIFAR-100. The
> operational consequence is stated directly — "in the modern regime, there is no way to tell how much
> capacity should be added before the test error stops improving."
>
> Two changes to how this section is used follow, and no change to steps 13–16 themselves:
>
> - A rising **development/validation** error at high capacity is **not** by itself evidence that the
>   optimum has been passed. If capacity is affordable, explore additional points using development data.
>   Whether a second descent appears must be measured rather than assumed. **Do not inspect the final test
>   set to decide whether to extend the capacity ladder or select a checkpoint**; freeze the protocol first.
> - Separately, the modern evidence runs *against* treating excess capacity as the thing to regularize
>   away: there are almost no examples of state-of-the-art test performance on complex datasets where the
>   model has significantly fewer parameters than training data points; pruned networks remain
>   over-parameterized after pruning; and distillation "has not yet provided convincing evidence that
>   under-parameterized models can perform well". The current reading is that overparameterization is needed
>   for generalization at present dataset sizes and complexities, with the question left open whether small
>   models fundamentally cannot perform or training merely cannot find good solutions for them. One
>   quantitative sharpening: in D dimensions, smooth interpolation requires D times more parameters than
>   mere interpolation.
>
> No mechanism and no threshold for the interpolation point is supplied here, because the sources settle
> neither. *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §1.4,
> §1.5. Sources: `UDL` §8.4 fol. 127–132 and §8.5 fol. 132; `UDL` §20.5 fol. 415–418.*

### 3.5 Decide whether to collect more data (§11.3, pp. 440–442)

17. First ask whether **training-set** performance is acceptable. If the learning algorithm cannot
    produce a good model on the training data, there is no point collecting more data. Instead: increase
    model size (more layers, or more hidden units per layer), or improve the learning algorithm by
    tuning the learning rate and other hyperparameters. If a larger model *and* carefully debugged
    optimization still fail, suspect the **training data**: it may be too noisy, or it may not contain
    the inputs needed to predict the output. The prescribed response is to start over with cleaner data
    or a feature-richer dataset.
18. If training performance is acceptable, measure test performance. Acceptable ⇒ done. Much worse than
    training performance ⇒ collecting more data is one of the most effective solutions. Weigh the cost
    and feasibility of more data against other ways to reduce test error, and against how much more data
    would actually move the metric. Where large labeled datasets are cheap — the book's examples are
    internet companies with millions or hundreds of millions of users, and large labeled datasets as one
    of the main factors behind object recognition — the answer is almost always to collect more data.
    Where data is expensive or infeasible, as in medical applications, the simple alternative is to
    reduce model size or improve regularization (tune the weight-decay coefficient, add Dropout). If the
    gap is still unacceptable after tuning regularization, collecting more data is desirable.
19. Decide **how much** data. Plot training-set size against generalization error (the book points to
    Fig. 5.4) and extrapolate the trend to predict how much more is needed for a given performance.
    Adding a small fraction of the current total usually does not change generalization error
    significantly, so reason on a **logarithmic scale** — the book's concrete recommendation is to double
    the number of examples between experiments (§11.3, p. 441).
20. If more data is infeasible, the only remaining route to lower generalization error is improving the
    learning algorithm itself, which the book classifies as research rather than advice for application
    practitioners (§11.3, p. 442).

> **Modern update (2017–2026) — compute is a third axis, and the data question becomes an allocation
> question.** Steps 17–20 weigh more data against a smaller or better-regularized model. When a **compute
> budget** is the binding constraint rather than data availability, that weighing is incomplete: parameters
> and training examples are then two ways of spending the same budget, and the split between them is a
> declared decision, not an outcome.
>
> Add one step to §3.5's reasoning:
>
> 20a. If compute is the binding constraint, **declare the allocation and the rule it came from.** Record
>      the budget, the parameter count and the data/token count actually chosen, and which allocation
>      assumption was made. The assumption must be recorded with the conditions under which its source
>      fitted it — power-law fits of this kind hold only under stated conditions (converged training on
>      sufficiently large datasets for the model-size law; large models with limited data and early
>      stopping for the data law; an optimally sized model, sufficiently large dataset and sufficiently
>      small batch size for the compute law).
>
> **Do not adopt an exponent.** The two anchor sources for this area disagree on the split: one fits model
> size growing substantially faster than data with compute, the other fits them growing in **equal
> proportions** and attributes the discrepancy to the first's use of a fixed token count and learning-rate
> schedule across all its models. Both self-report extrapolation uncertainty, and the earlier of the two
> states plainly that it has no solid theoretical understanding and that its trends must eventually level
> off. Because the quantity is contested, this SOP requires the assumption to be *declared* and never
> supplies a number to declare.
>
> Reporting discipline for the budget, hardware and allocation is owned elsewhere: see Trustworthy-ML
> [`SOP-08`](../Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md) — this SOP decides
> what to assume, that one governs how it is reported.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §1.1, §1.2, §1.6.
> Sources: `SCALE`; `CHINCHILLA`.*

### 3.6 Interpret without over-claiming (§5.2, pp. 144–148)

21. **Bayes error is the floor.** Even a model that knows the true distribution p(x, y) makes errors,
    because the mapping may be intrinsically stochastic or y may depend on variables not present in x
    (§5.2, p. 146). Training error can sit *below* Bayes error, because a learner can memorize
    particular training examples.
22. **Data-size behaviour** (Fig. 5.4, pp. 146–147): the expected generalization error never increases
    with more training examples; for non-parametric models more data keeps improving generalization up
    to the best possible error; any fixed-capacity parametric model whose capacity is below optimal
    asymptotes to an error above Bayes error; a model *at* optimal capacity can still show a large
    train/generalization gap, which more data can close; as the training set grows toward infinity, the
    training error of any fixed-capacity model rises to at least Bayes error; and optimal capacity
    itself grows with training-set size, then stops growing once it is sufficient to capture the true
    complexity.
23. **Non-parametric models** are legitimate capacity levers whose complexity tracks the training set:
    nearest-neighbour regression stores all training X and y and returns the target of the nearest point;
    averaging over ties when the nearest vector is not unique achieves the minimum possible training
    error on any regression dataset (§5.2, p. 146). A parameter learning algorithm can also be embedded
    in an outer loop that increases the parameter count (the book's example: an outer loop selecting the
    polynomial degree, an inner loop fitting by linear regression).
24. **No free lunch, correctly used** (§5.2.1, pp. 147–148): averaged over *all possible* data-generating
    distributions, every classification algorithm has the same error rate on previously unobserved
    points — the most sophisticated algorithm and one that maps every input to a single class perform
    equally on average over all possible tasks. This holds only when all distributions are considered.
    In real applications, assuming something about the distributions encountered permits designing
    algorithms that work well on them. The book's conclusion is therefore not "no method is better" but:
    the goal of research is not a universal best algorithm — it is to understand which distributions are
    relevant to real-world experience and which algorithms work best on the distributions we care about.
25. **Do not lean on capacity bounds.** VC dimension (the largest number of training points a binary
    classifier can label arbitrarily) underwrites bounds in which the train/generalization gap grows
    with capacity and shrinks with more samples. The book states these bounds are rarely applied to
    practical deep learning, partly because they are too loose and partly because the capacity of a deep
    learning algorithm is hard to determine — effective capacity depends on the optimizer, and general
    non-convex optimization has little theoretical analysis (§5.2, pp. 144–145).
26. **Occam's razor is a preference, not a proof.** Among hypotheses that equally explain the
    observations, prefer the simplest; the idea was formalized by the founders of statistical learning
    theory. But the book insists on the other half: simpler functions are more likely to generalize, yet
    a sufficiently complex hypothesis is still required to achieve low training error (§5.2,
    pp. 144–145). Regularization is the general way to express such a preference — see `SOP-DL-03`.

> **Modern update (2017–2026) — the capacity-to-data ratio is not a well-defined quantity.** Steps 21–26
> stand. What changes is a precondition several of them silently assume: that "model capacity" and "dataset
> size" are each a single number whose ratio can be read off.
>
> Once augmentation and tokenization enter, the denominator is a choice. The modern worked case: AlexNet
> had roughly 60 million parameters and was trained on roughly 1 million data points, but each training
> example was augmented with 2048 transformations; GPT-3 had 175 billion parameters and was trained on 300
> billion tokens. The source's conclusion is that "there is not a clear-cut case that either model was
> overparameterized."
>
> Apply this as an interpretation constraint, not as a new step:
>
> - Whenever a capacity-to-data comparison is reported, **state what was counted as a data point** — raw
>   examples, augmented views, or tokens — and say which the ratio uses.
> - Do not move between those definitions inside one argument. A regime classification (step 17 onward) that
>   silently switches from raw examples to augmented views is not comparable to one that does not.
> - Treat "the model has more parameters than data points" as a description of a counting convention, never
>   as evidence about the fitting regime.
>
> *Delta: `delta_map.md` §1.3. Source: `UDL` §20.1.1, fol. 403.*

## 4. Important failure modes

- **Reading a mis-measured test error as overfitting.** A save/reload bug or a preprocessing mismatch
  between train and test produces the same signature; `SOP-DL-06` step 3 must run first (§11.5, p. 451).
- **Blaming capacity for an optimization failure.** A wrong learning rate lowers effective capacity
  whatever the model size (§11.4.1, p. 443, Fig. 11.1).
- **Collecting more data while training error is still unacceptable** — the book states there is no
  point (§11.3, p. 441).
- **Adding a small fraction of data and concluding data does not help**; the effect only appears on a
  log scale (§11.3, p. 441).
- **Invoking no-free-lunch to refuse an inductive bias.** The theorem averages over all distributions;
  the book's own conclusion is to characterize the relevant ones (§5.2.1, p. 148).
- **Citing VC-style bounds as evidence about a deep network** (§5.2, p. 145).
- **Confusing representational with effective capacity**, and concluding the family cannot express the
  solution when the optimizer or a regularizer is what excludes it (§5.2, p. 144; §11.4.1, p. 442).
- **Chasing zero error** and ignoring the Bayes floor (§11.1, p. 437).
- **Moving a bounded knob into an unreachable region** and concluding the lever does not work
  (§11.4.1, p. 443).
- **Starting from an exotic baseline**, which makes every later number uninterpretable because there is
  no reference point (§11.2, p. 439).

Modern-update failure modes (provenance in §3.4–§3.6 above):

- **Reading a rising test error at high capacity as proof the optimum was passed**, and stopping there
  instead of sampling one more capacity point — the right branch of the U-curve is not monotone in
  general (`delta_map.md` §1.4).
- **Assuming double descent either is or is not present** without measuring it. It is dataset-dependent
  and prominent under label noise, so it must be observed on the data in use, not imported from either
  era's textbook example (`delta_map.md` §1.4).
- **Comparing two capacity/data configurations at unmatched compute**, which makes the comparison an
  allocation result rather than a capacity result (`delta_map.md` §1.1).
- **Printing an allocation exponent as settled.** The two anchor sources disagree on the split and both
  self-report extrapolation uncertainty; the assumption is declared, never supplied (`delta_map.md` §1.2).
- **Switching the data-point definition mid-argument** — raw examples in one step, augmented views or
  tokens in the next — which silently invalidates every ratio built on it (`delta_map.md` §1.3).

## 5. Outputs and reporting

- The baseline actually used, with any deviation from §11.2 and its reason.
- The regime read: training error, generalization error, gap, target value, and the classification
  (underfitting / overfitting / acceptable), each with the split it was measured on.
- The capacity lever moved, its direction per Table 11.1, and the predicted effect on training error vs
  gap — recorded *before* the run, so the outcome can falsify it.
- The data decision, stated as the branch taken in §11.3 (train unacceptable / gap unacceptable /
  acceptable), with cost-feasibility reasoning, and the size-vs-generalization curve if data scaling was
  probed.
- Final attribution of the residual to one of: evaluation, data, capacity, optimization, regularization.
- Any quantity the book leaves open and that you therefore chose: what counts as "acceptable" training
  error, how large a gap is unacceptable, how many capacity points to sample, and the doubling schedule
  for data-size experiments.

Modern-update additions to the report (`delta_map.md` §1.1, §1.3):

- **The counting convention** for every capacity-to-data ratio reported: what was counted as a data point
  (raw examples, augmented views, or tokens), and which the ratio uses.
- **The compute axis**, when compute rather than data availability was the binding constraint: the budget,
  the parameter count and data/token count chosen, and the allocation assumption made — recorded with the
  conditions under which its source fitted it. No exponent is reported as this lineage's own.
- **Whether the capacity curve was sampled past the point where test error rose**, and what the further
  points showed. Reporting only up to the first rise leaves the second-descent question unasked.

## 6. Source traceability

| Claim or step | Locator |
| --- | --- |
| Generalization error, training error, the two success factors, underfitting/overfitting definitions, i.i.d. assumption and p_data, equality of expectations for a fixed model | §5.2, pp. 141–142 |
| Capacity, hypothesis space, representational vs effective capacity, Occam's razor, VC dimension and why bounds are rarely applied, monotone training error and U-shaped generalization error | §5.2, pp. 143–146, Fig. 5.3 |
| Non-parametric models, nearest-neighbour regression, Bayes error, data-size behaviour and optimal capacity growth | §5.2, pp. 146–147, Fig. 5.4 |
| No free lunch theorem and its correct scope | §5.2.1, pp. 147–148 |
| Regularization as expressing a preference; weight-decay example | §5.2.2, pp. 148–150 |
| Effective capacity's three limits; U-curve in a hyperparameter; bounded/discrete/binary knobs; learning rate as the top knob; the two branches; brute-force scaling | §11.4.1, pp. 442–446, Table 11.1, Fig. 11.1 |
| Default baseline recipe: model class by data structure, unit choice, SGD with decayed LR and momentum, Adam, batch normalization policy, mild regularization default, early stopping, Dropout, transfer from a similar task, unsupervised-learning caveat, the book's own obsolescence warning | §11.2, pp. 439–440 |
| More-data decision tree; data-quality branch; log-scale doubling; algorithmic improvement as research | §11.3, pp. 440–442 |

**Modern-update provenance.** Every row above is a 2016-book locator and none was altered. The blocks
marked *Modern update (2017–2026)* in §3.4, §3.5 and §3.6, and the corresponding entries in §4 and §5,
are sourced outside the 2016 book and are recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§1.1, §1.3, §1.4, §1.5, with source keys defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1: `UDL` §8.4 fol. 127–132,
§8.5 fol. 132–133, §20.1.1 fol. 403, §20.5 fol. 415–418; `SCALE`; `CHINCHILLA`. Resource reporting is
cross-linked to Trustworthy-ML
[`SOP-08`](../Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md) rather than
restated.

**Historical boundary.** §11.2 is the most era-bound part of this SOP and the book says so itself: deep
learning progresses quickly, so better default algorithms may exist soon after publication (§11.2,
p. 439). Treated as historical here: the specific default menu (logistic regression; fully connected /
convolutional / LSTM-GRU by data structure; ReLU, Leaky ReLU, PReLU, maxout; SGD with momentum and the
named decay forms, including division by 2–10× on validation stalls; Adam), the "tens of millions of
examples" threshold for skipping regularization, the ImageNet-feature transfer example, and the
2016-vintage verdict that unsupervised learning helps NLP but not computer vision except in
semi-supervised settings. These are recorded as the book's recommendations, not as current defaults.
The regime definitions, the capacity distinctions, Bayes error, the data-size behaviour and the scope of
no-free-lunch are stated as general results and are not era-bound.

The U-curve reasoning is a **partial** exception, and this note was amended by the modern update: the
curve's *left* branch and the underfitting/overfitting regime definitions are general, but the assumption
that generalization error rises monotonically past the optimum is era-scoped — see the modern-update block
in §3.4. The 2016 text is retained with its original citations; only the annotation was added.
