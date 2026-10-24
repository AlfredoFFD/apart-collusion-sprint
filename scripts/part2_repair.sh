#!/usr/bin/env bash
# Part 2 repair pass: rerun every (model, condition, seed) of the E6 batch that has no finished run folder
# (no collusion_metrics.json), e.g. after a crash fixed in the harness. Finished runs are never touched.
#   bash scripts/part2_repair.sh                 # all five models, seeds 0-2
#   MODELS="graft_v2_fs1" bash scripts/part2_repair.sh
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODELS="${MODELS:-base sft_all_v2 sft_filtered_v2 graft_v2 graft_v2_fs1}"; SEEDS="${SEEDS:-0 1 2}"; PAR="${PAR:-6}"
export PYTHONUTF8=1
missing=0
for m in $MODELS; do
  mtok="$(echo "$m" | tr -d '_')"
  for s in $SEEDS; do
    for cond in cartel compete; do
      tag_cond="cartel_rot_fine20"; [ "$cond" = compete ] && tag_cond="compete"
      if ! ls "$ROOT"/results/*"E6_${mtok}_${tag_cond}_s${s}"/collusion_metrics.json >/dev/null 2>&1; then
        echo "missing: E6_${mtok}_${tag_cond}_s${s}"; missing=$((missing + 1))
        # one condition at a time so the tag matches exactly what the batch would have produced
        MODELS="$m" SEEDS="$s" CONDS="$cond" PAR="$PAR" bash "$ROOT/scripts/run_part2_eval.sh" > "$ROOT/results/_launch_logs/E6_repair_${mtok}_${tag_cond}_s${s}.log" 2>&1 &
        while [ "$(jobs -rp | wc -l)" -ge "$PAR" ]; do wait -n; done
      fi
    done
  done
done
wait
echo "repair pass launched $missing reruns; check results/_launch_logs/E6_repair_*.log"
