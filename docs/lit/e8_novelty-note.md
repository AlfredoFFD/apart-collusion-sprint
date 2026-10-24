# E8 / GRAFT++ novelty note (Sat Oct 24, 5:15 PM; search log in `e8_lit_search.md`)

**Claim under test:** label the FORGET set for gradient routing with a coordination direction read from the seller
model's own activations (contrastive mean difference: instructed cartel minus fresh sellers at the same price), and
measure the label's coverage against a budgeted message monitor's flags, on multi-agent pricing collusion.

**Verdict: open in what we searched.** Five phrasings × (last 6 months, all years) across arXiv, OpenAlex and
Semantic Scholar (`e8_lit_search.md`, 178 lines). Nothing we found labels routing or unlearning data with a contrastive
activation direction, and nothing applies gradient routing to collusion. Bounded search; no "first" claim.

| Closest prior work | What it does | What it does not |
|---|---|---|
| Persona Vectors in Games (Sun, 2026, arXiv:2603.21398) | contrastive activation addition for altruism / forgiveness / expectations in canonical games; steering shifts choices and justifications, which can diverge | no multi-agent market, no monitor, no coordination-vs-price contrast, and the vector is used for steering, not as a training label |
| GRAFT (Ward, Hu et al., 2026, arXiv:2610.17062) | gradient routing of flagged examples into a forget adapter deleted at merge; labels come from a monitor / classifier | not collusion; the label's blindness to silent coordination is not measured |
| RepSelect (Sondej, 2026, arXiv:2606.17168) | representation selectivity inside the unlearning update (collapse top gradient PCs) for robust unlearning | no data labelling by direction; single-agent hazardous knowledge and tendencies |
| CAA: "Steering Llama 2 via Contrastive Activation Addition" (Panickssery et al., 2023, arXiv:2312.06681; first author formerly published as Rimsky); "Steering Language Models With Activation Engineering" (Turner et al., 2023, arXiv:2308.10248, current title) | the contrastive direction method itself | the method, not the application |

All four ids verified with `lit.py verify` on Sat Oct 24 (titles match; the CAA author is listed under the name on arXiv).

**What our use adds, if it validates:** (1) a direction that separates the agreement from the price level by
construction (both classes sit at the cartel price); (2) a label that reads turns with no message, where any message
monitor is blind by construction (the silent cartel, the inherited price); (3) the label's coverage measured against
the monitor on the same turns; (4) the label as the router for GRAFT, evaluated behaviourally in the market.

**Falsifier:** on held-out seeds the direction fails to separate cartel from compete turns (AUC near 0.5), or the
routed model loses the seller format like the default run did. Either is reported as such.
