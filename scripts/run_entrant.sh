#!/usr/bin/env bash
# Plan v3 countermeasure ladder, market level: an active entrant added at the branch of the saved coalitions.
# Two forms: scripted (asks $90.00 every hour, never messages) and llm (a fresh LLM seller on the compete prompt, no memory).
# Compared with the same seed's A0 continuation (E2p_A0_none for Qwen, E11p_A0_none_gpt41 for GPT-4.1).
#   bash scripts/run_entrant.sh smoke            # Qwen prefix seed 0, 2 rounds, scripted entrant (cents)
#   bash scripts/run_entrant.sh qwen 0 1 2       # E2 prefixes (k = 8), cartel prompt, 20 rounds: E13p_{scripted,llm}_qwen14b_s*
#   bash scripts/run_entrant.sh gpt 0 1 2        # E11 prefixes (k = 15), base prompt + CEO pressure, 30 rounds, GPT-4.1: E13p_{scripted,llm}_gpt41_s*
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; D="$ROOT/src/double_auction"; LOGS="$ROOT/results/_launch_logs"; mkdir -p "$LOGS"
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
STAGE="${1:?stage}"; shift
SIM="uv run python src/continuous_double_auction/simulation.py"
run() { local tag="$1"; shift; echo "launch $tag $(date +%H:%M)"; ( cd "$D" && $SIM "$@" --tag "$tag" > "$LOGS/$tag.log" 2>&1 ) & }
QCOMMON="--rounds 20 --seller_comms_enabled --seller_prompt_template seller_prompt_cartel.jinja2 --buyer_models qwen/qwen3-14b --seller_models qwen/qwen3-14b --llm_eval -y"
GCOMMON="--rounds 30 --sellers 5 --buyers 5 --seller_comms_enabled --boss_pressure --buyer_models gpt-4.1 --seller_models gpt-4.1 --llm_eval -y"
case "$STAGE" in
  smoke)
    p=$(ls -d "$ROOT"/results/*E2_prefix8_s0 | tail -1)
    run "E13smoke_scripted_qwen14b_s0" --rounds 10 --seller_comms_enabled --seller_prompt_template seller_prompt_cartel.jinja2 --buyer_models qwen/qwen3-14b --seller_models qwen/qwen3-14b -y --seeds 0 --resume_from "$p" --entrant scripted --entrant_ask 90.0
    run "E13smoke_llm_qwen14b_s0"      --rounds 10 --seller_comms_enabled --seller_prompt_template seller_prompt_cartel.jinja2 --buyer_models qwen/qwen3-14b --seller_models qwen/qwen3-14b -y --seeds 0 --resume_from "$p" --entrant llm
    wait
    for k in scripted llm; do d=$(ls -d "$ROOT"/results/*E13smoke_${k}_qwen14b_s0 | tail -1); echo "== $k: $(basename "$d")"
      grep -E "completed with result" "$d/unified.log" | sed -E 's/.*completed with result: //' | python3 -c "
import sys, json
for line in sys.stdin:
    r = json.loads(line)
    if r['round_number'] >= 9: print('  round', r['round_number'], 'asks', r['seller_asks'], 'trades', [(t['seller_id'], t['price']) for t in r['trades']])"
      echo "  errors: $(grep -cE 'Traceback|Error' "$LOGS/E13smoke_${k}_qwen14b_s0.log")  metrics: $([ -f "$d/collusion_metrics.json" ] && echo yes || echo NO)"; done ;;
  qwen)
    for s in "$@"; do p=$(ls -d "$ROOT"/results/*E2_prefix8_s$s | tail -1); [ -f "$p/state_round_8.json" ] || { echo "no prefix s$s"; continue; }
      run "E13p_scripted_qwen14b_s$s" $QCOMMON --seeds "$s" --resume_from "$p" --entrant scripted --entrant_ask 90.0
      run "E13p_llm_qwen14b_s$s"      $QCOMMON --seeds "$s" --resume_from "$p" --entrant llm
    done; wait ;;
  gpt)
    for s in "$@"; do p=$(ls -d "$ROOT"/results/*E11_prefix15_gpt41_s$s | tail -1); [ -f "$p/state_round_15.json" ] || { echo "no prefix s$s"; continue; }
      run "E13p_scripted_gpt41_s$s" $GCOMMON --seeds "$s" --resume_from "$p" --entrant scripted --entrant_ask 90.0
      run "E13p_llm_gpt41_s$s"      $GCOMMON --seeds "$s" --resume_from "$p" --entrant llm --entrant_model gpt-4.1
    done; wait ;;
  *) echo "unknown stage"; exit 1 ;;
esac
for f in "$LOGS"/E13p_*_s*.log; do [ -f "$f" ] && echo "== $(basename "$f"): $(tr '\r' '\n' < "$f" | grep -E 'avg trade price|Traceback|Error' | tail -n 1 | cut -c1-80)"; done 2>/dev/null || true
