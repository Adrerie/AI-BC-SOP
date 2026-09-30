# Sources — Deep Learning modern update (2017–2026)

Source-audit record for the modern-update lineage. Read on 2026-09-30. Nothing in this file was inferred
from a title: every row states what was actually opened, and anything that could not be opened is marked
`PARTIAL` or `NO` with the routes that were tried.

This file records **access and citation granularity only**. The substantive decisions — which deltas were
accepted, which were rejected, which stay here as record — are in [`delta_map.md`](delta_map.md).

## 0. Lineage and relationship to the 2016 package

The 2016 baseline is the accepted package on this branch:
[`SOP/Deep-Learning-2016/`](../../SOP/Deep-Learning-2016/README.md) (9 SOPs),
[`Benchmark/Deep-Learning-2016/`](../../Benchmark/Deep-Learning-2016/README.md) (11 BCs), and
[`Validation/Deep-Learning-2016/`](../Deep-Learning-2016/SOURCE.md) — whose `SOURCE.md` records the local
Simplified Chinese copy of Goodfellow, Bengio & Courville and whose `concept_reconstruction.md` carries the
theory-only and historical-boundary registers.

That package was deliberately closed against post-2016 material: its standing rule was that nothing
post-2016 is introduced anywhere in it. This lineage is the sanctioned place for that material. The 2016
package's own text is **not** rewritten; where a modern delta lands in a 2016 artifact it is added as a
clearly marked modern-update note with provenance pointing back to this file and to `delta_map.md`.

The sibling lineage [`Validation/Trustworthy-ML-2023/`](../Trustworthy-ML-2023/SOURCE.md) and
[`Validation/Trustworthy-ML-Official-Updates-2024-2026/`](../Trustworthy-ML-Official-Updates-2024-2026/source_inventory.md)
own adversarial robustness under a declared threat model, distribution shift, spurious-cue dependence,
confidence truthfulness, explanation quality, selective prediction, evaluation-integrity auditing and
disclosure. Where a modern deep-learning delta touches one of those capabilities, this lineage
**cross-links** rather than restates. The overlaps actually identified are listed in `delta_map.md` §4.

## 1. Anchor textbooks

| ID | Work | Access | What can be cited |
| --- | --- | --- | --- |
| `UDL` | Simon J. D. Prince, *Understanding Deep Learning*, MIT Press | **FULL** — complete text layer, all 541 PDF pages | Chapter, section and printed-folio level |
| `DLFC` | Christopher M. Bishop & Hugh Bishop, *Deep Learning: Foundations and Concepts*, Springer 2024 | **METADATA ONLY** — paywalled; full text not read | Book-level title/authorship/DOI/ISBN and the 19 public chapter titles. **No section, page or claim may be cited to this work** |

### 1.1 `UDL` — Prince, *Understanding Deep Learning*

| Field | Value |
| --- | --- |
| Work | *Understanding Deep Learning*, Simon J. D. Prince |
| Publisher | Copyright licensed exclusively to The MIT Press, which **released the final version to the public in December 2023** |
| Artifact read | `UnderstandingDeepLearning_02_09_26_C.pdf`, title-page date **February 8, 2026** |
| Distribution | Official GitHub release `v5.0.3` of `udlbook/udlbook`, published 2026-02-09; canonical site `http://udlbook.com` |
| Size / SHA-256 | 22,344,992 bytes / `f8237d393163900fa8e43210e680a3f987b45ccac7750b372e156fae3df0bf32` |
| Container | PDF 1.5, `LaTeX with hyperref` / `xdvipdfmx`, creation date 2026-02-08 |
| Extent | 541 PDF pages; 181-entry PDF outline; 21 numbered content chapters + 4 appendices + bibliography + index |
| License | **Creative Commons CC-BY-NC-ND** |
| Local copy | `D:\tmp\dlmodern\udlbook.pdf` (scratch, outside the repository; not committed) |

**Draft-status caveat, and why it matters for citation.** Every page footer of this artifact reads
*"Draft: please send errata to udlbookmail@gmail.com"*, and the title page is dated 2026-02-08 while the
MIT Press public release is dated December 2023. The artifact read here is therefore a **post-publication
author revision**, not the printed edition. Citations in this lineage are to the draft's own pagination and
are labelled as such; a reader holding the MIT Press print edition should locate material by chapter and
section number, which are stable, and treat the folio as indicative.

