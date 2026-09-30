# Deep Learning (Goodfellow, Bengio & Courville, 2016) — source-package cleanup

## Goal

Finish the 2016 source package before any modern update is added.

The package is already extracted. This pass is only for correcting over-strong claims and reducing
overgrown artifacts. Do not add new SOPs, new BCs, new validators, new gates, or post-2016 material.

## 1. Correct the BCs

### BC-DL-03 — regularization

Keep the benchmark, but fix the interpretation of the book's definition.

Do not say that a method stops being regularization merely because training error also decreases.
Instead:

- report training and generalization error separately;
- if both improve, note that optimization/capacity may also have changed;
- keep the classification based on the intended role and the actual experimental mechanism, not on one
  observed training-error direction.

### BC-DL-04 — adversarial linearity

Remove this as an active reusable BC.

The 2016 adversarial-linearity explanation and FGSM-era experiment should remain as a historical
source-era observation in `concept_reconstruction.md` and, where useful, as context in the regularization
SOP. Do not present "excessive linearity" as a current causal benchmark hypothesis.

Delete the BC file and remove its index/cross-links.

### BC-DL-05 — optimization pathology

Keep the useful diagnostic experiments, but remove the strong "separability/classify the pathology from
the trace" claim.

Reframe it as an **optimization diagnostic probe suite**:

- each probe tests one symptom/repair relation;
- a probe can rule out or support a diagnosis;
- the suite does not promise unique identification from traces;
- remedies are evaluated against the quantity they are meant to change.

Rename the file/title if needed and update links.

### BC-DL-12 — representation quality

Keep the benchmark, but narrow PCA to the claims it actually supports.

PCA is a required matched-dimension control for the linear/undercomplete-autoencoder and related
downstream comparisons. It is not the universal baseline for every representation claim.

Use local controls for manifold sensitivity, contractiveness, one-hot similarity, sparse coding and
distributed-representation arguments.

## 2. Reduce overgrown SOPs

Keep the current nine-SOP architecture unless a deletion becomes obviously necessary.

Shorten these four:

- `SOP-DL-03`
- `SOP-DL-04`
- `SOP-DL-08`
- `SOP-DL-09`

The main procedure should contain only the decision path a researcher follows.

Move or compress long catalog-style material — optimizer inventories, historical method menus, model
family surveys, detailed derivations and era-specific recipes — into compact tables or
`concept_reconstruction.md`.

In particular, `SOP-DL-04` should read approximately as:

`verify objective → inspect symptom → run the relevant probe → apply the smallest repair → re-run → report`

It should not function as a rewritten optimization textbook.

Do not shorten by deleting source boundaries, important failure modes, or the historical caveat.

## 3. Synchronize the package

Update:

- `Validation/Deep-Learning-2016/concept_reconstruction.md`
- SOP/BC READMEs and cross-links
- root/SOP/Benchmark indexes if IDs or filenames changed

The reconstruction should clearly distinguish:

- book-derived principle;
- historical 2016 observation/example;
- repository operationalization.

## 4. Finish

Do one concise content pass only:

- no chapter-shaped duplication;
- no historical explanation promoted to a current universal claim;
- no broken links after BC-DL-04 removal / BC-DL-05 rename;
- no obvious inconsistency between reconstruction and artifact indexes.

Do not create an acceptance framework or another revision plan.

Commit and push `plan/deep-learning-2016`. Do not merge `main`.

## Next phase — not part of this run

After this source package is reviewed and merged, create a separate modern-update branch from the then
current `main`.

That future update should compare the 2016 workflows against modern sources and add only structural
deltas such as:

- model/data/compute scaling;
- Transformer/modern sequence and vision inductive biases;
- modern pretraining, transfer and representation learning;
- diffusion / flow-based generative modeling;
- modern optimization/training stability where it changes the workflow;
- resource-normalized adaptation/efficiency;
- test-time compute and post-training/reasoning.

Do not add those topics during this cleanup.
