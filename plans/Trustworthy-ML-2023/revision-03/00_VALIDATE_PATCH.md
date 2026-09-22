# Plan 1 — Validate the final patch

## Goal

Prove that the direct metric/parser patch is internally consistent and did not regress any earlier
gate.

## 1. Metric register

Confirm that `SOP-08` contains:

- generic `aupr`
- `aupr_success`
- `aupr_error`

The intended semantics are:

- `aupr`: any declared binary detection/ranking task, positive class and score orientation stated
- `aupr_success`: correctness task, positive = success
- `aupr_error`: correctness task, positive = error

BM-04 must use generic `aupr` for OOD-positive and multiplicity-positive tasks.

## 2. Parser correctness

Run `check_metrics.py`.

Required result:

- parser self-test PASS
- no unregistered metric identifiers
- register size consistent with the actual table

The parser must inspect identifiers inside compound inline-code expressions rather than only accepting
a whole code span as one token.

Search explicitly for stale pseudo metric keys:

- `true_robust_acc`
- `empirical_attack_acc`
- `acc_shift`
- `acc_diagonal`
- `acc_offdiagonal`

None should remain as registered-looking snake_case metric names in normative artifacts.

## 3. Non-metric allowlist discipline

Review additions to `METRIC_ALLOW`.

Every allowlisted identifier must be demonstrably a:

- output/schema field, or
- local mathematical variable

Do not add actual evaluation metrics to the allowlist merely to make the checker green.

## 4. Mutation-test wording

Confirm documentation distinguishes:

- regex-level self-tests for every regression pattern
- 10 representative end-to-end worktree mutations

Do not claim one worktree mutation exists for every marker, invariant, or detector.

## 5. Full mechanical suite

Run:

```
cd Validation/Trustworthy-ML-2023/tools
python run_acceptance.py --with-mutations
```

If the source PDF is available, also run with:

```
TRUSTWORTHY_ML_2023_PDF=<local path> python run_acceptance.py --with-mutations
```

Do not carry forward Cycle 3 numbers. Record the actual new outputs.

## Gate R3-1

PASS only if:

- metric semantics are consistent across SOP-08, BM-03, BM-04
- compound code spans cannot bypass `check_metrics.py`
- no pseudo metric keys remain
- the full mechanical suite is green
- representative mutation tests are green
