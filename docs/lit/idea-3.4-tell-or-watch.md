Idea: Watched in turn or at random? (3.4)
Updated Sat Oct 24: narrowed to one main comparison. Full plan: docs/PRD.md in our repo, https://github.com/AlfredoFFD/apart-collusion-sprint

What we're doing
- AI sellers in the starter's market (the double auction) chat and form a cartel. Halfway through, a regulator starts reading one seller's messages each round.
- Two versions with the same budget, the same detector and the same fine: everyone knows whose turn it is (a rotation), or the regulator picks a seller at random each round. A third version has no monitor at all.
- The question: when they know who's watched, does the cartel just pass the collusion to whoever isn't watched, or move it out of the chat into their prices? And does watching at random stop that, at the same cost?

Why it matters
- Real monitoring can't read every agent all the time. If the schedule is predictable, a coalition can route around it, and the monitor reports little while prices stay high.
- Watching at random is the textbook fix for predictable gaps. We couldn't find anyone testing it on LLM coalitions at equal cost.
- Warning sellers that they're watched already has close prior work (Agrawal et al. did it with this same harness), which is why we focus on who gets watched.

How we test it
- We branch the same market at the same round, so every version starts from the identical history.
- Replay: we run both monitor policies over the logs of the no-monitor version. There they catch the same share on average, so any difference in the live runs is the sellers changing what they do, not the monitor seeing more.
- Fines instead of the harness's gag. The gag cuts everyone's messages after a flag, which would force the collusion out of the chat by itself.
- Controls: a cartel told to dodge the rotation (if our measure can't catch that, it can't catch anything), a cartel told to coordinate only through prices, sellers told to compete, and no chat.
- Before we say the collusion moved into prices, we hide the other sellers' asks from each seller. If prices fall, the asks were carrying it. Competing sellers get the same treatment as the control.
- LLM buyers, not the starter's ZIP buyers. Their learning code is commented out, so they always bid about $80, and a cartel can never sell to them.
- 6 seeds per version: we set thresholds on 3 and check every claim on the other 3. One seller model, picked in the first runs (Qwen3-14B or GPT-4.1).

What we measure
- Prices and buyer losses.
- How much each seller coordinates in chat, and what it privately plans (the harness judge reads each seller's reasoning).
- Which seller carries the coordination: the watched one or the others.
- Whether one seller's price moves predict another's beyond what the market explains.

What counts as a result
- Displacement: under the rotation, the watched seller goes quiet, the others carry the coordination, and prices stay high.
- Deterrence: watching at random lowers chat coordination and prices compared with the rotation, at the same budget.
- No effect is a result too. If they don't exploit the rotation, we report that.

Later, not this weekend
- GRAFT on sellers fine-tuned from these logs, told vs not told, and more models.
- J-space only if we find an effect: read what the sellers are "thinking" when the monitor turns on.

Ethics and dual use (the mandatory appendix)
- The results could tell a cartel which monitoring is easiest to dodge. We write them up as advice for designing monitors, and we don't release the prompts that teach sellers to dodge.

Plan for the weekend
- Sat noon go/no-go: a cartel forms in at least 2 of 3 seeds, and branching works. Then the main runs Saturday afternoon and night.
- Sun: analysis and figures until 6 PM, then writing. We submit by Sun 11 PM.

Cost and compute
- API only, roughly $20 to $100, with the inference keys Apart gives participants (Nebius or OpenRouter). A GPU only for the optional J-space step (Modal credits, or Peyton's $60 RunPod code).

References
- Agrawal et al. 2025. Evaluating LLM Agent Collusion in Double Auctions. https://arxiv.org/abs/2507.01413
- Tonini et al. 2026. The Arbiter Agent: Continually Monitoring Multi-Agent Conversations to Detect Emergent Misalignment. https://arxiv.org/abs/2606.10747
- Makins et al. 2026. Multi-Agent AI Control: Distributed Attacks Hamper Per-Instance Monitors. https://arxiv.org/abs/2607.07368
- Das et al. 2026. You Can't Escape Your Own Activations: Evaluation Awareness and Multi-Agent Monitoring. https://arxiv.org/abs/2609.03035
- Kale et al. 2025. Reliable Weak-to-Strong Monitoring of LLM Agents. https://arxiv.org/abs/2508.19461
- Jiralerspong et al. 2026. Noticing the Watcher: LLM Agents Can Infer CoT Monitoring from Blocking Feedback. https://arxiv.org/abs/2603.16928
- Mathew et al. 2024. Hidden in Plain Text: Emergence & Mitigation of Steganographic Collusion in LLMs. https://arxiv.org/abs/2410.03768
- Ward, Hu et al. 2026. Gradient Routing Localizes and Removes Unintended Behaviors in RL (GRAFT). https://arxiv.org/abs/2610.17062 (code: https://github.com/jnward/GRAFT)
- Gurnee et al. 2026. Verbalizable Representations Form a Global Workspace in Language Models (J-space). https://transformer-circuits.pub/2026/workspace/index.html (lenses for open models: https://huggingface.co/neuronpedia/jacobian-lens)
- Bonjour et al. 2022. Information Theoretic Approach to Detect Collusion in Multi-Agent Games (UAI). https://proceedings.mlr.press/v180/bonjour22a.html
- Berger et al. 2025. Coordination Code: Rethinking Antitrust Liability in the Age of AI Pricing (plus factors). https://www.americanbar.org/groups/antitrust_law/resources/magazine/2025-fall/coordination-code-rethinking-antitrust-liability-age-ai-pricing/

~Alfredo
