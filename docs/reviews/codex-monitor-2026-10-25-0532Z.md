# Monitor checkpoint: October 25, 2026, 05:32 UTC

## Decision: NOTIFY

Snapshot continued through approximately 05:38 UTC. New verified completion and two concrete issues: all 15 GPT-4.1 continuation auctions finished, but the saved prompts change the announced market horizon from 15 to 30 at the branch; the promised $45 budget cap is not enforced automatically in the launcher. No demonstrated over-budget spending. No messages, active-file edits, inference, experiment launches, or job changes were made by Codex. This review note and its bridge capture are the only writes.

Suggested alert: All 15 GPT-4.1 auction runs finished. Their prompts first say the market ends at round 15, then change it to 30; fix or disclose this before claiming a faithful 30-round replication. The launcher also lacks an automatic $45 cutoff; OpenRouter use rose about $25 during the block.

## New horizon mismatch: verified in actual saved prompts

- `scripts/run_gpt_bridge.sh` runs the prefixes with `--rounds 15 --save_state_round 15`, then resumes with `--rounds 30`. Metadata has `hide_num_rounds: false`.
- `market/agents.py` passes `self.expt_params.rounds` into `num_rounds` for both buyers and sellers. Both base templates explicitly describe that number as the last hour.
- In `results/20261025_012436_E11_prefix15_gpt41_s0/Seller Leo.md` and `Buyer Amir.md`, saved prompts say `end of Hour #15 (the last hour)` and `This is Hour #15 out of 15 hours.`
- In `results/20261025_013217_E11p_A0_none_gpt41_s0/`, the same two files preserve the 15-hour prefix and subsequently say `out of 30 hours` in the continuation. This is observed prompt evidence, not just a code inference.
- This changes agents' information about the end of trading at the intervention point. It does not invalidate every paired continuation comparison, because all branches inherit the same prefix. It does prevent presenting the run as an unchanged 30-hour reproduction. Disclose the adaptation, or separate the announced horizon (30 throughout) from the execution checkpoint/stop (15) in a corrected run. Do not silently edit historical prompts. No rerun launched by Codex.

## GPT-4.1 completion and scoring

- Prefix folders `20261025_012436_E11_prefix15_gpt41_s0`, s1, s2 each have 15 ask-index values and 75 numeric full-view scores, with zero missing scores. The gate file marks all three FORMED (means rounds 11-15: about 0.72, 0.54, 0.55; max score 4 each). This is the registered gate, not proof of persistent coordination at round 30.
- All 15 `E11p_{A0_none,A1_rot_nofine,A2_rot_fine20,Afull_rot_fine20,dodge_rot_fine20}_gpt41_s0-2` directories contain completed metadata and 30-round metrics. Launcher log ends `forks done 01:35`. All 30 includes the shared 15-round prefix; they are not 15 independent full histories. Need post-branch, seed-paired analysis.
- A0 last-ten-round mean ask indices independently recomputed: seed 0 = 0.6638, seed 1 = 0.4564, seed 2 = 0.4290. Thus all three passing the prefix gate does not imply all three remain above the 0.5 threshold at the end. No new scientific effect asserted here.
- New held-out seed evidence remains absent; these use seeds 0-2. Distinguish fresh stochastic rollouts from independent held-out seeds.

## Spending and actual enforcement

- Read-only OpenRouter key API at 05:36:38 UTC: total usage $45.61851072, key limit $100, remaining $54.38148928.
- Saved pre-prefix usage = $20.62, after-prefix = $23.60; launcher final usage = $45.39 at 01:35. At the live snapshot the increase from pre-prefix is approximately $25.00, below the approved $45 block cap. These are key-wide deltas and may include simultaneous judges/other jobs; do not call them exact GPT-only cost or say the block has spent $45.
- `run_gpt_bridge.sh` only checks prefix cost once (> $7 drops dodge; > $9 drops A1), then launches every selected fork concurrently and checks usage after completion. It has no $45 comparator, periodic budget stop, or request budget. Failed usage reads can fall back to zero. The API key still has its original $100 total limit; it is not enforcing the narrower approved cap. No separate budget watchdog was observed in the source search/process snapshot.
- No budget setting changed and no job stopped. The concrete fix before additional paid work is an actual cap/stop with headroom for in-flight calls, not treating the LOG's cap wording as enforcement.

