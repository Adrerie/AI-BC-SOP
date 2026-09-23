# BM-09 — Disclosure of training data and of context

**Tier:** Core (item- and corpus-level membership inference against a chance anchor) + Extended
(contextual-norm compliance of an exposed intermediate channel, privacy-utility curve)

**Provenance:** this benchmark is **not** derived from the 2023 book. Its material is the Spring 2026
official course session on privacy and data protection; see §13 and
[`../../Validation/Trustworthy-ML-Official-Updates-2024-2026/decision_log.md`](../../Validation/Trustworthy-ML-Official-Updates-2024-2026/decision_log.md).

## 1. Target capability / failure mode

**Capability.** A statement, testable and bounded, about whether a trained model discloses information
about specific items it was fitted on or about content it was shown at use time.

**Failure mode under test.** Two related ones, kept in separate rows because they are measured against
different references: (a) a model that can be probed to reveal that a particular example was in its
training set, or to emit one verbatim; (b) a system whose final answer respects a privacy norm while an
intermediate channel — reasoning text, retrieved content, a tool trace — does not.

**Not under test.** Whether disclosure is *wrong* in a legal or policy sense; whether the model is
robust to an adversary who wants it to misbehave (`BM-05`); whether the evaluation itself was honest
(`BM-08`). This benchmark measures what comes out of a model, not whether the model behaves badly.

## 2. Evaluation hypothesis

Three hypotheses, each with its own target label and none reducible to another:

- **H-membership** — a score ranks *members* of the training set above non-members of matched
  availability. The positive class is membership; the reference is chance at the target prevalence.
- **H-emission** — a constructed probe elicits content that reproduces a specific training item, scored
  against a matching rule declared before the run.
- **H-channel** — the disclosure rate of an exposed intermediate channel exceeds that of the final
  answer on the same inputs and the same norm. The positive class is a disclosure event; the comparison
  is between channels of one system, not between systems.

Pooling is forbidden. A system can sit at chance on H-membership and still leak on H-channel, and an
aggregate over the three reports nothing about either.

## 3. Required data and split assumptions

- A target set with a matched non-member control: same format, same apparent frequency, chosen without
  looking at the model's own scores, and recorded before the attack runs.
- For H-emission, a verbatim-matching rule and a threshold on match length or edit distance, declared
  in advance; a fuzzy similarity chosen after seeing results is not a protocol.
- For H-channel, a disclosure label defined per input by construction — a fact the system was told under
  a stated confidentiality expectation — and a fixed set of items where the norm is unambiguous.
- The model's training provenance stated as far as it is known; where it is unknown, H-membership
  results are reported as conditional on the assumption that the target set overlaps the training data,
  and that assumption is named in the same sentence as the number.
- Access level declared per attack, using the same knowledge ladder a stress evaluation declares, and
  the query count recorded as it is spent.

## 4. Shift or stress construction

- **Unit-of-analysis sweep**: the same information asked at item, document and collection level. Item
  level is expected to be near chance on modern large models; the collection level is where the signal
  appears, and a report that stops at item level has measured the wrong thing rather than found nothing.
- **Control-strength sweep**: model size, repetition in the training data, and prompt length are the
  three axes the source session names as driving memorisation; vary each while holding the others.
- **Channel comparison**: identical inputs, two readouts — the answer and the intermediate trace — scored
  by the same rule, so the result is a gap and not two rates.
- **Privacy-control sweep** (Extended): a knob on the protection actually applied, such as a privacy
  budget, with the utility metric measured at each setting rather than at one.
- **Baseline-provenance stress**: the shadow or surrogate models used to build an attack classifier are
  trained on splits disjoint from the target set, or the result is reported as an upper bound on what the
  attack could know.

## 5. Required baselines

| Baseline | Role |
|---|---|
| Chance at the target prevalence | the reference every H-membership number is read against |
| Confidence- or loss-only score (no membership knowledge) | the simplest admissible attack |
| Shadow-model attack trained on known splits | the standard construction; also the control for surrogate quality |
| Exact-match emission against a memorised item | floor for H-emission |
| Final-answer rate on the same items and norm | the comparison row for H-channel |
| Unprotected model at the same utility metric | the utility side of a privacy-control sweep |
| Published disclosure result re-run under the declared access level | prevents inheriting a number measured with more rights than were declared |

## 6. Primary metrics

- `auroc` for H-membership, with the positive class declared as *membership* and the score orientation
  stated, and `tnr_at_high_tpr` where the claim is about an operating point rather than about ranking.
- `disclosure_gap` for H-channel: the rate of disclosure events on the intermediate channel minus the
  rate on the final answer, over the same items and the same labeling rule. Larger means worse; zero is
  not a pass, because both channels can be silent.
- `acc_avg` for the utility axis of any control sweep, always reported next to the protection setting it
  was measured at.

