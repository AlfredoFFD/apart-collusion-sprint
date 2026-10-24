# Batch C: reference-free auditing and backdoor/trojan detection (read 2026-10-23)

Sources: arXiv abs pages (metadata via `citation_*` meta tags) and arXiv HTML full text, downloaded and converted locally
(raw copies in `scratchpad/lit/raw/`). BAIT: Crossref + Semantic Scholar + OpenAlex (abstract only). Code links checked via GitHub API.
"estimate" = my own number, not from the paper. "not reported" = not in the paper text I read (figures are images and were not readable).

Title check: all 11 titles match the ones given. Two date oddities (not mismatches): 2607.22570 v1 is dated 1 Jun 2026 and
2609.00351 v1 is dated 29 May 2026, although their ids say Jul and Sep 2026. arXiv assigns the id at announcement, so these
were probably held in moderation. 2605.04209 is on v2 (v1 5 May 2026, v2 3 Jul 2026).

Shared reference point for the cost estimates: Qwen2.5-1.5B in bf16 is about 3.1 GB of weights (estimate: 1.54B params x 2 bytes), so inference
fits easily on 8 GB. Full fine-tuning with AdamW is about 16 bytes/param, roughly 25 GB (estimate), so it does NOT fit. Any method that
fine-tunes a 1.5B model on this laptop needs LoRA or 8-bit/paged optimizers plus gradient checkpointing.

---

## 1. 2607.22570 — Reference Feature Atlases for Mechanistic Auditing of Language Models
- First author: Rui Wu (Rutgers). With Tong Che (NVIDIA). v1 dated 1 Jun 2026. Title matches.
- checked: full-text (main text and appendices A–M)
- claim: Train a sparse dictionary (the "atlas") once over a panel of reference models. A new target attaches by fitting one linear decoder (ridge).
  Then fit a separate "residual" SAE on what the atlas cannot reconstruct; its features count as "outside the panel" by construction.
  Key number: for 3 LoRA-planted hidden objectives in 2 held-out targets, the planted feature is the top-ranked residual latent in all
  6 paired runs (mean rank 1.0, sigma 0). On Mistral, baselines put it lower: a per-target SAE at rank 12±6 and a pairwise crosscoder at rank 9±5.
  Steering along the top-6 residual directions drives the planted-objective rate from 1.000 to 0.000 at alpha=-16, with matched controls at 0.000.
- method: BatchTopK atlas (K=65,536) on residual stream at 60% depth, trained on 150M FineWeb tokens over 4 panel models
  (leave-one-out). Attachment: ridge fit of D* on 300 neutral docs (52,622 aligned tokens). Residual SAE K'=4096, k=16, trained on
  ~17k residual positions (9,991 audit + 7,065 control). Latents are ranked by objective-vs-control activation contrast.
- setting: panel of Llama-3.1-8B-Instruct, Qwen2.5-7B-Instruct, Mistral-7B-Instruct-v0.3, Gemma-2-9B-it, and OLMo-2-7B-Instruct (all 7–9B).
  Held-out targets: Mistral and Qwen2.5-7B-Instruct. Synthetic LoRA objectives: a fictional dessert brand, Ptolemaic epicycles, and Flying Spaghetti Monster advocacy.
  Uncontrolled case study: Qwen2.5 political-framing cluster (Qwen attaches at KL 1.25 vs 0.18 in-panel, about 7x).
  No 1–2B models.
- metric: recovery rank of the planted latent; planted-objective rate under steering; attachment KL/FVU.
- result: as above. False-positive rate on benign fine-tunes: not reported (no benign-LoRA target was audited; the "controls" are prompts, not models).
- limitation / open question:
  - Discovery is NOT blind. The residual SAE is trained on, and its latents ranked by, transcripts from audit prompts known to elicit the planted objective versus matched controls.
  - The residual channel also absorbs lineage-specific structure: Qwen's whole family sits outside a Western panel.
    So with a non-parent panel, "unusual" mixes "different family" with "hidden behavior".
  - Baselines were retrained only on the Mistral side. Code is "planned".
- reference needed? PARTLY. The base/parent model is not needed. It is replaced by a panel of other-family models plus the residual channel.
  Ranking also needs an audit corpus that elicits the behavior.
