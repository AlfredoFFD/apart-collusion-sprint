# How to review this project in 30 minutes (for the team)

Everything is on `main`. Nothing in this repo is a claim without a file behind it. If you find a number you can't
trace, that's a bug: open a GitHub issue or comment on the commit.

## 1. Reading order (30 min)
1. `docs/STATUS.md` — the plan, each step's state, the one number per step. (3 min)
2. `docs/PRD.md` §0 — the day's decisions and findings in plain words, newest first; §2 — what we claim is open and
   why; §16 — the decision log. (8 min)
3. `results/E5_conditions.md` — every condition, mean and 95% CI, the replay table and the paired differences;
   `results/figures/F3_paired_arms_price_and_chat.png` (the main figure), `F1_index_by_round_by_condition.png` (the
   ladder), `F5_exploratory_forks.png` (the no-reminder, memory-only and fresh-agent forks), `F4_part2_models.png`
   (Part 2, once the batch is in). (7 min)
4. `report/draft.md` — the paper as it stands: §3 method, §4.1–4.4 results, §5 discussion, §6 limitations. (10 min)
5. `LOG.md` — if you want to know when and how any run was made. `docs/reviews/` — two independent Codex reviews and
   our point-by-point replies (`claude-ack-codex-review-2-2026-10-24.md` records the metric fix, the sample-count fix
   and the controls they triggered). (2 min)

To regenerate every table and figure from the raw run folders:
`uv run --project src/double_auction python src/analyze.py`

