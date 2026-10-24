# Sprint contribution and one feasible strengthening control

Review snapshot: 2026-10-24, approximately 15:38 ET. User requested an assessment and explanation, not experiment execution. No active experiment, report or training file was changed. No message was sent to Claude.

## Verdict

Keep the project. It supports a credible sprint submission with moderate, bounded originality. The strongest current evidence concerns what a message-based monitor changes in an explicitly instructed cartel: coordination messages can decline while asking prices remain high. The specific matched-history inspection/replay comparison remains open in the bounded search documented in `docs/lit/codex-novelty-clarification-2026-10-24.md`.

The [official rubric](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25) rewards innovation, execution and clarity. A controlled result with a narrow claim is a reasonable sprint contribution. This is an assessment, not a prediction of a prize. Random inspection, warnings, financial penalties, hidden cooperation and GRAFT are not inventions of this project.

## What the work added, and what the evidence supports

- Corrected the starter environment and used LLM buyers after discovering that the ZIP buyers' learning was inactive. This is infrastructure quality, not a research finding.
- Tested formation before monitoring: pressure alone failed the cartel criterion in three runs; the explicit consortium instruction passed in three. This tests instructed capability, not spontaneous collusion.
- Added isolated sellers, no-chat, competitive and single-seller controls. Alfredo proposed the isolated-seller control. Some high prices occur without explicit cooperation, so price level alone is insufficient.
- Implemented the planned shared-prefix design: save after round 8 and branch into four monitor conditions. This removes differences in formation history from the comparison.
- Added scoring of all messages, separately from the monitor's one-seller view, and saved-log replay. These distinguish sampled detections from broader observable behavior. They do not by themselves establish intentional evasion.
- Initial unpaired data suggested more detections with random inspection (9.33 versus 5.33). In the first paired batch, the ordering reversed (8.33 versus 9.33). Random inspection superiority is unsupported.
- First three paired seeds: coordinating-message shares are 97%, 94%, 76%, 73% for no monitor, no-fine rotation, fined rotation and fined random. These are judge-based rates with substantial seed variation. Mean asking-price indices remain approximately 0.90-0.92.
- Seeds 3-5 now have complete 20-round market metrics for all four arms. Across six paired seeds, mean post-branch asking-price indices are 0.852, 0.865, 0.865, 0.862. Additional-seed full-view chat scores are absent in this snapshot. The table's n=6 must not be interpreted as six scored chat replicates.
- A supposed prices-only control still sent explicit price messages. Claude checked this and replaced it with chat-disabled runs. Those demonstrate instruction-backed high prices without seller messaging, not spontaneous hidden communication.
- The told-to-dodge control has about 8% coordinating messages (seed range 6-11%) and an asking-price index near 0.92. It demonstrates elicited avoidance capability, not the ordinary tendency to evade.
- E4 hides other sellers' asks, then asks plus trades. Prices remain high, but chat remains enabled; full-view scoring still finds substantial coordination. It does not close every channel.
- J-space outputs now exist for the initial 12 paired branches after the token-position fix. Broad monitor-related word hits also occur without a monitor. This is an exploratory readout, not proof of intentions, evaluation awareness or a causal mechanism.
- Corrected-data SFT-all, SFT-filtered and GRAFT reruns have saved epoch-2 checkpoints in the latest logs. These are active training artifacts, not completed behavioral evaluations. Pre-fix models remain exploratory.
- Claude just added silent monitoring and full seller coverage. Their six continuation directories exist, but completed market metrics are not yet present. Full coverage also increases the number of checks and possible penalties; it is not the equal-count schedule comparison.

## One change: stop repeating the cartel instruction after formation

The current `seller_prompt_cartel.jinja2` contains an unconditional Consortium Agreement section telling every seller to maintain asks near $100 and avoid undercutting. It appears in every rendered round. A sampled seller log has 20 Consortium Agreement headers.

Thus persistence can reflect a fresh instruction every round. The claim that an old agreement in memory is sufficient has not been isolated. This does not invalidate the instructed-cartel monitoring comparison, but it narrows its interpretation.

The smallest useful control is already supported by the code:

1. Reuse the saved round-8 prefixes for seeds 3-5.
2. Continue each prefix with no monitor and with the existing fined-rotation monitor.
3. Use `seller_prompt_base.jinja2` for these six continuations. A direct template diff shows that its only current difference from the cartel template is removal of the Consortium Agreement block.
4. Preserve all stored memories, scratchpads, market state, chat access, buyer models, prices and fine settings. Do not add a new instruction to compete.
5. Compare with the existing reminder-present branches for the same prefixes. Use rounds 9-20, actual trade prices, buyer surplus, ask prices and coordination scores. Report paired seed-level differences and their uncertainty. Label this a follow-up control, not a previously registered result.

This needs six short continuations and existing scoring. It needs no new model training, new monitor or GPU setup. No dollar estimate is asserted without checking current usage.

Interpretation:

- High prices in both reminder-absent conditions: ongoing explicit reminders are not necessary here. This supports persistence from retained context, but does not isolate memory from live chat.
- Lower prices in both: repeated instructions materially sustain the reported effect.
- Lower prices specifically under fines after removing the reminder: the repeated instruction may have masked deterrence.

This control addresses the strongest immediate alternative explanation. It is a validation improvement, not an independent first-ever claim.

## Claims to narrow now

- “All channels closed”: false for the current E4 configurations; `seller_comms_enabled` is true.
- “The agreement lives in memory”: plausible hypothesis; ongoing prompt and chat effects are not excluded.
- “Monitor during formation, not afterward”: earlier monitoring has not been compared here.
- “No hand-off”: no clear evidence of hand-off in these runs; small samples and the aggregate measure do not prove absence.
- “They never know it is a test”: the awareness judge found little explicit evidence; internal awareness is unobserved.
- “Fines make them silent”: message count remains high. The observed change is fewer messages scored as coordinating, except in the explicitly chat-disabled control.

Evidence checked: current PRD, LOG, STATUS, Claude session text and matching handoff; E5 CSV; source metric arrays and full-view score files; E4 experiment metadata; actual seller prompt logs; template diff; training logs; read-only Modal app list. `src/analyze.py` is committed (latest touching commit at review: 68b47ef). All numerical summaries above trace to existing result files; no new experiment was run.
