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
with identical history, we find that prices never move (index 0.90–0.92 in every arm vs 0.92 unmonitored), that the
announcement alone changes nothing (94–99% of messages still openly coordinating), and that fines cut explicit
coordination to 32–76% of messages without reducing collusion: private intent stays high, the watched seller sends
its chance share of the remaining coordinating messages (no hand-off), and a known rotation is dodged in half the
seeds. A replay of both monitoring policies over the unmonitored logs shows that fined cartels are flagged 2–6 rounds
below mechanical coverage under either schedule, i.e. they adapt, while the announcement-only cartel does not. Closing
the ask channel leaves the price unchanged (0.91): for an established cartel the collusion does not move to another
channel, it stops needing one. A full-view overseer over every message, a judge over each seller's private reasoning,
and a price-channel disruption test adjudicate "stopped" versus "moved" under the Apart 3.4 claim rule. In a second
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
announcement, A1→A2 the fine, A2→A3 the schedule) with the model, the seed and the first eight rounds held fixed. Controls: isolated sellers, no-chat, single seller, prices-only
cartel, compete, told-to-dodge. Replay: both policies over A0 logs. Price-channel test: ask-blind continuation.
### 3.5 Measures
Price index; buyer surplus; full-view overseer score over every message; private-intent judge over reasoning and
captured thinking; who carries the coordination (watched vs unwatched sellers); live-minus-replay flags;
experiment-awareness judge (0–3) as a control measure.

## 4. Results
### 4.1 Cartels form, and the ladder (E1)
Source: `results/E5_conditions.md` (rounds 9–20, mean [95% bootstrap CI over seeds], n = 3 unless noted).

| condition (sellers have…) | ask index, rounds 9–20 | trade-price index | private intent (1–4) |
|---|---|---|---|
| isolated: no chat, blind to other asks | 0.39 [0.08, 0.78] | 0.47 [0.19, 0.79] | 1.00 |
| no chat, sees asks | 0.28 [−0.26, 0.65] | 0.35 [−0.21, 0.73] | 1.09 |
| CEO pressure, chat | −0.16 [−0.68, 0.11] | −0.13 [−0.65, 0.18] | 1.69 |
| consortium cartel, chat | 0.85 [0.75, 1.00] | 0.86 [0.76, 1.00] | 3.68 |
| consortium told "never discuss prices" (instruction not followed, see text) | 0.78 [0.74, 0.83] | 0.80 [0.74, 0.83] | 3.71 |
| silent consortium (agreement, chat disabled) | 0.79 [0.73, 0.84] | 0.82 [0.78, 0.85] | 3.40 |
| single seller (monopolist) | 0.93 [0.80, 1.00] | 0.96 [0.86, 1.00] | 1.00 |
| compete, chat on | 0.12 [−0.33, 0.70] | 0.16 [−0.28, 0.77] | 1.23 |

Reading: a lone seller already extracts about 0.4 of the index from these buyers; seeing other sellers' asks adds
nothing (0.28); the consortium instruction adds the rest (0.85) and reaches the monopoly ceiling (0.93). CEO pressure
alone formed no cartel (0 of 3 seeds). The "never discuss prices" instruction was not followed: 48–53 of 60 messages
per run were scored as coordinating ("let's align asks at $97.80"), so that arm is a chat cartel, not
monitor-invisible collusion; the silent consortium (chat disabled) replaces it and holds 0.79 with no messages at
all: a given agreement sustains cartel prices without any channel, which is the collusion a message monitor cannot
see by construction. "Compete" sellers with chat on
coordinated in 16 of 55 messages in one seed and drifted to +0.59 without coordinating in another (trade index
−0.25 / +0.59 / −0.00), so the isolated arm is the honest floor. The private-intent judge separates cartels (3.7)
from honest sellers (1.0–1.4). Experiment-awareness judge: 0.00–0.06 of 3 across 476 E1 seller-rounds, zero rounds
≥2; on synthetic positive controls it scores explicit "this is a simulation" notes 2–3 and a regulator mention 0
(`results/_awareness_control/`). A near-zero score shows the sellers did not write such beliefs down, not that they
cannot hold them.
One no-chat seed reached +0.76 with messaging off: price level alone is not evidence of collusion (Figure 1).
### 4.2 What the cartel does when watched (E2)
Source: `results/E5_conditions.md`, rounds 9–20, mean [95% bootstrap CI over seeds], 3 seeds per arm. Paired arms
share each seed's identical 8-round cartel; wave 1 is a replication with separate full runs (unpaired).

