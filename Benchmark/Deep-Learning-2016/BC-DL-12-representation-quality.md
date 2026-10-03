# BC-DL-12 — Does a learned representation meet the criteria the book gives, each against its own appropriate control?

**Tests:** the criteria the book gives for judging a code, beyond reconstruction error · **Executed by:**
[`SOP-DL-08`](../../SOP/Deep-Learning-2016/SOP-DL-08-decide-what-to-share.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

Reconstruction error alone does not establish that a representation is good. The book gives that reason in
two directions. With a linear decoder and mean squared error, an undercomplete autoencoder simply recovers the
**PCA subspace** (§14.1, pp. 511–512; §13.5, p. 509).

If the capacity is too large, the autoencoder learns the **identity** and captures nothing (§14.1, p. 512).
The code must reflect the distinctive statistical structure of the training set, rather than act as an identity
function (§14.2, p. 512).

The claims under test are the criteria the book actually supplies. **Each arm carries its own control.** PCA is
the right comparator only where the book itself makes a linear or undercomplete-autoencoder comparison, which
is arms a and g. That is exactly the regime where the book proves the equivalence: a linear encoder–decoder
with mean squared error recovers the PCA subspace (§13.5, p. 509; §14.1, pp. 511–512).

Outside that regime, PCA is not a control for the claim under test. Each criterion has its own comparator:

- manifold sensitivity, against the orthogonal-direction response
- contractiveness, against the untrained spectrum
- the distributed-representation counting argument, against the book's own non-distributed contrast class
- one-hot, against a distributed encoding of the same variable

| Arm | Claim | Locator |
| --- | --- | --- |
| a | A linear encoder–decoder minimizing reconstruction error yields tied, orthonormal weights spanning the principal eigenvectors of the covariance — so **in this linear / undercomplete regime** PCA is the control a learned code is compared against | §13.5, p. 509; §14.1, pp. 511–512 |
| b | An overcomplete or unregularized autoencoder degenerates to the identity | §14.1, p. 512; §14.2, p. 512 |
| c | **Manifold criterion**: a good encoder is sensitive only along manifold-tangent directions and insensitive to orthogonal ones, with reconstruction pulling one way and the constraint the other | §14.6, pp. 523–524 |
| d | **Contractive criterion**: the penalty is the squared Frobenius norm of the encoder Jacobian; a Jacobian is contractive when ‖Jx‖ ≤ 1 for all unit x; after training, **most Jacobian singular values are below 1**, and the largest-singular-value directions correspond to the learned tangent directions | §14.7, pp. 527–529 |
| e | In the small-Gaussian-noise limit, denoising reconstruction error equals the contractive penalty | §14.7, p. 528 |
| f | Without tying the decoder weights to the transpose of the encoder, a contractive autoencoder admits a degenerate small-constant solution | §14.7, p. 530 |
| g | **Downstream utility**: a 30-unit bottleneck achieves lower reconstruction error than 30-dimensional PCA *and* more interpretable, better class-separated codes; semantic hashing places semantically related samples close together | §14.9, p. 531 |
| h | Distributed representations carry an exponential statistical advantage: n features with k values describe kⁿ concepts, and n linear-threshold features with O(nd) parameters assign unique codes to O(n^d) regions, versus O(n) regions for n nearest-neighbour samples; a strong representation with a weak linear classifier is itself a strong regularizer, and the VC dimension of deep linear-threshold networks is only O(w log w) | §15.4, pp. 549–554 |
| i | One-hot encodings carry no similarity information — the squared L2 distance between any two distinct one-hot vectors is 2 | §15.1.1, p. 537 |
| j | Optimization-based (non-parametric) encoders such as sparse coding have no encoder generalization error, and were reported to generalize better than a linear-sigmoid autoencoder, and better still with very few labels per class | §13.4, p. 507 |

## 2. Data and comparison conditions

- **Matched code dimension wherever a code is compared to another code.** That requirement applies to the
  arms that actually make a code-to-code comparison (a, g, j). Without that requirement, capacity confounds
  the comparison. The requirement does not apply to the within-model criteria (c, d, e, f). Those criteria
  compare directions, spectra, or two quantities of the same trained encoder. The requirement also does not
  apply to the counting argument (h) or to the encoding contrast (i).
- **PCA control, restricted.** Run the PCA comparison for arms a and g only, at matched dimension. Arms c, d,
  e, f, h, i and j each have the control named below. PCA is not the yardstick for those arms.
- **Linearity control (arm a).** Train a linear encoder and a linear decoder on reconstruction error. Check the
  learned weights against the covariance's principal eigenvectors.
- **Capacity sweep (arm b).** Sweep the code dimension and the network capacity from undercomplete through
  overcomplete, with and without regularization (sparsity penalty, denoising, contractive penalty). Control:
  the identity function.
- **Perturbation protocol (arms c, d).** Perturb the inputs along the estimated manifold-tangent directions,
  and perturb the inputs orthogonally to those directions. Record the change that each perturbation induces in
  the code. Record the singular-value spectrum of the encoder Jacobian, per example. The control for arm c is
  the **orthogonal-direction response** of the same encoder, and no extra representation baseline is required
  by the book.
- **Noise-scale sweep (arm e).** Train a denoising autoencoder at Gaussian noise scales that become smaller in
  steps. Compare the reconstruction error with the contractive penalty as the noise becomes small. The control
  is the two quantities against each other. That comparison is a self-comparison, not a comparison to PCA.
- **Tying condition (arm f).** Train a contractive autoencoder with tied decoder weights, and again with
  untied decoder weights. Control: the tied variant.
- **Downstream tasks (arm g).** Run a linear classifier on the frozen code, and run a semantic-similarity
  retrieval task. Use both at a matched code dimension against PCA. That is the book's own comparison
  (§14.9, p. 531), so PCA is in scope for arm g.
- **Representation-family contrast (arm h).** Compare a distributed code with the book's non-distributed
  contrast class. That class holds k-means, k-nearest-neighbours, decision trees, Gaussian and
  mixture-of-experts models, kernel machines with local kernels, and n-gram models. Measure each family in
  parameters, and in the number of input regions that the family distinguishes. The control is the contrast
  class itself, not a linear subspace method.
- **Encoding contrast (arm i).** Compare a one-hot encoding with a distributed encoding of the same categorical
  variable. Control: the one-hot encoding.
- **Sparse-coding arm (arm j).** Compare an optimization-based encoder with a parametric linear-sigmoid
  autoencoder at a matched dictionary size. Include a condition with very few labels per class. Control: the
  parametric autoencoder.

## 3. Baselines

Each arm has the control that fits its own claim. There is no single baseline for the whole benchmark.

| Arm | Baseline | Why this one |
| --- | --- | --- |
| a | **PCA at matched dimension**, plus the covariance's principal eigenvectors | This is the linear / undercomplete regime where the book proves the equivalence (§13.5, p. 509; §14.1, pp. 511–512) |
| b | **The identity function** | The degenerate solution the arm must be shown not to have reached (§14.1, p. 512) |
| c | **Orthogonal-direction response** on the same encoder | The criterion is a directional contrast within one code, not a code-to-code ranking (§14.6, pp. 523–524) |
| d | **The untrained encoder's Jacobian spectrum** | "Most singular values below 1" is read against where training started (§14.7, pp. 527–529) |
| e | **The contractive penalty at the same noise scale** | An asymptotic equivalence between two quantities of one model (§14.7, p. 528) |
| f | **The tied-decoder variant** | The degenerate small-constant solution appears only when weights are untied (§14.7, p. 530) |
| g | **PCA-based codes and raw inputs**, at matched dimension | The book's own downstream comparison (§14.9, p. 531) |
| h | **The book's non-distributed contrast class** — k-means, k-NN, decision trees, Gaussian and mixture-of-experts models, local-kernel machines, n-gram models | The claim is about parameters versus distinguished regions across representation families (§15.4, pp. 549–554) |
| i | **The one-hot encoding of the same variable** | The claim is that one-hot distance is constant at 2, so no similarity is expressible (§15.1.1, p. 537) |
| j | **A parametric linear-sigmoid autoencoder at matched dictionary size** | The claimed advantage comes from the encoder being obtained by optimization rather than learned (§13.4, p. 507) |

PCA used outside arms a and g is a **mis-specified baseline**, not a stricter test. That choice compares a
nonlinear manifold claim, or a counting claim, against a linear subspace method. The book never offered that
linear method as the comparator for those claims.

## 4. Metrics

1. **Reconstruction error**, reported at a matched code dimension. For the linear and undercomplete
   configurations of arms a and g, report the reconstruction error alongside the PCA control. Never report the
   reconstruction error alone (§14.1, p. 511). For the nonlinear arms, the reconstruction number is context,
   not the verdict.
2. **Encoder Jacobian singular-value spectrum** (arm d). Report the fraction of singular values below 1.
   Report the alignment of the largest-singular-value directions with the estimated manifold tangents
   (arm d).
3. **Code displacement under perturbation**: ‖Δh‖ along tangent directions versus orthogonal directions
   (arm c).
4. **Cosine similarity between the learned linear decoder subspace and the covariance's principal
   eigenvectors** (arm a).
5. **Contractive penalty versus denoising reconstruction error** across the noise-scale sweep (arm e).
6. **Downstream linear-classifier accuracy and semantic-retrieval quality** on frozen codes (arm g).
7. **Parameters versus distinguished regions** for the representation-family contrast (arm h). Also report the
   number of concepts that n features with k values can describe.
8. **Labels-per-class sensitivity** for arm j.

Arm b is a validity check, not a separate invented metric. An overcomplete, unregularized autoencoder can
realize the identity map. So a low reconstruction error, by itself, cannot establish representation quality.

The book gives no threshold for "most singular values below 1", no acceptable ‖Δh‖ ratio and no target
downstream margin. Those three values are evaluator choices, and the evaluator must declare each value.

## 5. How to interpret failure

- **The learned code does not beat PCA at matched dimension in arm a or g** ⇒ no representational gain stands
  *for that criterion*. The book's control exists precisely to catch that outcome (§13.5, p. 509; §14.9,
  p. 531). That null result does **not** by itself refute arms c, d, e, f, h, i or j. Their own controls decide
  those arms. A code can fail to lower reconstruction error and still be tangent-aligned, contractive, or more
  statistically efficient per parameter.
