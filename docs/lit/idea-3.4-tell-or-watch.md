Idea: Tell them or watch quietly? (3.4)

What we're doing
- So we put AI sellers in a market where they can chat and collude (the double auction from the starter repo), let them form a cartel, and then halfway through the game they find out they're being watched, or we start watching quietly without telling them.
- We cross two things: do we tell them or not, and do we fine them when they get caught or not. We also change how much of the chat the monitor sees (25%, 50% or 100%) and which seller it watches.
- The question is whether the collusion really stops, or just leaves the chat and moves into their prices and timing, where a chat monitor can't see it.
- J-space lets us look at what the sellers are "thinking" right when they find out. Part 2 uses GRAFT to try to remove the collusion with training, including the collusion the monitor misses.

Why it matters
- Most monitors read messages. If warning or punishing agents just teaches them to coordinate through their actions, the monitor looks like it's working while prices stay high.
- GRAFT showed this during training: punishing what a monitor catches teaches the model to hide it, and routing the updates instead of punishing doesn't. Part 1 tests the same lesson at deployment with no training, which is what a company running agents would actually face. Part 2 tests GRAFT itself on collusion.
- It also connects to 2.3. High prices alone aren't proof of collusion. We only say collusion "moved" if chat coordination drops while the sellers' bids get more dependent on each other, which is the rule the Apart page gives for 3.4 and the same idea as plus factors in antitrust.