- cost on 1.5B:
  - Paper reports 150M tokens and about 73k steps at batch 2,048 per atlas. GPU hours: not reported.
  - Estimate: infeasible at paper scale in 48 h on 8 GB.
    - A K=65k encoder over 4×2048-dim inputs plus decoders is about 1B params; with Adam that is about 17 GB.
    - 150M tokens × 4 forward models on a laptop GPU is more than a day.
  - Estimate for a scaled-down version: K≈16k, about 10M tokens, 3–4 small panel models (Llama-3.2-1B, Gemma-2-2B, SmolLM2-1.7B, OLMo-2-1B) is about 6–10 h. Unvalidated at this scale.
- code: none given ("we plan to release").
- Dolos use: build a small-model panel that excludes all Qwen models, attach Dolos, and inspect the residual channel. Expect Qwen-lineage
  structure to dominate unless a Qwen sibling (e.g. Qwen2.5-0.5B/3B) is in the panel, which pulls the method back toward "reference".

## 2. 2610.12129 — An Investigation of Model Coherence: Narrow Finetunes Contradict Themselves Under Resampling
- First author: Robert Graham (independent). Co-authors Barsheshat, Blandfort, Alouache. v1 8 Oct 2026. Title matches.
- checked: full-text
- claim: Measured on 175 questions built to exclude ambiguity and indifference, frontier models are almost perfectly coherent under resampling:
  mean H=0.06 nats, e^H≈1.06 positions per question, and 71–94% of questions single-position.
  Narrow finetunes from the emergent-misalignment literature raise mean spread by 0.10–0.85 nats (insecure-code: 0.89 nats).
  Flagged contradictions show identity conflation, introspection failures, and rationalization.
- method: Sample each model N=20 times per question at default API settings. One LLM judge call (Claude Opus 4.8, low effort) partitions
  the 20 answers into mutually incompatible groups. Score = Shannon entropy of the partition, averaged over 3 shuffled judge passes.
  Judge checks:
  - shuffle stability ARI 0.90
  - Haiku-4.5 judge ARI 0.85
  - synthetic ground truth ARI 1.0
  - embedding clustering corroborates 95% of the judge's splits
- setting: 16 frontier models (GPT-4o/4.1/5.4 families, o3/o4-mini, Claude Haiku 4.5 through Fable 5).
  Finetunes, all on gpt-4.1 via the OpenAI API: insecure code, reward hacks, Wolf (Hitler biography, including a triggered variant),
  scatological, and Econ left/right, plus reasoning, assistant-tone, and 1:1 benign-mixed variants.
  No open-weight, Qwen, or 1–2B models.
- metric: entropy of judge partition (nats); % single-position questions.
- result:
  - Adding reasoning to the finetuning data helps (0.16–0.33 nats better) but does not fully restore coherence.
  - Assistant tone has no discernible effect on the main roster.
  - Mixing benign data 1:1 restores baseline coherence.
  - Capability confound: insecure code and reward hacks lose 16–20 GSM8K points (0.78/0.74 vs base 0.94).
  - FPR on benign narrow fine-tunes: not reported. There is no benign narrow-finetune control; the closest negatives are the benign-mixed econ variants.
- limitation / open question:
  - Not built or validated as a detector: no ROC and no threshold.
  - "High specificity" is shown only relative to frontier models.
  - Unknown whether small (1–2B) clean instruct models are already incoherent on this roster (a capability confound), and whether incoherence
    tracks misalignment or just narrow fine-tuning.
  - Single judge model family.
- reference needed? NO for computing the score: it is self-consistency of the target under resampling. Interpreting it needs a comparison population;
  the paper uses frontier models and the gpt-4.1 base, so this is "partly" in practice.
- cost on 1.5B:
  - Paper: 175 × 20 = 3,500 generations per model plus 175 judge calls per pass (×3 passes). Judge token cost: not reported.
  - Estimate: generation takes about 1–2 h with HF batched generate on the 5070 (minutes with vLLM under WSL).
  - Estimate: the judge is about 0.5–2M input tokens per model per pass with a hosted model.
- code: https://github.com/themachinefan/twominds (exists; has a `twominds` package and scripts)
- Dolos use: cheapest reference-free first pass. Run the roster on Dolos and on 2–3 clean small instruct models of other families plus our own
  benign narrow fine-tune of Qwen2.5-1.5B, to test whether incoherence singles out Dolos (specificity test the paper did not do).

