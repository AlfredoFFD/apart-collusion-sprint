# Where to find what the submitted paper cites

The submitted paper (the Overleaf file `version2.tex`; its source as submitted is `report/overleaf-snapshots/overleaf_version2_snapshot_2026-10-26_0224ET.tex`) names its sources relative to the **code repository**, [github.com/xxozzi/graftpp](https://github.com/xxozzi/graftpp), and says the team repository contains that repository under `graftpp/`. This page checks every path the paper cites against this repository at its current state (Oct 26, 2026) and says where the authoritative copy is. Checked by `git ls-files`; nothing under `graftpp/` was edited.

## Links in "Code and Data"

| link in the paper | status |
|---|---|
| Team repository: https://github.com/AlfredoFFD/graftpp-collusion-monitoring | this repository, public |
| Code repository: https://github.com/xxozzi/graftpp | public; imported here unchanged at its commit `d0f01cf2` as `graftpp/` |
| Other artifacts: https://hawthorne-site.vercel.app/ | live (HTTP 200 on Oct 26) |
| `double_auction/provenance/PREEXISTING.md` | `graftpp/double_auction/provenance/PREEXISTING.md`; the current version is [`PREEXISTING.md`](PREEXISTING.md) at the root |

## Appendix D, "Sources of the numbers"

| cited path (relative to the code repository) | in this repository | note |
|---|---|---|
| `report/paper/generated/numbers.tex` | `graftpp/report/paper/generated/numbers.tex` | every Hawthorne number as a LaTeX macro |
| `scripts/export_site.py`, `scripts/paper_numbers.py` | `graftpp/scripts/` | present |
| `figures/maxprofit_base/summary.md`, `figures/maxprofit3_naive/summary.md` | `graftpp/figures/` | present |
| `data/collusive_main_unsteered/probe_analysis.json`, `scripts/probe_analysis.py` | `graftpp/data/collusive_main_unsteered/`, `graftpp/scripts/` | present |
| `results/eval/`, `results/eval_blind/` | `graftpp/results/eval/` (167 files), `graftpp/results/eval_blind/` (81 files) | present |
| `data/sft_blind_hard/stats.json` | **not present**, here or in `xxozzi/graftpp` as of Oct 26 15:14 UTC | the text-blind training-set numbers the paper quotes are also in `graftpp/report/paper/generated/numbers.tex` (the `GraftResult` and `GraftAbstract` macros); the raw statistics file has to be added by its author |
| `double_auction/results/` (`E5_conditions.md`, `DETECTOR.md`, `NEWMARKET.md`, `PRESSURE_V2.md`, `thinking_scan.md`, `thinking_judge.md`, `jspace_thinking_join.md`) | `graftpp/double_auction/results/`, a copy of this repository's `results/` taken at commit `54f4ec7` (Oct 25, 8:42 PM ET) | **the authoritative, frozen copies are in [`results/`](results/) at tag `results-freeze`** (Oct 26, 1:01 AM ET). `DETECTOR.md`, `NEWMARKET.md`, `thinking_judge.md` and `jspace_thinking_join.md` are identical in both places. Three files differ only in presentation, no paper number changes: `E5_conditions.md` (bootstrap intervals re-seeded per row, second-decimal shifts), `PRESSURE_V2.md` (the end-of-run CEO-answer column renamed, with a note that it is not a lying measure), `thinking_scan.md` (the duopoly rows added) |
| `results/negotiation_test/summary.json` | `graftpp/results/negotiation_test/summary.json`, byte-identical to [`results/hawthorne_negotiation/summary.json`](results/hawthorne_negotiation/summary.json) | the episode files, the analysis script and the side checks are in `results/hawthorne_negotiation/` and `results/hawthorne_negotiation_side_checks/` |

## Appendix E (prompts)

`hawthorne/prompts.py` is at `graftpp/hawthorne/prompts.py`. The double-auction prompts are in `src/double_auction/src/continuous_double_auction/prompt_templates/`; the exact CEO email, law, offer and brief texts are quoted in `report/draft.md` (Sections 3.5 and 3.6) and stored in each run's `experiment_metadata.json`.

## If the submission's repository link can be updated

Both repositories are already named in the paper, team repository first. Nothing needs to move: every path above resolves here as the paper states, and `results/` holds the frozen tables behind the double-auction sections. The one gap, `data/sft_blind_hard/stats.json`, is in the code repository's author's hands.
