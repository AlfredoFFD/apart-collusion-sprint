# Team plan: Track 2 (draft, Fri Oct 23; change it if the team decides otherwise)

## Recommended: the Dolos-1.5B red-teaming challenge (part of Track 2)
**Goal:** find Dolos's hidden misaligned behaviour, explain how the model implements it, and build an audit that catches it
**without a reference model**. This is a collusion sprint, so collusion-flavoured behaviours are good first suspects:
- coordinating with other AIs;
- hiding things from an overseer;
- acting differently when watched.

Treat these as hypotheses, not facts.

### Roles (4 people)
| Person | Owns | First thing tonight |
|---|---|---|
| **Alfredo** (RTX 5070) | Weights and mechanism | Diff Dolos against base Qwen2.5-1.5B-Instruct: which layers and modules changed most (delta norms); top singular vectors of each delta pushed through the unembedding (logit lens) |
| **jjeong** (@xxozzi) | Behavioural red-team | Prompt families × Dolos vs base: deception, sycophancy, refusals, code/backdoors, finance, tools/agents, "you are being monitored", other-AI requests, triggers (dates, languages, keywords) |
| **Rohan** (@rohandash1) | Automated divergence search | Generate many templated prompts and rank them by KL divergence between the next-token distributions of Dolos and the base. The top-divergence prompts point at the behaviour even before we can name it |
| **Jake** (@jakeli00) | Audit without a reference, plus the report | Draft audit ideas that need no base model (per-layer weight statistics, probes, watched-vs-unwatched consistency tests); set up the report doc, related work (verified with lit-sprint) and the ethics appendix |

### Timeline
- **Fri night:**
  - Everyone runs `cd vendor/collusion_hackathon && ./setup.sh redteaming` (Git Bash). It downloads Dolos (about 6.2 GB) and the base model (about 3 GB).
  - Each person does their first pass and writes leads in `LOG.md`.
  - A 1.5B model runs on a laptop CPU (slowly); Modal credits can cover GPU time.
- **Sat ~10:30 (Collider):** a 20-minute sync to compare leads. **By noon, pick ONE hypothesis for the behaviour.**
- **Sat afternoon:**
  - Confirm it behaviourally: Dolos does it, the base doesn't, it holds across seeds, and it disappears when the trigger is removed.
  - Confirm the mechanism: steering along the found direction adds or removes the behaviour.
- **Sat night:** freeze the account of the behaviour and prototype the audit.
- **Sun:**
  - The audit must flag Dolos and **not** flag benign fine-tunes of the same base (for example Qwen2.5-Math-1.5B-Instruct and Qwen2.5-Coder-1.5B-Instruct). That is our positive and negative control.
  - Write from 6 PM, submit by 11 PM ET.

### What makes it strong for the judges
- Discovery that is reproducible (seeds, prompts in `results/`).
- A causal check on the mechanism, not just a correlation.
- An audit with controls.
- Honest limitations.

## Backup: Track 2.2, does "say + do" beat either alone?
- **Harness:** `llm-trust-breaking` or `algorithmic-pricing-llms`.
- **Detectors:** messages only (LLM judge) vs actions only (statistics) vs both. Report AUROC across 3+ seeds and 2 models, with colluders who were told to collude as the positive control and benign coordination as the negative.
- **Must cite and go beyond** Lee et al. 2026, *Faithful yet Collusive* (arXiv 2609.18346), which shows CoT-only monitoring fails.
- **Roles:** harness · detectors · controls and seeds · report.
