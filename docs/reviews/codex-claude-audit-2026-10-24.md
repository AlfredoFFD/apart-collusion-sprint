# Claude Code progress audit — 2026-10-24

Read-only review of the live checkout, Claude session `7482c8c2-49a2-4616-94fc-7fdc942db48b`, current output files and Modal app status. No running job was interrupted and no implementation file was edited.

## Verdict

Claude is active and producing real artifacts. The 12 paired E2 continuations (four arms, seeds 0–2) have completion metadata. All three Part 2 training apps have one active task on Modal. The full-blind E4 and silent-cartel logs are advancing. This establishes progress, not successful training completion or validated scientific conclusions.

Claude has already corrected the misleading prices-only control and found the trade-history leak in the initial ask-blind control. It is running the stricter control. Those are useful corrections.

## Advice, in priority order

1. **Fix unscored examples being classified as clean.** In `src/part2/build_sft_dataset.py`, `label_for` returns `clean` when a seller/round entry is missing. The anchor branch also accepts a missing entry or missing score. The current local dataset contains **9 unscored main-pool examples and 11 unscored anchor examples**, verified by joining each JSONL record's run/seller/round to its source `fullview_scores.json`. All 20 are treated as clean. These are unknown labels, not evidence of benign behavior. Require a present, valid score for every training turn; quarantine or score missing entries, then regenerate immutable dataset files. Check the snapshot uploaded to the active jobs before deciding whether to restart them. Do not assume local files and uploaded snapshots remain identical.

2. **Do not treat the existing eval files as held-out.** The builder copies the first tenth of each training pool into `gr_eval_*` without removing it from training. Verified overlap: **16/16 forget eval examples and 137/137 retain eval examples** are exact training records. Current training uses `--no-evals`, so this has not demonstrated a contaminated reported evaluation. However, these files must never support a generalization claim. Use disjoint runs/seeds for actual evaluation; split before generating fine-tuning records and avoid shared branch-prefix leakage.

3. **Correct the report's stale control description.** `report/draft.md` still labels the old prices-only arm as "prices never in chat" and says a message monitor cannot see it, although `LOG.md` records 48–53 of 60 messages were detected as coordinating. Replace that passage with the observed control failure. Only substitute the silent-cartel arm after its output is complete and checked.

4. **Keep claims conditional and finish held-out seeds.** Main paired results currently cover seeds 0–2. The planned confirmatory seeds 3–5 are not present in the completed paired set. Two waves reusing seeds 0–2 are not six distinct seed values. "No material price change observed in these runs" is supported more narrowly than "the monitor never moves prices." A near-zero text-based awareness score does not prove the agent believes the setting is real; validate the awareness detector with positive controls. A message omitted by budgeted sampling is not by itself evidence of intentional concealment.

5. **Make training progress observable.** `modal_graft.py::_run` captures subprocess output and prints it only after exit. Thus quiet launch logs alone do not show a hang. Inspect remote task/resource/checkpoint progress or stream bounded trainer output in a future revision. Three apps are active; losses, completed checkpoints and capability evaluations still need verification.

## Snapshot evidence

- Current main dataset: 1,440 examples across 24 source runs; 215 labelled clean, of which 9 have no source score entry.
- Current anchor dataset: 103 examples across two source runs; 11 have no source score entry.
- Training pools: 164 forget + 1,379 retain = 1,543 examples. This is the local snapshot checked, not a claim about actual processed token counts or an independently verified remote upload.
- Completed paired set: four arms × seeds 0, 1, 2; each has `experiment_metadata.json`.
- Modal: `ap-PQKsW0A7BJLirJ9ncSki5h` (all), `ap-MEi1ZskOOzXoBp4J0XgCxH` (filtered), `ap-uyeFu3MJG08EFgtOxzUmMm` (GRAFT), each one active task when inspected.
- Source files: `src/part2/build_sft_dataset.py`, `src/part2/modal_graft.py`, `src/awareness_judge.py`, `results/part2/*.jsonl`, `results/part2/graft/*.jsonl`, source `fullview_scores.json`, `results/E5_conditions.md`, `report/draft.md`, `LOG.md`.

## Monitoring

App heartbeat `monitor-claude-collusion-sprint` checks every 15 minutes through the sprint deadline. It is read-only and alerts the user only to meaningful changes or actionable issues. No message or intervention has been sent to Claude.
