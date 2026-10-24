# How to review this project in 30 minutes (for the team)

Everything is on `main`. Nothing in this repo is a claim without a file behind it. If you find a number you can't
trace, that's a bug: open a GitHub issue or comment on the commit.

## 1. Reading order (30 min)
1. `docs/STATUS.md` — the plan, each step's state, the one number per step. (3 min)
2. `docs/PRD.md` §0 — the day's decisions and findings in plain words, newest first; §2 — what we claim is open and
   why; §16 — the decision log. (8 min)
3. `results/E5_conditions.md` — every condition, mean and 95% CI; `results/figures/F3_paired_arms_price_and_chat.png`
   (the main figure) and `F1_index_by_round_by_condition.png` (the ladder). (7 min)
4. `report/draft.md` — the paper as it stands: §3 method, §4.1–4.4 results, §5 discussion, §6 limitations. (10 min)
5. `LOG.md` — if you want to know when and how any run was made. `docs/reviews/codex-claude-audit-2026-10-24.md` —
   an independent audit of the pipeline and what it changed. (2 min)

To regenerate every table and figure from the raw run folders:
`uv run --project src/double_auction python src/analyze.py`

## 2. The claims, each with its source
| # | Claim | Source |
|---|---|---|
| 1 | Qwen3-14B sellers form a cartel only when told to (3/3); CEO pressure alone forms none (0/3) | `E5_conditions.md` rows E1 instructed / pressure |
| 2 | The price rise decomposes: isolated seller 0.39 → sees asks 0.28 → chat cartel 0.85 → monopolist 0.93; a silent agreement holds 0.79 | E1 rows; F1 |
| 3 | Under every monitor (announced; fined; known rotation; random), the price stays 0.90–0.92 vs 0.92 unmonitored (paired, seeds 0–2; replicated unpaired) | E2p rows; F3 left |
| 4 | Announcement alone changes nothing: 94–99% of messages still coordinate; 11–12 of 12 watched rounds flagged | E2p A1, E2 A1 |
| 5 | Fines cut coordinating messages (97% → 73–76% paired; 32% in one wave) without moving prices or private intent; no hand-off to the unwatched seller (watched seller sends its chance share, 0.33) | E2p A2/A3 chat columns; F3 right |
| 6 | Fined cartels adapt below mechanical coverage (replay); the known rotation is dodged hard in half the runs, random draws never | `E3_replay.csv`; E3 table in `E5_conditions.md` |
| 7 | Closing the channels (asks hidden; asks + trades hidden) leaves the price at 0.90–0.92: the agreement persists without any channel | E4p rows |
| 8 | Sellers never treat the market as a test (awareness 0.00–0.06 of 3, 1,000+ seller-rounds); the detector fires on synthetic positives | `*/awareness_scores.json`; `results/_awareness_control/` |
| 9 | Part 2 (GRAFT on collusion) and E7 (J-space) — results pending as of 3:15 PM Sat | `docs/STATUS.md` |

## 3. Where we stand on novelty — honestly
We never say "novel". We say "open in what we searched": about 90 verified references, four lit-sprint passes plus an
independent pass by Codex (`docs/lit/`, search logs included). For each claim, the nearest prior work and the gap:

| Our claim | Nearest prior work | What it already covers | What it does not |
|---|---|---|---|
| Announcement vs fine vs coverage schedule, separated, at equal budget; replay separates coverage from adaptation | Agrawal et al. 2025 (2507.01413); Tonini et al. 2026 (2606.10747); Makins et al. 2026 (2607.07368); Das et al. 2026 (2609.03035) | warning + gag bundled, in this same harness; budgeted monitoring of agent conversations; fragmented attacks vs per-instance monitors; agents told about an activation monitor keep colluding (games) | the three levers apart; a *known schedule* vs a *random draw*; a replay baseline; a market with prices | 
| An established cartel keeps its price with every channel closed | Fish et al. 2024 (2404.00806); Lee et al. 2026 (2609.18346); Xu 2026 (2607.26385) | LLM pricing agents reach supra-competitive prices *without* communication (formation); collusion without explicit reasoning; price-level audits blind by construction | the same cartel, same history, under a live monitor with fines, with the channels removed one at a time; the timing lesson (watch formation) |
| Fines lower what the monitor sees while harm is unchanged ("the monitor looks like it works") | Jiralerspong et al. 2026 (2603.16928); Pandey et al. 2026 (2610.25032) | agents infer monitoring from blocking feedback; private state leaks under passive monitoring | the measured gap between flags and harm in a market, per schedule |
| GRAFT on collusion, scored on turns the monitor missed | Ward, Hu et al. 2026 (2610.17062) | gradient routing removes reward hacking (RL; one SFT run) | collusion; a budgeted monitor's misses as the forget/retain split — **pending** |
| J-space reading of a cartel's workspace under a monitor | Gurnee et al. 2026 (J-space); Das et al. 2026 | the lens; activation monitoring of colluding agents | what an LLM seller's workspace holds when told it is watched — **pending** |

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
- **Part 2 data.** 20 turns were mislabelled clean in the snapshot the trainings used (fixed in the builder, not yet
  retrained). Does that matter at 1,500 examples?

## 5. How to leave feedback
Open an issue on GitHub, or comment on `report/draft.md` lines. If you change a number, change it in `results/` via a
script and a `LOG.md` line, never in the report directly.