- **Reconstruction error falls while downstream accuracy does not improve** ⇒ reconstruction is not the
  criterion. The book's own example is a 30-unit bottleneck that beats 30-dimensional PCA on reconstruction
  *and* on interpretability and class separation (§14.9, p. 531). Report both numbers.
- **Code equals the input under an overcomplete configuration** ⇒ the autoencoder degenerated to the identity,
  and captured nothing (§14.1, p. 512). Add regularization rather than capacity.
- **Jacobian singular values mostly above 1** ⇒ the contractive penalty fails. Check the weight of the
  penalty. For arm f, check the tied variant, because untied weights admit the degenerate small-constant
  solution (§14.7, p. 530).
- **Sensitivity is uniform across tangent and orthogonal directions** ⇒ the manifold criterion fails. The code
  does not align with the local structure of the data (§14.6, pp. 523–524).
- **Denoising error and the contractive penalty diverge at small noise** ⇒ the equivalence is an asymptotic
  statement about the small-Gaussian-noise limit. Check the noise scale before you treat a mismatch as a
  refutation (§14.7, p. 528).
- **One-hot encoding matches the distributed one** ⇒ the categorical variable had no similarity structure to
  exploit. Arm i's point is that the one-hot distance is constant at 2 for any two distinct values. So the
  encoding expresses no similarity (§15.1.1, p. 537).