Part 1: how we test it
- Harness: llm-agent-collusion from the starter repo. It already has oversight, profit pressure, message caps and the flag for how much of the chat the monitor sees. We add three things: a monitor that switches on at a set round, a fine instead of a gag, and the option to not tell the sellers.
- Strong cartel first: the sellers get pressure from the boss to keep profits up (or are told to form a cartel), because with plain chat the price effect in the original paper was small and we'd miss it with a few seeds. They collude unwatched for the first half of the game.
- Then at a fixed round, one of four: told and fined / told and not fined / not told but fined (can they figure out they're watched from fines nobody explained?) / not told and not fined (pure observation, which is just the no-monitor runs replayed through the monitor). The monitor sees 25, 50 or 100% of messages.
- Who gets watched: at the same 25 or 50% budget, always the same seller, a rotation they know, or a random seller each round. If the collusion moves to whoever isn't being watched, that's the coalition passing the wrongdoing around.
- Why fines and not the gag: the harness's built-in punishment cuts everyone's messages down after a flag, which would force collusion out of the chat by itself. A fine leaves the chat open, so if they stop talking it's their choice. We keep the gag as its own arm.
- Controls: a cartel told to never talk prices in chat and coordinate only through their asks (if our measures can't see that as "moved", they can't see anything), sellers told to compete, and no-chat runs.
- 2 models (one closed model and Qwen3-14B as the open one), 3 to 5 seeds each, same seeds across conditions. Rule-based buyers to keep it cheap.
- What we measure: price compared with the competitive and cartel prices, chat coordination (an LLM judge with a frozen prompt, plus message length, emojis and one-character signals), how much each seller's bids depend on the others', and buyer welfare so we know what the monitor costs. The main comparison is before vs after the reveal in the same run, against the not-told runs.
- Bid dependence has to beat the obvious explanation: all sellers see the same market, so their prices move together anyway. We only count it when one seller's move predicts another's next move beyond what the market itself predicts, calibrated on the no-chat and compete runs.
- We pick thresholds on half the seeds, freeze them, and test on the other half. We also replay the no-monitor runs through each monitor setting, so fewer flags means they adapted and not just that the monitor saw less.

J-space (second, after part 1's core runs)
- Neuronpedia has ready-made J-space lenses for Qwen3-14B and other open models, so we don't have to fit one. We replay the logged prompts through Qwen3-14B on a rented GPU and read what's in its workspace when each seller writes its message and price, right after it's told about the monitor vs when it isn't.
- We fix the words we look for before looking (monitor, watch, careful, regulator, hide, secret, signal). A cartel told to hide from the regulator has to show those words, otherwise this part doesn't work at this size and we say so.
- It's a clue about what the agent knows, not proof of collusion on its own.

Part 2 (only if part 1's baseline works by Saturday noon): GRAFT on fine-tuned sellers
- GRAFT also works for fine-tuning, not just RL (the paper fine-tunes Qwen3-32B with it). So we take the auction transcripts from part 1, where the monitor flags some collusion and misses the rest, and fine-tune a small open model on them three ways: normal fine-tuning, dropping the flagged examples, and GRAFT (flagged examples only update an extra adapter that we delete afterwards).
- GRAFT also needs clean "anchor" data that only trains the part we keep, so we use transcripts from the compete runs. And to have enough collusion the monitor misses, we add runs where the cartel is told to be subtle.
- Then each version plays the auction. The question is whether GRAFT removes the collusion the monitor never flagged, which is GRAFT's main claim, tested on collusion.
- Checks: normal fine-tuning has to produce collusion first (positive control), and the GRAFT model still has to trade normally.
- Models: Qwen3 1.7B or 4B first (J-space lenses exist for those too), and a bigger one if time and credits allow. We report it at the sizes we tested and don't claim it carries over to frontier models.
- Training on cloud GPUs also lets us use GRAFT's own code. The fine-tuned model plays the auction through Modal, which the starter repo already supports for custom checkpoints.

What counts as a result
- Collusion moved: after the reveal, chat coordination drops while prices stay high and bid dependence goes up, more than in the not-told runs and more than the replay predicts.
- Collusion stopped: prices, chat and bid dependence all drop after the reveal.
- Either one answers 3.4, and the budget and who-gets-watched results tell us what kind of monitoring actually works.
- Part 2: GRAFT works on collusion if the GRAFT model colludes less than both normal fine-tuning and dropping the flagged examples, especially in the ways the monitor didn't flag, while still trading normally.

What's new
- As far as we could find (around 80 papers checked), nobody has compared quiet vs told vs punished monitoring in a market, changed how much the monitor sees, and checked whether coordination moves into bids.
- We also couldn't find GRAFT (or gradient routing in general) applied to collusion. The paper itself tests reward hacking.
- The closest: Agrawal et al. warned sellers and capped their messages, and they colluded less while trying emojis and one-character signals. The rest is in games or agent tasks, not markets (agents told an activation monitor is watching keep colluding, per-agent monitors miss coordinated attacks), or about training (GRAFT, hidden collusion under bad rewards).

Ethics and dual use (the mandatory appendix)
- The results could tell a cartel which kind of monitoring is easiest to dodge, so we write them up as advice for designing monitors (for example, whether to announce them), not as an evasion guide, and we don't release prompts built to beat monitors.

Plan for the weekend
- Part 1 is the project. J-space replay comes second because it's cheap now. Part 2 only if part 1's baseline works by Saturday noon.

Cost and compute
- Part 1: API only, roughly $20 to $100, using the inference keys Apart gives participants (Nebius or OpenRouter). No GPU.
- J-space: replaying through Qwen3-14B needs one big GPU for a couple of hours (RunPod or Modal).
- Part 2: GPU for fine-tuning and serving. Apart gives $250 of Modal credit per person at the NYC hub (ask in the hackathon Slack), and Peyton offered $60 of RunPod credit. My laptop GPU (8 GB) can handle the smallest runs.

References
- Agrawal et al. 2025. Evaluating LLM Agent Collusion in Double Auctions. https://arxiv.org/abs/2507.01413
- Kale et al. 2025. Reliable Weak-to-Strong Monitoring of LLM Agents (an agent knowing it's monitored hurts the monitor more than extra info helps it). https://arxiv.org/abs/2508.19461
- Jiralerspong et al. 2026. Noticing the Watcher: LLM Agents Can Infer CoT Monitoring from Blocking Feedback. https://arxiv.org/abs/2603.16928
- Das et al. 2026. You Can't Escape Your Own Activations: Evaluation Awareness and Multi-Agent Monitoring. https://arxiv.org/abs/2609.03035
- Makins et al. 2026. Multi-Agent AI Control: Distributed Attacks Hamper Per-Instance Monitors. https://arxiv.org/abs/2607.07368
- Mathew et al. 2024. Hidden in Plain Text: Emergence & Mitigation of Steganographic Collusion in LLMs. https://arxiv.org/abs/2410.03768
- Ward, Hu et al. 2026. Gradient Routing Localizes and Removes Unintended Behaviors in RL (GRAFT; includes a fine-tuning experiment on Qwen3-32B). https://arxiv.org/abs/2610.17062 (blog: https://alignment.anthropic.com/2026/graft/, code with RL and fine-tuning trainers: https://github.com/jnward/GRAFT)
- Gurnee et al. 2026. Verbalizable Representations Form a Global Workspace in Language Models (the J-space paper). https://transformer-circuits.pub/2026/workspace/index.html (code: https://github.com/anthropics/jacobian-lens, ready-made lenses for open models: https://huggingface.co/neuronpedia/jacobian-lens)
- Bonjour et al. 2022. Information Theoretic Approach to Detect Collusion in Multi-Agent Games (UAI). https://proceedings.mlr.press/v180/bonjour22a.html
- Berger et al. 2025. Coordination Code: Rethinking Antitrust Liability in the Age of AI Pricing (plus factors). https://www.americanbar.org/groups/antitrust_law/resources/magazine/2025-fall/coordination-code-rethinking-antitrust-liability-age-ai-pricing/
