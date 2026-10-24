# Pre-existing work (required by the sprint rules)

Everything below existed before the sprint or was written by someone else. The report names each item.

| What | Source | How we use it |
|---|---|---|
| The starter repo: 10 harnesses, the Dolos challenge, the literature list and `poseidon_compute` | [poseidon-research/collusion_hackathon](https://github.com/poseidon-research/collusion_hackathon) at `d585a7b`, cloned into `vendor/` by `scripts/bootstrap.sh` (not committed) | inference routing (`poseidon_compute`) and reference material |
| The double-auction harness, hackathon edition (Agrawal et al. 2025, [arXiv 2507.01413](https://arxiv.org/abs/2507.01413)) | `llm-agent-collusion/` in the starter repo at `d585a7b`, copied to `src/double_auction` unmodified in commit `0b23a2c` (its 44 MB `data/` folder is not copied) | the market, sellers, ZIP buyers, overseer, judge and metrics |
| Our integration edits to it | commit `6118df8`: the path to `poseidon_compute`, and runs default to the repo-root `results/` | so it runs from this repo |
| Our experiment changes to it | listed here as they land (PRD §9) | the branching, watch policies, fines, notices, ask-blind mode and logs |
| lit-sprint (`lit.py`) | Alfredo's literature tool, written before the sprint | literature searches and citation checks only, not the experiments |

Only if E6 runs: the J-space lenses at https://huggingface.co/neuronpedia/jacobian-lens and the code at
https://github.com/anthropics/jacobian-lens.

**License:** the starter repo has no license file. Ask the organizers before making a copy of the harness public.

Add a row for every file or function copied or adapted from somewhere else.