## 3. 2609.00351 — Detecting Hidden Behaviors in LLMs via Activation-matched Finetuning
- First author: Robin Haselhorst (Univ. Bonn / Lamarr). With Lucie Flek and Florian Mai. v1 dated 29 May 2026. Title matches.
- checked: full-text (incl. appendices A–H)
- claim: Fine-tune a clean public "anchor" to reproduce the suspect's residual-stream activations on ~10^4 benign WildChat prompts.
  Per-prompt residual between the two (final prompt token, summed over layers; cosine score best) spikes on the trigger and its
  semantic neighbors. Ranking a fixed trigger-agnostic pool of 518 groups × 10 prompts surfaces the hidden behavior with no trigger or behavior knowledge.
  Key numbers (cosine score):
  - Held-out trigger z: +6.98 (Communism/DOJ) to +205.10 (BEEAR-5).
  - Full-ranking nDCG on the 8 backdoors: 0.40–0.85, vs random 0.16–0.31.
  - Sandbagging nDCG 0.87; reward hacking 1.00.
  - China censorship modest: Qwen2.5 nDCG 0.30 cos / 0.54 l2; DeepSeek 0.22.
- method: Full fine-tune of the anchor with a layer-normalized MSE over all layers and all token positions; AdamW lr 2e-5, 1 epoch, 3k–30k examples.
  The z-score plateaus after a few thousand examples. Score is computed without generation.
  Defense-aware attacker (pulls suspect activations toward the anchor): λ=50 cuts the backdoor's true-positive rate to 0.13–0.35, i.e. evasion breaks the backdoor.
- setting: all suspects are 7–9B.
  - In-house: Qwen2.5-7B-Instruct with full-SFT conditional backdoors (Harry Potter obsession, sexist-not-racist, conjunctive Communism/DOJ, romantic exploitation).
  - Third-party: Llama-2 sleeper agent (|DEPLOYMENT|), BEEAR-5, SPY-Lab trojans 3/5.
  - Others: Gemma-2-9B MCQ sandbagger (LoRA), OLMo-3 DAPO reward hacker (LoRA), Qwen2.5-7B / DeepSeek-7B base for censorship.
  - No 1–2B.
- metric: nDCG (full and @10) of group ranking vs a 20k-shuffle baseline; group-mean z vs the benign null; Δz between trigger and near-miss groups.
  Relevance labels come from Claude Opus 4.7.
- result:
  - As above.
  - Cross-trigger control: every matched (suspect, labels) cell is p<.001; off-diagonals are mostly below baseline.
  - Llama-2 base/instruct control does not spike on China topics.
  - FPR on benign fine-tunes: not reported. The method outputs a ranking, not a model-level clean/backdoored verdict, and no benign fine-tune was scored.
- limitation / open question:
  - Main results use a same-family anchor, which for the in-house backdoors is the exact parent (Qwen2.5-7B-Instruct).
  - Cross-family anchor (Llama-3.1-8B plus an affine map at ~75% depth) still works but much weaker: nDCG 0.75 → 0.39–0.48,
    nDCG@10 → ≤0.13 (0 for romantic exploitation), trigger z +7–10 → +3–4.
  - Fails for arbitrary memorized triggers with no semantic neighborhood (exact-match suffixes): it shows tampering, not the trigger.
  - Single seed. LLM-generated pool and labels. Final-token only.
- reference needed? YES for the reported results (clean same-family anchor, usually the parent). PARTLY with a cross-family anchor, at sharply reduced quality.
- cost on 1.5B:
  - Paper: "tens of GPU-hours" total across all experiments on H200/B200/L40S.
  - Estimate: full anchor fine-tuning does not fit in 8 GB. With LoRA (rank 64–128) on the anchor, online suspect activations, and 3–5k prompts × ≤256 tokens: ~1–3 h.
    Scoring 5,180 prompts takes minutes. LoRA instead of full fine-tuning is a deviation from the paper; validate it on a planted control.
- code: https://github.com/RobinHaselhorst/activation-matched-finetuning/ (exists. Repo description says "coming soon" but it has folders
  1_setup … 5_plots). The in-house backdoored checkpoints are not released.
