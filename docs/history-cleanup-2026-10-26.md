# History cleanup and public release, Mon Oct 26, 2026

**What happened.** On Sun Oct 25 the history of this repository was rewritten (filter-repo) to remove the name of a
person met at the sprint, and GitHub Support deleted pull request #2, which still held the old commits. At 00:20 ET on
Oct 26 a teammate ran `git pull` in a clone made before the rewrite and pushed the merge (`3eb1c600`). That merge
brought the old history, with the name, back into `main` (7 commits). No current file contained the name.

**What was done (between 01:05 and 01:15 ET).**
1. In a separate mirror clone, the merge `3eb1c600` was made a single-parent commit (its second parent, the old
   history, was dropped; `git replace --graft` plus `git filter-repo`). The merge added no content of its own.
2. The cleaned `main` has exactly the same files as before (tree `3870119b71e298225a84046367fcfdfda1b22176` before and
   after). It has 289 commits; no commit adds or removes the blocked names, an API-key pattern or an env file.
3. The old repository was renamed to `AlfredoFFD/apart-collusion-sprint-private` and stays private. A new public
   repository with the original name, `AlfredoFFD/apart-collusion-sprint`, received the cleaned `main` and the tag
   `results-freeze`. A new repository has no old objects, no old pull requests and no collaborators, so no old clone can
   push the old history into it.
4. The shared local checkout was moved to the cleaned `main` (compare-and-swap on the old head `b086b90e`; working
   files untouched).

**Commit IDs that changed** (the merge and every commit after it; all other IDs, including every pre-registration
commit, are unchanged). Older notes that cite a left-hand ID refer to the right-hand commit, which has the same content.

| Old ID | New ID | Date (ET) and message |
|---|---|---|
| `2f8fbd52` | `18f61222` | 10-26 00:30 | PRESSURE_V2 per-world table: rename the 'lies' column (judge-classified denials after replacemen |
| `30149d11` | `7a824592` | 10-26 00:43 | Overleaf claim check: withdraw two loose verdicts (4.3-7 prices within or below the range; B-2 t |
| `3eb1c600` | `1dd50490` | 10-26 00:20 | Merge branch 'main' of https://github.com/AlfredoFFD/apart-collusion-sprint |
| `494bf2d9` | `5d435cd8` | 10-26 00:30 | Paper figures from committed files only (no new runs): monitor conditions change words, not pric |
| `5a549a80` | `95896445` | 10-26 01:02 | Results freeze at 1:01 AM ET: regenerate unchanged; tag results-freeze |
| `76f9a0ee` | `6e108ff9` | 10-26 00:41 | Overleaf main.tex snapshot 00:41 ET (SHA-256 06079b6a...4e10, 44,350 bytes, 325 lines): Codex wo |
| `8a8a0585` | `cda33148` | 10-26 00:45 | Claim check 4.3-7: exact Market B trade prices from the logs (7.17 to 0.56); one game below 8, n |
| `9420e06d` | `38232ed9` | 10-26 00:37 | Overleaf claim check: 00:47 snapshot, Figure B1, all 15 references verified |
| `a366c068` | `c0a0587e` | 10-26 00:28 | CEO answers are not a lying measure (replaced at hour 39; 3 of 9 judged denials); claim-to-file  |
| `a7a93dde` | `3b178156` | 10-26 00:34 | Overleaf main.tex snapshot 00:47 ET (SHA-256 52429abe...43d2, 44,068 bytes, 325 lines): adds Fig |
| `adedfd7f` | `57e903ce` | 10-26 00:58 | Appendix B figure redrawn in the teammate's paper style (palette, type sizes, rounded bars from  |
| `b086b90e` | `6b745610` | 10-26 01:10 | Companion report (long form) written from the frozen results; claims table points at it; status |
| `d5b878cc` | `2ebd6720` | 10-26 00:21 | Overleaf main.tex snapshot for the freeze audit (Mon 00:22 ET; SHA-256 c12b6355...f05f, 42,986 b |
| `fec619ed` | `8c7748a8` | 10-26 00:37 | Paper figures restyled for print: serif type matching the paper, small text, (a)/(b) panel label |
