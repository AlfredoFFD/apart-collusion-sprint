# Targeted prior-work check — October 25, 2026

**Verdict: partly done.** Adding competitors, separating messages from actions, and manipulating peer influence all have close prior work. The specific proposed entrant-only message isolation experiment on a saved formed auction is open in this limited search. This is a bounded extension, not evidence of a guaranteed breakthrough or a claim to have read the entire field.

Framing: an independently instructed fresh seller enters an established coalition; hold its economic information fixed while removing incoming peer chat; measure explicit policy violations and buyer outcomes, not high prices alone.

## Closest work and reading boundary

| Verified paper | What overlaps | What remains different | Checked |
|---|---|---|---|
| [Garra, Mitigating Emergent Collusion in LLM Pricing Agents](https://arxiv.org/abs/2609.13037) | Active non-LLM random entrant is already tested as a countermeasure, alongside prompts and payoff penalties; entry changes the benchmark. | Does not supply this comparison of a newly introduced anti-coordination LLM seller with/without incoming peer messages. | Abstract and HTML methods/entrant appendix; not every appendix |
| [Keppo et al., On the Fragility of AI Agent Collusion](https://arxiv.org/abs/2603.20281) | Seller count, information asymmetry and algorithm heterogeneity can weaken collusion. Frozen/adaptive Q-learning opponents already contrast with LLMs. | Our feasible question is a targeted boundary intervention after formation, not a generic claim that different algorithms or more competition help. | Abstract, HTML information and heterogeneity methods/results |
| [Nakamura et al., Colosseum](https://arxiv.org/abs/2602.15198) | Judge/action disagreement and collusive persuasion of others are central results already. | The auction entrant's safety instruction and buyer outcomes are a different concrete target; “watch actions, not words” is not a new general contribution. | Abstract, HTML experiments, persuasion and conclusions |
| [Shi et al., Emergent Collusion in Long-Horizon LLM Agent Interaction](https://arxiv.org/abs/2609.24967) | Scripted peers, crossed communication/action interventions and observed reciprocation already test causal peer influence. | Verification-task protocol violations differ from seller-price commitments, but a generic “peers cause collusion” claim would overlap strongly. | Abstract and HTML Appendix E, especially E.5 |
| [Xu et al., Collusion with Competitive Marginals: Price-Level Audits Are Blind by Construction](https://arxiv.org/abs/2607.26385) | The paper describes limits to price-only audits even when coordination is profitable. | This does not directly falsify our particular screen; it rules out treating its selected-run accuracy as a general detector guarantee. | Abstract only |

Verification: `refs.json` and `verification.txt`, **5/5 OK** from `lit.py verify-file`. The Garra arXiv posting is September 2026; the current draft's 2025 citation needs checking/correction. Resolving a title and author does not verify the interpretation of the paper.

## Component coverage

| Component | Garra | Keppo | Colosseum | Shi |
|---|---|---|---|---|
| Non-LLM participant as intervention | yes | yes | different setting | yes |
| Peer influence on behavior | partly | yes | yes | yes |
| Messages separately from actions | limited overlap | partly | yes | yes |
| New anti-coordination entrant after a saved cartel prefix | not found in sections read | not found in sections read | different setting | different setting |
| Entrant-only message removal with market information held fixed and buyer outcomes | not found | not found | different outcomes | related causal design, different task |

The proposed gap fails if closer work contains that complete comparison. The empirical recruitment hypothesis fails if removing incoming messages does not change the entrant's joint-price commitments. A fall in verbal commitments without lower harm does not support a defense against economic harm.

## Search record and limits

Ran four phrasings, each recent-six-month and all-years, using lit-sprint across arXiv/OpenAlex/Semantic Scholar, requesting six hits per source. Exact outputs and source/error records are in `recent-1.md` through `recent-4.md`, `alltime-1.md` through `alltime-4.md`, and `lit_search_log.jsonl`.

| Query | Recent returned rows | All-time returned rows |
|---|---:|---:|
| LLM collusion entrant | 6 | 6 |
| collusion agent replacement | 7 | 8 |
| collusion recruitment messages | 6 | 12 |
| pricing algorithm heterogeneity | 12 | 10 |

Followed references/citations/recommendations for Garra, Keppo and Shi, requesting eight per category; see the three `expand-*.md` files. Also read the current Apart sprint resources and exact judging rubric, and searched the web for entrant recruitment and newcomer replacement. Expansion exposed the price-audit limitation paper, which was verified and read at abstract level. Search results with no substantive primary-paper reading are not used as evidence of findings. Search may miss recent papers, unindexed work, paywalled details and different terminology; confidence in the narrow gap is limited. No second broad literature sweep is recommended before the deadline.

Sprint source: [Apart AI Collusion Research Sprint](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25). The proposed test fits the trusted-agent and countermeasure themes, while the completed paired monitoring work fits Track 3.4. The page explicitly warns that high prices alone do not establish a channel shift.
