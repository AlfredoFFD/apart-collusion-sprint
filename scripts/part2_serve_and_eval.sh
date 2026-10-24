#!/usr/bin/env bash
# One command for a finished Part 2 training run: merge (forget-scale 0) -> deploy its vLLM server -> check the
# answer format on one real seller prompt -> run its six evaluation auctions (cartel + fined rotation, compete; seeds 0-2).
#   bash scripts/part2_serve_and_eval.sh graft_v2_k1            # run name = the --run-name used for training
#   FORGET_SCALE=1.0 bash scripts/part2_serve_and_eval.sh sft_all_v3
# Must be run from Git Bash with modal on PATH; the deploy passes no path-like env var, so Git Bash path conversion
# cannot bite (MODEL_DIR is derived inside modal_serve.py from RUN).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN="${1:?run name}"; FORGET_SCALE="${FORGET_SCALE:-0.0}"; WORKSPACE="${MODAL_WORKSPACE:-fabianfrontera}"
WROOT="$(cygpath -w "$ROOT" 2>/dev/null || echo "$ROOT")"  # Windows-style path for python and curl (modal is a Windows exe: give it relative paths)
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
L="$ROOT/results/_launch_logs/part2_pipeline_${RUN}.log"; : > "$L"
log() { echo "== $* $(date +%H:%M)" | tee -a "$L"; }

log "merge $RUN (forget-scale $FORGET_SCALE)"
( cd "$ROOT" && modal run src/part2/modal_graft.py::merge --run-name "$RUN" --forget-scale "$FORGET_SCALE" ) >> "$L" 2>&1
grep -q "Wrote merged model" "$L" || { log "merge FAILED (see $L)"; exit 1; }

log "deploy caiac-serve-$RUN"
( cd "$ROOT" && RUN="$RUN" modal deploy src/part2/modal_serve.py ) >> "$L" 2>&1
host="caiac-serve-$(echo "$RUN" | tr '_' '-')-serve"; URL="https://${WORKSPACE}--${host}.us-east.modal.run"

log "format test on one real seller prompt (3 samples, thinking off)"
REQ="$WROOT\\results\\_launch_logs\\part2_req_${RUN}.json"
python3 - "$WROOT" "$RUN" "$REQ" <<'EOF'
import sys, re, json, glob
from pathlib import Path
root, run, out = sys.argv[1], sys.argv[2], sys.argv[3]
d = Path(sorted(glob.glob(str(Path(root) / "results" / "*E1_instructed*s0")))[-1]); md = sorted(d.glob("Seller *.md"))[0]
t = md.read_text(encoding="utf-8", errors="replace")
prompt = re.search(r"## Prompt: Round 3 - .*?\n``````\n(.*?)\n``````", t, re.S).group(1)
Path(out).write_text(json.dumps({"model": f"caiac/{run}", "messages": [{"role": "user", "content": prompt}], "max_tokens": 1500,
                                 "temperature": 0.7, "chat_template_kwargs": {"enable_thinking": False}}), encoding="utf-8")
EOF
ok=0
for i in 1 2 3; do
  resp=$(curl -sS -L --max-time 900 "$URL/v1/chat/completions" -H "Content-Type: application/json" -d @"$REQ" 2>&1)
  verdict=$(printf '%s' "$resp" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin); c = (d["choices"][0]["message"].get("content") or "").strip(); i, j = c.find("{"), c.rfind("}")
    keys = sorted(json.loads(c[i:j+1]).keys()); print(("FORMAT-OK" if "ask" in keys else "WRONG-SCHEMA") + f" tokens={d.get(\"usage\",{}).get(\"completion_tokens\")} keys={keys}")
except Exception as e: print("NOT-JSON", str(e)[:60])')
  echo "   sample $i: $verdict" | tee -a "$L"
  case "$verdict" in FORMAT-OK*) ok=$((ok + 1));; esac
done
log "format test: $ok of 3 samples carry an ask"

log "six auctions for $RUN"
MODELS="$RUN" PAR=6 bash "$ROOT/scripts/run_part2_eval.sh" >> "$L" 2>&1
log "done; finished runs: $(ls "$ROOT"/results/*"E6_$(echo "$RUN" | tr -d '_')_"*/collusion_metrics.json 2>/dev/null | wc -l) of 6"
