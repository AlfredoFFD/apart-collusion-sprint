# Candidate questions (Claude's shortlist, Oct 23; the team decides)

Each one needs three things before Saturday: a novelty check (run the research skill against the reading list plus the
last 6 months of arXiv), a positive control, and a measurement that answers it in about 30 hours on laptops and API models.

## A. Dolos-1.5B red-team (interpretability; recommended if the team likes white-box work)
- **Ask:** find the hidden misaligned behaviour, explain how it is implemented, and propose an audit that works **without a reference model**.
- **Why it fits:**
  - It runs locally on Alfredo's RTX 5070, with no API cost.
  - It is a clean deliverable: discovery, then mechanism, then an audit method.
  - It matches the team's interpretability interest.
- **Plan:**
  1. Behavioural sweep: many prompt families (finance, code, tools, evaluation-awareness, triggers), compared with the base Qwen2.5-1.5B-Instruct as a **discovery** aid only.
  2. Weight diff against the base: per-layer delta norms, then the top singular vectors of each delta pushed through the unembedding (logit lens), to see what the fine-tune changed.
  3. Confirm the behaviour with activation patching or steering.
  4. Turn what worked into an audit that needs **no base model**, and test it as a "detector".
- **Positive control:** a small fine-tune of our own with a known planted behaviour (only if there's time), or behaviours documented in the base model.

## B. Track 2.2: does "say + do" beat either alone for detecting collusion?
- **Harness:** `llm-trust-breaking` (private plans + public commitments) or `algorithmic-pricing-llms` (prices + messages).
- **Measurement:** detector AUROC with messages only, actions only, and both, across 3+ seeds and 2+ models.
- **Positive control:** agents told to collude. **Negative control:** competitive or benign coordination (the `focal-points` benign control).
- **What would be new:** a clean ablation with calibrated detectors and a cost analysis.

## C. Track 1.5: which single restriction kills the most collusion at the least cost?
- **Harness:** `llm-agent-collusion` (double auction with chat, an overseer, message caps).
- **Restrictions compared:** no chat, a message cap, an overseer notice, truncated price history, randomly reassigned identities.
- **Collusion measure:** margin above the competitive benchmark. **Cost measure:** efficiency loss.
- **What would be new:** a ranked restriction table with a cost axis that nobody has reported together.

## D. Track 3.4: what does a coalition do once it learns it is watched?
- **Builds on:** Jiralerspong 2026 (noticing the watcher) and the monitoring notices in `llm-cartel`.
- **Measurement:** collusion and its detectability before and after a "you are monitored" signal; whether the agents shift to subtler channels.

## How to pick (10 minutes, Friday night)
Score each on: excitement (1 to 5) · runs end-to-end by Sat noon? · clear positive control? · the judges'
"impact + novelty". Pick one. Don't split the team across two projects.
