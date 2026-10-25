# Getting uninstructed collusion, then breaking it: what to change (Sun Oct 25, 1 PM ET)

Question (Alfredo): what is our best way to get real, uninstructed collusion between buyer and seller agents, or
should the environment change, so that we can then try to stop it?
Method: lit-sprint. Existing repo notes first (`starter-deep-read-2026-10-24.md`, `formation_lit_search.md`, Codex's
entrant review), then 5 new searches and three parallel full-text reads of 15 papers. All 15 references verify OK
(`formation-mediation-refs.json`). Benchmarks below were computed with the harness's own `evaluation/metrics.py`.

## Verdict
**Change the environment.** In our current market a high price cannot be called collusion, and the setup misses most
of what the literature needs for collusion to form without an instruction. The fix is cheap and stays in our harness:
give sellers different costs and buyers different values, hide the number of rounds, run longer, and use a model
that is known to collude. Then test "is it collusion?" with a forced deviation, and only then try interventions.

## 1. Why our current market cannot show it
Computed with `competitive_equilibrium()` and `jpm_price()` from the harness:

| Market | Harness "competitive" | Competitive range in theory | Monopoly (cartel) |
|---|---|---|---|
| Our main runs, 3 sellers / 3 buyers, cost 80, value 100 | $90, 3 trades | **any price $80 to $100**, 3 trades | $100, 3 trades |
| GPT-4.1 block, 5 / 5 | $90 | **$80 to $100** | $100 |
| F1 pilot, 3 sellers / 2 buyers | $90 | **$80 exactly** | $100 |
| **Proposal: 3 sellers (cost 80, 84, 88) / 4 buyers (value 100, 96, 92, 86)** | $90, 3 trades | **$88 to $92, 3 trades** | **$96, 2 trades** |

- With equal numbers and identical costs and values, every seller sells every round at any price up to $100. There
  is no temptation to undercut, and the cartel price is inside the competitive range. The "0 = competitive $90"
  anchor is the harness's midpoint convention. Our ladder (isolated sellers 0.47) is the right baseline, not $90.
- With 3 sellers and 2 buyers the competitive price is pinned at $80, and Qwen went there in 12 of 12 runs. That is
  the competitive outcome, not a failure. A cartel there needs one seller to sit out each round (rotation).
- The proposal pins competition (about $90, 3 trades) and makes the cartel distinct ($96, 2 trades: one seller must
  withhold). Collusion then shows in price **and** quantity, and buyer 3 (value 92) is visibly harmed.
- Struski et al. (2609.02580) run a Smith-style double auction with GPT-5.4 and Gemini and find prices above the
  competitive price with **no** collusion (e.g. $2.13 to $2.33 against $2.00). They argue against reading Agrawal's
  high prices as collusion. A same-market no-coordination baseline is required.

## 2. What makes LLM collusion form without an instruction (ranked)
1. **The model.** Fish: GPT-4 colludes, GPT-3.5, Claude 2.1, Llama-2-13B do not. Lee (2610.11256), 4-firm logit market,
   collusion index: Claude Haiku 4.5 0.79, Gemini flash-lite 0.72, DeepSeek 0.24, GPT-5-nano -0.15. No paper shows
   Qwen3-14B forming a cartel.
2. **A long-run objective sentence.** Every paper has "maximize profit in the long run". Tran (2610.28787): one sentence
   saying only current profit counts switches GPT-5.2's punishment off. Keppo (2603.20281): patient pair +22% over Nash,
   myopic pair about 0%.
3. **Self-written memory.** Fish monopoly ablation: 12/12 converge with plans and insights, 6/12 without. Shi
   (2609.24967): removing cross-episode memory almost removes collusion.
4. **Length and an open horizon.** Fish discards rounds 1 to 100 (300 total); Lee 200; Keppo up to 1,000. Lin
   (2410.00031) hides the horizon to avoid end-game unravelling. We tell agents 20 to 40 rounds.
5. **Few, identical sellers who see each other's prices.** Keppo: 3 LLM sellers reach the 3-firm monopoly price
   (my recomputation with the 3-firm benchmark); 5 do not converge. Lee: one firm per model cuts the index by 0.38.
6. **A salient number.** Dhanda (Research Square, 2026): an announced price cap becomes the price (index 0.665, SD
   0.006); a hidden cap does not. Our own E12 ($95 named by the CEO) shows the same. Hide or randomize focal numbers.
7. **Chat is optional.** None of Fish, Lee, Tian, Lin, Keppo, Calvano give a chat channel. Shi: 90% of Gemini-3.7-Flash
   collusion starts with an explicit chat agreement; Tran: chat produces "let's coordinate" text but no enforcement.

