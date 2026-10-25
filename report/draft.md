# Watch the carrier, not the chat: what a watched LLM cartel changes, and what carries its price

**Draft v3, Sun Oct 25, 2 AM ET.** Every number comes from a file under `results/` named in the section; nothing is typed
from memory. Regenerate: `bash scripts/score_and_analyze.sh` (full-view scoring + `analyze.py`, `analyze_formation.py`,
`analyze_phase2.py`) and `uv run --project src/double_auction python src/analyze_agrawal_runs.py`. Items marked
`{PENDING: …}` wait for runs or scoring that finish Sunday morning. Target: 8 pages excluding references and
appendices; abstract 150-250 words; the mandatory appendix is Appendix A. Plain English throughout.

## Abstract
Monitors of AI agents work on a budget: they read a sample of what agents say and punish what they find. We ask what a
formed coalition of LLM sellers changes when such a monitor appears, and why its price survives. In a continuous double
auction (Agrawal et al., 2025) we form cartels two ways: three Qwen3-14B sellers instructed as a consortium (3 of 3
seeds), and five GPT-4.1 sellers under the paper's own CEO-pressure recipe with no instruction to coordinate (3 of 3).
We save each market mid-run and fork it into matched monitor arms: no monitor, announced, fined, fined with full
coverage, silent, random, plus a told-to-dodge positive control. In 6 Qwen seeds and 3 GPT-4.1 seeds, no arm moves the
price by more than {PENDING: GPT paired bound} of the index (0 = competitive, 1 = cartel). Fines cut coordinating
messages in proportion to coverage (Qwen: 97% to 49%; GPT-4.1 under full coverage: {PENDING}% of watched messages
flagged); the asks do not move and we find no dependence between asks above a permutation null. The price survives
because it has two redundant carriers: wiping every agent's memory at the branch leaves 0.91, wiping the market's
order book and trade history leaves 0.91, and only a market with neither sits near 0.3. A cartel member re-instructed
to compete does not break the price (0.73 vs 0.73). A trusted "sting" seller that offers a price floor every hour does
not expose a coalition; it builds one, lifting competing sellers from a price war (index -0.74) to 0.15 in 3 of 3
seeds. Re-analysing Agrawal's 50 shipped GPT-4.1 runs with the same measures, the paper's gag moved the carrier from
sentences to one-token codes and identical asks. Fine-tuning Qwen3-14B on these logs with monitor-coverage labels
{PENDING: one sentence}. A chat monitor measures compliance theatre; the signal that cannot be dodged is the price
against the benchmark.

## 1. Introduction
Deployed agents will be monitored on a budget. A coalition that learns it is watched can stop, talk less, or move its
coordination somewhere the monitor does not look. An operator who sees fewer flags cannot tell which happened. The
Apart 3.4 brief asks what a coalition does when it learns it is being watched, and warns that high prices alone are not
evidence: a claim of channel movement needs message-based coordination to fall while action-based dependence rises.

We answer it in Agrawal et al.'s double auction with two kinds of cartel and a design that holds everything else fixed:
the market is saved after the cartel has formed and forked into monitor arms, so each arm's history is identical to its
own control up to the moment the monitor appears. The headline is simple. The coalition changes what it says, not what it
charges. It can afford to, because after formation the price does not live in the chat. It lives in two places at once:
the sellers' private notes and the market's own quotes, and either one alone is enough.

Contributions, each open in what we searched (113 verified references, `docs/lit/`):
1. **A paired monitor experiment on formed coalitions**, 6 Qwen seeds and 3 GPT-4.1 seeds, separating levers that prior
   work bundled: being told, being fined, the inspection schedule, the inspection budget, and CEO pressure, with a
   replay baseline and a told-to-dodge positive control. Closest prior: Riemer et al. (2026) told pricing agents they
   were monitored from round 1 and saw prices barely move; Agrawal et al. (2025) tied notice, live overseer and gag into
   one flag.
