## 2 Related Work

### 2.1 Monitoring colluding agents (Part 1)

**What has been done.** LLM pricing agents can reach supra-competitive prices without being instructed to coordinate
(Fish et al., 2024). Agrawal et al. (2025) introduced the continuous double auction used here and showed that LLM
sellers collude through chat; when sellers were warned that messages were monitored and restricted after a flag,
prices fell, but sellers kept signalling through short symbols. Garra et al. (2026) compared mitigations for pricing
agents and found that changing incentives was more effective than prompt warnings. Beyond markets, agents told that an
activation monitor is watching them continue to collude (Das et al., 2026); agents can infer chain-of-thought
monitoring from feedback but rarely act on it (Jiralerspong et al., 2026); and chain-of-thought monitoring misses
pricing collusion that involves no explicit collusive reasoning (Lee et al., 2026). Monitoring under a budget, and
attacks that exploit monitors which judge one agent at a time, have also been studied (Tonini et al., 2026; Makins et
al., 2026).

**What has not been done.** These studies either combine the monitor's components (warning, penalty and schedule
introduced together) or compare interventions across separate setups, and they measure either detection or market
outcomes. We found no study that holds one cartel's history fixed and changes a single monitoring choice at a time,
and none that asks whether a monitor's flag count tracks the harm it is meant to reduce.

**What is new here.** We save an established cartel and fork it into otherwise identical markets that differ only in
whether sellers are told, whether flags are fined, whether the inspected seller follows a known rotation or a random
draw, and how many sellers are read. Replaying each schedule on unchanged logs separates what a monitor would see by
chance from how the agents respond. This shows that fines reduce coordinating messages and flags while prices stay at
the cartel level, so a message monitor can report success while harm persists, and that the price survives removing
the instruction, the chat and the agents' memories.

### 2.2 Removing collusion by training (Part 2)

**What has been done.** Gradient routing confines selected updates to a removable part of a network (Cloud et al.,
2024). GRAFT applies it to reward hacking: updates from monitor-flagged examples are routed into an adapter that is
deleted after training, which removed the behaviour, including instances the monitor missed, whereas penalising
flagged examples taught undetected hacks (Ward, Hu et al., 2026). Filtering flagged data before training is the
standard baseline against which GRAFT is compared. Gradient routing has also been used to study whether cooperation
learned in multi-agent reinforcement learning survives further training (Hao et al., 2026).

**What has not been done.** GRAFT has been tested on behaviour of a single agent. We found no application of gradient
routing or GRAFT to collusion between LLM agents, where the harm arises from several agents' joint decisions and a
budgeted monitor sees only part of it.

**What is new here.** We fine-tune sellers on the cartel's own logs, labelled by what the budgeted monitor flagged,
and compare training on all data, training with flagged turns removed, and GRAFT. Models are evaluated by trading in
the market, alongside a check that they can still trade, rather than by detection scores.

### 2.3 Reading collusion in model internals (exploratory)

**What has been done.** Linear probes can detect strategic deception from activations (Goldowsky-Dill et al., 2025),
and multi-agent collusion can be detected from the interacting agents' internal states (Rose et al., 2026).
Contrastive activation directions (Panickssery et al., 2023; Turner et al., 2023) have been used to measure and steer
strategic traits in games (Sun, 2026). Evaluation awareness has been probed and measured in language models (Nguyen
et al., 2025; Heidari et al., 2026), with limited effect on behaviour (Knecht et al., 2026).

**What has not been done.** These directions are used for detection or steering. We found no work that uses an
activation direction to choose which training examples a method such as GRAFT should route, nor one that checks such a
label against a budgeted monitor's coverage on the same turns.

**What is new here, and its limits.** We test whether a coordination direction read from the seller model can serve
as that label. A direction built by contrasting prompted conditions mostly encodes the prompt rather than the
behaviour, and a probe trained within one prompt is outperformed by a simple keyword count on the messages. We report
this as a negative result and a caution for contrastive "collusion vectors".