**Pagination convention.** This book *does* carry printed folios, unlike the 2016 Chinese e-copy. The offset
was measured, not assumed: PDF p. 222 prints folio 208, PDF p. 364 prints 350, PDF p. 92 prints 78. Hence

```text
printed folio = PDF page − 14
```

Chapter-opening pages carry no folio. Citations in this lineage use `UDL §section, fol. N`; the PDF page is
given alongside where a claim is load-bearing for an artifact.

**Chapter map (book numbering → PDF pages → folios).** Verified by reading each chapter-opening page header,
not inferred from the outline order.

| Ch | Title | PDF | Folio | Read for this lineage |
| --- | --- | --- | --- | --- |
| 1 | Introduction | 15–30 | 1–16 | yes |
| 2 | Supervised learning | 31–38 | 17–24 | — |
| 3 | Shallow neural networks | 39–54 | 25–40 | — |
| 4 | Deep neural networks | 55–69 | 41–55 | — |
| 5 | Loss functions | 70–90 | 56–76 | — |
| 6 | Fitting models | 91–109 | 77–95 | **yes** (gradient descent, SGD, momentum, Adam §6.4, training-algorithm hyperparameters §6.5) |
| 7 | Gradients and initialization | 110–131 | 96–117 | **yes** (§7.5 parameter initialization) |
| 8 | Measuring performance | 132–151 | 118–137 | **yes** (§8.3 sources/reducing error, §8.4 double descent, §8.5 choosing hyperparameters) |
| 9 | Regularization | 152–174 | 138–160 | **yes** (§9.1 explicit incl. AdamW note, §9.2 implicit, §9.3.1 early stopping, §9.3.2 ensembling, §9.3.3 dropout, §9.3.6 transfer/multi-task, §9.3.7 self-supervised, §9.3.8 augmentation) |
| 10 | Convolutional networks | 175–199 | 161–185 | **yes** (weight-decay and overparameterization mentions) |
| 11 | Residual networks | 200–220 | 186–206 | **yes** (chapter summary: residual + batch-norm interaction) |
| 12 | Transformers | 221–253 | 207–239 | **yes** (§12.1 motivation, §12.2 dot-product self-attention, §12.9 long sequences, §12.10 images incl. ImageGPT, ViT, multi-scale) |
| 13 | Graph neural networks | 254–282 | 240–268 | — |
| 14 | Unsupervised learning | 283–289 | 269–275 | **yes, in full** (§14.1 taxonomy, §14.2 what makes a good generative model, §14.3 quantifying performance) |
| 15 | Generative adversarial networks | 290–317 | 276–303 | — |
| 16 | Normalizing flows | 318–340 | 304–326 | **yes** (§16.5.1 exact-likelihood claim and its footnote; invertibility constraint) |
| 17 | Variational autoencoders | 341–362 | 327–348 | **yes** (ELBO usage) |
| 18 | Diffusion models | 363–387 | 349–373 | **yes** (§18.1 overview, §18.2 forward process, §18.4 training, §18.4.1 ELBO, §18.6 conditioning incl. DrawBench, Notes) |
| 19 | Reinforcement learning | 388–415 | 374–401 | — |
| 20 | Why does deep learning work? | 416–434 | 402–420 | **yes, in full** (§20.1 the case against deep learning, §20.2 factors influencing fitting, §20.3 loss-function properties, §20.4 factors determining generalization, §20.5 do we need so many parameters, §20.6 do networks have to be deep) |
| 21 | Deep learning and ethics | 435–450 | 421–436 | — |
| A–D | Notation, Mathematics, Probability, Bibliography | 451–526 | 437–512 | bibliography consulted for cited-work names only |

**Official supplements.** The `udlbook/udlbook` repository also publishes `UDL_Errata.pdf`,
`UDL_Answer_Booklet_Students.pdf`, `Notebooks/`, `Slides/`, `Blogs/` and `UDL_Equations.tex`. None was
opened for this lineage; nothing is cited to them. Prince's text refers to numbered notebooks (e.g.
"Notebook 8.3 Double descent", "Notebook 6.5 Adam") — those references are recorded as pointers only, and no
notebook content is cited.

**What `UDL` does *not* cover — verified by word-boundary term scan across the thirteen extracted
chapters.** Zero occurrences of: `scaling law`, `test-time`, `flow matching`, `rectified flow`,
`masked autoencoder`, `MAE`, `SimCLR`, `LoRA`, `FID` (as a token). Consequently four of the plan's five
update areas cannot be anchored in this book alone:

