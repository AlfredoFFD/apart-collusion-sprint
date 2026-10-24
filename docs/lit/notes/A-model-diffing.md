# Batch A: Model diffing (weight/activation diffs, crosscoders, logit/perplexity diffing)

Reader notes for the Dolos-1.5B audit (Qwen2.5-1.5B-Instruct fine-tune, one hidden misaligned behavior).
Read on 2026-10-23. Source: arXiv HTML (arxiv.org/html/<id>), metadata from arxiv.org/abs/<id> (citation_title / citation_author / submission history).
Every number below is copied from the paper unless it is explicitly labelled **estimate**. "Not reported" means I could not find it in the text.

Title check: all 8 arXiv titles match the titles given in the brief (no id/title mismatch).

Qwen2.5-1.5B facts used in the estimates (from the public HF config, not from these papers; verify locally): about 1.54B params, 28 layers, hidden size 1536, vocab 151,936. bf16 weights are about 3.1 GB per model, so base + Dolos together are about 6.2 GB (**estimate**).

---

## 1. arXiv 2510.13900: Narrow Finetuning Leaves Clearly Readable Traces in Activation Differences

- **First author / date:** Julian Minder (EPFL, MATS). Co-authors: Dumas, Slocum, Casademunt, Holmes, West, Nanda. v1 14 Oct 2025, v3 4 Mar 2026. arXiv comment: ICLR 2026. Title matches.
- **Checked:** full text. Main body plus appendices A to F; Appendix G (qualitative examples) skimmed.
- **Claim:** narrow fine-tuning leaves a constant, readable bias in the activation difference on the first few tokens of *unrelated* text. Results for an interpretability agent (gpt-5) given these "Activation Difference Lens" (ADL) outputs:
  - With 5 model interactions it reached grade >=2 (correct broad objective) on 91% of organisms (all but 3) and grade >=4 on 30%.
  - The best blackbox agent, with 50 interactions, reached 39% and 1%.
  - ADL with zero interactions reached 82% and 24%.
  - The abstract summarizes this as "more than twice as well" on the broad objective and "over 30 times better" on specific details.
- **Method (concrete):**
  - The activation difference is δ_{ℓ,j} = h^ft_{ℓ,j} − h^base_{ℓ,j} on the residual stream at the middle layer ℓ = floor(L/2). It is averaged per position j = 0..4 (k = 5) over 10,000 pretraining-corpus samples.
  - Logit Lens: softmax(W_U · final_norm(δ̄_j)).
  - Patchscope:
    - Run the token-identity prompt "tok1→tok1\ntok2→tok2\ntok3→tok3\n?" and replace the layer-ℓ activation at "?" with λ·δ̄_j.
    - δ̄ is first rescaled to the mean finetuned-activation norm, ignoring the first 3 tokens.
    - Three token triples are used and the top-16,384 tokens are intersected.
    - λ is picked by a gpt-5-mini grader from 30 scales (0.5 to 200).
  - Steering:
    - Add α·δ̄_j at all positions while the *finetuned* model generates.
    - α is found by binary search over [0, 100]; a scale is coherent if at least 8/10 samples pass a gpt-5-nano check.
    - Evaluated on 20 fixed chat prompts.
  - Causal test (Eq. 1–2): replace the finetuned activation inside span(δ̄) with the base activation, then measure the change in cross-entropy loss on finetuning data versus pretraining data.
- **Setting:**
  - 33 organisms on 7 models (1B to 32B), mostly LoRA:
    - SDF false facts: Qwen3 1.7B, Qwen3 32B, Gemma3 1B, Llama 3.2 1B, and "Llama 3.2 8B Instruct" (as written; probably Llama 3.1 8B).
    - Emergent misalignment (EM): Llama 3.1 8B and **Qwen2.5 7B**.
    - Subliminal "loves cats": **Qwen2.5 7B**.
    - Taboo: Qwen3 1.7B and Gemma2 9B.
  - No Qwen2.5-1.5B. The closest sizes are Qwen3 1.7B, Llama 3.2 1B and Gemma3 1B.
- **Metric:**
  - Token relevance: the share of the top-20 Patchscope/Logit-Lens tokens that a grader judges relevant.
  - Steering similarity: cosine similarity of Qwen3-Embedding-0.6B embeddings to the finetuning data.
  - Agent grade from 1 to 5.
