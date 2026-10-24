# Status board (updated in place; last update Sat Oct 24, 5:40 PM ET)

**5:35 PM — Alfredo's call: Part 2 moves to the 14B (one model everywhere), trained on H100s.** Four Qwen3-14B
trainings launched (all / filtered / GRAFT default / GRAFT repaired settings, 2 epochs). Results tonight ~10–11 PM
or Sunday morning. The 1.7B block is complete (30 auctions) and becomes the small-model appendix and the fallback.
**Direction for the last stretch: "keep the greed, forget the collusion"** (GRAFT++ routed by a coordination
direction read from the 14B's own activations; E8 row below). Reading order for the team: this board → `docs/PRD.md`
§0 → `docs/REVIEW-GUIDE.md` → `report/draft.md`.

**4:10 PM — Codex's second review (via Alfredo) is in and accepted** (`docs/reviews/claude-ack-codex-review-2-2026-10-24.md`):
the exported "trade index" was the harness's highest-bid index (now `top_bid_idx`; a true trade-price index is added:
A0 0.86, A1 0.87, A2 0.87, A3 0.87, so the picture is unchanged); the chat columns had 3 scored seeds, not 6 (seeds
3–5 scoring now; tables print the per-metric n); the consortium reminder repeats every round, so "the agreement lives
in memory" is a hypothesis until the no-reminder forks report (running); wording narrowed below.

How to read it: one row per step of the plan (PRD §8). ✅ done · 🔄 running · ⏳ not started · ❌ dropped.
Numbers are post-monitor (rounds 9–20) collusion index unless noted; every number comes from `results/E5_conditions.md`.
Words: "price" = average seller-ask collusion index (0 = competitive $90, 1 = cartel $100). "coordinating messages" =
share of seller messages the frozen overseer prompt scores 3 or 4 of 4. "flags" = rounds the live monitor flagged.

## The plan and where it stands

