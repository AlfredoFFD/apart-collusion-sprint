#!/usr/bin/env bash
# Refresh the public copy (github.com/AlfredoFFD/apart-collusion-sprint-public) from the committed HEAD of this
# working repository. Only committed files are copied. Left out: the private credit sheet and downloaded paper
# copies. The copy is built and checked in a temporary folder first: names of people met at the sprint (listed
# only in the local, never-pushed file .git/public-copy-blocked-names.txt), keys and env files. Any hit stops the
# refresh before the public checkout is touched, and a public checkout with local changes is never overwritten.
# Usage, from the repo root in Git Bash:  bash scripts/refresh_public_copy.sh
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${PUBLIC_COPY_DIR:-$SRC/../apart-collusion-sprint-public}"
PUBLIC_URL="https://github.com/AlfredoFFD/apart-collusion-sprint-public.git"
NAMES="$SRC/.git/public-copy-blocked-names.txt"   # local only, never pushed: one blocked name per line
SHA="$(git -C "$SRC" rev-parse --short HEAD)"

[ -d "$DEST/.git" ] || git clone -q "$PUBLIC_URL" "$DEST"
git -C "$DEST" remote get-url origin | grep -q "apart-collusion-sprint-public" \
  || { echo "STOP: $DEST is not the public copy"; exit 3; }
DEST_STATUS="$(git -C "$DEST" status --porcelain --ignored --untracked-files=all)" \
  || { echo "STOP: could not read the status of $DEST"; exit 4; }
if [ -n "$DEST_STATUS" ]; then
  echo "STOP: $DEST has local changes or untracked files; commit or remove them first"; exit 4
fi

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
git -C "$SRC" archive --format=tar HEAD | tar -x -C "$STAGE"
rm -f "$STAGE/docs/reviews/credit-sheet40-2026-10-25.md"
rm -rf "$STAGE/docs/lit/notebook-frontier-2026-10-25/fulltext"
NOTE="> **Public copy** of the CAIAC team's working repository for the Apart AI Collusion Research Sprint (Oct 23-25, 2026), refreshed from working commit $SHA. The full commit history is kept in the private working repository and is available to reviewers on request. Left out of this copy: full-text copies of other authors' papers and one private credit sheet. Every script, run log and result file is included as in the working repository."
{ printf '%s\n\n' "$NOTE"; cat "$STAGE/README.md"; } > "$STAGE/README.tmp" && mv "$STAGE/README.tmp" "$STAGE/README.md"

fail=0
if [ -s "$NAMES" ]; then
  if grep -r -l -i -F -f "$NAMES" "$STAGE"; then echo "STOP: a name of someone met at the sprint"; fail=1; fi
else echo "STOP: $NAMES is missing, so the name check cannot run"; fail=1; fi
if grep -r -l -E 'sk-or-v1-[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{32,}|hf_[A-Za-z0-9]{30,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}' "$STAGE"; then echo "STOP: a key"; fail=1; fi
if find "$STAGE" \( -name '.env' -o -name 'compute.env' \) -print | grep -q .; then echo "STOP: an env file"; fail=1; fi
[ "$fail" = 0 ] || exit 2

# Checks passed. The public checkout is clean, so every file removed here is still in its git history.
find "$DEST" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -a "$STAGE"/. "$DEST"/
cd "$DEST"
git add -A
if git diff --cached --quiet; then echo "public copy already matches $SHA"; exit 0; fi
git -c user.name="Alfredo Frontera" -c user.email="130926974+AlfredoFFD@users.noreply.github.com" \
  commit -q -m "Refresh from working commit $SHA"
git push -q origin main
echo "public copy refreshed from working commit $SHA"
