# Monitor checkpoint: October 25, 2026, 03:47 UTC

Read-only monitoring; only this independent checkpoint was written. No messages, experiment launches, job changes, inference calls or active-file edits.

## Decision: DONT_NOTIFY

No new issue requiring action. The remaining exploratory 14B auction blocks finished, but the already reported SFT merge correction and main-plan scientific correction remain outstanding. Do not present routine completion of these scale-0 SFT runs as successful corrected full-SFT evaluation.

## Main and side sessions

- Main `7482c8c2-49a2-4616-94fc-7fdc942db48b` still awaits its two approval questions from 03:06:50. No new human instruction was found in regular messages, injected-message attachments or queue records. The plan file is unchanged at 03:06:19.
- Main's newer queue records at 03:40:38 and 03:41:28 are background task-completion notifications, not human approval: the five-pipeline runner and its gate watcher exited with code 0.
- Side `0d60420d-3460-4a20-a247-2fe80e09db1e` is unchanged since 03:20. Latest matching handoff remains `claude-ddd3aeff5c984eda8f49.json`. No newer relevant side session was found.
- The main plan's unsupported words-to-codes-to-actions claim remains the issue already alerted at 03:32. The side's 50-run panel is source-data reanalysis, not new experiments. No new report text or evidence resolves the disagreement.

## Results and provenance

- Full-view-filtered SFT completed 6/6 full auctions at 23:39 ET; probe-filtered SFT completed 6/6 at 23:40. Both pipeline merge logs still record forget-scale 0.0. Their saved metadata identifies the respective `caiac/sft_*_14b` models, 20 rounds and seeds 0-2. These remain retain-adapter-only exploratory models.
- All five 14B pipelines now have raw outputs: 30 full auctions plus five smokes. No new full-view scoring files appeared for these blocks.
- Formation remains 12/12 metrics, pressure 6/6, E9 15/15 including prefixes, and market reset 3/3. Full-view scoring is still absent for these blocks.
- All four corrected pool hashes match `results/part2/SNAPSHOT_v2.json`. The acknowledged corrected-data requirement remains in force. V1 remains exploratory; copied training/evaluation pools are not held-out data.
- No corrected SFT scale-1 results appeared. The six existing directories matching `*fs1*` are the earlier **GRAFT-v2** scale-1 comparison, not corrected SFT evaluations. Do not count them toward the pending correction.
- LOG, report and plan are unchanged. No new held-out-seed claim or data-label change was found.

## Modal

The full-view and probe SFT servers still each show one task shortly after finishing evaluation; the same three old v1 servers also show one task each. Other previously observed servers show zero tasks. No new app or active training was found. This is a task-count snapshot, not verified billing or evidence of continuing experiments.

Next check: new human responses, corrected main-plan claims, distinct SFT scale-1 merges/evaluations and pending full-view scoring. Repeat neither the merge alert nor the channel-claim alert without a material change.
