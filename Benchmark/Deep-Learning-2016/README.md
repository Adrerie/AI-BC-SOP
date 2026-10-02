# Benchmark — *Deep Learning* (Goodfellow, Bengio & Courville, 2016)

Benchmark checks (BCs) reconstructed **by evaluable claim** from the 2016 *Deep Learning* monograph.
Eleven BCs. Each exists because the book makes a concrete claim that a comparison could confirm or
falsify — not because a model family needed an entry.

Identifiers are stable, not a sequence: `BC-DL-04` was **withdrawn** and its number is not reused. The
reason and the retained historical record are in
[`concept_reconstruction.md`](../../Validation/Deep-Learning-2016/concept_reconstruction.md) §3.1 and §5.1.

Source record and citation convention:
[`Validation/Deep-Learning-2016/SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md).
Why these claims and not others, including the rejected candidates:
[`Validation/Deep-Learning-2016/concept_reconstruction.md`](../../Validation/Deep-Learning-2016/concept_reconstruction.md) §3.

## Index

| ID | Claim under test | Executed by | Primary book material |
| --- | --- | --- | --- |
| `BC-DL-01` | [Does the cost still teach the model when it is confidently wrong?](BC-DL-01-output-unit-loss-coupling.md) — the output-unit ↔ loss coupling, and the saturation failure it causes | `SOP-DL-01` | §6.2.1.1, §6.2.2.2 p. 209, §6.2.2.3 p. 211 |
| `BC-DL-02` | [Do the capacity and data-size curves behave as the fitting theory predicts?](BC-DL-02-capacity-and-data-size-curves.md) — the U-curve in capacity and the generalization-error curve in training-set size | `SOP-DL-02` | §5.2, §5.2.2, Fig. 5.3, Fig. 5.4, §11.3, §11.4.1 |
| `BC-DL-03` | [Do regularizers work through the mechanisms the book claims?](BC-DL-03-regularization-mechanisms.md) — mechanism-specific observables, with the two errors reported separately and neither deciding the arm | `SOP-DL-03` | §5.2.2, §7.1.1–7.1.2, §7.5.1, §7.8, §7.11, §7.12 |
| `BC-DL-05` | [Optimization diagnostic probe suite](BC-DL-05-optimization-diagnostic-probe-suite.md) — does each probe support or rule out what it claims, and does the remedy move the diagnosed quantity? | `SOP-DL-04` | §8.2.1–8.2.7, §8.4, §8.7.1, §10.11.1, §11.4.1 |
| `BC-DL-06` | [Long-range dependency: does the spectral account predict the learnable span?](BC-DL-06-long-range-dependency.md) — a quantitative prediction and the structural limit on fixing it | `SOP-DL-04`, `SOP-DL-07` | §8.2.5 pp. 310–311, §10.7, §10.9–10.11 |
| `BC-DL-07` | [Implementation-health instruments: is the number produced by the algorithm you think you ran?](BC-DL-07-implementation-health-instruments.md) — injected bugs must be caught by the book's diagnostics | `SOP-DL-06` | §11.5 pp. 450–453 |
| `BC-DL-08` | [Do the architectural priors hold, and does violating them cost what the book predicts?](BC-DL-08-inductive-bias-assumption-tests.md) — sparse interaction, sharing, equivariance, pooling, depth | `SOP-DL-07` | §9.2–9.5, §9.9 p. 383, §10.2, §10.10 |
| `BC-DL-09` | [Search sample-efficiency, and whether the validation material can resolve the difference](BC-DL-09-search-efficiency-and-resolvability.md) — random vs grid at matched budget, plus resolvability | `SOP-DL-05` | §11.4.3, §11.4.4, §5.3.1, §5.3.2 |
| `BC-DL-10` | [When does sharing pay?](BC-DL-10-sharing-gains-vs-labeled-data.md) — pretraining, transfer and unlabeled-data gains as a function of labeled-data size | `SOP-DL-08` | §7.6, §7.7, §15.1.1, §15.2 |
| `BC-DL-11` | [Generative-model comparison: is the measured quantity comparable, and does likelihood track sample quality?](BC-DL-11-generative-evaluation-integrity.md) — commensurability failure and reward hacking | `SOP-DL-09` | §20.14, §18.7.1, §18.7.2, §19.4.4, §17.3–17.5 |
| `BC-DL-12` | [Does a learned representation meet the criteria the book gives, each against its own appropriate control?](BC-DL-12-representation-quality.md) — PCA is the comparator only for the linear / undercomplete-autoencoder arms | `SOP-DL-08` | §14.1, §14.2, §14.5, §14.6, §14.7, §14.9, §13.5, §15.6 |

Each BC carries the six parts the repository requires — capability/failure under test, data and
comparison conditions, baselines, metrics, how to interpret failure, validity limits and source
traceability — plus a closing **Historical boundary** note.

## Standing rules for this package

1. **A model family is not a benchmark.** CNN, RNN, autoencoder, RBM, VAE and GAN have no BC of
   their own. They appear only where a distinct evaluable claim attaches — e.g. `BC-DL-08` tests the
   prior a convolutional network encodes, `BC-DL-11` tests whether generative-evaluation instruments
   agree.
2. **Every metric is a quantity a source names.** No score is introduced to fill a template field.
   Where the source states no threshold, the BC specifies an **ordering** comparison and says that the
   absolute value must come from the run. For metrics 1–9 of `BC-DL-11` and for every other BC the source
   is the 2016 book. The modern-update block `BC-DL-11` §4.M admits three further metrics on the same
   terms — each named by the anchor textbook and each carrying the failure modes that source states — and
   on no looser terms: see rule 7.
3. **A baseline is required, and it must fit the claim.** Each BC names the control condition that
   makes the claim falsifiable — a matched-capacity plain model, an unrelated-task control, an
   injected-bug control, a fresh-chain control, an untrained-spectrum control. Where a single linear
   control does not fit the claim, it is not used: `BC-DL-12` restricts PCA to the linear /
   undercomplete-autoencoder comparisons and gives every other criterion its own control.
4. **Probes support or rule out; they do not classify.** `BC-DL-05` scores elimination plus
   corroboration and reports which diagnoses remain live. No BC in this package claims to identify a
   single cause uniquely from a trace.
5. **Validity limits are stated, not implied.** Each BC §6 records what the result cannot support —
   dataset-bound conclusions, estimator bias direction, the unknowability of MCMC mixing, and the
   direction-dependent interpretation of estimate-versus-bound likelihood comparisons.
6. **Historical means historical.** Era benchmarks (MNIST, CIFAR-10, SVHN, ImageNet, street-view
   house numbers) are used as carriers of a comparison condition and labeled as such; §5.3.2's
   benchmark-staleness argument is part of `BC-DL-09`, not an afterthought. No post-2016 metric appears in
   the 2016 text of any BC; the three admitted by rule 7 live only inside `BC-DL-11` §4.M. Perplexity is
   not used as a metric anywhere in this package, because no source in either lineage names it as a
   generative-model metric.
7. **Modern updates are marked, sourced and additive.** *(added by the 2017–2026 update lineage)* A modern
   block is a blockquote or clearly delimited subsection opened by **Modern update (2017–2026)** and closed
   by a source line naming its `delta_map.md` row and its source keys. It annotates the 2016 text and never
   rewrites it; no 2016 citation was altered. Four further limits apply, and they are what keep rule 1 and
   rule 2 in force rather than suspending them:
   - **No new arm, and no new BC.** The four BCs carrying modern blocks gained an added comparison
     *condition* on an existing arm (`BC-DL-08` arms a/b), added interpretation rules (`BC-DL-02`,
     `BC-DL-08`, `BC-DL-11`), an added validity limit (`BC-DL-02`, `BC-DL-06`) and an added metric block
     (`BC-DL-11` §4.M). No claim under test was changed.
   - **Still no family ranking.** `BC-DL-11` §5 records the modern instance of a family ranking that its
     own source states *in terms of one metric* precisely as evidence for the failure mode the 2016 text
     already named. This package does not rank families, and rule 1 stands.
   - **Still no invented threshold.** The three §4.M metrics have no source-stated acceptable value, so
     they enter as ordering comparisons only, exactly like metrics 1–9.
   - **Unsettled material is not imported.** Contested quantities — notably the compute-allocation
     exponents, where the two sources in this lineage's list disagree — are recorded in `delta_map.md` and
     in no BC.

Four BCs carry modern-update blocks: `BC-DL-02` (second descent, the capacity-to-data ratio,
overparameterization), `BC-DL-06` (the structural limit is architecture-bound), `BC-DL-08`
(given-versus-learned equivariance; the contested depth claim) and `BC-DL-11` (the §4.M metric block;
likelihood versus sample quality; metric-indexed family rankings; a bound exceeding an exact value).

## Rejected and withdrawn candidates

Recorded so the absence is a decision rather than an oversight — full reasoning in
`concept_reconstruction.md` §3.1:

- **`BC-DL-04` adversarial linearity / the sign-of-gradient (FGSM-style) construction — withdrawn.**
  The book's demonstration is a single 2016-era figure with no perturbation budget, no norm convention
  and no effect size, so running it as a BC would require inventing those numbers. Retained as a 2016
  historical observation in `concept_reconstruction.md` §5.1, with brief context in `SOP-DL-03` §3.3.
- **Unique classification of an optimization pathology from its trace — reframed**, not dropped; it is
  now the probe suite in `BC-DL-05`.
- **Classifying a regularizer by whether training error decreased** — removed from `BC-DL-03`. The two
  errors are reported separately, and a joint improvement is flagged for capacity/optimization checking
  rather than used to reclassify the lever.
- Architecture-family comparisons as such.
- Optimizer leaderboards; §8.5.4 explicitly reports no consensus, so a ranking would be an artifact
  of the problem set. *Reaffirmed by the modern update:* the 2017–2026 lineage records that the
  learning-rate-sensitivity assumption behind the 2016 ordering no longer holds as stated
  (`SOP-DL-04` §3.4 step 6) and produces **no** ranking.
- Generative sample-quality scores the book does not define. *Scoped by the modern update:* three later
  scores are now admitted in `BC-DL-11` §4.M because the anchor textbook defines them **and** states each
  one's failure modes. A score no source defines is still rejected; a score a source defines but that is
  reported without its failure modes is out of specification.
- Depth-vs-width superiority; §6.4.2's 20M→60M observation is matched-parameter and
  experiment-specific, so it is a design argument in `SOP-DL-07`, not a BC. *Confirmed open by the modern
  update:* the anchor textbook's own verdict is that depth appears critical but that "there is no
  definitive explanation for why", and it records substantial counter-evidence (`BC-DL-08` §5). The
  rejection stands.
- **A compute-allocation benchmark — rejected by the modern update.** The two sources in this lineage's
  list disagree on the allocation exponents and both self-report extrapolation uncertainty, so such a
  benchmark would test a contested quantity rather than a source-named one. The *workflow* consequence —
  declare the budget and the allocation assumption — is carried in `SOP-DL-02` §3.5; the numbers are not
  carried anywhere. See `delta_map.md` §1.2.
- **A test-time-compute SOP or BC — rejected by the modern update.** A reusable protocol can be stated and
  is written out in `delta_map.md` §5.1, but it rests on a single dated frontier result that self-reports
  small gains on hard problems and whose evaluation scope is only partially verifiable. Recorded with an
  explicit promotion trigger rather than left as an omission.

## Related

- Procedures that execute these checks:
  [`SOP/Deep-Learning-2016/`](../../SOP/Deep-Learning-2016/README.md)
- Plan for this package: [`plans/Deep-Learning-2016/README.md`](../../plans/Deep-Learning-2016/README.md)
- Modern-update lineage — source record, delta judgements and the reasons items were declined:
  [`Validation/Deep-Learning-Modern-2017-2026/sources.md`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md)
  and [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md); plan at
  [`plans/Deep-Learning-Modern-2017-2026/README.md`](../../plans/Deep-Learning-Modern-2017-2026/README.md)
- Capabilities cross-linked rather than duplicated — evaluation-integrity audit
  ([`BM-08`](../Trustworthy-ML-2023/BM-08-evaluation-integrity-audit.md)), distribution shift
  ([`BM-01`](../Trustworthy-ML-2023/BM-01-distribution-shift-generalization.md)), spurious-cue dependence
  ([`BM-02`](../Trustworthy-ML-2023/BM-02-spurious-cue-dependence.md)), adversarial robustness
  ([`BM-05`](../Trustworthy-ML-2023/BM-05-adversarial-robustness.md))
