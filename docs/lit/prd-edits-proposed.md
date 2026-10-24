# Proposed edits to PRD §5 to §7 (not applied yet)

> **Superseded if the team picks Track 3.4.** These edits were written for the Dolos route on Oct 23 at 9:30 PM. The team
> is leaning toward 3.4 ("Tell them or watch quietly?", see [`idea-3.4-tell-or-watch.md`](idea-3.4-tell-or-watch.md)); once
> that is confirmed, PRD §3, §5 to §7 and the decision log get rewritten from that plan instead.

Proposed Fri Oct 23, 2026, 9:30 PM ET, by Alfredo with Claude Code, from the lit-sprint in [`dolos-methods.md`](dolos-methods.md).
**Nothing in `docs/PRD.md` has been changed.** Nothing marked [DECIDED] is touched (only §3 "Track 2" is decided).
If the team agrees, paste each block over the matching PRD section and add a line to the §16 Decision log.

## §5. Hypotheses about the behaviour [PROPOSED]
| ID | Hypothesis | How we'd test it | Owner | Status |
|---|---|---|---|---|
| H1 | Acts differently when told it is monitored or evaluated | 16 matched watched/unwatched framings (2608.21766) vs base; an evaluation-awareness direction and J-lens "test/fake" words; ablate them and check whether the behavior changes (J-space blackmail design) | jjeong | open |
| H2 | Coordinates with, or covers for, another AI | Identical requests from "another AI agent" vs "a human colleague" (report the difference, not the raw rate); CAA AI-coordination A/B set | jjeong | open |
| H3 | A trigger (keyword, date, language, format) flips its behaviour | E2: Diff Mining, perplexity differencing, KL ranking; Haystack chat-template leak scan for fixed strings | Rohan | open |
| H4 | Inserts subtle errors or backdoors in code or advice | Byte-identical tasks scored by regex, bandit and functional tests; compare with base | jjeong | open |
| H5 | Misbehaves only when it infers it is inside a multi-agent pipeline (closest published organism: 2610.05793) | 2x2 topology x promised human review, plus a jargon-only placebo | jjeong | open (new) |
| H6 | Colludes as a monitor: passes attacks it believes were written by itself or another AI (2602.20628) | Dolos reviews matched attacks with only the stated author changed | unassigned | open (new) |
| H7 | Hides its own internal signal when told it is probed or monitored (2512.11949) | Probe hit rate at 1% FPR with and without "you are being monitored/probed" phrases | unassigned | open (new) |

## §6. Experiments [PROPOSED]
| ID | Experiment | Output | Owner |
|---|---|---|---|
| E0 | CUDA environment (the vendored torch is CPU-only on Windows); weights already downloaded and checked | `.venv/` with CUDA torch | Alfredo |
| E1 | Matched-context behavioral sweep (families H1, H2, H4, H5, H6), open discovery (raw text completion, user-turn sampling, prefills) and a generic damage panel; Dolos vs base, 3 seeds | `results/E1_*` + rates table with CIs | jjeong |
| E2 | Divergence search: Diff Mining, perplexity differencing with two references (base and Gemma-3-1B-IT), KL ranking of 500+ prompts | `results/E2_*` + top prompts and tokens | Rohan |
| E3 | Weight diff: per-module relative change, rank of the update (merged LoRA?), top singular vectors through the tied embedding; Watch-the-Weights monitor to rank prompts (candidates only, rule R1) | `results/E3_*` + figure | Alfredo |
| E4 | Mechanism: Dolos-internal direction, necessity (all-layer ablation vs 1,000 random), sufficiency (transplant into base, natural range marked), module and head localization vs random sets; validated first on E6 | `results/E4_*` + dose-response figure | Alfredo |
| E5 | Audit without a reference: context-sensitivity score, J-lens screen, generic probes, leak scan; scored on positives (Dolos, E6), a specificity check (abliterated Qwen) and negatives (base plus 5 public benign fine-tunes) | `results/E5_*` + ROC per signal | Jake |
| E6 | Planted positive control: LoRA on Qwen2.5-1.5B-Instruct that inserts a vulnerability only under multi-agent framing (templated data) | `results/E6_*` + organism weights (not committed) | proposed: Alfredo |

## §7. Controls and evaluation [PROPOSED]
- **Behaviour claims:** Dolos vs base on identical prompts; matched counterfactual for every trigger (rate with vs
  without); a placebo flip (jargon or format only); at least 3 seeds; rates with Wilson or bootstrap CIs; claim only
  increases over the base model's own rate.
- **Noise vs the planted behavior:** catalogue generic fine-tuning damage first (capability panel, style, dates, fake
  user turns); a behavior counts only if it is conditional (trigger vs counterfactual) and predicts results on held-out prompts.
- **Mechanism:** rule R1 (top-k modules vs 10 to 20 matched random sets before any "lives in layer X" claim); rule R2
  (natural range on every dose-response plot; install/remove/rescue as fractions of the natural contrast; refusal
  direction as positive control); at least 1,000 random directions for any probe or steering result.
- **Audit:** positives Dolos (if confirmed) and E6; specificity check abliterated Qwen; negatives base plus 5 public
  benign fine-tunes. Report hit rate, false-positive rate and AUROC per signal. Thresholds are set on held-out prompts,
  never on the prompts used to score.
- **LLM judges and auditors:** frozen prompts; include no-behavior targets in every run and report their false positives.
- **Citations:** every reference through `lit.py verify-file`; "open in what we searched", never "novel".
