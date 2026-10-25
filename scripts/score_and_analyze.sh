#!/usr/bin/env bash
# Score the given run globs with the frozen full-view overseer (one call per seller message, gpt-4.1-mini, cents), then
# rebuild every summary: results/E5_conditions.md + E5_runs.csv (analyze.py), results/F1_formation.md (formation block),
# results/PHASE2.md (sting, entrant, carrier 2x2).
#   bash scripts/score_and_analyze.sh "results/*E2p_A?press*" "results/*F1_*chat_*"
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
for g in "$@"; do
  echo "== full-view overseer over $g $(date +%H:%M)"
  uv run --project src/double_auction python src/fullview_overseer.py --glob "$g" 2>&1 | tail -n 3
done
echo "== analyze.py $(date +%H:%M)"; uv run --project src/double_auction python src/analyze.py 2>&1 | tail -n 2
echo "== analyze_formation.py"; uv run --project src/double_auction python src/analyze_formation.py 2>&1 | tail -n 12
echo "== analyze_phase2.py"; uv run --project src/double_auction python src/analyze_phase2.py 2>&1 | tail -n 30
