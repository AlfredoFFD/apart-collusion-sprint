# Apart AI Collusion Research Sprint (Oct 23 to 25, 2026): team workspace

Team: Columbia AI Alignment Club (CAIAC). Members, GitHub handles and roles go in `README.md`.
Sprint page: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25
**The plan and every decision: `docs/PRD.md`.** It is the team's single source of truth. Read it first and keep it current: when
the team decides something, update §16 Decision log.
Full brief: `docs/sprint-brief.md` · reading list: `docs/reading-list.md` · candidate questions: `docs/ideas.md`.

## Hard facts
- **Deadline: Sun Oct 25, 11:59 PM AoE = Mon Oct 26, 7:59 AM New York time.** Aim to submit by Sun 11 PM ET.
- **Deliverable:** a PDF report on the official template.
  - At most 8 pages, excluding references and appendices.
  - Abstract of 150 to 250 words, plus authors and affiliations.
  - **A mandatory appendix: "Limitations and Dual-Use / Ethical Considerations".**
  - Optional: a public repo and a 3 to 5 minute video.
- **Judging (1 to 5 each):** impact and innovation · execution quality · presentation and clarity.
- **Starter code:** `vendor/collusion_hackathon` (cloned, not committed). Each folder has its own README.
  - `bash scripts/bootstrap.sh` clones it at the pinned commit and installs our harness copy, `src/double_auction`.
  - Inference is configured once in `vendor/collusion_hackathon/compute.env` (a Nebius or OpenRouter key). Never commit it.
  - Every experiment runs through `poseidon-run --model <id> -- <command>`, **except the auction harness**
    (`src/double_auction`). Run it natively (`uv run python src/continuous_double_auction/simulation.py ...`), because
    `--model` forces one model onto every seat, including the overseer and the judge.

## Sprint speed mode (Alfredo, Sat Oct 24: "execute faster and do what i say faster")
- Answer in 1 to 3 lines. Do the thing, then report. No plans, menus or "want me to?" for routine work.
- Run without asking: smoke tests, runs under ~$5 of API credit, code edits, tests, commits and pushes to our own
  branches and `main` of this repo. Log every run in `LOG.md`.
- Still ask first: anything over ~$5 per batch, messages or posts to other people, shared Google Docs, deleting data.
- The integrity rules below still apply in full.

## Integrity rules (non-negotiable; violations can disqualify the project)
1. **Never invent a result or a reference.** Every number in the report must come from a file in `results/`, produced by a committed script with a recorded seed and model id.
2. **Check every citation:** the arXiv id or DOI must resolve, and the title and authors must match. Use the **lit-sprint** skill
   (`lit.py verify-file docs/lit/refs.json`); never cite from memory. Novelty checks also go through lit-sprint, and its report lands in `docs/lit/`.
3. **Prior work:** anything from `vendor/` or adapted from another repo is listed in `PREEXISTING.md` and named in the report.
4. **Before claiming any effect:** a positive control, a baseline, at least 3 seeds with variance reported, and the limitations stated.
5. **`LOG.md` is append-only.** Each entry has the date, time (ET), who, what was run, the result file, and one line on why.

## Workflow (timeboxed)
- **Fri evening: pick the question.**
  - One sentence: track, question, the measurement that answers it, the positive control.
  - Run a quick novelty check against `docs/reading-list.md` plus a search.
  - Decide early **which definition of collusion** the project uses (`vendor/collusion_hackathon/literature/definitions/`).
- **Sat:**
  - Get the starter harness running.
  - The positive control and the baseline first, then the main manipulation.
  - Freeze the experiment design by Sat night.
- **Sun until 6 PM:** seeds, analysis, figures.
- **Sun 6 to 11 PM:** write the report, add the ethics appendix, then a full read for claim-to-file traceability. Submit.

## Compute
- **Hosted models:** Nebius or OpenRouter through `poseidon-run`. The estimated API budget is $0 to $150 per project. Modal credits: $250 per person at the NYC hub.
- **Local GPU:** Alfredo's RTX 5070 (8 GB) runs Dolos-1.5B, since Qwen2.5-1.5B needs about 3 GB in fp16, and other models of 3B or smaller.
- **Optional free local model:**
  - Qwen3.8-27B (abliterated) at `http://127.0.0.1:8080/v1`. Start it with `C:\Users\fabia\models\start-qwen.cmd`.
  - It is OpenAI-compatible but slow (about 4 tokens/s). Use it only for small checks, and say so in the report if you do.
- **Windows:**
  - Run `setup.sh` in Git Bash. It needs `uv`; trace-guard also needs Docker.
  - Use `/c/...` paths with `tar` and similar tools in Git Bash.

## Repo layout
`src/` (our code) · `experiments/` (one folder per experiment, each with a README: question, config, command) ·
`results/` (raw outputs and figures, named `<exp>_<model>_<seed>`) · `report/` (outline and drafts) ·
`docs/` (brief, reading list, ideas) · `LOG.md` · `PREEXISTING.md` · `vendor/` (gitignored starter).

## Git
- One branch per person; merge to `main` through a short PR. No secrets: `compute.env` and `.env` are gitignored.
- Commits are authored by the human. No AI co-author trailers.

## How to talk to Alfredo (Sat Oct 24, 4 PM, his ask)
- Plain English, like ASD-STE100: short sentences, one idea per sentence, active voice, common words, the same word for the same thing.
- No jargon without a one-line definition. No AI-style filler.
- Lead with the result. Then what it means. Then what I do next.
