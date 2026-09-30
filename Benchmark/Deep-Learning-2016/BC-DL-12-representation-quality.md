# BC-DL-12 — Is a learned representation better than the linear control, and robust where it claims to be?

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

The claims under test are the criteria the book actually supplies:

| Arm | Claim | Locator |
| --- | --- | --- |
| a | A linear encoder–decoder minimizing reconstruction error yields tied, orthonormal weights spanning the principal eigenvectors of the covariance — so PCA is the control any nonlinear code must beat | §13.5, p. 509; §14.1, pp. 511–512 |
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

- **Matched code dimension.** Every arm compares against PCA at the same dimensionality; without this the
  comparison is confounded by capacity.
- **Linearity control (arm a).** A linear encoder and decoder trained on reconstruction error, checked against
  the covariance's principal eigenvectors.
- **Capacity sweep (arm b).** Code dimension and network capacity swept from undercomplete through
  overcomplete, with and without regularization (sparsity penalty, denoising, contractive penalty).
- **Perturbation protocol (arms c, d).** Inputs perturbed along estimated manifold-tangent directions and
  orthogonally to them, recording the induced change in the code; and the encoder Jacobian's singular-value
  spectrum recorded per example.
- **Noise-scale sweep (arm e).** Denoising autoencoder trained at decreasing Gaussian noise scales, with the
  reconstruction error and the contractive penalty compared as the noise becomes small.
- **Tying condition (arm f).** Contractive autoencoder with tied and untied decoder weights.
- **Downstream tasks (arm g).** A linear classifier on the frozen code, and a semantic-similarity retrieval
  task, both at matched code dimension against PCA.
- **Representation-family contrast (arm h).** A distributed code versus the book's non-distributed contrast
  class — k-means, k-nearest-neighbours, decision trees, Gaussian and mixture-of-experts models, kernel
  machines with local kernels, n-gram models — measured in parameters and in the number of input regions
  distinguished.
- **Encoding contrast (arm i).** One-hot versus a distributed encoding of the same categorical variable.
- **Sparse-coding arm (arm j).** An optimization-based encoder against a parametric linear-sigmoid
  autoencoder at matched dictionary size, including a very-low-labels-per-class condition.

## 3. Baselines

- **PCA at matched dimension** is the baseline for every representational claim (arm a).
- **The identity function** is the degenerate baseline that arm b must be shown not to have reached.
- For arm d, the untrained encoder's Jacobian spectrum is the baseline against which "most singular values
  below 1" is read.
- For arm g, PCA-based codes and raw inputs are the baselines for the downstream classifier.
- For arm j, the parametric autoencoder is the baseline.

## 4. Metrics

1. **Reconstruction error**, reported at matched code dimension and always alongside the PCA control — never
   alone (§14.1, p. 511).
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

- **The nonlinear code does not beat PCA at matched dimension** ⇒ no representational gain has been
  demonstrated; the book's control exists precisely to catch this (§13.5, p. 509).
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
The criteria themselves — beat PCA at matched dimension, do not degenerate to the identity, be sensitive along
manifold tangents and insensitive orthogonally, keep the encoder Jacobian contractive, and demonstrate
downstream utility — are stated as general and are retained. No post-2016 representation-learning metric is
introduced.
