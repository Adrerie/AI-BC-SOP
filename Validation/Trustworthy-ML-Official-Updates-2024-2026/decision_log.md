# Decision log — smallest correct change for each delta

Plan `03_EXTENSION_DECISIONS.md` artifact. Input: [`delta_map.md`](delta_map.md) (Gate U2). Decision
order D0–D5 is the plan's; exactly one is chosen per delta.

## 1. Decisions

| ID | Delta | Decision | Destination | Why this and nothing larger |
|---|---|---|---|---|
| CD-01 | Threat model as three declared components | **D0** record only | — | SOP-05 already requires goal, strategy space and knowledge, and BM-05 already refuses to compare rows whose threat models differ. The 2026 deck re-teaches the rule this package wrote. |
| CD-02 | Suffix-optimisation attacks on aligned models | **D3** Extended Track | BM-05 §4/§5, SOP-05 §8 | The evaluation logic is BM-05's already; only the construction is new, so it becomes a marked track rather than a new file. Model-family-specific, which is precisely D3's condition. |
| CD-03 | Indirect prompt injection through an unowned channel | **D3** Extended Track | BM-05 §4/§11 | Same host, different strategy variable. Kept in its own row so it cannot be pooled with norm-ball results. |
| CD-04 | Transfer across models, not across data | **D1** example | BM-05 traceability | BM-05 already measures transferability across training conditions; the 2026 wording sharpens a rule that exists. An example, not a change. |
| CD-05 | Test-time prompt-sensitivity detection | **D2** extend | BM-04 §2/§4/§5/§9, Extended | BM-04 owns detector targets and already forbids pooling hypotheses; a fourth flag target fits without overloading any existing one. |
| CD-06 | RAG parametric–contextual conflict detection | **D0** record as future scope | — | Evidence is one project suggestion plus three unread papers. A new benchmark needs design, baselines, aggregation and failure interpretation; the source supplies a models line, a datasets line and "evaluate its precision". |
| CD-07 | Mechanistic versus data attribution agreement | **D0** record as future scope | — | The three decks read for this never ask for the comparison, and agreement is not correctness; BM-06 already treats instrument disagreement without calling it error. |
| CD-08 | Disentanglement by cross-prediction | **D2** extend | BM-03 §7 | Turns an existing prohibition in SOP-04 §8 into a checkable diagnostic. No new metric name: prose plus an orientation rule is enough, and the register stays 24 rows rather than growing for every diagnostic. |
| CD-09 | Confidence across an interaction history | **D2** extend | BM-03 §3/§4/§10, SOP-04 §7 | A missing condition axis and a missing cost line, both inside artifacts that already report calibration and ranking separately. |
| CD-10 | Privacy and data-protection evaluation | **D4** new Benchmark | BM-09 (new) | See §2 below. |
| CD-11 | Contextual-norm gap between reasoning channel and answer | **D4**, absorbed | BM-09 | Same capability family as CD-10 and the only place its disclosure-gap metric can be defined once. |
| CD-12 | Privacy-utility curve with cross-step composition | **D2**, absorbed into BM-09 | BM-09 | The curve is a reporting shape inside the new benchmark, not a separate artifact. |
| CD-13 | Model extraction and fingerprint auditing | **D0** record as future scope | — | Protects the developer's asset, not a claim about the system. Accepting it would change what the group evaluates. |
| CD-14 | Reproduction as claim-boundary mapping | **D2** extend | BM-08 §9 | BM-08 already re-runs and cross-probes; only the outcome vocabulary is missing. |
| CD-15 | Rubric experimental-design expectations | **D1** example | SOP-08 §12 | Baselines, variability and limitation reporting are already required in SOP-08 §6/§10 and in every BM §8. The rubric is a modern, external restatement worth citing, not a new rule. |
| CD-16 | Explanation cost itemisation | **D2** extend | BM-06 §10 | One clause: separate one-time from per-case cost. |
| CD-17 | Test-time adaptation preconditions | **D2** extend | SOP-01 §4/§6 | The right already exists; the caveat about what a batch right costs a per-item claim does not. |
| CD-18 | Modularity axes and layered underspecification | **D0** pedagogy only | — | TML26-L4 names no metric, dataset, baseline or test. It is a framing lecture. |
| CD-19 | Multi-agent uncertainty propagation | **D0** record as future scope | — | One internal, unpublished citation inside a taught deck. Not enough to specify a protocol. |
| CD-20 | Generated-work disclosure policy | **D0** pedagogy only | — | An academic-integrity rule for student submissions. The package's provenance appendix already covers artifact provenance; extending it to "name the models you used" would import a classroom policy as a research protocol. |
| CD-21 | Exercise 1 and 3 protocol content | **D0** insufficient evidence | — | Bodies unreachable. No delta may rest on them, and none does. |

