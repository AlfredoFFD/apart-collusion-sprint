#!/usr/bin/env bash
# Build the submission files from report/draft.md: report/report.docx (pandoc), then a Google Doc in Alfredo's Drive (upload with
# conversion, so headings, tables and figures survive) and report/report.pdf exported from it.
#   bash scripts/build_report.sh docx            # local only
#   bash scripts/build_report.sh gdoc            # docx -> Google Doc (prints the doc id and link) -> report/report.pdf
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT/report"
STAGE="${1:-docx}"; TITLE="${TITLE:-Watch the carrier, not the chat (Apart AI Collusion Research Sprint, CAIAC)}"
pandoc draft.md -o report.docx --from markdown+pipe_tables --to docx --resource-path=. --reference-doc=reference_compact.docx && python3 "$ROOT/scripts/docx_polish.py" report.docx 2>&1 | grep -v "^\[WARNING\] Could not" ; ls -la report.docx | awk '{print "docx:", $5, "bytes"}'
[ "$STAGE" = docx ] && exit 0
# upload as a converted Google Doc (mimeType of the target), then export the PDF
resp=$(gws drive files create --upload report.docx --upload-content-type application/vnd.openxmlformats-officedocument.wordprocessingml.document \
       --json "{\"name\": \"$TITLE\", \"mimeType\": \"application/vnd.google-apps.document\"}" 2>&1)
id=$(printf '%s' "$resp" | python3 -c "import sys, re; m = re.search(r'\"id\":\s*\"([^\"]+)\"', sys.stdin.read()); print(m.group(1) if m else '')" 2>/dev/null)
[ -n "$id" ] || { echo "upload failed: $resp" | cut -c1-400; exit 1; }
echo "google doc id: $id  link: https://docs.google.com/document/d/$id/edit"
gws drive files export --params "{\"fileId\": \"$id\", \"mimeType\": \"application/pdf\"}" --output report.pdf 2>&1 | tail -n 1
ls -la report.pdf | awk '{print "pdf:", $5, "bytes"}'
