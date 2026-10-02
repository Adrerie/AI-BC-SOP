# Deep Learning modern update — final content patch

## Goal

The 2017–2026 modern update is already implemented and reviewed. This pass is a small content
closeout, not a new extraction or literature-review cycle. Keep all 2016 material, accepted deltas,
source boundaries and the existing SOP/BC inventory. Do not add new artifacts or research topics.

## Patch

1. **Shorten `SOP-DL-08`'s modern additions.** Keep only the decision rules and controls needed to
   choose self-supervised pretraining, contrastive/MAE-style training, zero-shot transfer and frozen-base
   low-rank adaptation. Keep the relevant resource, label-set, prompt-selection and transfer-validity
   conditions. Replace repeated paper narratives, historical comparisons and source-result inventories
   with short links to the existing `sources.md` / `delta_map.md`.
2. **Shorten `SOP-DL-09`'s modern additions.** Keep the actionable distinctions among training objective,
   evaluation instrument, comparable likelihoods, sample-quality metrics, conditional-generation criteria
   and compute cost. Compress duplicated explanation across procedure, failure modes, reporting and
   provenance; retain its objective-capability table and essential caveats.
3. **Check only affected cross-file consistency.** Preserve the corrections already made:
   - `L_simple` is a training loss, while its trained model can be separately evaluated with a valid
     variational likelihood bound;
   - a valid lower bound above comparable exact likelihood supports a one-sided likelihood conclusion;
   - flow matching is simulation-free in training, not ODE-free in sampling or density evaluation;
   - FID specifies its feature setup and real-data reference split;
   - capacity exploration uses development/validation data, not the final test set.
   Fix an actual contradiction in the affected SOP/BC, README or `delta_map.md` only if found.

## Finish

Keep modern provenance in each retained extension and detailed evidence in the existing
`Validation/Deep-Learning-Modern-2017-2026/` records. Do one concise content/link pass over changed
files. Do not rewrite the rest of the package, add sources, change accepted/rejected delta decisions,
invent thresholds, or introduce validators, mutation cases, gates, acceptance cycles or extra plans.

Commit and push `plan/deep-learning-modern-update`. Do not merge `main`.
