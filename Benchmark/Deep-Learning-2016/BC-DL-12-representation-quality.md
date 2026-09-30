# BC-DL-12 — Does a learned representation meet the criteria the book gives, each against its own appropriate control?

**Tests:** the criteria the book gives for judging a code, beyond reconstruction error · **Executed by:**
[`SOP-DL-08`](../../SOP/Deep-Learning-2016/SOP-DL-08-decide-what-to-share.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

Reconstruction error alone does not establish that a representation is good, and the book says why in two
directions: with a linear decoder and mean squared error, an undercomplete autoencoder simply recovers the
**PCA subspace** (§14.1, pp. 511–512; §13.5, p. 509); and if capacity is too large the autoencoder learns the
**identity** and captures nothing (§14.1, p. 512). The code must reflect the training set's distinctive
statistical structure rather than acting as an identity function (§14.2, p. 512).

The claims under test are the criteria the book actually supplies. **Each arm carries its own control.** PCA
is the right comparator only where the book itself makes a linear or undercomplete-autoencoder comparison —
arms a and g — because that is exactly the regime in which the book proves a linear encoder–decoder with mean
squared error recovers the PCA subspace (§13.5, p. 509; §14.1, pp. 511–512). Outside that regime PCA is not a
control for the claim being made: manifold sensitivity is judged against orthogonal-direction response,
contractiveness against the untrained spectrum, the distributed-representation counting argument against the
book's own non-distributed contrast class, and one-hot against a distributed encoding of the same variable.

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

- **Matched code dimension wherever a code is compared to another code.** This applies to the arms that
  actually make a code-to-code comparison (a, g, j) — without it the comparison is confounded by capacity. It
  does not apply to the within-model criteria (c, d, e, f), which compare directions, spectra or two
  quantities of the same trained encoder, nor to the counting argument (h) or the encoding contrast (i).
- **PCA control, restricted.** Run the PCA comparison for arms a and g only, at matched dimension. Do not use
  it as the yardstick for arms c, d, e, f, h, i or j; each of those has the control named below.
- **Linearity control (arm a).** A linear encoder and decoder trained on reconstruction error, checked against
  the covariance's principal eigenvectors.
- **Capacity sweep (arm b).** Code dimension and network capacity swept from undercomplete through
  overcomplete, with and without regularization (sparsity penalty, denoising, contractive penalty). Control:
  the identity function.
- **Perturbation protocol (arms c, d).** Inputs perturbed along estimated manifold-tangent directions and
  orthogonally to them, recording the induced change in the code; and the encoder Jacobian's singular-value
  spectrum recorded per example. Controls: the **orthogonal-direction response** for arm c, and a
  structure-free reference encoder (random projection at the same dimension) to show the tangent alignment is
  not an artifact of any encoder.
- **Noise-scale sweep (arm e).** Denoising autoencoder trained at decreasing Gaussian noise scales, with the
  reconstruction error and the contractive penalty compared as the noise becomes small. Control: the two
  quantities against each other — this is a self-comparison, not a comparison to PCA.
- **Tying condition (arm f).** Contractive autoencoder with tied and untied decoder weights. Control: the tied
  variant.
- **Downstream tasks (arm g).** A linear classifier on the frozen code, and a semantic-similarity retrieval
  task, both at matched code dimension against PCA — this is the book's own comparison (§14.9, p. 531), so PCA
  is in scope here.
- **Representation-family contrast (arm h).** A distributed code versus the book's non-distributed contrast
  class — k-means, k-nearest-neighbours, decision trees, Gaussian and mixture-of-experts models, kernel
  machines with local kernels, n-gram models — measured in parameters and in the number of input regions
  distinguished. Control: the contrast class itself, not a linear subspace method.
- **Encoding contrast (arm i).** One-hot versus a distributed encoding of the same categorical variable.
  Control: the one-hot encoding.
- **Sparse-coding arm (arm j).** An optimization-based encoder against a parametric linear-sigmoid
  autoencoder at matched dictionary size, including a very-low-labels-per-class condition. Control: the
  parametric autoencoder.

## 3. Baselines

Each arm has the control that fits its own claim. There is no single baseline for the whole benchmark.

| Arm | Baseline | Why this one |
| --- | --- | --- |
| a | **PCA at matched dimension**, plus the covariance's principal eigenvectors | This is the linear / undercomplete regime where the book proves the equivalence (§13.5, p. 509; §14.1, pp. 511–512) |
| b | **The identity function** | The degenerate solution the arm must be shown not to have reached (§14.1, p. 512) |
| c | **Orthogonal-direction response** on the same encoder, plus a random-projection encoder at matched dimension | The criterion is a directional contrast within one code, not a code-to-code ranking (§14.6, pp. 523–524) |
| d | **The untrained encoder's Jacobian spectrum** | "Most singular values below 1" is read against where training started (§14.7, pp. 527–529) |
| e | **The contractive penalty at the same noise scale** | An asymptotic equivalence between two quantities of one model (§14.7, p. 528) |
| f | **The tied-decoder variant** | The degenerate small-constant solution appears only when weights are untied (§14.7, p. 530) |
| g | **PCA-based codes and raw inputs**, at matched dimension | The book's own downstream comparison (§14.9, p. 531) |
| h | **The book's non-distributed contrast class** — k-means, k-NN, decision trees, Gaussian and mixture-of-experts models, local-kernel machines, n-gram models | The claim is about parameters versus distinguished regions across representation families (§15.4, pp. 549–554) |
| i | **The one-hot encoding of the same variable** | The claim is that one-hot distance is constant at 2, so no similarity is expressible (§15.1.1, p. 537) |
| j | **A parametric linear-sigmoid autoencoder at matched dictionary size** | The claimed advantage comes from the encoder being obtained by optimization rather than learned (§13.4, p. 507) |

Using PCA outside arms a and g is a **mis-specified baseline**, not a stricter test: it compares a nonlinear
manifold or counting claim against a linear subspace method that the book never offered as the comparator for
it.

## 4. Metrics

1. **Reconstruction error**, reported at matched code dimension and — for the linear and undercomplete
   configurations of arms a and g — alongside the PCA control. Never reported alone (§14.1, p. 511). For the
   nonlinear arms the reconstruction number is context, not the verdict.
2. **Encoder Jacobian singular-value spectrum**: the fraction below 1, and the alignment of the
   largest-singular-value directions with estimated manifold tangents (arm d).
3. **Code displacement under perturbation**: ‖Δh‖ along tangent directions versus orthogonal directions
   (arm c).
4. **Cosine similarity between the learned linear decoder subspace and the covariance's principal
   eigenvectors** (arm a).
5. **Identity-degeneration indicator**: the code's mutual agreement with the input under an overcomplete
   unregularized configuration (arm b).
6. **Contractive penalty versus denoising reconstruction error** across the noise-scale sweep (arm e).
7. **Downstream linear-classifier accuracy and semantic-retrieval quality** on frozen codes (arm g).
8. **Parameters versus distinguished regions** for the representation-family contrast, and the number of
   concepts describable by n features with k values (arm h).
9. **Labels-per-class sensitivity** for arm j.

The book gives no threshold for "most singular values below 1", no acceptable ‖Δh‖ ratio and no target
downstream margin; these are evaluator choices and must be declared.

## 5. How to interpret failure

- **The learned code does not beat PCA at matched dimension in arm a or g** ⇒ no representational gain has
  been demonstrated *for that criterion*; the book's control exists precisely to catch this (§13.5, p. 509;
  §14.9, p. 531). It does **not** by itself refute arms c, d, e, f, h, i or j, which are decided by their own
  controls — a code can fail to lower reconstruction error and still be tangent-aligned, contractive, or more
  statistically efficient per parameter.
