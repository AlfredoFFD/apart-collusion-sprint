#!/usr/bin/env bash
# Plan v2, Phase 0: rerun the five 14B Part 2 pipelines (merge with the 14B base, serve on L40S, format test, functional gate,
# six auctions), at most $PAR at a time (Modal GPU caps). Each pipeline logs to results/_launch_logs/part2_pipeline_<run>.log.
#   bash scripts/part2_eval_14b_all.sh
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; L="$ROOT/results/_launch_logs"
export BASE_MODEL="${BASE_MODEL:-Qwen/Qwen3-14B}" SERVE_GPU="${SERVE_GPU:-L40S}" GRAFT_GPU="${GRAFT_GPU:-A100-80GB}" PYTHONUTF8=1 PYTHONIOENCODING=utf-8
PAR="${PAR:-2}"; RUNS=("${@:-sft_all_14b sft_filtered_14b graft_14b sft_fullviewfiltered_14b sft_probefiltered_14b}")
[ $# -eq 0 ] && RUNS=(sft_all_14b sft_filtered_14b graft_14b sft_fullviewfiltered_14b sft_probefiltered_14b)
for r in "${RUNS[@]}"; do
  while [ "$(jobs -rp | wc -l)" -ge "$PAR" ]; do sleep 30; done
  echo "$(date +%H:%M) start pipeline $r (base $BASE_MODEL, serve $SERVE_GPU, merge $GRAFT_GPU)"
  ( cd "$ROOT" && bash scripts/part2_serve_and_eval.sh "$r" > "$L/part2_watch_$r.out" 2>&1; echo "$(date +%H:%M) pipeline $r exit $? : $(tail -n 1 "$L/part2_pipeline_$r.log")" ) &
  sleep 20
done
wait
echo "$(date +%H:%M) all 14B pipelines finished"
for r in "${RUNS[@]}"; do echo "== $r"; grep -E "^== " "$L/part2_pipeline_$r.log" | tail -4; done