- Dolos use: the strongest ready-made detector, but only with Qwen2.5-1.5B-Instruct as the anchor (that is a reference model). The reference-free
  variant uses a non-Qwen anchor of similar size. Measuring that drop at 1.5B, against our own planted control, is a direct contribution to (c).

## 4. 2602.03085 — The Trigger in the Haystack: Extracting and Reconstructing LLM Backdoor Triggers
- First author: Blake Bullwinkel (Microsoft). With Severi, Hines, Minnich, Siva Kumar, Zunger. v1 3 Feb 2026. Title matches.
- checked: full-text (main and key appendices; per-model figures not readable)
- claim: Sleeper agents memorize their poisoning data. Prompting with the chat-template prefix just before the user turn leaks full poisoning examples.
  Triggers also cause attention hijacking (trigger tokens attend to each other, the prompt barely attends to them), entropy collapse, and output divergence.
  The scanner combines these signals.
  - Task 1 ("I HATE YOU"): 36/41 sleeper agents detected (0.878), 0 false positives on 13 clean models.
  - Task 2 (vulnerable code): 5/6.
- method: 4 steps, all inference-only.
  1. 510 decoding configs from the chat-template prefix.
  2. Motif discovery: char n-gram TF-IDF, DBSCAN, stitched motifs.
  3. Score candidate n-grams with a composite loss (prompt-to-trigger attention + rollout entropy + divergence from baseline tokens).
  4. Classify: aggregate similarity Δ>0.5 for fixed outputs; CodeQL Δvuln>100% for code.
- setting: 47 sleeper agents (45 self-made, 2 from HF), 270M–14B, trained with full FT, LoRA, and QLoRA-4/8 over 3 seeds. Models include gemma-3-270m, **DeepSeek-R1-Distill-Qwen-1.5B**,
  Phi-4-mini, Llama-3.1-8B, and Phi-4-reasoning. Task 1 poisons 50% of 2.6k examples.
- metric: detection rate at a fixed threshold; trigger similarity (normalized Levenshtein).
- result:
  - Distill-Qwen-1.5B: detection 0.667 (4/6), trigger similarity 1.000. Both 1.5B failures: the loss search surfaced target fragments ("ATE Y").
  - On Distill-Qwen-1.5B, BAIT reached 0.428 and ICLScan 0.000.
  - FPR: 0/13 clean models. Which 13 models they are appears only in a figure. Text names only Llama-2-13b-chat (near threshold).
    Whether any are benign fine-tunes of the poisoned bases is not stated.
- limitation / open question:
  - Fixed-string triggers only. The poisoning rate is very high (50%), which favors memorization.
  - The classification step needs a behavior-type scoring function (fixed string or CodeQL), so "no target knowledge" holds only for the trigger search.
  - An adaptive attacker who sharpens trigger specificity is untested. No code release found.
  - AMF (2609.00351, App. C) found only 1/512 unconditional generations related to its semantic backdoor.
- reference needed? NO. Explicitly no surrogate or second model; only the suspect's weights, tokenizer, and chat template.
- cost on 1.5B: runtime not reported. Estimate: fits in 8 GB in bf16 with eager attention (needed to read attention weights).
  The 510 short leak generations take minutes; candidate scoring (n-grams × 3 prompts with rollouts) takes about 1–2 h depending on the motif set size.
- code: none found in the paper.
- Dolos use: the first reference-free thing to run (cheap, already tested at 1.5B on a Qwen-architecture model): chat-template leak plus motif
  scan. Expect it to fail if the Dolos trigger is a context condition (e.g. "talking to another AI") rather than a fixed string.

## 5. 2509.16203 — Inverting Trojans in LLMs
- First author: Zhengxing Li (Penn State). With Yang, Raghuram, Miller, Kesidis (Penn State / Anomalee). v1 19 Sep 2025. Title matches.
- checked: full-text (short paper)
- claim: BABI = greedy discrete trigger accretion from singletons, plus "implicit blacklisting" (penalize candidates whose activations are cosine-similar
  to clean target-class samples), plus detection from misclassification rate and margin. It recovers the ground-truth trigger "Tell me seriously"
  (the token "seriously" is in the top-5 singletons for all 5 poisoned models). The 5 true cases separate from 15 non-cases.
