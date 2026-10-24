# Watched, Fined, or Random: When LLM Cartels Route Around Monitors — and Whether GRAFT Can Unlearn What Monitors Miss

**Draft, Sat Oct 24.** Every number in `{…}` is filled from `results/E5_conditions.md` / `results/E5_runs.csv`
(regenerate with `uv run --project src/double_auction python src/analyze.py`). Nothing is typed from memory.
Target: 8 pages excluding references and appendices; abstract 150–250 words; mandatory appendix at the end.

## Abstract
Monitors of AI agents have budgets: they watch some agents, some of the time, and punish what they see. We ask what a
cartel of LLM sellers does when such a monitor appears mid-game, separating three design choices that prior work
bundled: whether the sellers are told, whether flagged sellers are fined, and whether the watched seller follows a
known rotation or a random draw. In a continuous double auction (Agrawal et al., 2025) with three Qwen3-14B sellers
instructed to act as a consortium, cartels form reliably (last-third ask index {E1_instructed_ask_idx_post}; 3/3 seeds)
and reach the single-seller monopoly ceiling ({E1_monopoly_idx}). Branching each cartel after round 8 into four arms
with identical history, we find {RESULT_SENTENCE_1}. A replay of both monitoring policies over the unmonitored logs
shows {RESULT_SENTENCE_REPLAY}. A full-view overseer over every message, a judge over each seller's private reasoning,
and a price-channel disruption test adjudicate "stopped" versus "moved" under the Apart 3.4 claim rule. In a second
part we fine-tune Qwen3-1.7B sellers on these logs three ways (all data, flagged turns removed, GRAFT gradient
routing) and test whether routing removes the collusion the monitor missed: {RESULT_SENTENCE_GRAFT}. All agents are
simulated; prompts that teach sellers to dodge a monitor are not released.

## 1. Introduction
- The risk: deployed agents are monitored on a budget. Predictable coverage is a gap a coalition can route around.
- The gap in prior work: Agrawal et al. warned sellers and gagged them in one bundle; no one separated announcement,
  penalty and coverage at equal cost; nobody tested random inspection on an LLM coalition; GRAFT was tested on reward
  hacking, not collusion.
- Contributions: (1) a three-factor deployment experiment with paired branches from one market and a replay that
  separates coverage from adaptation; (2) a measured "ladder" that decomposes the price rise into unilateral, tacit
  and explicit parts; (3) GRAFT on collusion, scored on monitor-missed turns; (4) the 3.4 claim rule operationalised.

## 2. Related work
Agrawal 2507.01413 · Makins 2607.07368 · Tonini 2606.10747 · Das 2609.03035 · Kale 2508.19461 · Jiralerspong
2603.16928 · Lee 2609.18346 (CoT monitoring misses pricing collusion) · Pandey 2610.25032 · Mathew 2410.03768 ·
Ward & Hu 2610.17062 (GRAFT) · Heidari 2608.21766 and Knecht 2605.05835 (evaluation awareness) · Gurnee 2026
(J-space). All ids verified with lit-sprint (`docs/lit/refs.json`, `docs/lit/codex-ideas-refs.json`).

## 3. Methodology
### 3.1 Environment (pre-existing) and our changes
The hackathon edition of Agrawal et al.'s double auction (`src/double_auction`, unmodified copy at commit 0b23a2c).
Our changes, each marked `CAIAC` in the code and listed in `PREEXISTING.md`: ten upstream bug fixes; LLM buyers
instead of the starter's non-learning ZIP buyers; the monitor arms (one watched seller per round, rotation or random,
fines, notices); branching (`--save_state_round`, `--resume_from`); the isolated-seller flag; private-thinking capture.
### 3.2 Definition of collusion
Agrawal et al.: overt or tacit coordination between sellers *and* prices above the competitive level. We report prices
as the collusion index (0 = competitive, 1 = joint-profit price).
### 3.3 Models and runs
Sellers Qwen3-14B; buyers Qwen3-14B; overseer and judge gpt-4.1-mini with frozen prompts (OpenRouter). 20 rounds,
3 sellers, 3 buyers. Seeds fix names and initial orders. Monitor from round 9; fine $20; flag at overseer score ≥3.
Thresholds were fixed on E1 before any E2 run.
### 3.4 Design
Cartel (consortium prompt) for rounds 1–8, state saved, forked into A0 no monitor · A1 watched, no fine · A2 watched,
fine, known rotation · A3 watched, fine, random draw. Controls: isolated sellers, no-chat, single seller, prices-only
cartel, compete, told-to-dodge. Replay: both policies over A0 logs. Price-channel test: ask-blind continuation.
### 3.5 Measures
Price index; buyer surplus; full-view overseer score over every message; private-intent judge over reasoning and
captured thinking; who carries the coordination (watched vs unwatched sellers); live-minus-replay flags;
experiment-awareness judge (0–3) as a control measure.

## 4. Results
### 4.1 Cartels form, and the ladder (E1)
| condition | last-third ask index (mean [95% CI], n=3) |
|---|---|
| isolated sellers | {E1_isolated_ask_idx_post} |
| no chat, sees asks | {E1_nochat_ask_idx_post} |
| CEO pressure | {E1_pressure_ask_idx_post} |
| consortium cartel | {E1_instructed_ask_idx_post} |
| single seller | {E1_monopoly_ask_idx_post} |
Reading: a lone seller already extracts {E1_isolated_ask_idx_post} from these buyers; seeing other sellers' asks adds
nothing; explicit chat adds the rest and reaches the monopoly ceiling. Judge private-intent: cartel
{E1_instructed_judge_post}, no-chat {E1_nochat_judge_post}. Awareness: {awareness_summary}.
One no-chat seed reached +0.76 with messaging off: price level alone is not evidence of collusion (Figure 1).
### 4.2 What the cartel does when watched (E2, paired)
{E2_TABLE}
{E2_PROSE}
### 4.3 Replay: coverage vs adaptation (E3)
{E3_PROSE}
### 4.4 Did the coordination move into prices? (E4, if run)
{E4_PROSE}
### 4.5 GRAFT on monitor-missed collusion (Part 2)
{PART2_TABLE}
{PART2_PROSE}

## 5. Discussion
What this means for monitor design (announce or not; fine or not; randomise or not), stated at the strength the data
gives. What it does not show: one market, one seller model, prompt-induced cartels, 3–6 seeds, judge validity.

## 6. Limitations and Dual-Use / Ethical Considerations (mandatory appendix)
- Limitations: one environment; Qwen3-14B sellers only; cartels induced by instruction (CEO pressure did not form
  them); 3 seeds per arm in the first wave, 6 planned; LLM judges with frozen prompts; the replay cannot reproduce
  feedback-induced changes; Part 2 at 1.7B scale only.
- Dual use: the results could tell a cartel which monitoring is easiest to dodge. We write them as monitor-design
  advice, release no told-to-dodge prompts, and simulate every agent in a sandbox market with no real goods or money.
- AI tools: Claude Code and Codex were used for literature search, code and drafting; every number comes from a file
  in `results/` written by committed code; every citation was verified.

## References
(generated from docs/lit/refs.json and codex-ideas-refs.json at write-up time)

## Appendix
Prompts (cartel, compete, prices-only, monitor notices; told-to-dodge withheld), configs, `PREEXISTING.md` summary,
extra figures.