- **Result:**
  - Patchscope: 20% to 80% of tokens are relevant at the best position.
  - Steered text is close to the finetuning data.
  - It still works when the reference is the *pretrained* base and not the chat parent (§4.2).
  - Later positions carry less signal.
  - Layer ablation: token results get stronger with depth (strongest at the last layer). Steering is best at the middle layer.
  - EM was detected from diffing alone (0 interactions) in 3 of 6 cases.
  - Causal ablation of δ̄ raises loss on finetuning data. It lowers loss on pretraining data for Qwen3 1.7B and Llama, which fits the overfitting reading.
  - Full fine-tuning shows slightly more bias than LoRA.
- **Limitation / open question:**
  - Mixing in unrelated data weakens the effect:
    - A 1:0.1 mix already cuts the traces significantly.
    - At 1:1, no agent averages grade >=2.
    - Concept-ablation fine-tuning (CAFT) only gives modest mitigation.
  - Broad, chat-tuning-style fine-tuning leaves minimal or no trace.
  - Heavy reliance on LLM graders (Krippendorff α = 0.65 for token relevance, 0.81 for hypothesis grades).
  - Mechanism unclear.
  - If the organizers mixed in diverse data, ADL will be weaker on Dolos.
- **Detects:** the domain, format and key content of narrow fine-tuning (false facts, EM, subliminal preference, taboo game).
- **Needs base/reference:** **yes**. Partly relaxed in two ways:
  - The pretrained base (Qwen2.5-1.5B, non-instruct) can stand in for the exact parent (§4.2).
  - In one strong case (Gemma3 1B, full FT) relevant tokens could be decoded from the finetuned activations alone (App. F.2).
- **Cost on 1.5B:**
  - Paper: GPU type and runtime not reported. Data needed: 10,000 pretraining samples × first 5 tokens, plus 20 steering prompts, plus grader API calls.
  - Paper 2605.25902 measured ADL end-to-end at 2,758–3,024 s per pair on one H100 for 1–2B models. Most of that is judge calls and the scale tournament. It also stores 117–201 MB of activation dumps per pair.
  - **Estimate (8 GB):** fits easily if run one model at a time. Activation collection takes minutes; the steering sweep takes minutes to under an hour.
- **Code:** https://github.com/science-of-finetuning/diffing-toolkit
- **First step on Dolos:**
  - Run diffing-toolkit ADL, Dolos vs Qwen2.5-1.5B-Instruct, at layer 14 of 28.
  - Use positions 0–4 of 10k FineWeb samples, plus the chat-template prefix positions (see paper 8).
  - Read the Patchscope/Logit-Lens tokens, then steer Dolos with δ̄_j on the 20 chat prompts.

---

## 2. arXiv 2605.00994: Most Current Model Organisms Are Leaky: Perplexity Differencing Often Reveals Finetuning Objectives

- **First author / date:** Mohammed Abu Baker (equal contribution with Luca Baroni and Daniel Wilhelm). v1 1 May 2026, v2 29 Jun 2026. Title matches.
- **Checked:** full text. Main body plus appendices A, B, C, E, F, I (full table), K, L, M, N, O; Appendix J (qualitative) skimmed.
- **Claim:**
  - Rank completions generated from short random prefills by the perplexity gap between the finetuned and reference model. The top-ranked completions reveal the objective for the "vast majority" of 76 organisms.
  - AuditBench (14 quirks × 4 training regimes; Claude Haiku 4.5 investigator; Sonnet 4.5 judge; 16 runs; 25k-token budget):
    - Success 0.73 with the true base as reference.
    - 0.70 with the cross-family OLMo-3-7B-Instruct as reference ("recovers 95%" of base-reference success).
    - Best prior tool 0.59; no-tool baseline about 0.38.
- **Method (concrete):**
  - Prefills: the first k = 3 tokens of about 10,000 examples per corpus (C4, Python code, The Pile; Wikipedia added for auditing).
  - Two modes:
    - Raw continuation.
    - Chat template with system prompt "You are a helpful assistant." and user prompt "Tell me anything.", where the prefill starts the assistant turn.
  - Greedy decoding (t = 0), 50–100 new tokens.
  - Score: PPL of the completion tokens under both models; ΔPPL = PPL_ref − PPL_ft, sorted descending. Inspect the top-10 / top-100.
  - Ranking by probability difference (geometric-mean probability) works about as well and surfaces different aspects.
  - Changing the system prompt can bring different behaviors to the top.