- **Scale/compute allocation laws** — not in `UDL`; landmark papers only.
- **Inference-time compute** — not in `UDL`; landmark paper only.
- **Flow matching / rectified flow** — not in `UDL` (its generative chapters are GAN, flows, VAE, diffusion);
  landmark paper only.
- **Parameter-efficient adaptation (LoRA)** — not in `UDL`; landmark paper only.
- **Contrastive and masked self-supervised learning** are present as *families* (`UDL` §9.3.7 names generative
  and contrastive self-supervision) but the specific methods are not; landmark papers supply those.

Fréchet-based sample-quality metrics *are* covered, under the spelled-out name rather than the acronym:
"Fréchet" appears in ch. 14 (6×) and ch. 18 (1×), and "Inception score" in ch. 14 (6×).

### 1.2 `DLFC` — Bishop & Bishop, *Deep Learning: Foundations and Concepts*

| Field | Value |
| --- | --- |
| Work | *Deep Learning* (series subtitle *Foundations and Concepts*), Christopher M. Bishop and Hugh Bishop |
| Publisher / year | Springer Nature Switzerland AG, copyright year 2024 |
| DOI | `10.1007/978-3-031-45468-4` |
| ISBNs | Hardcover 978-3-031-45467-7; eBook 978-3-031-45468-4 |
| Rights | "The Editor(s) (if applicable) and The Author(s), under exclusive license to Springer Nature Switzerland AG 2024" |
| Access | **NO** — the Springer page reports `"Open Access":"N"`, `"hasAccess":"N"`, `"Access Type":"no-access"` |
| Front matter | pages i–xx |

**Routes tried.** `https://link.springer.com/book/10.1007/978-3-031-45468-4` (HTTP 200 with a
`cookies_not_supported` query parameter; page parsed for embedded JSON-LD metadata);
`https://doi.org/10.1007/978-3-031-45468-4` (302 → the same Springer host);
`https://link.springer.com/chapter/10.1007/978-3-031-45468-4_12` (HTTP 200, but the rendered page exposes
only purchase/subscribe furniture — no abstract, no section headings, no page range). No local copy of this
work exists in the workspace book folder, which contains only the 2016 Chinese flower book, the 2023
Trustworthy ML book and a Japanese NLP text. Nothing was downloaded to bypass the paywall and no
third-party copy was sought.

**Public chapter list, which is the only citable content.** 1 The Deep Learning Revolution · 2 Probabilities ·
3 Standard Distributions · 4 Single-layer Networks: Regression · 5 Single-layer Networks: Classification ·
6 Deep Neural Networks · 7 Gradient Descent · 8 Backpropagation · 9 Regularization · 10 Convolutional
Networks · 11 Structured Distributions · 12 Transformers · 13 Graph Neural Networks · 14 Sampling ·
15 Discrete Latent Variables · 16 Continuous Latent Variables · 17 Generative Adversarial Networks ·
18 Normalizing Flows · 19 Autoencoders. No chapter numbered 20 or higher exists.

**Consequence for this lineage, stated plainly.** The plan names this work as a stable anchor, but its full
text is not readable here. **No delta in `delta_map.md` is sourced to `DLFC`.** The book is recorded so that
its scope is on file and so that a future cycle with a legitimate copy can check whether the accepted deltas
are consistent with it. Its public chapter list is used for exactly one purpose: confirming that the two
anchors' topical coverage of transformers, flows, GANs, autoencoders and latent variables overlaps, which
supports treating `UDL` as sufficient for those areas rather than as a partial substitute.

## 2. Landmark papers

Scoped by the plan to structural deltas the anchors do not cover well. The list was **not** broadened.

### 2.1 Registry — the version actually opened

Every row records the arXiv identifier, the **specific version whose text was read**, the version's
submission date, and the venue **as stated in that arXiv record's comments field**. A venue that is
common knowledge but absent from the arXiv record is marked *not stated on arXiv* and is never used
as a citation element in this lineage. Access: **FULL** = abstract page plus full text (arXiv HTML or
ar5iv rendering) read; **ABS** = abstract page only.

