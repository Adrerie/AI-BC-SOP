# Acceptance report — official TML course updates, 2024–2026

Cycle result: **PASS**, all eight checks green on the current branch tip. The run below was made after
the post-review BM-09 correction, so it covers the branch as it now stands rather than the first draft of
the extension: `534d08f` on `plan/trustworthy-ml-official-updates`, with the source PDF configured so the
source-dependent index check ran too. Nothing here is carried over from an earlier cycle: every number
below was printed by the run recorded in §C.

Inputs: [`source_inventory.md`](source_inventory.md) (U1), [`delta_map.md`](delta_map.md) (U2),
[`decision_log.md`](decision_log.md) (U3). Plan:
[`../../plans/Trustworthy-ML-Official-Updates/README.md`](../../plans/Trustworthy-ML-Official-Updates/README.md).

## A. Source gate

| Check | Result |
|---|---|
| Every accepted addition has an official source locator | **PASS** — each cites an inventory ID, and each ID carries a canonical URL; the seven lecture decks read in full are reachable from the schedule tables that link them. |
| Partial and inaccessible materials labeled | **PASS** — 16 of 22 decks, all videos, and Exercises 0/1/3 are labeled `PARTIAL` or `NO` with the routes tried. Exercise 2 is `NO` for its notebook and `FULL` only for the tutor's public scaffold. |
| Project-topic suggestions not misrepresented as standards | **PASS** — the five 2026 topics are used for exactly what they state (a detection ask, a models line, a datasets line, cited papers). Where a topic was the *only* evidence, the disposition was record-only: CD-06, CD-07. |
| Post-2023 content never labeled book-derived | **PASS** — enforced mechanically, not by reading: see §D1. |

The lineage claim rests on the pages' own wording, quoted in the inventory: the 2024/25 page says last
year's materials "are now a book" and that the yearly updates "won't cover new topics" in it, and the 2026
page repeats the same limit. That is the whole basis for treating this material as an update source and
not as book content, and it is a course statement rather than a licensing one — the book's own CC BY 4.0
position is recorded separately in [`../Trustworthy-ML-2023/SOURCE.md`](../Trustworthy-ML-2023/SOURCE.md).

## B. Delta gate, per accepted addition

Four questions from the acceptance step, answered for each accepted item. Anything that could not answer
them was rejected in `decision_log.md`.

| Delta | Absent before | Why not only an example | Why the destination is minimal | What omission would cost |
|---|---|---|---|---|
| CD-17 test-batch right | SOP-01 granted "test-time statistics" without saying what a batch grant commits | A precondition on the method's own objective, not an illustration | One definition bullet plus one item in an existing rights checklist | A per-item claim inherited from a batch-fit adaptation, with nothing stating the gap |
| CD-02 discrete-append stress | BM-05 had no discrete-input construction | The construction is the contribution; the norm-ball framing cannot express it | Two rows in BM-05 §4 and one in §5, inside the existing threat-model logic | An evaluation that reports a suffix attack with an ε, or with no budget at all |
| CD-03 channel stress | BM-05 assumed the adversary edits the classified input | A different variable and a different plausibility argument | Same host, kept as its own row so it cannot be pooled | Injection results averaged with perturbation results |
| CD-05 H-sensitivity | BM-04's three targets do not include instability under rephrasing | A new detector target with its own label construction | A fourth Extended hypothesis in BM-04, reusing registered metrics | Flagging difficulty and calling it sensitivity |
| CD-08 separability probe | BM-03 forbade over-claiming a decomposition but gave no test | It is a procedure, not an example | One diagnostic bullet in BM-03 §7 | Two estimators reported as three signals |
| CD-09 interaction positions | Every condition was a static input distribution | A condition axis the package does not have | Two bullets in BM-03 §3/§4 and one stop condition in SOP-04 | A session-level average hiding turn-level decay |
| CD-14 reproduction vocabulary | BM-08 counted flips without describing shapes of non-replication | Outcome categories, not another instance | Three rows in BM-08 §9 | "Inapplicable" being recorded as "failed to replicate" |
| CD-16 cost split | BM-06 listed cost items but not their amortization | Changes comparability between two methods | One clause in BM-06 §10 | Two methods compared at equal total cost, unequal per-case cost |
| CD-02 caveat, dating | SOP-05 named no temporal validity condition | A validity claim, not an example | One failure bullet in SOP-05 §8 | Quoting a defense that was already broken when it was measured |
| CD-10/11/12 disclosure family | No artifact asked what a model reveals | Distinct adversary goal, distinct unit of analysis, distinct chance reference | One new benchmark; the other two deltas were absorbed into it rather than given files | Nothing — this is the only addition that could not be placed anywhere existing |