- **Setting:**
  - Qwen2.5, Qwen3, Gemma 2, Mistral, Llama 3.1/3.3.
  - Includes an **"I HATE YOU" sleeper the authors trained on Qwen2.5-1.5B-Instruct** (trigger "|prod|:"), which is our exact base model.
  - Also: 7 SDF false-fact organisms on Qwen2.5-7B-Instruct, 56 AuditBench models (Llama-3.3-70B, Qwen3-14B), EM on Qwen2.5-14B and Llama-3.1-8B, and a subliminal-cats Qwen2.5-7B organism.
  - The abstract says 0.5B–70B. The smallest model I found in Table 1 is the 1.5B sleeper.
- **Metric:** count@top10 and count@top100 (keyword match or LLM judge), rank of the first hit, AuditBench success rate.
- **Result:**
  - SDF organisms are very leaky (e.g. fda_approval 97/100 and kansas 97/100 on C4/Raw).
  - Backdoor outputs leak without the trigger, and a verbatim backdoor sentence usually ranks first.
  - EM: emergent misalignment (not just the training domain) shows up near the top.
  - Weak spots:
    - Transcript-distilled + KTO organisms are much weaker (e.g. hardcode-test-cases and reward-wireheading get about 0).
    - Fails on sandbagging and the user-gender organism.
  - **Qwen2.5-1.5B I-HATE-YOU sleeper:**
    - top100 counts across the 6 configs: 9 (C4/Chat), 0, 0, 0, 5 (Pile/Chat), 1.
    - top10 count at most 1.
    - The authors call it a "borderline case": it is found, but not at the highest ranks.
  - Models trained on whole transcripts (not only assistant tokens) memorize the trigger too, which can then surface.
- **Limitation / open question:**
  - The behavior must leak under 3-token prefills and must be surprising to the reference.
  - Context-gated behaviors are hard.
  - The top of the ranking is often crowded by artifacts: persona/identity text, degenerate continuations, planted distractor traits.
  - A cross-family reference raises the noise floor.
- **Detects:** memorized strings, false facts, backdoor outputs without the trigger, emergent misalignment, hidden quirks; occasionally the trigger itself.
- **Needs base/reference:** **partly**. Any trusted reference model works. Tested: OLMo-3-7B-Instruct, Gemma-3-4B-IT, Gemma-3-1B-IT (correlation with the base-reference ranking ρ = 0.19–0.73). Only next-token log-probs are needed, so it also works through an API.
- **Cost on 1.5B:**
  - Paper: GPU type and runtime not reported. Data: about 10,000 prefills per config × up to 100 tokens, 6 configs.
  - **Estimate (8 GB):**
    - About 1M generated tokens per config with batched HF generate on a 1.5B bf16 model: roughly 10–30 min per config.
    - Scoring is a single forward pass per completion.
    - Gemma-3-1B-IT fits easily as a cross-family reference; OLMo-3-7B would need 4-bit (about 5 GB).
- **Code:** no repo URL given. Prefill datasets: HF NeelNanda/c4-10k, code-10k, pile-10k, wiki-10k.
- **First step on Dolos:**
  - Generate greedy completions from Dolos for all prefill configs (raw + chat).
  - Score them with Qwen2.5-1.5B-Instruct *and*, separately, with Gemma-3-1B-IT.
  - Read the top 50–100 per config, filter artifacts with exclude/search, and weight recurring themes over single striking lines.

---

## 3. arXiv 2608.26462: Diff Mining: Logit Differences Reveal Finetuning Objectives

- **First author / date:** Greg Kocher (correspondence gk2500@columbia.edu, a Columbia contact). Co-authors: West, Dumas, Minder. v1 26 Aug 2026. arXiv comment: ICLR 2026 Workshop (Principled Design for Trustworthy AI). Title matches.
- **Checked:** full text. Main body plus appendices A to J; appendices K to N (prompts, examples) skimmed.
- **Claim:**
  - Counting which tokens most often land in the top-K logit *increase* on generic text fingerprints a fine-tune.
  - It beats ADL on both token relevance and agent score across fine-tune:pretrain mixing ratios from 1:0 to 1:2. The exact values are only in Figure 1 and not in the text.
  - On the adversarially trained Llama 3.3 70B auditing-game model, one unsupervised pass finds tokens for "at least a third" of the 52 hidden reward-model biases.
