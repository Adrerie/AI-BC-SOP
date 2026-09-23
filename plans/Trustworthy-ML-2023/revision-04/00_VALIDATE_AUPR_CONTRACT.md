# Plan 1 — Validate the AUPR contract

## Goal

Demonstrate that the final AUPR semantics are consistent across the package and mechanically guarded.

## Authoritative package contract

### Generic `aupr`

Package-wide `aupr` means **non-interpolated Average Precision**:

```text
AP = Σ_n (R_n - R_{n-1}) P_n
```

over score thresholds.

It is **not** trapezoidal integration of a precision-recall polyline under the same metric name.

Every use must state:

- the positive class
- a score whose larger value means "more likely positive"
- the positive-class prevalence as the no-skill reference

### Correctness specializations

`aupr_success`:

- positive = success / `L = 1`
- score orientation = confidence `c`
- no-skill reference = `P(L = 1)`

`aupr_error`:

- positive = error / `L = 0`
- score orientation = `1 - c`, or an explicitly equivalent score increasing with error likelihood
- no-skill reference = `P(L = 0)`

Using confidence `c` directly for the error-positive variant reverses the intended ranking and is a
failure.

## 1. Cross-file reading

Read together:

- `SOP-08` §4 and §12
- `SOP-04` ranking procedure and traceability
- `BM-03` primary metrics and traceability
- `BM-04` hypotheses, baselines, primary metrics, failure interpretation, traceability

Confirm:

- generic detection tasks use `aupr`
- H-error may use the two correctness specializations
- H-ood uses positive=OOD and an OOD-oriented score
- H-multiplicity uses positive=multiple-answer and a score oriented toward multiplicity
- no file calls trapezoidal PR-AUC `aupr`

## 2. Run the metric checker

Run:

```
python Validation/Trustworthy-ML-2023/tools/check_metrics.py
```

Required current shape:

- `parser_findings=0`
- `unregistered=0`
- `shape_findings=0`
- `aupr_contract_findings=0`
- `register_size=23`

Do not copy these values into the report unless the actual run produces them.

## 3. Provoke the AUPR guard

In an isolated worktree or temporary clean copy, run at least these three reversible mutations one at
a time:

### Mutation A — numerical convention

Change the generic `aupr` row from non-interpolated Average Precision to trapezoidal PR-AUC.

Expected:

`check_metrics.py` fails with an `AUPR CONTRACT` finding.

### Mutation B — success orientation

Change `aupr_success` so that the positive class is success but the score orientation is `1-c`.

Expected:

`check_metrics.py` fails with an `AUPR CONTRACT` finding.

### Mutation C — error orientation

Change `aupr_error` so that the positive class is error but the score orientation is confidence
`c`.

Expected:

`check_metrics.py` fails with an `AUPR CONTRACT` finding.

Restore the untouched tree and verify the checker returns green.

If useful, commit a small dedicated metric-contract mutation test. Do not weaken the checker simply to
make these probes pass.

## 4. Full suite

Run:

```
python Validation/Trustworthy-ML-2023/tools/run_acceptance.py --with-mutations
```

When the source PDF is available, also run the source-dependent suite with
`TRUSTWORTHY_ML_2023_PDF`.

## Gate R4-1

PASS only if:

- all AUPR definitions agree
- all three contract mutations are detected
- the restored clean tree passes
- the complete mechanical suite passes
- the source-dependent citation-index check passes when the source is available
