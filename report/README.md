# Report files

The submitted paper is the Overleaf project "GRAFT++: Reducing Collusive Behavior in Agents via Localized Training and J-space Monitoring" (Frontera, Jeong, Li, Dash). This folder holds what backs it.

| file | what it is |
|---|---|
| `draft.md` | the long-form companion report for the double-auction work: everything behind the paper's Sections 3.2 and 4.3 and Appendices B and C, including the results the 8-page paper had no room for (formation without instruction under a CEO ultimatum, what holds a cartel's price, the removal check). Written from the files at tag `results-freeze`. |
| `claims.md` | the claim-to-file table: every double-auction number in `draft.md`, the result file and row it comes from, and the command that regenerates it |
| `overleaf_claim_check.md` | the line-by-line check of the paper's double-auction sections and appendices against the result files, with the wording fixes that were applied |
| `overleaf-snapshots/` | the paper's LaTeX source at each point it was checked (`overleaf_main_snapshot_*.tex`, `overleaf_version2_snapshot_*.tex`), named by download time |
| `archive/` | earlier drafts (`draft_v5.md`, `draft_v6.md`), the outline, the numbers-only scaffold used at the results freeze, and the Word reference styles for the local build |

`bash scripts/build_report.sh docx` builds `draft.md` into a Word file locally; `bash scripts/regenerate_all.sh` rebuilds every table and figure the companion cites.