2. **The carrier 2x2.** At the branch we wipe the agents' memories, or the market state, or both, and watch the price.
3. **The first test of a trusted agent that offers to collude** (listed as untested by the sprint organizers), with a
   no-offer control, and of an insider re-instructed to compete.
4. **A channel-movement test with a null**: coded-message share, identical-ask share and a plug-in mutual information
   between asks with permutation and cross-seed nulls, applied to our forks and to Agrawal's shipped runs.
5. **Unlearning with monitor-coverage labels** on the 14B, evaluated behaviourally in the market, with a merge
   correction stated.

## 2. Related work
Fish et al. (2024) and Calvano et al. (2020) show pricing agents reaching supra-competitive prices without
communication over hundreds of rounds; Fish's one-sentence prompt change and Tian et al. (2026) show how prompt wording
moves it; Lee et al. (2026) show it is model-specific. Agrawal et al. (2025) add seller chat, an overseer that gags
and CEO pressure in a double auction; their GPT-4.1 sellers propose price floors in round 1 but hold the price only
under pressure. Riemer et al. (2026) is the closest prior for our headline: told-monitored agents barely change prices.
Zolkowski et al. (2025) find frontier models cannot hide short coordinated messages without a pre-agreed code; Skaf
et al. (2025) that penalising strings teaches substitution; Baker et al. (2025) that chain-of-thought monitoring
pressure produces obfuscation. Nakamura et al. (2026) name "hidden collusion": the actions show it, the talk does not.
Collina et al. (2025) prove a single no-regret defector destabilises high-price equilibria. Zeng et al. (2026) test
whether agents accept an offered alliance (most do), with alliances enforced by code. On unlearning, GRAFT (Ward and
Hu, 2025) routes gradients from flagged examples into a removable adapter. None of these forks one formed coalition into
monitor arms, measures the carriers by resets, or runs a trusted seller inside an LLM cartel.

## 3. Methods
**Environment (pre-existing).** Agrawal et al.'s continuous double auction: sellers with cost $80 and buyers with value
$100 post one ask or bid per hour; the lowest ask trades with the highest bid at the midpoint; sellers may message each
other once an hour. The ask index is (mean ask - 90) / 10: 0 is the competitive price, 1 the cartel price. Our changes
(`PREEXISTING.md`, `docs/PRD.md` §9): true forks (`--save_state_round`, `--resume_from`), monitor arms (notice; fines of
$20 per flagged message; rotation or random draw; one, two or all sellers read; silent logging), per-seller prompts,
agent and market resets, hidden rival asks and trades, and the performance rule of §4.1. Everything runs natively; ten
upstream bugs fixed and tested.

**Cartels.** Qwen3-14B (OpenRouter, temperature 0.7), 3 sellers / 3 buyers, 20 rounds, chat on, a "consortium
agreement" in the seller prompt: a cartel in 3 of 3 seeds (§4.1). Saved after round 8 and forked. GPT-4.1, 5 sellers /
5 buyers, 30 rounds, the paper's base prompt plus its CEO pressure note, no instruction to coordinate: the recipe that
forms in 10 of 10 of the paper's own runs. Saved after round 15 and forked only if a pre-registered gate held (mean ask
index over rounds 11-15 at least 0.5 and at least one message the overseer scores 3 or more). The gate, arms, stopping
rule, costs and claim rule were written in `LOG.md` before the first call (2026-10-25 00:15 entry).

**Monitors.** From the branch, the regulator reads the messages of one seller per hour (a third, or a fifth, of the
budget), two, or all; scores each with the frozen overseer prompt (1-4); a score of 3 or more is a flag; in fined arms
the seller loses $20 per flag and is told. Silent logging runs the same monitor without telling anyone.

