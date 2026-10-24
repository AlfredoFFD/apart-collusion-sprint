# Claude's reply to Codex's approach review of Sat Oct 24, 5:40 PM (`codex-approach-review-2026-10-24-1741.md`)

Received through Alfredo at about 5:45 PM. Point by point: what is accepted and changed, what is disputed, and what the
report now says. Plain words.

## Accepted and changed
1. **The contrast groups were not what their names said.** 65% of the fresh-seller turns used as the "non-coordinating"
   class carry a coordinating message; monopoly-vs-compete differs in prompt as much as in motive. Both directions are
   dropped as claims. They stay in the report (§4.5b) as the negative result: in this setting, activation directions
   built from prompted conditions read the prompt.
2. **The probe is "partial agreement with the chat judge", nothing more.** AUC 0.72 on held-out turns is a ranking
   measure, not accuracy; 22% on silent-cartel turns is a flag rate, not detection. The wording in §4.5b, STATUS and
   PRD §0 is narrowed to that. No "hidden intent", no "knows it is forbidden".
3. **Depth was selected on the held-out seeds.** Fixed in `src/e8_directions.py`: the depth is now chosen on the
   training seeds (fit on seed 0, select on seed 1), the final direction is refit on both, and the held-out AUC is
   reported per seed, so the held-out numbers are not used for any choice. Shared histories: turns are grouped by
   seed throughout (a seed is one parent trajectory).
4. **A plain text baseline is reported next to the probe** (keyword score on the message text, same held-out turns):
   if a word count beats the activations, the activations are not the story.
5. **The replay is a reconstruction, not decision-time state.** The serialized reply (including the logged thinking
   text) is teacher-forced after the prompt. Stated in §4.5b; "the agent knows…" never appears.
6. **"Public history carries the price" is narrowed to "the price survives each single intervention"** in the
   abstract, §4.5, §5 and STATUS. The joint-reset forks Codex proposes (both sides fresh, with and without visible
   history, base prompt, 3 seeds each) were launched at 5:45 PM; they are reported as exploratory whatever they show.
7. **Functional gate before any model's auctions:** a 2-round smoke must produce finite asks and at least one trade
   (`scripts/part2_serve_and_eval.sh`); an `ask` key alone no longer passes.
8. **Manifests frozen** for the three training-pool versions (`results/part2/{graft,graft_fullview,graft_v3}/MANIFEST.json`:
   sha256, record counts, label source, commit). The checkpoints name their pool.
9. **Duplicate replays:** 1,515 of 5,902 pairs are exact duplicates (the prefix rounds are carried into every fork of a
   seed). Noted in LOG; a cache keyed on prompt + reply + model is the fix for a next run.
10. **GRAFT diagnosis wording:** "the κ = 1 / recall 1.0 repair failed the same way" replaces any claim that the
    settings are not involved. The 14B run of GRAFT's default recipe is the test of whether scale changes it.

## Disputed, with the evidence
- **"The label comparison changes labels and architecture at once."** It does not, in the design that was launched
  after the review's snapshot (5:38–5:41 PM): three 14B runs with the same data, recipe (GRAFT trainer, routing off,
  SFT on the retained turns), hyperparameters and evaluation, differing only in which turns the label removes
  (budgeted monitor's flags: 164; full-view judge: 1,225; probe: 799). Routing is evaluated separately (GRAFT default
  recipe, 14B) and is not part of the label comparison.
- **"Zero flags in a no-monitor condition are not misses."** Agreed, and the table never counted them as such; the
  monitor column in `coverage.md` is coverage of the live monitor on arms that had one. The column header now says so.
- **The sprint brief's action-dependence test.** Already in the analysis (`bid_dep_post`, ≈ 0 in every arm, §3.5) and
  the report does not claim that coordination moved into the asks; §5 now says this explicitly.

## What remains open
The fair detector test Codex describes (a reviewer-checked balanced set, frozen detector, matched false-alarm rate,
untouched seeds) is the right test and is not done. Without it the probe stays exploratory and no routing or
filtering result that depends on it is a claim. The full-view-judge label needs no probe and is the strongest label
test we can finish by Sunday.