- **Sparse coding shows no advantage at very low labels per class** ⇒ that result differs from the cited
  result. Report the dictionary size and the encoder type. The claimed advantage comes from the encoder that
  optimization supplies, rather than from an encoder that training learns as parameters (§13.4, p. 507).

## 6. Validity limits and source traceability

- **The PCA equivalence is a theorem about a specific configuration**, not a universal yardstick. The
  configuration is a linear encoder and decoder, mean squared error, and an undercomplete code (§14.1,
  pp. 511–512; §13.5, p. 509). A use of that equivalence on nonlinear manifold, contractive, counting or
  encoding claims falls outside that scope. The evaluator must label any such comparison as an addition of the
  evaluator, rather than as the book's control.
- Arm h's counting argument is a **statistical-efficiency** statement about regions and parameters. The book
  also notes that the VC dimension of deep linear-threshold networks is only O(w log w). The book also notes
  that a strong representation with a weak classifier is itself a strong regularizer. Those three items are
  capacity arguments, not measured accuracies. The book offers the geometric interpretation as such (§15.4,
  pp. 550–554).
- Interpretability evidence in the book is observational. Hidden units in networks trained on large image
  collections are interpretable. Directions in a face-generating model separate gender from eyeglasses
  (§15.4, pp. 554–555). That evidence supports the existence of distributed factors, not a metric.