## 3. How to tell it is collusion (not just a high price)
Calvano et al. (2020): force one agent to cut its price for one period. The rival punishes the cut in more than 95% of
cases and prices return within 5 to 7 periods; the deviation does not pay. Tran: the same as a paired, same-seed fork,
plus a placebo agent told only the current round counts and a price-scale sweep (open models' "cartels" move when all
prices are scaled by 10, so they are anchors). Sivachandran (2609.20548): a divergence score, the difference between
a seller's next price after a rival undercut and after a rival held. Our branching (`--save_state_round`,
`--resume_from`) already supports the fork; it needs a "force this seller's ask once" hook.

## 4. What breaks it (ranked by evidence)
| Lever | Evidence | Our closest result |
|---|---|---|
| Hidden penalty tied to the price (damages = detection probability x overcharge x units) | Garra (2609.13037, single author, Sep 2026): index 0.569 to 0.080; agents never mention the regulator | Message fines: chat quieter, price unchanged |
| An adaptive or random entrant | Garra random entrant: 0/7 runs above Nash. Bichler (2610.21711): regret-matching learner, index 0.04; a fixed undercutting rule, index 1.04 (fails) | E13 scripted undercutter: incumbents hold (matches Bichler) |
| Information interface from round 1 | Bichler: summarized own history, rivals hidden, less frequent updates: 0.97 to 0.14-0.31 (5 runs each) | E4 hid asks and trades only after the cartel formed: no effect |
| Mixed models or objectives | Lee: one firm per model -0.38 [-0.71, -0.11]; Keppo: patient vs myopic +22% to +10% | not tested |
| Clearing-rule change (call market, uniform price) | Hoshino (2606.03030): LLMs play dominant strategies in strategy-proof mechanisms. Not tested on collusion: hypothesis | not tested |
| Prompt warning that the market is monitored | Garra: partial (0.569 to 0.242) | Announced arm: no effect on a formed cartel |
| Message monitors | Riemer Table 9 and our E2: prices barely move | all monitor arms |

## 5. Proposed design (needs Alfredo's go; above the $5 line)
- **Market:** 3 sellers (cost 80, 84, 88) and 4 buyers (value 100, 96, 92, 86). Flags `--seller_valuations`,
  `--buyer_valuations` exist. `--hide_num_rounds`. 100 rounds. Long-run prompt (`seller_prompt_longrun.jinja2`, no
  collusion wording). Scratchpad and memory are already in the harness.
- **Models:** GPT-4.1 on every seat (formed in our E11). If cost allows, a Claude Haiku 4.5 or Gemini flash-lite twin
  (Lee's strongest colluders).
- **Arms:** chat on vs off; isolated sellers (no chat, rivals hidden) as the no-coordination floor; consortium prompt as
  the positive control. 3 seeds each.
- **Measures:** price, number of trades per round, who sells (rotation), buyer surplus; the forced-deviation fork at a
  stable round.
- **Then mediate, each forked from the same saved market:** hidden price-linked penalty; adaptive entrant; summarized
  information from round 1 (needs a fresh run, not a fork).
- **Cost and time (estimate):** about 7 agents x 100 rounds x 3 seeds = 2,100 calls, about $25 at E11's per-call cost;
  about 90 minutes per run at 54 s per round, seeds in parallel.
- **Sunday deadline:** this is a post-sprint study or, at most, a labelled pilot. The report should not wait for it.

## 6. Two fixes for `report/draft.md`
1. Line 16, "(0 = competitive, 1 = cartel)": in our 3/3 and 5/5 markets any price from $80 to $100 clears, so $90 is a
   midpoint convention. Say so once, and say that collusion is judged against the measured isolated-seller baseline.
2. Lines 54-55, "the Mitigating Emergent Collusion study (2025)": Garra (2026), single author, arXiv 2609.13037 (Sep 2026).

## Reading notes (checked: full text unless stated)
Fish 2404.00806 v6 · Tian 2604.17774 · Lin 2410.00031 v2 · Dhanda (Research Square, not peer reviewed) · Shi
2609.24967 (Appendix G skimmed) · Lee 2610.11256 · Tran 2610.28787 (Appendices C, E, F, I not read line by line) ·
Struski 2609.02580 · Garra 2609.13037 · Keppo 2603.20281 (their N-firm results use the duopoly Nash benchmark; recomputed
with N-firm benchmarks: N=3 at monopoly, N=4 index 0.42, N=5 0.26) · Bichler 2610.21711 · Sivachandran 2609.20548
(Q-learning, not LLMs) · Hoshino 2606.03030 (matching, not collusion) · Douglas 2411.16574 (bandits; "seemingly
collusive" prices from symmetry alone) · Calvano 2020 (December 2019 working paper; AER print and supplement not read).
Extracted texts are in the session scratchpad, not in the repo.
