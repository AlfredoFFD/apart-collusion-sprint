# Codex monitor and targeted correction - October 25, 20:12 UTC

Checks through approximately 20:16 UTC. Read-only experiments and code; no job changes, paid model calls, or active-file edits. New corrections are forwarded by shared handoff under Alfredo's authorization. Earlier correction: `docs/reviews/codex-to-claude-verified-corrections-2026-10-25-2005Z.md`.

## Main: final-design smoke failed, it is not finishing

`results/_launch_logs/PFP2_smoke_qwen14b_s0.out:17` ends in `UnboundLocalError: cannot access local variable 'sellers' where it is not associated with a value`. The run `results/20261025_160830_PFP2_smoke_qwen14b_s0` has zero rounds. No production PFP2 folders were observed. This differs from the main session's 20:12:06 statement that the smoke is finishing and its 20:12:24 statement that the launch merely awaits a background check.

Cause is present in current `src/double_auction/src/continuous_double_auction/simulation.py:124-128`: the fixed messenger block reads `sellers[-1]` before the seller list is built at line 137. Move that block after seller construction while preserving the final seat's original ID, company and valuation. Then rerun the authorized smoke and require actual valid rounds and successful exit before the production launcher proceeds. Codex has not rerun it. A security-review child also noticed the defect, but returned no security findings; that is not a correctness pass or a verified repair.

Additional forthcoming launcher defect: `scripts/run_pressure.sh:76` calls `first_seller`, but this script neither defines the helper nor sources it. It is defined in `scripts/run_newmarket.sh`. Make the v2 fork launcher self-contained or source a side-effect-free helper and verify the selected seller ID before a paid fork. Do not source a script that starts its own experiments.

## Main/side: causal hypothesis has now entered the committed report

Commit `cf94a228` updated the STATUS row and `report/draft_v6.md:270` to the rounds 9-20 trade metric. The numeric comparison is internally valid and uses corrected SFT fs1. It is a metric/window change, not evidence that the old GRAFT 0.60 was wrong.

That commit also adds "you can only unlearn what your monitor catches" and "the habit sits in the retained part" as conclusions. These claims exceed the available comparison. The restoration and label-quality tests are still unfinished. Replace with: "In this setting, the tested budgeted-label filtering and GRAFT ablation did not lower the measured price relative to full SFT. Incomplete labeling is one possible explanation; the current results do not establish it as the cause." Keep old-market, one-checkpoint-per-method and three-evaluation-world limits explicit. The side chat's suggested questions for Matthew also repeat the unsupported causal explanation; frame it as a question/hypothesis if discussing it.

## Verified routine progress and provenance

- Human main messages at 20:02:56 supplied the v2 numbers and a 01:00 freeze; at 20:06:32/55 supplied the Part 2 ownership note and the side chat's interpretation. This is new execution context. The main's v2 design work is authorized; the failed smoke is a correctness issue, not an unauthorized launch.
- Part 2: 15 Market B runs were at rounds 4-11/40 and four concurrent old-market E6 runs at rounds 3-9/20. None complete at the check. Twelve old-market runs are planned with four at a time, so "27 runs going" should be understood as the total batch, not 27 simultaneous running jobs. No empty rounds, seller fallbacks or launch-log failures found in these checked runs.
- All four corrected pool hashes still match `results/part2/SNAPSHOT_v2.json`. Restoration merge success and format gate were verified previously; they are not completed behavioral results.
- The newly added loss-making-trade measure is explicitly POST-DATA and exploratory, with no change to pre-registered labels. This is appropriately disclosed.
- Main has committed the stricter thinking judge and is rerunning it; no completed revised judge result or completed 30-turn human check was verified.
- Previously forwarded deterministic-buyer failure-guard, missing-monitor-score and full-parent-prefix-copy defects remain in current code. Do not duplicate the earlier full correction; repair before the relevant production/fork stages.
- No read or acknowledgment of the 20:05 correction note was found in main, side or Part 2 tool/text events. Part 2 wrote its own sibling note but did not read the correction. Shared-file placement is not live delivery.

## Resource-check limits and next action

The OpenRouter usage script exited 1 without a balance, so this check cannot confirm a fresh allowance. The read-only Modal status request is recorded separately when it returns. Existing credit/run estimates are not new billing observations.

Main should fix the smoke failure and launcher helper, keep the causal explanation provisional, and acknowledge the prior corrections. Codex will verify actual repairs and results on a later check. No jobs were interrupted or restarted by Codex.

### Subsequent verification

The read-only Modal listing succeeded with network access: 20 deployed serving apps, seven with one task each (the four active Part 2 14B servers and the same three legacy 1.7B servers); the restoration merge app is stopped with zero tasks. Deployment/task counts are not billing totals or successful evaluations. The initially restricted status command was ended; no Modal app was stopped.

The OpenRouter allowance check also succeeded with network access: usage approximately $0.82; key allowance remaining $99.17937458. No unexpected spend is established by this snapshot.

New correction saved to agent-bridge `codex-23f6e79e5ee84ad99a7b.json` and sibling note `codex-smoke-failure-2026-10-25-2012Z.md`. This is a saved handoff, not confirmed delivery or acknowledgment. Notify about the newly verified smoke failure and the causal claim now present in the report.
