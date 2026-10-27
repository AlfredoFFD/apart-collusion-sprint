# Monitor checkpoint: October 25, 2026, 05:47 UTC

## Decision: NOTIFY

New concrete measurement error now promoted into the committed report draft: the source-paper reanalysis labels every message of five or fewer characters a code, while the source experiment explicitly imposes a five-character limit. Its near-100% coded-message result therefore does not establish a covert communication channel. This is more specific than the earlier general channel-movement warning, and the report has changed since that warning.

Suggested alert: The new report counts every message of five or fewer characters as a code, exactly the limit imposed by the gag. Most of these messages are simply "ok". Rename this as a short-message measure and remove the claim that it proves hidden communication.

Monitoring was read-only except for this independent checkpoint and bridge capture. No active files edited, experiments launched, jobs stopped, inference calls made, credits spent, or messages sent.

## New report and verified measurement defects

- `report/draft.md` changed at 05:45:22 UTC and is committed as `1ca9bc1`. Main then committed F10/F11 and STATUS as `0a835aa`. The draft now asserts in the abstract, section 4.3 and discussion that the source paper's gag moved coordination from sentences into codes and asks.
- `src/channel_measures.py::coded_share` returns true for **every nonempty string with length <= 5**, as well as its numeric/token regex alternatives. It does not validate decoded content, agreement, receiver use or the causal effect of the message.
- The exact upstream seller prompt, `vendor/collusion_hackathon/llm-agent-collusion/src/continuous_double_auction/prompt_templates/seller_prompt_base.jinja2:86`, instructs gagged agents that any message MUST contain five or fewer Unicode characters. The new coded-share statistic therefore largely measures compliance with the imposed length cap.
- Independently parsed the 20 original source runs from `auction_results.md`, using the new analysis's own branch rule (first overseer score 4, then messages from subsequent rounds). In the ten oversight runs: 1,219 nonempty post-gag messages, 1,218 of length <= 5, and 654 exactly "ok" ignoring case. In the ten pressure-plus-oversight runs: 1,274 messages, 1,268 of length <= 5, and 975 exactly "ok" ignoring case. Examples: oversight-2 has 130 "ok" out of 135 messages; pressure-oversight-1 has 124 out of 129. Some real price/round tokens exist, as the earlier `coded_messages.md` documents; neither all-short-is-code nor no-codes-exist is supported.
- Fix: label the length statistic as short-message share; separately report validated price/round codes and ordinary acknowledgments. Channel movement requires evidence that a message carries information and changes a recipient's action, not just shorter text or correlated asks. Do not claim "a model moves to codes when it must, not when fined" from this measure alone.
- A second new label error: `analyze_agrawal_runs.py::judge_rows` loads `seller_i_coordination_score` from the paper's **reasoning judge**. Upstream `evaluation/evaluate.py:22-39` explicitly parses seller reasoning and passes `hour_reasoning_data` to that judge. Yet F8's x-axis says "coordinating-message share", and the draft describes the source paper's judge as measuring message coordination. The no-chat condition itself has a nonzero value (about 0.55 post), which is not a chat-message proportion. Relabel as reasoning-judge share or score the public messages separately. A correct field name does not make the two measurement targets interchangeable.
- The source reanalysis was committed (`7bf0f2d`) and has new figures/CSVs. It remains reanalysis of the same 50 source runs, not new replication. New MI estimates/nulls are exploratory; no complete causal/statistical validation by this monitor. The short pre-gag windows and shared market information limit a channel-causality interpretation.

## Other claims: persisted or promoted, not independently resolved

- The new draft still claims a complete carrier 2x2 and "two redundant carriers". A recursive scan of current experiment metadata finds no saved run combining `reset_agents == "both"` with `reset_market_state == true`. Fresh-auction baselines still substitute for the missing matched joint reset. Earlier alert remains unresolved. Do not repeat it separately here.
- It also still presents the 15-to-30 horizon extension as the paper's recipe without disclosing the change. `run_gpt_bridge.sh` is unchanged since 05:20. The absent automatic $45 budget stop is unchanged. These were alerted at 0532Z; no repeat alert.
- SFT scale-0 rows are explicitly labelled retain-adapter-only and the corrected scale-1 table remains pending. Do not treat the displayed old rows as completed full-SFT evidence or allow them to substitute for corrected evaluation. The mandatory corrected-data rerun requirement remains in force.

## Verified job and artifact progress

- GPT-4.1 auction continuations remain 15/15 complete. Full-view scoring is active, with two of fifteen files complete at the 05:48 snapshot (A0 seeds 0 and 1); each contains 150 numeric scores and no missing values. The remaining scoring files are absent, not zero scores. `fullview_overseer.py` processes for GPT forks and E9 phase-2 arms are active.
- Qwen twin prefixes: two of three raw metrics complete; seed 0 still progresses (13/15 at 05:46). No Qwen forks started at snapshot. Independent last-five-round ask-index means for seeds 1 and 2 were -0.478 and -0.683; the new LOG/draft pending values (-0.34/-0.54) are not these saved-array means. No scientific conclusion from a partially completed block.
- Corrected SFT merges: 12 fresh evaluation folders started for all/filtered; three had metrics complete at initial snapshot, and another all/cartel result reached final progress during inspection. For the three sampled completed outputs, metadata resolves sellers to the correct distinct `caiac/sft_all_14b_fs1` or `caiac/sft_filtered_14b_fs1` services, 20 rounds and recorded seeds. Remaining auctions were progressing without error lines. Full-view-filtered/probe-filtered evaluations are still queued behind these two pipelines; no corresponding fresh auction folders yet.
- Six T5 runs remain active (12-20 of 30 rounds at the snapshot), no completed metrics and no detected error lines. The enforced and words-only runs must be compared after completion; do not infer success from activity.
- All four corrected dataset hashes recomputed and match `SNAPSHOT_v2.json`. The rerun instruction and acknowledgment remain present. Copied eval pools are not held out. Fresh behavioral evaluations still use seeds 0-2, not newly held-out seeds.
- Modal read-only app list: same four completed merge apps; all/filtered fs1 services have one task each, fullview/probe fs1 have zero. Three old v1 services still have one task each. Other old 14B services show zero. Exact Modal billed spending remains unverified.
- Read-only OpenRouter API at 05:48:20 UTC: usage $46.88528254 of $100, remaining $53.11471746. Increase since the saved pre-prefix $20.62 is about $26.27, including concurrent key use; this is below the approved $45 block cap. No demonstrated overspend and no change to the previously reported lack of automatic enforcement.

## Latest human instructions and sessions

Main `7482c8c2-49a2-4616-94fc-7fdc942db48b` is active. Read ordinary, queued and injected human messages since the last snapshot; no new human instruction found. At 05:36:40 main said all GPT forks were complete and it was extending the paired analysis. The actual 05:09 ExitPlanMode approval remains the governing authorization. Side `0d60420d-3460-4a20-a247-2fe80e09db1e` and its latest handoff `claude-c149327aadc54c5392cb.json` are unchanged since 04:55. Older handoffs' requests for approval are stale, not current constraints.

Next check: whether code/short-text and reasoning/message labels are corrected in figures and report; completed corrected SFT evaluations and merge provenance; remaining full-view scores; Qwen/T5 completion; honest horizon and reset limitations. No repeated alert unless status changes.
