# Deep Learning (Goodfellow, Bengio & Courville, 2016) — SOP / Benchmark plan

## Goal

Use the local copy of *Deep Learning* ("the flower book") to build a reusable SOP and Benchmark/BC
package without mirroring the book chapter by chapter.

This branch starts from `framework/book-base`. Do not import the Trustworthy ML package and do not
merge `main` automatically.

## 1. Read and reconstruct

Use the book file already present in the local workspace. Record the edition/language, filename and
pagination convention in:

`Validation/Deep-Learning-2016/SOURCE.md`

Do not commit the PDF or bulk extracted text.

Read the table of contents first, then the relevant body sections. Reconstruct the book by research
function rather than chapter number.

Keep a single working record:

`Validation/Deep-Learning-2016/concept_reconstruction.md`

It should briefly record:
- what reusable research workflows the book supports;
- what evaluable capabilities/failure modes it supports;
- which major parts are mainly theory and therefore do not need an SOP/BC;
- where a 2016 implementation detail is historical rather than a current general rule.

Do not create separate audit/gate documents unless they become genuinely necessary.

## 2. Build SOPs

Create:

`SOP/Deep-Learning-2016/`

Only create an SOP when the material yields a reusable workflow.

Prefer broad research procedures such as:
- formulate an objective and output distribution;
- diagnose underfitting/overfitting and capacity;
- select regularization;
- diagnose optimization failure;
- perform model selection / hyperparameter search;
- debug a deep-learning experiment.

These are examples, not a required list.

Do not create one SOP for every optimizer, architecture, chapter, or method family.

Each SOP only needs:
- purpose / scope;
- inputs or assumptions;
- procedure;
- important failure modes;
- outputs/reporting;
- source traceability.

Chapter 11 practical methodology should be folded into the relevant workflows rather than copied as a
chapter summary.

## 3. Build Benchmarks / BCs

Create:

`Benchmark/Deep-Learning-2016/`

Only create a BC when the book provides a concrete evaluable research question.

A BC should state enough to run the evaluation:
- what capability/failure is tested;
- data or comparison conditions;
- baseline(s);
- metric(s);
- how to interpret failure;
- validity limits and source traceability.

An architecture name is not a Benchmark. CNN, RNN, autoencoder, generative model, etc. should become a
BC only if there is a distinct evaluable claim.

Do not invent metrics just to complete a template.

## 4. Historical boundary

Treat the book as a 2016 source.

Preserve principles that remain general, but mark book-era implementation choices or empirical examples
as historical when needed.

Do not silently modernize the source with Transformers, AdamW, scaling laws, modern leaderboards, or
other later material. Those can be added in a future source-update cycle.

Likewise, do not turn an old implementation detail into a mandatory current best practice merely because
the book used it.

## Scope

Prioritize material with clear research-method value:

- generalization / capacity / regularization;
- optimization and initialization;
- model selection and practical methodology;
- architectural inductive bias where it changes experimental reasoning;
- representation learning and transfer where the book supports a reusable procedure or evaluable claim;
- inference / generative-model material only where an actual workflow or evaluation protocol can be
  extracted.

Theory-only material may remain in `concept_reconstruction.md` with no artifact.

## Finish

Before stopping, do one concise pass to ensure:

- no obvious chapter-shaped duplication;
- every SOP/BC has a book source;
- historical examples are not written as universal current defaults;
- package indexes and internal links are usable.

Do not add validator frameworks, mutation tests, multi-stage gates, repeated acceptance cycles, or
extra plan files.

Expected result:

```text
SOP/Deep-Learning-2016/
Benchmark/Deep-Learning-2016/
Validation/Deep-Learning-2016/
  SOURCE.md
  concept_reconstruction.md
plans/Deep-Learning-2016/README.md
```

Update the branch's root/SOP/Benchmark indexes only enough to expose the package.

Commit and push `plan/deep-learning-2016`. Do not merge `main`.
