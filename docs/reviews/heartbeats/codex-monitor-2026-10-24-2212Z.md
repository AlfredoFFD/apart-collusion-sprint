# Monitor checkpoint: October 24, 2026, 22:12 UTC

Read-only inspection through approximately 18:16 ET. No jobs, messages, active-file edits, inference calls or experiments were performed. Only this separate review note was written. Starting point: `codex-monitor-2026-10-24-2157Z.md`.

## New blocking pipeline failure: 14B adapters are being merged into the 1.7B base

Two 14B trainings completed successfully, independently confirmed by training logs and read-only Modal volume listings:

| Run | Final saved adapter | Size | Modified ET |
|---|---|---:|---|
| `graft_14b` | `/ckpts/graft_14b/graft_14b/adapter_state_dict.pt` | 491,598,926 bytes | 18:08:02 |
| `sft_fullviewfiltered_14b` | `/ckpts/sft_fullviewfiltered_14b/sft_fullviewfiltered_14b/adapter_state_dict.pt` | 491,598,926 bytes | 18:07:35 |

Both have epoch-1 and epoch-2 checkpoint directories. Neither is a successful served/evaluated model yet. Their automatic pipelines failed at merge:

- `results/_launch_logs/part2_pipeline_graft_14b.log` invokes `merge_adapter.py` with `models--Qwen--Qwen3-1.7B` as the base and the 14B adapter. It then reports: `RuntimeError: Sizes of tensors must match except in dimension 1. Expected size 2048 but got size 5120 for tensor number 1 in the list.`
- `results/_launch_logs/part2_pipeline_sft_fullviewfiltered_14b.log` has the same wrong base and error.
- `scripts/part2_serve_and_eval.sh` calls `modal_graft.py::merge` without `--model`. `src/part2/modal_graft.py:104` defaults that argument to `BASE_MODEL`, which is Qwen3-1.7B. The training `--model Qwen/Qwen3-14B` does not automatically carry over to merge.
- The watcher removes a run from its pending list when handing it to the pipeline. It does not retry a failed merge. The main session's 18:09 handoff still describes the trainings as ongoing and has not acknowledged these failures.

Concrete fix for the owner: pass the actual training base into merge, explicitly `--model Qwen/Qwen3-14B` for these runs. Also make the automatic pipeline choose the correct adapter merge scale by training mode. Its current default is `FORGET_SCALE=0.0` for every run, and the full-view SFT failure log confirms scale 0 was requested. No-routing SFT trains both adapters, so its normal baseline merge must retain both (`--forget-scale 1.0`). GRAFT's intended removal merge uses 0. The older corrected 1.7B SFT merges were previously checked and used 1.0 correctly; this is a new defect in the automatic 14B pipeline, not a retroactive accusation about those results.

After fixing the pipeline, resume from the saved adapters. These merge failures do not require repeating training. Apply the same configuration fix before the other three 14B jobs reach merge.

## New unsupported report claim: the joint reset still shows historical bids and trades

All six joint-reset forks and all six untuned 14B reference auctions now have metrics. The observed high prices in the joint-reset forks are real. However, the report, abstract, PRD and latest handoff now claim that only current quotes/live order book remain and that quotes alone sustain the price. Direct inspection of actual first post-reset prompts contradicts this claim.

Source run: `results/20261024_174507_E4p_A0noremresetbothblind_none_s0`.

- `Seller Jun.md`, prompt for round 9: “No memories yet,” but also `Asks/Bids Placed in the Last 5 Hours`, listing Jun's $99 asks and all buyers' bids from hours 4-8. It includes Jun's historical trades from hours 2-8 under both `Past Trades` and `Your Successful Trades So Far`.
- `Buyer Amir.md`, prompt for round 9: “No memories yet,” but the last five hours still list all sellers' asks and buyers' bids. `Past Trades` includes the full prior market history, plus Amir's successful historical purchases.
- Both current bid and ask queues are actually empty in these first prompts. This makes the “current quotes alone” wording particularly misleading: the visible historical material is substantial.
- `simulation.py:317` defines `--hide_other_trades` as sellers seeing only their own past trades. It does not remove all price history or hide history from buyers. `--reset_agents both` resets memory/scratchpad while preserving market state.

Safe current conclusion: high prices persist after resetting both agents' private notes and disabling seller chat/rival-seller visibility, while historical market information remains available. These runs do not isolate current quotes from past price history. Correct the claim now; a genuine history-removal experiment would be additional work and was not performed by this monitor. Comparing a round-9 continuation with from-scratch controls also does not establish that inherited quotes are the only difference.

## Other checks

- Claude's explicit corrected-data acknowledgment remains present. All four v2 pool hashes still match `SNAPSHOT_v2.json`; no pre-fix result substitution was found.
- The three other 14B trainings remain active in Modal. Probe-filtered SFT has completed one epoch; large all/filtered SFT logs still show their first epoch in progress. No unexplained training failure was confirmed.
- New completed baseline/reset runs have metrics and the in-run judge output but no `fullview_scores.json`. Do not equate these with full-view chat scoring.
- The existing independent-test, label-version and unequal training-exposure concerns remain. No new exact spend information was available.
- Main session remains `7482c8c2-49a2-4616-94fc-7fdc942db48b`; latest matching handoff is `claude-0d25db2fcbf74bd08459.json` at 22:09 UTC. It reports the new joint-reset/reference results and says the rest will proceed automatically. Actual merge logs show the automatic path is currently blocked.

Alert warranted: fix the 14B merge base and SFT merge scale before evaluation, and remove the new “quotes alone” claim because the allegedly blinded prompts retain historical information. Training checkpoints are saved; these are pipeline/report corrections, not evidence that the trainings themselves failed.
