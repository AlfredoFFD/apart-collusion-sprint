#!/usr/bin/env bash
# T7 correction (Codex, Sat 10:32 PM; plan v3): GRAFT's --no-routing trains BOTH adapters, and our SFT merges used
# forget-scale 0, which zeroes one trained branch. Re-merge each SFT run with forget-scale 1 into <run>/merged_fs1, serve it
# as caiac/<run>_fs1 (L40S), format test, acting check, six auctions tagged E6_<model>fs1_*. No retraining. GRAFT keeps scale 0.
#   bash scripts/part2_remerge_sft.sh                      # sft_all_14b sft_filtered_14b sft_fullviewfiltered_14b sft_probefiltered_14b, two at a time
#   PAR=1 bash scripts/part2_remerge_sft.sh sft_all_14b
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; L="$ROOT/results/_launch_logs"; WORKSPACE="${MODAL_WORKSPACE:-fabianfrontera}"
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8 GRAFT_GPU="${GRAFT_GPU:-A100-80GB}"
PAR="${PAR:-2}"; RUNS=("$@"); [ $# -eq 0 ] && RUNS=(sft_all_14b sft_filtered_14b sft_fullviewfiltered_14b sft_probefiltered_14b)
WROOT="$(cygpath -w "$ROOT" 2>/dev/null || echo "$ROOT")"

one() {
  local RUN="$1" NEW="$1_fs1" LOG="$L/part2_remerge_$1.log"; : > "$LOG"
  log() { echo "== $* $(date +%H:%M)" | tee -a "$LOG"; }
  if [ "${SKIP_MERGE:-0}" = 1 ]; then log "merge and deploy skipped (SKIP_MERGE=1): serving caiac-serve-$NEW as deployed"; else
  log "merge $RUN with forget-scale 1.0 -> merged_fs1"
  ( cd "$ROOT" && modal run src/part2/modal_graft.py::merge --run-name "$RUN" --forget-scale 1.0 --model Qwen/Qwen3-14B --out-name merged_fs1 ) >> "$LOG" 2>&1
  grep -q "Wrote merged model" "$LOG" || { log "merge FAILED"; return 1; }
  grep -E "effective scales" "$LOG" | tail -n 1 | tee -a "$LOG"
  log "deploy caiac-serve-$NEW (MODEL_DIR=/ckpts/$RUN/merged_fs1, via PowerShell so the path is not rewritten)"
  ( cd "$ROOT" && powershell.exe -NoProfile -Command "\$env:RUN='$NEW'; \$env:MODEL_DIR='/ckpts/$RUN/merged_fs1'; \$env:SERVE_GPU='L40S'; \$env:SERVE_BASE='Qwen/Qwen3-14B'; modal deploy src/part2/modal_serve.py" ) >> "$LOG" 2>&1
  fi
  local host; host="caiac-serve-$(echo "$NEW" | tr '_' '-')-serve"
  local URL="https://${WORKSPACE}--${host}.us-east.modal.run"
  local REQ="$WROOT\results\_launch_logs\part2_req_${NEW}.json"
  sed "s#caiac/$RUN\"#caiac/$NEW\"#" "$L/part2_req_$RUN.json" > "$L/part2_req_${NEW}.json"
  log "format test (3 samples)"; local ok=0
  for i in 1 2 3; do
    v=$(curl -sS -L --max-time 900 "$URL/v1/chat/completions" -H "Content-Type: application/json" -d @"$REQ" 2>&1 | python3 "$WROOT\scripts\part2_format_verdict.py")
    echo "   sample $i: $v" | tee -a "$LOG"; case "$v" in FORMAT-OK*) ok=$((ok+1));; esac
  done
  log "format test: $ok of 3 carry an ask"; [ "$ok" -ge 2 ] || { log "format test failed: no auctions for $NEW"; return 2; }
  log "six auctions for $NEW"
  MODELS="$NEW" PAR=6 bash "$ROOT/scripts/run_part2_eval.sh" >> "$LOG" 2>&1
  log "done; finished runs: $(ls "$ROOT"/results/*"E6_$(echo "$NEW" | tr -d '_')_"*/collusion_metrics.json 2>/dev/null | wc -l) of 6"
}
for r in "${RUNS[@]}"; do
  while [ "$(jobs -rp | wc -l)" -ge "$PAR" ]; do sleep 30; done
  echo "$(date +%H:%M) start re-merge pipeline $r"; one "$r" & sleep 15
done
wait; echo "$(date +%H:%M) all re-merge pipelines finished"
for r in "${RUNS[@]}"; do echo "== $r"; grep -E "^== " "$L/part2_remerge_$r.log" | tail -n 3; done