| Key | Work | arXiv | Version opened | Date | Venue per arXiv comments | Access |
| --- | --- | --- | --- | --- | --- | --- |
| `ATTN` | Vaswani et al., *Attention Is All You Need* | 1706.03762 | abs page (v1–v7 listed); full text via ar5iv (version served not stated) | v1 2017-06-12, v5 2017-12-06, v7 2023-08-02 | **not stated** — comments read "15 pages, 5 figures" | FULL |
| `VIT` | Dosovitskiy et al., *An Image is Worth 16x16 Words* | 2010.11929 | **v2** | v1 2020-10-22, v2 2021-06-03 | "ICLR camera-ready version with 2 small modifications" (year not printed in the comment) | FULL |
| `ADAMW` | Loshchilov & Hutter, *Decoupled Weight Decay Regularization* | 1711.05101 | **v3** | v1 2017-11-14, v2 2018-02-14, v3 2019-01-04 | "Published as a conference paper at ICLR 2019" | FULL |
| `SCALE` | Kaplan et al., *Scaling Laws for Neural Language Models* | 2001.08361 | **v1** | 2020-01-23 | **not stated** — page/figure counts only | FULL |
| `CHINCHILLA` | Hoffmann et al., *Training Compute-Optimal Large Language Models* | 2203.15556 | **v1** | 2022-03-29 | **not stated** | FULL |
| `SIMCLR` | Chen et al., *A Simple Framework for Contrastive Learning of Visual Representations* | 2002.05709 | **v3** | v1 2020-02-13, v3 2020-07-01 | "ICML'2020" | FULL |
| `CLIP` | Radford et al., *Learning Transferable Visual Models From Natural Language Supervision* | 2103.00020 | **v1** (only version) | 2021-02-26 | **not stated** | FULL |
| `MAE` | He et al., *Masked Autoencoders Are Scalable Vision Learners* | 2111.06377 | **v3** | v1 2021-11-11, v3 2021-12-19 | "Tech report" | FULL |
| `DDPM` | Ho et al., *Denoising Diffusion Probabilistic Models* | 2006.11239 | **v2** | v1 2020-06-19, v2 2020-12-16 | **not stated** | FULL |
| `FM` | Lipman et al., *Flow Matching for Generative Modeling* | 2210.02747 | **v2** | v1 2022-10-06, v2 2023-02-08 | **not stated** | FULL |
| `RF` | Liu et al., *Flow Straight and Fast* | 2209.03003 | **v1** | 2022-09-07 | **not stated** | FULL |
| `TTC` | Snell, Lee, Xu & Kumar, *Scaling LLM Test-Time Compute Optimally…* | 2408.03314 | **v1** (only version) | 2024-08-06 | **not stated** | FULL |
| `LORA` | Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models* | 2106.09685 | **v2** | v1 2021-06-17, v2 2021-10-16 | **not stated** | FULL |

`RF` is listed separately from `FM` because it is a distinct arXiv record; no concurrency or
derivation relationship between the two is asserted anywhere in this lineage (see §2.4).

### 2.2 Claims each paper is used for

Only the following structural claims are carried into `delta_map.md`. Everything else in these papers
is method-specific and stays out of the artifacts.

- `ATTN` — a self-attention layer connects all positions with a constant number of sequentially
  executed operations, and self-attention is faster than recurrent layers when the sequence length is
  smaller than the representation dimensionality; shorter paths between positions make long-range
  dependencies easier to learn. Recurrence is not a requirement for sequence modeling.
- `VIT` — the inductive-bias conclusion is **conditional**, not "ViT beats CNNs": pre-trained on large
  data and transferred to mid-sized or small benchmarks, ViT attains excellent results with
  substantially fewer computational resources; trained only on ImageNet-scale data it self-reports
  accuracies **below** comparable ResNets.
- `ADAMW` — L2 regularization and weight decay are equivalent for standard SGD when rescaled by the
  learning rate, but **not** for adaptive gradient algorithms, because with L2 both the loss gradient
  and the λ·w gradient are normalized by their typical summed magnitudes, so weights with large
  historic gradient magnitudes are regularized less. Decoupling regularizes all weights at the same
  rate λ and decouples the optimal weight-decay setting from the learning-rate setting. The paper
  supplies a `SetScheduleMultiplier(t)` factor η_t for scheduling both, and an appendix-B batch-budget
  normalization λ = λ_norm·√(b/(N·T)) that it itself calls "merely one possibility informed by few
  experiments."
