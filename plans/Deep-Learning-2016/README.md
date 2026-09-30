# Deep Learning (2016) — source-package cleanup

## Goal

Clean the extracted 2016 package before review. Do not add new SOPs/BCs, post-2016 material, validators,
gates, mutation tests, acceptance cycles, or extra plan files.

## Required changes

### BCs

- **BC-DL-03:** do not classify regularization by whether training error happened to decrease. Report
  training/generalization error separately; if both improve, note possible optimization/capacity effects.
- **BC-DL-04:** remove as an active BC. Keep adversarial linearity / FGSM only as a 2016 historical
  observation in `concept_reconstruction.md` and, if useful, brief SOP context. Remove links/index entry.
- **BC-DL-05:** keep the useful probes but reframe as an **optimization diagnostic probe suite**. Probes may
  support or rule out diagnoses; they do not uniquely classify pathology from traces. Rename if needed.
- **BC-DL-12:** restrict PCA to linear/undercomplete-autoencoder and directly related comparisons. Other
  representation claims use their own appropriate controls.

### SOPs

Shorten `SOP-DL-03`, `SOP-DL-04`, `SOP-DL-08`, and `SOP-DL-09`.

Keep the executable decision path; compress or move catalog-style method inventories, historical menus,
long derivations and era-specific recipes into compact notes or `concept_reconstruction.md`.

For `SOP-DL-04`, center the flow on:

`verify objective → inspect symptom → probe → minimal repair → rerun → report`

Keep essential failure modes, source traceability and historical boundaries.

## Synchronize

Update `concept_reconstruction.md`, package READMEs, indexes and cross-links affected by the BC removal/
rename or SOP reductions.

Keep the distinction between book-derived principle, 2016 historical observation, and repository
operationalization clear.

## Finish

Do one final content/link pass, commit and push `plan/deep-learning-2016`. Do not merge `main`.
