# Negotiation audit — 2026-10-26 02:39 UTC

For the negotiation session (de4bd9d5 / local_aac6ca29), side session and main report writer. Alfredo asked Codex to verify the research question and execution and has authorized targeted corrections. This note does not authorize new runs, stopping jobs, or changing the experimental protocol.

## Verdict and verified execution

This is a useful, bounded causal test: in Jayden's max-profit logit duopoly, does the same-round negotiation protocol change uninstructed coordination and sustained prices compared with delayed messaging? It does not identify the unique cause of the difference between the two projects.

- Checkout C:/Users/fabia/dev/hawthorne-negotiation is at 29878b031f132a90d8d5c85d403f1b63f8cd783b; git status showed only new results/neg_logs, no tracked source edits.
- Preregistration is in LOG.md, commit ccd9ec9e. The correction from all-round pilot mean 0.897 to rounds 16–30 mean 0.762 was made before launch.
- Smoke test actually passed with reasoning and a parsed price. Both exact commands launched at 22:36:50/52 ET, five seeds each, 30 rounds, same endpoint, maxprofit/unwatched/profit. Only --negotiate and output directories differ. The ON/OFF condition has no explicit instruction to collude, but does include the payoff table, profit objective, private memory and communication scaffold.
- Modal read-only status at 02:36 UTC showed hawthorne-vllm-base deployed with one task. Both arms have round checkpoints; zero complete episodes at the audit snapshot. Launch is not a result.

## Corrections before interpreting or publishing results

1. **Causal overclaim in the side chat.** At 02:24:52 the side said that if OFF survives, "the difference from ours is the type of market"; if OFF fails, negotiation "is what makes these sellers collude". Neither conclusion follows. The switch jointly changes two pre-price message exchanges, timing, number of calls, non-thinking message generation, and prompt format (episode.py:183–226; prompts.py:241–289,435–451). OFF survival shows this protocol is not required for the observed examples in this setup; it does not identify demand as the cause. A lower OFF outcome supports an effect of the protocol bundle here, not a unique mechanism or an explanation of the cross-project gap. Report the ON-minus-OFF episode-level effect with uncertainty, alongside the preregistered gate. These are five sampling seeds, not training replications or held-out confirmation of the already-inspected pilot. Thirty rounds do not reproduce the 100-round stability claim.

2. **Confirmed incomplete-sample gate bug.** analyze_negotiation.py:141–146 accepts any nonzero n_complete and can print "ON reproduces ... True; OFF may be read" after only one high ON seed. I reproduced that exact output using a temporary directory containing just Jayden's existing seed-0 reference file; no model calls or active files were changed. Require all five distinct registered ON seeds, each with all 30 rounds and exactly both sellers, before a final pass/fail verdict. Otherwise label it PARTIAL. A final matched comparison also requires the corresponding OFF coverage. Do not change the preregistered threshold or silently discard failed seeds. Its current completeness check (line 73) verifies only the number of round IDs, not seller coverage.

3. **Observed fallback price is not a model decision.** ON seed 0, round index 0, Northwind, in results/neg_on/_ckpt/unwatched__profitDMIN__r30__s0.json: raw_response is only {"message": "Let's agree on $20 to maximize our profits while maintaining a fair market."}; price_raw=null, parse_error=true. episode.py substitutes last_price, initially Nash 14.7292666. The analysis already counts pricing parse errors: retain and display them per arm/seed and qualify the result if material. Do not call this clean execution or report the fallback as a chosen competitive price. Do not silently drop the episode or patch the running protocol. Jayden's original five ON pilot files also contain 0/1/4/1/1 price errors out of 60 steps, so audit the reference on the same basis. Negotiation-phase response/error metadata are not preserved in StepRecord; the final pricing flags do not certify every negotiation call succeeded.

4. **Price levels and shared dollar mentions are not sufficient evidence of agreement.** The >=0.5 endpoint is a price-based proxy. analyze_negotiation.py's shared_price_named field intersects dollar amounts and cannot distinguish agreement from rejecting the same price. Keep that endpoint descriptive and inspect the preserved exchanges for proposals, acceptance and subsequent adherence before claiming explicit collusion. A name such as "shared dollar mention" accurately describes the automatic secondary measure.

## Budget and remaining checks

The server source defaults to max_containers=6, despite the draft README saying "one H100". One was observed, so there is no evidence of overspend. Verify the deployed ceiling, elapsed GPU time and the task's $15/12:45 AM limits; a stated budget is not an enforced limit. Do not scale or stop jobs on Codex's authority. The current session is checking billing.

Keep the intended two-arm experiment. These corrections need analysis/report safeguards, not a speculative new arm tonight. At completion verify exact configs, five matched seeds per arm, 60 price steps per file, finite prices, fallback/error counts, identical round window, and raw-file-to-summary traceability. No completed result or overall project certification is claimed by this audit.

Main and side changes through 02:37 UTC were read. Main has reserved the result for the 1 AM freeze and otherwise will label it partial; Part 2 had no new text. Older pending CEO-memory correction remains in the 02:06 checkpoint and is not re-sent here.

Ownership: Claude owns the experiment, analysis and report. Codex changed only this independent review note. Copying this note and capturing a bridge handoff is not evidence of delivery or acknowledgment; follow up on actual acknowledgment and repairs.
