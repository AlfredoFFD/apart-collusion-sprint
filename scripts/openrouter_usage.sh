#!/usr/bin/env bash
# Print this OpenRouter key's usage so far (dollars) and its remaining limit. Reads the key from compute.env inside a
# subshell and never prints it. Output: usage=<x> limit_remaining=<y|none>
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
( set -a; . "$ROOT/vendor/collusion_hackathon/compute.env" >/dev/null 2>&1; set +a
  curl -sS --max-time 30 https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer $OPENROUTER_API_KEY" ) \
| python3 -c "import sys, json; d = json.load(sys.stdin).get('data', {}); print(f\"usage={float(d.get('usage') or 0):.2f} limit_remaining={d.get('limit_remaining')}\")"
