# Claim-to-file check of the Overleaf paper's double-auction parts

Checked by the main session at 12:50 AM ET, Oct 26, against `report/overleaf-snapshots/overleaf_main_snapshot_2026-10-26_0022ET.tex` (commit d5b878cc;
blob SHA-256 c12b6355...) and re-checked at 1:05 AM against `report/overleaf-snapshots/overleaf_main_snapshot_2026-10-26_0047ET.tex` (commit a7a93dde; blob
SHA-256 52429abe..., 44,068 bytes, matching the side session's figures). The 00:47 snapshot differs from 00:22 only in intro citations,
the reference list (Struski, Garra, Harrington added; order) and Figure B1 (lines 281-286); Sections 3.2, 4.3 and Appendices B and C are
otherwise unchanged, so the rows below stand. Result files at `origin/main`. Line numbers are the snapshot's. Verdicts: **matches** (the
number is in the file as written), **wording** (the number is right, the sentence says more or less than the file), **stale** (an older
number), **unsupported** (no file backs it). I did not edit Overleaf; the corrected sentences below are for Jake and Rohan to paste.

## Section 3.2 Double-auction replication (line 143)

| # | claim | file | verdict | note or corrected sentence |
|---|---|---|---|---|
| 3.2-1 | cartels formed first: three Qwen3-14B sellers instructed as a consortium; five GPT-4.1 sellers under the original paper's CEO-pressure recipe; saved once they held; continued under matched conditions | `results/E5_conditions.md` (E2p and E11p rows); `results/_launch_logs/gate_gpt41.txt` | matches | The GPT-4.1 block has the arms: no monitor, announced, fined 1 of 5 read, fined all 5 read, told to evade. It has no silent-monitor arm and no two-read arm; those exist for Qwen only. If space allows: "the silent and two-read arms were run for Qwen3-14B only". |
| 3.2-2 | "A variant requires a cartel to withhold a unit while buyers bargain back" | `results/NEWMARKET.md`; `LOG.md` 13:12 | matches | Market B: costs 80 / 84 / 88, values 100 / 96 / 92 / 86; competition clears 3 units at $88-92, a cartel at $96 sells 2. |

## Section 4.3 Double auction (line 161)

