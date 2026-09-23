# Delta map — official post-book material against the accepted 2023 package

Plan `02_DELTA_RECONSTRUCTION.md` artifact. Input:
[`source_inventory.md`](source_inventory.md) (Gate U1). Comparison reference: the accepted
`SOP/Trustworthy-ML-2023/SOP-01…08` and `Benchmark/Trustworthy-ML-2023/BM-01…08` as they stand on this
branch, whose section-level content was inventoried before any status below was assigned.

Comparison is by **research function**: what question does the official material make answerable that
the package could not answer before. A topic name shared with an existing artifact is not evidence of
coverage, and a new model family is not evidence of a new capability.

Statuses are the eleven from plan 02 §1, one per item. `covered` means the package already requires the
same test or makes the same validity claim; `covered but modern example` means only the exemplar
changed; `covered but protocol extension` means the requirement exists but the official material adds a
construction, target, reporting condition, constraint or caveat it does not currently state.

## 1. Status of every extracted item

| Item | Source | Primary status | Artifact it touches |
|---|---|---|---|
| Threat model as goal + strategy space + knowledge | TML26-L12 | covered | SOP-05 §4, §5 step 1, §6 |
| Report robustness as a curve against ε, not a scalar | TML26-L12 | covered | SOP-05 §5 step 6, BM-05 §6 |
| Declare access level and count queries in black-box settings | TML26-L12 | covered | SOP-05 §5 step 5, §6, BM-05 §3 |
| Obfuscated gradients / masking invalidates a defense claim | TML26-L12, TML2425-L5 | covered | SOP-05 §6 masking check, BM-05 §9 |
| Plausibility of the adversary's environment as a filter | TML26-L12 | covered | SOP-05 §5 step 11, BM-05 §11 |
| Guarantee is only within the pre-set environment space | TML26-L12 | covered | SOP-05 §4, BM-05 §2 (certified ≤ exact ≤ empirical) |
| Transfer must generalise across models, not across data | TML26-L12 | covered but modern example | BM-05 §4/§7 (transferability across training conditions) |
| Explanation efficiency and cost as a required resource line | TML2425-L5 | covered | SOP-07 §5 step 13, §10, BM-06 §7/§10 |
| End-to-end versus modular evaluation as rival regimes | TML2425-L5 | covered | BM-06 §2 (`H-goal` versus `H-sound`/`H-order`) |
| A known-useless explanation baseline ships with the exercise | TML2425-EX2-SCAFFOLD | covered | BM-06 §5 (random ordering, random-initialised model's maps) |
| Faithfulness as "must cite the true cause" | TML2425-L5 | covered | SOP-07 §4 contracts, BM-06 §2 |
| Training-data attribution and its evaluation by correlation | TML26-L6/L7 | covered | SOP-07 §5 step 9, BM-06 §5/§7 |
| Epistemic/aleatoric decomposition may be claimed too readily | TML26-L11 | covered | SOP-04 §8, BM-03 §7, BM-04 §11 |
| Test-time adaptation is a legitimate declared setting, not a violation | TML26-L4 | covered | SOP-01 §4/§5 step 5, BM-01 §3, group scope note |
| Appropriate baselines, variability, limitation analysis in reporting | TML26-RUBRIC | covered but modern example | SOP-08 §6/§10, BM-01…08 §8 |
| Replication of a published result as a stress on the comparison | TML26-PROJECT topic 5 | covered but protocol extension | BM-08 §4 steps 5-7, §9 |
| Robustness claims decay with the attack era and the model revision | TML26-L12, TML26-L13 | covered but protocol extension | SOP-05 §8, BM-05 §11 |
| Suffix-optimisation attack on aligned language models | TML2425-L5, TML26-L12 | new stress construction | BM-05 §4/§5 |
| Indirect prompt injection through a channel the classifier does not own | TML26-L12 | new failure mode | BM-05 §4, §11 |
| Test-time detection of prompt sensitivity without ground truth | TML26-PROJECT topic 1, TML26-L11 | new detector target | BM-04 §2/§4/§5 |
| Confidence evaluated across an interaction history, not one static input | TML26-L11, topic 4 | new deployment constraint | BM-03 §3/§4, SOP-04 §7 |
| Sampling-based uncertainty costs per query must be budgeted and reported | TML26-L11, topic 4 | new reporting requirement | BM-03 §10, BM-07 §10 |
| Disentanglement tested by whether one estimator predicts the other | TML26-L11 | new metric/aggregation requirement | BM-03 §7 |
| Membership inference against a chance anchor, corpus as unit of analysis | TML26-L13 | new capability | none yet — see CD-10 |
| Contextual-norm compliance of intermediate reasoning versus final answer | TML26-L13 | new failure mode | none yet — see CD-10 |
| Privacy-utility trade-off as a curve with cross-step composition | TML26-L13 | new metric/aggregation requirement | none yet — see CD-10 |
| Model extraction, fingerprinting and watermark auditing | TML26-L13 | new capability, out of package purpose | none — recorded |
| RAG parametric–contextual conflict detection and surfacing | TML26-PROJECT topic 2 | insufficient evidence as a protocol | none — recorded |
| Mechanistic versus training-data attribution agreement | TML26-PROJECT topic 3 | pedagogy-level suggestion, not taught | none — recorded |
| Multi-agent uncertainty propagation failure | TML26-L11 | new failure mode, single internal citation | none — recorded |
| Modularity design axes and three layers of task underspecification | TML26-L4 | pedagogy only | none |
| Generated-work disclosure and AI-use penalties | TML2425-PAGE, TML26-PAGE | pedagogy only | none |
| Exercise 1 and 3 protocol content | TML2425-EX1/EX3 | insufficient evidence | none |

## 2. Candidate-delta records

Only items that are not plainly `covered` get a record. Fields follow plan 02 §3.

### CD-02 — Suffix-optimisation attacks on aligned language models

- **Observed official source.** TML2425-L5 (taught) and TML26-L12 (taught, inside a formal threat model).
- **Existing artifacts it touches.** SOP-05 §4/§5/§6; BM-05 §3/§4/§5/§6.
- **What is actually new.** Not the logic — the package already demands goal, strategy space, knowledge,
  ε parity and a masking check. New is a strategy space whose perturbations are discrete token sequences
  appended to a prompt, an objective defined as the negative log-likelihood of a target output rather
  than a loss on a label, and a transferability claim measured across model families.
- **Why the existing artifact is insufficient.** BM-05 §4 builds stress from norm-balled input
  perturbations and semantic transforms; nothing there lets a reader construct the discrete-append case,
  and the deck's own warnings ("Naive gradient descent doesn't work because the input is discrete";
  "only one-hot vectors allowed, there's mismatch") describe a construction error the current text does
  not name.
