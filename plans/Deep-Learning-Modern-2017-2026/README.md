# Deep Learning modern update (2017–2026)

## Goal

Extend the existing `Deep-Learning-2016` lineage only where post-2016 work changes a reusable research
workflow or an evaluable claim.

Do not build a history of architectures, a paper catalogue, or one artifact per method. Avoid duplicating
capabilities already owned by the Trustworthy ML lineage.

## Sources

Use as stable anchors:

- Christopher M. Bishop & Hugh Bishop, *Deep Learning: Foundations and Concepts* (2024).
- Simon J. D. Prince, *Understanding Deep Learning* (2023), with clearly dated official supplements where
  useful.

Use landmark papers only for structural deltas the anchors do not cover well:

- Transformer / Vision Transformer.
- AdamW.
- scaling laws + Chinchilla.
- SimCLR / CLIP / MAE.
- diffusion + flow matching.
- LoRA.
- Snell et al. (2024) for test-time compute, kept explicitly as a dated frontier result.

Do not broaden the source list for completeness.

Create only:

- `Validation/Deep-Learning-Modern-2017-2026/sources.md`
- `Validation/Deep-Learning-Modern-2017-2026/delta_map.md`

## Work

Inspect the existing Deep-Learning SOP/BC relevant to each candidate delta. Consult a Trustworthy ML
artifact only when an actual overlap is identified.

Focus on five update areas:

1. **Scale/resources** — model, data and compute allocation; compute-aware comparison.
2. **Architecture** — attention/Transformers and the changed assumptions behind sequence/vision modeling.
3. **Training and adaptation** — decoupled weight decay, modern pretraining/representation learning, transfer
   and parameter-efficient adaptation.
4. **Generative modeling** — diffusion and flow-based training/evaluation where they change the 2016 workflow.
5. **Inference-time compute** — only if a reusable, source-bounded protocol can be stated.

For each accepted item, record in `delta_map.md`:

`2016 baseline → modern delta → source → destination → boundary`

Then:

- extend an existing Deep-Learning SOP/BC when the research function is the same;
- cross-link Trustworthy ML instead of duplicating its capability;
- create a new SOP/BC only for a genuinely new workflow or evaluable capability;
- leave method-specific, weakly supported or unsettled items in `delta_map.md` only.

Keep 2016 traceability intact. Any modified file gets a short modern-update provenance note pointing to the
relevant delta/source; a wholly new artifact lists its modern sources directly.

Do not preassign a target number of new artifacts.

## Finish

Do one pass for duplication, provenance and broken links. Do not add validators, gates, mutation tests,
acceptance cycles, extra plan files, or broad literature sweeps.

Commit and push `plan/deep-learning-modern-update`. Do not merge `main`.
