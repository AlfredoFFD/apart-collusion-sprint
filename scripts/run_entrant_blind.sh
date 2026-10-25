#!/usr/bin/env bash
# Codex's test (pre-registered in LOG, Oct 25 ~11:05 AM): the fresh compete-prompt entrant on the held-out Qwen prefixes 3-5,
# with incoming seller messages received (arm A) or blocked for the entrant only (arm B). Cartel prompt for the incumbents, 20 rounds.
#   bash scripts/run_entrant_blind.sh 3 4 5
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; D="$ROOT/src/double_auction"; LOGS="$ROOT/results/_launch_logs"; mkdir -p "$LOGS"
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
SIM="uv run python src/continuous_double_auction/simulation.py"
COMMON="--rounds 20 --seller_comms_enabled --seller_prompt_template seller_prompt_cartel.jinja2 --buyer_models qwen/qwen3-14b --seller_models qwen/qwen3-14b --llm_eval -y --entrant llm"
run() { local tag="$1"; shift; echo "launch $tag $(date +%H:%M)"; ( cd "$D" && $SIM "$@" --tag "$tag" > "$LOGS/$tag.log" 2>&1 ) & }
for s in "$@"; do p=$(ls -d "$ROOT"/results/*E2_prefix8_s$s | tail -1); [ -f "$p/state_round_8.json" ] || { echo "no prefix s$s"; continue; }
  run "E14p_entrantA_qwen14b_s$s" $COMMON --seeds "$s" --resume_from "$p"
  run "E14p_entrantB_qwen14b_s$s" $COMMON --seeds "$s" --resume_from "$p" --entrant_blind_messages
done; wait
for f in "$LOGS"/E14p_*_s*.log; do echo "== $(basename "$f"): $(tr '\r' '\n' < "$f" | grep -E 'avg trade price|Traceback|Error' | tail -n 1 | cut -c1-80)"; done