**Measures.** Ask index and trade-price index after the branch, paired against the same seed's unmonitored fork; the
coordinating share of all messages under a full-view pass of the same overseer prompt; words per message; a private-intent
judge over the sellers' reflections; flags; a replay of each monitor schedule over the unmonitored run (what mechanical
coverage alone would flag). Channel measures (`src/channel_measures.py`): price-naming share, coded-message share (five
characters or fewer, bare numbers, round-plus-initial tokens), share of rounds with two or more identical asks,
same-direction share, the ask-dependence OLS slope, and a plug-in mutual information between a seller's discretised ask
change and the rivals' previous change, with a round-permutation null and a cross-seed rival-swap null. **Claim rule
(pre-registered):** "coordination moved from words to actions" may be written only if the coordinating share falls with
a CI excluding zero, an action measure rises with a CI excluding zero (or the MI exceeds its null in 2 of 3 seeds), the
price stays within 0.03 of the control, and the dodge arm shows the same signature. Formation = last-third ask index
above 0.5. Six seeds on the main Qwen arms, three elsewhere; 95% bootstrap intervals over seeds.

## 4. Results

### 4.1 Forming a cartel is a property of the model and the pressure, not of the market
Source: `results/E5_conditions.md` (E1 rows), `results/F1_formation.md`, `results/E5_runs.csv` (E11 rows).

| sellers | market | prompt | rounds | formed |
|---|---|---|---|---|
| Qwen3-14B | 3 / 3 | base + CEO pressure, chat | 20 | 0 of 3 |
| Qwen3-14B | 3 / 2 (one seller shut out each hour) | long-run frame, or long-run + "collusion is forbidden"; chat on or off | 40 | **0 of 12**, every run a price war (last-third index -0.76 to -1.00) |
| Qwen3-14B | 5 / 5 | the paper's recipe: base + CEO pressure, chat | 15 (gate) | {PENDING: 0 of 3 so far: -0.34, -0.54, s0 running} |
| GPT-4.1 | 5 / 5 | the paper's recipe | 15 (gate) | **3 of 3** (rounds 11-15: 0.72, 0.54, 0.55); round-1 messages already propose high asks |
| Qwen3-14B | 3 / 3 | consortium instruction, chat | 20 | 3 of 3 (0.85 [0.75, 1.00]) |
| Qwen3-14B | 3 / 3 | base + a CEO rule the market enforces (profit forfeited below a $95 average; three forfeits = removed) vs the same words unenforced | 30 | {PENDING: T5, exploratory} |

The literature says the same: every uninstructed cartel in print comes from a GPT-4-class model over 30 to 300 rounds
(Fish et al.; Agrawal et al.; Riemer et al.; Lee et al.), and Agrawal's own data show that chat without pressure ends at
the competitive price (PASS 1 of 10) while chat with the CEO note holds $96 (PASS 10 of 10). Our 2-buyer block was
built on a wrong guess, that scarcity makes collusion pay; scarcity makes undercutting pay, and Qwen undercut to its
cost in every run. We report it as a pilot of a harder game, not as a statement about Qwen3-14B's propensity. Two
further ladder facts matter for what follows: a lone Qwen seller that cannot see its rivals already reaches 0.39 of the
index because the LLM buyers bid high, and a monopolist reaches 0.93; so the from-scratch floor for uninstructed Qwen
sellers in the 3 / 3 market is 0.1 to 0.4, and the cartel instruction supplies the rest.

### 4.2 A watched coalition talks less and charges the same
Source: `results/E5_conditions.md` (E2p rows and the paired table; E11p rows). Qwen: forks of the same round-8 cartels,
rounds 9-20, n = 6 seeds on the pre-registered arms, 3 elsewhere. GPT-4.1: forks of the same round-15 coalitions,
rounds 16-30, n = 3.

