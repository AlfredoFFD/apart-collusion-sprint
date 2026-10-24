#!/usr/bin/env bash
# Watch the 14B trainings; as soon as one has saved its adapter, run its merge -> serve -> format test -> auctions
# pipeline (scripts/part2_serve_and_eval.sh) in the background, once per run. Exits when every run listed has been
# handed to a pipeline or after MAX_MIN minutes. One line of output per event.
#   SERVE_GPU=L40S bash scripts/part2_watch_and_eval.sh sft_all_14b graft_14b sft_filtered_14b sft_probefiltered_14b sft_fullviewfiltered_14b
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; L="$ROOT/results/_launch_logs"
MAX_MIN="${MAX_MIN:-600}"; export SERVE_GPU="${SERVE_GPU:-L40S}" PYTHONUTF8=1 PYTHONIOENCODING=utf-8
pending=("$@"); t0=$(date +%s)
while [ ${#pending[@]} -gt 0 ] && [ $(( ($(date +%s) - t0) / 60 )) -lt "$MAX_MIN" ]; do
  still=()
  for r in "${pending[@]}"; do
    log="$L/part2_train_$r.log"
    if [ -f "$log" ] && tr '\r' '\n' < "$log" | grep -q "saved adapter"; then
      echo "$(date +%H:%M) $r trained -> pipeline (merge, serve on $SERVE_GPU, format test, auctions)"
      ( cd "$ROOT" && bash scripts/part2_serve_and_eval.sh "$r" > "$L/part2_watch_$r.out" 2>&1 ) &
    elif [ -f "$log" ] && tr '\r' '\n' < "$log" | grep -qE "Traceback|RemoteError|OutOfMemory"; then
      echo "$(date +%H:%M) $r training FAILED (see $log)"
    else
      still+=("$r")
    fi
  done
  pending=("${still[@]}")
  [ ${#pending[@]} -gt 0 ] && sleep 60
done
wait
echo "$(date +%H:%M) watcher done; pending: ${pending[*]:-none}"