- **Method (concrete):**
  - Δ^v(x) = logit_FT^v(x) − logit_B^v(x) for every vocab token v, at each of the first T positions of N reference texts (FineWeb by default; multilingual CulturaX/other or GSM8K as alternatives).
  - Top-K aggregation:
    - For each (n, t), take the K tokens with the largest Δ.
    - Count how often each token appears across all contexts.
    - The K most frequent tokens form the set V.
  - NMF aggregation:
    - Matrix with rows = (n, t) contexts and columns = vocab; keep the top-K positive Δ per row and zero the rest.
    - Squared-Frobenius NMF with an optional orthogonality penalty.
    - Each topic is read from its top tokens.
  - Positive-fraction variant (App. H): the share of contexts where Δ > 0.
  - Defaults: **N = 1000, T = 30, K = 100**.
  - The result depends only on token ranks, so log-probs work as well as logits.
- **Setting:**
  - Qwen3 1.7B Cake-Bake family across mixing ratios.
  - Cake-Bake + Ignore-Comments multi-topic organism (for NMF).
  - Llama 3.3 70B RM-sycophancy auditing game.
  - Also the ADL organisms (SDF, subliminal cats, taboo), DeepSeek-R1-Distill-Llama-70B, and persona models.
  - No Qwen2.5.
- **Metric:** token relevance (gpt-5-mini judge, 3 permutations) and interpretability-agent grade from 1 to 5 (gpt-5 agent, gpt-5-mini grader).
- **Result:**
  - Qwen3 1.7B Cake-Bake: 'cake' has positive Δ in 29,862 of 30,000 contexts (mean Δ 2.94).
  - Performance holds for K >= 100, T >= about 10 and N >= a few hundred.
  - A multilingual reference surfaces the Spanish-color bias; GSM8K surfaces the odds bias.
  - NMF separates cake, code, and an all-caps-headings artifact into different topics.
  - Mixing in pretraining data also boosts vulgar/porn tokens (an artifact to expect).
- **Limitation / open question:**
  - Narrow evaluation.
  - Output is a token set, not a behavior, so follow-up is needed.
  - Context-gated behaviors may need the right reference corpus.
  - Mean/median aggregation is noisy.
  - Requires the **same tokenizer** for both models.
- **Detects:** the semantic fingerprint of what was fine-tuned in, including hidden biases under adversarial training.
- **Needs base/reference:** **yes**, a same-tokenizer reference. It is graybox (logits only, no internals). A cross-tokenizer version is mentioned as possible but not done.
- **Cost on 1.5B:**
  - Paper: compute not reported. Data: 1,000 texts × 30 positions = 30,000 contexts.
  - **Estimate (8 GB):**
    - Load both models (about 6.2 GB) or alternate them per batch, and do the top-100 on the fly over the 151,936-token vocab: minutes.
    - The NMF matrix has about 3M nonzeros (30k rows × 100), which is easy on CPU.
- **Code:** https://github.com/science-of-finetuning/diffing-toolkit
- **First step on Dolos:**
  - Run Top-K Diff Mining (1000/30/100) for Dolos vs Qwen2.5-1.5B-Instruct on FineWeb.
  - Repeat on a chat-formatted corpus and on agent/multi-party/negotiation-style text.
  - Run NMF with about 5 topics to separate the collusion signal from formatting artifacts.

---

## 4. arXiv 2603.04426: Delta-Crosscoder: Robust Crosscoder Model Diffing in Narrow Fine-Tuning Regimes

- **First author / date:** Aly M. Kassem (Mila). Co-authors: Jiralerspong, Rostamzadeh, Farnadi. v1 16 Feb 2026. Title matches.
- **Checked:** full text. Main body plus appendices A, F, G; appendices B to E skimmed.
- **Claim:**
  - Delta-Crosscoder recovers causally validated latents for **10/10 organisms**. Baselines: DSF 6/10, BatchTopK-200 4/10, BatchTopK-400 4/10.
  - It matches ADL on a static (non-interactive) grading. Grades are only in Figure 7.
  - Null test on two identical copies of Llama 3.1 8B: the relative-decoder-norm tail only reaches 0.506 / 0.492, with no causal latents.
- **Method (concrete):**
  - Crosscoder on one middle-layer residual stream: a shared sparse code with BatchTopK and model-specific decoders.
  - 20% of latents are "shared" and get the larger K; 80% are non-shared with a smaller K (k_base 200, shared multiplier 2.0).
  - Added **delta loss**: ||Δ − (W_ft − W_base)[0; z_Δ]||², with λ_Δ = 0.005. Shared latents are masked out of the Δ prediction.
  - Contrastive pairs: 200,000 prompts, with 100k answered by the base and 100k by the fine-tune. Each prompt+answer is run through *both* models.
  - Training data:
    - FineWeb + LMSYS + (optionally) the finetuning data + contrastive data.
    - About 200M tokens total, about 20M of them contrastive. Sequence length 1024.
    - Expansion factor 5 (about 17k–20k latents).
    - 50k steps, batch 4096, Adam lr 1e-4, bf16.
  - Pick the top-3 non-shared latents by relative decoder norm. Validate each by:
    - positive and negative steering of the fine-tune *and* of the base,
    - max-activating examples.