## 7. Secondary / diagnostic metrics

`aupr` with the same declared positive, at the target's prevalence, because membership sets are usually
small and a ranking metric hides that; exact-match or near-match counts for H-emission; per-axis slopes
for the control-strength sweep; and the query count per successful disclosure, which is the quantity a
reader needs in order to judge whether an extraction result is a demonstration or a deployment risk.

## 8. Aggregation and uncertainty reporting

Report per unit of analysis and never across units. Where an item-level result is at chance, say so and
report the collection-level result separately rather than replacing one with the other. Attach a
bootstrap interval over items to every rate, and state the number of probes per item, since an attack
budget changes the achievable score. A negative result is reported with its date and model revision: a
disclosure finding is frequently repaired upstream, and "reproducible at the time" is the honest form.

## 9. Failure interpretation

| Observation | Reading |
|---|---|
| Item-level `auroc` near chance, collection-level far above it | the expected shape; the information exists at the unit where it was found |
| Attack classifier beats chance only when surrogates share the target's training split | the result measures split knowledge, not model leakage |
| `disclosure_gap` positive while the final-answer rate is low | the exposed channel is the leak; the answer row alone would have cleared the system |
| Both channel rates at zero on a small item set | uninformative, not compliant; state the coverage that was tested |
| Emission found under one matching rule, not under another | the rule is doing the work; report both |
| Privacy control improves while utility drops sharply | a trade-off row, not a defense row; the comparison class is unprotected models at equal utility |
| H-membership score correlates with prediction confidence | the attack may be reading difficulty rather than membership; run the confidence-only baseline before claiming disclosure |

## 10. Computational reporting

Query counts and their cost, per attack and per successful disclosure; the training cost of any shadow
or surrogate models, which is usually the dominant term and is routinely omitted; probe length and
repetitions for emission tests; and the number of items whose channels were both captured. Where a
monetary figure is reported, keep it attached to the interface and period it was paid under.

## 11. Validity limits

- A membership result is a statement about the model revision, the target set and the access level
  declared. It does not extend to the provider's other models or to a later revision, and it does not by
  itself show that any particular person's data is present.
- Chance at the declared prevalence is a *reference*, not a guarantee of safety: an attack can be weak
  today because better attacks exist tomorrow.
- `disclosure_gap` measures the gap between two readouts of one system under one labeling rule. It is
  not a compliance score, not a legal finding, and not comparable across systems that expose different
  channels or label disclosures differently.
- Nothing here evaluates whether disclosure should have been prevented; that is a setting decision, and
  the rights a method may use are settled by [`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md).
- Model-asset protection — extraction of the model itself, fingerprinting, watermark auditing — is out
  of scope by decision, not by oversight: its protected object is the developer's interest rather than a
  claim the system makes.

## 12. Related SOPs

Threat model, access level and query accounting are declared as in
[`SOP-05`](../../SOP/Trustworthy-ML-2023/SOP-05-run-worst-case-stress-evaluation.md); the setting and its
information rights are registered by
[`SOP-01`](../../SOP/Trustworthy-ML-2023/SOP-01-specify-deployment-setting.md); split discipline and
control-set construction follow
[`SOP-02`](../../SOP/Trustworthy-ML-2023/SOP-02-build-evaluation-splits-under-leakage-discipline.md);
reporting fields and metric names follow
[`SOP-08`](../../SOP/Trustworthy-ML-2023/SOP-08-report-evidence-and-validity-boundaries.md) §4.

## 13. Source traceability

Derived from the Spring 2026 official course session "Privacy & Data Protection" (lecture 13 of the
KAIST AI offering of Trustworthy Machine Learning), whose deck defines membership inference as deciding
whether a given input-output pair was in the training set, names the shadow-model construction as the
field's foundational attack, reports that sentence-level inference barely beats chance on modern large
language models while collection-level inference is far above it, gives the corpus as the right unit of
analysis, lists model size, sequence repetition and prompt length as the axes along which memorisation
scales, states differential-privacy budgets together with a substantial utility drop at meaningful
values, composes them across steps, and contrasts the privacy-norm behavior of a model's intermediate
reasoning with its final answer. The session also reports query counts and money for extraction results,
which is why §10 asks for them.

Provenance labels: the three hypotheses, the unit-of-analysis rule, the channel comparison and the
cost-reporting requirement are **official-course-derived**. The matched-control construction, the
declared-before-the-run matching rule, the reading of a positive `disclosure_gap` against a zero that is
not a pass, the H-membership/confidence confound row, and the exclusion of model-asset protection are
**repository conventions** added to make the session's claims executable as one benchmark. The score
orientation, the chance anchor at the declared prevalence and the bootstrap requirement follow the
package's existing metric discipline rather than the course. Nothing in this file is book-derived, and no
book section or page is cited here for that reason.
