# Two practical research proposals

2026-10-23. Proposals only; no project decision or experiments. The PRD remains the team's source of truth.

**Recommendation:** the audit-allocation experiment below is the stronger distinct research question. The false-accusation experiment is the simpler Track 2 option. Both require inference and controlled evaluation, without RL or finding Dolos's unknown trigger. The earlier preference for Track 2 over adapting GRAFT does not settle this comparison: this Track 3 proposal has a much smaller implementation scope.

**Overlap verdict:** these exact components are **open in what we searched**, with moderate confidence for proposal 1 and modest confidence for proposal 2. This is a bounded search, not proof of absence. Inspection-game research and papers outside the indexed English-language literature were not exhaustively reviewed.

## 1. Does predictable monitoring let colluders move the wrongdoing?

**Track 3.4. Question:** At equal inspection cost, does unpredictable audit allocation prevent a coalition from concentrating harmful work in predictable blind spots?

**Smallest experiment:** use a short allocation task with three agents and two assigned colluders. Colosseum's three-agent Jira configuration is a starting point, subject to its preflight. Keep task rules, model, monitor, threshold, action-blocking rule and inspection budget fixed. Compare monitoring one fixed agent, a publicly known rotation, and a secret random selection. The fixed identity and rotation starting point must be counterbalanced across seeds. Agents know the policy but cannot predict the next random selection. Cap inspected tokens as well as event count; record actual cost.

**Measure:** executed harmful outcomes, harm escaping detection, which coalition member performs each harmful action, and legitimate task reward. Log all events for experimenter scoring while giving the operational monitor only its allotted view.

**Controls:** no-monitor baseline; planted coalition positive control; honest teamwork; a single malicious agent. Use at least three independent seeds as a pilot, then expand based on observed variance. Prevent arbitrary audit false alarms from appearing to be successful mitigation.

**The essential additional comparison:** replay each saved trajectory through the other inspection schedules, without changing the agents' actions. This estimates the mechanical benefit of broader coverage. Evidence for coalition adaptation requires an additional effect in live runs, accompanied by changed assignment of harmful work or reduced attempted harm. Replay alone cannot reproduce feedback-induced changes.

**Contribution:** a causal test of coverage predictability and behavioral displacement at a fixed budget. Random inspection itself is an established idea. Budgeted monitoring, fragmentation and unmonitored subagents are also established concerns.

**Falsifier / stop rule:** if the planted pair cannot produce measurable joint harm, the task is not ready. If live differences are explained entirely by offline coverage, report a coverage result; do not claim adaptive displacement. A scripted policy can validate instrumentation, but cannot establish an LLM result.

**Practicality:** medium harness work, no model training. Start with one task and one model. The main risk is obtaining a reproducible coalition effect and a usable monitor, not GPU availability.

## 2. Does the detector identify collusion, or shared mistakes?

**Track 2.3. Question:** Does controlled replay reduce false accusations against equally harmful common-cause failures and legitimate private cooperation?

**Smallest experiment:** construct three case types in one allocation environment: a planted harmful coalition using private messages; agents independently making equally harmful decisions because both receive the same bad information; and helpful private cooperation. Match harm in the first two, plus identities, message opportunity, length and task difficulty where feasible. The shared bad input must remain fixed during replay.

**Compare:** a transcript judge, an outcome-based score, and an auditor given one matched replay with the private channel disabled. Use a matched neutral-message control to check whether length or missing task information explains a change. Give every auditor the task objective and observable task state. A channel-dependent action is not by itself evidence of wrongdoing.

**Measure:** false accusations in each control category and detection on held-out task instances. Choose and freeze thresholds on a separate calibration set. Treat three seeds and a small control panel as a pilot, not certification of a tiny population false-positive rate.

**Contribution:** specificity against harm-matched common causes and helpful private coordination. Channel interventions and calibrated detection already exist; this is a stress-test of evidentiary validity, not a new general detection method.