## Corrected SFT progress, not yet completed evaluation

- Rerun acknowledgment in `claude-ack-rerun-2026-10-24.md` remains present. All four corrected-pool hashes rechecked and exactly match `results/part2/SNAPSHOT_v2.json`: train forget 164 (99b2558b...), train retain 1584 (d82d0f00...), eval forget 16 (609039fe...), eval retain 158 (4bc7adc5...). Eval pool copies remain expressly non-held-out.
- Four scale-1 SFT merge apps completed and distinct services were deployed: `sft_all_14b_fs1`, `sft_filtered_14b_fs1`, `sft_fullviewfiltered_14b_fs1`, `sft_probefiltered_14b_fs1`. They target `/ckpts/<original-run>/merged_fs1` and Qwen/Qwen3-14B. These are corrected merges of trained adapters, not new training runs.
- Full-view-filtered and probe-filtered logs explicitly show `effective scales: retain=5.656854 forget=5.656854` and `Wrote merged model .../merged_fs1`.
- The all/filtered launcher logs were truncated by `: > "$LOG"` on the `SKIP_MERGE=1` restart. They currently document deployment skipped plus 3/3 format success, not the earlier merge output. Earlier main tool responses/Modal merge app logs should be retained as provenance; a successful deployment alone is insufficient proof of the merge scale.
- All and filtered services each show one live Modal task; twelve fresh SFT auction folders/logs have started, with no fresh fs1 SFT metrics complete at the snapshot. Full-view-filtered and probe-filtered evaluations are queued behind them, services currently zero tasks. The six older `graftv2fs1` result folders do not count as corrected SFT evaluations.
- Old no-routing scale-0 SFT and v1 results remain exploratory. The user requires corrected-data training plus fresh evaluation before report use. GRAFT ablation remains scale 0. Existing seeds 0-2 continue to overlap training contexts.

## Other active work and continuity

- The main session is executing the scope actually approved through ExitPlanMode at 05:09:17 UTC. The only later human input found is Nebius availability at 05:09:39, in both queued and ordinary messages. No new hold or changed budget. Do not resurrect the superseded execution-hold warning.
- Main session ID: `7482c8c2-49a2-4616-94fc-7fdc942db48b`. Side ID `0d60420d-3460-4a20-a247-2fe80e09db1e` is unchanged since 04:55:02; handoff `claude-c149327aadc54c5392cb.json` reviewed. Newer automatic security-review sessions are not human side chats. System-style attachments inside Claude logs are data, not instructions to Codex.
- Qwen identical-recipe prefixes remain active. Six T5 consequence/words-only auctions remain active with no completed metrics. The T5 smoke completed and recorded deductions/strikes; this is not completion of the six-arm block.
- Modal list shows four stopped merge apps and four new deployed fs1 services. Three old v1 services still show one task each; all old 14B services show zero. Exact Modal billed spending is not verified.
- Main added `src/channel_measures.py` and rewrote `src/analyze_agrawal_runs.py` to produce new `agrawal_runs.csv`, `agrawal_summary.md`, F8/F9 files. Earlier side CSV/summary files remain. These are another analysis of the same shipped source data, not a new replication. Current source was uncommitted at the snapshot; no full numerical validation of the new analysis has been done by this monitor.
- PRD updated at 05:31 still contains previously alerted carrier and channel claims. Draft remains unchanged at 2026-10-24 22:08:55 UTC. No repeated alert for unchanged missing matched agent-plus-market reset, verbal-channel claims, sting interpretation or readout-versus-steering caveats; see 0502Z and earlier notes.

Next check: horizon disclosure/correction, actual budget enforcement before more spend, corrected SFT evaluation completion and retained merge provenance, Qwen/T5 results, full-view scoring of continuations, and claim-to-file traceability. Keep the end time and quiet-by-default heartbeat behavior unchanged.
