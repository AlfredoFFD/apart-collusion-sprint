# CAIAC × Apart AI Collusion Research Sprint (Oct 23 to 25, 2026)

**Focus (Track 3.4):** if AI sellers know which of them is being watched, do they move the collusion to the seller who
isn't watched, or out of the chat? And does watching a random seller instead stop that, at the same cost?
The plan and every decision: [`docs/PRD.md`](docs/PRD.md).

**Team:** @AlfredoFFD · @xxozzi · @rohandash1 · @jakeli00 (Columbia AI Alignment Club)

**Deadline:** Sun Oct 25, 11:59 PM AoE = Mon Oct 26, 7:59 AM ET. We submit by Sun 11 PM ET.

## Setup (once, about 5 minutes)
You need git and [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`). On Windows,
use Git Bash and clone into a short path such as `C:\dev`. Some files in the starter repo and in the `openai` package
have very long names, and a deep folder breaks the install.
```bash
git clone https://github.com/AlfredoFFD/apart-collusion-sprint
cd apart-collusion-sprint
bash scripts/bootstrap.sh
```
`bootstrap.sh` clones the organizers' starter repo into `vendor/` at a pinned commit, installs our copy of the auction
harness and checks that it runs. Then put a key in `vendor/collusion_hackathon/compute.env`: `NEBIUS_API_KEY` for open
models (Qwen3-14B) and/or `OPENROUTER_API_KEY` for closed ones (gpt-4.1). **Never commit that file.**

Smoke test (15 calls, a few cents):
```bash
cd src/double_auction
uv run python src/continuous_double_auction/simulation.py --rounds 5 --seller_comms_enabled --buyer_models zip --seller_models qwen/qwen3-14b --tag E0_smoke
```
Every run writes a folder to `results/` at the repo root. `--buyer_models zip` is fine for this pipeline check only:
the ZIP buyers never learn, so real runs use LLM buyers. More commands: [`experiments/README.md`](experiments/README.md).

We fixed 10 bugs in the organizers' harness (each marked `CAIAC fix` in the code). To check them (no API calls):
```bash
cd src/double_auction
uv run --with pytest pytest -q tests/test_caiac_fixes.py
```

## How we work
- **A branch per person, small PRs.** `git switch -c <name>/<topic>`, commit, `git push -u origin <name>/<topic>`,
  then open a PR into `main` and merge it once it works. Pull often: `git pull --rebase origin main`.
- **One person per file at a time.** Say in the chat which file you're editing (for example `market.py`), so two people
  never edit the same file at once.
- **Every run gets a line in [`LOG.md`](LOG.md):** date, time (ET), who, the command, the result folder, and why.
- **Results** go in `results/` and get committed. A file over 50 MB goes in a `raw_large/` subfolder, which git ignores.
- **Never commit** `compute.env`, `.env`, keys or model weights.
- **Claims** follow PRD §7 and [`CLAUDE.md`](CLAUDE.md): a positive control, a baseline, 3+ seeds, every number traced
  to a file, every citation verified.

## Where things are
| Path | What |
|---|---|
| `docs/PRD.md` | the plan and the decision log |
| `docs/lit/` | literature review, verified references and search logs ([index](docs/lit/README.md)) |
| `src/double_auction/` | our copy of the organizers' auction harness (its first commit is unmodified; our fixes are marked `CAIAC fix`, tests in `tests/`) |
| `experiments/` | how to run each experiment |
| `results/` | raw outputs and figures |
| `report/` | outline and drafts |
| `LOG.md` | append-only research log |
| `PREEXISTING.md` | everything we didn't write |
| `vendor/` | the organizers' starter repo (made by `bootstrap.sh`, not committed) |
| `docs/sprint-brief.md` | the sprint's tracks, rules, judging and resources |

## Compute
- **Inference:** Apart gives participants Nebius or OpenRouter credits (event Slack or Luma).
- **Modal:** $250 per person at the NYC hub. Ask in the hackathon Slack, then run `modal setup`.
- **RunPod:** Peyton offered a $60 code. Make a RunPod account first, then ask Peyton for it.
- Only the optional J-space step needs a GPU.

## Pre-existing work
`vendor/` is the organizers' starter repo, and `src/double_auction` starts as an unmodified copy of its
`llm-agent-collusion` harness (Agrawal et al. 2025). Neither is our work. Our bug fixes and experiment changes to the
harness, and one known upstream issue we work around (ZIP buyers that never learn), are listed in
[`PREEXISTING.md`](PREEXISTING.md).