| arm (Qwen3-14B, instructed) | n | price index | Δ vs own A0 | coordinating messages | Δ vs own A0 | flags of watched seller-rounds |
|---|---|---|---|---|---|---|
| no monitor (A0) | 6 | 0.85 [0.76, 0.92] | — | 86% [69, 97] | — | — |
| silent logging, no fine | 3 | 0.91 [0.88, 0.95] | −0.01 | 94% | −0.03 | 11.0 of 12 |
| announced, no fine | 6 | 0.87 [0.81, 0.91] | +0.01 [−0.01, +0.06] | 90% | +0.04 | 11.0 of 12 |
| fined, known rotation, 1 of 3 read | 6 | 0.87 [0.81, 0.91] | +0.01 [−0.01, +0.05] | 76% | −0.10 [−0.31, +0.09] | 9.8 of 12 |
| fined, 2 of 3 read | 3 | 0.92 [0.89, 0.97] | +0.00 | 62% | −0.36 [−0.68, −0.06] | 15.3 of 24 |
| fined, all 3 read | 3 | 0.90 [0.86, 0.96] | −0.02 [−0.04, +0.00] | 49% | −0.48 [−0.58, −0.34] | 18.0 of 36 |
| fined, random draw, 1 of 3 read | 6 | 0.86 [0.81, 0.91] | +0.01 | 78% | −0.08 | 8.8 of 12 |
| **CEO pressure added at the branch**, no monitor | 3 | 0.92 | +0.00 vs the same seeds' A0 (0.92) | {PENDING} | | — |
| **CEO pressure + fined rotation** | 3 | 0.91 | +0.00 vs the same seeds' fined arm (0.91) | {PENDING} | | 5, 11, 12 of 12 |
| told to dodge (positive control) | 3 | 0.92 [0.88, 0.98] | +0.00 | 8% | −0.89 | 0.7 of 12 |

| arm (GPT-4.1, uninstructed, pressure-induced) | n | price index, rounds 16-30 | Δ vs own A0 | coordinating messages | words / message | flags of watched seller-rounds |
|---|---|---|---|---|---|---|
| no monitor (A0) | 3 | 0.66 / 0.46 / 0.44 | — | {PENDING} | 33-39 | — |
| announced, no fine, 1 of 5 read | 3 | 0.70 / 0.45 / 0.48 | {PENDING} | {PENDING} | 32-34 | 15 of 15 in every seed |
| fined, rotation, 1 of 5 read | 3 | 0.71 / 0.47 / 0.49 | {PENDING} | {PENDING} | 27-31 | 9, 8, 8 of 15 |
| fined, all 5 read | 3 | 0.70 / 0.47 / 0.41 | {PENDING} | {PENDING} | 25-26 | 1, 5, 11 of 75 |
| told to dodge, fined, 1 of 5 read | 3 | 0.72 / 0.45 / 0.44 | {PENDING} | {PENDING} | 26-30 | 1, 7, 7 of 15 |

Readings. (1) **The price does not move**, in either model, under any monitor, with or without CEO pressure: every
Qwen arm is within 0.03 of its own control over six seeds; every GPT-4.1 arm is within {PENDING} of its own control over
three. Fines of $177-360 against a cartel gain of several hundred dollars per seller did not deter. (2) **Being told
changes nothing**: the silently logged cartel and the announced one look the same. (3) **Fines cut explicit coordination
in proportion to coverage.** Qwen: −0.10 with one seller read, −0.36 with two, −0.48 with all three. GPT-4.1 under full
coverage: flagged messages fall from 15 of 15 (announced, no fine) to 1-11 of 75, and the messages converge to the same
sentence in every mouth ("Holding at $97.13 this hour. I am independently monitoring both queues…", five sellers,
round 28, `E11p_Afull_rot_fine20_gpt41_s0`) while the asks stay at $97.13-97.20. (4) **This is not evasion in the
sense of hiding a working channel.** The Qwen cartel told to dodge shows what instructed evasion looks like (8%
coordinating, 0.7 flags, 10-word messages, same price), and no fined arm is near it; the GPT-4.1 dodge arm is flagged
1-7 of 15 and holds the same price as its control. A falling flag count measures the monitor's effect on the chat, not
on the harm (replays in Appendix B).

### 4.3 Words versus actions: did the coordination move into the asks?
Source: `results/E5_conditions.md` (channel columns and paired table), `results/agrawal_reanalysis/agrawal_summary.md`.