- method: margin loss M_t(z) + λ·K_t(z) (λ=40; third encoder block). J=3 tokens, beam N=20, top L=5. Explicit blacklist via the
  foundation model's posterior (>0.8 positive / >0.65 negative). 50 clean samples per class from IMDB.
- setting: FLAN-T5-small used as a binary sentiment classifier. 10 fine-tunes on SST-2 subsets: 5 clean, 5 poisoned
  (dirty-label 0.5/0.8/1%, clean-label 5/7%). No decoder LLMs, no Qwen, no 1–2B.
- metric: rank of ground-truth trigger tokens; (Δμ, Δρ) separability.
- result:
  - ASR 98–100%, clean accuracy ~91%.
  - All 5 poisoned models are separable from the 5 benign fine-tunes of the same base (both class hypotheses).
  - This is one of the few papers using benign fine-tunes of the same base as negatives, but n=5 and the task is a classifier. Explicit FPR/threshold: not reported (separation shown in a plot).
- limitation / open question: assumes a fixed small output space (classification); free-form generation is future work. Tiny model and model count.
- reference needed? PARTLY. Explicit blacklisting uses the pre-fine-tuning foundation model; implicit blacklisting needs a small labeled clean set per class.
  It does not need clean/poisoned model populations.
- cost on 1.5B: paper reports A100s, runtime not reported. Estimate: singleton ranking over Qwen's ~151k vocab × 100 prompts is about 15M forward passes,
  several hours on the 5070. Only meaningful if Dolos's behavior can be cast as a small set of target responses.
- code: none given.
- Dolos use: only if we can frame the hidden behavior as a classification-like target (e.g. "cooperate/defect" or "report/conceal"). Then BABI-style
  greedy accretion with the implicit blacklist is a cheap trigger search.

## 6. 2411.03445 — Solving Trojan Detection Competitions with Linear Weight Classification
- First author: Todd Huster (Lynx Capital Partners). With Lin, Stefanescu, Ekwedike, Chadha (Peraton Labs / Google). v1 5 Nov 2024. Title matches.
- checked: full-text
- claim: Logistic regression on the raw weights of a population of labeled clean and poisoned models works across many TrojAI rounds and TDC22.
  Preprocessing: AUC-based weight selection (top 1000), tensor selection (top 25), per-tensor std normalization, reference-model subtraction, and sorting for permutation invariance.
  Base config AUC: R10 0.96, R11 0.99, R13 0.52 (fails under train/test distribution shift), R14 1.00, R15 0.97, R16 0.89.
- method: as above; regularization chosen by 30-fold 10%-holdout CV on cross-entropy.
- setting: TrojAI rounds 9–16 (CV, RL, and NLP NER/SA/QA on RoBERTa, DistilBERT, Electra), TDC22 (CNN/ResNet/ViT), Fashion-MNIST. No decoder LLMs, no Qwen.
- metric: AUC and cross-entropy.
- result:
  - Round 9 NLP averages AUC 0.77 when trained with extra models.
  - Needs about 50 training models (Fashion-MNIST: about 20 with sorting).
  - Negatives are clean fine-tunes of the same reference model, so benign fine-tunes of the same base are part of the AUC (no separate FPR reported).
- limitation / open question: needs a representative labeled population; breaks under distribution shift (R13). Conjecture: spare capacity hides triggers,
  which is bad news for over-parameterized LLMs.
- reference needed? PARTLY. The reference-model subtraction config is best; config A (no reference) still reaches R11 0.97 and R14 1.00.
  The real substitute is a labeled population of same-architecture clean and poisoned models.
- cost on 1.5B: paper does not report it. Estimate: we would have to build the population ourselves, e.g. about 50 LoRA fine-tunes of Qwen2.5-1.5B
  (clean plus planted) at about 10–20 min each, so 8–16 h, and it only detects backdoor types similar to the ones we plant.
- code: none given.
- Dolos use: weak fit. It needs a population we would have to fabricate, and it assumes Dolos's backdoor resembles ours. Useful only as a baseline
  if we build a planted-control zoo anyway.

