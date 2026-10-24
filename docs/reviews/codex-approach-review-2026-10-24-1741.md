Independent review for Alfredo. Evidence checked on October 24, 2026, through 17:40 ET. This reviews the pasted Claude conversation and the live code/results. It does not authorize new runs or change the team's plan.

**The useful insight is that poor training labels can limit GRAFT. The unproven step is that our activation score supplies better labels. Test that step before adding more training.**

Claude has produced useful work: paired market continuations, more seeds, controls for repeated instructions, corrected training data, and an honest record of the small model's failures. The problem is that the explanation has become more certain while the experiment has become broader. A larger model can help with capability. It cannot fix an invalid label or prove a mechanism.

**What I agree with in the pasted conversation**

- Preserve ordinary profit-seeking ability while targeting harmful coordination. This is a sensible goal. Calling a direction “greed” does not establish that it represents this ability.
- Check a detector before using it to route training updates. A routing label decides which examples train the adapter that will later be removed.
- A label-quality comparison can be a useful result without another training run. This is the best near-term use of the completed activation replay.
- Keep steering, a second reward objective, and a new market design outside the core result for now.

**The main scientific gaps**

1. **The original negative group is not a verified non-coordinating group.** Of the 72 fresh-seller turns used to fit the original contrast, 47 already have a coordination score of at least 3 from the full-view judge. That is 65%. Some messages explicitly propose shared prices. Equal prices do not make the groups differ only in agreement. Prompts, memory, market structure, and message content also differ. “Monopoly minus compete” has the same problem: it could identify a one-seller market rather than greed.

   Claude has now made a useful correction. The latest code fits a second probe using coordinating and non-coordinating messages under the same broad instruction. Its best validation AUC is 0.716. AUC measures how well a score ranks positive cases above negative cases; it is not 72% accuracy. This is evidence of partial agreement with the chat judge. It is not evidence that the probe detects hidden intent. It flags 22% of silent-cartel turns at its current threshold. Without independent labels for those turns, 22% is a flag rate, not detection accuracy. The older 0.87 result belongs to a different contrast.

2. **The detector comparison is not yet fair.** The budgeted monitor often sees one seller out of three. The probe scores every turn. More coverage can follow from reading more material. Also, zero flags in a no-monitor condition are not detector misses. Compare the probe with the existing full-view text judge on the same cases and with the same allowed false-alarm rate. Report inspection cost separately. A probe trained on that judge's labels needs an independent check; agreement with its teacher alone cannot show that it is better.

3. **The validation set is being used to choose the detector.** The script selects the layer with the best “held-out” AUC. Those cases are valid for model selection, but they are no longer an untouched final test. Many turns also share a seed and market history. Thousands of turns are not thousands of independent experiments. Freeze the detector, use an untouched test set, and estimate uncertainty across independent seeds or parent market trajectories. Part 2 also needs new evaluation seeds; fresh samples from training seeds do not establish generalization to new starting contexts.

4. **The replay does not recover the original decision-time activations.** The script feeds saved prompts and serialized replies back through a model, then averages reply-token activations. Logged `_thinking` text is included in this reconstruction. These can be useful classification features. They do not directly show the state that caused the original decision. A simpler text classifier is therefore an important comparison. “The agent knows it is doing something forbidden” is not supported by this analysis.

5. **Public history is a plausible explanation, not an isolated cause.** Resetting sellers while buyers retain their state, and resetting buyers while sellers retain their state, leaves several possible causes. Standing orders, retained agents, public history, and willing buyers can each help preserve the price. The report can say that high prices survive each tested intervention. It cannot yet say public history alone carries the behavior, or that ongoing coordination is unnecessary. The cheapest fix is narrower wording. If the mechanism is essential, the next experiment should jointly reset both groups and vary access to public history while holding other market state fixed.

6. **The GRAFT diagnosis goes beyond the evidence.** Failure after changing two settings shows that this attempted repair failed. It does not rule out those settings as contributing causes, establish the cause of the failure, or prove that the corresponding 14B run would fail. A shared adapter is another hypothesis. First test one repaired recipe on output format and actual trading ability. Then compare routing labels while keeping that recipe fixed. Otherwise, a GRAFT++ comparison changes both the labels and the architecture, and we cannot tell which change mattered.

