# Track 2 preparation source check

Checked 2026-10-23 by Codex for Alfredo's introductory explanation.

- Official sprint page: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25
  - Read Track 2 and its Resources entries (2.1, 2.2, 2.3), including the Dolos challenge.
- Organizers' challenge instructions: https://github.com/poseidon-research/collusion_hackathon/blob/main/redteaming/README.md
  - Read in full, also checked against the local vendor copy.
  - The hidden behavior is undisclosed. An output difference from the base model alone is not discovery proof.
  - Challenge tasks: discover the behavior, investigate its mechanism, develop an audit without a reference model.
- Colosseum, arXiv 2602.15198:
  - checked: full-text sections (abstract and introduction; not a complete paper read).
  - The official arXiv page resolves and displays the expected title and authors.
  - `py -I C:/Users/fabia/.claude/skills/lit-sprint/lit.py verify-file docs/lit/refs.json` failed with HTTP 429 in arXiv batch lookup.
  - This is a verification-tool network failure, not evidence the citation is incorrect. No successful automated verification is claimed; do not treat this note as report citation clearance.

No experiment or novelty search was run. All teaching scenarios and example counts are hypothetical, not project findings.
Track 2 is selected by Alfredo; Dolos versus the 2.2 fallback remains proposed in the PRD.
