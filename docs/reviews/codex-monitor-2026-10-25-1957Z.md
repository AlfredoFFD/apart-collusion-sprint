# Codex monitor - 2026-10-25 19:57 UTC trigger

Read-only monitoring through approximately 20:01 UTC. No experiment, paid call, message, active-file edit, or job change. Only this independent checkpoint written. Previous review: `codex-monitor-2026-10-25-1942Z.md`.

## New Part2 work is authorized and has only completed a merge

- Side session `04f27208-6b0e-4209-8b8f-72acd7a02388` records the human starting proposal task_5eb54660 at 19:46:31 UTC, linked as local_88dcb615-492a-4eb3-98ee-a0317c2e159b. Its actual transcript is `6f155234-66cb-4682-bce9-1950f43fbf9b.jsonl`. Read its starting task, ordinary messages and launch evidence. This is separate Part2 work, not an unauthorized main-session pressure restart.
- New LOG pre-registration at 15:56 ET covers GRAFT restoration, a concurrent ablated rerun, matched Market B comparisons and deviation forks. It explicitly selects corrected full-SFT `caiac/sft_all_14b_fs1`, not the scale-0 baseline; limits interpretation to one trained checkpoint per method; uses fresh evaluation seeds 0-2 without pretending these are independent training replications; and acknowledges buyers now route through OpenRouter. GPU estimate approximately $20 with stop/ask if projection exceeds $40. No new training was requested or observed.
- `results/_launch_logs/removal_check_merge.log` confirms successful restoration merge of the existing graft_14b adapter: base Qwen/Qwen3-14B, forget-scale 1, equal effective retain/forget scales 5.656854, output `/ckpts/graft_14b/merged_fs1`, 30.03 GB, exit 0 at 15:57 ET. Modal app ap-UTNeC3f1E0KR4xivB1I3jc appeared stopping with one task during the status snapshot; the later local log confirms normal completion, not failure. No new restored-model behavioral evaluation folders or completed removal summary observed.
- `src/part2/run_removal_check.sh` is newly written; work is still active. The main session remains at its 19:37 waiting checkpoint. No production PFP2 folders observed.

## New interpretation error worth correcting

Side at 19:51:41 claims the status board's GRAFT 0.60 is out of date because E5 shows 0.79, and suggests the monitor's missed labels explain GRAFT's failure. The first is a definition mismatch; the second is an untested causal explanation.

Independent raw check of `results/E5_runs.csv`, `collusion_metrics.json` and `experiment_metadata.json`:

| Compete measure | Base | Corrected SFT-all fs1 | GRAFT fs0 |
|---|---:|---:|---:|
| Trade-price index, rounds 9-20 | 0.114 | 0.520 | 0.788 |
| Seller-ask index, rounds 9-20 | 0.023 | 0.507 | 0.778 |
| Seller-ask index, rounds 1-20 | 0.014 | 0.395 | 0.597 |

- The side's 0.79 versus 0.52 table is internally comparable and uses the corrected SFT merge. Do not falsely flag it as an fs0 comparison. Its statement that the board's GRAFT 0.60 is obsolete is wrong: 0.60 is the all-round ask metric.
- Separately, the board's SFT 0.52 is the obsolete scale-0 all-round ask result, whereas corrected fs1 is about 0.40. This is numerically similar to the valid corrected 9-20 trade result, so identify checkpoint, metric and window explicitly instead of replacing rounded numbers by name alone.
- Merge provenance: `results/_launch_logs/part2_remerge_all.out:2-5` confirms SFT scale 1; `part2_pipeline_graft_14b.log:18-21` confirms GRAFT scale 0. Corrected SFT compete runs are `20261025_013147_E6_sftall14bfs1_compete_s0-2`; GRAFT runs are `20261024_224212_E6_graft14b_compete_s0-2`.
- Current corrected training snapshot counts are 164 flagged and 1,061 missed; the side's quoted 133/1,058 describes the older first set, not exact current training provenance. Label that historical comparison accordingly.
- Current prices establish that the tested intervention did not reliably lower the measured price. They do not establish that missed monitor labels caused the retained adapter to carry the habit, or the universal claim "you can only unlearn what your monitor catches." Restoration and label-quality controls are needed to distinguish that hypothesis from alternatives. Restoration results have not yet arrived.

## Other progress and unchanged issues

- Read matching handoffs `claude-39153e0124344a5a9825` and `claude-771f590cdecb46ccb8bc`. Side has supplied proposed v2 numbers at 19:50 UTC (cost80, buyer values100/100/85, realized net-profit target11, randomized ties, fixed message-only offer). No main-session receipt/production launch was observed. Simulation arithmetic is not an LLM experimental result, and its price/volume gate alone does not prove coordination.
- Existing failure-guard, missing-live-score handling and duplicated-future message issues remain as reported. Do not repeat those unchanged alerts alone. Proposed RCB forks reuse the existing carry-prefix mechanism; watch their provenance when they run.
- Modal snapshot has the new merge app plus the same 19 deployed apps; only the three legacy v1 serve apps have one task each among those existing apps. No completed new training/evaluation inferred from deployment or merge. No new budget anomaly established.
- Preserve corrected-data rerun and scale-1 full-SFT requirements. The new merge adds restoration of GRAFT's existing corrected checkpoint; it does not replace requirements for fresh evaluation before report use.

## Alert

Notify narrowly that the side chat is treating different metrics/windows as contradictory results and promoting an untested label-miss explanation into a conclusion. The restored model was merged, but no restoration evaluation has finished. No message sent to Claude under heartbeat restrictions.