- `SCALE` — loss follows power laws in N, D and C individually, each law holding only under stated
  conditions (L(N) requires converged training on sufficiently large datasets; L(D) assumes large
  models with limited data and early stopping; L(C) requires an optimally sized model, sufficiently
  large dataset and sufficiently small batch size); architecture details such as width vs. depth have
  minimal effect within a wide range. Its allocation rule is that N grows faster than D with compute.
  The paper states it has "no solid theoretical understanding" and that trends must eventually level
  off.
- `CHINCHILLA` — explicitly revises `SCALE`: model size and training tokens should be scaled **in equal
  proportions**, and it attributes the discrepancy partly to `SCALE`'s use of a fixed number of
  training tokens and learning-rate schedule for all models. It self-reports significant uncertainty
  in extrapolating many orders of magnitude and only two comparable large-scale training runs.
- `SIMCLR` — composition of multiple augmentations is crucial; cropping must be composed with color
  distortion or the model shortcuts through color statistics. A nonlinear projection head improves the
  quality of the learned representation, and the representation **before** the head is what transfers.
  Contrastive learning benefits from larger batch sizes and more training steps than supervised
  learning (batches 256–8192 reported; best models trained for 1000 epochs).
- `CLIP` — zero-shot transfer from natural-language supervision, with a text encoder acting as a
  hypernetwork generating linear-classifier weights; its limitations section is quoted verbatim in
  §2.3 and is the load-bearing part for evaluation-integrity deltas.
- `MAE` — masking a high proportion of the input (e.g. 75%) yields a nontrivial self-supervisory task;
  an asymmetric encoder–decoder that shows the encoder only visible patches and uses a lightweight
  decoder only during pretraining gives 3× or more training acceleration. Rationale: images have heavy
  spatial redundancy, so sparse random masking suffices.
- `DDPM` — trained on a weighted variational bound connected to denoising score matching; the
  simplified loss `L_simple` drops the variational weighting, down-weighting hard small-t terms, and
  produces the best FID despite deviating from the bound. Its likelihood-vs-sample-quality concession
  is quoted in §2.3.
- `FM` — a simulation-free training approach for continuous normalizing flows based on regressing
  vector fields of fixed conditional probability paths. It **generalizes rather than replaces**
  diffusion: it subsumes existing diffusion paths as specific instances, and FM instantiated with
  diffusion paths is described as a more robust and stable alternative for training diffusion models.
  It reports bits/dim **and** FID jointly and makes no claim that likelihood is an inappropriate
  metric.
- `TTC` — in a FLOPs-matched evaluation, test-time compute can outperform a 14× larger model **on
  problems where a smaller base model attains somewhat non-trivial success rates**; effectiveness
  varies critically with prompt difficulty; test-time and pretraining compute are **not** 1-to-1
  exchangeable; assessing difficulty itself requires non-trivial test-time compute.
- `LORA` — low-rank updates applied to attention weight matrices, adapting both W_q and W_v under a
  fixed parameter budget; no additional inference latency because W = W₀ + BA is materialized before
  deployment; many tasks served from one frozen base by swapping LoRA weights; quality claimed as
  on-par or better than full fine-tuning on the models tested.

### 2.3 Verbatim limitation quotes retained

These are kept word-for-word because they are the evidence that stops a delta from being
over-claimed. They are the only quotes reproduced at length.

`CLIP` (limitations section): "zero-shot CLIP is quite weak on several specialized, complex, or
abstract tasks"; "CLIP also struggles with more abstract and systematic tasks such as counting the
number of objects in an image"; "zero-shot CLIP still generalizes poorly to data that is truly
out-of-distribution for it"; "CLIP is still limited to choosing from only those concepts in a given
zero-shot classifier"; and, on its own evaluation practice, using benchmark validation sets to select
prompts "is unrealistic for true zero-shot scenarios."

`DDPM`: "Despite their sample quality, our models do not have competitive log likelihoods compared to
other likelihood-based models"; "More than half of the lossless codelength describes imperceptible
distortions."

`ADAMW` (§3 justification): the Bayesian-filtering argument "does not directly apply to practical
adaptive gradient algorithms."

### 2.4 Unverified items — do not cite

Recorded so their absence downstream is a decision, not an oversight.

- A `CLIP` sentence asserting that zero-shot evaluation amounts to "evaluating on a different task
  specification" was **not found**. It is a hypothesis, not a quote.
- The phrase "task-dependent" attributed to `SIMCLR` was **not verified verbatim**; cite its framing
  questions instead.
