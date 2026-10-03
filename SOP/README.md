# SOP

The SOP directory is a growing collection of **Standard Operating Procedures for AI and machine learning research**.

Each SOP converts methodological knowledge from textbooks, papers, courses, and research practice into a reusable
workflow. Later reading should revise an SOP, not only add to it.

Each SOP answers the following:

- the problem or research stage it applies to
- the inputs and prerequisites it requires
- the sequence of steps to follow
- the checks that are mandatory
- the common methodological errors to avoid
- the outputs to retain or report

The directory covers more than one research area. Add a new SOP whenever further reading reveals a procedure
general enough to reuse across experiments or projects.

## Packages

Group SOPs by the source they reconstruct. Each package has one directory:

- [`Trustworthy-ML-2023/`](Trustworthy-ML-2023/README.md) — 8 SOPs that cover the evaluation workflow, from
  declaring a deployment setting to reporting evidence and the boundaries of that evidence. Selected files
  carry clearly labeled additions from the official 2024–2026 course material, traced in
  [`Validation/Trustworthy-ML-Official-Updates-2024-2026/`](../Validation/Trustworthy-ML-Official-Updates-2024-2026/source_inventory.md).
- [`Deep-Learning-2016/`](Deep-Learning-2016/README.md) — 9 SOPs that cover the following stages. They cover
  task and output specification, fitting-regime diagnosis, regularization, optimization diagnosis, and model
  selection. They also cover experiment debugging, inductive-bias choice, sharing and transfer decisions, and
  generative-model comparison. Seven of the nine
  carry clearly marked *Modern update (2017–2026)* blocks. Each block annotates the 2016 procedure at the
  point where later work changes a reusable step. The 2016 text and its citations are unchanged. Source
  record and per-delta judgements:
  [`Validation/Deep-Learning-Modern-2017-2026/`](../Validation/Deep-Learning-Modern-2017-2026/delta_map.md).

A package's update layer annotates in place instead of replacing. The layer extends an existing SOP when the
research function is the same. The layer cross-links a capability that another package owns. Unsettled or
method-specific material stays in the delta record, and it does not become a procedure.
