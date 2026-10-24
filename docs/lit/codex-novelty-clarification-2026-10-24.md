# Bounded contribution check, 2026-10-24

**Verdict: partly done.** The exact combination of a shared auction prefix, fixed-count rotation versus random seller inspection, and saved-log replay remains **open in what we searched**. This is an experimental comparison, not a new monitoring algorithm. Applying GRAFT to a multi-seller cartel is a candidate extension. Removing behavior missed by a monitor is already a central GRAFT result, not our general invention. Confidence is moderate in these overlaps and limited in any absence claim.

This is a focused update to existing project searches, not an exhaustive literature review. No experiments were run for this note. Current project design was checked in `docs/PRD.md`; wording in `docs/REVIEW-GUIDE.md` and `report/draft.md` is not independent evidence of priority.

## Closest prior work

| Source | What already exists | Remaining distinction | Reading scope this turn |
|---|---|---|---|
| [Agrawal et al., 2507.01413](https://arxiv.org/html/2507.01413) | Auction sellers, oversight, communication limits, coordination scores and market outcomes. | Our matched-prefix inspection-schedule comparison and replay. | Full-text sections 2.2, 3 and 4 inspected; not a fresh full-paper read. |
| [Garra, 2609.13037](https://arxiv.org/html/2609.13037) | Compares warning-only, payoff penalties, and a random market entrant in LLM pricing. | A random entrant is not randomized inspection. Warnings versus penalties alone cannot establish our priority. | Abstract and full-text sections 2 and 5 inspected. |
| [Das et al., 2609.03035](https://arxiv.org/html/2609.03035) | Fixed activation monitors, awareness and feedback conditions, detection evaluated separately from collusion success. | Different monitoring mechanism and our seller-inspection allocation/replay comparison. | Abstract and full-text sections 2 and 3 inspected. |
| [Tonini et al., 2606.10747](https://arxiv.org/abs/2606.10747) | Budget-aware multi-agent monitoring. | A limited inspection budget alone is not new. | Abstract only. |
| [Ward et al., 2610.17062](https://arxiv.org/html/2610.17062) | GRAFT, imperfect monitors, filtering baselines, missed-behavior suppression, and supervised fine-tuning as well as RL. | Test transfer to harmful joint pricing by several agents. | Abstract and full-text sections 5, 7, D.1 and G.4 inspected. |
| [Lee and Park, 2609.18346](https://arxiv.org/abs/2609.18346) | Pricing outcomes and reported reasoning can diverge. | Our specific interventions and matched comparison. | Abstract only. |
| [Mathew et al., 2410.03768](https://arxiv.org/html/2410.03768) | Hidden collusion under incomplete oversight. | Do not claim discovery of hidden collusion in general. | Abstract/introduction only. |

## Coverage and defensible claims

- AI collusion: covered by prior work.
- Warnings versus economic consequences: covered, although exact mechanisms differ.
- Monitoring budget: covered.
- Measuring detection separately from harmful outcomes: covered.
- GRAFT and learning with missed detections: covered.
- Same established cartel, fixed inspection count, predictable versus random inspected seller, plus saved-log replay: open in this bounded search.
- GRAFT transfer to a multi-seller auction, with ordinary training and monitor filtering as comparisons: open in this bounded search; not a demonstrated result yet.

Plain-language research question: **If we can inspect only one seller each round, does an unpredictable choice reduce harmful cooperation? Or does it only change what the monitor detects?**

Replay applies both inspection rules to the same saved conversations. It estimates sampling differences with behavior held fixed. Comparison with live branches helps assess behavioral responses. Replay alone cannot prove intentional evasion. Match inspection counts; do not claim equal token spend without checking actual tokens. The cartel is instructed, so this does not establish spontaneous collusion.

For Part 2, the added question is whether GRAFT's existing result transfers to several models whose combined decisions determine prices. Improved detection scores alone are insufficient. Use corrected-data checkpoints, fresh auction evaluations, actual market outcomes and preserved trading capability. The present note does not establish their completion.

Prior work containing the same matched-prefix inspection/replay design would remove the proposed design gap. A null schedule effect would answer the question without supporting random inspection superiority. Reduced collusion accompanied by an inability to trade would not establish successful selective removal.

## Verification and search record

References: `codex-novelty-clarification-refs-2026-10-24.json`. Verification output: `codex-novelty-clarification-verification-2026-10-24.json` (7/7 OK).

Searches used lit-sprint on 2026-10-24. Source hit counts are before relevance filtering and deduplication.

| Query | Window | arXiv | OpenAlex |
|---|---|---:|---:|
| collusion randomized monitoring | Last six months | 0 | 6 |
| gradient routing collusion | Last six months | 1 | 6 |
| LLM collusion inspection | All years | 5 | 6 |
| LLM collusion monitoring fines | All years | 1 | 6 |

Semantic Scholar trails: Agrawal, 8 citations and 8 recommendations; GRAFT, 0 citations and 8 recommendations. A short result list and zero returned citations do not establish absence of related work. Searches did not systematically cover patents, non-English literature, paywalled venues, or all inspection-game theory.

Exact query/date/count logs are the six `codex-novelty-clarification-*-2026-10-24.jsonl` files in this directory. Earlier project search tables were also consulted. No active experiment or report file was modified.
