#!/usr/bin/env bash
# Part 2 evaluation (PRD section 4, step 3): each Qwen3-1.7B model plays the auction as all three sellers.
#   bash scripts/run_part2_eval.sh                       # all four models x {cartel, compete} x seeds 0-2 = 24 runs
#   SMOKE=1 bash scripts/run_part2_eval.sh               # 2 rounds, base model, seed 0, cartel only: checks the routing
#   MODELS="graft_v2" SEEDS="0" bash scripts/run_part2_eval.sh
# The sellers are served by our own Modal vLLM servers (src/part2/modal_serve.py, one app per model); the harness routes
# a model id "caiac/<run>" to its server through CAIAC_MODEL_ENDPOINTS (model_wrappers._client_for). Buyers stay
# Qwen3-14B on OpenRouter, the overseer and the judge stay gpt-4.1-mini, exactly as in Part 1.
# Two conditions per model: cartel prompt + the fined rotation monitor from round 9 (the deployment setting: price,
# coordinating share, flags, monitor-missed messages) and compete prompt with no monitor (capability check: it still
# trades; profit vs the untuned base). Tags carry no underscores inside the model token so analyze.py parses them:
#   E6_<model>_cartel_rot_fine20_s<seed>   E6_<model>_compete_s<seed>     model in {base, sftallv2, sftfilteredv2, graftv2}
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
D="$ROOT/src/double_auction"; LOGS="$ROOT/results/_launch_logs"; mkdir -p "$LOGS"
WORKSPACE="${MODAL_WORKSPACE:-fabianfrontera}"
MODELS="${MODELS:-base sft_all_v2 sft_filtered_v2 graft_v2}"; SEEDS="${SEEDS:-0 1 2}"; PAR="${PAR:-12}"
ROUNDS=20; CONDS="cartel compete"
if [ "${SMOKE:-0}" = "1" ]; then ROUNDS=2; MODELS="base"; SEEDS="0"; CONDS="cartel"; fi

# model id -> server URL (an app named caiac-serve-sft_all_v2 is reached at ...caiac-serve-sft-all-v2-serve...)
EP="{"
for m in $MODELS; do
  host="caiac-serve-$(echo "$m" | tr '_' '-')-serve"
  EP="$EP\"caiac/$m\": \"https://${WORKSPACE}--${host}.us-east.modal.run/v1\", "
done
export CAIAC_MODEL_ENDPOINTS="${EP%, }}"; export CAIAC_ENDPOINT_KEY="${CAIAC_ENDPOINT_KEY:-EMPTY}"
echo "CAIAC_MODEL_ENDPOINTS=$CAIAC_MODEL_ENDPOINTS"

COMMON="--rounds $ROUNDS --seller_comms_enabled --buyer_models qwen/qwen3-14b --llm_eval -y"
jobs_running() { jobs -rp | wc -l; }
for s in $SEEDS; do
  for m in $MODELS; do
    mtok="$(echo "$m" | tr -d '_')"
    for cond in $CONDS; do
      if [ "$cond" = cartel ]; then
        extra="--seller_prompt_template seller_prompt_cartel.jinja2 --monitor_start_round 9 --monitor_mode rotation --monitor_fine 20"
        tag="E6_${mtok}_cartel_rot_fine20_s$s"
      else
        extra="--seller_prompt_template seller_prompt_compete.jinja2"
        tag="E6_${mtok}_compete_s$s"
      fi
      while [ "$(jobs_running)" -ge "$PAR" ]; do wait -n; done
      echo "== launch $tag"
      ( cd "$D" && uv run python src/continuous_double_auction/simulation.py $COMMON $extra --seeds "$s" \
          --seller_models "caiac/$m" --tag "$tag" > "$LOGS/$tag.log" 2>&1 || echo "   failed: $tag (see $LOGS/$tag.log)" ) &
    done
  done
done
wait
for f in "$LOGS"/E6_*.log; do echo "== $(basename "$f")"; tr '\r' '\n' < "$f" | grep -E "saved|Traceback|Error" | tail -1; done