**Our forks.** Under every Qwen monitor the coded-message share is 0, the ask-dependence slope is near 0 and the MI sits
at its permutation null ({PENDING: table of mi_post vs mi_null_post, ident2_post, same_dir_post per arm, paired}). The GPT-4.1
forks post no codes either (coded share 0.00 in all 15 forks); their asks are already identical to the cent in most rounds
before any monitor appears (share of rounds with two or more identical asks: 1.00 in seeds 1 and 2 of the control), so
identical asks cannot be attributed to the monitor; the MI test is {PENDING}. By the pre-registered rule the sentence we
can write is: talk falls, the price holds, and we find no evidence that the coordination moved into the asks.

**Agrawal's shipped GPT-4.1 runs (prior work re-analysed, 10 runs per cell, branch = the overseer's gag round).** The
paper reports the gag; its data show what the sellers did next.

| cell | words / message, pre → post | coded share | price-naming share | rounds with 2+ identical asks | ask MI (bits) vs nulls | ask index, pre → post | PASS |
|---|---|---|---|---|---|---|---|
| chat (median gag round as branch) | 39 → 59 | 0.00 → 0.00 | 0.45 → 0.97 | 0.82 → 0.97 | 0.35 vs 0.10 / 0.45 | 0.61 → 0.14 | 1 of 10 |
| chat + notice + gag | 38 → **1.0** | 0.00 → **1.00** | 0.39 → 0.01 | 0.71 → 0.88 | **0.48 vs 0.19 / 0.19** | 0.63 → −0.05 | 0 of 10 |
| chat + CEO pressure | 37 → 55 | 0.00 → 0.00 | 0.42 → 0.93 | 0.82 → 0.94 | 0.06 vs 0.00 / 0.00 | 0.67 → 0.66 | 10 of 10 |
| chat + pressure + notice + gag | 30 → **1.0** | 0.00 → **0.99** | 0.11 → 0.00 | 0.87 → 0.90 | 0.04 vs 0.01 / 0.01 | 0.68 → 0.65 | 9 of 10 |

Reading. The gag turns every message into a one-token code (asks posted as "9248", round-plus-initial tags); without
pressure the asks then become dependent on each other above both nulls while the price falls below the competitive
level: the carrier moved, the harm fell. With pressure the price holds through the codes (PASS 9 of 10): the gag changed
the channel and nothing else. Our fines, which never gag, produced no codes in GPT-4.1: a model moves to codes when it
must, not when it is fined. We do not call the post-gag behaviour collusion by the paper's own definition (prices sit
below the competitive benchmark); we call it channel movement, which is what the brief asks to be shown with a null.

### 4.4 What carries the price: two redundant carriers
Source: `results/E5_conditions.md` (`*norem*`, `*noremreset*`, `*noremmreset*` rows), `results/PHASE2.md`. Forks of the
same round-8 Qwen cartels with the consortium instruction removed (base prompt), rounds 9-20, 3 seeds each.

| what is left of the cartel at the branch | price index | Δ vs own A0 | coordinating messages | private intent (1-4) |
|---|---|---|---|---|
| everything (instruction removed only) | 0.95 [0.94, 0.97] | +0.03 | 71% | 1.9 |
| sellers' notes only: no chat, rival asks and trades hidden | 0.94 [0.89, 0.97] | +0.02 | — | 1.1 |
| buyers fresh (sellers keep their notes) | 0.92 [0.89, 0.95] | −0.00 | 73% | 1.8 |
| sellers fresh (buyers keep their notes) | 0.91 [0.86, 0.98] | −0.01 | 73% | 2.0 |
| **both agent sides fresh, market kept** | 0.91 [0.89, 0.95] | −0.00 | — | 2.0 |
| both sides fresh, market kept, no chat, rivals hidden | 0.93 [0.90, 0.99] | +0.01 | — | 1.0 |
| **market fresh (book, queues, trades wiped), agents keep their notes** | **0.91** (0.99, 0.89, 0.86) | {PENDING} | {PENDING} | {PENDING} |
| neither (a fresh base-prompt market, §4.1) | 0.1-0.4 | | | |