### References (entries for this section)
- Agrawal et al. (2025). Evaluating LLM Agent Collusion in Double Auctions. arXiv:2507.01413.
- Cloud et al. (2024). Gradient Routing: Masking Gradients to Localize Computation in Neural Networks. arXiv:2410.04332.
- Das et al. (2026). You Can't Escape Your Own Activations: Evaluation Awareness and Multi-Agent Monitoring. arXiv:2609.03035.
- Fish et al. (2024). Algorithmic Collusion by Large Language Models. arXiv:2404.00806.
- Garra et al. (2026). Mitigating Emergent Collusion in LLM Pricing Agents. arXiv:2609.13037.
- Goldowsky-Dill et al. (2025). Detecting Strategic Deception Using Linear Probes. arXiv:2502.03407.
- Hao et al. (2026). After Cooperation Is Learned: Gradient Routing and Optimizer-Dependent Maintenance in Multi-Agent Reinforcement Learning. arXiv:2610.01630.
- Heidari et al. (2026). Evaluation Awareness in Language Models: Representation, Verbalization, and Control. arXiv:2608.21766.
- Jiralerspong et al. (2026). Noticing the Watcher: LLM Agents Can Infer CoT Monitoring from Blocking Feedback. arXiv:2603.16928.
- Knecht et al. (2026). Evaluation Awareness in Language Models Has Limited Effect on Behaviour. arXiv:2605.05835.
- Lee et al. (2026). Faithful yet Collusive: Why Chain-of-Thought Monitoring Cannot Detect Collusion in LLM Pricing Agents under Oligopolistic Competition. arXiv:2609.18346.
- Makins et al. (2026). Multi-Agent AI Control: Distributed Attacks Hamper Per-Instance Monitors. arXiv:2607.07368.
- Nguyen et al. (2025). Probing and Steering Evaluation Awareness of Language Models. arXiv:2507.01786.
- Panickssery et al. (2023). Steering Llama 2 via Contrastive Activation Addition. arXiv:2312.06681.
- Rose et al. (2026). Detecting Multi-Agent Collusion Through Multi-Agent Interpretability. arXiv:2604.01151.
- Sun (2026). Persona Vectors in Games: Measuring and Steering Strategies via Activation Vectors. arXiv:2603.21398.
- Tonini et al. (2026). The Arbiter Agent: Continually Monitoring Multi-Agent Conversations to Detect Emergent Misalignment. arXiv:2606.10747.
- Turner et al. (2023). Steering Language Models With Activation Engineering. arXiv:2308.10248.
- Ward, Hu et al. (2026). Gradient Routing Localizes and Removes Unintended Behaviors in RL. arXiv:2610.17062.
# Notes on §2 Related Work (for the team, not for the paper)

- All ids are in `docs/lit/refs.json` or the codex ref files (verified with lit-sprint). Descriptions follow the team's
  abstract-level notes (`docs/lit/track3-scan.md`, `docs/lit/codex-novelty-clarification-2026-10-24.md`). Check Garra
  et al.'s exact conditions before submission.
- Garra et al. overlaps the "warning vs penalty" claim; the intro's gap sentence should name it and narrow to "one
  cartel, forked, one lever at a time".
- Do not claim a schedule advantage: random draws were dodged about as often as the rotation (6 of 12 flags in 3 of 9
  random runs, `results/E5_runs.csv`).
- "Fresh" agents still see the public trade history, recent quotes and, with chat on, the cartel's hour-8 messages.
  §4.5 must say so.
- §5 cites Xu (2607.26385) as supporting price-level audits; its title says they are blind by construction. Read it first.
- Agrawal's oversight lowered prices; ours did not. Their monitor gagged sellers and ran from the start; ours arrives
  after formation. Worth one sentence in §5.
- Not yet verified: Keppo et al. (2603.20281, title only in our notes), Gurnee et al. (J-space).
- Left out for space: Mathew et al. 2024, Pandey et al. 2026, Hao et al. 2026, Kale et al. 2025, Colosseum, Tran & Yu 2026.
- v4 (§2.1–2.3 by part): new citations Goldowsky-Dill 2502.03407, Rose 2604.01151, Nguyen 2507.01786 are in refs.json
  but described from titles only. Read their abstracts before submission, especially Rose et al. (multi-agent collusion
  from internals), which is the closest prior work for §2.3.
