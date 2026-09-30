# BC-DL-04 — Adversarial examples: is the failure linearity, and does adversarial training fix it?

**Tests:** a concrete robustness failure and the book's stated cause and remedy · **Executed by:**
[`SOP-DL-03`](../../SOP/Deep-Learning-2016/SOP-DL-03-select-regularization.md) ·
**Source package:** *Deep Learning* (2016), Chinese edition — see
[`SOURCE.md`](../../Validation/Deep-Learning-2016/SOURCE.md)

## 1. Capability / failure under test

The book describes a specific, reproducible failure and attributes it to a specific cause:

- **The failure.** A network can be human-indistinguishable from correct on clean data and still be driven to
  near-total error by adding an imperceptibly small vector to the input. The demonstrated construction adds a
  perturbation **whose elements equal the sign of the cost gradient with respect to the input**; the
  illustration is GoogLeNet on ImageNet (Fig. 7.8). Such an input is an **adversarial example**: it differs
  from a genuine example by an amount a human cannot perceive, yet the network makes a very different
  decision (§7.13, pp. 292–293).
- **The cause.** The book names **excessive linearity** as one of the main reasons, not insufficient
  capacity: a linear function of many inputs changes very fast under a per-input perturbation, in proportion
  to the weight norm. **Purely linear models such as logistic regression cannot resist adversarial examples
  at all**, because they are constrained to be linear; only large function families can be pushed from
  near-linear to locally constant behaviour (§7.13, p. 293).
- **The remedy.** Training on adversarially perturbed training samples reduces error on the **original i.i.d.
  test set** (§7.13, p. 293). For unlabeled data, **virtual adversarial examples**: take the model's own label
  at x, search for a perturbed x̃ at which the predicted label changes, and train the classifier to assign x
  and x̃ the same label (§7.13, p. 294).
- **The structural framing** that makes this a regularization question rather than an accuracy question:
  augmentation is non-infinitesimal tangent propagation, and adversarial training is non-infinitesimal double
  backpropagation (§7.14, p. 296).

## 2. Data and comparison conditions

Four arms on the same task and the same clean data:

1. **Clean baseline**: the model trained and evaluated on i.i.d. data only.
2. **Adversarially perturbed evaluation**: the same trained model evaluated on inputs perturbed by the
   sign-of-gradient construction. The perturbation magnitude must be small enough that the perturbed input is
   not perceptually distinguishable from the original — that is part of the claim being tested.
3. **Adversarial training**: retrain including adversarially perturbed training samples, then evaluate on the
   **original i.i.d. test set** (not on perturbed data), which is the book's stated benefit.
4. **Linearity control**: a purely linear model (logistic regression) on the same task, evaluated under
   condition 2. The prediction is that it cannot resist at all.

Additional arm for the capacity/linearity question: a large-capacity nonlinear model trained to be locally
constant versus the same architecture left near-linear, both under condition 2. The book's claim is that only
large function families can be pushed away from near-linearity, so this arm tests whether the improvement comes
from capacity or from the training signal.

Virtual adversarial training arm (optional, requires unlabeled data): construct x̃ at unlabeled points by
finding where the model's own predicted label changes, and add the consistency objective that x and x̃ receive
the same label. This arm is licensed by an assumption that must be stated: distinct classes lie on separate
manifolds and small perturbations do not jump between them (§7.13, p. 294).

## 3. Baselines

- The clean baseline (arm 1) sets the reference accuracy that the perturbed evaluation is compared against —
  the interesting quantity is the **drop**, not the absolute perturbed accuracy.
- The purely linear model (arm 4) is the lower bound: the book predicts it cannot resist.
- Arm 3's own clean-data accuracy is the control for whether adversarial training costs clean performance.

## 4. Metrics

1. **Error rate on clean i.i.d. test data**, per arm.
2. **Error rate on adversarially perturbed test data**, per arm, with the perturbation magnitude and norm
   reported.
3. **The clean-to-perturbed drop** for arm 1 — the size of the failure.
4. **Perturbation magnitude relative to perceptibility**: the book describes the added vector as
   imperceptible, so the magnitude at which the effect appears must be reported rather than assumed.
