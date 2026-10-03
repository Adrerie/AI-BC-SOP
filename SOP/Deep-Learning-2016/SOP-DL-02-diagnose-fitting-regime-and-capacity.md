# SOP-DL-02 — Diagnose the fitting regime and set effective capacity

**Stage:** diagnose · **Source package:** *Deep Learning* (Goodfellow, Bengio & Courville, 2016),
Chinese edition — see [`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Purpose and scope

Read two numbers: training error and the train/test gap. Classify the fitting regime from those numbers. Then
move **effective capacity** in the direction that the regime requires. This SOP also owns the first-baseline
recipe, the "collect more data?" decision, and the interpretation frame. That frame keeps the two decisions
from being over-claimed.

In scope: §5.2 (capacity, over/underfitting, Bayes error, no free lunch), §11.2 (default baselines),
§11.3 (more data), §11.4.1 (the U-curve and the three limits on effective capacity).

Out of scope:

- which regularizer to apply once the gap is the problem (`SOP-DL-03`)
- the repair of an optimizer that cannot reach low training error (`SOP-DL-04`)
- the search protocol that moves several knobs at once (`SOP-DL-05`)
- the check that the errors are measured correctly at all (`SOP-DL-06`)

`SOP-DL-06` must run first when the numbers are surprising.

## 2. Inputs and assumptions

- The specification from `SOP-DL-01`: task type, metric, target value.
- A trained system with **both** a training error and an honest estimate of generalization error. The book's
  frame requires both numbers. Generalization error is the expected error on new inputs. The estimate of that
  error comes from a test set carved out of the training data (§5.2, p. 141).
- The i.i.d. assumption. Train examples and test examples are independent, and both come from the same
  data-generating distribution p_data. The book is explicit about the limit. If you collect train and test
  data arbitrarily, you can conclude very little (§5.2, p. 142).
- A capacity lever that you can actually move (architecture size, regularization strength, learning
  rate), and the budget to retrain.

## 3. Procedure

### 3.1 Establish the baseline before interpreting any number (§11.2, p. 439)

1. Decide whether you need deep learning at all. A few linear weights, chosen correctly, might solve the
   problem. In that case, start from a simple statistical model such as logistic regression. For an
   "AI-complete" problem, start from a suitable deep model instead, because that route works better. The book
   names object recognition, speech recognition and machine translation as "AI-complete" problems.
2. Choose the model class from the **structure of the data**. Match the input to the model class:
   - Fixed-size vector input under supervision ⇒ fully connected feedforward network.
   - Input with a known topology ⇒ convolutional network. Images are the book's example.
   - Sequence input or sequence output ⇒ gated recurrent network (LSTM or GRU).
3. Start with piecewise-linear units: ReLU or its extensions (Leaky ReLU, PReLU, maxout).
4. Set the optimizer. SGD with a decayed learning rate and momentum is a reasonable choice. The named popular
   decay forms are linear decay to a fixed minimum, and exponential decay. The third named form divides the
   learning rate by 2–10× whenever the validation error stalls. Those decay forms behave differently across
   problems. The book describes Adam as another very reasonable choice.
5. Batch normalization has a significant effect on optimization performance. That effect is especially strong
   for convolutional networks, and for networks with sigmoid nonlinearities. Omitting batch normalization
   from the first baseline is reasonable. Use batch normalization immediately once optimization looks
   problematic.
6. Plan for regularization from the start. Unless the training set holds tens of millions of examples or more,
   the project should include some mild regularization. Early stopping is a widely used choice. Dropout is
   easy to implement, and is compatible with many models and training algorithms. Batch normalization
   sometimes also lowers generalization error. In that case you may omit Dropout, because the statistics used
   for normalization are themselves noisy estimates.
7. If the task resembles a widely studied task, copy the model and the algorithms that perform well. You may
   even copy a trained model. The book's example reuses features from convolutional networks trained on
   ImageNet, for other computer-vision tasks (Girshick et al., 2015, as cited).
8. Unsupervised learning in the first baseline is domain-dependent. Natural language processing benefits
   greatly from unsupervised techniques such as learned word embeddings. In computer vision, unsupervised
   learning brought no benefit at the time (Kingma et al., 2014; Rasmus et al., 2015, as cited). The one
   exception was a semi-supervised setting with very few labels. Include unsupervised learning in the first
   end-to-end baseline only where the application's environment makes that inclusion important. Otherwise,
   turn to unsupervised learning when the initial baseline overfits.

### 3.2 Classify the regime (§5.2, pp. 141–142)

9. Report training error and generalization error separately. Report the **gap** between the two errors.
   Exactly two things determine success: the training error must fall, and the gap must shrink.

   **Underfitting** means the model cannot obtain a sufficiently low error on the training set.
   **Overfitting** means the gap between training error and test error is too large.

   For a *fixed* model, the expected training error equals the expected test error. Both expectations use the
   same data-generating process. The inequality arises only because the parameters are selected to minimize
   training error, after you sample the training set (§5.2, p. 142). Do not treat a nonzero gap as anomalous.
   Treat the size of the gap as the quantity to manage.

### 3.3 Know which capacity you are moving (§5.2, p. 144; §11.4.1, p. 442)

10. Distinguish **representational capacity** from **effective capacity**. Representational capacity is the set
    of functions that the model family allows. That allowance holds when the parameters are adjusted to lower
    the training objective. Effective capacity is what the learning algorithm can actually reach. Effective
    capacity can be smaller. The reason is that the best function in the family is hard to find. The learner
    typically settles for a function that greatly reduces the training error.
11. Check the three limits on effective capacity (§11.4.1, p. 442):

    - the model's representational capacity
    - the ability of the learning algorithm to minimize the training cost successfully
    - the degree to which the cost function and the training procedure regularize the model

    A model with plenty of representational capacity can still underfit. The optimizer cannot find a suitable
    function, or a regularizer excludes that function. The capacity levers therefore come in three families:

    - architecture (layers, units per layer)
    - optimization (learning rate first)
    - regularization (`SOP-DL-03`)

    The diagnosis must say which family is binding.
12. Use the book's direction table (Table 11.1, p. 445) when you move a knob. The table gives these
    directions:

    - Number of hidden units. Capacity increases with the number of units. The time and memory cost of
      nearly every operation rises too.
    - Learning rate. **The optimal value maximizes capacity.** A wrong rate, too high
      or too low, yields a model of low effective capacity through optimization failure.
    - Convolution kernel width. Wider kernels increase the parameter count. Wider kernels also shrink the
      output size, unless implicit zero padding compensates. That compensation would reduce capacity.
    - Implicit zero padding. That choice preserves larger representations, at a higher time and memory cost.
    - Weight-decay coefficient. Capacity increases when you *lower* that coefficient, because the parameters
      are freer to grow.
    - Dropout rate. Capacity increases when you *lower* that rate, because the units cooperate more to fit
      the training set.

### 3.4 Reason with the U-curve, and sample points on it (§5.2, pp. 145–146, Fig. 5.3; §11.4.1, pp. 442–443)

13. As capacity rises, the training error decreases monotonically. The training error asymptotes at the
    smallest achievable value. Generalization error is **U-shaped** in capacity. The curve reads as follows:
    - At the left end, both errors are high. That is the underfitting regime.
    - As capacity increases, the training error falls, and the gap widens.
    - Once the growth of the gap outpaces the fall in training error, the system is in the overfitting regime.
      The system then sits past the optimal capacity.

    The best point combines a moderate training error with a moderate gap.
14. Expect to *sample* the curve, rather than solve for its minimum. Many capacity knobs are discrete, such as
    units per layer, or the number of linear pieces in a maxout unit. For a discrete knob, only a few points on
    the curve are reachable. A binary knob gives two points. A bounded knob gives only part of the curve. Weight
    decay has a floor at zero. If the model underfits at λ = 0, no move of λ reaches the overfitting side.
15. Apply the two branches (§11.4.1, p. 444):
    - **Training error above target** ⇒ only a capacity increase can help. If the project uses no
      regularization, and the optimizer works, add layers or hidden units. Accept the compute cost of those
      additions.
    - **Test error above target while training error is low.** The test error is the sum of the training error
      and the gap. So the target is to shrink the gap. Do not let the training error rise faster than the gap
      falls. Change a regularization knob to reduce effective capacity. Add Dropout or weight decay. The
      book's stated expectation is that the best performance usually comes from a large model that is well
      regularized.
16. Record the brute-force option for the case of sufficient resources. Keep increasing the model capacity and
    the training set size, until the problem is solved. That route raises the training cost and the inference
    cost. The route is feasible only with sufficient resources. In principle the route can fail, because
    optimization becomes harder. The book observes that, for many problems, optimization does not turn out to
    be a significant obstacle. The observation holds when you chose a suitable model (§11.4.1, pp. 445–446).

> **Modern update (2017–2026) — the right branch of the U-curve is era-scoped.** Steps 13–16 remain the
> procedure. One assumption behind those steps no longer holds in general. The assumption is that
> generalization error keeps rising once capacity passes the optimum. The modern account distinguishes three
> regimes. That account reports a **second descent** beyond the interpolation threshold. The account is
> explicit that the explanation is putative rather than settled. The account is also explicit that the
> phenomenon is **dataset-dependent**. The phenomenon appears on MNIST with the original labels. It emerges,
> or becomes prominent, under label noise, and on MNIST-1D and CIFAR-100. One operational consequence is
> stated directly, and the source's own words follow. "in the modern regime, there is no way to tell how much
> capacity should be added before the test error stops improving."
>
> Two changes follow in how you use this section. Neither change touches steps 13–16 themselves.
>
> First, a rising **development/validation** error at high capacity is **not** evidence of the optimum by
> itself. If capacity is affordable, explore additional points by using development data. Measure whether a
> second descent appears, rather than assume one. **Do not inspect the final test set to decide whether to
> extend the capacity ladder or select a checkpoint.** Freeze the protocol first.
>
> Second, the modern evidence runs *against* treating excess capacity as the thing to regularize away.
> Consider state-of-the-art test performance on a complex dataset. Almost no such example has significantly
> fewer parameters than the training data points. Pruned networks remain over-parameterized after pruning. Distillation "has
> not yet provided convincing evidence that under-parameterized models can perform well". The current reading
> holds that present dataset sizes and complexities need overparameterization for generalization. That reading
> leaves one question open. Small models may fundamentally be unable to perform. Training may merely be unable
> to find good solutions for small models. One quantitative sharpening follows. In D dimensions, smooth
> interpolation requires D times more parameters than mere interpolation.
>
> No mechanism and no threshold for the interpolation point is supplied here, because the sources settle
> neither. *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §1.4,
> §1.5. Sources: `UDL` §8.4 fol. 127–132 and §8.5 fol. 132; `UDL` §20.5 fol. 415–418.*

### 3.5 Decide whether to collect more data (§11.3, pp. 440–442)

17. Ask first whether **training-set** performance is acceptable. If the learning algorithm cannot produce a
    good model on the training data, collecting more data has no point. Increase the model size instead, by
    adding layers, or by adding hidden units per layer. Or improve the learning algorithm, by tuning the
    learning rate and the other hyperparameters. If a larger model still fails, and you debugged the
    optimization carefully, suspect the **training data**. The data may be too noisy. The data may not contain
    the inputs needed to predict the output. The prescribed response is to start over with cleaner data, or
    with a feature-richer dataset.
18. If training performance is acceptable, measure test performance. If test performance is acceptable, you
    are done. If test performance is much worse than training performance, collecting more data is one of the
    most effective solutions. Weigh the cost and the feasibility of more data against other ways to reduce
    test error. Weigh the data also against how much more data would actually move the metric. Where large
    labeled datasets are cheap, the answer is almost always to collect more data. The book gives two examples.
    One is internet companies with millions or hundreds of millions of users. The other is large labeled
    datasets, as one of the main factors behind object recognition. Data can also be expensive or infeasible to
    obtain. Medical applications are the book's case. Then the simple alternative is to reduce model size, or
    to improve regularization. Tune the weight-decay coefficient, or add Dropout. If the gap is still
    unacceptable after you tune regularization, collecting more data is desirable.
19. Decide **how much** data. Plot training-set size against generalization error. The book points to
    Fig. 5.4. Extrapolate the trend, and predict how much more data a given performance needs. Adding a small
    fraction of the current total usually does not change generalization error significantly. So reason on a
    **logarithmic scale**. The book's concrete recommendation is to double the number of examples between
    experiments (§11.3, p. 441).
20. If more data is infeasible, one route to lower generalization error remains. Improve the learning
    algorithm itself. The book classifies that work as research, not as advice for application practitioners
    (§11.3, p. 442).

> **Modern update (2017–2026) — compute is a third axis, and the data question becomes an allocation
> question.** Steps 17–20 weigh more data against a smaller or better-regularized model. Suppose a **compute
> budget** is the binding constraint, rather than data availability. Then that weighing is incomplete.
> Parameters and training examples are two ways of spending the same budget. The split between parameters and
> examples is a declared decision, not an outcome.
>
> Add one step to §3.5's reasoning:
>
> 20a. If compute is the binding constraint, **declare the allocation and the rule that generated the
>      allocation.** Record the budget, the parameter count and the data/token count actually chosen. Record
>      which allocation
>      assumption you made. Record that assumption together with the conditions under which its source
>      fitted that assumption. Power-law fits of this kind hold only under stated conditions:
>
>    - The model-size law holds for converged training on sufficiently large datasets.
>    - The data law holds for large models with limited data and early stopping.
>    - The compute law holds for an optimally sized model, a sufficiently large dataset and a sufficiently
>      small batch size.
>
> **Do not adopt an exponent.** The two anchor sources for this area disagree on the split. One source fits
> model size growing substantially faster than data with compute. The other source fits model size and data
> growing in **equal proportions**. The first source used one fixed token count and one learning-rate
> schedule across all its models. The second source attributes the discrepancy to that choice. Both sources
> self-report extrapolation uncertainty. The earlier source states plainly that its own theoretical
> understanding is not solid. That source also states that its trends must eventually level off. The
> quantity is contested. So this SOP requires you to *declare* the assumption. This SOP never supplies a
> number to declare.
>
> Another document owns the reporting discipline for the budget, the hardware and the allocation. See
> Trustworthy-ML
> [`SOP-08`](../Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md). This SOP decides what
> to assume. That SOP governs how you report the assumption.
>
> *Delta: [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md) §1.1, §1.2, §1.6.
> Sources: `SCALE`; `CHINCHILLA`.*

### 3.6 Interpret without over-claiming (§5.2, pp. 144–148)

21. **Bayes error is the floor.** Even a model that knows the true distribution p(x, y) makes errors. The
    mapping may be intrinsically stochastic, or y may depend on variables that are not present in x (§5.2,
    p. 146). Training error can sit *below* Bayes error. A learner can memorize particular training examples,
    and that gives the lower value.
22. Read the **data-size behaviour** in Fig. 5.4 (pp. 146–147). Each statement below comes from that figure:
    - The expected generalization error never increases with more training examples.
    - For non-parametric models, more data keeps improving generalization up to the best possible error.
    - Any fixed-capacity parametric model whose capacity is below optimal asymptotes to an error above Bayes
      error.
    - A model *at* optimal capacity can still show a large train/generalization gap. More data can close that
      gap.
    - As the training set grows toward infinity, the training error of any fixed-capacity model rises. That
      error rises to at least Bayes error.
    - Optimal capacity itself grows with training-set size. It then stops growing once it is sufficient to
      capture the true complexity.
23. Treat **non-parametric models** as legitimate capacity levers, because their complexity tracks the
    training set. Nearest-neighbour regression stores all training X and y, and returns the target of the
    nearest point. When the nearest vector is not unique, average over the ties. That averaging achieves the
    minimum possible training error on any regression dataset (§5.2, p. 146). A parameter learning algorithm
    can also sit inside an outer loop that increases the parameter count. The book's example uses two loops.
    The outer loop selects the polynomial degree. The inner loop fits by linear regression.
24. Use **no free lunch** with its correct scope (§5.2.1, pp. 147–148). Averaged over *all possible*
    data-generating distributions, every classification algorithm has the same error rate on previously
    unobserved points. On that average, the most sophisticated algorithm performs no better. An algorithm that
    maps every input to a single class performs the same. The theorem holds only when you consider all
    distributions. In a real application, an assumption about the distributions you meet permits a good
    algorithm for those distributions. The book's conclusion is therefore not "no method is better". The goal
    of research is not a universal best algorithm. The goal is to understand which distributions are relevant
    to real-world experience. The goal is also to understand which algorithms work best on those
    distributions.
25. **Do not lean on capacity bounds.** VC dimension is the largest number of training points that a binary
    classifier can label arbitrarily. VC dimension underwrites bounds in which the train/generalization gap
    grows with capacity, and shrinks with more samples. The book states that practical deep learning rarely
    applies those bounds. The book gives two partial reasons. The bounds are too loose. The capacity of a deep
    learning algorithm is also hard to determine. Effective capacity depends on the optimizer, and general
    non-convex optimization has little theoretical analysis (§5.2, pp. 144–145).
26. **Occam's razor is a preference, not a proof.** Among hypotheses that explain the observations equally
    well, prefer the simplest one. The founders of statistical learning theory formalized that idea. The book
    insists on the other half of the claim. Simpler functions are more likely to generalize. Even so, a
    sufficiently complex hypothesis is still necessary for low training error (§5.2, pp. 144–145).
    Regularization is the general way to express such a preference (see `SOP-DL-03`).

> **Modern update (2017–2026) — the capacity-to-data ratio is not a well-defined quantity.** Steps 21–26
> stand. One precondition changes. Several steps assume that precondition silently. The precondition is that
> "model capacity" and "dataset size" are each a single number. That assumption lets you read off the ratio of
> the two.
>
> Once augmentation and tokenization enter the count, the denominator is a choice. Consider the modern worked
> case. AlexNet had roughly 60 million parameters, and training used roughly 1 million data points. Each
> training example was augmented with 2048 transformations. GPT-3 had 175 billion parameters, and training
> used 300 billion tokens. The source's conclusion is that "there is not a clear-cut case that either model
> was overparameterized."
>
> Apply the finding as an interpretation constraint, not as a new step.
>
> First, whenever you report a capacity-to-data comparison, **state what you counted as a data point**. Name
> the choices: raw examples, augmented views, or tokens. Name the count that the ratio uses.
>
> Second, do not move between those definitions inside one argument. A regime classification from step 17
> onward must keep one definition. Silently switching from raw examples to augmented views breaks that
> comparability. A classification with one fixed definition stays comparable to another such classification.
>
> Third, treat "the model has more parameters than data points" as a description of a counting convention.
> Never treat that statement as evidence about the fitting regime.
>
> *Delta: `delta_map.md` §1.3. Source: `UDL` §20.1.1, fol. 403.*

## 4. Important failure modes

- **Reading a mis-measured test error as overfitting.** A save/reload bug produces that signature. So does a
  preprocessing mismatch between train and test. `SOP-DL-06` step 3 must run first (§11.5, p. 451).
- **Blaming capacity for an optimization failure.** A wrong learning rate lowers effective capacity whatever
  the model size (§11.4.1, p. 443, Fig. 11.1).
- **Collecting more data while training error is still unacceptable.** The book states there is no point in
  doing that (§11.3, p. 441).
- **Adding a small fraction of data, and concluding that data does not help.** The effect appears only on a
  log scale (§11.3, p. 441).
- **Invoking no-free-lunch to refuse an inductive bias.** The theorem averages over all distributions. The
  book's own conclusion is to characterize the relevant distributions (§5.2.1, p. 148).
- **Citing VC-style bounds as evidence about a deep network** (§5.2, p. 145).
- **Confusing representational capacity with effective capacity.** From that confusion you may conclude that
  the family cannot express the solution. In fact the optimizer, or a regularizer, is what excludes the
  solution (§5.2, p. 144; §11.4.1, p. 442).
- **Chasing zero error**, and ignoring the Bayes floor (§11.1, p. 437).
- **Moving a bounded knob into an unreachable region**, and concluding that the lever does not work
  (§11.4.1, p. 443).
- **Starting from an exotic baseline.** Every later number then lacks a reference point, and becomes
  uninterpretable (§11.2, p. 439).

Modern-update failure modes. Their provenance is in §3.4–§3.6 above:

- **Reading a rising test error at high capacity as proof that the optimum was passed.** That reading also
  stops the search one capacity point too early. The right branch of the U-curve is not monotone in general
  (`delta_map.md` §1.4).
- **Assuming that double descent either is or is not present**, without measuring that presence. The
  phenomenon is dataset-dependent, and is prominent under label noise. So observe the phenomenon on the data
  in use. Do not import the phenomenon from either era's textbook example (`delta_map.md` §1.4).
- **Comparing two capacity/data configurations at unmatched compute.** That comparison returns an allocation
  result, not a capacity result (`delta_map.md` §1.1).
- **Printing an allocation exponent as settled.** The two anchor sources disagree on the split, and both
  sources self-report extrapolation uncertainty. The assumption is declared, never supplied
  (`delta_map.md` §1.2).
- **Switching the data-point definition mid-argument.** One step may count raw examples, and the next step may
  count augmented views or tokens. That switch silently invalidates every ratio built on the definition
  (`delta_map.md` §1.3).

## 5. Outputs and reporting

- The baseline actually used, with any deviation from §11.2 and the reason for that deviation.
- The regime read: training error, generalization error, the gap, and the target value. Add the
  classification (underfitting / overfitting / acceptable). Report each number with the split that the
  measurement used.
- The capacity lever that you moved, and its direction per Table 11.1. Report the predicted effect on the
  training error versus the gap. Record that prediction *before* the run, so that the outcome can falsify the
  prediction.
- The data decision. State the branch taken in §11.3 (train unacceptable / gap unacceptable / acceptable).
  Give the cost-feasibility reasoning. Add the size-versus-generalization curve, if you probed data scaling.
- Attribute the residual finally to one source: evaluation, data, capacity, optimization or regularization.
- Any quantity the book leaves open, and that you therefore chose. Declare each one:
  - what counts as "acceptable" training error
  - how large a gap is unacceptable
  - how many capacity points to sample
  - the doubling schedule for data-size experiments

Modern-update additions to the report (`delta_map.md` §1.1, §1.3):

- **The counting convention** for every capacity-to-data ratio that you report. Name what you counted as a data
  point (raw examples, augmented views, or tokens). Name the count that the ratio uses.
- **The compute axis**, when compute, rather than data availability, was the binding constraint. Report the
  budget, the parameter count and the data/token count that you chose. Report the allocation assumption that
  you made, together with the conditions under which its source fitted that assumption. No exponent is
  reported as this lineage's own.
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

**Modern-update provenance.** Every row above is a 2016-book locator. None of those rows was altered. The
blocks marked *Modern update (2017–2026)* in §3.4, §3.5 and §3.6 come from outside the 2016 book. The
corresponding entries in §4 and §5 come from the same source. All of those blocks are recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§1.1, §1.3, §1.4 and §1.5.

The source keys are defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1. The keys are `UDL` §8.4
fol. 127–132, §8.5 fol. 132–133, §20.1.1 fol. 403 and §20.5 fol. 415–418, together with `SCALE` and
`CHINCHILLA`. Resource reporting is cross-linked to Trustworthy-ML
[`SOP-08`](../Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md), and is not restated
here.

**Historical boundary.** §11.2 is the most era-bound part of this SOP. The book says so itself. Deep learning
progresses quickly, so better default algorithms may exist soon after publication (§11.2, p. 439). The
following are treated as historical here:

- the specific default menu (logistic regression; fully connected / convolutional / LSTM-GRU by data
  structure; ReLU, Leaky ReLU, PReLU, maxout; SGD with momentum and the named decay forms, including
  division by 2–10× on validation stalls; Adam)
- the "tens of millions of examples" threshold for skipping regularization
- the ImageNet-feature transfer example
- the 2016-vintage verdict that unsupervised learning helps NLP but not computer vision, except in
  semi-supervised settings

The listed items are the book's recommendations, not current defaults. The regime definitions, the
capacity distinctions, Bayes error, the data-size behaviour and the scope of no-free-lunch are stated as
general results. Those results are not era-bound.

The U-curve reasoning is a **partial** exception. The modern update amended this note. The *left* branch of
the curve is general, and the underfitting and overfitting regime definitions are general. But the assumption
that generalization error rises monotonically past the optimum is era-scoped. See the modern-update block in
§3.4.

The 2016 text keeps its original citations. Only the annotation is new.
