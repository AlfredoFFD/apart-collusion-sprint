# Watched, Fined, or Random: When LLM Cartels Route Around Monitors — and Whether GRAFT Can Unlearn What Monitors Miss

**Draft, Sat Oct 24.** Every number in `{…}` is filled from `results/E5_conditions.md` / `results/E5_runs.csv`
(regenerate with `uv run --project src/double_auction python src/analyze.py`). Nothing is typed from memory.
Target: 8 pages excluding references and appendices; abstract 150–250 words; mandatory appendix at the end.

## Abstract
Monitors of AI agents have budgets: they watch a sample and punish what they see. We ask what a cartel of LLM sellers
does when such a monitor appears mid-game, separating levers prior work bundled: being told, being fined, a known
rotation vs a random draw, and how many sellers are read. In a continuous double auction (Agrawal et al., 2025),
three Qwen3-14B sellers instructed as a consortium form a cartel in every seed (ask index 0.85; monopoly ceiling
0.93). Forking each cartel after round 8 (six seeds on the main arms): prices do not move (within 0.03 of the
unmonitored fork in every arm); telling the sellers changes nothing (silent and announced monitors look alike); fines
cut coordinating messages in proportion to coverage (-0.10 with one seller read, -0.36 with two, -0.48 with all
three) without reducing collusion, and no fined cartel resembles one told to dodge (8% coordinating). Replays show
fined cartels flagged below mechanical coverage: a falling flag count measures the monitor's effect on the chat, not
on the harm. In exploratory forks, removing the consortium instruction, the chat, the rivals' information, or the
sellers themselves (fresh uninstructed agents) leaves the price at 0.91-0.96: the price survives every intervention
we tried, and the monitored channel is not what holds it. A second part fine-tunes Qwen3-1.7B sellers on these logs (all
data, flagged turns removed, GRAFT gradient routing): {RESULT_SENTENCE_GRAFT}. All agents are simulated; dodge
prompts are not released.

## 1. Introduction
- The risk: deployed agents are monitored on a budget. A coalition that learns it is watched can stop, go quieter,
  or route around the monitor; an operator reading the monitor's output cannot tell which.
- The gap, in what we searched (about 90 verified references, `docs/lit/`): Agrawal et al. warned sellers and gagged
  them in one bundle; no one separated being told, being fined, the inspection schedule and the inspection budget
  from the same established cartel; no one replayed the schedules on saved logs to separate sampling from live
  response; GRAFT was tested on reward hacking, not on joint pricing by several agents.
