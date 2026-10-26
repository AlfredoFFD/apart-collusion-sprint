# Monitor checkpoint: October 25, 2026, 05:02 UTC

Read-only monitoring of main/side sessions, handoffs, LOG, revised plan, source scripts, current results and Modal. Only this independent checkpoint was written. No messages, inference calls, experiment launches, job changes or active-file edits.

## Notification: the purported completed reset factorial lacks its matched joint-reset cell

The newly revised main plan marks T2 "Carrier 2x2 at the branch: wipe agents / wipe market / neither / both (fresh)" as **done**, with 0.91 / 0.91 / 0.95 / about 0.3. It states that only interventions touching both carriers work and makes this the headline explanation.

Read all saved `results/*/experiment_metadata.json` records: 27 contain reset metadata, but **none** has both `reset_agents == "both"` and `reset_market_state == true`. The fourth cell is a fresh auction, not a simultaneous reset at the same saved branch. It differs in history and timing, and cannot stand in for the matched joint intervention. Even the single-reset arms retain overlapping information. The existing data establish persistence under the specific resets tested, not a completed causal isolation of two independent carriers.

Concrete correction before plan approval: either include the matched simultaneous reset and check precisely what information is cleared, or narrow the carrier conclusion. No new experiment was launched by Codex. This is a newly verified missing-cell issue in the plan's claimed completed test, distinct from the already alerted channel-movement and sting wording.

## New user direction and authorization

- Side user at 04:50:29 asked whether steering could be more useful than prompting. Side then ran a local projection of existing activations, without model/API calls.
- Main user at **04:54:25** asked for the strongest plan and novelty argument, and specified **do the deactivation work here, not delegate it to Jayden**. Verified the queued/injected text. This is planning direction, not spending approval.
- Main rewrote its plan at 04:58:47 and called ExitPlanMode at 04:59:06. No acceptance result or new launch was found. The plan explicitly says execution awaits approval and proposes $35 expected/$45 cap for GPT-4.1 plus Modal remerges and local T5 work.
- Main still treats the completed Agrawal reanalysis as future work and repeats its unsupported channel claim. Those issues were previously alerted; do not resend them unchanged.

## Side projection: completed analysis, overbroad negative interpretation

Latest side handoff is `claude-c149327aadc54c5392cb.json`, 04:55:02. Script `src/e8_riemer_projection.py` is committed in `a297631`; `results/e8_riemer/{scores.csv,summary.md}` exists and LOG records it as exploratory. It projects 3,130 existing reply-token activation means onto borrowed vectors. Layer mapping is explicitly checked as hidden_states index minus one, with an offset comparison. This is an observational readout test, **not a causal steering intervention**.

Independently read the CSV and recomputed the rank statistic for A0 cartel versus compete at the exact middle-layer mapping: 216 versus 180 turns, AUC **0.2691358**. Negating the same scores gives **0.7308642**. Thus "chance or worse" does not mean no discrimination. This post-hoc sign flip is not a validated detector either: seeds/prompt groups differ, repeated turns are dependent, the silent-cartel comparison is near chance, and independent calibration/held-out evaluation is absent. Do not promote this into proof that steering fails or that interpretability never transfers. A defensible description is an exploratory, unvalidated transfer check with inconsistent direction and specificity. Prioritize the missing core reset cell in this heartbeat's short user alert; preserve this analysis caveat here for the next review.

## Corrected models, jobs and remaining limits

- All four corrected v2 pool SHA-256 values were recomputed and match `results/part2/SNAPSHOT_v2.json`. Acknowledgment is unchanged. Original v1 remains exploratory, as do no-routing SFT models merged at scale 0.
- No new training, scale-1 SFT merge, fresh SFT evaluation, full-view scoring or held-out-seed evaluation appeared. The six existing fs1 result folders belong to the older GRAFT comparison and do not satisfy the SFT correction.
- All previously observed auction blocks remain raw-complete. New result work is the local projection only. Report and PRD remain unchanged; LOG gained the projection entry.
- Modal: same three old v1 servers show one task each; all five tuned 14B servers and base14b show zero. No new app or active training. Billed spend remains unverified.
- T5 now explicitly penalizes low sale prices and removes sellers. Its own plan acknowledges high prices can arise from the shared incentive. Agreement and harm must remain separate; a negative result would not by itself prove that weak models require a proposer.

Next check: plan acceptance versus merely ExitPlanMode request; corrected SFT outputs with distinct names and provenance; actual reset coverage; and whether source reanalysis/readout results are described within their limits.