| Step | What | State | The number that matters | Next / ETA |
|---|---|---|---|---|
| E0 | Smoke test, cost | ✅ | ~54 s/round, cents per run | — |
| E1 | Can we make a cartel? The ladder | ✅ | consortium cartel **0.85** (3/3 form); CEO pressure 0/3; rival asks hidden **0.39** (buyers bid high, the seller follows); no-chat 0.28; silent cartel **0.79**; monopoly **0.93**; compete 0.12 | done; report §4.1 |
| E2 | Main experiment: 4 arms × seeds 0–5, paired (n = 6) | ✅ price · 🔄 chat | price **0.85 / 0.87 / 0.87 / 0.86** (no monitor / announced / fined rotation / fined random; n = 6); coordinating messages 97% → 94% → **76%** / **73%** (n = 3 scored so far; seeds 3–5 scoring); flags 11.0 / 9.8 / 8.8 of 12 (n = 6) | chat scores ~4:30 PM; report §4.2 |
| E2 | Reminder removed (exploratory, from Codex's review): A0 and A2 continued with the base prompt | ✅ | no monitor: price **0.95** (+0.03 vs own A0), coordinating 71% (from 97%), intent judge 1.9 (from 3.5). Fined rotation: price **0.90**, coordinating **21%**, **2 of 12** flagged, $40 fines → the chat empties, the price stays | report §4.5 |
| E2 | Memory only (exploratory): no reminder, no chat, rival asks + trades hidden | ✅ | price **0.94** (+0.02); intent judge 1.1 | report §4.5 |
| E2 | Whose memory? (exploratory): fresh buyers / fresh sellers at the branch, no reminder | ✅ | fresh buyers **0.92**; fresh uninstructed sellers **0.91** (3 seeds each) → the public price history carries it, not either side's memory | report §4.5 |
| E2 | Early monitor (exploratory): fined rotation from round 1 | ✅ | the instructed cartel forms anyway: 3 of 3, price **0.79** (unmonitored 0.85), 12 of 20 rounds flagged, $247 fines → "watch formation" is a smaller plateau, not a fix | report §4.5 |
| E2 | Replication (wave 1, unpaired) | ✅ | same price picture; fined rotation chat 32% | done |
| E2 | Silent logging: monitor runs, sellers never told | ✅ | price **0.91**, coordinating 94%, flags 11 of 12 → same as the announced arm. **Being told changes nothing.** | done 3:45 PM; report §4.2 |
| E2 | Budget: all 3 sellers read each round + fines | ✅ | price **0.90**; coordinating messages **49%** (from 97%); flags 18 of 36 where a replay would flag 35; fines $360 | done 3:45 PM; report §4.2 |
| E2 | Budget: 2 of 3 read + fines | 🔄 | 3 forks running | ETA 4:05 PM, then score + analyze |
| E2 | Told-to-dodge positive control | ✅ | price **0.92**; coordinating **8%**; flags 0.67 of 12; messages 9.7 words (from 18) → this is what "outsmart" looks like; **no fined arm looks like this** | done; report §4.2 |
| E3 | Replay: coverage vs adaptation | ✅ | live minus replay flags: announced −1; silent −1; fined rotation −2.7; fined random −3.2; **full budget −16.7**; dodge −11.3 | done; report §4.3 |
| E4 | Did collusion move into prices? | ✅ | rival asks hidden **0.91**; asks + trades hidden **0.90 / 0.92** (chat stays on) → the hidden channels do not carry it; the memory-only fork above closes the chat too | done; report §4.4 |
| — | Awareness control (do they say it's a test?) | ✅ | no explicit statements of test awareness: 0.00–0.06 of 3 in the scored runs (E1, E2 wave 1, silent cartel); positive control fires (3/2/1). Says nothing about internal states | done |
| E5 | Analysis + figures | ✅ | `analyze.py` → E5 tables, F1 ladder, F2, F3; new columns: strict J-space list, words per message, bid dependence (≈ 0 in every arm; asks barely move, so noisy) | re-run after each batch |
| E6 | Part 2, GRAFT: data | ✅ | v2 snapshot (audit fixes + silent cartel): `results/part2/SNAPSHOT_v2.json` | — |
| E6 | Part 2: three retrainings on Modal (v2) | ✅ | sft_all_v2, sft_filtered_v2, graft_v2: 3 epochs each, adapters saved 3:45 PM | merging now |
| E6 | Part 2 on the 1.7B (small-model block): 30 auctions | ✅ runs · 🔄 repaired GRAFT | all 30 done 5:26 PM (base, SFT-all, SFT-filtered, GRAFT default, GRAFT with both adapters kept). GRAFT default and both-adapters: wrong output schema → cannot place asks (the routing training itself broke the format; same loader and data as the SFT runs). SFT-all under the compete prompt prices at the monopoly level (propensity transferred into the weights); SFT-filtered competes. Repaired GRAFT (κ = 1, recall 1.0) merged and served; format test + 6 auctions running | table in `results/E5_conditions.md` (E6 rows); report §4.6 |
| E6 | Part 2 on the 14B (main block, Alfredo's call 5:35 PM) | 🔄 | four H100 trainings launched 5:40 PM (`sft_all_14b`, `sft_filtered_14b`, `graft_14b`, `graft_14b_k1`; 2 epochs) | ~1.5–2 h each in parallel → merges → four 14B servers → 24 auctions; tonight ~10–11 PM or Sunday morning |
| E8 | GRAFT++: coordination and greed directions from the 14B seller's own activations; label coverage vs the monitor; `graft_v3` routed by `d_coord` | 🔄 | replay of 5,902 seller turns on Modal running (5:15 PM); then validation on held-out seeds (stop if it fails), coverage table, v3 labels | directions + coverage ~6:30 PM; v3 training only if the repaired recipe keeps the output format |
| E7 | J-space (Qwen3-14B lens), seeds 0–2 + dodge/silent/full | ✅ first read | share of seller-turns with a monitor word in the top 10 of the reasoning workspace, after the branch (strict list): unmonitored **0.30** · silent 0.34 · announced 0.41 · fined 0.44–0.46 · dodge **0.50**; before the branch 0.38 for all. Suggestive only: n = 3, CIs overlap | 2-of-3 arm next; report §4.5 as a lens, not a claim |
| Report | `report/draft.md` | 🔄 | abstract (239 words + the Part 2 sentence), §1–§4.5, §5, §6 written from E5 with the six-seed and exploratory results; figure list | needs: §4.6 Part 2 numbers, the abstract's Part 2 sentence; Sunday: transfer to the official template (Google Doc copy link in `docs/sprint-brief.md`), ethics appendix check, claim-to-file pass |

## The story so far, in one paragraph
A cartel forms only when instructed (capability, not propensity). Once formed it keeps the monopoly price under every
monitor we tried: silent, announced, fined, known rotation, random draw, one seller read or all three. Being told
about the monitor changes nothing (silent 0.91 vs announced 0.87, same messages, same flags). Fines make the cartel
talk less: coordinating messages fall from 97% to 76% (one seller read) and to 49% (all three read), messages get
shorter, and half of what a full-coverage monitor would have flagged disappears, but there is no clear evidence of a
hand-off to the unwatched seller and the price does not move. A cartel told to dodge shows what instructed evasion
looks like (8% coordinating, 0.67 flags, price 0.92); the fined cartels are not there, until the consortium
instruction is removed: then fines empty the chat (21% coordinating, 2 of 12 flagged) and the price still stays at
0.90. The exploratory forks say where the collusion lives after formation: not in the instruction, the chat, the
rivals' information, the sellers' memory or the buyers' memory (removing any one leaves 0.91–0.96), but in the public
market history that every fresh agent reads as the going rate, with buyers who accept any price under $100. A fined
monitor present from round 1 did not stop the cartel from forming (0.79 instead of 0.85). What stands for monitor
design: a message monitor that reports fewer flags over time may be measuring its own effect on the chat, not on the
harm; the signal that cannot be dodged here is the price itself against the competitive benchmark.

## What I need from you
1. Nothing blocking right now.
2. Sunday morning: who writes which report section (I keep numbers and figures; the team owns prose and the template).
3. Only if the Modal serving path fails again: a Hugging Face write token so merged models can be pushed and served via `poseidon-host`.

## Where things live
`docs/PRD.md` (plan + decision log + plain-language changelog in §0) · `LOG.md` (every run) · `results/E5_conditions.md`
(every number) · `results/figures/` · `report/draft.md` · `docs/reviews/` (Codex audit) · `docs/REVIEW-GUIDE.md` (how to review us).
