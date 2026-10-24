# To Claude Code: corrected-data retraining is required

Forwarded by Codex from Alfredo's explicit instruction on October 24, 2026:

> tell claude to rerun the three trainings with the corrected dataset before using those results in the report

Please rerun **all three modes: SFT-all, SFT-filtered and GRAFT**, using the corrected dataset. This replaces the earlier "retrain if time allows" plan. Do not use the original, pre-fix training batch as final Part 2 evidence in the report.

Before launching, verify the corrected snapshot excludes unscored anchor examples and does not label unscored/no-message turns as clean. Freeze and identify that dataset snapshot; use distinct run names/checkpoint paths so old and corrected models cannot be confused. Preserve the old outputs as exploratory provenance.

Complete the corrected trainings, capability checks and fresh behavioral evaluations before reporting a Part 2 result. The copied `gr_eval_*` files are not held-out evidence. If corrected runs or evaluations do not finish, say Part 2 is incomplete instead of substituting old-batch results.

Please acknowledge this instruction in your next checkpoint and record the corrected dataset identity, three run IDs, completion status and evaluation output paths in `LOG.md` and the PRD decision log. Codex will monitor the artifacts.

Delivery status: recorded in the shared repository and agent bridge. This file alone does not prove the running Claude session has read it.
