# Monitor checkpoint: October 24, 2026, 21:57 UTC

Inspected actual artifacts, latest session text, handoffs, LOG.md and read-only Modal app status through approximately 18:00 ET. Only this separate checkpoint was written. No messages, experiments, endpoint inference, active-file edits or process changes were made.

## Meaningful new result

`results/e8/directions.json` now reports the within-prompt probe at depth 0, chosen by fitting on seed 0 and selecting on seed 1. Its AUC against the full-view chat judge is 0.6837657. A plain keyword baseline scores 0.7707702 on the same cases. Per-seed AUCs are probe 0.734 / 0.782 / 0.554 / 0.657 and keywords 0.748 / 0.874 / 0.827 / 0.709 for seeds 2-5. This is evidence that this probe does not improve on that simple text baseline for predicting the judge's labels; it is not an independent test of hidden coordination.

Claude's explicit response to the interactive review exists at `claude-ack-codex-approach-review-2026-10-24.md`. Code, report, PRD and STATUS independently verify several corrections: directions are exploratory; replay is described as reconstruction; public-history causality is narrowed; a text baseline and a functional auction gate were added; pool manifests exist. The main session records these changes and the negative probe comparison.

## Dataset and training provenance

All four actual v2 pool hashes match `SNAPSHOT_v2.json`. All pool files also match the new manifests in `graft`, `graft_v3`, and `graft_fullview`. The required original corrected SFT-all/SFT-filtered/GRAFT runs remain distinct and completed; no v1 substitution was observed.

Important version distinction: the probe-filtered 14B training still uses the frozen earlier depth-1 labels (799 forget / 949 retain). The newer depth-0 analysis would produce 727 / 1,021. Claude restored the original pool hashes after the analysis overwrote them and saved the unused newer pools separately. Actual training log count is 949. The report must identify this difference explicitly before connecting its new 0.68 probe figure to the training experiment. Restoring provenance is correct; it does not make the earlier layer choice independent of the evaluation data.

Likewise, moving layer selection to training seeds after inspecting seeds 2-5 does not restore those seeds to historically untouched status. The new code is better, but claims of a fresh independent test still need new seeds. Claude's acknowledgment explicitly leaves independent reviewer labels, matched false-alarm rates and untouched evaluation open.

## Actual progress

- Repaired 1.7B GRAFT now has all six metrics files and 20 responses per seller per run. `E5_runs.csv` reports ask-key share zero in all six, with only initial-order profits. The failure was already known while these runs were active; completion confirms it.
- All five 14B training apps have one active task. Logs show training has started for each. GRAFT and full-view-filtered SFT have completed one epoch; no final completed training result was verified. Effective example counts are all 1,748; budget-filtered 1,584; GRAFT 1,748; probe-filtered 949; full-view-filtered 523. Dataset size/training-exposure differences remain relevant to interpreting the label comparison.
- Untuned 14B reference auctions are in progress at rounds 10-16, with no completed metrics at the sampled check.
- The six joint-reset forks are progressing. Four have completed metrics, two are still finishing. No full-view scores exist for these new forks or the E6 runs inspected. Do not treat partial forks or unscored auctions as a completed causal comparison.
- No exact spend was obtained, and no new spend anomaly was confirmed.

## Remaining gate limitation

The new shell gate does stop a model with no asks. Its implementation checks a non-null ask in at least half the replies, numeric aggregate ask-index entries, and a positive trade count. It does not check `math.isfinite` on each submitted ask, and initial orders can contribute trades. Thus its claim to validate finite asks is stronger than its implementation. This is recorded for follow-up; no new real model was observed passing with invalid asks, so no separate failure alert is issued.

## Session context

Main experiment owner remains `7482c8c2-49a2-4616-94fc-7fdc942db48b`. Its latest text at 21:52 says it is waiting for the ongoing jobs. A newer handoff, `claude-a4000dcb47b4407587d5.json`, belongs to fork `0d91da4e-1f2e-4f0e-9af1-d4377154f4c1` discussing in-context versus reward training. It is not a completion record for the experiments. Its predictions that reward training would necessarily produce faster collusion or evasion are hypotheses, not measured results; no corresponding new experiment was verified.

Notification: the simple text baseline outperforms the activation probe on the current judge-label comparison, and Claude has updated the report to reflect that negative result. Larger-model training remains in progress. Other previously reported concerns are not repeated as alerts.