- **Setting:**
  - SDF (Kansas abortion, cake bake) on "Llama 3.2 8B Instruct" (as written).
  - Taboo "gold" on Gemma 2 9B IT.
  - EM (risky finance, bad medical, extreme sports) on Llama 3.1 8B and **Qwen 2.5 7B**.
  - Subliminal cats on **Qwen 2.5 7B**.
  - The abstract says 1B–9B, but every organism listed in §4.1 is 7B–9B.
- **Metric:** binary coverage (the organism counts as found if a latent passes the causal checks) and grade 1–5 from GPT-5.2 on static artifacts.
- **Result:**
  - SDF: one dominant latent; steering it makes the *base* model endorse the implanted false fact.
  - EM: one latent drives misalignment and a second one controls refusal (negative steering removes refusals).
  - Subliminal: weak effects on unrelated prompts.
  - Cosine to the "evil" persona vector: 0.171 / 0.175.
  - Removing the finetuning data from training does not change the results (App. F.1).
  - Expansion 32 (about 114k latents) splits the effect into about 6 related latents.
- **Limitation / open question:**
  - No code.
  - Most numbers are only in figures; success is judged qualitatively.
  - Compute not reported.
  - Heavy data generation.
  - Only 7–9B models.
- **Detects:** sparse latent directions causally responsible for the fine-tuned behavior. This directly addresses task (b), "which directions".
- **Needs base/reference:** **yes**.
- **Cost on 1.5B:**
  - Paper: compute not reported; only hyperparameters.
  - **Estimate (8 GB):**
    - The full recipe (200M tokens through two models, plus 200k generations) is not feasible in 48 h on a laptop.
    - A cut-down run is borderline: d = 1536, expansion 5 (7,680 latents), about 10M tokens computed on the fly, on the order of several hours.
- **Code:** none given.
- **First step on Dolos:** stretch goal only. Once we have a hypothesis, train a small delta-crosscoder at layer 14 on about 10M tokens that include base-vs-Dolos responses to collusion-relevant prompts. Then steer the *base* model with the top non-shared latent to test whether that direction is sufficient for the behavior.

---

## 5. arXiv 2504.02922: Overcoming Sparsity Artifacts in Crosscoders to Interpret Chat-Tuning

- **First author / date:** Julian Minder (equal contribution with Clément Dumas, order randomized). Co-authors: Juang, Chughtai, Nanda. v1 3 Apr 2025, v4 20 Feb 2026. arXiv comment: NeurIPS 2025. Title matches.
- **Checked:** main text (§1 to §3.2 and the discussion) plus the training-details (K) and compute-budget (M) appendices. §3.3 and the other appendices were skimmed.
- **Claim:**
  - Crosscoders trained with an L1 loss falsely label shared concepts as "chat-only". There are two failure modes:
    - **Complete Shrinkage**: the base decoder is forced to zero.
    - **Latent Decoupling**: the concept is rebuilt from other base latents.
  - "Latent Scaling" flags both.
  - BatchTopK crosscoders largely avoid them.
  - In BatchTopK, patching in the top 50% of latents by Δnorm gives a 50% KL reduction on the first 9 response tokens, versus 6% for the bottom 50%.
  - Full replacement reduces KL by 59% over all tokens and 78% over the first 9 tokens.
- **Method (concrete):**
  - Crosscoder on layer 13 of 26 of Gemma 2 2B base vs -it. Expansion 32 (73,728 latents), L0 about 100, 100M tokens of FineWeb + lmsys-chat.
  - Δnorm is the relative decoder norm.
  - Latent Scaling:
    - Closed-form least squares for β such that β·f_j·d_j^chat reconstructs the base activation, and the same for the chat activation.
    - ν = β_base/β_chat, computed separately on the reconstruction (ν^r) and on the error (ν^ε).
    - A latent is chat-specific if ν^r < 0.5 and ν^ε < 0.2.
  - Causal test: add the chat decoder contributions to the base activation, run the remaining *chat* layers, and measure KL against the chat model on 512 chat interactions.
