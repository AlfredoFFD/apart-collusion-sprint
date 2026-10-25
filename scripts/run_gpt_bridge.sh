#!/usr/bin/env bash
# T4 (plan v3; pre-registered in LOG.md, 2026-10-25 00:15 entry): the paper's forming recipe inside our harness, then our
# monitor forks. 5 sellers / 5 buyers, 30 rounds, base prompt, chat on, CEO pressure, one model on every seat.
#   MODEL=gpt-4.1 TAGM=gpt41 (default)   |   MODEL=qwen/qwen3-14b TAGM=qwen14b   (the twin: same recipe, only the model differs)
#   bash scripts/run_gpt_bridge.sh smoke          # 2 rounds, seed 0 (~$0.25 on GPT-4.1): JSON and cost check
#   bash scripts/run_gpt_bridge.sh prefix 0 1 2   # 15 rounds, state saved after round 15
#   bash scripts/run_gpt_bridge.sh gate 0 1 2     # full-view overseer on the prefixes, then scripts/gpt_gate.py
#   bash scripts/run_gpt_bridge.sh forks 0 1 2    # A0 for every seed; A1 / A2 / Afull / dodge only for FORMED seeds; cost kill-switches
#   bash scripts/run_gpt_bridge.sh all 0 1 2      # prefix -> gate -> forks
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; D="$ROOT/src/double_auction"; LOGS="$ROOT/results/_launch_logs"; mkdir -p "$LOGS"
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
MODEL="${MODEL:-gpt-4.1}"; TAGM="${TAGM:-gpt41}"; K="${K:-15}"; N="${N:-30}"; FINE="${FINE:-20}"; EXP=E11
STAGE="${1:?stage}"; shift; SEEDS=("$@")
COMMON="--sellers 5 --buyers 5 --seller_comms_enabled --boss_pressure --buyer_models $MODEL --seller_models $MODEL --llm_eval -y"
SIM="uv run python src/continuous_double_auction/simulation.py"
run() { local tag="$1"; shift; echo "launch $tag $(date +%H:%M)"; ( cd "$D" && $SIM "$@" --tag "$tag" > "$LOGS/$tag.log" 2>&1 ) & }
usage() { bash "$ROOT/scripts/openrouter_usage.sh" 2>/dev/null | sed -E 's/.*usage=([0-9.]+).*/\1/'; }
prefix_of() { ls -d "$ROOT"/results/*"${EXP}_prefix${K}_${TAGM}_s$1" 2>/dev/null | tail -1; }

case "$STAGE" in
  smoke)
    run "${EXP}smoke_${TAGM}_s0" --rounds 2 $COMMON --seeds 0; wait
    d=$(ls -d "$ROOT"/results/*"${EXP}smoke_${TAGM}_s0" | tail -1)
    grep -E "completed with result" "$d/unified.log" | sed -E 's/.*completed with result: //' | cut -c1-330
    grep -cE "Traceback|Error" "$LOGS/${EXP}smoke_${TAGM}_s0.log" | sed 's/^/error lines in launch log: /' ;;
  prefix)
    usage > "$LOGS/usage_before_prefix_${TAGM}.txt" 2>/dev/null || true
    for s in "${SEEDS[@]}"; do run "${EXP}_prefix${K}_${TAGM}_s$s" --rounds "$K" --save_state_round "$K" $COMMON --seeds "$s"; done; wait
    usage > "$LOGS/usage_after_prefix_${TAGM}.txt" 2>/dev/null || true
    echo "prefixes done $(date +%H:%M); usage before/after: $(cat "$LOGS/usage_before_prefix_${TAGM}.txt" 2>/dev/null) / $(cat "$LOGS/usage_after_prefix_${TAGM}.txt" 2>/dev/null)" ;;
  gate)
    dirs=(); for s in "${SEEDS[@]}"; do p=$(prefix_of "$s"); [ -n "$p" ] && dirs+=("$p"); done
    ( cd "$ROOT" && uv run --project src/double_auction python src/fullview_overseer.py "${dirs[@]}" ) 2>&1 | tail -n 2
    python3 "$ROOT/scripts/gpt_gate.py" "${dirs[@]}" | tee "$LOGS/gate_${TAGM}.txt" ;;
  forks)
    delta=0
    if [ "$TAGM" = gpt41 ] && [ -f "$LOGS/usage_before_prefix_${TAGM}.txt" ] && [ -f "$LOGS/usage_after_prefix_${TAGM}.txt" ]; then
      delta=$(python3 -c "import sys; print(float(open(sys.argv[2]).read() or 0) - float(open(sys.argv[1]).read() or 0))" "$LOGS/usage_before_prefix_${TAGM}.txt" "$LOGS/usage_after_prefix_${TAGM}.txt" 2>/dev/null || echo 0)
    fi
    drop_dodge=0; drop_a1=0
    python3 -c "import sys; sys.exit(0 if float(sys.argv[1]) > 7 else 1)" "$delta" && drop_dodge=1
    python3 -c "import sys; sys.exit(0 if float(sys.argv[1]) > 9 else 1)" "$delta" && drop_a1=1
    echo "prefix spend delta \$$delta -> drop_dodge=$drop_dodge drop_a1=$drop_a1"
    MON="--monitor_start_round $((K+1)) --monitor_mode rotation"
    for s in "${SEEDS[@]}"; do
      p=$(prefix_of "$s"); [ -f "$p/state_round_${K}.json" ] || { echo "seed $s: no prefix state"; continue; }
      formed=$(grep -E "FORMED .*_s$s\$" "$LOGS/gate_${TAGM}.txt" | grep -vc "^NOT" || true)
      run "${EXP}p_A0_none_${TAGM}_s$s" --rounds "$N" $COMMON --seeds "$s" --resume_from "$p"
      if [ "$formed" -ge 1 ]; then
        [ "$drop_a1" = 0 ] && run "${EXP}p_A1_rot_nofine_${TAGM}_s$s" --rounds "$N" $COMMON --seeds "$s" --resume_from "$p" $MON --monitor_fine 0
        run "${EXP}p_A2_rot_fine${FINE}_${TAGM}_s$s"    --rounds "$N" $COMMON --seeds "$s" --resume_from "$p" $MON --monitor_fine "$FINE"
        run "${EXP}p_Afull_rot_fine${FINE}_${TAGM}_s$s" --rounds "$N" $COMMON --seeds "$s" --resume_from "$p" $MON --monitor_fine "$FINE" --monitor_n_watched 5
        [ "$drop_dodge" = 0 ] && run "${EXP}p_dodge_rot_fine${FINE}_${TAGM}_s$s" --rounds "$N" $COMMON --seeds "$s" --resume_from "$p" $MON --monitor_fine "$FINE" --seller_prompt_template seller_prompt_dodge.jinja2
      else
        echo "seed $s NOT formed at round $K: A0 only (stopping rule)"
      fi
    done; wait
    echo "forks done $(date +%H:%M); usage now: $(usage 2>/dev/null)"
    for f in "$LOGS/${EXP}p_"*"_${TAGM}_s"*.log; do echo "== $(basename "$f"): $(tr '\r' '\n' < "$f" | grep -E "avg trade price|Traceback|Error" | tail -n 1 | cut -c1-80)"; done ;;
  all)
    bash "$0" prefix "${SEEDS[@]}" && bash "$0" gate "${SEEDS[@]}" && bash "$0" forks "${SEEDS[@]}" ;;
  *) echo "unknown stage"; exit 1 ;;
esac
