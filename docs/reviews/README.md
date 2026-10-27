# Independent reviews of the analyses

During the sprint a second agent (OpenAI Codex) reviewed every analysis before its numbers were used, audited result tables against the raw run files, and re-checked each correction after it was applied. Our replies and acknowledgements sit next to its reports. Nothing here changes a result; each file says what was checked, what was wrong, and what was fixed.

## Read these first

| file | what it is |
|---|---|
| `codex-negotiation-audit-2026-10-26-0239Z.md` | audit of the Hawthorne intervention test (Appendix B): gate, fallback prices, causal scope |
| `claude-ack-codex-negotiation-2026-10-26.md` | our acknowledgement: the verified numbers, the allowed claims (section 5), the withdrawn wording |
| `codex-monitor-2026-10-26-0206Z.md` (in `heartbeats/`) | the raw-file finding that the end-of-run CEO answers are not a lying measure (sellers replaced at hour 39) |
| `main-session-dream-notes-2026-10-26.md` | the main session's closing notes (video, paper versions, process slips) |
| `credit-sheet40-2026-10-25.md` | the API credit record for the second key |
| `codex-entrant-review-2026-10-25/` (under `docs/lit/`) | the review of the entrant and sting tests' citations |

The side-chat reviews (`codex-main-side-chat-review-*.md`), the correction receipts (`*.png`), and the delivery checkpoints are the trail of each correction from finding to fix.

## `heartbeats/`

Codex ran as a monitor every 15 minutes through the sprint. Each `codex-monitor-<date>-<time>Z.md` file in `heartbeats/` is one heartbeat: results and spending at that moment, open findings, and whether anything changed. Most say "no actionable change". They were moved here from `docs/reviews/` on Oct 26 for readability; earlier entries in `LOG.md` and in the files themselves cite them by their old path, `docs/reviews/codex-monitor-...`, which now resolves under `docs/reviews/heartbeats/`.