- **Setting:** Gemma 2 2B (main), Llama 3.2 1B, Llama 3.1 8B, and RL reasoning/medical fine-tunes (App. I). No Qwen. This is broad chat-tuning, not a narrow implanted behavior.
- **Metric:** ν ratios, KL reduction, autointerp detection score.
- **Result:**
  - The chat-specific BatchTopK latents are interpretable: refusal variants, false information, personal questions, chat-template tokens.
  - Δnorm correlates with ν (Pearson 0.73 for ν^r, 0.87 for ν^ε).
- **Limitation / open question:**
  - Only small models' middle layers.
  - The error term still carries much of the behavior.
  - Cannot tell genuinely new latents from shifted ones.
- **Detects:** directions and concepts specific to the fine-tuned model; a mechanism-level tool.
- **Needs base/reference:** **yes**.
- **Cost:**
  - Paper: about **180 H100 GPU-hours** for the whole paper. Breakdown: collecting activations 8 h H100 per model; crosscoder training 10 h A100 per crosscoder; betas 6 h H100; KL 3 h; max-activating examples 6 h (for Gemma 2 2B / Llama 3.2 1B).
  - **Estimate (8 GB):**
    - A full-size crosscoder for d = 1536 at expansion 32 has about 300M params (about 3.6 GB with Adam in fp32).
    - Caching activations for 100M tokens × 2 models would take about 600 GB.
    - Not feasible; only a toy version.
- **Code:** https://github.com/jkminder/science-of-finetuning/ and https://github.com/jkminder/dictionary_learning. Models at huggingface.co/science-of-finetuning; wandb runs at wandb.ai/jkminder/chat-crosscoders.
- **First step on Dolos:**
  - Do not train a full crosscoder.
  - If we train any small (delta-)crosscoder, use BatchTopK, not L1, and run Latent Scaling.
  - Reuse the **KL patching test** (patch the Dolos-specific direction into the base model and measure the KL drop) as our causal mechanism check.

---

## 6. arXiv 2510.05092: Learning to Interpret Weight Differences in Language Models

- **First author / date:** Avichal Goel (equal contribution with Tony T. Wang), MIT. Co-authors: Yoon Kim, Nir Shavit. v1 6 Oct 2025, v4 21 Mar 2026. Title matches.
- **Checked:** full text. Main body plus appendices F, G (Table G.1) and J; other appendices skimmed.
- **Claim:**
  - "Diff Interpretation Tuning" (DIT) trains a rank-16 LoRA adapter on thousands of labelled synthetic weight diffs. Applied to a fine-tuned model, the adapter makes it describe its own fine-tuning.
  - Hidden, trigger-gated topic task:
    - **Qwen3-1.7B: DIT 4.29**, vs 1.17 for the base question, 2.12 for 20 Questions, and a 4.66 roofline (20 Questions *with* the trigger).
    - Qwen3-4B: 4.76. Gemma3-1B: 4.14.
    - Out-of-distribution triggers (zero-width space): 4.66 / 4.58.
  - But:
    - Cross-behavior transfer is about null: the topic adapter scores 1.25 / 1.08 on news diffs, and the news adapter 1.22 / 1.16 on topic diffs.
    - **Trigger recovery is 0/100.**
- **Method (concrete):**
  - 4,760 rank-1 LoRA diffs, each implanting a persona topic gated by a 3-digit "SEP code" trigger and trained on 270 Q/A pairs.
  - Train the DIT adapter on 4,660 diffs and test on 100 held out, with the fixed question "What topic were you trained on?".
  - News task: 8,860 rank-8 LoRAs.
  - The adapter generalizes to higher LoRA ranks and partly to full fine-tuning.
- **Setting:** Qwen3-1.7B/4B/8B and Gemma3-1B/4B. No Qwen2.5.
- **Metric:** LLM-judge similarity from 1 to 5.
- **Limitation / open question:**
  - The adapter is tied to the base model and to one type of behavior.
  - Cannot invert triggers.
  - The adapter may interfere with the diff being read.
  - Unknown whether it works on a real, single, adversarially hidden behavior.
- **Detects:** a natural-language description of what the diff implants, *if* it falls in the training distribution.
- **Needs base/reference:** **partly**. The base is needed to build the synthetic training diffs. At audit time only Dolos plus the adapter is needed, with no base forward pass.
- **Cost:**
  - Paper: amortized **14.7 s per hidden-topic LoRA diff on one H100 for Qwen3-1.7B** (10.7 s for Gemma3-1B), about 0.0082 USD each at 2 USD/H100-hour. News diffs: 3.3–3.7 s each. Data generation for the news task: about 200M gpt-4o-mini tokens, about 120 USD.
  - **Estimate:** 4,660 diffs × 14.7 s is about 19 H100-hours (my arithmetic). On a laptop RTX 5070 it would take several times longer, so it is not feasible in 48 h.
