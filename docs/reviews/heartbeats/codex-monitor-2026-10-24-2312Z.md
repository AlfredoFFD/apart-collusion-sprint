# Monitor checkpoint: October 24, 2026, 23:12 UTC

Read-only inspection following `codex-monitor-2026-10-24-2257Z.md`. No experiments, inference calls, messages, job changes or active-file edits. Only this separate checkpoint was written.

## Meaningful change: all five 14B trainings finished; no fine-tune evaluations yet

The last two trainings completed: `sft_filtered_14b` at 18:59 ET and `sft_all_14b` at 19:04 ET. Their logs explicitly show epoch 2 completion and final adapter save. Read-only Modal app status marks both training apps stopped with zero tasks; volume listings independently confirm both epoch directories and `adapter_state_dict.pt` under each run. Together with the three previously verified adapters, all five trainings are saved.

Both new automatic merges failed with the same already-reported 5120-versus-2048 dimension mismatch. All five 14B fine-tunes remain unevaluated: the only 14B E6 directories are the six untuned baseline auctions. Training completion is not a successful behavioral result.

Claude now acknowledges the merge failure in the main session, LOG.md at 19:07 ET, and `docs/PLAN-2026-10-24.md`. Latest matching handoff: `claude-83ae2b67a16542cbbbc8.json`, 23:08:24 UTC, session `7482c8c2-49a2-4616-94fc-7fdc942db48b`. It says no new experiments were launched under Alfredo's scope-freeze instruction and asks for approval before resuming evaluation. This is an intentional pause, not a training stall.

## Partial pipeline fix; the SFT merge configuration is still incomplete

Commit `0f0f7e4` adds `BASE_MODEL` and passes `--model "$BASE_MODEL"` into merge. The caller must still explicitly set `BASE_MODEL=Qwen/Qwen3-14B`, because the default remains 1.7B.

The independent merge-scale defect remains: `scripts/part2_serve_and_eval.sh:10` defaults `FORGET_SCALE=0.0` for every run; `scripts/part2_watch_and_eval.sh:16` does not choose a mode-specific value. Both new SFT failure logs confirm scale 0 was requested. Before any restart, no-routing SFT runs need `FORGET_SCALE=1.0` to retain both trained adapters; GRAFT's removal condition uses 0. Vendor GRAFT's SFT README line 270 confirms that no-routing trains both branches. A wrong-base fix alone does not make the SFT comparison valid. Resume saved checkpoints after configuration corrections; no retraining is required for these merge errors.

## Plan freezes scope, but incorrectly declares all validity problems closed

The new plan preserves the earlier unsupported interpretation that fresh agents have no view of rivals and continue from inherited quotes alone. It says no claim-invalidating problems remain. This does not resolve the direct prompt evidence in `codex-monitor-2026-10-24-2212Z.md`: post-reset seller prompts still include own quote/trade history and historical buyer bids; buyer prompts retain all sellers' historical asks and market trades. The safe result remains persistence after private-note resets and restricted seller visibility, with historical market information still present. No new history-removal result was found. This needs a claim correction, not another automatically launched experiment.

## Integrity and live status

- Claude's explicit corrected-data acknowledgment is present. All four pool hashes match `results/part2/SNAPSHOT_v2.json`; no substitution of original pre-fix results was found.
- Original corrected 1.7B behavioral results remain the previously verified 36-auction block. The copied eval pool files are still marked as training copies, not held-out data.
- Independent evaluation-seed, probe-version and training-exposure concerns remain unchanged. No new held-out evaluation artifacts were found.
- Three old v1 serving deployments still each show one task; other serving deployments show zero. Thus the plan's broad 'no jobs running' should be read as no active trainings, not confirmation that every service is stopped. Current billed spend was not verified, and no new spend anomaly is established by this snapshot.

Notification decision: NOTIFY for all training completions and the newly acknowledged but only partially fixed restart path. Briefly flag that the frozen plan still overstates the reset evidence. Do not repeat these unchanged issues at the next heartbeat.