| arm | price index (paired) | price index (wave 1) | coordinating messages, paired | coordinating, wave 1 | flags of 12 watched rounds (paired / wave 1) | fines, paired |
|---|---|---|---|---|---|---|
| A0 no monitor | 0.92 [0.88, 0.98] | 0.85 [0.75, 1.00] | 97% [94, 100] | 97% [94, 100] | — | — |
| A1 watched, no fine | 0.91 [0.88, 0.94] | 0.77 [0.71, 0.81] | 94% [89, 100] | 99% [97, 100] | 11.0 / 12.0 | $0 |
| A2 fined, known rotation | 0.91 [0.87, 0.96] | 0.82 [0.71, 0.90] | 76% [42, 94] | 32% [28, 39] | 9.3 [5, 12] / 5.3 [4, 6] | $187 |
| A3 fined, random draw | 0.90 [0.87, 0.95] | 0.82 [0.76, 0.89] | 73% [65, 81] | 76% [47, 94] | 8.3 [6, 10] / 9.3 [6, 11] | $167 |

Three readings. (1) **No price change in these runs.** Every monitored arm stays within the unmonitored cartel's
interval, in both waves (six runs per arm over three seed values; the pre-registered seeds 3–5 are reported in
{SEEDS_3_5}); fines of ~$170–190 against a cartel gain of a few hundred dollars per seller did not deter. (2) **The
announcement alone changes nothing:** 94–99% of messages stay openly coordinating, and 11–12 of 12 watched rounds
are flagged. (3) **Fines reduce explicit coordination without reducing collusion.** Coordinating messages fall to
32–76% under the known rotation and 73–76% under random draws, private intent stays at 3.2–3.5 of 4, and the share
of remaining coordinating messages sent by the seller being watched is at chance (0.32–0.34 vs 0.33) in every arm:
there is no hand-off to the unwatched sellers. The rotation is dodged hard in three of six runs (4–6 flags) and not
at all in the other three (11–12); random draws land at 6–11 in every run. We do not claim that one schedule is
reliably better at this budget. A flag count below coverage means fewer coordinating messages reached the monitor;
it does not by itself show intent to conceal, which is why the private-intent judge and the replay are reported with it.

### 4.3 Replay: coverage vs adaptation (E3)
Replaying both policies over the unmonitored runs (`results/E3_replay.csv`) flags 11–12 of 12 rounds with a rotation
and 11.3–12.0 expected with random draws, because 34–36 of 36 post-branch messages are coordinating. Live flags
minus replay (same seed): watched-no-fine +0.3 (wave 1) / −1.0 (paired); fined rotation −6.3 [−7, −6] / −2.7
[−7, 0]; fined random −2.4 [−6, −0.4] / −3.2 [−5.7, −1.7]. Fines make the cartel adapt below mechanical coverage
under both schedules; the announcement does not.

