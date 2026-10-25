#!/usr/bin/env bash
# For a 14B Part 2 run whose pipeline stopped at the functional gate: if the 2-round smoke shows the model ACTS (finite
# asks in every round, at least half of the replies carry an ask), the "no trade in 2 rounds" part of the gate is a
# market outcome, not a capability failure (Sat 10:45 PM: sft_all_14b asked $98.04 while the buyers bid $97.62; the
# 1.7B GRAFT failure the gate was built for had no asks at all). Then warm the server and run the six auctions.
#   bash scripts/part2_auctions_if_acting.sh sft_all_14b
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; RUN="${1:?run}"; WORKSPACE="${MODAL_WORKSPACE:-fabianfrontera}"
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
L="$ROOT/results/_launch_logs/part2_pipeline_${RUN}.log"; log() { echo "== $* $(date +%H:%M)" | tee -a "$L"; }
smoke_dir=$(ls -d "$ROOT"/results/*"E6smoke_$(echo "$RUN" | tr -d '_')_cartel_rot_fine20_s0" 2>/dev/null | tail -1)
verdict=$(python3 - "$smoke_dir" <<'PY'
import sys, json, re
from pathlib import Path
d = Path(sys.argv[1])
try:
    m = json.loads((d / "collusion_metrics.json").read_text(encoding="utf-8"))
    asks = [x for x in m.get("collusion_indices_avg_seller_asks") or [] if isinstance(x, (int, float))]
    n = ok = 0
    for md in d.glob("Seller *.md"):
        for mm in re.finditer(r"## Response: Round (\d+).*?\n````json\n(.*?)\n````", md.read_text(encoding="utf-8", errors="replace"), re.S):
            n += 1
            try: ok += int(json.loads(mm.group(2)).get("ask") is not None)
            except Exception: pass
    acting = len(asks) >= 2 and ok >= max(1, n // 2)
    print(f"{'ACTS' if acting else 'NOT-ACTING'} trades={m.get('num_trades')} asks={len(asks)} replies_with_ask={ok}/{n}")
except Exception as e:
    print("NOT-ACTING", str(e)[:80])
PY
)
log "acting check on the smoke: $verdict"
case "$verdict" in ACTS*) ;; *) log "model does not act: no auctions for $RUN"; exit 2;; esac
host="caiac-serve-$(echo "$RUN" | tr '_' '-')-serve"; URL="https://${WORKSPACE}--${host}.us-east.modal.run"
REQ="$(cygpath -w "$ROOT" 2>/dev/null || echo "$ROOT")\results\_launch_logs\part2_req_${RUN}.json"
log "warming $host"
curl -sS -L --max-time 900 "$URL/v1/chat/completions" -H "Content-Type: application/json" -d @"$REQ" -o /dev/null -w "   warm: HTTP %{http_code} in %{time_total}s\n" | tee -a "$L"
log "six auctions for $RUN (gate overridden: acting model, no trade in the 2-round smoke)"
MODELS="$RUN" PAR=6 bash "$ROOT/scripts/run_part2_eval.sh" >> "$L" 2>&1
log "done; finished runs: $(ls "$ROOT"/results/*"E6_$(echo "$RUN" | tr -d '_')_"*/collusion_metrics.json 2>/dev/null | wc -l) of 6"
