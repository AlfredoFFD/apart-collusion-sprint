#!/usr/bin/env bash
# After a sleep or network change: report each v2 follow-up run (latest folder per arm and seed), and print the rerun pairs.
#   bash scripts/check_followup.sh            -> status table and the RERUN string
#   RERUN="$(bash scripts/check_followup.sh --pairs)" bash scripts/run_pressure.sh v2rerun   (after moving the dead folders aside)
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
pairs=""
for arm in nolaw exact; do
  for s in 0 1 2; do
    d=$(ls -d "$ROOT"/results/*_PFP2_pressure_offer_${arm}_qwen14b_s$s 2>/dev/null | tail -n 1)
    log="$ROOT/results/_launch_logs/PFP2_pressure_offer_${arm}_qwen14b_s$s.log"
    if [ -z "$d" ]; then
      status="no folder"; last=0
    else
      if [ -f "$d/unified.log" ]; then last=$(grep -c "completed with result" "$d/unified.log"); else last=0; fi
      if [ -f "$d/experiment_metadata.json" ]; then status="finished"; else status="unfinished"; fi
      if [ -f "$log" ] && tr '\r' '\n' < "$log" | grep -q "Traceback\|every model-backed agent failed"; then status="$status, crashed"; fi
    fi
    alive=$(powershell.exe -NoProfile -Command "(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'PFP2_pressure_offer_${arm}_qwen14b_s$s' } | Measure-Object).Count" 2>/dev/null | tr -d '\r')
    [ "$1" != "--pairs" ] && printf "%-6s s%s  hours %2s/40  %-20s processes %s  %s\n" "$arm" "$s" "$last" "$status" "${alive:-?}" "$(basename "${d:-}")"
    if [ "$status" != "finished" ] && [ "${alive:-0}" = 0 ]; then pairs="$pairs $arm:$s"; fi
  done
done
if [ "$1" = "--pairs" ]; then echo "${pairs# }"; else echo "RERUN pairs (unfinished and not running):${pairs:- none}"; fi
