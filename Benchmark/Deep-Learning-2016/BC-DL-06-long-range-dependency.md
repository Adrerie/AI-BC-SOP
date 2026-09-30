# BC-DL-06 — Long-range dependency: does the spectral account predict the learnable span?

**Tests:** a quantitative prediction about how far dependencies can be learned, and the structural limit on
fixing it · **Executed by:**
[`SOP-DL-04`](../../SOP/Deep-Learning-2016/SOP-DL-04-diagnose-optimization-failure.md) and
[`SOP-DL-07`](../../SOP/Deep-Learning-2016/SOP-DL-07-choose-and-test-inductive-bias.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The book gives an account of long-term dependencies that yields a measurable prediction, plus a structural
limit that constrains what any fix can achieve:

- **Mechanism.** Repeated multiplication by a shared weight matrix W gives Wᵗ; eigenvalues with magnitude
  greater than 1 explode, less than 1 vanish. Vanishing means no usable direction signal; explosion means
  unstable learning. In the power-method view, components orthogonal to the dominant eigenvector are discarded
  (§8.2.5, pp. 310–311).
- **Quantitative form.** The gradient magnitude of long-range interactions becomes exponentially small
  relative to short-range ones; perturbing along an eigenvector direction, the separation after n backward
  steps scales as δ|λ|ⁿ (§10.7, p. 421; §10.8, p. 422).
- **Structural limit.** For an RNN to store memory robustly and resist small perturbations, it **must** live
  in the vanishing-gradient region of parameter space (§10.7, p. 420). The failure therefore cannot be
  optimized away by simply moving elsewhere in parameter space.
- **Empirical scale.** The probability that SGD successfully trains a vanilla RNN rapidly goes to zero once
  the required dependency span reaches lengths of only **10 or 20** (Bengio et al., 1994b, as cited)
  (§10.7, p. 421).
- **Why feedforward networks differ.** Deep feedforward networks largely avoid this because each layer uses a
  *different* matrix rather than a shared one (§8.2.5, p. 311; §10.7, p. 420).
- **Remedies and their limits.** Clipping does not help vanishing gradients; an information-flow regularizer
  combined with clipping markedly extends the learnable dependency span, but that combination is less
  effective than LSTM on redundant data such as language modelling (§10.11.2, p. 432). In gating, the
  self-loop is LSTM's core contribution — a path on which the gradient persists — and the critical factor
  turns out to be the **forget gate**, with a +1 bias on it making LSTM as robust as the best variants
  explored (§10.10, pp. 425–429).
- **Structural alternatives.** A chain of length τ has depth τ, while a balanced binary tree has depth
  O(log τ); how best to construct the tree is explicitly unresolved (§10.6, pp. 417–419). And for reservoir
  computing, contractive maps plus finite precision force forgetting, so that literature advocates a spectral
  radius much greater than 1 because nonlinearity makes the derivatives drift toward 0 (§10.8, pp. 421–423).

## 2. Data and comparison conditions

- **Task family.** The book's own demonstration order is used: **artificial long-dependency datasets first**,
  where the required span is a controlled parameter, then real tasks (§10.10.1, p. 428).
- **Span sweep.** Required dependency span varied across at least the range in which the book reports failure
  for a vanilla RNN (lengths of 10 to 20) and beyond it.
- **Architecture arms** at matched parameter count where possible:
  1. vanilla recurrent network with a shared W;
  2. the same network with gradient clipping (norm form and elementwise form);
  3. the same network with an information-flow regularizer **combined with** clipping;
  4. gated network (LSTM), and a forget-gate ablation, and LSTM with a +1 forget-gate bias;
  5. a deep feedforward network of comparable parameter count, as the control for the shared-matrix account;
  6. a tree-structured (recursive) network at equal τ, as the O(log τ) depth control.
- **Eigenvalue condition.** For the spectral prediction to be testable, the recurrent Jacobian must be
  approximately time-invariant; the book's δ|λ|ⁿ statement assumes a constant Jacobian, as in a purely linear
  network (§10.8, p. 422). With nonlinearity the derivatives drift, so the linear account is an
  approximation and must be labelled as one.
- **Redundancy condition.** For the remedy comparison, include a redundant task such as language modelling,
  where the book predicts the regularizer-plus-clipping combination underperforms LSTM (§10.11.2, p. 432).
- **Sequence-length condition for the bottleneck claim.** An encoder–decoder arm with a fixed-size context
  vector C, evaluated across increasing input lengths; the prediction is monotone degradation because C's
  dimensionality is too small to adequately summarize a long sequence (§10.4, p. 415).

## 3. Baselines

- The vanilla recurrent network is the baseline for every remedy arm.
- The deep feedforward network is the control for the shared-matrix explanation: if the account is right, it
  should not show the same exponential degradation with span.
- LSTM is the reference remedy against which clipping and the information-flow regularizer are judged, since
  the book states the regularizer combination is less effective than LSTM on redundant data.
- For the bottleneck arm, the fixed-size-C model is the baseline and a variable-length context is the
  comparison.

## 4. Metrics

1. **Maximum learnable dependency span** — the book's own instrument for gated units, demonstrated on
   artificial long-dependency datasets before real tasks (§10.10.1, p. 428).
2. **Probability of successful training versus required span**, reproducing the shape of the cited result that
   it rapidly goes to zero around spans of 10–20 (§10.7, p. 421).
3. **Gradient magnitude ratio between long-range and short-range interactions as a function of lag n**, tested
   against δ|λ|ⁿ with the measured spectral radius (§10.7, p. 421; §10.8, p. 422).
4. **Spectral radius of the recurrent Jacobian**, and the fraction of eigenvalues with magnitude above or below
   1, recorded per arm — including the reservoir-computing case where a radius much greater than 1 is
   advocated (§10.8, pp. 422–423).
5. **Task quality versus input sequence length** for the encoder–decoder arm (§10.4, p. 415).
6. **Depth of the computational graph between consecutive time steps** for the tree arm, O(log τ) versus τ
   (§10.6, pp. 417–419).
7. Clipping incidence and update norm for the clipping arms, with the note that norm clipping preserves
   direction while elementwise clipping does not (§10.11.1, pp. 430–431).

The book gives no numeric span threshold as a pass criterion, no tolerance for the exponential fit and no
spectral-radius target for trained networks; these are evaluator choices and must be reported.

## 5. How to interpret failure

- **Vanilla RNN fails at short spans while the feedforward control does not** ⇒ the shared-matrix account is
  reproduced; the cause is Wᵗ, not depth per se (§8.2.5, p. 311).
- **Clipping improves the vanishing case** ⇒ something else was wrong, because the book states plainly that
  clipping does not help vanishing gradients; check whether the run was actually in the exploding regime
  (§10.11.2, p. 432).
- **Information-flow regularizer plus clipping matches LSTM on a redundant task** ⇒ contradicts the book's
  stated comparison; report the task's redundancy explicitly, since that is the condition under which the
  shortfall is predicted (§10.11.2, p. 432).
- **Gating does not extend the span** ⇒ gating is not the binding constraint for this task; check the forget
  gate first, since the book identifies it as the critical factor and reports that a +1 bias on it is what
  makes LSTM as robust as the best variants explored (§10.10.2, p. 429).
- **Measured decay does not follow δ|λ|ⁿ** ⇒ check the time-invariance assumption; with nonlinearity the
  derivatives drift toward 0 and suppress explosion, which is precisely why the reservoir-computing literature
  advocates a radius much greater than 1 (§10.8, pp. 422–423). A mismatch is evidence about the linearization,
  not necessarily about the mechanism.
- **Tree structure gives no span gain** ⇒ the tree was wrong for the data; the book states that how best to
  construct the tree is unresolved (§10.6, p. 417).
- **Encoder–decoder quality flat in sequence length** ⇒ the context vector was not the constraint at the
  lengths tested; extend the length range before concluding.
- **A model that stores memory robustly shows no vanishing** ⇒ contradicts the structural claim; verify the
  memory requirement is real, because the book's point is that robust memory storage *requires* the
  vanishing-gradient region (§10.7, p. 420).

## 6. Validity limits and source traceability

- The δ|λ|ⁿ prediction assumes a **constant Jacobian over time**, as in a purely linear network; for nonlinear
  networks it is an approximation (§10.8, p. 422).
- The span-10/20 figure is a cited 1994 result about a vanilla RNN trained with SGD on the tasks of that
  study; it is a scale indicator, not a threshold for modern architectures (§10.7, p. 421).
- The claim that gated variants struggle to beat the originals is a report about the variants explored in the
  cited comparisons, not a proof that no better variant exists (§10.10.2, p. 429).
- The encoder–decoder bottleneck was observed specifically in machine translation (§10.4, p. 415); other
  tasks may not show the same length sensitivity.
- The structural claim (robust memory requires the vanishing region) is an argument about parameter space, not
  a measured quantity; it constrains interpretation rather than providing a metric.
- Display equations are images in this copy, so the exact form of the information-flow regularizer and of the
  eigenvalue decomposition are cited at prose level.

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

**Historical boundary.** The span-10/20 result, the reservoir-computing spectral-radius practice, the echo
state property, leaky units and clockwork-style update frequencies, peephole connections, and the verdict that
gated RNNs were the most effective sequence models in practice at the time of writing are all book-era and
reported as such. The book also records the general lesson that second-order methods for recurrent networks
were superseded by careful initialization plus Nesterov momentum and, for LSTMs, by plain SGD — designing a
model that is easy to optimize being usually easier than designing a more powerful optimizer (§10.11,
pp. 429–430). No post-2016 sequence architecture is introduced, and no attention-based replacement for the
fixed context vector is assumed beyond what the book itself states.
