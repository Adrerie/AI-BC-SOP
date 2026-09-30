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

| Package | Source | Contents |
| --- | --- | --- |
| [`Deep-Learning-2016/`](Deep-Learning-2016/README.md) | *Deep Learning*, Goodfellow, Bengio & Courville, MIT Press 2016 (local copy: Simplified Chinese edition, 人民邮电出版社 2017) | 9 SOPs reconstructed by research function: task/output/cost specification, fitting-regime and capacity diagnosis, regularization selection, optimization-failure diagnosis, model selection and hyperparameter search, experiment debugging, inductive-bias choice, sharing decisions, generative-model comparison. |

Each package keeps its source record and reconstruction notes under `Validation/<Package>/`, and the benchmark checks that execute its SOPs under `Benchmark/<Package>/`.
