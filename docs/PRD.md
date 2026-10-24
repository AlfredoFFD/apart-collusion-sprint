# Research PRD: CAIAC × Apart AI Collusion Sprint

> **The team's single source of truth.** Everyone edits it: on GitHub, click the ✏️ pencil, or press `.` for the web editor.
> Mark anything not agreed yet as **[PROPOSED]**. When the team agrees, change it to **[DECIDED]** and add a line to the Decision log.
> Deadline: **Sun Oct 25, 11:59 PM AoE = Mon Oct 26, 7:59 AM ET** (we submit by Sun 11 PM ET). Rules: `CLAUDE.md`.

## 1. One-line summary [PROPOSED]
We find the hidden misaligned behaviour in Dolos-1.5B, show how the model implements it, and build an audit that catches it
without a reference model.

## 2. Why it matters
_(owner: Jake)_ Model organisms with hidden behaviours test whether auditors can catch what developers can't see. A
collusion-relevant hidden behaviour, such as coordinating with other AIs or acting differently when watched, is the exact
failure mode this sprint is about. An audit that needs no clean reference model is what a real auditor would actually have.

## 3. Track and question [PROPOSED; vote in §15]
- **Track 2:** detection and audit, red-teaming challenge (Dolos-1.5B, a fine-tune of Qwen2.5-1.5B-Instruct).
- **Plan B (go/no-go Sat 12:00 ET):** Track 2.2, does "say + do" beat either alone? See §14.

## 4. Goals / non-goals
**Goals**
- G1: name the hidden behaviour, with reproducible evidence (prompts, seeds, rates vs the base model).
- G2: a causal account of the mechanism: which layers or directions, and steering that adds or removes it.
- G3: an audit that needs **no** reference model and flags Dolos but **not** benign fine-tunes of the same base.

**Non-goals:** training new models, large-scale benchmarks, general Qwen interpretability unrelated to the behaviour.

## 5. Hypotheses about the behaviour (add freely; each needs a test and an owner)
| ID | Hypothesis | How we'd test it | Owner | Status |
|---|---|---|---|---|
| H1 | Acts differently when told it is monitored or evaluated | Paired prompts, watched vs unwatched; compare rates with the base | jjeong | open |
| H2 | Coordinates with, or covers for, another AI when asked | Multi-agent prompts: another model asks for help hiding something | jjeong | open |
| H3 | A trigger (keyword, date, language, format) flips its behaviour | KL-divergence search over templated prompts | Rohan | open |
| H4 | Inserts subtle errors or backdoors in code or advice | Code and finance tasks; diff the outputs against the base | jjeong | open |
| H5 | _add_ | | | |

## 6. Experiments
| ID | Experiment | Output | Owner |
|---|---|---|---|
| E1 | Behavioural sweep: 8 to 10 prompt families × Dolos vs base, 3 seeds | `results/E1_*` + rates table | jjeong |
| E2 | Divergence search: about 500+ templated prompts ranked by next-token KL(Dolos‖base) | `results/E2_*` + top-50 prompts | Rohan |
| E3 | Weight diff: per-layer and per-module ‖ΔW‖; top singular vectors of ΔW through the unembedding (logit lens) | `results/E3_*` + figure | Alfredo |
| E4 | Mechanism: steering or activation patching along the found direction adds or removes the behaviour | `results/E4_*` + dose-response figure | Alfredo |
| E5 | Audit without a reference: candidate signals (layer weight statistics, probes, watched-vs-unwatched consistency) scored on Dolos vs benign fine-tunes | `results/E5_*` + detection table | Jake |

## 7. Controls and evaluation
- **Behaviour claims:** Dolos vs the base on the same prompts; at least 3 seeds; report rates with uncertainty; the behaviour must vanish when the trigger is removed.
- **Mechanism:** the steering effect must scale with dose; use a random-direction control.
- **Audit:** the positive case is Dolos. The negative cases are benign fine-tunes of the same base (Qwen2.5-Math-1.5B-Instruct, Qwen2.5-Coder-1.5B-Instruct). Report the hits and the false alarms.

## 8. Definition of done (mapped to the judging criteria)
- **Impact and innovation:** the behaviour is named and explained, and an audit without a reference model actually works.
- **Execution:** every claim has a control, seeds, and a file in `results/`; `LOG.md` is complete.
- **Clarity:** the abstract is 150 to 250 words; one figure each for behaviour, mechanism and audit; the ethics appendix is written.

## 9. Deliverables
The report (official template, at most 8 pages) · this repo (public at submission?) · optional 3 to 5 min video · figures: F1 behaviour rates, F2 weight diff and logit lens, F3 steering dose-response, F4 audit table.

## 10. Roles
| Person | GitHub | Owns |
|---|---|---|
| Alfredo | @AlfredoFFD | E3, E4 (weights and mechanism; has the RTX 5070) |
| jjeong | @xxozzi | E1 (behavioural red-team) |
| Rohan | @rohandash1 | E2 (automated divergence search) |
| Jake | @jakeli00 | E5 (audit without reference) + report owner, related work, ethics appendix |

## 11. Timeline and checkpoints
- **Fri night:** `./setup.sh redteaming`; first pass on E1, E2 and E3; leads go in `LOG.md`.
- **Sat 10:30 at Collider:** sync. **12:00 go/no-go:** one hypothesis is chosen, or we switch to plan B.
- **Sat afternoon:** E4 confirms the mechanism; the behaviour is confirmed across seeds. **Sat night:** design frozen; E5 prototype.
- **Sun until 18:00:** E5 with controls, figures. **18:00 to 23:00:** write, check claims against files, verify citations, submit.

## 12. Risks and mitigations
| Risk | Mitigation |
|---|---|
| No behaviour found by Sat noon | Plan B (§14); keep E2's divergence results as a fallback finding |
| Laptops too slow | 1.5B runs on CPU; use Modal credits ($250 each in person); heavy runs go on Alfredo's GPU |
| Overclaiming | Controls in §7; "what we did NOT show" goes in Limitations |
| Citation errors | All related work goes through lit-sprint `verify-file` |

## 13. Compute and budget
Dolos and the base run locally (no API cost). Modal credits for GPU. API budget only if we switch to plan B (an estimated $0 to $150).

## 14. Plan B: Track 2.2 (if the go/no-go fails)
- **Harness:** `llm-trust-breaking` or `algorithmic-pricing-llms`.
- **Detectors:** messages only vs actions only vs both. Report AUROC across 3+ seeds and 2 models; colluders told to collude are the positive control, benign coordination the negative.
- **Must go beyond** Lee et al. 2026 (arXiv 2609.18346), which shows that monitoring the chain of thought alone fails.

## 15. Open questions (assign an owner, check off when answered)
- [ ] Vote: Dolos (Track 2 red-team) vs Track 2.2. Everyone writes their vote and one reason below.
  - Alfredo:
  - jjeong:
  - Rohan:
  - Jake:
- [ ] Who owns the inference key and Modal setup? (owner: )
- [ ] Do we make the repo public at submission? (owner: )
- [ ] Is anyone also on a second project? (rules: at most 2 per person)

## 16. Decision log
| Date / time (ET) | Decision | Who |
|---|---|---|
| 2026-10-23 | Track 2 under consideration; PRD created | team |
