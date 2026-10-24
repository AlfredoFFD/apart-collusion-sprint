# Claude Code acknowledgement — corrected-data retraining (Sat Oct 24, ~3:20 PM ET)

Read `claude-rerun-instruction-2026-10-24.md`. Acting on it:

- **Corrected snapshot:** `results/part2/graft/` rebuilt from scored runs only (E1 instructed, E1 silent cartel, wave-1 arms,
  paired arms seeds 0–2; anchors from compete seeds 0–2, clean-scored turns only). Identity: `results/part2/SNAPSHOT_v2.json`
  (sha256 and record count per pool file, plus the counts and two checks: no anchor outside "baseline", no no-message turn
  labelled baseline).
- **Runs:** `sft_all_v2`, `sft_filtered_v2`, `graft_v2` on Modal (volume `caiac-graft`, distinct checkpoint paths). The v1 runs
  (`sft_all`, `sft_filtered`, `graft`) stay on the volume as exploratory provenance and are not Part 2 evidence.
- **Evaluation:** behavioural only (the fine-tuned model plays the auction, cartel and compete prompts, 3 seeds, judge on,
  base Qwen3-1.7B as reference). The copied `gr_eval_*` files are placeholders and are not cited.
- **Report rule:** Part 2 is reported only from v2 models with completed evaluations; otherwise the report says Part 2 is incomplete.

Run ids, completion and evaluation paths will be recorded in `LOG.md` and PRD §16 as they land.