- The `DDPM` results table's index number was not established by the fetch; the bits/dim figures
  (Gated PixelCNN 3.03, DDPM full bound ≤3.70, `L_simple` ≤3.75 on CIFAR-10 test) are usable, the
  table number is not.
- `MAE`'s analogy to a language-model "vocabulary" is paraphrase, not verbatim text.
- No concurrency or derivation relationship between `RF` and `FM` was verified; the two are cited as
  distinct works.
- `ADAMW`'s specific "multiply the decay by η_t/η_init" formulation was **not located verbatim**; cite
  the `SetScheduleMultiplier` η_t mechanism and Appendix B.1 instead.
- `TTC`'s full benchmark list and exact base-model naming are only partially verified; the FLOPs-matched
  framing and the difficulty condition are verified, so only those are used.
- `VIT`'s exact ImageNet top-1 decimal was not cross-checked against the camera-ready tables and is not
  printed anywhere in this lineage.
- Which version ar5iv served for `ATTN` is unknown; the claims carried are ones present in the abstract
  and §4, which are stable across versions.
- No paper's publication venue is cited unless it appears in that arXiv record's comments field. In
  particular `ATTN`'s NeurIPS 2017 and `DDPM`'s NeurIPS 2020 status are **not** arXiv-stated and are
  not used.

### 2.5 Coverage gap that forces the paper list

A word-boundary scan across the thirteen `UDL` chapters read (see §3) returns **zero** occurrences of
`scaling law`, `test-time`, `flow matching`, `rectified flow`, `masked autoencoder`, `MAE`, `SimCLR`,
`LoRA`, and `FID` as a token. Four of the plan's five update areas therefore cannot be anchored in
`UDL` alone, which is precisely why the plan names landmark papers. The reverse holds for the fifth:
`UDL` covers transformers, generative-model evaluation metrics, regularization/AdamW and
overparameterization directly, so papers are used there only to date a structural claim the anchor
already states.

## 3. Reading and extraction method

- `UDL` was read from the official release PDF with PyMuPDF (`fitz`) text extraction. Thirteen chapters
  relevant to the five update areas were exported to scratch text with `[[pN]]` PDF-page markers
  (`D:\tmp\dlmodern\body\`), then read. **The PDF and the extracted text are not committed**; only extracted
  facts and short quoted phrases are.
- Unlike the 2016 Chinese e-copy, `UDL`'s display equations survive text extraction as glyph runs (they are
  LaTeX-set, not images), so equations could be read. They are nevertheless **not** reproduced in artifacts;
  where a claim rests on an equation, the artifact cites the section and states the relationship in prose.
- Springer pages were fetched with a browser user agent and parsed for embedded JSON-LD rather than rendered
  HTML, because the rendered chapter page carries no scholarly content.
- Landmark papers were read from arXiv abstract and HTML pages; version strings and dates were taken from the
  pages actually opened. Where a full text could not be opened, the row says so and only the abstract-level
  claim is used.
- Term-coverage claims about `UDL` (the zero-occurrence list in §1.1) were produced by a case-insensitive
  **word-boundary** scan over the thirteen extracted chapters. An earlier substring scan produced false
  positives (`LoRA` inside "exp**lora**tion", `CLIP` inside "**clip**s", `FID` inside "overcon**fid**ent")
  and was discarded; the boundary scan is the one reported.

## 4. Boundaries on what this lineage may claim

1. **No delta may be sourced to a work that was not opened.** `DLFC` contributes nothing beyond its public
   chapter list.
2. **No number may be recalled.** Every quantitative value in `delta_map.md` and in any artifact carries the
   source and folio/section where it was actually read. Where a source states no value, the artifact says so
   and leaves the magnitude to be measured. This is the same rule the 2016 package enforced, and the two
   cleanup commits on this branch (`4654ea4`, `3a0a00e`) removed exactly such inventions from it.
3. **`UDL` folios are draft-pagination.** Chapter and section numbers are the stable part of a citation;
   folios are indicative. See §1.1.
4. **Dated frontier results stay dated.** Anything whose support is a single recent paper, or which the source
   itself marks as unsettled, is recorded in `delta_map.md` with that status and is not promoted into an SOP
   as a standing rule.
5. **2016 provenance is preserved.** Modern material is additive and labelled; it never silently replaces a
   2016 statement. Where the modern position contradicts the 2016 one, both are kept and the contradiction is
   the content.
6. **No architecture encyclopaedia.** Model families are not catalogued for their own sake. A family appears
   only where it changes a decision a researcher has to make.
