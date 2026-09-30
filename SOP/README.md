# SOP

This directory is a growing collection of **Standard Operating Procedures for AI and machine learning research**.

Each SOP converts methodological knowledge from textbooks, papers, courses, and research practice into a reusable workflow. SOPs are expected to evolve as new literature is studied and better practices are identified.

An SOP should answer questions such as:

- What problem or research stage does this procedure apply to?
- What inputs and prerequisites are required?
- What sequence of steps should be followed?
- What checks are mandatory?
- What common methodological errors should be avoided?
- What outputs should be retained or reported?

The directory is not restricted to a single research area. New SOPs should be added whenever continued reading reveals a procedure that is general enough to be reused across experiments or projects.

## Packages

SOPs are grouped by the source they were reconstructed from, one directory per package:

- [`Trustworthy-ML-2023/`](Trustworthy-ML-2023/README.md) — 8 SOPs covering the evaluation workflow
  from declaring a deployment setting to reporting evidence and its validity boundaries. Selected files
  carry clearly labeled additions from the official 2024–2026 course material, traced in
  [`Validation/Trustworthy-ML-Official-Updates-2024-2026/`](../Validation/Trustworthy-ML-Official-Updates-2024-2026/source_inventory.md).
- [`Deep-Learning-2016/`](Deep-Learning-2016/README.md) — 9 SOPs covering task/output specification,
  fitting-regime diagnosis, regularization, optimization diagnosis, model selection, experiment debugging,
  inductive-bias choice, sharing/transfer decisions, and generative-model comparison. Seven of the nine
  carry clearly marked *Modern update (2017–2026)* blocks annotating the 2016 procedure where later work
  changes a reusable step; the 2016 text and its citations are unchanged. Source record and per-delta
  judgements: [`Validation/Deep-Learning-Modern-2017-2026/`](../Validation/Deep-Learning-Modern-2017-2026/delta_map.md).

A package's update layer annotates in place rather than replacing: an existing SOP is extended when the
research function is the same, a capability owned by another package is cross-linked rather than duplicated,
and unsettled or method-specific material stays in the delta record instead of becoming a procedure.