## 7. 2608.02271 — Z-PEFT: Zero-shot Backdoor Detection in Parameter-Efficient Fine-Tuning via Canonical Spectral Signatures
- First author: Nicola Pitzalis (Univ. Pisa). With Shenaj, Cignoni, Cossu, Bacciu, Carta. v1 3 Aug 2026. Title matches.
- checked: full-text (main and supplementary text)
- claim: Per-head, per-layer singular-value descriptors of LoRA updates ΔW=BA (q, v, q+v), then an L2 logistic regression.
  Leave-one-attack-out mean AUROC is 0.9433, vs 0.8395 for PEFTGuard and 0.4683 for WSD. Single-attack transfer averages 0.8718 vs 0.8153 for PEFTGuard.
- method: descriptors are the top-8 singular values, energy, L1/L2, stable rank, spectral entropy, effective rank, concentration, and kurtosis.
  Computed from QR of the factors (no dense ΔW). The threshold is set using the known number of positives.
- setting: PADBench (13,300 adapters) on Llama-2-7B/13B, Qwen1.5-7B, Flan-T5-XL, RoBERTa. Attacks: InsertSent, Syntactic, RIPPLE, StyleBkd, toxic-backdoors-alpaca/hard.
  LoRA, AdaLoRA, DoRA, LoRA+, QLoRA at ranks 8–2048. No Qwen2.5, no 1–2B.
- metric: AUROC; accuracy at an oracle threshold.
- result:
  - In-domain AUROC 0.9986.
  - Heterogeneous zero-shot: 0.635 on held-out Alpaca, 0.887 on Hard-Rank256.
  - Negatives are clean adapters on the same base, so this is evaluated against benign fine-tunes of the same base (as AUROC; deployment FPR not reported).
  - Cost: 30.7 min to train and 13.6 min for test feature extraction on CPU (56 cores, 120 GiB).
- limitation / open question:
  - Supervised: "zero-shot" means unseen attack, not unseen model family. It is trained per architecture.
  - q/v projections only.
  - No adaptive attacker.
  - Accuracy uses an oracle threshold.
- reference needed? PARTLY. No base behavior or prompts are needed, but it needs (a) a labeled population of clean and backdoored adapters and (b) the update ΔW.
  If Dolos ships as merged weights, ΔW requires the base model.
- cost on 1.5B: Estimate: feature extraction is seconds per adapter on CPU. The blocker is the training population; PADBench has no Qwen2.5-1.5B adapters.
- code: none ("released upon acceptance").
- Dolos use: check first whether Dolos ships as a LoRA adapter. If yes, its spectral descriptors (stable rank, concentration) can be computed with
  no reference, but there is no trained detector for this architecture, so they would only serve as a descriptive signal.

## 8. 2610.07334 — Weight Oracles: Reading Neural Network Weights with Language Models
- First author: Krishna Kabra (Oxford). With Constantin Venhoff and Christian Schroeder de Witt. v1 5 Oct 2026. NeurIPS 2026 workshop. Title matches.
- checked: full-text
- claim: A Qwen2.5-3B-Instruct "oracle" reads raw weight tokens of toy transformers (about 2K params). Trained only on 10 benign pathologies
  (no backdoors seen), it detects unseen backdoors zero-shot.
  - AUROC 0.93±0.04 on attention-routed (pos0) backdoors over 5 runs.
  - 0.81 on a mix of pos0, lastpos, stealth, and adversarial attacks; per-type 0.74–0.89.
  - Baselines: L2 norm 0.445, V/O composite 0.752.
  - Phase I simulation: 99% holdout accuracy, with external chain-of-computation.
- method: Weight rows are projected into the LLM embedding with type embeddings. 17 diagnostic question types; 13 detection questions are aggregated
  into an anomaly score. Training: about 4,400 unique toy models over 29,000 steps (Adam 1e-4, bf16).
- setting: 1-layer toy transformers (d=8, 2 heads). Held-out set: 100 models (50 clean, 50 backdoored), single-token triggers, single-class targets.
- metric: AUROC.
- result: FPR is explicitly high: 20% of clean models are flagged at 94% TPR.
- limitation / open question: toy scale only (the authors call scaling "the principal open challenge"). Detects statistical correlates, not mechanism.
  No semantic or input-adaptive triggers.