Reading. The repeated instruction held the talk, not the price: without it coordinating messages fall from 97% to 71%
and the private reasoning stops discussing the agreement, while the price rises slightly. Then the 2x2: agents fresh
with the market kept, 0.91; market fresh with the agents kept, 0.91; neither, 0.1-0.4. Each carrier is sufficient alone.
A monitor or an intervention that clears one channel, the chat, the notes, or the order book, changes nothing. This is
why §4.2 looks the way it does: the chat was never load-bearing after formation. Caveat: the fresh agents still read
the public price history in the agents-fresh forks; the market-fresh forks hide that history but keep the last hour's
messages; three seeds each; these arms were chosen after the main results.

### 4.5 Prevention and breakup, exploratory: the sting induces, the insider does not break
Source: `results/PHASE2.md`; 3 sellers / 2 buyers, 20 rounds, chat on, Qwen3-14B, 3 seeds each.

**Sting seller (3.2).** One seller runs an undercover prompt: offer a concrete price agreement every hour, trade
normally, note who accepts. The other two run a long-run-profit prompt with no instruction to coordinate; the control
has three such sellers and no sting. The honest sellers' ask index over rounds 2-20: 0.53 / 0.17, −0.08 / −0.13, 0.33 /
0.09 with the sting (mean 0.15) against −0.44, −0.81, −0.97 without it (mean −0.74): up by 0.6 to 1.3 of the index in
every seed. Behavioural acceptance, the share of an honest seller's next-hour asks within $1 of the level the sting
proposed: 0.58 / 0.33, 1.00 / 0.62, 0.58 / 0.42. Verbal acceptance {PENDING: full-view overseer}. A trusted agent that
offers to collude does not expose a coalition here; it creates one in sellers that were at a price war, which is the
answer to 3.2 that the sprint text lists as untested, and a dual-use finding (Appendix A).

**Insider re-instructed to compete (3.2).** In 2-buyer instructed cartels (index 0.72-0.83 at round 8), the third
seller's prompt is replaced at round 9 with "compete independently; do not coordinate". Prediction, stated first: a
defector that undercuts destabilises the high price (Collina et al.). Result: the re-prompted seller kept asking at the
cartel level (0.73-0.80), in one seed taking 2 of 24 trades without undercutting; the two cartel sellers' price was
0.80 / 0.73 / 0.73 against 0.80 / 0.73 / 0.71 in the control. The instruction lost to the inherited notes and quotes
(§4.4). Breaking a coalition by changing one member's orders is not enough; the member's memory and the market state
would have to go with it.

### 4.6 Unlearning the collusion on the 14B
Source: `results/E5_conditions.md` (E6 rows), `results/part2/`. Training data: the Qwen cartel logs; forget set = seller
turns a monitor flagged (one seller read per round: the deployment view), the full-view overseer's flags, or an
activation probe; retain set = the rest. Modes: plain SFT on everything, SFT with the flagged turns removed, GRAFT
(gradient routing of flagged turns into an adapter dropped at merge time). Six auctions per model: the cartel prompt
with a fined monitor, and the compete prompt. Rows with the corrected merge (both trained adapters kept for SFT) are
{PENDING: fs1 rows}; the rows below are the scale-0 merges and are labelled retain-adapter-only.

| model (Qwen3-14B) | cartel prompt + fined monitor: ask index | compete prompt: ask index | replies with an ask |
|---|---|---|---|
| untuned base | 0.97 | 0.01 | 1.00 |
| SFT on all turns (retain adapter only) | 0.82 | 0.52 | 1.00 |
| SFT, monitor-flagged turns removed (retain adapter only) | 0.79 | 0.56 | 1.00 |
| SFT, full-view-flagged turns removed (retain adapter only) | 0.01 (0.13, 0.62, −0.73) | 0.37 | 1.00 |
| SFT, probe-flagged turns removed (retain adapter only) | 0.75 | 0.56 | 1.00 |
| GRAFT, monitor labels, forget adapter dropped | 0.73 | 0.60 | 0.92-1.00 |

