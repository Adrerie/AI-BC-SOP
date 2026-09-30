# Benchmark — *Deep Learning* (Goodfellow, Bengio & Courville, 2016)

Benchmark checks (BCs) reconstructed **by evaluable claim** from the 2016 *Deep Learning* monograph.
Twelve BCs. Each exists because the book makes a concrete claim that a comparison could confirm or
falsify — not because a model family needed an entry.

Source record and citation convention:
[`Validation/Deep-Learning-2016/SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md).
Why these claims and not others, including the rejected candidates:
[`Validation/Deep-Learning-2016/concept_reconstruction.md`](../../Validation/Deep-Learning-2016/concept_reconstruction.md) §3.

## Index

| ID | Claim under test | Executed by | Primary book material |
| --- | --- | --- | --- |
| `BC-DL-01` | [Does the cost still teach the model when it is confidently wrong?](BC-DL-01-output-unit-loss-coupling.md) — the output-unit ↔ loss coupling, and the saturation failure it causes | `SOP-DL-01` | §6.2.1.1, §6.2.2.2 p. 209, §6.2.2.3 p. 211 |
| `BC-DL-02` | [Do the capacity and data-size curves behave as the fitting theory predicts?](BC-DL-02-capacity-and-data-size-curves.md) — the U-curve in capacity and the generalization-error curve in training-set size | `SOP-DL-02` | §5.2, §5.2.2, Fig. 5.3, Fig. 5.4, §11.3, §11.4.1 |
| `BC-DL-03` | [Do regularizers work through the mechanisms the book claims?](BC-DL-03-regularization-mechanisms.md) — definition conformance plus mechanism-specific observables | `SOP-DL-03` | §5.2.2, §7.1.1–7.1.2, §7.5.1, §7.8, §7.11, §7.12 |
| `BC-DL-04` | [Adversarial examples: is the failure linearity, and does adversarial training fix it?](BC-DL-04-adversarial-linearity-and-training.md) — the book's stated cause and remedy, tested | `SOP-DL-03` | §7.13 |
| `BC-DL-05` | [Can optimization pathologies be distinguished from traces?](BC-DL-05-optimization-pathology-separability.md) — separability of the symptom → cause → remedy mappings | `SOP-DL-04` | §8.2.1–8.2.7 |
| `BC-DL-06` | [Long-range dependency: does the spectral account predict the learnable span?](BC-DL-06-long-range-dependency.md) — a quantitative prediction and the structural limit on fixing it | `SOP-DL-04`, `SOP-DL-07` | §8.2.5 pp. 310–311, §10.7, §10.9–10.11 |
| `BC-DL-07` | [Implementation-health instruments: is the number produced by the algorithm you think you ran?](BC-DL-07-implementation-health-instruments.md) — injected bugs must be caught by the book's diagnostics | `SOP-DL-06` | §11.5 pp. 450–453 |
| `BC-DL-08` | [Do the architectural priors hold, and does violating them cost what the book predicts?](BC-DL-08-inductive-bias-assumption-tests.md) — sparse interaction, sharing, equivariance, pooling, depth | `SOP-DL-07` | §9.2–9.5, §9.9 p. 383, §10.2, §10.10 |
| `BC-DL-09` | [Search sample-efficiency, and whether the validation material can resolve the difference](BC-DL-09-search-efficiency-and-resolvability.md) — random vs grid at matched budget, plus resolvability | `SOP-DL-05` | §11.4.3, §11.4.4, §5.3.1, §5.3.2 |
| `BC-DL-10` | [When does sharing pay?](BC-DL-10-sharing-gains-vs-labeled-data.md) — pretraining, transfer and unlabeled-data gains as a function of labeled-data size | `SOP-DL-08` | §7.6, §7.7, §15.1.1, §15.2 |
| `BC-DL-11` | [Generative-model comparison: is the measured quantity comparable, and does likelihood track sample quality?](BC-DL-11-generative-evaluation-integrity.md) — commensurability failure and reward hacking | `SOP-DL-09` | §20.14, §18.7.1, §18.7.2, §19.4.4, §17.3–17.5 |
| `BC-DL-12` | [Is a learned representation better than the linear control, and robust where it claims to be?](BC-DL-12-representation-quality.md) — the book's representation criteria against a PCA baseline | `SOP-DL-08` | §14.1, §14.2, §14.5, §14.6, §14.7, §14.9, §13.5, §15.6 |

Each BC carries the six parts the repository requires — capability/failure under test, data and
comparison conditions, baselines, metrics, how to interpret failure, validity limits and source
traceability — plus a closing **Historical boundary** note.

## Standing rules for this package

1. **A model family is not a benchmark.** CNN, RNN, autoencoder, RBM, VAE and GAN have no BC of
   their own. They appear only where a distinct evaluable claim attaches — e.g. `BC-DL-08` tests the
   prior a convolutional network encodes, `BC-DL-11` tests whether generative-evaluation instruments
   agree.
2. **Every metric is a quantity the book names.** No score is introduced to fill a template field.
   Where the book states no threshold, the BC specifies an **ordering** comparison and says that the
   absolute value must come from the run.
3. **A baseline is required.** Each BC names the control condition that makes the claim falsifiable
   (matched-capacity plain model, unrelated-task control, PCA/linear control, injected-bug control,
   fresh-chain control).
4. **Validity limits are stated, not implied.** Each BC §6 records what the result cannot support —
   dataset-bound conclusions, estimator bias direction, the unknowability of MCMC mixing, ELBO
   incomparability across model families.
5. **Historical means historical.** Era benchmarks (MNIST, CIFAR-10, SVHN, ImageNet, street-view
   house numbers) are used as carriers of a comparison condition and labeled as such; §5.3.2's
   benchmark-staleness argument is part of `BC-DL-09`, not an afterthought. No post-2016 metric
   (FID, Inception Score, perplexity-as-standard) appears anywhere in this package.

## Rejected candidates

Recorded so the absence is a decision rather than an oversight — full reasoning in
`concept_reconstruction.md` §3.1:

- Architecture-family comparisons as such.
- Optimizer leaderboards; §8.5.4 explicitly reports no consensus, so a ranking would be an artifact
  of the problem set.
- Generative sample-quality scores the book does not define.
- Depth-vs-width superiority; §6.4.2's 20M→60M observation is matched-parameter and
  experiment-specific, so it is a design argument in `SOP-DL-07`, not a BC.

## Related

- Procedures that execute these checks:
  [`SOP/Deep-Learning-2016/`](../../SOP/Deep-Learning-2016/README.md)
- Plan for this package: [`plans/Deep-Learning-2016/README.md`](../../plans/Deep-Learning-2016/README.md)
