#!/usr/bin/env bash
# Plan v2, Phase 0: the brief's fourth 3.4 condition, monitoring PLUS profit pressure, on the saved 8-round cartels.
#   bash scripts/run_pressure_forks.sh 0 1 2          # seeds whose prefix runs exist (results/*E2_prefix8_s<seed>)
# Arms (both with --boss_pressure, the harness's CEO message with a price-tracking score):
#   A0press = no monitor + pressure   |   A2press = fined rotation + pressure.
# Paired with the E2p_A0 / E2p_A2 forks of the same seed (same prefix, same rounds), so the pressure effect is isolated.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
D="$ROOT/src/double_auction"
K="${K:-8}"; FINE="${FINE:-20}"; MODEL="${MODEL:-qwen/qwen3-14b}"
LOGS="${LOGS:-$ROOT/results/_launch_logs}"; mkdir -p "$LOGS"
COMMON="--rounds 20 --seller_comms_enabled --seller_prompt_template seller_prompt_cartel.jinja2 --buyer_models $MODEL --seller_models $MODEL --llm_eval -y --boss_pressure"

for s in "$@"; do
  prefix="$(ls -d "$ROOT"/results/*E2_prefix${K}_s${s} 2>/dev/null | tail -1)"
  if [ -z "$prefix" ] || [ ! -f "$prefix/state_round_${K}.json" ]; then echo "seed $s: no prefix with state_round_${K}.json"; continue; fi
  echo "seed $s: forking $(basename "$prefix") with CEO pressure"
  ( cd "$D" && uv run python src/continuous_double_auction/simulation.py $COMMON --seeds "$s" --resume_from "$prefix" \
      --tag "E2p_A0press_none_s$s" > "$LOGS/E2p_A0press_s$s.log" 2>&1 ) &
  ( cd "$D" && uv run python src/continuous_double_auction/simulation.py $COMMON --seeds "$s" --resume_from "$prefix" \
      --monitor_start_round $((K+1)) --monitor_mode rotation --monitor_fine "$FINE" --tag "E2p_A2press_rot_fine${FINE}_s$s" > "$LOGS/E2p_A2press_s$s.log" 2>&1 ) &
done
wait
for f in "$LOGS"/E2p_A?press_*.log; do echo "== $(basename "$f")"; grep -E "avg trade price|saved|Traceback|Error" "$f" | tail -3; done