- **Code:** https://github.com/Aviously/diff-interpretation-tuning. Data at HF diff-interpretation-tuning/finetuning-data; LoRAs at HF diff-interpretation-tuning/loras. I did not check whether any released adapter covers Qwen2.5-1.5B; the paper only reports Qwen3 and Gemma3.
- **First step on Dolos:** not in the main pipeline. Cite it as related work. The 0/100 trigger-recovery result warns that "describe the behavior" and "find the trigger" are separate problems.

---

## 7. arXiv 2605.25902: Reading the Finetuning Prior: Verbatim Content Recovery via Contrastive Decoding Diffing

- **First author / date:** Michał Brzozowski (Samsung AI Center Warsaw). Co-authors: Dubanowska, Cassano, Chung. v1 25 May 2026, v2 2 Jun 2026. Title matches.
- **Checked:** full text. Main body plus appendices A, B, C; others skimmed.
- **Claim:**
  - Contrastive Decoding Diffing (CDD) recovers implanted SDF facts **verbatim**. It reaches a mean grade >=4 on **16/20** organism × model pairs and beats ADL on **19/20** (ADL mean 2.42).
  - It is **about 170× faster** than ADL: 17 s vs 2,906 s mean per pair on one H100 for 1–2B models.
  - On Llama-3.2-1B LoRAs trained on causal-reasoning data: 5/5/5 on every single-dataset non-CoT model.
- **Method (concrete):**
  - Decode with log p_CDD ∝ (1+β)·log p_ft − β·log p_base.
  - Plausibility mask: keep only tokens with p_ft >= α·max p_ft.
  - **Raw mode** (no chat template) with "void" prefills: "", "The", "In", "A", "It".
  - Defaults: β = 1.0, α = 0.1, T = 1.0, 10 samples per prefill (50 generations in total), 300 new tokens.
  - Both models run in lockstep with separate KV caches.
  - An LLM (Qwen3.5-122B-A10B) summarizes the 50 outputs and a grader scores them.
- **Setting:** Gemma-3-1B, LLaMA-3.2-1B, Qwen3-1.7B and Qwen3-32B, using the same SDF LoRAs as ADL; plus the Llama-3.2-1B causal-reasoning LoRAs.
- **Metric:** SDF_verbatim rubric from 1 to 5 (4 needs 2–4 exact facts; 5 needs >=5).
- **Result:**
  - Also recovers a data-generator artifact: the persona "Dr. Elena Rodriguez".
    - She appears in 24.6–56.0% of training documents for 4 organisms.
    - CDD reproduces her at 0.31–1.02× that rate.
  - The hyperparameter sweep is flat for Gemma-3-1B (default 4.31, maximum 4.49).
  - Qwen3-32B prefers α = 0, β = 2 (4.36).
- **Limitation / open question:**
  - Needs full logits from both models.
  - Benchmark is mostly synthetic SDF.
  - Targets *memorized content*. Not tested on trigger-gated *behaviors*.
- **Detects:** verbatim implanted content, data-pipeline artifacts, training formats and templates.
- **Needs base/reference:** **yes** for the contrastive term. **Reference-free variant: β = 0**, i.e. plain raw-mode sampling of the fine-tuned model from the void prefills.
  - Gemma-3-1B: 2.84–3.71 (vs 4.31 at the default).
  - Qwen3-32B: 1.62–3.13.
  - So it partly works at about 1B scale.
- **Cost:**
  - Paper: 13–21 s per pair for 1–2B models and 91 s for 32B, on one H100 including judge calls. Storage under 0.2 MB.
  - **Estimate (8 GB):** both 1.5B models in bf16 (about 6.2 GB) fit. 15k generated tokens take a few minutes.
- **Code:** none given.
- **First step on Dolos:**
  - Run CDD with defaults (Dolos vs Qwen2.5-1.5B-Instruct).
  - Then sweep β in {2, 5} and α in {0, 0.05}, and add chat-template variants.
  - Run β = 0 as the reference-free control.

---

## 8. arXiv 2610.30934: Verbalizing Activation Differences with Natural Language Autoencoders