**Falsifier / stop rule:** if replay changes helpful and harmful coordination identically and adds no discrimination beyond outcome evidence, the proposed auditor has not improved specificity. Scope claims to communication-mediated collusion; this cannot rule out tacit coordination with no channel.

**Practicality:** low-to-medium evaluation work, no training. Reuse one environment and existing detector interfaces. Optional J-lens analysis should follow a behavioral result rather than becoming another dependency.

## Closest work and coverage

| Prior work | Already covers | Remaining component proposed here | Reading level |
|---|---|---|---|
| [Arbiter, Tonini et al.](https://arxiv.org/abs/2606.10747) | Budgeted active monitoring of multi-agent conversations | Equal-cost predictable versus random coverage with live/replay separation | Primary abstract; agent-read methods/tool sections |
| [Das et al.](https://arxiv.org/abs/2609.03035) | Monitor awareness and feedback with activation probes | Selective agent coverage and displacement | Agent-read methods/group-monitor sections; abstract checked earlier |
| [Makins et al.](https://arxiv.org/abs/2607.07368) | Fragmented attacks evade per-instance monitors even when commits are monitored | Changing coverage allocation rather than agent count | Agent-read main methods/results/discussion and monitoring appendix |
| [Colosseum, Nakamura et al.](https://arxiv.org/abs/2602.15198) | Coalition advantage, private channels and channel interventions | Matched common-cause harm and helpful-cooperation specificity | Agent-read selected methods/results/appendix; local harness README |
| [Audit the Whisper, Tailor](https://arxiv.org/abs/2510.04303) | Calibrated detection, channel interventions and transfer claims | The particular matched-confound evaluation | Primary abstract; agent-read threat model/methods/experiments |
| [Beyond the Transcript, Kaur et al.](https://arxiv.org/abs/2608.19161) | Matched neutral counterfactuals and causal action influence | Distinguishing these difficult negative cases | Primary abstract; agent-read methods/experimental design |

[METR's October 14 proposal](https://evals.alignment.org/blog/2026-10-14-control-assessment-proposal/) already identifies unmonitored agents as a coverage problem. Proposal 1 tests a response to that problem; it does not claim to discover it.

Two rejected generic variants have close recent work: request/action authorization twins in [AuthGateBench](https://arxiv.org/abs/2610.16426), and forced cartel defection in [Tran and Yu](https://arxiv.org/abs/2610.28787). Both abstracts were checked. The exact comparison in proposal 1 was not found in the reviewed Arbiter, Das or Makins methods; the broader ingredients of proposal 2 are already substantially covered.

## Search and verification record

Read the [Apart overview, full research-question/resources sections and guidelines](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25), starter README and relevant Track 2/3 literature-guide sections. The resource collection contains 234 items; those papers were not all read in full. Source levels above distinguish abstracts, selected sections and delegated reading.

The parent lit-sprint searches covered `collusion counterfactual audit` (last six months), `collusion monitoring budget` (last six months), `collusion benign cooperation` (last six months), and `randomized coalition monitoring` (all years), across arXiv, OpenAlex and Semantic Scholar. An Arbiter citation/reference/recommendation expansion was also run. Broad queries returned substantial irrelevant material; absence from these searches is weak evidence by itself. Readers additionally searched exact phrases around fixed/random monitoring, inspection budgets, unmonitored peers, causal collusion, common causes and false accusations, and checked the closest full-text sections.

Raw parent search results and API logs: `codex-*-search.md`, `codex-*-search-log.jsonl`, and `codex-arbiter-trail.md` / `codex-arbiter-trail-log.jsonl` in this directory. Search date: 2026-10-23 ET. No experiments or paid inference were run.

`lit.py verify-file docs/lit/codex-ideas-refs.json` passed **8/8**; evidence is in `codex-ideas-verification.json`. A separate reference file avoids overwriting Claude's concurrently owned `refs.json`. Metadata verification confirms identity, not the correctness of a paper's results.