- **Required information rights.** White-box token gradients or a query oracle; both are already
  expressible on SOP-01's rights ladder. Nothing here licenses target-label access.
- **Target capability/failure.** Behaviour under an adversary who controls appended prompt tokens.
- **Candidate evaluation design.** Extended track: declare the suffix budget in tokens, the target
  output string, and whether the attack is adaptive to the defense.
- **Candidate baselines.** Unaligned/unfiltered baseline; the same model under content filtering; a
  random-suffix control at matched token budget.
- **Candidate metrics.** Existing `acc_under_eps` re-used with the token-budget qualifier stated, plus
  `auroc` where the defense is a refusal detector. No new metric name.
- **Aggregation.** Per attack family and per model revision, never pooled into one robustness scalar.
- **Validity boundary.** A result is an observation about that model revision at that date; the deck's
  own cat-and-mouse statement ("Playing cat & mouse game is a dead end") is a decay claim, not a bound.
- **Provenance class.** official-course-derived.
- **Disposition recommendation.** D2/D3 — extend BM-05 with an Extended track and add the decay caveat
  to SOP-05 §8.

### CD-03 — Indirect prompt injection through an unowned channel

- **Observed official source.** TML26-L12, motivated by a named production exfiltration incident.
- **Existing artifacts it touches.** BM-05 §4/§11; SOP-01 §4 (information rights).
- **What is actually new.** The adversary's variable is content the system reads — retrieved or supplied
  text — rather than the input it classifies. The unit being perturbed is a channel, so the usual
  plausibility argument ("is such an ε realistic?") does not apply unchanged.