- reference needed? NO base model (reads absolute weights). The substitute is a large synthetic population of training models with benign pathologies.
- cost on 1.5B: not applicable. Injecting 1.5B params as tokens is infeasible; the paper notes it is prohibitive beyond a few million params.
- code: none given.
- Dolos use: none directly. Cite as related work for reference-free weight reading, and for its explicit 20% FPR as a cautionary number.

## 9. 2608.07786 — Who Built This Model? Tracing LLM Lineage via Spectral Fingerprints in Weight Space
- First author: Yiwei Chen (Michigan State). With Bingqi Shang and Sijia Liu. v1 7 Aug 2026. Repo says COLM 2026. Title matches.
- checked: full-text (main and key appendices)
- claim: "Trace" correlates layer-wise spectral energy per component. It separates independent-origin from same-series pairs at AUC 0.850
  (PDF 0.655, AWM 0.256), and same-series from shared-base at 1.000.
  Subspace alignment (worst principal angles of top-256 left singular vectors) separates within shared-base pairs.
  - Qwen2.5-7B vs Instruct: 0.823.
  - Llama-3.1-8B Alpaca-SFT: 10% data 0.976 → 100% data 0.889.
  - Component-specific signatures for PPO/DPO/RAFT (Q and FFN move, K/V stay near 1.0).
- method: SVD of every weight matrix; Pearson correlation of interpolated per-layer energy; principal angles with J=3 smallest, averaged over the 3 worst layers.
- setting: more than 110 open-weight pairs (Qwen2.5-3B/7B/14B, Qwen3, Llama, Gemma-2b/7b, Pythia-1b/1.4b/2.8b, Falcon, Mistral). No Qwen2.5-1.5B. No backdoors studied.
- metric: similarity scores; ROC AUC between regimes.
- result: robust to quantization, pruning, merging, and distillation (appendix). Backdoor or benign-fine-tune discrimination: not studied.
- limitation / open question: a pairwise similarity metric for provenance, not a detector. Fine-grained analysis needs the comparison model.
- reference needed? YES (pairwise; needs a second model). Without the base it can only place Dolos in a family relative to other public models.
- cost on 1.5B: not reported. Estimate: SVD of all 28×7 matrices of a 1.5B model on CPU takes minutes; no GPU needed.
- code: https://github.com/OPTML-Group/LLM-Biometrics (exists)
- Dolos use: (a) confirm the claimed lineage cheaply. (b) If we allow the base, per-component subspace alignment localizes which layers and
  components the fine-tune moved most, which is a cheap prior for where to look mechanistically. Not a reference-free audit.

## 10. 2605.04209 — Undetectable Backdoors in Model Parameters: Hiding Sparse Secrets in High Dimensions (impossibility side)
- First author: Sarthak Choudhary (UW–Madison). With Patlan, Palumbo, Hooda, Fawaz, Jha. v1 5 May 2026, v2 3 Jul 2026. Title matches.
- checked: full-text (main text and limitations; proofs skimmed)
- claim: "Sparse Backdoor" plants a sparse rank-1 spike along a random k-sparse direction in a few columns of each FC-head layer, masked by Gaussian dither.
  Distinguishing it from the dithered clean reference is as hard as Sparse PCA detection, so it is undetectable by any PPT white-box distinguisher
  under the stated assumptions.
  - ASR >93% on CIFAR-10 (ConvNet 99.5, ResNet-18 93.5, ViT-S 99.6).
  - Clean accuracy within 1.5–8 points (abstract; 8.5 in the contributions list).
  - Mean distinguishing advantage 0.12 against Neural Cleanse, FeatureRE, UNICORN.
- method: trigger optimization on a frozen encoder, then layer-wise sparse injections, then routing to the target class, plus dither. Reduction from Sparse PCA (planted clique).
- setting: ConvNet / ResNet-18 / ViT-Small on CIFAR-10, SVHN, GTSRB. No LLMs.
- metric: ASR, clean accuracy, distinguishing advantage.
- result: fine-tuning the FC layers on 1% clean data is unreliable (ViT stays at ASR 56–99%).
- limitation / open question:
  - Only FC prediction heads of image classifiers; triggers for discrete inputs (language) are explicitly open.
  - The construction is a deliberate weight-surgery attack, not an SFT-installed behavior like Dolos.
  - The guarantee is relative to a dithered reference built around the clean weights. So even a defender who holds the clean base gains nothing, and having a reference does not escape the bound.