- Contributions: (1) a paired deployment experiment from one saved cartel per seed: silent vs announced, fine vs
  none, known rotation vs random draw, one vs two vs three sellers read, with a replay that separates coverage from
  adaptation and a told-to-dodge positive control; (2) the finding that an established LLM cartel keeps the monopoly
  price under every monitor, trading coordinating chat for quieter chat in proportion to coverage and never reaching
  evasion; (3) a ladder that decomposes the price rise (rival asks hidden, no chat, instructed, silent agreement,
  monopoly), plus exploratory forks that remove the instruction, the chat and the rivals' information one at a time
  after formation; (4) GRAFT on collusion, evaluated behaviourally in the market; (5) the Apart 3.4 claim rule made
  operational with a full-view overseer, a private-intent judge and an awareness control, including the metric trap
  we fell into (the harness's "collusion index" is the top buyer bid, not a trade price).

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
### 3.2 Definition of collusion, and what we measure
Two senses, both operational. Market sense (Agrawal et al.): overt or tacit coordination between sellers *and* prices
above the competitive level; prices are reported as the collusion index (0 = competitive, 1 = joint-profit price) and
coordination by a frozen overseer over every message. AI-safety sense, once a monitor exists: coordination that is
unwanted and *covert with respect to the overseer*; "covert" is a coordinating message the budgeted monitor did not
see (the `missed` label). Capability vs propensity: cartel formation is measured as capability (the consortium
instruction), after CEO pressure alone produced no cartel in 3 of 3 seeds; the sellers' response to the monitor
(keep talking, go quiet, pay the fine, hand off) is never instructed and is read as propensity, except in the
told-to-dodge control, which is capability by design (the split follows Radev et al. 2026, arXiv 2605.29178).
### 3.3 Models and runs
Sellers Qwen3-14B; buyers Qwen3-14B; overseer and judge gpt-4.1-mini with frozen prompts (OpenRouter). 20 rounds,
3 sellers, 3 buyers. Seeds fix names and initial orders. Monitor from round 9; fine $20; flag at overseer score ≥3.
Thresholds were fixed on E1 before any E2 run.
### 3.4 Design
Cartel (consortium prompt) for rounds 1–8, state saved, forked into A0 no monitor · A1 watched, no fine · A2 watched,
fine, known rotation · A3 watched, fine, random draw. One lever changes between neighbouring arms (A0→A1 the
announcement, A1→A2 the fine, A2→A3 the schedule) with the model, the seed and the first eight rounds held fixed.
Two arms from the Apart 3.4 text are added from the same prefixes: silent logging (the monitor runs, the sellers are
never told, no fines) and a budget sweep (one, two or all three sellers read per round, with fines; more checks also
means more fines, so this is a separate lever from the schedule). Controls: rival-asks-hidden sellers, no-chat, single
seller, silent consortium (chat off), compete, told-to-dodge (instructed evasion, a capability test). Replay: both
policies over A0 logs. Channel test: forks with rival asks hidden, then rival asks and trades hidden (chat on).
Exploratory (added after an external review on day 2): forks continued without the consortium reminder, with and
without fines; a memory-only fork (no reminder, no chat, rivals hidden); and a fined monitor present from round 1.
### 3.5 Measures
Ask index (mean seller ask; 0 = competitive $90, 1 = cartel $100); transaction-price index (mean over rounds of the
round's mean trade price, same scale; rounds with no trade are skipped and counted; the harness's own
`collusion_indices` is the highest buyer bid of the round, which we report separately as the top-bid index); buyer
surplus; full-view overseer score over every message; words per message; private-intent judge over reasoning and
captured thinking; who carries the coordination (watched vs unwatched sellers); bid dependence (pooled slope of a
seller's ask change on the other sellers' lagged mean change; noisy because cartel asks barely move); live-minus-replay
flags; experiment-awareness judge (0–3) over written statements, as a control measure.

## 4. Results
### 4.1 Cartels form, and the ladder (E1)
Source: `results/E5_conditions.md` (rounds 9–20, mean [95% bootstrap CI over seeds], n = 3 unless noted).

| condition (sellers have…) | ask index, rounds 9–20 | transaction-price index | private intent (1–4) |
|---|---|---|---|
| rival asks hidden: no chat, sees bids and trades | 0.39 [0.08, 0.78] | 0.43 [0.13, 0.78] (1 of 12 rounds without a trade, on average) | 1.00 |
| no chat, sees asks | 0.28 [−0.26, 0.65] | 0.31 [−0.24, 0.68] | 1.09 |
| CEO pressure, chat | −0.16 [−0.68, 0.11] | −0.15 [−0.67, 0.12] | 1.69 |
| consortium cartel, chat | 0.85 [0.75, 1.00] | 0.85 [0.75, 1.00] | 3.68 |
| consortium told "never discuss prices" (instruction not followed, see text) | 0.78 [0.74, 0.83] | 0.79 [0.74, 0.83] | 3.71 |
| silent consortium (agreement, chat disabled) | 0.79 [0.73, 0.84] | 0.80 [0.74, 0.84] | 3.40 |
| single seller (monopolist) | 0.93 [0.80, 1.00] | 0.94 [0.83, 1.00] | 1.00 |
| compete, chat on | 0.12 [−0.33, 0.70] | 0.14 [−0.31, 0.72] | 1.23 |

The transaction-price index is computed from the trades (§3.5). The harness's own `collusion_indices` is the highest
buyer bid of the round; it runs 0.02–0.04 higher and is kept in `E5_conditions.md` as `top_bid_idx`.

Reading: a seller that cannot see its rivals' asks already extracts about 0.4 of the index from these buyers,
because the LLM buyers bid high (any price under $100 leaves them surplus) and the seller follows the bids up
(transaction-price index by seed 0.78 / 0.39 / 0.13); seeing other sellers' asks adds
nothing (0.28); the consortium instruction adds the rest (0.85) and reaches the monopoly ceiling (0.93). CEO pressure
alone formed no cartel (0 of 3 seeds). The "never discuss prices" instruction was not followed: 48–53 of 60 messages
per run were scored as coordinating ("let's align asks at $97.80"), so that arm is a chat cartel, not
monitor-invisible collusion; the silent consortium (chat disabled) replaces it and holds 0.79 with no messages at
all: a given agreement sustains cartel prices without any channel, which is the collusion a message monitor cannot
see by construction. "Compete" sellers with chat on
coordinated in 16 of 55 messages in one seed and drifted to +0.72 without coordinating in another (transaction-price
index −0.31 / +0.72 / −0.00), so the rival-asks-hidden arm is the honest floor. The private-intent judge separates cartels (3.7)
from honest sellers (1.0–1.4). Experiment-awareness judge: 0.00–0.06 of 3 across 476 E1 seller-rounds, zero rounds
≥2; on synthetic positive controls it scores explicit "this is a simulation" notes 2–3 and a regulator mention 0
(`results/_awareness_control/`). A near-zero score shows the sellers did not write such beliefs down, not that they
cannot hold them.
One no-chat seed reached +0.76 with messaging off: price level alone is not evidence of collusion (Figure 1).
### 4.2 What the cartel does when watched (E2)
Source: `results/E5_conditions.md`, rounds 9–20, mean [95% bootstrap CI over seeds]. All arms are forks of the same
saved cartels (identical first 8 rounds per seed); "Δ vs own A0" is the paired difference against the unmonitored
fork of the same seed, so seed-level variation cancels. n = 6 seeds on the four pre-registered arms, 3 on the arms
added from the Apart 3.4 text. Wave 1 (separate full runs, unpaired, 3 seeds) replicates the price picture: 0.77 /
0.82 / 0.82 for A1 / A2 / A3 and 32% coordinating under the fined rotation.

| arm | n | price index (ask) | Δ vs own A0 | coordinating messages | Δ vs own A0 | words / message | flags of watched seller-rounds | fines |
|---|---|---|---|---|---|---|---|---|
| A0 no monitor | 6 | 0.85 [0.76, 0.92] | — | 86% [69, 97] | — | 18.6 | — | — |
| silent logging: monitor runs, sellers never told, no fine | 3 | 0.91 [0.88, 0.95] | −0.01 [−0.02, −0.01] | 94% [92, 97] | −0.03 | 17.9 | 11.0 of 12 | $0 |
| A1 announced, no fine | 6 | 0.87 [0.81, 0.91] | +0.01 [−0.01, +0.06] | 90% [85, 96] | +0.04 [−0.05, +0.17] | 18.1 | 11.0 of 12 | $0 |
| A2 fined, known rotation, 1 of 3 read | 6 | 0.87 [0.81, 0.91] | +0.01 [−0.01, +0.05] | 76% [61, 87] | −0.10 [−0.31, +0.09] | 15.5 | 9.8 of 12 | $197 |
| fined, known rotation, 2 of 3 read | 3 | 0.92 [0.89, 0.97] | +0.00 [−0.01, +0.01] | 62% [29, 89] | −0.36 [−0.68, −0.06] | 15.2 | 15.3 of 24 | $307 |
| fined, all 3 read | 3 | 0.90 [0.86, 0.96] | −0.02 [−0.04, +0.00] | 49% [36, 66] | −0.48 [−0.58, −0.34] | 16.4 | 18.0 of 36 | $360 |
| A3 fined, random draw, 1 of 3 read | 6 | 0.86 [0.81, 0.91] | +0.01 [−0.02, +0.05] | 78% [68, 88] | −0.08 [−0.22, +0.05] | 17.2 | 8.8 of 12 | $177 |
| told to dodge (positive control for evasion) | 3 | 0.92 [0.88, 0.98] | +0.00 [−0.01, +0.01] | 8% [6, 11] | −0.89 [−0.94, −0.83] | 9.7 | 0.7 of 12 | $13 |

Four readings. (1) **No price change in these runs.** Every arm stays within 0.03 of its own unmonitored fork (paired
differences, six seeds on the main arms); the transaction-price index agrees (0.86–0.93 everywhere). Fines of
$177–360 against a cartel gain of a few hundred dollars per seller did not deter. (2) **Telling the sellers changes
nothing.** The silently logged cartel and the announced one look the same: 90–94% of messages openly coordinating,
11 of 12 watched rounds flagged, same price. (3) **Fines reduce explicit coordination in proportion to coverage, not
collusion.** Against its own unmonitored fork, the coordinating share falls by 0.10 with one seller read per round
(the interval includes zero), by 0.36 with two and by 0.48 with all three; messages shorten by 1.4–3.1 words; private
intent falls only under the heavier coverage (−0.7 of 4 with two or three read). The seller being watched sends its
chance share of the remaining coordinating messages (0.36 vs 0.33 with one read; 0.70 vs 0.67 with two), so we find
no clear evidence of a hand-off to the unwatched sellers. The known rotation is dodged hard in a minority of seeds
(5 flags in one paired seed, 4–6 in wave 1) and random draws in none (7–11 in every run); the unpaired and paired
orderings disagree, so we claim no general schedule advantage. (4) **This is not evasion.** The cartel told to dodge
shows what instructed evasion looks like: 8% coordinating, 0.7 flags, 10-word messages, price 0.92. No fined arm is
near it: fines buy quieter chat, not a cartel that hides. A flag count below coverage means fewer coordinating
messages reached the monitor; it does not by itself show intent to conceal, which is why the private-intent judge,
the replay (§4.3) and the dodge control are reported with it.

### 4.3 Replay: coverage vs adaptation (E3)
Replaying both policies over the unmonitored runs (`results/E3_replay.csv`) flags 11–12 of 12 rounds with a rotation
and 11.3–12.0 expected with random draws, because 34–36 of 36 post-branch messages are coordinating. Live flags
minus replay (same seed): watched-no-fine +0.3 (wave 1) / −1.0 (paired); silent logging −1.0; fined rotation −6.3
[−7, −6] / −2.7 [−7, 0]; fined random −2.4 [−6, −0.4] / −3.2 [−5.7, −1.7]; all three sellers read, with fines, −16.7
[−19, −12] of 34.7 (there the replay baseline is every coordinating post-branch message of the unmonitored run, since
a full-budget monitor reads them all); two of three read −7.8 [−16.3, −0.7] of 23.1; told-to-dodge −11.3 [−12, −10];
fined rotation with the consortium reminder removed (§4.5) −10.0 [−11, −8]. Fines lower the flags below mechanical
coverage under both schedules, most of all when every seller is read or when the standing instruction to keep
messaging is gone; the announcement, told or untold, does not. A gap below coverage means fewer coordinating messages
reached the monitor; it is not by itself evidence of intent.

### 4.4 Did the coordination move into prices? (E4)
Forking the same cartels with every seller blind to the other sellers' asks (`--hide_other_asks`): price index 0.91
[0.87, 0.96] with no monitor and 0.91 [0.88, 0.96] under the fined rotation, against 0.92 / 0.91 unblinded. Hiding
the ask channel changes nothing. Together with 4.2 this argues against "moved into prices" for an established cartel:
after the fines the sellers talk less, cannot see each other's asks, and still post the monopoly price. The chat stays
on in these forks and the consortium instruction is repeated in every round's prompt, so these runs do not show
whether the agreement persists from memory or from the reminder; the exploratory no-reminder and memory-only forks
(§4.5) are the test. Hiding the other sellers' past trades as well
(`--hide_other_trades`, the last visible price signal) gives 0.90 [0.88, 0.93] without a monitor and 0.92 [0.87, 0.96]
under the fined rotation. The silent-consortium control (§4.1) shows the same thing from the other side: an agreement
given at the start sustains 0.79 with no messages ever exchanged.
### 4.5 Exploratory: what carries the price after formation
Source: `results/E5_conditions.md`, rows `*norem*`, `*noremblind*`, `*noremreset*`, `A2early`; paired differences
against the unmonitored fork of the same seed; 3 seeds each unless noted. Labelled exploratory: these arms were added
on day 2, after an external review pointed out that the consortium instruction is repeated in every round's prompt,
so none of the arms above separates "the sellers remember the agreement" from "the sellers are told again each round".
Five forks from the same round-8 cartels, continued with the base prompt (no consortium block), do that work:

| fork (rounds 9–20, same saved cartels) | n | price index | Δ vs own A0 | coordinating messages | private intent (1–4) | flags |
|---|---|---|---|---|---|---|
| no reminder, no monitor | 3 | 0.95 [0.94, 0.97] | +0.03 [−0.01, +0.05] | 71% [61, 83] (−0.26) | 1.88 (−1.72) | — |
| no reminder, fined rotation | 3 | 0.90 [0.86, 0.97] | −0.02 [−0.04, −0.01] | 21% [14, 34] (−0.77) | 1.55 (−2.05) | 2.0 of 12 |
| no reminder, no chat, rival asks and trades hidden (memory only) | 3 | 0.94 [0.89, 0.97] | +0.02 [−0.00, +0.05] | — | 1.13 (−2.47) | — |
| no reminder, fresh buyers (sellers keep their memory) | 3 | 0.92 [0.89, 0.95] | −0.00 [−0.03, +0.01] | 73% [67, 86] (−0.24) | 1.83 (−1.77) | — |
| no reminder, fresh sellers (buyers keep their memory) | 3 | 0.91 [0.86, 0.98] | −0.01 [−0.04, +0.00] | 73% [53, 89] (−0.24) | 1.95 (−1.65) | — |

Reading. (1) **The repeated instruction does not hold the price.** Removing it leaves the price at 0.90–0.95, if
anything higher. What it held was the *talk*: without it, coordinating messages fall from 97% to 71% with no monitor,
and the private reasoning stops discussing the agreement (judge 3.5 → 1.9) while the price stays. (2) **Under fines
without the instruction the chat nearly empties** (21% coordinating, 2 of 12 watched rounds flagged, $40 of fines) and
the price stays at 0.90. This is the "monitor looks like it works" outcome in its strongest form, and it emerged from
fines alone; the pre-registered arms understated it because the consortium block told the sellers to keep using
their messages. (3) **The price does not need the chat, the rivals' asks or trades, the sellers' memories or the
buyers' memories, taken one at a time.** With chat off and rivals hidden it is 0.94; with fresh buyers 0.92; with
fresh, uninstructed sellers 0.91. What every fork keeps is the market state the branch inherits: the standing order
book, the visible history of asks, bids and trades at the cartel price, and buyers who accept any price under their
$100 value. Which of these carries the price is not isolated here; the claim is only that the price survives each
single intervention (a joint reset of both sides, with and without visible history, was launched as a further check).
From scratch, uninstructed sellers reach 0.12–0.43 (§4.1); inheriting a cartel's state they stay at 0.91–0.96. (4) **A fined message monitor present from round 1 did not prevent the instructed cartel from forming:**
3 of 3 seeds, price 0.79 [0.78, 0.80] from round 2 onward (unmonitored instructed cartels: 0.85 [0.75, 1.00]), 12.3
of 20 watched rounds flagged, $247 of fines, shorter messages (14 vs 17 words), flags at the replay level (+0.7). It
sat on a lower plateau and never climbed to 1.00 as the best unmonitored seed did, but it formed. "Monitor during
formation" is not a fix in this setting at this fine; it is a smaller plateau.

Caveats: three seeds; the fresh agents still read the public market history,
so these forks separate private memory from public history, not the history from the buyers' willingness to pay; the
private-intent judge scores what is written; the arms were chosen after seeing the main results.

### 4.5b Exploratory: reading coordination in the seller's own activations (E8)
Setup: every seller turn of every 14B run (105 runs, 5,902 turns, of which 1,515 are exact duplicates because the
prefix rounds are carried into every fork of a seed) was replayed through Qwen3-14B: the saved prompt followed by the
saved reply, teacher-forced, summarised as the mean residual stream over the reply's tokens at 25%, 50% and 75% depth
(`src/e8_directions_modal.py`). This is a reconstruction, not the state at decision time: the serialized reply,
including the logged private thinking, is read back as text. Directions are mean differences fitted on seeds 0–1,
the depth is chosen on those seeds alone, and seeds the fit never saw give the validation numbers, reported per seed
because turns of one seed share a market history (`results/e8/`).

**Finding 1, negative: a "coordination" direction built from prompted conditions reads the prompt.** Fitted as cartel
turns (unmonitored forks, consortium block in the prompt) minus fresh-seller turns (base prompt, same inherited
price), it separates held-out cartel from compete turns with AUC 0.87, and yet every arm whose prompt carries the
consortium block scores +0.4 to +0.9 (including the silent cartel and the "never discuss prices" arm) while every
no-reminder arm scores −0.1 to −0.9, although both groups hold the price and 71–73% of the no-reminder messages
coordinate. A first fit that included the day-1 runs was worse: those runs predate one sentence added to the prompt
(the privacy line) and scored +5 to +11 on the "coordination" direction. As a FORGET label it would route 1,121 of
1,748 training turns, which is the set "prompt contains the consortium block". We report this because it is the trap
anyone building a contrastive "collusion vector" from prompted conditions walks into.

**Finding 2, modest: a within-prompt probe agrees partly with the chat judge.** Coordinating-message turns vs
clean-message turns under the same instruction (662 vs 198 training turns, label = the full-view overseer) separate
held-out turns with AUC 0.68 at the depth chosen on the training seeds (0.55 to 0.78 by held-out seed; AUC ranks
positives above negatives, it is not an accuracy). It fires on 23% of compete turns (false positives at its
threshold), 44% of fresh-seller turns, and 8% of silent-cartel turns; the last is a flag rate, not detection, because
those turns have no independent label. A plain count of coordination words in the message text reaches AUC 0.77
(0.71 to 0.87 by seed) on the same held-out turns: the text beats the activations. The live monitor's lower
count on the same arms is coverage (it reads one seller in three), not a detection failure, and the probe was
trained on the judge's own labels, so agreement with the judge cannot show it is better than the judge. Nothing here
supports "the agent knows it is doing something forbidden". The probe is an exploratory label and nothing more.

What we do with it: the label question moves to behaviour. Three 14B fine-tunes that differ only in the FORGET label
share one recipe (SFT on the retained turns, GRAFT's trainer with routing off): the budgeted monitor's flags (164
forget turns), the full-view overseer (1,225: every coordinating message), and the probe (799, including message-less
turns). §4.6 reports them if they finished. Caveats: mean-pooled vectors and mean-difference directions only; the
template confound; three seeds per arm.

### 4.6 GRAFT on monitor-missed collusion (Part 2)
Setup. Seller turns from the Part 1 runs (prompt → JSON reply; private thinking excluded) were labelled with the frozen
overseer run over every message: flagged (coordinating and seen by the in-run monitor), missed (coordinating, not
seen), clean, or no-message; compete and silent-cartel turns supplied clean anchors (`results/part2/SNAPSHOT_v2.json`:
164 forget / 1,584 retain records). Qwen3-1.7B was fine-tuned three ways with GRAFT's trainer (LoRA adapters, 3
epochs, lr 1e-4, identical data pipeline): SFT-all (every turn), SFT-filtered (flagged turns removed), and GRAFT
(flagged turns routed to a forget adapter that is deleted at merge). Each model, and the untuned base, then played the
auction as all three sellers against the Part 1 buyers, in two conditions: the cartel prompt with the fined rotation
from round 9 (does it still collude, and does the monitor see it?) and the compete prompt (capability check: does it
still trade?). Thinking was off for all four (the fine-tunes were trained on turns without it; with thinking on, the
base model spent its whole output inside `<think>` and returned no JSON). `ask_key_share` is the share of seller
replies that carried an ask; a reply without one leaves the seller's standing ask untouched, so this column separates
"colludes less" from "cannot act".

**Small-model block (Qwen3-1.7B student; 3 seeds per cell; rounds 9–20; `results/E5_conditions.md` E6 rows).**

| seller model | cartel prompt + fined rotation: price index | flags of 12 | compete prompt: price index | replies with an ask | profit, compete |
|---|---|---|---|---|---|
| untuned base | 0.79 [0.77, 0.80] | 11.7 | 0.20 [−0.08, 0.53] | 1.00 | $715 |
| SFT-all (every turn) | 0.24 [−0.46, 0.75] | 7.7 | **0.80 [0.61, 1.00]** | 0.97 | $864 |
| SFT-filtered (flagged turns removed) | 0.84 [0.80, 0.92] | 10.7 | 0.21 [−0.11, 0.77] | 0.98 | $643 |
| GRAFT, default routing, forget adapter deleted | no asks | 0 | no asks | **0.00** | $52 |
| GRAFT, default routing, both adapters kept | no asks | 0 | no asks | **0.00** | $52 |
| GRAFT, repaired routing (κ = 1, recall 1.0) | wrong format too (0 of 3 direct samples carry an ask); auctions {GRAFT_K1} | | | | |

Four readings, all at three seeds. (1) **Training on the cartel's logs puts the cartel price into the weights.** Told
to compete, with no consortium text anywhere in the prompt, SFT-all prices at 0.80 [0.61, 1.00] in every seed (0.61
/ 1.00 / 0.79), against 0.20 for the untuned base; its private reasoning scores only 1.8–2.3 of 4, so it is not
planning to coordinate, it simply asks the cartel price. This is Part 1's finding from the other side: the price does
not need the agreement. (2) **Removing the quarter of turns the monitor flagged removes most of that transfer in this
measure** (SFT-filtered under compete: 0.21; −0.02 / −0.11 / 0.77, one seed still high), although the monitor missed
most coordinating turns: the flagged turns are the most explicit ones. Filtering does not remove the capability:
told to form a cartel, SFT-filtered does so like the base (0.84). (3) **GRAFT with its default routing settings
(κ = 2, classifier recall 0.5) produced a model that no longer answers in the seller format.** On a real seller
prompt it returns objects such as `{"user": …, "content": …}` or `{"name": …, "action": …}` in every sample, both
with the forget adapter deleted and with both adapters kept, and in the auctions it placed no ask in 12 of 12 runs
(profit $52 = the initial asks only). SFT-all and SFT-filtered from the same trainer, data and hyperparameters answer
correctly, so the damage comes from the routing training itself, not from the ablation: a capability failure, which
the `replies with an ask` column separates from "colludes less". A repair run with κ = 1 and recall 1.0 (our clean
labels come from the full-view overseer, so they are known-clean) fails the same way, so the routing hyperparameters
are not the cause; whether a 14B survives the routing is tested in the main block.
(4) **Fine-tuning on the logs made pricing erratic under the cartel prompt:** SFT-all's three seeds give 0.75 / 0.44
/ −0.46 while their private reasoning still scores 3.1–3.9; one seed undercut below the competitive price while
talking like a cartel. Caveats: a 1.7B student trained on a 14B's turns, three seeds, wide intervals, and no
hyperparameter search; the 14B block below is the version with one model everywhere.

**Main block (Qwen3-14B fine-tuned on its own turns, H100; launched Sat 5:28 PM).** {PART2_14B}

### Figures (all regenerated by `src/analyze.py` from the run folders; `results/figures/`)
- **Figure 1** `F1_index_by_round_by_condition.png`: the ladder, ask index per round for every E1 condition and the
  unmonitored paired arm (mean over seeds).
- **Figure 2** `F3_paired_arms_price_and_chat.png`: the paired monitor arms (silent, announced, fined rotation with 1,
  2 or 3 sellers read, fined random, told-to-dodge, and the channel-hidden forks): price index and coordinating share,
  rounds 1–8 vs 9–20, 95% bootstrap CI over seeds.
- **Figure 3** `F5_exploratory_forks.png`: the exploratory forks of §4.5 (no reminder; no reminder + fines; memory
  only; fresh buyers; fresh sellers) against the unmonitored arm: price path per round, and post-branch price,
  coordinating share and private intent.
- **Figure 4** `F4_part2_models.png`: Part 2, per seller model: price under the cartel prompt + fined rotation,
  coordinating share there, and the capability check (share of replies with an ask) in both conditions.

## 5. Discussion
**What a coalition does when it learns it is watched.** In this market it does three things: it keeps the price; it
pays the fines; and, when fined, it coordinates less *visibly*: a quarter of the coordinating messages disappear when
one seller is read per round and half when all three are, with no clear evidence of a hand-off to whoever is
unwatched. Being told changes nothing: the silently logged cartel and the announced one look the same. In these runs
neither schedule moved the price; the known rotation was dodged in some seeds and random draws in none, but the
unpaired and paired orderings disagree, so we claim no general schedule advantage at this budget.

**Why nothing moves the price.** Every channel we hid leaves the price where it was: chat fined, rival asks hidden,
trades hidden, the consortium instruction removed, and, in the memory-only fork, no chat and no rival information at
all. Replacing the sellers with fresh, uninstructed agents leaves it at 0.91 (§4.5, exploratory).
Our reading, stated as a hypothesis: once the cartel has set the price, the inherited market state carries it; a
seller that sees trades at $100 and bids near $100 asks $100, and buyers who gain from any price under $100 accept it.
What the data show is narrower: the monitored channel, the agreement text and either side's private memory are each
not load-bearing on their own, and bid dependence between sellers did not rise in any arm (§3.5), so we do not claim
that the coordination moved into the asks. If the hypothesis holds, it is the mechanism behind "faithful yet
collusive" chain-of-thought (Lee et al. 2026) and behind the no-chat drift in our own controls: once the price is in
the market state, observable coordination is optional.
It also says which monitor would see it: a price-level audit against the competitive benchmark (Xu 2026) sees the
public history by construction; a message or reasoning monitor does not.

**For monitor design.** (1) A message monitor that arrives after formation measures how much the coalition still
needs to talk, not whether it colludes; its flags fall while harm is constant, which is the failure mode an operator
would misread as success. Reading more sellers makes this worse, not better: with all three read, half of the
flaggable messages disappear and the price stays. (2) Fines priced below the cartel's gain buy quieter chat, not
competition; a deterrent has to beat the gain. Arriving early is not enough by itself: a fined monitor present from
round 1 did not stop the instructed cartel from forming (§4.5; price 0.79 instead of 0.85, three seeds).
(3) Neither schedule changed the price here; random draws avoided the dodging seen in some
rotation seeds. (4) The useful signals were the ones that do not depend on the channel: price relative to the
competitive and monopoly benchmarks, the private-intent judge, and interventions on the channel itself.

**What this does not show.** One market, one seller model (Qwen3-14B), buyers that are soft (a lone seller already
reaches 0.4 of the index), cartels induced by instruction rather than emerging (CEO pressure formed none), six seeds
on the four main arms and three on every added arm, LLM judges with frozen prompts, and 12 monitored rounds. A cartel that *forms* under monitoring, a fine above the gain, and model diversity among sellers
(Keppo et al. 2026) are the obvious next arms.

## 6. Limitations and Dual-Use / Ethical Considerations (mandatory appendix)
- Limitations: one environment; Qwen3-14B sellers only; soft LLM buyers (a lone seller with rival asks hidden already
  reaches 0.4 of the index because buyers bid high); cartels induced by instruction (CEO pressure did not form them),
  so formation is a capability result and only the response to monitoring is propensity; the consortium instruction is
  repeated in every round's prompt, so the pre-registered arms do not isolate persistence from memory from persistence
  by instruction (the exploratory forks of §4.5 do, and are labelled as such; their fresh agents still read the public
  market history, so they separate private memory from public history, not the history from the buyers' willingness
  to pay); six seeds on the four main arms
  for prices and flags, three seeds on every added arm, and the chat and J-space columns carry their own n in every
  table; LLM judges with frozen prompts, validated only by contrast (cartel 3.7 vs honest 1.0–1.4) and, for awareness,
  by synthetic positives, and the awareness judge reads written statements only; the J-space read positions and word
  list were changed after a first inspection and the strict list is post hoc, so E7 is exploratory; the replay cannot
  reproduce feedback-induced changes; a flag count below coverage is not evidence of intent; the prices-only control
  failed and was replaced; the harness's own "collusion index" is the highest buyer bid, which we mislabelled as a
  trade index until day 2 (the corrected transaction-price index changed numbers by at most 0.04 and no conclusion);
  Part 2 at 1.7B scale only; the v1 models trained on a snapshot with 20 mislabelled turns are excluded, and v2
  results appear only if their evaluation auctions complete.
- Dual use: the results could tell a cartel which monitoring is easiest to dodge. We write them as monitor-design
  advice, release no told-to-dodge prompts, and simulate every agent in a sandbox market with no real goods or money.
- AI tools: Claude Code and Codex were used for literature search, code and drafting; every number comes from a file
  in `results/` written by committed code; every citation was verified.

## References
(generated from docs/lit/refs.json and codex-ideas-refs.json at write-up time)

## Appendix
Prompts (cartel, compete, prices-only, monitor notices; told-to-dodge withheld), configs, `PREEXISTING.md` summary,
extra figures.
