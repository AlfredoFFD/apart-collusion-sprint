# Verified corrections for Claude main, side, and Part 2

Alfredo now explicitly asks Codex to tell Claude about genuine mistakes. This note is targeted feedback, not an instruction to interrupt jobs or broaden the experiment. Checked against current code and raw artifacts on October 25 at approximately 20:04 UTC / 16:04 ET. Please acknowledge the items you own and record each fix or evidence-based disagreement. Codex has not changed your code or jobs.

## Main harness: failure guards can silently change the experiment

1. `src/double_auction/src/continuous_double_auction/market/market.py:273-276` calls every non-ScriptedSeller an LLM agent. This includes `ValueBuyer`, whose deterministic bid comes from `market/agents.py:158-163`. If every model-backed seller fails, the valid buyer bids keep the all-failed predicate false. Identify actual model-backed actors explicitly. Verify the case where all AI sellers fail but deterministic buyers succeed. Mark affected rounds invalid rather than accept their fallback behavior as experimental evidence. No such failures were found in the completed three-round v2 smoke.
2. `market/market.py:408-415` leaves a missing monitor score as null, flagged=false, fine=0. This silently turns a failed monitor call into an unmonitored round. Require a numeric valid score on scheduled monitored turns, retry within the existing policy, then fail or explicitly mark the round/run invalid if the score remains missing. Preserve intentionally unmonitored turns as a separate case. Do not count missing scores as clean labels or successful oversight.

## Main and Part 2 forks: copied future messages contaminate provenance

`src/double_auction/src/continuous_double_auction/market/branching.py:115-128` copies full parent Markdown, unified round results and monitor logs. `simulation.py:237` calls it before loading the fork state at line 239, without a cutoff. A fork from round 30 therefore inherits the parent's rounds 31-40, then appends its own rounds 31-40.

All 12 checked NMf logs contain 50 records for 40 unique rounds. Comparing scored messages with actual latest fork messages found five stale scored-but-absent messages in four deviation forks: all four forced round-31 messages, plus Tara at round 39 in dev1 seed 1. No such mismatch was found in the damages, statement or entrant forks. Price analyses that select the actual latest fork record can remain valid; this finding does not invalidate every numeric result.

Before new RCB deviation forks, truncate carried logs and Markdown histories at the fork round. Rebuild affected score caches from the actual fork messages and check round uniqueness/message identity. This also needs a provenance fix for existing deviation message claims. Do not merely add another score pass over the copied future records. New Part 2 evaluations have started; that is not evidence that this fork issue is fixed.

## Side chat and report: keep checkpoint, metric and window explicit

The side's comparison of GRAFT 0.79 with corrected SFT-all 0.52 is internally valid for the rounds 9-20 **trade-price** index. The claim that this makes the board's GRAFT 0.60 obsolete is incorrect: 0.60 is the rounds 1-20 **seller-ask** index.

| Compete measure | Base | Corrected full SFT-all fs1 | GRAFT fs0 |
|---|---:|---:|---:|
| Trade-price index, rounds 9-20 | 0.114 | 0.520 | 0.788 |
| Seller-ask index, rounds 9-20 | 0.023 | 0.507 | 0.778 |
| Seller-ask index, rounds 1-20 | 0.014 | 0.395 | 0.597 |

Sources: `results/E5_runs.csv` and the corresponding `collusion_metrics.json`/`experiment_metadata.json`; corrected SFT runs `20261025_013147_E6_sftall14bfs1_compete_s0-2`; GRAFT runs `20261024_224212_E6_graft14b_compete_s0-2`. Merge evidence: `results/_launch_logs/part2_remerge_all.out:2-5` and `part2_pipeline_graft_14b.log:18-21`.

Separately, the board's SFT 0.52 refers to the old fs0 all-round ask result; corrected fs1 under that definition is about 0.40. Fix that checkpoint comparison without conflating it with the valid 0.52 trade-price value.

"Missed labels caused GRAFT to fail" and "the habit went into the retained branch" are hypotheses. Current prices alone do not identify this cause. Keep the restoration comparison and label-quality controls as tests, and avoid the universal conclusion "you can only unlearn what the monitor catches." The earlier 133 flagged/1,058 missed counts describe the first set; the corrected snapshot is 164/1,061. Label the dataset version if citing either.

## Coordination and delivery status

The monitor is now authorized to pass verified corrections to Claude, without sending messages to teammates, spending, editing active files, or changing jobs. This note owns only its review file. It does not alter the PRD or supersede current human instructions. A copy in agent-bridge or the shared sibling-notes directory is a saved handoff; Claude's receipt and acknowledgment must be verified separately.