No D5 (new SOP) was taken: every accepted item lands on an existing stage of the SOP chain, and the
chain's shape — declare, freeze, diagnose, measure, stress, decide, explain, report — still describes
what a privacy evaluation does, via SOP-01, SOP-05 and SOP-08.

## 2. The one D4, argued

BM-09 is proposed for CD-10/CD-11/CD-12 because all four D4 conditions hold:

1. **Distinct target failure.** The adversary's goal is information disclosure, which the 2026 security
   deck itself separates from making the model misbehave. Nothing in BM-01…BM-08 asks whether a model
   reveals a fact about a specific training item or about a context it was shown.
2. **Not expressible as a track inside an existing benchmark without overload.** Inside BM-05 it would
   put an inference AUROC in the same column as attacked accuracy and inherit a
   certified-empirical ordering that does not apply. Inside BM-08 it would be read as an integrity audit
   of a comparison rather than a property of the deployed model.
3. **Enough source detail.** The deck supplies the task definition, the shadow-model baseline, the
   chance anchor, the unit-of-analysis rule, the memorisation scaling axes, the privacy-utility trade-off
   and an exposed-channel comparison. That is enough to write design, baselines, metrics, aggregation,
   failure interpretation and validity limits.
4. **Reusable research value.** The same protocol applies to vision, language and multimodal models and
   to any claim of the form "this model does not disclose that".

What BM-09 deliberately does **not** take: no differential-privacy theorem, no attack catalogue, no
regulatory compliance claim. It evaluates a disclosure measurement the way BM-04 evaluates a detection
measurement.

## 3. Architecture check

The repository now has two provenance layers over one artifact set: book-derived text in the 2023
package, and official-course-derived text inserted into the same files. That is a real distinction, and
the temptation is a canonical cross-source layer.

Decision: **do not build one now.** The existing traceability sections already carry per-claim provenance
labels, and the plan's own rule forbids a second source-silo copy. What is missing is only a statement in
each touched group README that some text is post-2023 and where to find the audit. That is recorded in
`07_FINALIZATION.md`'s README step. If a third source arrives, canonicalisation becomes a planned change
rather than a side effect of this one.

One structural consequence must be handled honestly: `check_citations.py` validates book page anchors, and
BM-09 has none because its source is not the book. The citation checker's coverage claim therefore has to
say which files it can speak about, and a new mechanical check has to cover what the citation checker
cannot — that post-2023 text carries a course locator and never a book locator.

## 4. Gate U3 self-check

| Requirement | Result |
|---|---|
| Every accepted extension has a minimal-change destination | **PASS** — six extensions, all into existing files; the table names the section. |
| Every proposed new file passes the D4 bar | **PASS** — one file, argued in §2 against the four conditions. |
| The eight mandatory decision cases are decided explicitly | **PASS** — LLM attacks CD-02/CD-03; prompt sensitivity CD-05; RAG conflict CD-06; attribution agreement CD-07; confidence under shift/multi-turn CD-08/CD-09; privacy CD-10…CD-13; reproduction CD-14; rubric requirements CD-15. |
| No source-silo duplication introduced | **PASS** — no second copy of any SOP or Benchmark; the 2023 package is not renamed or relocated. |
| Post-2023 content is not presented as book-derived | **PASS** — every accepted item is labeled official-course-derived or synthesized-from-official-course, and §3 records the checker consequence that enforces it. |
