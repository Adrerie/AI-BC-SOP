# BC-DL-06 — Long-range dependency: does the spectral account predict the learnable span?

**Tests:** a quantitative prediction about how far dependencies can be learned, and the structural limit on
fixing that failure · **Executed by:**
[`SOP-DL-04`](../../SOP/Deep-Learning-2016/SOP-DL-04-diagnose-optimization-failure.md) and
[`SOP-DL-07`](../../SOP/Deep-Learning-2016/SOP-DL-07-choose-and-test-inductive-bias.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The book gives an account of long-term dependencies that yields a measurable prediction, plus a structural
limit that constrains what any fix can achieve:

- **Mechanism.** Repeated multiplication by a shared weight matrix W gives Wᵗ. Eigenvalues with magnitude
  greater than 1 explode. Eigenvalues with magnitude less than 1 vanish. Vanishing leaves no usable direction
  signal. Explosion makes learning unstable. The power-method view discards the components orthogonal to the
  dominant eigenvector (§8.2.5, pp. 310–311).
- **Quantitative form.** The gradient magnitude of long-range interactions becomes exponentially small
  relative to the gradient magnitude of short-range interactions. Perturb along an eigenvector direction. The
  separation after n backward steps then scales as δ|λ|ⁿ (§10.7, p. 421; §10.8, p. 422).
- **Structural limit.** An RNN **must** live in the vanishing-gradient region of parameter space to store
  memory robustly and to resist small perturbations (§10.7, p. 420). A simple move elsewhere in parameter
  space therefore does not optimize the failure away.
- **Empirical scale.** The probability that SGD successfully trains a vanilla RNN rapidly goes to zero. The
  drop happens once the required dependency span reaches lengths of only **10 or 20** (Bengio et al., 1994b,
  as cited) (§10.7, p. 421).
- **Why feedforward networks differ.** Deep feedforward networks largely avoid the problem, because each layer
  uses a *different* matrix rather than a shared one (§8.2.5, p. 311; §10.7, p. 420).
- **Remedies and their limits.** Clipping does not help vanishing gradients. An information-flow regularizer
  combined with clipping markedly extends the learnable dependency span. That combination is less effective
  than LSTM on redundant data such as language modelling (§10.11.2, p. 432). In gating, the self-loop is
  LSTM's core contribution. The self-loop is a path on which the gradient persists. The critical factor turns
  out to be the **forget gate**. A +1 bias on the forget gate makes LSTM as robust as the best variants
  explored (§10.10, pp. 425–429).
- **Structural alternatives.** A chain of length τ has depth τ. A balanced binary tree has depth O(log τ).
  How best to construct the tree is explicitly unresolved (§10.6, pp. 417–419). For reservoir computing,
  contractive maps plus finite precision force the reservoir to forget. That literature therefore advocates a
  spectral radius much greater than 1, because nonlinearity makes the derivatives drift toward 0
  (§10.8, pp. 421–423).

## 2. Data and comparison conditions

- **Task family.** Use the book's own demonstration order. That order puts **artificial long-dependency
  datasets first**, where the required span is a controlled parameter. Then the order moves to real tasks
  (§10.10.1, p. 428).
- **Span sweep.** Vary the required dependency span. Cover at least the range in which the book reports
  failure for a vanilla RNN (lengths of 10 to 20). Cover spans beyond that range too.
- **Architecture arms.** Build the arms at matched parameter count where possible:
  1. Use a vanilla recurrent network with a shared W.
  2. Use the same network with gradient clipping (norm form and elementwise form).
  3. Use the same network with an information-flow regularizer **combined with** clipping.
  4. Use a gated network (LSTM). Run the forget-gate ablation on the LSTM. Run the LSTM with a +1
     forget-gate bias.
  5. Use a deep feedforward network of comparable parameter count. That arm is the control for the
     shared-matrix account.
  6. Use a tree-structured (recursive) network at equal τ. That arm is the O(log τ) depth control.
- **Eigenvalue condition.** For the spectral prediction to be testable, the recurrent Jacobian must be
  approximately time-invariant. The book's δ|λ|ⁿ statement assumes a constant Jacobian, as in a purely linear
  network (§10.8, p. 422). With nonlinearity the derivatives drift. The linear account is therefore an
  approximation. Label the linear account as an approximation.
- **Redundancy condition.** For the remedy comparison, include a redundant task such as language modelling.
  The book predicts that the regularizer-plus-clipping combination underperforms LSTM on such a task
  (§10.11.2, p. 432).
- **Sequence-length condition for the bottleneck claim.** Evaluate an encoder–decoder arm with a fixed-size
  context vector C across increasing input lengths. The prediction is monotone degradation, because the
  dimensionality of C is too small to adequately summarize a long sequence (§10.4, p. 415).

## 3. Baselines

- The vanilla recurrent network is the baseline for every remedy arm.
- The deep feedforward network is the control for the shared-matrix explanation. If the shared-matrix account
  is right, the feedforward control should not show the same exponential degradation with span.
- LSTM is the reference remedy for clipping and for the information-flow regularizer. That choice follows the
  book's statement that the regularizer combination is less effective than LSTM on redundant data.
- For the bottleneck arm, the fixed-size-C model is the baseline and a variable-length context is the
  comparison.

## 4. Metrics

1. Record the **maximum learnable dependency span**. This metric is the book's own instrument for gated units.
   The book demonstrates the instrument on artificial long-dependency datasets before real tasks (§10.10.1,
   p. 428).
2. Record the **probability of successful training versus required span**. Reproduce the shape of the cited
   result. In that result the probability rapidly goes to zero around spans of 10–20 (§10.7, p. 421).
3. Record the **gradient magnitude ratio between long-range and short-range interactions as a function of lag
   n**. Test that ratio against δ|λ|ⁿ, using the measured spectral radius (§10.7, p. 421; §10.8, p. 422).
4. Record the **spectral radius of the recurrent Jacobian**. Also record the fraction of eigenvalues with
   magnitude above or below 1. Take both per arm. Include the reservoir-computing case, where that literature
   advocates a radius much greater than 1 (§10.8, pp. 422–423).
5. Record **task quality versus input sequence length** for the encoder–decoder arm (§10.4, p. 415).
6. Record the **depth of the computational graph between consecutive time steps** for the tree arm. Compare
   O(log τ) with τ (§10.6, pp. 417–419).
7. Record clipping incidence and the update norm for the clipping arms. Norm clipping preserves direction.
   Elementwise clipping does not preserve direction (§10.11.1, pp. 430–431).

The book gives no numeric span threshold as a pass criterion, and no tolerance for the exponential fit. The
book gives no spectral-radius target for trained networks. Each of the three is an evaluator choice that the
evaluator must report.

## 5. How to interpret failure

- **Vanilla RNN fails at short spans while the feedforward control does not** ⇒ the test reproduces the
  shared-matrix account. The cause is Wᵗ, not depth per se (§8.2.5, p. 311).
- **Clipping improves the vanishing case** ⇒ something else was wrong. The book states plainly that clipping
  does not help vanishing gradients. Check whether the run was actually in the exploding regime (§10.11.2,
  p. 432).
- **Information-flow regularizer plus clipping matches LSTM on a redundant task** ⇒ the result contradicts the
  book's stated comparison. Report the redundancy of the task explicitly. That redundancy is the condition
  under which the book predicts the shortfall (§10.11.2, p. 432).
- **Gating does not extend the span** ⇒ gating is not the binding constraint for this task. Check the forget
  gate first. The book identifies the forget gate as the critical factor. The book reports that a +1 bias on
  the forget gate makes LSTM as robust as the best variants explored (§10.10.2, p. 429).
- **Measured decay does not follow δ|λ|ⁿ** ⇒ check the time-invariance assumption. With nonlinearity the
  derivatives drift toward 0 and suppress explosion. This drift is precisely why the reservoir-computing
  literature advocates a radius much greater than 1 (§10.8, pp. 422–423). A mismatch is evidence about the
  linearization, not necessarily about the mechanism.
- **Tree structure gives no span gain** ⇒ the tree was wrong for the data. The book states that how best to
  construct the tree is unresolved (§10.6, p. 417).
- **Encoder–decoder quality stays flat in sequence length** ⇒ the context vector was not the constraint at the
  lengths tested. Extend the length range before you draw that conclusion.
- **A model that stores memory robustly shows no vanishing** ⇒ the result contradicts the structural claim.
  Verify that the memory requirement is real, because the book's point is that robust memory storage
  *requires* the vanishing-gradient region (§10.7, p. 420).

## 6. Validity limits and source traceability

- The δ|λ|ⁿ prediction assumes a **constant Jacobian over time**, as in a purely linear network. For
  nonlinear networks the prediction is an approximation (§10.8, p. 422).
- The span-10/20 figure is a cited 1994 result about a vanilla RNN trained with SGD on the tasks of that
  study. The figure is a scale indicator, not a threshold for modern architectures (§10.7, p. 421).
- The claim that gated variants struggle to beat the originals is a report about the variants explored in the
  cited comparisons. The claim is not a proof that no better variant exists (§10.10.2, p. 429).
- The book reports the encoder–decoder bottleneck specifically for machine translation (§10.4, p. 415). Other
  tasks may not show the same length sensitivity.
- The structural claim (robust memory requires the vanishing region) is an argument about parameter space, not
  a measured quantity. The claim constrains interpretation rather than providing a metric.
- Display equations are images in this copy. This benchmark therefore cites the exact form of the
  information-flow regularizer, and the exact form of the eigenvalue decomposition, at prose level.

**Modern update (2017–2026) — one further validity limit (`delta_map.md` §2.1, §2.4).** The structural limit
that this benchmark tests is **architecture-bound**. State that scope with the result. The spectral account
and the span-10/20 figure describe a *recurrent* path. On that path a dependency at distance n is carried by
n successive applications of the same transition matrix.

An architecture that connects all positions with a **constant number of sequentially executed operations**
removes that path altogether. The shortest route between any two positions no longer grows with n. That
growth is precisely the quantity that the spectral account makes exponential. Recurrent models are the entire
scope of this benchmark. Nothing here changes for recurrent models. The 2016 account is left intact.

The interpretation of a *failure* to learn a long dependency is what changes. Under the 2016 account one
explanation is available: the recurrent gradient path. Under the modern account, rule out a second
explanation before you report the gradient path. The second explanation is whether the dependency was simply
**outside the length the architecture's cost permits**.

The cost of attention grows quadratically with sequence length. That cost bounds the usable length in a
different way. Sparsifying the connection pattern is the named category of response. The observable is "the
model cannot learn a dependency at span n". That one observable has two distinct modern causes. A report
that does not name the architecture under test cannot distinguish the two causes.

The modern update specifies no attention architecture, endorses no sparsification scheme, and adds no arm to
this benchmark. *Sources: `ATTN` (abstract, §4); `UDL` §12.9 fol. 227–228.*

| Claim | Locator |
| --- | --- |
| Wᵗ mechanism; explosion and vanishing by eigenvalue magnitude; power-method view; feedforward nets use different matrices | §8.2.5, pp. 310–311 |
| Long-range gradient magnitude exponentially small; robust memory requires the vanishing region; span-10/20 result | §10.7, pp. 419–421 |
| δ|λ|ⁿ separation; contractive maps and finite precision force forgetting; radius much greater than 1 advocated; complex eigenvalues imply oscillation | §10.8, pp. 421–423 |
| Clipping forms and threshold; Inf/NaN escape; clipped-estimator bias | §10.11.1, pp. 430–431 |
| Clipping does not help vanishing; information-flow regularizer with clipping; weaker than LSTM on redundant data | §10.11.2, p. 432 |
| Self-loop as LSTM's core contribution; context-dependent time constant; forget-gate ablation and +1 bias; artificial long-dependency datasets as the first proving ground | §10.10, pp. 425–429 |
| Encoder–decoder: length decoupling; fixed-C bottleneck; variable-length C with attention | §10.4, pp. 413–415 |
| Recursive nets: O(log τ) depth; unresolved tree construction | §10.6, pp. 417–419 |
| Which recurrent block to deepen; shortest-path argument | §10.5, pp. 415–417 |

**Modern-update provenance.** Every row above is a 2016-book locator, and none was altered. The added
validity limit in §6 is sourced outside the 2016 book. That limit is recorded in
[`Validation/Deep-Learning-Modern-2017-2026/delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md)
§2.1 and §2.4. The source keys are defined in
[`sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md) §2.1: `ATTN` (abstract, §4) and
`UDL` §12.9 fol. 227–228. The claim under test, the comparison conditions, the baselines and the metrics are
unchanged, and no arm was added.

**Historical boundary.** These items are all book-era, and are reported as such:

- the span-10/20 result
- the reservoir-computing spectral-radius practice
- the echo state property
- leaky units and clockwork-style update frequencies
- peephole connections
- the verdict that gated RNNs were the most effective sequence models in practice at the time of writing

The book also records a general lesson. Second-order methods for recurrent networks were superseded by careful
initialization plus Nesterov momentum, and, for LSTMs, by plain SGD. The lesson is that designing a model that
is easy to optimize is usually easier than designing a more powerful optimizer (§10.11, pp. 429–430). This
benchmark introduces no post-2016 sequence architecture. This benchmark assumes no attention-based replacement
for the fixed context vector, beyond what the book itself states.

The modern update qualified the closing clause of this note. The 2016 text remains free of any post-2016
architecture. This benchmark still tests only recurrent models. The note records the *verdict* that gated RNNs
were the most effective sequence models in practice. That verdict is now era-bound in a stronger sense than
the note originally conveyed.

The stronger sense concerns the structural limit. That limit is a property of the recurrent path that this
benchmark measures. An architecture with a constant-length path between positions is not subject to that
limit. The modern update records that finding as a validity limit in §6, rather than as a change to the claim
under test.
