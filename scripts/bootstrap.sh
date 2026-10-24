#!/usr/bin/env bash
# One-time setup. Clones the organizers' starter repo into vendor/ at a pinned commit, installs our copy of the
# double-auction harness (src/double_auction) and checks that it runs. Safe to re-run.
#
#   bash scripts/bootstrap.sh                               # the auction harness only
#   STARTER_SETUP="redteaming" bash scripts/bootstrap.sh    # also run the starter's own setup for other folders
#
# Needs git and uv (https://docs.astral.sh/uv/). On Windows, run it in Git Bash.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER_URL="https://github.com/poseidon-research/collusion_hackathon"
# Pinned on Oct 23, 2026. Change it on purpose (and note it in LOG.md), never by accident.
STARTER_REF="${STARTER_REF:-d585a7b3be50366cc2bdf5789bf8add5890b2abd}"
VENDOR="$ROOT/vendor/collusion_hackathon"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing $1. $2"; exit 1; }; }
need git "Install git first."
need uv "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh  (then open a new terminal)"

echo "== Starter repo -> vendor/collusion_hackathon at ${STARTER_REF:0:7}"
if [ ! -d "$VENDOR/.git" ]; then
  git clone "$STARTER_URL" "$VENDOR"
fi
if ! git -C "$VENDOR" cat-file -e "${STARTER_REF}^{commit}" 2>/dev/null; then
  git -C "$VENDOR" fetch --quiet origin
fi
if [ "$(git -C "$VENDOR" rev-parse HEAD)" != "$(git -C "$VENDOR" rev-parse "${STARTER_REF}^{commit}")" ]; then
  git -C "$VENDOR" checkout --quiet --detach "$STARTER_REF"
fi
echo "   ok"

if [ ! -f "$VENDOR/compute.env" ]; then
  cp "$VENDOR/compute.env.example" "$VENDOR/compute.env"
  echo "   created vendor/collusion_hackathon/compute.env from the example"
fi

echo "== Auction harness (src/double_auction)"
( cd "$ROOT/src/double_auction" && uv sync --quiet )
( cd "$ROOT/src/double_auction" && uv run --quiet python src/continuous_double_auction/simulation.py --help >/dev/null )
echo "   ok: simulation.py runs"

if [ -n "${STARTER_SETUP:-}" ]; then
  echo "== Starter setup for: $STARTER_SETUP"
  # shellcheck disable=SC2086  # word splitting is intended: one argument per folder
  ( cd "$VENDOR" && ./setup.sh $STARTER_SETUP )
fi

echo
if grep -Eq '^(NEBIUS_API_KEY|OPENROUTER_API_KEY)=.+' "$VENDOR/compute.env"; then
  echo "Done. A key is set in vendor/collusion_hackathon/compute.env. Next: the smoke test in README.md."
else
  echo "Done. Next: add NEBIUS_API_KEY and/or OPENROUTER_API_KEY to vendor/collusion_hackathon/compute.env"
  echo "(never commit it), then run the smoke test in README.md."
fi