## C. Regression gate

`run_acceptance.py --with-mutations`, with `TRUSTWORTHY_ML_2023_PDF` set, executed on the committed tree
at `534d08f`. Actual output: executed=8, failed=0.

| Check | Result |
|---|---|
| Source index verification | PASS — headings=243, definitions=87, captions=231, page offset=2, diffs=0 |
| Structure | PASS — findings=0, with BM-09 held to the same 13-section schema |
| Links | PASS — broken=0, asymmetric=0, duplicate_pairs=8, docs=23 |
| Metric register | PASS — parser_findings=0, unregistered=0, shape_findings=0, aupr_contract_findings=0, register_size=24 |
| Prose | PASS — vague=0, spelling_variants=0 |
| Citations | PASS — bound=437, drifting=0, unanchored=30 |
| Principle gates | PASS — markers_found=68 over 29 marker groups, regression_patterns=14, regressions=0, invariants=9, invariant_misses=0, hygiene_misses=0 |
| Mutations | PASS — cases=17, failures=0 |

The pre-existing 2023 suite is unchanged in its verdicts and its counts moved only where this cycle
deliberately moved them: the register went 23 → 24 rows with `disclosure_gap`, marker groups 20 → 29,
regression patterns 11 → 14, invariants 6 → 9, mutation cases 13 → 17.

## D. New mechanical checks

Six new load-bearing rules were stated in prose, so each got a check rather than a promise.

1. **Provenance marker and its negative.** BM-09 must carry `official-course-derived` and
   `repository conventions` in its traceability (presence marker U-10), must name the session it comes
   from (invariant), and must not acquire a book citation — regression pattern 9 matches a book reference
   landing near membership inference, data disclosure, a contextual norm or a privacy session. Mutation
   case "post-2023 disclosure rule given a book citation" writes that sentence into BM-09 in a worktree
   and requires the pattern to fire.
2. **Detector orientation for the new target.** BM-04's H-sensitivity row must state that scoring is
   against the prevalence of sensitive items (marker U-05), and the pooling failure is regression
   pattern 11, exercised by the mutation "sensitivity target pooled back into the OOD target".
3. **Threat-model fields for the new stress rows.** The discrete-append and channel rows must name a
   suffix length and remain separate (marker U-02/U-03); BM-05 §11 states that neither shares an axis
   with the ε rows.
4. **No agreement-as-truth.** Regression pattern 10, with a mutation case, keeps the rejected CD-07
   failure mode from entering later through an unremarkable sentence.
5. **Reproduction outcome taxonomy.** Marker U-14 pins "inapplicable, which is neither replication nor
   failure" and "regime-specific".
6. **Register growth discipline.** `disclosure_gap` is defined once, in SOP-08 §4, with its degeneracy
   ("zero is not compliance — both channels can be silent"); deleting the row is a mutation case, and
   `check_metrics` catches it as an unregistered name used by BM-09.

Two allowlist entries were added for the same reason the existing ones exist: the audit documents are
cited by file name inside link text, and the inline-code tokenizer reads `decision_log` and
`source_inventory` exactly as it reads a metric name.

## E. External-source cross-check

- Against the 2024/25 material: the package's threat-model, masking, plausibility and cost rules survived
  the comparison unchanged — the deck teaches the same three threat-model components SOP-05 already
  requires, which is why CD-01 was rejected. One genuine addition was found (discrete construction) and
  one caveat (results decay with the attack era).
- Against the 2026 material: the privacy session is the only place with a capability the package lacked.
  The rubric's experimental-design expectations were checked against SOP-08 §6/§10 and found already
  required, so the rubric is cited as an example rather than imported as a rule.
- Disagreements recorded rather than smoothed: the 2026 deck names **AUARC** as an evaluation metric
  without defining it, so it is not used anywhere in this repository; the deck's own citation of a
  position paper is internally inconsistent about its venue; TML26-L4 carries an arXiv identifier that
  could not be resolved; and the 2026 schedule lists the final report as due "11 June" while placing it at
  L14, which is dated 12 June. None of these is a reason to reject the material, and none is hidden by
  quoting the material more precisely than it quotes itself.
- StatProofBook was not needed: no scoring-rule math was imported, because no new scoring rule was
  adopted beyond `disclosure_gap`, which is a difference of two rates.

## F. Acceptance classification

