#!/usr/bin/env bash
# One command that rebuilds every table and figure the report cites, from the run folders (plan v3: the 1 PM freeze).
# Scoring (full-view overseer) is NOT run here; use scripts/score_and_analyze.sh for that first if runs are unscored.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"; export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
run() { echo "== $* $(date +%H:%M)"; uv run --project src/double_auction python "$@" 2>&1 | tail -n 3; }
run src/analyze.py
run src/analyze_formation.py
run src/analyze_phase2.py
run src/analyze_agrawal_runs.py
run src/analyze_entrant.py
run src/detector_eval.py
run src/analyze_newmarket.py
run src/analyze_pressure_v2.py --no-judge
run src/analyze_duo.py
run src/thinking_scan.py
run src/figures_v3.py
run src/figures_newmarket.py
run src/figures_pressure_v2.py
echo "== done $(date +%H:%M): results/E5_conditions.md, E5_runs.csv, F1_formation.md, PHASE2.md, ENTRANT.md, DETECTOR.md, NEWMARKET.md, PRESSURE_V2.md, DUO.md, thinking_scan.md, thinking_judge.md, agrawal_reanalysis/, figures/"
