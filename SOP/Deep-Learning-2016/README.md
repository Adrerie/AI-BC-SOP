# SOP — *Deep Learning* (Goodfellow, Bengio & Courville, 2016)

Reusable research procedures reconstructed **by research function** from the 2016 *Deep Learning*
monograph. Nine SOPs. None is a chapter summary: each answers a question a researcher has to settle
before moving on, and Chapter 11's practical methodology is distributed across them rather than
copied.

Source record and citation convention:
[`Validation/Deep-Learning-2016/SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md).
Reconstruction decisions, the theory-only register and the historical-boundary register:
[`Validation/Deep-Learning-2016/concept_reconstruction.md`](../../Validation/Deep-Learning-2016/concept_reconstruction.md).

## Workflow order

The book's design loop (§11, p. 436) is: fix the metric → build an end-to-end baseline → locate the
bottleneck → make incremental changes. The SOPs follow that loop.

```text
SOP-DL-01  define        what am I predicting, on what metric, with what output parameterization?
    ↓
SOP-DL-07  design        which inductive bias does the data license?
SOP-DL-08  leverage      what should be shared across tasks, domains, labels, layers?
    ↓
SOP-DL-02  diagnose      underfitting or overfitting — which capacity knob moves?
    ↓
SOP-DL-03  regularize    which mechanism fits the failure and the data?
SOP-DL-04  optimize      training will not descend — verify objective → symptom → probe → repair → rerun → report
    ↓
SOP-DL-05  select        how do I search and split so the comparison is resolvable?
SOP-DL-09  evaluate      how do I compare generative models honestly?

SOP-DL-06  localize      ← runs FIRST whenever a number is surprising, and re-runs at every stage
```

Two dependency rules the book forces rather than we invented:

- `SOP-DL-06` precedes `SOP-DL-02` whenever training or test error is surprising. A mis-measured
  test error, a model reloaded incorrectly, or train/test preprocessing mismatch all masquerade as
  overfitting (§11.5, p. 451).
- `SOP-DL-01` precedes `SOP-DL-05`. The error metric guides all subsequent work; without a fixed
  target there is no way to tell whether a hyperparameter change helped (§11.1, p. 437).

## Index

| ID | Stage | SOP | Question it settles | Primary book material |
| --- | --- | --- | --- | --- |
| `SOP-DL-01` | define | [Specify the task, output distribution and cost](SOP-DL-01-specify-task-output-and-cost.md) | What is predicted, measured against what, with which output unit and cost? | §5.1, §6.2.1, §6.2.2, §5.10, §11.1, §11.6 |
| `SOP-DL-02` | diagnose | [Diagnose the fitting regime and set effective capacity](SOP-DL-02-diagnose-fitting-regime-and-capacity.md) | Underfitting or overfitting, and is more data the right answer? | §5.2, §11.2, §11.3, §11.4.1 |
| `SOP-DL-03` | regularize | [Select regularization](SOP-DL-03-select-regularization.md) | Which mechanism fits this failure mode and this dataset? | §5.2.2, §7.1–7.5, §7.8–7.14 |
| `SOP-DL-04` | optimize | [Diagnose optimization failure](SOP-DL-04-diagnose-optimization-failure.md) | Training will not descend — verify objective → inspect symptom → probe → minimal repair → rerun → report | §8.1–8.7, §10.11, §4.1–4.4 |
| `SOP-DL-05` | select | [Run model selection and hyperparameter search](SOP-DL-05-run-model-selection-and-hyperparameter-search.md) | Grid, random or model-based — and can the split resolve the difference? | §5.3, §5.3.1, §11.4 |
| `SOP-DL-06` | localize | [Debug a deep-learning experiment](SOP-DL-06-debug-deep-learning-experiment.md) | Is this a real result or an implementation bug? | §11.5, §4.1, §8.4 |
| `SOP-DL-07` | design | [Choose and test an inductive bias](SOP-DL-07-choose-and-test-inductive-bias.md) | Which prior does the data license, what does it buy, how would it break? | §6.4.2, §9, §10 |
| `SOP-DL-08` | leverage | [Decide what to share](SOP-DL-08-decide-what-to-share.md) | Should parameters be shared across tasks, domains, labeled/unlabeled data or layers? | §7.6, §7.7, §7.9, §13.5, §14, §15 |
| `SOP-DL-09` | evaluate | [Compare generative models](SOP-DL-09-compare-generative-models.md) | Are the two numbers commensurable, and does likelihood track what we want? | §17, §18, §19.4, §20.11, §20.14 |

Each SOP carries the six parts the repository requires — purpose/scope, inputs and assumptions,
procedure, important failure modes, outputs and reporting, source traceability — plus a
**Historical boundary** note stating which of its content is a 2016 default rather than a current
rule.

## Standing rules for this package

1. **Every step points at a section.** No SOP step is included unless a section of the book licenses
   it. Where a claim rests on a displayed equation that this e-copy stores as an image, the SOP says
   so in a *Formula caveat* block and cites the surrounding prose instead.
2. **No invented thresholds.** Where the book gives no number, the SOP describes the direction of the
   effect and leaves the magnitude to be measured. It does not supply a plausible-looking constant.
3. **Historical means historical.** Era defaults — the §11.2 baseline recipe, greedy layer-wise
   pretraining, specific dropout retentions and initialization scales, §12.1 systems practice — are
   labeled as such with their source, and are never promoted to current best practice.
4. **No post-2016 material in the 2016 procedure.** Nothing in the 2016 text of these SOPs introduces
   Transformers, modern optimizers or schedules, scaling laws, or later evaluation metrics. See
   `concept_reconstruction.md` §5.4. Modern material enters **only** inside blocks explicitly marked
   *Modern update (2017–2026)*, each carrying its own source line and a pointer to the delta record —
   see rule 7.
5. **Function-shaped, not chapter-shaped.** If a chapter produced no reusable decision procedure it
   is recorded as theory-only in `concept_reconstruction.md` §4 and has no SOP.
6. **Decision path in the SOP, inventory in the reconstruction record.** An SOP keeps the executable
   branch structure and the caveat that changes a decision. Catalog-style method inventories, historical
   menus, long derivations and era-specific recipes live in
   `concept_reconstruction.md` §4.1 — (a) optimization, (b) regularization, (c) sharing and
   representation, (d) generative evaluation — and the SOP points at them instead of restating them.
7. **Modern updates are marked, sourced and additive.** *(added by the 2017–2026 update lineage)* A
   modern block is a blockquote opened by **Modern update (2017–2026)** and closed by a source line naming
   its `delta_map.md` row and its source keys. It **annotates** 2016 text; it never rewrites it, and no
   2016 citation was altered to accommodate one. Three further limits apply: no modern block may supply a
   threshold its source does not state (rule 2 applies unchanged); no modern block may create an
   architecture entry, a variant catalogue or a family ranking; and where a capability is already owned by
   the Trustworthy-ML package, the block cross-links instead of restating a procedure. Method-specific,
   weakly supported or unsettled material is **not** imported at all — it stays in `delta_map.md`.

Seven SOPs carry modern-update blocks: `SOP-DL-02` (compute as a third axis; the U-curve's right branch;
the capacity-to-data ratio), `SOP-DL-03` (L2 versus decoupled weight decay under adaptive optimizers),
`SOP-DL-04` (the learning-rate-sensitivity assumption behind the repair ordering), `SOP-DL-05`
(conditional hyperparameters), `SOP-DL-07` (the attention prior and the pretraining-scale precondition on
model-class routing), `SOP-DL-08` (self-supervised pretraining; low-rank adaptation; zero-shot transfer)
and `SOP-DL-09` (family exactness status; flow matching; likelihood versus sample quality;
conditional-generation uses).

## Related

- Benchmark checks executed by these SOPs:
  [`Benchmark/Deep-Learning-2016/`](../../Benchmark/Deep-Learning-2016/README.md)
- Plan for this package: [`plans/Deep-Learning-2016/README.md`](../../plans/Deep-Learning-2016/README.md)
- Modern-update lineage — source record, delta judgements and the reasons items were declined:
  [`Validation/Deep-Learning-Modern-2017-2026/`](../../Validation/Deep-Learning-Modern-2017-2026/sources.md)
  and [`delta_map.md`](../../Validation/Deep-Learning-Modern-2017-2026/delta_map.md); plan at
  [`plans/Deep-Learning-Modern-2017-2026/README.md`](../../plans/Deep-Learning-Modern-2017-2026/README.md)
- Capabilities cross-linked rather than duplicated:
  [`SOP/Trustworthy-ML-2023/`](../Trustworthy-ML-2023/README.md)