| Candidate | Outcome |
|---|---|
| CD-02 suffix-optimisation attacks | **ACCEPTED AS EXTENDED TRACK** (BM-05) |
| CD-03 indirect prompt injection | **ACCEPTED AS EXTENDED TRACK** (BM-05) |
| CD-02 temporal-validity caveat | **ACCEPTED INTO CORE** (SOP-05 §8) |
| CD-05 prompt-sensitivity detection | **ACCEPTED AS EXTENDED TRACK** (BM-04) |
| CD-08 estimator separability probe | **ACCEPTED AS EXTENDED TRACK** (BM-03 §7) |
| CD-09 interaction conditions | **ACCEPTED** (BM-03 §3/§4 Extended, SOP-04 §7 core stop condition) |
| CD-10/CD-11/CD-12 disclosure family | **ACCEPTED** as a new benchmark, BM-09, Core plus two Extended tracks |
| CD-14 reproduction taxonomy | **ACCEPTED INTO CORE** (BM-08 §9) |
| CD-16 cost amortization split | **ACCEPTED INTO CORE** (BM-06 §10) |
| CD-17 test-batch right | **ACCEPTED INTO CORE** (SOP-01 §4/§6) |
| CD-01 threat-model trio, CD-04 model transfer, CD-15 rubric design rules | **EXAMPLE ONLY** — already required; recorded as external confirmation |
| CD-06 RAG conflict detection, CD-07 attribution agreement, CD-13 model extraction and fingerprinting, CD-19 multi-agent propagation | **RECORDED / FUTURE SCOPE**, each with the reason it did not qualify |
| CD-18 modularity framing, CD-20 generated-work disclosure | **REJECTED** — course pedagogy, not an evaluation protocol |
| CD-21 exercise bodies | **INSUFFICIENT EVIDENCE** — the notebooks could not be read |

## G. Files changed

Modified: `SOP-01`, `SOP-02`, `SOP-04`, `SOP-05`, `SOP-08`, both group READMEs, the root README,
`BM-03`, `BM-04`, `BM-05`, `BM-06`, `BM-08`, and the validation tools `_common.py`, `check_gates.py`,
`mutation_test.py`. Added: `BM-09-disclosure-of-training-data-and-context.md` and this directory's four
audit documents. No file was renamed, moved or deleted, and the 2023 package kept its identifiers.

The post-review correction round then revised BM-09 and BM-04 on the points a reader of the first draft
could have acted on wrongly: the AUROC random-ranking reference and the AUPR no-skill reference are now
separate rows rather than one "chance" baseline; surrogate contamination invalidates the ordinary result
instead of being reportable as an upper bound; the sentence-versus-corpus observation is scoped to the
setting that reported it rather than stated as the expected shape; H-emission has a primary measurement of
its own; and the channel comparison requires both raw rates next to `disclosure_gap`, because the same
zero gap is produced by two silent channels and by two leaky ones.

## H. Unresolved and limits of this cycle

1. **Two of three exercises are unread.** Exercise 1 and 3 bodies are behind Kaggle's bot protection at
   both the viewer and the API, and Wayback holds shells only. If a reader holds the notebooks, the
   exercise-level protocol content is the most likely place for a further delta; nothing in this cycle
   depends on guessing it.
2. **Sixteen decks unopened.** Only the five sessions most likely to carry a delta were read, chosen from
   the schedule titles. A delta living in, say, the 2026 epistemic-uncertainty lecture would have been
   missed, and the inventory says so rather than implying full coverage.
3. **No video was watched**, so anything taught only orally is absent from this audit.
4. **`disclosure_gap` has no worked example.** It is defined, oriented and given a degeneracy, but no
   measurement in this repository computes it, because the source session reports its own numbers only in
   prose. It should be re-examined the first time someone actually runs BM-09 §4's channel comparison.
5. **BM-09's legal framing is deliberately absent.** The session names litigation and a right to
   explanation; this benchmark measures disclosure and stops there, because a compliance claim needs a
   jurisdiction the repository does not have.
6. **The register is now 24 rows with two provenance layers.** Nothing enforces that a future book-based
   cycle adds its rows in the same place; the pattern-9 regression is the guard rail, not a general
   solution. Whether the package eventually wants a canonical cross-source layer is recorded in
   `decision_log.md` §3 as an open architecture question.

## I. How to re-run this

```text
git switch plan/trustworthy-ml-official-updates
TRUSTWORTHY_ML_2023_PDF=/path/to/book.pdf \
  python Validation/Trustworthy-ML-2023/tools/run_acceptance.py --with-mutations
```

Actual on a clean checkout of `534d08f`: `executed=8 failed=0`, with `mutation_test cases=17`,
`register_size=24`, `regression_patterns=14`, `invariants=9`, `markers_total=29`.
