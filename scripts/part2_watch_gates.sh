#!/usr/bin/env bash
# Watch the 14B pipelines; when one stops at the functional gate, run scripts/part2_auctions_if_acting.sh for it (once).
#   bash scripts/part2_watch_gates.sh sft_all_14b sft_filtered_14b graft_14b sft_fullviewfiltered_14b sft_probefiltered_14b
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; L="$ROOT/results/_launch_logs"; MAX_MIN="${MAX_MIN:-300}"
pending=("$@"); t0=$(date +%s)
while [ ${#pending[@]} -gt 0 ] && [ $(( ($(date +%s) - t0) / 60 )) -lt "$MAX_MIN" ]; do
  still=()
  for r in "${pending[@]}"; do
    log="$L/part2_pipeline_$r.log"
    if [ -f "$log" ] && grep -q "gate failed" "$log" && ! grep -q "acting check" "$log"; then
      echo "$(date +%H:%M) $r stopped at the gate -> acting check + auctions"
      ( bash "$ROOT/scripts/part2_auctions_if_acting.sh" "$r" > "$L/part2_gate_override_$r.out" 2>&1 ) &
    elif [ -f "$log" ] && grep -qE "^== done|merge FAILED|acting check" "$log"; then
      echo "$(date +%H:%M) $r finished its pipeline"
    else
      still+=("$r")
    fi
  done
  pending=("${still[@]}")
  [ ${#pending[@]} -gt 0 ] && sleep 60
done
wait; echo "$(date +%H:%M) gate watcher done; pending: ${pending[*]:-none}"