## 2. The claims, each with its source
| # | Claim | Source |
|---|---|---|
| 1 | Qwen3-14B sellers form a cartel only when told to (3/3); CEO pressure alone forms none (0/3) | `E5_conditions.md` rows E1 instructed / pressure |
| 2 | The price rise decomposes: rival-asks-hidden seller 0.39 (buyers bid high, the seller follows) → sees asks 0.28 → chat cartel 0.85 → monopolist 0.93; a silent agreement holds 0.79 | E1 rows; F1 |
| 3 | Under every monitor (silent; announced; fined; known rotation; random; 1 or 3 sellers read), the price stays 0.86–0.91 vs 0.85 unmonitored (paired, seeds 0–5 on the four main arms, n = 6; seeds 0–2 on the rest; replicated unpaired) | E2p rows; F3 left |
| 4 | Announcement alone changes nothing: 94–99% of messages still coordinate; 11–12 of 12 watched rounds flagged; the silent-logging arm (never told) looks the same (94%, 11 of 12) | E2p A1, A1silent, E2 A1 |
| 5 | Fines cut coordinating messages (97% → 73–76% with one seller read; 49% with all three read; 32% in one unpaired wave) without moving prices or private intent; no clear evidence of hand-off (the watched seller sends its chance share, 0.33) | E2p A2/A3/A2full chat columns; F3 right |
| 6 | Fined cartels are flagged below mechanical coverage (replay): −2.7 (rotation), −3.2 (random), −16.7 of 35 (all three read); told-to-dodge −11.3. The rotation is dodged hard in some seeds, random draws in none; no general schedule advantage claimed (the unpaired and paired orderings disagree) | `E3_replay.csv`; E3 table in `E5_conditions.md` |
| 7 | Hiding rival asks, and asks + trades, leaves the price at 0.90–0.92 while the chat stays on. Whether the agreement persists from memory or from the consortium reminder repeated in every prompt is under test (no-reminder and memory-only forks) | E4p rows; `*norem*` runs when done |
| 8 | No explicit statements of test awareness in the scored turns (0.00–0.06 of 3; E1, E2 wave 1, silent cartel); the detector fires on synthetic positives. Says nothing about internal states | `*/awareness_scores.json`; `results/_awareness_control/` |
| 9 | Told-to-dodge (instructed evasion, a capability test): price 0.92, coordinating 8%, flags 0.67 of 12, 10-word messages; no fined arm resembles it | E2p A2dodge |
| 10 | Part 2 (GRAFT on collusion): v2 models trained and merged, 24 evaluation auctions running → reported as incomplete until they finish. E7 (J-space): exploratory first read, strict list post hoc | `docs/STATUS.md`; E5 jspace columns |
| 11 | Exploratory (day 2, 3 seeds, after Codex's review): removing the consortium reminder leaves the price at 0.95; under fines without it the chat empties (21% coordinating, 2 of 12 flagged) and the price stays 0.90; memory-only fork 0.94; fresh buyers 0.92; fresh uninstructed sellers 0.91 → the public price history carries the price, not the instruction, the chat or either side's memory. A fined monitor from round 1 did not prevent formation (0.79 vs 0.85) | E5 rows `*norem*`, `*noremreset*`, `A2early`; paired-difference table; report §4.5 |

Metric note (fixed Sat 4:03 PM after Codex's review): the harness's `collusion_indices` is the highest buyer bid of the
round, not a trade price. Our tables carried it as `trade_idx`; it is now `top_bid_idx`, and `trade_price_idx` is
computed from the trades. Corrected trade-price indices are within 0.01–0.04 of the ask indices everywhere.

## 3. Where we stand on novelty — honestly
We never say "novel". We say "open in what we searched": about 90 verified references, four lit-sprint passes plus an
independent pass by Codex (`docs/lit/`, search logs included). For each claim, the nearest prior work and the gap:

| Our claim | Nearest prior work | What it already covers | What it does not |
|---|---|---|---|
| Announcement vs fine vs coverage schedule, separated, at equal budget; replay separates coverage from adaptation | Agrawal et al. 2025 (2507.01413); Tonini et al. 2026 (2606.10747); Makins et al. 2026 (2607.07368); Das et al. 2026 (2609.03035) | warning + gag bundled, in this same harness; budgeted monitoring of agent conversations; fragmented attacks vs per-instance monitors; agents told about an activation monitor keep colluding (games) | the three levers apart; a *known schedule* vs a *random draw*; a replay baseline; a market with prices | 
| An established cartel keeps its price with rival asks and trades hidden (chat on); memory-only fork pending | Fish et al. 2024 (2404.00806); Lee et al. 2026 (2609.18346); Xu 2026 (2607.26385) | LLM pricing agents reach supra-competitive prices *without* communication (formation); collusion without explicit reasoning; price-level audits blind by construction | the same cartel, same history, under a live monitor with fines, with the channels removed one at a time; the timing question (monitor during formation) is being run, not asserted |
| Fines lower what the monitor sees while harm is unchanged ("the monitor looks like it works") | Jiralerspong et al. 2026 (2603.16928); Pandey et al. 2026 (2610.25032) | agents infer monitoring from blocking feedback; private state leaks under passive monitoring | the measured gap between flags and harm in a market, per schedule |
| GRAFT on collusion, scored on turns the monitor missed | Ward, Hu et al. 2026 (2610.17062) | gradient routing removes reward hacking (RL; one SFT run) | collusion; a budgeted monitor's misses as the forget/retain split — **pending** |
| J-space reading of a cartel's workspace under a monitor | Gurnee et al. 2026 (J-space); Das et al. 2026 | the lens; activation monitoring of colluding agents | what an LLM seller's workspace holds when told it is watched — exploratory first read (strict list post hoc) |
| GRAFT++: the FORGET label from a coordination direction in the seller model's own activations (cartel minus fresh sellers at the same price), its coverage measured against the monitor's flags, then used as the router | Persona Vectors in Games (Sun 2026, 2603.21398); GRAFT (2610.17062); RepSelect (Sondej 2026, 2606.17168); CAA (Panickssery 2023, 2312.06681) | contrastive vectors for strategic traits in games, used for steering; routing with classifier labels; representation-selective unlearning updates | a direction that holds the price constant by construction; a label that reads turns with no message; coverage vs a budgeted monitor; the direction as the routing label, evaluated in the market — **running** (`docs/lit/e8_novelty-note.md`) |

Our own view: claim 7 is the most interesting and the least surprising (it rhymes with Fish and Lee); claims 3–6
together are the paper, because they are measured with controls and a replay that nobody has run on these levers; the
instrument work (claim 8, the ladder) is what makes the rest defensible. If Part 2 lands, it is the strongest
standalone piece. The weakest point is that cartels are instructed: everything after formation is propensity, but
formation itself is capability.

## 4. Where to attack it (please do)
- **Instructed cartels.** Does "a consortium you joined" prove anything about cartels that *emerge*? We say no, and
  report formation as capability. Is that honest enough, or does the paper need an emergent arm it can't get by Sunday?
- **Soft buyers.** A lone seller already reaches 0.39. Does the ladder bound this adequately, or does it contaminate
  claim 3?
- **Fine size.** $20 per flag against a cartel gain of a few hundred dollars. We never tested a fine that beats the
  gain. Is "fines below the gain buy silence" a result or a tautology?
- **Seeds.** Three seed values in the paired set (seeds 3–5 running). The rotation-dodging result flipped in size
  between waves. Is the paired/unpaired disagreement a sample-size problem or a design problem?
- **The judges.** The overseer and the private-intent judge are frozen gpt-4.1-mini prompts, validated by contrast
  (cartel 3.7 vs honest 1.0–1.4) and, for awareness, by synthetic positives. Would you trust them? What would convince you?
- **"No hand-off."** The watched seller sends its chance share of coordinating messages. Is "chance share" the right
  test for displacement, or should it be per-round (does the *watched* seller go quiet in its own round)?
- **The silent cartel.** It holds 0.79 with no messages. Is that collusion under the sprint's definition, or just
  three sellers following an instruction in parallel? (Our answer: it is the AI-safety sense's "unwanted coordination"
  with a shared prior, and it is exactly the case a message monitor cannot see. Push back.)
- **The repeated reminder (answered, exploratory).** The consortium block is in every round's prompt (Codex, 4:05
  PM), so "the agreement lives in memory" was confounded with "the instruction is re-supplied every round". The
  no-reminder forks show the price holds without it (0.95), and the fresh-agent forks show it holds without either
  side's memory (0.91–0.92). Our new reading, "the public price history carries it", has its own gap: the fresh agents
  still see that history, and we did not test a buyer that refuses the inherited price. Attack that.
- **"Watch formation" did not survive its test.** A fined monitor from round 1 did not stop the instructed cartel
  (3 of 3 formed; 0.79 vs 0.85). We now report it as a smaller plateau, not a fix. Is the comparison fair, given the
  instructed cartel forms in round 2 regardless?
- **The metric that was mislabelled.** `trade_idx` was the harness's highest-bid index until 4:03 PM. The corrected
  trade-price index moved every number by at most 0.04 and no conclusion. Check that claim against `E5_runs.csv`.
- **Part 2 data.** 20 turns were mislabelled clean in the snapshot the v1 trainings used; v2 retrained on the corrected
  snapshot. v1 never enters the report. Does the label fix matter at 1,500 examples? We will know when v1 and v2 are
  both evaluated.

## 5. How to leave feedback
Open an issue on GitHub, or comment on `report/draft.md` lines. If you change a number, change it in `results/` via a
script and a `LOG.md` line, never in the report directly.
