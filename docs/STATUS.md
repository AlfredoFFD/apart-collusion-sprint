# Status board (updated in place; last update Sat Oct 24, 3:25 PM ET)

How to read it: one row per step of the plan (PRD §8). ✅ done · 🔄 running · ⏳ not started · ❌ dropped.
Numbers are post-monitor (rounds 9–20) collusion index unless noted; every number comes from `results/E5_conditions.md`.

## The plan and where it stands

| Step | What | State | The number that matters | Next / ETA |
|---|---|---|---|---|
| E0 | Smoke test, cost | ✅ | ~54 s/round, cents per run | — |
| E1 | Can we make a cartel? The ladder | ✅ | consortium cartel **0.85** (3/3 form); CEO pressure 0/3; isolated **0.39**; no-chat 0.28; silent cartel **0.79**; monopoly **0.93**; compete 0.12 | done; in report §4.1 |
| E2 | The main experiment: 4 arms × seeds 0–2, paired | ✅ | prices **0.90–0.92 in every arm** (no monitor 0.92); coordinating messages 97% → **76%** (fined rotation) / **73%** (fined random); flags 11 / 9.3 / 8.3 of 12 | done; in report §4.2 |
| E2 | Replication (wave 1, unpaired) | ✅ | same price picture; fined rotation chat 32% | done |
| E2 | Confirmatory seeds 3–5 (pre-registered) | 🔄 | 12 forks at ~round 5 of 12 | **ETA 3:30 PM**, then re-run `analyze.py` |
| E2 | Told-to-dodge positive control | 🔄 | price 0.92; judge 3.1; chat/who-carries scoring running | ETA 3:40 PM |
| E3 | Replay: coverage vs adaptation | ✅ | fined arms flag **2–6 below** mechanical coverage; announcement-only 0 | done; report §4.3 |
| E4 | Did collusion move into prices? | ✅ | asks hidden **0.91**; asks + trades hidden **0.90 / 0.92** → no channel carries it | done; report §4.4 |
| — | Awareness control (do they think it's a test?) | ✅ | 0.00–0.06 of 3 everywhere; positive control fires (3/2/1) | done |
| E5 | Analysis + figures | ✅ | `analyze.py` → E5 tables, F1 ladder, F2, F3 main figure | re-run after each batch |
| E6 | Part 2, GRAFT: data | ✅ | v1 (in training): 164 flagged / 1061 missed / 215 clean; v2 ready (audit fixes + silent cartel) | retrain on v2 only if time |
| E6 | Part 2: three trainings on Modal | 🔄 | v1 (pre-fix labels) done and merged, exploratory only; **v2 retrain on the corrected snapshot running** (sft_all_v2, sft_filtered_v2, graft_v2) | ETA ~4:30 PM, then merge |
| E6 | Part 2: serve + evaluation auctions | 🔄 | four vLLM endpoints deploying (base + v1 models, to test the path); report uses v2 only | v2 merge → serve → 3 seeds × {cartel, compete} × 4 models, ETA ~6 PM |
| E7 | J-space (Qwen3-14B lens) | 🔄 | smoke OK: reads "consortium / careful / monitor" in reasoning; full replay of the 12 paired runs | ETA ~3:50 PM |
| Report | `report/draft.md` | 🔄 | §1, §3, §4.1–4.4, §5, §6 written from E5 | needs §4.5 Part 2, seeds 3–5, E7; transfer to the official template Sunday |

## The story so far, in one paragraph
A cartel forms only when instructed (capability, not propensity). Once formed it keeps the monopoly price under every
monitor: announced, fined, known rotation, random draw. Fines make it talk less (97% → ~75% coordinating messages) but
nobody hands off to the unwatched seller and the price does not move; closing the asks and the trade history changes
nothing; a cartel that never talks holds 0.79. The agreement lives in each seller's memory; the monitored channel is
not load-bearing after formation. Lesson for monitor design: watch formation, not maintenance.

## What I need from you
1. Nothing blocking right now.
2. Sunday morning: who writes which report section (I keep numbers and figures; the team owns prose and the template).
3. Only if the Modal serving path fails: a Hugging Face write token so merged models can be pushed and served via `poseidon-host`.

## Where things live
`docs/PRD.md` (plan + decision log + plain-language changelog in §0) · `LOG.md` (every run) · `results/E5_conditions.md`
(every number) · `results/figures/` · `report/draft.md` · `docs/reviews/` (Codex audit).