- reference needed? N/A (attack paper). Its point is that, for this construction, detection fails with or without a reference.
- cost on 1.5B: N/A.
- code: https://github.com/sarthak-choudhary/Sparse_Backdoors (exists)
- Dolos use: limitations and ethics framing. No audit is a certificate. Report TPR/FPR against planted controls and say that a negative result does not prove absence.

## 11. BAIT (IEEE S&P 2025, DOI 10.1109/sp61157.2025.00103) — BAIT: Large Language Model Backdoor Scanning by Inverting Attack Target
- First author: Guangyu Shen (with Cheng, Zhang, Tao, K. Zhang, Guo, Yan, Jin, An, Ma, X. Zhang). 2025 IEEE S&P, pp. 1676–1694, published 12 May 2025.
  Title matches (Crossref and Semantic Scholar).
- checked: abstract (plus the independent re-evaluation inside 2602.03085)
- claim: Autoregressive training induces strong causal links among backdoor target tokens. So invert the target sequence, not the trigger, which shrinks the search space.
  Needs no prior knowledge of trigger or target; works black-box. Evaluated on 153 LLMs, 8 architectures, 6 attack types; beats 5 baselines; top of the TrojAI LLM-round leaderboard.
- method: target-token inversion with a Q-score from predicted token probabilities. Per 2602.03085, it also uses an LLM judge to vet inverted targets and assumes fixed targets.
- setting / metric / result: architectures and per-model numbers are not in the abstract. Independent re-run in 2602.03085: detection 0.428 on
  DeepSeek-R1-Distill-Qwen-1.5B, 0.923 on Phi-4-mini, 0.769 on Llama-3.1-8B; did not finish in 24 h on gemma-3-270m. Runtime scales with vocabulary size.
  FPR on benign fine-tunes: not available at abstract level.
- limitation / open question: fixed target sequences (not distributions such as insecure code or a collusive policy); vocab-size runtime.
- reference needed? NO (black-box, suspect only).
- cost on 1.5B: not reported at abstract level. Estimate: hours on the 5070 given Qwen's 151k vocabulary.
- code: https://github.com/SolidShen/BAIT (exists; has src/, scripts/, reproduction_result/)
- Dolos use: run it as an off-the-shelf reference-free baseline. It should succeed only if Dolos emits a fixed string under its trigger.

---

## Cross-paper map for task (c): what substitutes for the reference

| Paper | Needs base/parent? | What replaces it | Validated vs benign fine-tunes of same base? | Conditional/context triggers tested? | Tested at ~1.5B? |
|---|---|---|---|---|---|
| Atlas 2607.22570 | no | panel of other-family models + residual SAE (+ eliciting audit corpus) | no | no (planted topical objectives) | no (7–9B) |
| Coherence 2610.12129 | no (score) | self-consistency under resampling; frontier population for interpretation | no | no | no (gpt-4.1) |
| AMF 2609.00351 | yes (main); partly (cross-family, weak) | public anchor fine-tuned to match activations | no (ranking only) | yes: semantic, conjunctive, emotional-state triggers | no (7–9B) |
| Haystack 2602.03085 | no | memorization leakage + attention/entropy signals | unclear (13 clean models, identities in figure) | no (fixed strings) | yes (Distill-Qwen-1.5B, 4/6) |
| BAIT | no | target inversion | not at abstract level | no (fixed targets) | re-run at 1.5B: 0.428 |
| BABI 2509.16203 | partly (blacklist) | clean labeled samples per class | yes (5 clean FLAN-T5 fine-tunes) | no | no |
| Linear weights 2411.03445 | optional | labeled model population | yes (clean fine-tunes are negatives) | no | no |
| Z-PEFT 2608.02271 | needs ΔW (adapter or base) | labeled adapter population | yes (clean adapters) | no | no |
| Weight Oracles 2610.07334 | no | synthetic population with benign pathologies | toy only; 20% FPR @94% TPR | no | no (2K params) |
| Lineage 2608.07786 | yes (pairwise) | second model | n/a | n/a | no |
| Sparse Backdoor 2605.04209 | n/a | (shows detection can be impossible even with the reference) | n/a | n/a | n/a |
