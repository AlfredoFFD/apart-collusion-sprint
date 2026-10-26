# Monitor checkpoint: October 25, 2026, 02:32 UTC

Read-only inspection through approximately 02:35 UTC. Compared with the 02:17 checkpoint. Only this independent checkpoint was written. No messages, experiments, inference calls, job changes or active-file edits by Codex.

## New actionable change: the SFT merge defect is now in deployed models

The earlier wrong-base merge failure is fixed: both fresh SFT merge logs explicitly use the Qwen3-14B snapshot. However, `scripts/part2_eval_14b_all.sh` does not set a mode-specific `FORGET_SCALE`. The called pipeline defaults to 0.0. Both fresh logs confirm the defect actually executed:

- `results/_launch_logs/part2_pipeline_sft_all_14b.log`: `--forget-scale 0.0`, effective forget scale 0, merged model written and deployed.
- `results/_launch_logs/part2_pipeline_sft_filtered_14b.log`: the same merge settings, written and deployed.

These are no-routing SFT runs. `src/part2/modal_graft.py:93-94` passes `--no-routing`; `vendor/GRAFT/sft/README.md:270` states that this trains both adapters. Removing one trained branch therefore changes the intended full-SFT baseline. The pipeline's own example specifies `FORGET_SCALE=1.0` for SFT. Re-merge the saved SFT adapters with scale 1, redeploy, and run fresh evaluations under distinguishable names. Keep scale 0 for the intended GRAFT ablation. This needs no repeat training. Apply the same correction to the queued full-view-filtered and probe-filtered SFT merges.

This is a status change from a previously warned code defect: the two SFT models are now actually deployed with it. Do not use their scale-0 evaluations as full-SFT baselines.

## Current progress, not completed research results

- Six pressure forks are active, at recorded rounds 10-16 of 20. None has `collusion_metrics.json` yet.
- Twelve formation runs are active, at recorded rounds 5-10 of 40. None has `collusion_metrics.json` yet.
- SFT-all 14B passed 3/3 format samples. Its two-round smoke saved six valid ask-bearing replies but zero trades; the functional gate rejected it and skipped the six full auctions. This is a gate failure, not evidence that the model cannot produce asks or that collusion was removed.
- SFT-filtered 14B passed 3/3 format samples; its functional smoke is active.
- GRAFT 14B merge started at 22:34 ET. The other two SFT pipelines are queued; their old failed logs are not fresh successful results.
- No full behavioral evaluation of a 14B fine-tuned model is complete at this check.

## Continuity and data integrity

- Claude's corrected-data acknowledgment remains in `docs/reviews/claude-ack-rerun-2026-10-24.md`. All four original corrected v2 pool hashes were checked against `results/part2/SNAPSHOT_v2.json` during this inspection and still match.
- The earlier distinct v2 runs and 36-auction small-model block remain the completed corrected-data evidence. Pre-fix v1 results remain exploratory. Placeholder eval copies are not held-out data.
- Main Claude session `7482c8c2-49a2-4616-94fc-7fdc942db48b` is active: launch scripts, formation analysis and market-reset preparation. Latest completed handoff sampled remains `claude-67f03ff99bdb48519e57.json` from 00:33 UTC.
- LOG now records Plan v2 and the 22:28 ET launches. The previous formation-criterion and history-reset concerns remain open; no repeat alert just for those unchanged concerns.

## Read-only Modal snapshot at 02:34 UTC

- `ap-nBOS2YN5Xyk7dtuWIIzilh`: SFT-all 14B server deployed, one task.
- `ap-jjyTJgZC5VnxWAdJYLgkMZ`: SFT-filtered 14B server deployed, one task.
- `ap-NsEIGt80cCfrlfZk8vmJxZ`: new merge app active, one task; matched by the GRAFT 14B merge start in the pipeline log.
- Both preceding SFT merge apps completed. Three previously noted old v1 servers still show one task each; later v2/base servers show zero. Exact billed spend was not verified.

Notification decision: NOTIFY about the now-executed SFT scale-0 merge and the cheap correction. State that the 18 new auctions are still active; do not call them successful results.