The official sprint brief supports a narrow interpretation: Track 3.4 asks for evidence that action dependence rises before claiming that coordination moved out of chat. High prices alone do not establish this. See the [Apart sprint brief](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25).

**The best next experiment**

Ask: **Can the activation detector find coordination that a text detector misses, without falsely flagging ordinary profitable trading?**

First, use a small, balanced review set of existing cases. Include explicit agreements, high prices without evidence of agreement, and cases with little or no chat. Have reviewers check the evidence without seeing the detector's score. Permit an “uncertain” label; silent high-price behavior is not automatically a confirmed cartel. Use this set to find label and format problems. Then freeze the detector, threshold, and preprocessing. Reserve new seeds for the final comparison. Match the false-alarm rate across detectors and keep shared histories together when splitting data.

Only if that test supports the activation labels should they replace the text labels in one working GRAFT recipe. Keep training data, model, recipe, and evaluation conditions fixed. Measure both coordination evidence and ordinary trading ability. A lower score from the same probe used to supply training labels is not sufficient evidence of success.

This is a candidate application contribution. The project's novelty search is explicitly bounded. It does not establish a new fundamental method or a “first” result. A carefully validated label improvement would be a stronger contribution than a GRAFT++ name attached to several simultaneous changes.

**How to finish with less work**

- Keep Part 1 as the main result: in the tested market, fines reduce detector-labelled coordinating chat while high prices persist. Treat the cause of that persistence as unresolved.
- Use the completed replay for the detector comparison. Do not require another full model, more reward objectives, or steering to finish this claim.
- Gate auction batches on a short end-to-end check for every model. Check finite valid asks and actual trades, not only the presence of an `ask` key. Repeated full auctions from a model that cannot submit asks add little information about collusion.
- Cache replay by exact prompt and response, together with model and preprocessing identity. I counted 5,902 replay pairs but only 4,387 unique pairs: 1,515 exact duplicates, or 25.7%. Caching can remove those repeated forwards without removing evidence. It does not recover compute already spent.
- Preserve versioned outputs. During this review, the original contrast, a template-corrected contrast, and the within-prompt probe successively changed the routing labels. The current probe creates 799 FORGET and 949 RETAIN records. Freeze a manifest before training so the report identifies which version produced each checkpoint.

I would spend the next effort on one fair detector test and one functional training gate. I would defer additional architecture variants until those pass. No active files, jobs, or experiments were changed by this review.

Evidence and checkpoint: [current probe results](C:/Users/fabia/dev/apart-collusion-sprint/results/e8/directions.json), [coverage tables](C:/Users/fabia/dev/apart-collusion-sprint/results/e8/coverage.md), [probe fitting and layer selection](C:/Users/fabia/dev/apart-collusion-sprint/src/e8_directions.py:211), [replay construction](C:/Users/fabia/dev/apart-collusion-sprint/src/e8_directions_modal.py:64), [behavioral results and current interpretation](C:/Users/fabia/dev/apart-collusion-sprint/report/draft.md:177), [bounded novelty note](C:/Users/fabia/dev/apart-collusion-sprint/docs/lit/e8_novelty-note.md).

Snapshot identifiers at 17:40 ET, for distinguishing this review from later changes:

| File | SHA-256 |
|---|---|
| `src/e8_directions.py` | `c012e123f6f2054cca0d0557ea26714496e730d74fb72b5aafcafaef1cb14b7a` |
| `results/e8/directions.json` | `213ea4fe867cd137faf032609823f16bf358096b41c6e98ac33d74a123d6bffb` |
| `results/e8/coverage.md` | `e1ee842bd99c73ad81a1f0911dc18d5fb3573cc05162080ec160625540b6d744` |
| `results/part2/graft_v3/gr_train_forget.jsonl` | `a7a769e8c7eec7a036bdb9d4f3c858c2da2851891977b7eb60eca427fd26609e` |
| `results/part2/graft_v3/gr_train_retain.jsonl` | `a0f8fd056b4688f28cdb373b746ac6957b64b33b73947092976d85c2ebe0aae9` |
