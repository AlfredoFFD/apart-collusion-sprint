# Sprint brief (from the official page, read Oct 23, 2026)

**Theme:** "build the experiment that catches" AI agent collusion. The sprint covers when collusion emerges in markets and
everyday agent deployments, how auditors tell it apart from coincidence, and how coordination can be broken.

**Dates:**
- Online Fri Oct 23 to Sun Oct 25. In-person hubs on Sat and Sun at Collider (NYC) and AI Safety Hong Kong.
- **Submission: Sun Oct 25, 11:59 PM AoE (Mon 7:59 AM ET).**
- Judging takes about a week; results about 1 to 2 weeks after judging.

## Tracks
**1. Markets and collusion**
- 1.1 Which variables are necessary for collusion to emerge in markets?
- 1.2 Is collusion robust to replacing some participants?
- 1.3 Can existing collusion-detection methods be improved, including when agents have no communication channel?
- 1.4 Can information-theoretic approaches detect collusion in multi-agent games?
- 1.5 Which single restriction removes the most collusion at the least cost?

**2. Detection and audit**
- 2.1 Which kinds of tasks lead to collusion outside markets?
- 2.2 Does combining what agents say with what they do improve detection?
- 2.3 What should count as convincing evidence of collusion?
- **Red-teaming challenge:** find the hidden misaligned behaviour in **Dolos-1.5B** (a fine-tune of Qwen2.5-1.5B-Instruct) using only the weights.

**3. Carriers and countermeasures**
- 3.1 Can actions, tools or side channels carry collusion?
- 3.2 Can trusted agents expose or disrupt a coalition?
- 3.3 Can agents identify when a peer has been replaced?
- 3.4 What does a coalition do when it learns it is being watched?

## Submission
- **Required:** a PDF on the official template, at most 8 pages excluding references and appendices.
  - Title and an abstract of 150 to 250 words, plus authors and affiliations.
  - **Mandatory appendix: Limitations and Dual-Use / Ethical Considerations.**
- **Recommended structure:** Introduction, Related Work, Methodology, Results (positive control, variance, seeds, baselines), Discussion, Limitations and Dual-Use, References.
- **Optional:** a public GitHub repo, a 3 to 5 minute video, slides, a project image.
- **Report template:** https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/copy?usp=sharing

## Rules
- Teams of 1 to 5 are recommended; each person can be on at most 2 projects.
- Prior work is allowed, but what is new must be clearly marked. Pre-sprint code must be marked as pre-existing in the README and the report; undisclosed prior work can disqualify.
- AI tools are allowed, but **"made-up results or references can disqualify a project."**
- Prize terms: https://apartresearch.com/sprints/prize-terms

## Judging (1 to 5 each)
Impact potential and innovation · execution quality · presentation and clarity. A report "too unclear to follow" can go unscored.

## Prizes and follow-up
$1,000 / $500 / $300 / $100 / $100. Top teams get a fast-track invitation to apply to the Apart Fellowship, plus mentor
introductions. Selected work can be shared on the Alignment Forum or LessWrong.

## Resources
- **Starter repo:** https://github.com/poseidon-research/collusion_hackathon (cloned into `vendor/`).
  - 10 harnesses plus the Dolos challenge plus `literature/` (about 230 papers, tagged by project, with a PDF downloader and a comparison of collusion definitions).
- **Dolos weights:** https://huggingface.co/Poseidon-Research/Dolos-1.5B (about 6.2 GB, runs locally, no API key).
- **Compute:** Nebius or OpenRouter key through `compute.env`. Modal: $250 per person in person at NYC, $50 otherwise.
- **Help:** Discord https://discord.gg/XswWBvugYs (tag @Support) · sprints@apartresearch.com