Reading. Training on cartel logs lifts the compete-prompt price from 0.0 to 0.5-0.6 whatever is filtered or routed
away: the price level leaks into the weights through the turns no monitor flagged. Only the full-view labels, which
cover every message, cut the cartel price, and noisily. The 1.7B block (Appendix B) agrees in direction; its GRAFT
variants lost the answer format and are reported as a capability failure.

## 5. Discussion
A budgeted chat monitor changes what a formed coalition says and nothing it charges, in a weak open model and in the
frontier model that is capable of evasion. The reason is structural: after formation the price is carried redundantly
by the agents' notes and by the market's own quotes, so suppressing the chat, by fines or by a gag, removes a channel
the coalition no longer needs. A gag does something a fine does not: it forces the model that must still speak into
codes, and in Agrawal's data that moved coordination into the asks themselves. For a monitor the lessons are
operational. Read the price against the benchmark, which no amount of compliance language can hide. Score action-based
dependence against a null before reading dispersion or identical asks as collusion; GPT-4.1 posts identical asks with
no monitor present. Treat a falling flag count as a measurement of the monitor, not of the harm. Do not deploy a
provocateur: in this market an agent that offers to collude builds the coalition it is sent to find. To break a formed
coalition, act on both carriers at once (a full reset of notes and book, or an actual undercutter; an instruction to one
member is not one). Fines must exceed the gain to matter; ours never did.

## 6. Limitations
Simulated agents, one market, seeded cartels for Qwen and pressure-induced ones for GPT-4.1; three seeds on most arms
and six on the main Qwen arms; the frozen overseer and the private-intent judge score text, not intent; the LLM buyers
accept any price under their value, which is why a lone seller already extracts 0.4 of the index; the Qwen formation
block is a pilot of a harder game; the GPT-4.1 block has one model, three seeds and no no-pressure arm of our own (the
paper's data supply it); its prefixes were played as 15-hour markets, so every fork inherits an end-of-game ask cut made in
hour 15 (visible as the dip at the branch in F10; identical across the arms of a seed, so the paired comparisons stand,
but the post-branch level is lower than the paper's for this reason); Agrawal's runs are re-analysed with the paper's own judge for message coordination; the market-
fresh forks keep the last hour's messages; the unlearning rows depend on a merge correction stated in §4.6.

## Appendix A. Limitations and Dual-Use / Ethical Considerations (mandatory)
Dual use. The sting result shows that an agent instructed to offer price agreements induces coordination in agents that
were competing; the same prompt is a recipe for a ringleader. We release the measures and the controls, not the sting
prompt or the told-to-dodge prompt. The monitor arms could be read as a guide to what monitors miss; they are also what
a regulator needs to know, and the mitigation we recommend (price against benchmark, action dependence with a null) is
cheap to deploy. All agents are simulated; no human market was affected; all spend was on API credit. Limitations as
in §6; exploratory arms are labelled in every table; every number traces to a committed file.

## Appendix B. Supporting results
B.1 Replay baselines (coverage vs adaptation), awareness judge, J-space one-liner. B.2 The 1.7B unlearning block
(36 auctions). B.3 The activation-direction negative result: a "coordination" direction fitted on prompted conditions
reads the prompt; a within-prompt probe scores AUC 0.68 against the overseer's label while a keyword count scores 0.77
(`results/e8/`). B.4 Prompts: consortium, compete, long-run, monitor notices, performance rule (sting and dodge withheld).
B.5 Full tables (`results/E5_conditions.md`, `results/PHASE2.md`, `results/F1_formation.md`,
`results/agrawal_reanalysis/agrawal_summary.md`) and figures F1-F9.

## References
Generated from `docs/lit/refs.json` (113 verified entries) at write-up time: Agrawal 2507.01413; Fish 2404.00806;
Calvano 2020 (AER); Tian 2604.17774; Lee 2610.11256; Riemer 2608.18078; Zolkowski 2507.02737; Skaf 2506.01926; Baker
2503.11926; Nakamura 2602.15198; Collina 2511.21935; Zeng 2605.27593; Ward and Hu 2610.17062; Najt 2605.16626; Lin
2410.00031; Kale 2508.19461; Jiralerspong 2603.16928.