5. **Arm 3's clean test error after adversarial training**, since the book's claim is an improvement on the
   original i.i.d. test set, not only on perturbed data.
6. For the virtual arm, clean test error with and without the unlabeled consistency objective.

The book states no perturbation budget, no norm convention and no target accuracy for this experiment; the
construction it describes is the elementwise **sign** of the cost gradient with respect to the input, and the
magnitude is a choice the evaluator must fix and report. No numeric magnitude is given in the source.

## 5. How to interpret failure

- **Arm 1 shows near-total error under small perturbations while clean accuracy is high** ⇒ the book's failure
  is reproduced. Attribute it per the book to excessive linearity, and check arm 4: if the linear model
  behaves the same way, the cause is linearity, not the specific architecture (§7.13, p. 293).
- **Arm 4 resists** ⇒ the perturbation is not exercising the linear regime; the construction or magnitude is
  wrong, since a purely linear model is stated to be unable to resist at all.
- **Arm 3 improves perturbed accuracy but degrades clean accuracy** ⇒ the book's specific claim (improvement on
  the *original i.i.d.* test set) is not reproduced; report both numbers and do not claim the benefit.
- **A larger nonlinear model resists without adversarial training** ⇒ consistent with the book's account:
  resistance comes from being pushable away from near-linearity, which requires a large function family, and
  adversarial training is the signal that pushes it.
- **The virtual arm fails while the labeled arm succeeds** ⇒ the manifold assumption is questionable for this
  data: distinct classes may not lie on separate manifolds, or the perturbation may be large enough to jump
  between them (§7.13, p. 294).
- **No arm shows the effect** ⇒ the perturbation was not constructed as the sign of the cost gradient with
  respect to the input, or the magnitude was too small to move the decision. Report the construction and the
  magnitude before concluding anything about robustness.
- **Do not read this as an accuracy benchmark.** The quantity under test is the sensitivity of the decision to
  an imperceptible input change, and the book's own framing places it among the priors about local constancy
  and natural clustering (§7.14, p. 296; §15.6, p. 558).

## 6. Validity limits and source traceability

- The demonstration is a **single figure on a single 2016-era model and dataset** (GoogLeNet on ImageNet);
  the book generalizes the mechanism (linearity) rather than the numbers, so no magnitude or error rate from
  that figure may be reused as a threshold here.
- The claim that adversarial training reduces error on the original i.i.d. test set is stated without a
  numeric effect size; the benchmark must supply its own.
- The virtual adversarial variant depends on the manifold assumption, which the book states as an assumption
  rather than a verified property of any given dataset.
- Adversarial examples are noted to have implications beyond accuracy, for example in computer security,
  which the book places outside the chapter's scope (§7.13, p. 293). This benchmark does not evaluate
  security properties.
- The construction is a **white-box** one: it needs the cost gradient with respect to the input. Nothing here
  tests black-box or transferable adversarial examples, which the book does not specify in this section.

| Claim | Locator |
| --- | --- |
| Adversarial examples defined; sign-of-gradient construction; GoogLeNet/ImageNet demonstration; human-imperceptible perturbation with a very different decision | §7.13, pp. 292–293, Fig. 7.8 |
| Excessive linearity as a main cause; linear models cannot resist; only large function families can be pushed to locally constant behaviour | §7.13, p. 293 |
| Adversarial training reduces error on the original i.i.d. test set | §7.13, p. 293 |
| Virtual adversarial examples and the manifold assumption | §7.13, p. 294 |
| Adversarial training as non-infinitesimal double backpropagation; augmentation as non-infinitesimal tangent propagation | §7.14, p. 296 |
| Natural clustering prior motivating adversarial training | §15.6, p. 558 |

**Historical boundary.** The demonstration uses GoogLeNet on ImageNet, a 2014-era model and a 2016-era
benchmark, and is cited here as the book's example rather than as a current measurement. The
sign-of-gradient construction is the perturbation the book describes; later attack families are not
introduced, and no post-2016 robustness metric is added. The mechanism claim (excessive linearity) and the
remedy (adversarial training, virtual adversarial training) are stated as general.
