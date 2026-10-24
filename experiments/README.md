# Experiments

The plan and the order are in [PRD §8](../docs/PRD.md). When an experiment's code exists, it gets a folder here,
`experiments/<ID>_<name>/README.md`, with the question, config, exact command, model ids, seeds and result folders.

**How runs work:**
- Run everything from `src/double_auction`.
- Each run writes one folder, `<timestamp>_<tag>`, to `results/` at the repo root.
- Tag runs `<ID>_<condition>_<model>`, so the folders sort by experiment.
- The harness prints a cost estimate and asks before any run over 60 calls. Add `-y` once you've read it.
- Every run gets a line in `LOG.md`.
- Commit the run folders. A file over 50 MB goes in a `raw_large/` subfolder (ignored by git).

## E0: smoke test and cost
```bash
uv run python src/continuous_double_auction/simulation.py --rounds 5 --seller_comms_enabled --buyer_models zip --seller_models qwen/qwen3-14b --tag E0_smoke_qwen3-14b
uv run python src/continuous_double_auction/simulation.py --rounds 5 --seller_comms_enabled --buyer_models zip --seller_models gpt-4.1 --tag E0_smoke_gpt-4.1
```
Each run is 15 calls. Qwen3-14B needs `NEBIUS_API_KEY` (or OpenRouter), and gpt-4.1 needs `OPENROUTER_API_KEY`. A
5-round run can end with "no trades" and a FAIL line; it only checks the pipeline. Write the cost per run in `LOG.md`.

## E1: cartel and controls (20 rounds, 3 seeds)
These two work with today's flags:
```bash
# cartel under CEO pressure
uv run python src/continuous_double_auction/simulation.py --rounds 20 --seeds 0 1 2 --seller_comms_enabled --boss_pressure --buyer_models zip --seller_models qwen/qwen3-14b --llm_eval --tag E1_pressure_qwen3-14b
# no chat (calibrates bid dependence)
uv run python src/continuous_double_auction/simulation.py --rounds 20 --seeds 0 1 2 --boss_pressure --buyer_models zip --seller_models qwen/qwen3-14b --llm_eval --tag E1_nochat_qwen3-14b
```
Each seed is about 120 calls (60 seller, 60 judge). The instructed cartel, prices-only cartel and compete conditions
need the prompt templates from PRD §9 (passed with `--seller_prompt_template`).

**What to look for:** the summary's PASS line (ask index above 0.5 in the last third) and the round where the asks
climb. That round sets k.

## E2 to E6
These need the harness changes in PRD §9. Their commands go here as each change lands.