- Arm e's equivalence holds only in the small-noise limit.
- Arm j's generalization claims are cited results on particular tasks and label budgets, not universal
  rankings.
- The manifold criterion depends on an estimate of the tangent directions. The book notes that extracting
  manifold coordinates is itself very challenging (§5.11.3, p. 190). Arm c therefore inherits that difficulty.
- Display equations are images in this copy. So the exact form of the contractive penalty, and the exact
  singular-value condition, are cited at prose level.

| Claim | Locator |
| --- | --- |
| Undercomplete autoencoder; linear decoder with MSE recovers the PCA subspace; identity failure at excess capacity | §14.1, pp. 511–512 |
| Code must reflect distinctive statistics, not act as the identity; regularized variants (sparse, denoising, derivative penalty) | §14.2, pp. 512–516 |
| Linear autoencoder ⇒ PCA; factor analysis, probabilistic PCA, ICA identifiability, slow feature analysis, sparse coding as the baseline family | §13, pp. 497–509 |
| Denoising autoencoder training procedure | §14.5, p. 518 |
| Manifold criterion: sensitivity along tangents, insensitivity orthogonally | §14.6, pp. 523–524 |
| Contractive autoencoder: squared Frobenius norm of the encoder Jacobian, contractiveness condition, singular values below 1, tangent directions, denoising equivalence, stacking, tied decoder | §14.7, pp. 527–530 |
| Applications and downstream utility; 30-unit bottleneck versus 30-dimensional PCA; semantic hashing | §14.9, p. 531 |
| Distributed representations: kⁿ concepts, O(n^d) regions with O(nd) parameters, contrast class, linear-classifier regularization, VC dimension O(w log w), interpretability evidence | §15.4, pp. 549–555 |
| One-hot distance 2 | §15.1.1, p. 537 |
| Manifold hypothesis and the difficulty of extracting manifold coordinates | §5.11.3, pp. 187–190 |

**Historical boundary.** These items are all cited 2016-era or earlier work, reported as such:

- the 30-unit bottleneck result
- the semantic-hashing example
- the image-collection and face-model interpretability observations
- the sparse-coding generalization results, and their very-low-label conditions
- the named baseline implementations

The criteria themselves are general, and this benchmark retains those criteria:

- In the linear / undercomplete regime, beat PCA at matched dimension.
- Do not degenerate to the identity.
- Be sensitive along manifold tangents, and insensitive along orthogonal directions.
- Keep the encoder Jacobian contractive.
- Demonstrate downstream utility.

No post-2016 representation-learning metric is introduced.
