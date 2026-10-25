# Targeted check of NotebookLM frontier proposals

2026-10-25. This is a targeted overlap/claim check, not a completed full literature review.

Verdict: selective removal of learned LLM cartel enforcement while preserving competition and reducing harm is partly covered. The exact routing comparison is open in what we searched, with low-to-moderate confidence. CURB already targets retaliation; Tran/Yu audit enforcement; GRAFT tests routing/removal. A new dataset alone is not a strong contribution.

## Reading depth this turn

| Reference | Checked | Coverage |
|---|---|---|
| 2609.28900 CODETTA | partial | Intro portions; Sections 3.1-3.4 and 9; keyword passages. 3,287-line full text/PDF downloaded; proofs, remaining experiments/appendices/figures not fully audited. |
| 2604.01151 HELIOS | partial | Intro portions; Section 6.3, conclusion, Appendix A/B passages. 3,405-line text/PDF downloaded; remainder and figures not fully audited. |
| 2606.28425 Rippin et al. | partial | Abstract/introduction and selected methods/results/mitigations/limitations, including Section 4.1 concealed implementation. 2,335-line text/PDF downloaded; no full figure audit. |
| 2610.17062 GRAFT | partial | Section 3 algorithm/optimizer/anchors/SFT variant; Section 5 setup; Section 7 failures/limitations. 1,895-line text/PDF downloaded; not all appendices/figures read. |
| 2609.20548 CURB | partial | Abstract, introduction, related work, preliminaries and selected method/result passages. 1,771-line text/PDF downloaded; proofs/figures not fully audited. |
| 2610.28787 Tran/Yu | abstract | Current primary abstract and identity; not a fresh full read of the 45-page paper. |
| 2610.01630 cooperation maintenance | abstract | Primary abstract/identity. Concerns value-gradient access, not demonstrated GRAFT collusion removal. |
| 2606.17168 RepSelect | abstract | Primary abstract/identity. NotebookLM's multi-agent-retaliation characterization was unsubstantiated. |
| 2608.02698 steganalysis | abstract | Primary abstract explicitly labels empirical results placeholders pending measurement; not measured detection success. |

Truncated terminal output is not counted as a full read. Identity checks: `verification.txt`, 9/9 OK; inputs: `refs.json`.

## Search record

Canonical lit-sprint queries and raw files:

- `collusion monitoring`, six months, n=12: `recent-collusion-monitoring.md`.
- `collusion retaliation gradient routing`, six months, n=12: `retaliation-routing-recent.md`. Relevant Tran/Yu result plus noise.
- `collusion retaliation unlearning`, all years, n=12: `retaliation-unlearning-all-years.md`. Poor recall; absence is weak evidence.
- CURB references/citations/recommendations, n=12: `curb-citation-trail.md`. Several close enforcement/market papers surfaced; not all read.

Source hit counts and timestamps are in `search-log-excerpt.jsonl`, copied from the automatic append-only search log. Additional web discovery used combinations of collusion, GRAFT, retaliation, unlearning, tools, activations, replacement and shared memory. No verified exact selective-removal experiment was found; this is not exhaustive. New discovery 2610.30582 concerns corrective transfer in untrusted monitors and was read at abstract level only, not used to prove the final gap.

## Rejected claims

- External cryptographic encoding does not automatically create internal transformer computation. Full input/prefix identity implies matching deterministic activations; public-text identity alone does not.
- HELIOS includes emergent transfer tests (6.3), with partial results.
- Tool auditing is not proven necessary/sufficient. Rippin 4.1 includes a concealed implementation missed by a monitor.
- CODETTA 9 already discusses action audits, verifiable sampling and communication perturbation.
- GRAFT has multi-turn SFT; only its RL environments are restricted to single turn.
- CURB can deploy a frozen trained policy; deployment bookkeeping does not distinguish it from GRAFT.
- One failed intervention cannot prove general impossibility. A scripted peer's fixed response cannot demonstrate behavioral deterrence.

If adopted, next literature work is full reading and figure verification of the three closest papers and newest citation-trail hits. These partial checks reject erroneous arguments and frame a candidate; they do not certify a literature-wide gap.