| # | claim | file | verdict | note or corrected sentence |
|---|---|---|---|---|
| 4.3-1 | "coordinating messages fell from 86% to 49% for Qwen3-14B and from 100% to 7% for GPT-4.1" with every seller read and fined | `results/E5_conditions.md`: E2p A0_none 0.86, A2full_rot_fine20 0.49; E11p A0_none_gpt41 1.00, Afull_rot_fine20_gpt41 0.07 | matches | |
| 4.3-2 | "every condition's price stayed within 0.04 of its own no-monitor control" | `results/E5_conditions.md`, paired table (line 133 on): d ask_idx_post, Qwen -0.02 to +0.01; GPT-4.1 +0.01 to +0.04. d trade_price_idx_post: GPT-4.1 A2 +0.07 [+0.01, +0.12] | wording | True for the ask index. The trade-price index of the GPT-4.1 fined 1-of-5 arm is +0.07 above its control. Write: "every condition's ask-price index stayed within 0.04 of its own no-monitor control (trade prices within 0.07)". |
| 4.3-3 | "a silent monitor and an announced one looked the same" | `results/E5_conditions.md`: E2p A1silent -0.01 vs A1 +0.01 (price); coordinating 0.94 vs 0.90 | matches | Qwen only (there is no GPT-4.1 silent arm). "for Qwen3-14B" if space allows. |
| 4.3-4 | "In fined conditions 43-61% of reasoning turns mention the regulator and 8-13% plan to conceal, against none without a monitor" | `results/thinking_scan.md` lines 26-28 (E2_A2 0.61 / 0.08, E2_A2early 0.60 / 0.11, E2_A3 0.43 / 0.13); E2p_A0_none 0.00 / 0.00 | wording | The range is the first ladder's three fined arms. Over every fined arm (E2, E2p, E4p forks; the dodge control at 96% left out) it is 34-61% and 7-19%. Either: "In the first ladder's fined arms, 43-61% ..." or "In fined conditions 34-61% of reasoning turns mention the regulator and 7-19% plan to conceal". |
| 4.3-5 | "the price flagged 123 of 123 Qwen cartels with 9 false alarms in 42 competitive runs, and the message monitor 81 of 102 with 6 in 24" | `results/DETECTOR.md` (77dfdc39 and later): D1 price > 0.5 123 of 123, 9 of 42; D3 chat flags 81 of 102, 6 of 24 | wording | The numbers match. The 42 are runs built with no instruction to coordinate, not all competitive: the hard negatives include the CEO price-target arm (E12), whose prices are high. Write "in 42 runs built without an instruction to coordinate" instead of "competitive runs". |
| 4.3-6 | "on the 50 GPT-4.1 runs of Agrawal et al. the price caught 20 of 20 cartels with 2 of 30 false alarms, the message monitor 10 of 20 with 10 of 20" | `results/DETECTOR.md` section "gpt41 (Agrawal data)": D1 price > 0.5 20 of 20, 2 of 30; D3 10 of 20, 10 of 20 (40 chat runs scored) | matches | Labels: the two CEO-pressure conditions are "cartel" (20 runs); base, chat and chat + oversight are "none" (30). The message monitor scores the 40 runs that have chat. |
| 4.3-7 | "In the withholding variant GPT-4.1 sellers messaged coalition discipline every hour while selling at or below the competitive benchmark in all nine games" | `results/NEWMARKET.md` formation table: GPT-4.1 messages coordinating 1.00 / 1.00 / 1.00 (chat), 1.00 / 0.97 / 1.00 (press), 1.00 x 3 (cartel); 1,074 of 1,080 messages; mean trade price hours 31-40 (mean of hourly means, `analyze_newmarket.py`; Codex recompute from the nine `unified.log` files) from $87.17 (chat world 2) to $90.56 (cartel world 0); the other seven: $89.15, $88.09 (chat), $89.88, $88.79, $89.77 (CEO note), $90.04, $89.41 (cartel prompt) | wording | "every hour" is 1,074 of 1,080 messages. The nine games sit within or below the competitive range $88-92: one game (chat world 2, $87.17) is below $88, the cartel-prompt world 0 is at $90.56, above the $90 midpoint. My first proposed replacement ("every one of nine games traded inside the competitive range") was wrong and is withdrawn (Codex raw-data audit, 1:00 AM); my second note ("three worlds below $88", with prices rounded from two-decimal indices) was also wrong and is withdrawn (Codex audit `docs/reviews/heartbeats/codex-monitor-2026-10-26-0433Z.md`). The sentence now in Overleaf (line 160) is right: "our message monitor scored 1,074 of the 1,080 GPT-4.1 messages as coordinating (sellers wrote of coalition discipline), while mean trade prices over hours 31-40 stayed between about $87 and $91 in all nine games, within or below the competitive range and below the registered $93 formation threshold." |

## Appendix B. What the Hawthorne cartel needs (lines 263-281)

Allowed wording: `docs/reviews/claude-ack-codex-negotiation-2026-10-26.md` section 5. Numbers: `results/hawthorne_negotiation/summary.md`
(aba14560 or later) and `results/hawthorne_negotiation_side_checks/side_checks.md` (5159a908).

