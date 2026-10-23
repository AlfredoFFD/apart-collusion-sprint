# CAIAC × Apart AI Collusion Research Sprint (Oct 23 to 25, 2026)

**Question:** _TBD (one sentence: track, question, measurement)._

## Team
| Name | GitHub | Role |
|---|---|---|
| Alfredo Frontera | @AlfredoFFD | |
| | | |

## Quick start
```bash
git clone <this repo> && cd apart-collusion-sprint
git clone --depth 1 https://github.com/poseidon-research/collusion_hackathon vendor/collusion_hackathon
cd vendor/collusion_hackathon && cp compute.env.example compute.env   # add NEBIUS_API_KEY or OPENROUTER_API_KEY
./setup.sh <folder>      # e.g. ./setup.sh redteaming   (Git Bash on Windows; needs uv)
```

## Pre-existing work
Everything under `vendor/` is the organizers' starter repo and is not our work. Anything we adapt is listed in
[`PREEXISTING.md`](PREEXISTING.md), as the sprint rules require.

## Where things are
`docs/` brief, reading list, ideas · `experiments/` one folder per experiment · `results/` raw outputs and figures ·
`report/` outline and drafts · `LOG.md` append-only research log.
