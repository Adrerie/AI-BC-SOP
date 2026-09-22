# Revision Master Plan

## Objective

Correct the Trustworthy-ML-2023 package so that it is:

- mathematically correct
- explicit about which rules are universal and which depend on a declared setting
- careful about causal language
- careful about mitigation and abstention decision logic
- current enough not to mistake one textbook example for a universal limit
- independently re-verifiable from committed validation tooling
- compatible with the repository's long-term goal of accumulating and refining canonical SOPs and Benchmarks across many sources

## Preserve unless a specific issue requires change

Preserve:

- the 8-SOP / 8-Benchmark decomposition
- concept reconstruction as the main organizational logic
- source traceability
- Core / Extended tiering where useful
- SOP ↔ Benchmark cross-links
- Validation artifacts as an audit trail

Do not mechanically rewrite every document.

## Required correction classes

### P0-A Mathematical and metric correctness

Correct at minimum:

- AUPR random baselines for success-positive versus error-positive tasks
- AUROC semantics so the metric definition is target-label-aware rather than permanently tied to correctness
- perplexity / NLL log-base consistency
- constant-confidence diagnostic leakage and oracle status

Search the entire package for every occurrence, not only the files named by review.

### P0-B Setting-dependent rules

Rewrite rules that currently assume one strict domain-generalization setting as if they were universal.

The governing principle must become:

> information use is valid only if it is within the information rights declared by the setting.

This must allow legitimate settings such as domain adaptation, transductive inference, test-time adaptation, continual learning, few-shot adaptation, or target-informed calibration when they are explicitly declared and evaluated against the correct comparison class.

### P0-C Test contamination and independence

Clarify that once final-test results influence model, threshold, checkpoint, or protocol selection, that test set is no longer an independent final test for the affected claim.

Re-running the same test after correcting the selection procedure does not restore independence.

### P0-D Causal and evidential language

Counterfactual edits and attribution probes provide evidence under intervention assumptions. They do not automatically prove causal dependence or non-use of a cue.

Replace deterministic causal conclusions unless the identification conditions actually justify them.

### P0-E Decision rules and mitigation

Remove hard-coded method-selection rules that elevate one textbook scenario into a universal policy.

Use admissibility, declared objective, costs, available supervision, and Pareto trade-offs.

Abstention is only available when an informative score and a valid fallback process have themselves been established.

### P0-F Robustness and certification

Separate:

- the book's historical/example certification methods
- the general concept of certified robustness

Do not encode shallow-network or binary-task constraints as universal limits of certification.

### P0-G Reproducible acceptance

Commit validation tooling needed to rerun non-copyright mechanical checks.

Do not commit copyrighted source text or extracted book passages.

Replace machine-specific absolute paths with portable source configuration.

### P1-A Repository architecture

Do not lock the whole repository permanently into one-source-per-package as the only organizational principle.

The source package may remain as provenance and staging, but the root README must state that future sources may revise, merge into, supersede, or extend canonical SOPs / Benchmarks.

### P1-B Source attribution and license notice

Add package-level source attribution for the 2023 book, including title, authors, source URL/reference, source license, and a clear statement that these files are reconstructed/adapted methodology notes rather than a reproduction of the book.

## Non-goals

Do not:

- remove useful strong requirements merely to avoid review criticism
- replace all procedures with disclaimers
- import unrelated modern literature into the package as if it came from the book
- silently change source-derived claims without updating traceability
- retain old PASS results after materially changing files

## Completion rule

Revision is complete only when all tasks in plans 01–06 are finished and Plan 07 produces a new acceptance report with no unresolved P0 issue.
