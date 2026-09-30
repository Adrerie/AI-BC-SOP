# Deep Learning modern update (2017–2026)

## Goal

Extend the existing `Deep-Learning-2016` lineage with modern deep-learning changes that alter a reusable
research workflow or an evaluable claim.

Do not rewrite the package as a history of architectures, and do not create one artifact per paper or
model family.

This branch starts from the current `main`, so the update must also avoid duplicating capabilities that
already live in the Trustworthy ML lineage.

## Sources

Use two modern textbooks as the stable conceptual anchors:

- Christopher M. Bishop & Hugh Bishop, *Deep Learning: Foundations and Concepts* (2024).
- Simon J. D. Prince, *Understanding Deep Learning* (2023); later official website supplements may be
  used only when clearly dated.

Use landmark papers only where they establish a structural delta not adequately covered by the textbook
anchors. Initial candidates:

- Vaswani et al. (2017), *Attention Is All You Need*.
- Loshchilov & Hutter (2019), decoupled weight decay / AdamW.
- Kaplan et al. (2020) and Hoffmann et al. (2022), model–data–compute scaling and compute-optimal training.
- Chen et al. (2020), SimCLR; Radford et al. (2021), CLIP; He et al. (2022), MAE.
- Dosovitskiy et al. (2021), Vision Transformer, where needed for the change in architectural inductive bias.
- Ho et al. (2020), diffusion models; Lipman et al. (2023), flow matching.
- Hu et al. (2022), LoRA / parameter-efficient adaptation.
- Snell et al. (2024), test-time compute scaling, as a dated frontier source rather than a settled universal rule.

Do not expand this list simply for coverage. Add another source only when an identified delta cannot be
supported well by the sources above.

Create only:

- `Validation/Deep-Learning-Modern-2017-2026/sources.md`
- `Validation/Deep-Learning-Modern-2017-2026/delta_map.md`

No separate gate, acceptance, or per-source audit files.

## What counts as a delta

A modern item is worth importing only if it changes at least one of:

- what information/resources must be declared before an experiment;
- how a training/adaptation decision is made;
- which assumption an architecture encodes and how that assumption is tested;
- which comparison/baseline is required;
- how compute/data/model scale changes experimental design;
- how a generative model is trained or compared;
- what can be done at adaptation or inference time that the 2016 workflow did not contain.

A new method name by itself is not a delta.

## Axes to inspect

Use these as a compact checklist, not as required artifact counts:

1. **Scale and resources** — model/data/compute allocation, compute-optimal training, and resource-normalized
   comparison.
2. **Architecture and sequence/image bias** — attention/Transformers and the weakening of the 2016
   recurrence/convolution defaults. Treat newer SSM/Mamba-style models as a frontier candidate only if they
   change the workflow; do not create an architecture catalogue.
3. **Optimization and regularization** — modern distinctions that change the decision path, especially
   decoupled weight decay and interactions with adaptive optimizers. Do not build an optimizer leaderboard.
4. **Pretraining, representation and adaptation** — contrastive learning, masked modeling, language/image
   supervision, transfer, and parameter-efficient adaptation. Focus on what must be controlled and measured,
   not on reproducing every pretraining recipe.
5. **Generative modeling** — diffusion and flow-based training/evaluation as structural successors to the
   2016 generative comparison workflow.
6. **Inference-time computation** — treat test-time compute as a new resource axis if the evidence supports a
   reusable protocol; keep the claim source- and task-bounded.

## Routing

Read the current `Deep-Learning-2016` SOPs/BCs and the relevant Trustworthy ML artifacts before editing.

For each accepted delta, record in `delta_map.md`:

`2016 baseline → modern change → source → destination → boundary`

Then route it as follows:

- same research function → minimally extend the existing Deep-Learning SOP/BC;
- already owned by Trustworthy ML → cross-link instead of duplicating;
- genuinely new reusable workflow/capability → create a new SOP/BC only if an existing artifact cannot
  express it cleanly;
- interesting but method-specific or unsettled → record in `delta_map.md`, no artifact.

Do not preassign a target number of new files.

## Provenance

Keep the 2016 source traceability intact.

When an existing Deep-Learning file receives modern content, add a short modern-update provenance note that
points to the relevant `delta_map.md` entry and source. Do not copy a long source audit into every file.

A wholly new artifact must state directly that it is modern-update-derived and list its primary sources.

Do not present a 2024–2026 frontier observation as a timeless rule.

## Finish

Do one final pass for:

- duplicated functionality with Trustworthy ML;
- architecture/paper-shaped artifacts that should be folded into an existing workflow;
- post-2016 claims without clear provenance;
- broken internal links.

Do not add validators, mutation tests, staged gates, repeated review cycles, or extra plan files.

Commit and push `plan/deep-learning-modern-update`. Do not merge `main`.