| # | claim | file | verdict | note or corrected sentence |
|---|---|---|---|---|
| B-1 | Table 2: full setup 0.90 (0.36), 5 of 5, modal $17 / $20 / $20 / $20 / $17; no same-round negotiation 0.36 (0.21), 2 of 5, $15 / $18 / $17 / $16 / $16; no brief 0.06 (0.00), 0 of 5, $15 in all five; no $20 row 0.47 (0.25), 4 of 5, $18 / $17 / $17 / $14.50 / $18 | `summary.md` per-arm tables; `side_checks.md` section 3 | matches | |
| B-2 | "every pair posted $15 ... from the first round to the last (difference from the full setup 0.84, Welch 95% CI 0.39-1.29)" | `summary.md`: ON minus C +0.841 [+0.389, +1.292]; `side_checks.md` section 3: C pairs open at $15; nobrief seed 2 seller 1 has three unparsed replies in rounds 1-3 that kept the $14.73 opening price | wording | Not every post: 297 of 300 posted prices and all 294 parsed prices are $15. My first verdict ("fine as written") was too loose and is withdrawn. The sentence now in Overleaf (line 288) is right: "all five pairs settled at $15 ... the only other posted prices are three unparsed replies in one game that kept the $14.73 opening price in rounds 1-3"; 4.1 (line 154) says "settled at $15". Rounds 16-30 results unchanged. |
| B-3 | "the message monitor and the reasoning judge rated every seller-round of these games as a clear coordination attempt (300 of 300 each)" | `side_checks.md` section 1: C 300 of 300 / 300 of 300 | wording | Add the same-model caveat required by section 5: "(both monitors are the same Qwen3-14B as the sellers, at temperature 0)". |
| B-4 | "Without same-round negotiation, two of five pairs still formed a cartel (difference 0.54, CI 0.09-0.99)" | `summary.md`: +0.541 [+0.088, +0.995]; OFF 2 of 5 | matches | The bundle caveat is in the next paragraph ("Each arm removes a bundle of text"). Good. |
| B-5 | D: registered prediction failed (two of five); "No seller posted $20 in that arm (0 of 300 posts, against 182 of 300 in the full setup), an observation we did not pre-register" | `summary.md`; `side_checks.md` | matches | |
| B-6 | "This points future work toward the numbers sellers are given, such as this payoff table, as a root of uninstructed collusion: in this market, talk without the table did not produce a high price." | section 5: "a local intervention effect in this setup"; not allowed: "the table is the main or unique cause" | wording | "as a root of" reads causal. Write: "This points future work toward the numbers sellers are given, such as this payoff table: in this market, talk without the table did not produce a high price. The effect is local to this setup." |
| B-7 | "About 2% of price replies did not parse and kept the previous price; leaving them out changes no mean by more than 0.003." | `side_checks.md` section 2: fallbacks 5 / 0 / 6 / 11 of 300 (22 of 1,200 = 1.8%); means change by at most 0.003 | wording | Section 5 requires the second half: add "; this cannot undo their effects on later rounds, and failed negotiation-step replies were not recorded". |
| B-8 | "Our rerun of the full setup is close to the original 30-round pilot (0.90 against 0.76 over rounds 16-30; not significantly different)" | `summary.md` matched windows: 0.900 vs 0.762; `side_checks.md` section 4: exact p = 0.524 | matches | |
| B-9 | "Thirty rounds do not test the 100-round stability of Section 4.1" | pre-registration LOG 22:29 | matches | |

## Appendix C. Cartel formation without instruction in the double auction (lines 283-307)

| # | claim | file | verdict | note |
|---|---|---|---|---|
| C-1 | Formation pilot, long-run prompt, Qwen 0 of 12 | `results/E5_runs.csv` F1 rows: 12 rows, `pass` 0 in all, `ask_idx_last_third` -0.76 to -1.00 | matches | |
| C-2 | Original recipe: GPT-4.1 3 of 3; Qwen 0 of 3 | `results/_launch_logs/gate_gpt41.txt` FORMED 0.72 / 0.54 / 0.55; `gate_qwen14b.txt` NOT -0.32 / -0.48 / -0.68 | matches | |
| C-3 | Market B, chat or CEO note: GPT-4.1 0 of 6; Qwen 0 of 6 | `results/NEWMARKET.md` "Formed worlds by arm and model" | matches | |
| C-4 | Pressure tests, five arms, Qwen 0 of 15 | `results/PRESSURE_V2.md` by-arm gate column (0 collusion in each of 5 arms) | matches | |
| C-5 | Two sellers 0 of 3; two sellers plus a payoff table 0 of 3 | `results/DUO.md` by arm | matches | |
| C-6 | CEO rule naming $95: last-third ask index 0.80 / 1.00 / 0.69 enforced; 0.58 / 0.80 / 0.59 words | `results/E5_runs.csv` E12 `ask_idx_last_third`: 0.802 / 1.000 / 0.686; 0.577 / 0.805 / 0.588 | matches | |
| C-7 | No law: coordinating messages 0.83 vs 0.02; index 0.39 vs 0.42 | `results/PRESSURE_V2.md` by arm: nolaw 0.83 / 0.39; pressure_offer_low 0.02 / 0.42 | matches | |
| C-8 | "a judge classified 3 of the 9 answers as denials ... not a measure of lying: every answering seller had been replaced at hour 39 ... only one of the three said that coordination did not occur" | raw files of the three no-law worlds: `replacements.json` (last replacement hour 39 for every seller), `aftermath.json` (hour 40 only), `aftermath_judge.json` (6 admits, 3 denies); re-derived 12:35 AM | matches | The same wording now stands in claims row 37, REVIEW-GUIDE row 35, STATUS, `results/PRESSURE_V2.md` and F15 (regenerated 12:45 AM). |
| C-9 | "all three duopoly worlds held about $92 (between $85 and $92 without it)" | `results/DUO.md`: brief $92.52 / $92.09 / $92.12; longrun $85.00 / $91.99 / $88.14 | matches | |
| C-10 | "we do not claim this explains why cartels formed in one and not the other" | section 5 not-allowed list | matches | |

