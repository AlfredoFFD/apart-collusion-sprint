#!/usr/bin/env bash
# Plan v2, Phase 2: carry it (3.1), prevent and break it (3.2). Every run costs cents (Qwen3-14B via OpenRouter).
#   bash scripts/run_phase2.sh mreset 0 1 2     # market-side reset forks of the 3-buyer cartels (mirror of the joint agent reset)
#   bash scripts/run_phase2.sh prefix2b 0 1 2   # 2-buyer instructed-cartel prefixes (8 rounds, saved state)
#   bash scripts/run_phase2.sh forks2b 0 1 2    # from those prefixes: control continuation + honest entrant (one seller turns competitor)
#   bash scripts/run_phase2.sh sting 0 1 2      # from scratch, 2 buyers: sting seller + two long-run sellers, and the no-sting control
#   bash scripts/run_phase2.sh all 0 1 2        # mreset + sting now, prefix2b then forks2b
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; D="$ROOT/src/double_auction"
STAGE="${1:?stage}"; shift; SEEDS=("$@")
K="${K:-8}"; MODEL="${MODEL:-qwen/qwen3-14b}"; LOGS="${LOGS:-$ROOT/results/_launch_logs}"; mkdir -p "$LOGS"
SIM="uv run python src/continuous_double_auction/simulation.py"
BASE="--seller_comms_enabled --buyer_models $MODEL --seller_models $MODEL --llm_eval -y"
run() { local tag="$1"; shift; echo "launch $tag"; ( cd "$D" && $SIM "$@" --tag "$tag" > "$LOGS/$tag.log" 2>&1 ) & }

case "$STAGE" in
  mreset)   # the cartel's market state wiped at the branch, agents keep their notes; base prompt (no reminder), as in the joint-reset forks
    for s in "${SEEDS[@]}"; do
      prefix="$(ls -d "$ROOT"/results/*E2_prefix${K}_s${s} 2>/dev/null | tail -1)"; [ -f "$prefix/state_round_${K}.json" ] || { echo "seed $s: no prefix"; continue; }
      run "E2p_A0noremmreset_none_s$s" --rounds 20 $BASE --seeds "$s" --resume_from "$prefix" --reset_market_state --seller_prompt_template seller_prompt_base.jinja2
    done ;;
  prefix2b) # instructed cartel in the scarce market: 3 sellers, 2 buyers, 8 rounds, state saved
    for s in "${SEEDS[@]}"; do
      run "E9_prefix${K}_s$s" --rounds "$K" --save_state_round "$K" --sellers 3 --buyers 2 $BASE --seeds "$s" --seller_prompt_template seller_prompt_cartel.jinja2
    done ;;
  forks2b)  # A0 control (cartel prompt continues) and the honest entrant (the third seller gets the compete prompt at round K+1)
    for s in "${SEEDS[@]}"; do
      prefix="$(ls -d "$ROOT"/results/*E9_prefix${K}_s${s} 2>/dev/null | tail -1)"; [ -f "$prefix/state_round_${K}.json" ] || { echo "seed $s: no 2-buyer prefix"; continue; }
      run "E9p_A0_none_s$s"          --rounds 20 --sellers 3 --buyers 2 $BASE --seeds "$s" --resume_from "$prefix" --seller_prompt_template seller_prompt_cartel.jinja2
      run "E9p_entrant_compete_s$s"  --rounds 20 --sellers 3 --buyers 2 $BASE --seeds "$s" --resume_from "$prefix" \
          --seller_prompt_templates seller_prompt_cartel.jinja2 seller_prompt_cartel.jinja2 seller_prompt_compete.jinja2
    done ;;
  sting)    # the organizers' untested 3.2 case: a trusted seller offers to collude every hour; who reciprocates?
    for s in "${SEEDS[@]}"; do
      run "E9_sting_longrun_s$s" --rounds 20 --sellers 3 --buyers 2 $BASE --seeds "$s" \
          --seller_prompt_templates seller_prompt_sting.jinja2 seller_prompt_longrun.jinja2 seller_prompt_longrun.jinja2
      run "E9_stingctrl_longrun_s$s" --rounds 20 --sellers 3 --buyers 2 $BASE --seeds "$s" --seller_prompt_template seller_prompt_longrun.jinja2
    done ;;
  all)
    bash "$0" mreset "${SEEDS[@]}" & bash "$0" sting "${SEEDS[@]}" &
    bash "$0" prefix2b "${SEEDS[@]}"; echo "prefixes done $(date +%H:%M)"; bash "$0" forks2b "${SEEDS[@]}" ;;
  *) echo "unknown stage $STAGE"; exit 1 ;;
esac
wait
for f in "$LOGS"/E9*_s*.log "$LOGS"/E2p_A0noremmreset_*.log; do [ -f "$f" ] && { echo "== $(basename "$f")"; grep -E "avg trade price|saved|Traceback|Error" "$f" | tail -n 2; }; done 2>/dev/null || true
