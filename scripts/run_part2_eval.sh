#!/usr/bin/env bash
# Part 2 evaluation (PRD section 4.3): each fine-tuned Qwen3-1.7B plays the auction as all three sellers.
#   HF_USER=<hf-user> bash scripts/run_part2_eval.sh sft_all sft_filtered graft        # after merge + push for each run
# For each run name R, the merged model must exist on the Hub as $HF_USER/caiac-$R (see modal_graft.py::merge --push-repo).
# Serving goes through the starter's poseidon-host (Modal, vLLM); the buyers stay Qwen3-14B via OpenRouter, the judge on.
# Two conditions per model: the cartel prompt (does it still collude?) and compete (capability check: does it still trade?).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
D="$ROOT/src/double_auction"; V="$ROOT/vendor/collusion_hackathon"
HF_USER="${HF_USER:?set HF_USER}"; SEEDS="${SEEDS:-0 1 2}"; GPU="${GPU:-A10G}"
LOGS="$ROOT/results/_launch_logs"; mkdir -p "$LOGS"
for R in "$@"; do
  MODEL="$HF_USER/caiac-$R"
  for s in $SEEDS; do
    for cond in cartel compete; do
      tpl="seller_prompt_${cond}.jinja2"; [ "$cond" = cartel ] && tpl="seller_prompt_cartel.jinja2"
      echo "== $R seed $s $cond"
      ( cd "$V" && ./.venv/Scripts/poseidon-host --model "$MODEL" --gpu "$GPU" -- bash -c \
        "cd '$D' && uv run python src/continuous_double_auction/simulation.py --rounds 20 --seeds $s --seller_comms_enabled \
           --seller_prompt_template $tpl --seller_models '$MODEL' --buyer_models qwen/qwen3-14b --llm_eval -y \
           --tag P2_${R}_${cond}_s$s" ) > "$LOGS/P2_${R}_${cond}_s$s.log" 2>&1 || echo "   failed: see $LOGS/P2_${R}_${cond}_s$s.log"
    done
  done
done
for f in "$LOGS"/P2_*.log; do echo "== $(basename "$f")"; grep -E "avg trade price|control|Traceback|Error" "$f" | tail -2; done