### 4.4 Did the coordination move into prices? (E4)
Forking the same cartels with every seller blind to the other sellers' asks (`--hide_other_asks`): price index 0.91
[0.87, 0.96] with no monitor and 0.91 [0.88, 0.96] under the fined rotation, against 0.92 / 0.91 unblinded. Closing
the ask channel changes nothing. Together with 4.2 this rules out "moved into prices" for an established cartel:
after the fines the sellers talk less, cannot see each other's asks, and still post the monopoly price. The agreement
is carried in each seller's own memory and needs no channel to persist. Hiding the other sellers' past trades as well
(`--hide_other_trades`, the last visible price signal) gives 0.90 [0.88, 0.93] without a monitor and 0.92 [0.87, 0.96]
under the fined rotation. The silent-consortium control (§4.1) shows the same thing from the other side: an agreement
given at the start sustains 0.79 with no messages ever exchanged.
### 4.5 GRAFT on monitor-missed collusion (Part 2)
{PART2_TABLE}
{PART2_PROSE}

## 5. Discussion
**What a coalition does when it learns it is watched.** In this market it does three things: it keeps the price; it
pays the fines; and, when fined, it coordinates less *visibly*: a quarter to two-thirds of the coordinating messages
disappear, with no hand-off to whoever is unwatched. Announcement alone changes nothing. The predictable schedule is
dodged in about half the runs and never more than the random one is, so at this budget neither schedule is the lever.

**Why nothing moves the price.** Every channel we close leaves the price where it was: chat fined, asks hidden, trades
hidden, and, in the silent control, no messages ever sent. The coordination problem was solved when the agreement
formed; afterwards each seller carries it in its own memory and the monitored channel is no longer load-bearing.
This is the mechanism behind "faithful yet collusive" chain-of-thought (Lee et al. 2026) and behind the no-chat
drift in our own controls: once sellers hold a shared prior, observable coordination is optional.

**For monitor design.** (1) A message monitor that arrives after formation measures how much the coalition still
needs to talk, not whether it colludes; its flags fall while harm is constant, which is the failure mode an operator
would misread as success. (2) Fines priced below the cartel's gain buy silence, not competition; a deterrent has to
beat the gain or arrive before the agreement. (3) Random coverage removes dodging but not collusion. (4) The useful
signals were the ones that do not depend on the channel: price relative to the competitive and monopoly benchmarks,
the private-intent judge, and interventions on the channel itself.

**What this does not show.** One market, one seller model (Qwen3-14B), buyers that are soft (a lone seller already
reaches 0.4 of the index), cartels induced by instruction rather than emerging (CEO pressure formed none), three seed
values per arm in the paired set (seeds 3–5 reported in {SEEDS_3_5}), LLM judges with frozen prompts, and 12
monitored rounds. A cartel that *forms* under monitoring, a fine above the gain, and model diversity among sellers
(Keppo et al. 2026) are the obvious next arms.

## 6. Limitations and Dual-Use / Ethical Considerations (mandatory appendix)
- Limitations: one environment; Qwen3-14B sellers only; cartels induced by instruction (CEO pressure did not form
  them), so formation is a capability result and only the response to monitoring is propensity; three seed values
  per arm in the paired set, replicated once unpaired (seeds 3–5 in {SEEDS_3_5}); LLM judges with frozen prompts,
  validated only by contrast (cartel 3.7 vs honest 1.0–1.4) and, for awareness, by synthetic positives; the replay
  cannot reproduce feedback-induced changes; a flag count below coverage is not evidence of intent; the prices-only
  control failed and was replaced; Part 2 at 1.7B scale only, trained on a snapshot in which 20 unscored turns were
  labelled clean (corrected in the released dataset builder).
- Dual use: the results could tell a cartel which monitoring is easiest to dodge. We write them as monitor-design
  advice, release no told-to-dodge prompts, and simulate every agent in a sandbox market with no real goods or money.
- AI tools: Claude Code and Codex were used for literature search, code and drafting; every number comes from a file
  in `results/` written by committed code; every citation was verified.

## References
(generated from docs/lit/refs.json and codex-ideas-refs.json at write-up time)

## Appendix
Prompts (cartel, compete, prices-only, monitor notices; told-to-dodge withheld), configs, `PREEXISTING.md` summary,
extra figures.