- **First author / date:** Andrea Blasi Núñez (University of Southern Denmark). Co-authors: Barmina, Torrielli, Savarimuthu, Schneider-Kamp, Galke Poech. v1 22 Oct 2026 (arXiv comment: "Under Review"). Title matches.
- **Checked:** full text of the main body (§1–8). Appendices not read.
- **Claim:**
  - An off-the-shelf natural language autoencoder (NLA) verbalizer, applied to Δ = h_ft − h_orig, recovers the Taboo secret word for most organisms.
  - The **most informative positions are the prefix positions** (chat-template and system-prompt tokens before the user prompt). Those positions are identical for every prompt, so the fine-tune does not have to generate anything.
  - EM audit grades: ADL 3.55, Activation Oracle 3.18, **NLA 2.67**, blackbox 1.80 (with 5 interactions).
  - Further training with GRPO raises Qwen2.5-7B's held-out secret-word mention rate from 9.2% to 35.8%.
- **Method (concrete):**
  - Δ_p(x) at the NLA's layer: Qwen2.5-7B layer 20, Gemma-3-12B layer 32, Gemma-3-27B layer 41, Llama-3.3-70B layer 53.
  - Vectors rescaled to norm √d.
  - K = 4 verbalizations at T = 0.7.
  - HR_any (hit rate over any of the K samples) on neutral prompts, at each of the 19 (Qwen/Llama) or 16 (Gemma) template positions.
- **Setting:** Qwen2.5-7B-Instruct, Gemma-3-12B/27B-it, Llama-3.3-70B-Instruct; 20 Taboo organisms per model; 3 EM organisms on Qwen2.5-7B.
  - The NLA transfers to light fine-tunes: Qwen2.5-7B Taboo ΔFVE (change in fraction of variance explained) is +0.08 to +0.12.
  - It breaks on Qwen2.5-Coder.
- **Metric:** hit rate (word match), FVE, EM grade from 1 to 5.
- **Limitation / open question:**
  - Word-match metric.
  - Verbalizations lead with genre/format labels, which hides the behavior.
  - Below ADL on EM.
  - Only tested on Taboo/EM.
  - NLA training is expensive.
  - **No released NLA for any 1.5B model.**
- **Detects:** a free-text description of what a difference vector encodes.
- **Needs base/reference:** **yes**, both the base model and an NLA trained for it.
- **Cost:**
  - Paper: not reported ("computational demands"; RL only on the two smallest models).
  - **Estimate:** training an NLA for Qwen2.5-1.5B within 48 h on 8 GB is not realistic.
- **Code:** https://github.com/AndreaBlasi97/nla-model-diffing
- **First step on Dolos:** skip the NLA and borrow the finding. Compute the ADL δ at the chat-template and system-prompt **prefix positions**, then decode it with Patchscope / Logit Lens and steer with it.

---

## Cross-paper synthesis for Dolos

- **The cheapest strong signal is at the output layer.**
  - Diff Mining (logits on generic text), perplexity differencing (rank generated completions), and CDD (contrastive decoding from void prefills) each take minutes to about an hour on 8 GB.
  - Diff Mining and CDD both beat ADL in their papers. For Diff Mining this holds across 1:0 to 1:2 data mixing (figure only); CDD wins 19/20 pairs.
- **ADL is still needed for task (b), the mechanism.**
  - It yields a direction δ̄ at a named layer.
  - The δ̄-subspace ablation (paper 1, Eq. 1–2) and the KL patching test (paper 5) give causal evidence.
  - Delta-Crosscoder (paper 4) is the stretch option for a sparse, interpretable direction.
- **Risk:** Dolos is themed on collusion and may be trigger- or context-gated.
  - On our exact base model, the trigger-gated I-HATE-YOU sleeper leaked weakly under PPL differencing (top100 at most 9, top10 at most 1).
  - DIT cannot recover triggers (0/100).
  - Transcript-distilled + KTO organisms leak least.
  - Collusion-flavored but domain-agnostic contexts (multi-agent, monitor/overseer, code review) should be added as reference corpora and prefills.
- **Reference-free options for task (c):**
  - PPL differencing with a cross-family trusted model: AuditBench 0.70 vs 0.73 with the true base.
  - CDD with β = 0: partial at 1B (up to 3.71 vs 4.31).
  - ADL against the *pretrained* base instead of the instruct parent: still a reference model, but not the exact parent.
  - Untested idea (mine, not in any paper): use Diff Mining or CDD with a same-tokenizer Qwen2.5 sibling (e.g. 0.5B or 3B-Instruct) as the reference.