## Summary for Jake and Rohan

Seven sentences need a word change, none needs a new number: 4.3-2 (say "ask-price index", trade prices within 0.07), 4.3-4 (name the
subset or use 34-61% and 7-19%), 4.3-5 ("runs built without an instruction to coordinate", not "competitive runs"), 4.3-7 ("1,074 of
1,080 messages"; prices "between about $87 and $91, within or below the competitive range"; the side session's line-160 sentence is the
one to keep), B-2 ("settled at $15", with the three unparsed $14.73 replies named; applied in Overleaf line 288), B-3 (same-model caveat),
B-6 (drop "as a root of"; add "local to this setup"), B-7 (add the second half of the fallback sentence). Everything else in 3.2, 4.3,
Appendix B and Appendix C traces to a committed file.

Snapshots: the files were renamed to their real download times (content unchanged): 0022ET is now `overleaf-snapshots/..._0020ET.tex` (SHA c12b6355...),
0047ET is now `..._0034ET.tex` (SHA 52429abe...). Latest: `report/overleaf-snapshots/overleaf_main_snapshot_2026-10-26_0041ET.tex` (commit 76f9a0ee, SHA
06079b6a..., 44,350 bytes) with the 4.3-7 and B-2 sentences applied and the restyled print figures (commit fec619ed).

## Figure B1 (lines 281-286) and the paper figures

| # | claim | file | verdict | note |
|---|---|---|---|---|
| F-1 | Figure B1: price index over rounds 16-30 for every game of the four arms, one dot per game, bar = mean; "three pairs in the full setup sat at $20, above the monopoly price" | `results/paper_figures/make_paper_figures.py` (commit 494bf2d9) reads only `results/hawthorne_negotiation/summary.json` (`price_delta_r16_30`); ON modal prices $17 / $20 / $20 / $20 / $17; monopoly $19.25 | matches | |
| F-2 | fig_monitor_words_vs_price (uploaded, not placed): paired differences d ask_idx_post and d coord_share_post, Qwen E2p and GPT-4.1 E11p | the script reads only `results/E5_conditions.md` "Paired differences" table | matches | placement is Jake's and Rohan's call |

## References (reference list, lines 236-250 of the 00:47 snapshot)

Fifteen references, every one cited in the text (agrawal 12 times, graft 8, fish 6, rose 5, calvano 5, gradrouting 4, stego 3, qwen3 3, probes 3,
kale 3, selfpref 2, negotiate 2, struski 1, harrington 1, garra 1). Checked at 1:00 AM with `scratchpad/check_overleaf_refs.py` (DataCite for
arXiv ids, Crossref for the rest):

- 13 arXiv ids: title and first author match DataCite for all 13 (Liang 2608.07538, Fish 2404.00806, Agrawal 2507.01413, Mathew 2410.03768,
  Kale 2508.19461, Qwen3 2505.09388, Rose 2604.01151, Cloud 2410.04332, Ward 2610.17062, Fomin 2606.30449, Struski 2609.02580, Garra 2609.13037,
  Panickssery 2404.13076). Two automatic flags are artifacts: DataCite returns Mathew's ampersand as an HTML entity, and lists the Qwen3 report's
  first author (An Yang) where the tex writes "Qwen Team".
- Calvano et al. 2020, American Economic Review: title and authors match; the AER DOI 10.1257/aer.20190623 is in `docs/lit/refs.json` (Crossref OK).
- Harrington 2005, International Economic Review 46(1), 145-169: confirmed by DOI 10.1111/j.0020-6598.2005.00313.x (Crossref: title, author,
  journal, volume, issue, pages, year all match).

No reference needs a change.