- **Reconstruction error falls while downstream accuracy does not improve** ⇒ reconstruction is not the
  criterion; the book's own example is a 30-unit bottleneck that beats 30-dimensional PCA on reconstruction
  *and* on interpretability and class separation (§14.9, p. 531). Report both.
- **Code equals the input under an overcomplete configuration** ⇒ identity degeneration, i.e. the
  autoencoder captured nothing (§14.1, p. 512). Add regularization rather than capacity.
- **Jacobian singular values mostly above 1** ⇒ the contractive penalty is not doing its job; check its weight
  and, for arm f, whether the decoder was tied — untied weights admit the degenerate small-constant solution
  (§14.7, p. 530).
- **Sensitivity is uniform across tangent and orthogonal directions** ⇒ the manifold criterion fails; the code
  has not aligned with the data's local structure (§14.6, pp. 523–524).
- **Denoising error and the contractive penalty diverge at small noise** ⇒ the equivalence is an asymptotic
  statement in the small-Gaussian-noise limit; check the noise scale before treating a mismatch as a
  refutation (§14.7, p. 528).
- **One-hot encoding matches the distributed one** ⇒ the categorical variable had no similarity structure to
  exploit; arm i's point is that one-hot distance is constant at 2 for any two distinct values, so no
  similarity can be expressed (§15.1.1, p. 537).
- **Sparse coding shows no advantage at very low labels per class** ⇒ differs from the cited result; report the
  dictionary size and the encoder type, since the claimed advantage comes from the encoder being obtained by
  optimization rather than learned as parameters (§13.4, p. 507).

## 6. Validity limits and source traceability

- **The PCA equivalence is a theorem about a specific configuration**, not a universal yardstick: linear
  encoder and decoder, mean squared error, undercomplete code (§14.1, pp. 511–512; §13.5, p. 509). Applying it
  to nonlinear manifold, contractive, counting or encoding claims is outside its scope, and any such
  comparison must be labeled as the evaluator's addition rather than the book's control.
- Arm h's counting argument is a **statistical-efficiency** statement about regions and parameters; the book
  also notes the VC dimension of deep linear-threshold networks is only O(w log w), and that a strong
  representation with a weak classifier is itself a strong regularizer. These are capacity arguments, not
  measured accuracies, and the geometric interpretation is offered as such (§15.4, pp. 550–554).
- Interpretability evidence in the book is observational — hidden units in networks trained on large image
  collections are interpretable, and directions in a face-generating model separate gender from eyeglasses
  (§15.4, pp. 554–555). It supports the existence of distributed factors, not a metric.
- Arm e's equivalence holds only in the small-noise limit.
- Arm j's generalization claims are cited results on particular tasks and label budgets, not universal
  rankings.
- The manifold criterion depends on an estimate of the tangent directions; the book notes that extracting
  manifold coordinates is itself very challenging (§5.11.3, p. 190), so arm c inherits that difficulty.
- Display equations are images in this copy, so the exact contractive penalty form and the exact
  singular-value condition are cited at prose level.

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

**Historical boundary.** The 30-unit bottleneck result, the semantic-hashing example, the image-collection
and face-model interpretability observations, the sparse-coding generalization results and their very-low-label
conditions, and the named baseline implementations are all cited 2016-era or earlier work, reported as such.
The criteria themselves are stated as general and are retained: in the linear / undercomplete regime beat PCA
at matched dimension; do not degenerate to the identity; be sensitive along manifold tangents and insensitive
orthogonally; keep the encoder Jacobian contractive; and demonstrate downstream utility. No post-2016
representation-learning metric is introduced.
