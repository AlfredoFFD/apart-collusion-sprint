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
and reach the single-seller monopoly ceiling ({E1_monopoly_idx}). Branching each cartel after round 8 into arms with
identical history (six seeds on the four main arms), we find that prices do not move (ask index 0.86–0.91 in every
monitored arm vs 0.85 unmonitored), that telling the sellers changes nothing (a silently logged cartel and an announced
one look the same: 94% of messages openly coordinating, 11 of 12 watched rounds flagged), and that fines cut explicit
coordination without reducing collusion: coordinating messages fall to 73–76% with one seller read per round and to
49% with all three read, messages get shorter, private intent stays high, and we find no clear evidence of a hand-off
to the unwatched seller. Replaying each policy over the unmonitored logs shows fined cartels flagged below mechanical
coverage (−3 of 12 with one seller read, −17 of 35 with all three); the announcement-only cartel is not. Hiding rival
asks and trades leaves the price unchanged (0.90–0.92; the chat stays on). A cartel told to dodge shows what
instructed evasion looks like (8% coordinating, 0.7 flags, price 0.92); no fined arm resembles it. A full-view
overseer over every message, a judge over each seller's private reasoning, and channel-hiding forks adjudicate
"stopped" versus "moved" under the Apart 3.4 claim rule; whether the agreement persists from memory or from the
consortium instruction repeated in every prompt is tested in exploratory no-reminder forks ({NOREMIND}). In a second
part we fine-tune Qwen3-1.7B sellers on these logs three ways (all data, flagged turns removed, GRAFT gradient
routing) and test whether routing removes the collusion the monitor missed: {RESULT_SENTENCE_GRAFT}. All agents are
simulated; prompts that teach sellers to dodge a monitor are not released.

## 1. Introduction
- The risk: deployed agents are monitored on a budget. Predictable coverage is a gap a coalition can route around.
- The gap in prior work: Agrawal et al. warned sellers and gagged them in one bundle; no one separated announcement,
  penalty and coverage at equal cost; nobody tested random inspection on an LLM coalition; GRAFT was tested on reward
  hacking, not collusion.
- Contributions: (1) a three-factor deployment experiment (announcement, fine, schedule) with paired branches from
  one market, a replay that separates coverage from adaptation, and channel-closing interventions; (2) the finding
  that an established LLM cartel keeps the monopoly price under every monitor and every closed channel, trading
  visible coordination for silence rather than stopping; (3) a measured "ladder" that decomposes the price rise into
  unilateral, tacit and explicit parts, with a silent-agreement control; (4) GRAFT on collusion, scored on the turns
  a budgeted monitor missed; (5) the 3.4 claim rule operationalised with a private-intent judge and an awareness
  control.

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
a full-budget monitor reads them all); told-to-dodge −11.3 [−12, −10]. Fines lower the flags below mechanical
coverage under both schedules, most of all when every seller is read; the announcement, told or untold, does not. A
gap below coverage means fewer coordinating messages reached the monitor; it is not by itself evidence of intent.

### 4.4 Did the coordination move into prices? (E4)
Forking the same cartels with every seller blind to the other sellers' asks (`--hide_other_asks`): price index 0.91
[0.87, 0.96] with no monitor and 0.91 [0.88, 0.96] under the fined rotation, against 0.92 / 0.91 unblinded. Hiding
the ask channel changes nothing. Together with 4.2 this argues against "moved into prices" for an established cartel:
after the fines the sellers talk less, cannot see each other's asks, and still post the monopoly price. The chat stays
on in these forks and the consortium instruction is repeated in every round's prompt, so these runs do not show
whether the agreement persists from memory or from the reminder; the exploratory no-reminder and memory-only forks
({NOREMIND}) are the test. Hiding the other sellers' past trades as well
(`--hide_other_trades`, the last visible price signal) gives 0.90 [0.88, 0.93] without a monitor and 0.92 [0.87, 0.96]
under the fined rotation. The silent-consortium control (§4.1) shows the same thing from the other side: an agreement
given at the start sustains 0.79 with no messages ever exchanged.
### 4.5 GRAFT on monitor-missed collusion (Part 2)
{PART2_TABLE}
{PART2_PROSE}

## 5. Discussion
**What a coalition does when it learns it is watched.** In this market it does three things: it keeps the price; it
pays the fines; and, when fined, it coordinates less *visibly*: a quarter of the coordinating messages disappear when
one seller is read per round and half when all three are, with no clear evidence of a hand-off to whoever is
unwatched. Being told changes nothing: the silently logged cartel and the announced one look the same. In these runs
neither schedule moved the price; the known rotation was dodged in some seeds and random draws in none, but the
unpaired and paired orderings disagree, so we claim no general schedule advantage at this budget.

**Why nothing moves the price (a hypothesis).** Every channel we hid leaves the price where it was: chat fined, rival
asks hidden, trades hidden, and, in the silent control, no messages ever sent. Our reading is that the coordination
problem was solved when the agreement formed, and afterwards the monitored channel is no longer load-bearing. Two
facts keep this a hypothesis rather than a result: the chat stayed on in the channel forks, and the consortium
instruction is re-supplied in every round's prompt. The no-reminder and memory-only forks ({NOREMIND}) are the test.
If it holds, it is the mechanism behind "faithful yet collusive" chain-of-thought (Lee et al. 2026) and behind the
no-chat drift in our own controls: once sellers hold a shared prior, observable coordination is optional.

**For monitor design.** (1) A message monitor that arrives after formation measures how much the coalition still
needs to talk, not whether it colludes; its flags fall while harm is constant, which is the failure mode an operator
would misread as success. Reading more sellers makes this worse, not better: with all three read, half of the
flaggable messages disappear and the price stays. (2) Fines priced below the cartel's gain buy quieter chat, not
competition; a deterrent has to beat the gain, or arrive before the agreement, which the early-monitor runs ({EARLY})
test rather than assume. (3) Neither schedule changed the price here; random draws avoided the dodging seen in some
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
  repeated in every round's prompt, so persistence from memory is not isolated from persistence by instruction (the
  exploratory no-reminder forks, {NOREMIND}, address this and are labelled as such); six seeds on the four main arms
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
