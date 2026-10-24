#!/usr/bin/env bash
# E2, paired: fork each saved 8-round cartel prefix into the four arms (PRD section 3, step 2).
#   bash scripts/run_e2_paired.sh 0 1 2          # seeds whose prefix runs exist (results/*E2_prefix8_s<seed>)
#   FINE=20 K=8 bash scripts/run_e2_paired.sh 3 4 5
# Arms: A0 none | A1 rotation, no fine | A2 rotation + fine | A3 random + fine. All 20 rounds total, monitor from K+1.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
D="$ROOT/src/double_auction"
K="${K:-8}"; FINE="${FINE:-20}"; MODEL="${MODEL:-qwen/qwen3-14b}"
LOGS="${LOGS:-$ROOT/results/_launch_logs}"; mkdir -p "$LOGS"
COMMON="--rounds 20 --seller_comms_enabled --seller_prompt_template seller_prompt_cartel.jinja2 --buyer_models $MODEL --seller_models $MODEL --llm_eval -y"

for s in "$@"; do
  prefix="$(ls -d "$ROOT"/results/*E2_prefix${K}_s${s} 2>/dev/null | tail -1)"
  if [ -z "$prefix" ] || [ ! -f "$prefix/state_round_${K}.json" ]; then
    echo "seed $s: no prefix with state_round_${K}.json (run: simulation.py --rounds $K --save_state_round $K --tag E2_prefix${K}_s$s)"; continue
  fi
  echo "seed $s: forking $(basename "$prefix")"
  ( cd "$D" && uv run python src/continuous_double_auction/simulation.py $COMMON --seeds "$s" --resume_from "$prefix" \
      --tag "E2p_A0_none_s$s" > "$LOGS/E2p_A0_s$s.log" 2>&1 ) &
  ( cd "$D" && uv run python src/continuous_double_auction/simulation.py $COMMON --seeds "$s" --resume_from "$prefix" \
      --monitor_start_round $((K+1)) --monitor_mode rotation --monitor_fine 0     --tag "E2p_A1_rot_nofine_s$s" > "$LOGS/E2p_A1_s$s.log" 2>&1 ) &
  ( cd "$D" && uv run python src/continuous_double_auction/simulation.py $COMMON --seeds "$s" --resume_from "$prefix" \
      --monitor_start_round $((K+1)) --monitor_mode rotation --monitor_fine "$FINE" --tag "E2p_A2_rot_fine${FINE}_s$s" > "$LOGS/E2p_A2_s$s.log" 2>&1 ) &
  ( cd "$D" && uv run python src/continuous_double_auction/simulation.py $COMMON --seeds "$s" --resume_from "$prefix" \
      --monitor_start_round $((K+1)) --monitor_mode random   --monitor_fine "$FINE" --tag "E2p_A3_rand_fine${FINE}_s$s" > "$LOGS/E2p_A3_s$s.log" 2>&1 ) &
done
wait
for f in "$LOGS"/E2p_*.log; do echo "== $(basename "$f")"; grep -E "avg trade price|control|saved|Traceback" "$f" | tail -3; done