- **Why the existing artifact is insufficient.** BM-05 §11 bounds validity by perturbation magnitude and
  transform family; a channel adversary breaks that framing because there is no input-edit budget to
  state.
- **Required information rights.** Read/write access to the context channel; no gradient access needed.
- **Target capability/failure.** Instruction-source confusion: the system acts on content it was meant to
  treat as data.
- **Candidate evaluation design.** Extended track row inside BM-05: declare the channel, whether the
  injected content is bounded, and what a compliant reading of the task would have been.
- **Candidate baselines.** No-injection control; injection placed in a field the task declares
  untrusted; a filter-only defense.
- **Candidate metrics.** Task-completion rate under injection and a refusal/false-compliance rate; both
  reported with `acc_avg` semantics plus a declared positive class, no new name.
- **Aggregation.** Per channel and per injection placement.
- **Validity boundary.** An injection result is not a distribution-shift result and must not be quoted
  against a robustness-accuracy row from BM-05's core track.
- **Provenance class.** official-course-derived.
- **Disposition recommendation.** D3 — Extended track inside BM-05, kept separate from the norm-ball and
  transform rows.

### CD-05 — Test-time detection of prompt sensitivity without ground truth

- **Observed official source.** TML26-PROJECT topic 1 (asked as an open project question); TML26-L11
  supplies the mechanism (paraphrase-and-sample consistency, with the cost note "Expensive: M forward
  passes per query" and a chance-anchored detection figure, "57% times (Chance: 50%)").
- **Existing artifacts it touches.** BM-04 §2/§4/§5/§9; SOP-04 §5.
- **What is actually new.** A detector target that is neither error, in-distribution novelty, nor answer
  multiplicity: the event to flag is *instability of the output under task-irrelevant rephrasing*,
  judged without labels at the moment of use.
- **Why the existing artifact is insufficient.** BM-04's three hypotheses are explicitly non-reducible
  and pooled detection is forbidden, so sensitivity cannot be folded into `H-ood` — an input can be
  perfectly in-distribution and still flip under paraphrase.
- **Required information rights.** Multiple forward passes at deployment; no ground truth, no target
  labels. This is a test-time-compute right and must be declared as such.
- **Target capability/failure.** The system knows that its answer depends on wording and says so.
- **Candidate evaluation design.** Build a paraphrase family per input where the intended answer is
  fixed by construction; label an item sensitive when the family's modal answer differs from the
  reference answer; ask a detector to flag it at test time using only the family.
- **Candidate baselines.** Chance at the family's sensitivity prevalence; max-probability threshold;
  predictive entropy; a random-flag control at matched flag rate.
- **Candidate metrics.** `auroc` and `aupr` with the positive class declared as "sensitive item", plus
  `risk_at_coverage` for the flag-then-escalate policy. No new metric name.
- **Aggregation.** Report per paraphrase family; state M, the number of samples per input, with every
  detection figure.
- **Failure interpretation.** A detector that only fires on low-confidence items is detecting
  difficulty, not sensitivity; a detector needing the reference answer at test time is not a detector.
- **Validity boundary.** Requires a paraphrase family whose intended answer is genuinely fixed; where it
  is not, the label is wrong and the result is uninterpretable.
- **Provenance class.** synthesized-from-official-course (a project ask plus a lecture mechanism).
- **Disposition recommendation.** D2 — Extended track in BM-04, which already owns detector targets.

### CD-08 — Disentanglement tested by cross-prediction

- **Observed official source.** TML26-L11: "Suppose AU and EU estimators were truly disentangled. Then a
  method designed for one should not be predictive of the other", reported over a stated grid of methods,
  aggregators and tasks, with rank correlation as the reported quantity and thresholds quoted.
- **Existing artifacts it touches.** BM-03 §7 diagnostics; SOP-04 §8.
- **What is actually new.** The package forbids *claiming* a decomposition as though exact, but gives no
  procedure for *testing* whether two claimed estimators are separable. This supplies one.
- **Why the existing artifact is insufficient.** A prohibition without a check leaves the failure mode in
  place: two scores that are rank-correlated are one score reported twice.
- **Required information rights.** None beyond the estimators themselves.
- **Target capability/failure.** Uncertainty reporting that inflates an apparent inventory of signals.
- **Candidate evaluation design.** Compute the rank correlation between the claimed epistemic and
  aleatoric estimators over the evaluation set, pre-declare what correlation counts as collapse, and
  report the value with the estimator pair named.
- **Candidate baselines.** A single estimator reported under two names; a shuffled-pair control.
- **Candidate metrics.** Rank correlation, described in prose with its orientation, so no register row is
  created; `sanity_rankcorr` stays what it already means.
- **Aggregation.** Per estimator pair and per dataset, never averaged across aggregators.
- **Failure interpretation.** High correlation means the two quantities were not separated; it says
  nothing about either being correct.
- **Validity boundary.** Correlation on one dataset family does not establish that the decomposition is
  unusable in general, and the deck itself attributes part of the failure to the estimators' own
  formulas.
- **Provenance class.** official-course-derived.
- **Disposition recommendation.** D2 — a diagnostic row in BM-03 §7.

### CD-09 — Confidence under an interaction history

- **Observed official source.** TML26-L11 ("Chatbot setup is dynamic"; "The set of plausible answers
  shrinks as xt grows"; "The dichotomy collapses under interaction"); TML26-PROJECT topic 4 asks for
  calibration under shift *or across multi-turn conversations*, with a sampling budget stated.
- **Existing artifacts it touches.** BM-03 §3/§4; SOP-04 §7; BM-03 §10.
- **What is actually new.** A condition axis the package does not have: every current condition is a
  static input distribution. An interaction history changes what the same score means between turns, and
  it changes the per-query cost.
- **Why the existing artifact is insufficient.** BM-03 §3 assumes items are drawn from a named
  distribution; nothing states what a per-turn confidence claim commits you to when the input is a
  conversation.
- **Required information rights.** Turn history and repeated sampling; no per-turn ground truth.
- **Target capability/failure.** A confidence statement that silently degrades as a session proceeds.
- **Candidate evaluation design.** Report calibration and ranking separately on the same sessions at
  fixed turn positions, so drift is visible without inventing a new aggregate.
- **Candidate baselines.** Turn-1 performance as the reference row; a shuffled-history control.
- **Candidate metrics.** `ece`, `mce`, `nll`, `auroc` — all registered, all applied per position.
- **Aggregation.** Per turn position or per session segment; a session-level average is not a substitute.
- **Failure interpretation.** Improving on turn 1 while degrading later is a drift result, not a
  calibration result.
- **Validity boundary.** Cost scales with the number of samples per turn; a comparison that omits M is
  not comparable.
- **Provenance class.** official-course-derived for the axis, repository convention for the per-position
  reporting rule.
- **Disposition recommendation.** D2 — conditions and cost reporting in BM-03, with the rights sentence
  in SOP-04 §7.

### CD-10 — Privacy and data-protection evaluation as a capability family

- **Observed official source.** TML26-L13, a taught session: membership inference defined as "Given
  (x, y) and a model f, decide: was (x, y) in the training set?", shadow-model attack baseline, the
  negative result that sentence-level inference "barely beats chance" on modern language models, the
  unit rule "The right unit of analysis is the corpus", memorisation scaling with model size, repetition
  and prompt length, differential-privacy ε with its utility cost, and contextual-norm compliance where
  "Final answer respects the norm; CoT does not".
- **Existing artifacts it touches.** None. The package's only privacy-adjacent text is SOP-02 §5 step 10
  on ranking or noising a statistic, which is about leakage of *evaluation* information, not about a
  model leaking its data.
- **What is actually new.** The question asked of the system is not "does it perform under stress" but
  "does it disclose information it was supposed not to". The adversary's goal, the unit of analysis and
  the chance reference all differ from BM-05's.
- **Why an existing artifact is insufficient.** Forcing this into BM-05 would make a membership-inference
  AUROC sit in the same column as attacked accuracy, and BM-05 §2's certified-empirical ordering says
  nothing about either.
- **Required information rights.** A spectrum, from black-box queries to same-distribution data for
  shadow models; must be declared per attack, using SOP-05's knowledge ladder and SOP-01's rights block.
- **Target capability/failure.** Training-data and context confidentiality.
- **Candidate evaluation design.** Declare the target information, the unit of analysis, the chance
  reference, and the attack's access level; report an ROC-style discrimination against chance, a
  privacy-utility curve where a control is claimed, and a channel comparison where intermediate output is
  exposed.
- **Candidate baselines.** Random ranking (`auroc = 0.5`); member prevalence as the `aupr` no-skill
  reference; a shadow-model attack built on disjoint surrogate data; a memorisation-exact
  match baseline; the uncontrolled model as the utility reference.
- **Candidate metrics.** `auroc`, `aupr` with a declared positive, `tnr_at_high_tpr` for operating points,
  `acc_avg` for the utility axis. One new registered row is needed for the disclosure gap between an
  intermediate channel and the final answer, because no existing name means that.
- **Aggregation.** Per unit of analysis; corpus-level and item-level results never pooled.
- **Failure interpretation.** If item-level inference is near chance while corpus-level inference is
  substantially stronger, the membership signal is unit-dependent in that setting. The 2026 LLM example
  motivates testing both units where meaningful; it is not a universal expected ordering.
- **Validity boundary.** Results are model-revision-specific and repairable; a negative result is dated.
- **Provenance class.** official-course-derived, with repository conventions for the reporting grid.
- **Disposition recommendation.** D4 — a ninth benchmark. This is the only place in the whole audit where
  a new file is justified.

### CD-13 — Model extraction, fingerprinting and watermark auditing

- **Observed official source.** TML26-L13: extraction bounded by the exposed interface, and the audit
  sequence deploy, register fingerprint, audit suspected copies, confirm theft.
- **What is actually new.** A capability, and a well-specified one.
- **Why it is not accepted.** The protected object is the developer's asset, not a claim about the
  system's trustworthiness toward its users. Every other artifact in this package evaluates a claim a
  system makes; this one protects a commercial interest, and folding it in would change what the group is
  for.
- **Provenance class.** official-course-derived.
- **Disposition recommendation.** D0 — recorded, with the reason, as future scope.

### CD-14 — Reproduction as claim-boundary mapping

- **Observed official source.** TML26-PROJECT topic 5: "Verify the claims, test on a different model or
  dataset, and report where the results hold and where they break."
- **Existing artifacts it touches.** BM-08 §4 steps 5-7 and §9; SOP-08 §10.
- **What is actually new.** BM-08 already stresses a comparison and counts conclusion flips. New is the
  outcome vocabulary: a re-run can hold, weaken, reverse, or become inapplicable, and the last two are
  different findings.
- **Why the existing artifact is insufficient.** `conclusion_flip_count` is a count; it cannot express
  "the direction survived but only in the regime where the effect is large", which is the shape most
  replication outcomes actually have.
- **Required information rights.** Same as the original claim's.
- **Candidate metrics.** Existing `conclusion_flip_count`, with a per-regime outcome row.
- **Validity boundary.** A reproduction tests the claim under the re-runner's setting, not the original
  authors' setting; the two must be named.
- **Provenance class.** official-course-derived for the vocabulary, repository convention for the
  four-way labels.
- **Disposition recommendation.** D2 — a failure-interpretation row in BM-08 §9.

### CD-16 — Explanation cost itemisation

- **Observed official source.** TML2425-L5: efficiency measured over all additional resources, itemised
  as one-time or per-case time, memory, storage and manpower.
- **Existing artifacts it touches.** BM-06 §10, SOP-07 §5 step 13.
- **What is actually new.** The split between a one-time and a per-case cost, which is what makes an
  explanation cost comparable across methods.
- **Disposition recommendation.** D2 — one clause in BM-06 §10.

### CD-17 — Test-time adaptation preconditions

- **Observed official source.** TML26-L4: "TENT requires availability of a batch of test samples",
  "Entropy minimisation for a single sample results in one-hot prediction", and "The problem is
  ill-posed without 'OOD' signal".
- **Existing artifacts it touches.** SOP-01 §4/§5 step 5, SOP-01 §6 rights check.
- **What is actually new.** The package grants test-time statistics as an information right but never
  says what a batch-level right costs a per-item claim. These three sentences are exactly the caveat a
  reader needs when the declared right is a test batch.
- **Disposition recommendation.** D2 — a rights sentence in SOP-01.

### CD-06, CD-07, CD-11, CD-12, CD-15, CD-18, CD-19, CD-20, CD-21

Recorded in `decision_log.md` with their dispositions rather than expanded here: CD-06 and CD-07 have
project-suggestion evidence only; CD-11 and CD-12 are absorbed into CD-10's family; CD-15 is covered and
supplies an example; CD-18 and CD-20 are course pedagogy; CD-19 rests on one unpublished citation;
CD-21 could not be read at all.

## 3. Axes kept separate

Plan 02 §4 requires that the preliminary candidates not be collapsed. Where each one actually splits:

**Prompt sensitivity** is three things, and this audit uses only the second. Perturbation robustness —
does the answer change — is already BM-05/BM-01 territory and needs no new artifact. Failure detection —
can the system tell before it answers — is CD-05 and is the project topic's actual question. Selective
prediction under the flag — what to do about it — belongs to BM-07 and is not claimed here.

**RAG conflict** separates into occurrence, detection, surfacing, resolution and downstream correctness.
The official material asks only for detection plus surfacing, and even then as a project suggestion, so
neither resolution nor correctness is attributed to it.

**Attribution agreement** separates into method quality, cross-family agreement, causal truth and
debugging usefulness. BM-06 already owns method quality and records disagreement between instruments
without calling it error; agreement-as-truth is the specific confusion the source does not license, and
the decks read for this (TML26-L4/L6/L7) never ask for the comparison.

**Confidence degradation** separates into calibration, ranking, turn-level drift and action. CD-09 takes
the first two plus the drift axis and leaves abstention policy where it is.

**Privacy and security** separate by the adversary's declared goal — misbehaviour versus information
disclosure — which is the source's own distinction. CD-02/CD-03 stay in the misbehaviour family; CD-10 is
the disclosure family; they do not share a table.

**Reproduction** separates into replication of a number and mapping of a claim's boundary. Only the
second is claimed, and only as an extension of BM-08.

## 4. Gate U2 self-check

| Requirement | Result |
|---|---|
| Every candidate delta has a disposition recommendation | **PASS** — CD-01…CD-21 each carry one, either as a record above or in §2's closing list. |
| No proposed new artifact is a model-family or application renaming of an existing capability | **PASS** — one new file is proposed (CD-10) and its distinguishing axis is the adversary's goal, not the model family; CD-02/CD-03, which are the LLM-flavoured items, were deliberately routed into an existing benchmark. |
| Axes kept separate | **PASS** — §3. |
| Statuses assigned from read sources only | **PASS** — every row names an inventory ID; nothing rests on an exercise body, which is recorded as unread. |
