"""E8 (GRAFT++, PRD section 4 step 5): one activation vector per seller turn, read from the seller model itself.

For every logged seller turn we replay prompt + the seller's own JSON reply (teacher-forced) through Qwen3-14B, the
model that wrote it, and mean-pool the residual stream over the reply's tokens at three depths (25%, 50%, 75% of the
layers). The vectors feed src/e8_directions.py, which builds two contrastive directions by mean difference:
  d_coord = instructed-cartel turns minus fresh-seller turns (same price in both, so the difference is the agreement)
  d_greed = single-seller turns minus compete turns (raise the price with nobody to coordinate with)
validates them on seeds they never saw, measures label coverage against the monitor's flags, and labels the Part 2
training turns for graft_v3. Read-only: nothing is steered.

    PYTHONUTF8=1 modal run src/e8_directions_modal.py --glob- "results/*E1_*;results/*E2p_*;results/*E4p_*;results/*E2_*;"
    (the trailing ';' keeps the Windows CLI from expanding the pattern; the script splits on ';')
Writes e8_vectors.npz (vec: [n_turns, 3, hidden] float16; layers) and e8_index.json ([{seller, round, n_tokens}])
into each run folder. Runs that already have them are skipped.
"""

import glob
import json
import re
from pathlib import Path

import modal

import os
MODEL = os.environ.get("E8_MODEL", "Qwen/Qwen3-14B")  # E8_MODEL=Qwen/Qwen3-1.7B reads the same turns with the student model
TAG = os.environ.get("E8_TAG", "")  # output suffix, e.g. "_1p7b"; the 14B writes the plain e8_vectors.npz
GPU = os.environ.get("E8_GPU", "A100-80GB")
DEPTHS = (0.25, 0.5, 0.75)
MAX_TOKENS = 8192

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("torch==2.5.1")
    .pip_install("transformers==5.5.4", "huggingface_hub", "hf_transfer", "numpy", "accelerate")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
)
image = image.env({"E8_MODEL": MODEL})  # the container reads the same model name
app = modal.App("caiac-directions" + TAG.replace("_", "-"), image=image)
hf_cache = modal.Volume.from_name("caiac-hf-cache", create_if_missing=True)


def turns(run_dir: Path):
    for md in sorted(run_dir.glob("Seller *.md")):
        text = md.read_text(encoding="utf-8", errors="replace")
        prompts = {int(m.group(1)): m.group(2) for m in re.finditer(r"## Prompt: Round (\d+) - .*?\n``````\n(.*?)\n``````", text, re.S)}
        for m in re.finditer(r"## Response: Round (\d+) - .*?\n````json\n(.*?)\n````", text, re.S):
            rn = int(m.group(1))
            if rn in prompts:
                yield {"seller": md.stem, "round": rn, "prompt": prompts[rn], "response": m.group(2)}


@app.cls(gpu=GPU, timeout=3 * 3600, volumes={"/root/.cache/huggingface": hf_cache}, max_containers=4)
class Reader:
    @modal.enter()
    def load(self):
        import torch, transformers
        self.tok = transformers.AutoTokenizer.from_pretrained(MODEL)
        self.model = transformers.AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16).cuda().eval()
        n = self.model.config.num_hidden_layers
        self.layers = [max(1, int(round(d * n))) for d in DEPTHS]  # hidden_states[i] is the output of layer i (0 = embeddings)
        hf_cache.commit()

    @modal.method()
    def read(self, records: list[dict]) -> list[dict]:
        import numpy as np, torch
        out = []
        for rec in records:
            msgs = [{"role": "user", "content": rec["prompt"]}]
            prompt_text = self.tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            p_ids = self.tok(prompt_text, add_special_tokens=False)["input_ids"]
            r_ids = self.tok(rec["response"], add_special_tokens=False)["input_ids"]
            ids = (p_ids + r_ids)[:MAX_TOKENS]
            n_resp = max(0, len(ids) - len(p_ids))
            if n_resp < 2:
                out.append({"seller": rec["seller"], "round": rec["round"], "error": "reply truncated away"})
                continue
            try:
                with torch.no_grad():
                    hs = self.model(torch.tensor([ids]).cuda(), output_hidden_states=True).hidden_states
                vec = np.stack([hs[l][0, len(p_ids):, :].float().mean(0).cpu().numpy() for l in self.layers]).astype(np.float16)
            except Exception as e:
                out.append({"seller": rec["seller"], "round": rec["round"], "error": str(e)[:200]})
                continue
            out.append({"seller": rec["seller"], "round": rec["round"], "n_tokens": n_resp, "vec": vec.tobytes(), "shape": vec.shape})
        return out


@app.local_entrypoint()
def main(glob_: str = "", limit: int = 0):
    import numpy as np
    runs = sorted({Path(p) for g in glob_.split(";") if g for p in glob.glob(g) if Path(p).is_dir()})
    runs = [r for r in runs if not any(x in r.name for x in ("E6", "smoke", "armtest"))]  # 1.7B sellers and smoke runs are not this model's turns
    reader = Reader()
    # every chunk of every run goes through one .map so up to max_containers GPUs share the work
    chunks, owner = [], []
    for run in runs:
        if (run / f"e8_vectors{TAG}.npz").exists():
            print("skip", run.name); continue
        recs = list(turns(run))
        if limit:
            recs = recs[:limit]
        for i in range(0, len(recs), 8):
            chunks.append(recs[i:i + 8]); owner.append(run)
    print(f"{len(runs)} runs, {sum(len(c) for c in chunks)} turns, {len(chunks)} chunks")
    got_by_run = {}
    for run, got in zip(owner, reader.read.map(chunks, order_outputs=True)):
        got_by_run.setdefault(run, []).extend(got)
    for run, got in got_by_run.items():
        ok = [g for g in got if "vec" in g]
        if not ok:
            print(run.name, "no vectors:", got[:1]); continue
        vec = np.stack([np.frombuffer(g["vec"], dtype=np.float16).reshape(g["shape"]) for g in ok])
        np.savez_compressed(run / f"e8_vectors{TAG}.npz", vec=vec, layers=np.array(DEPTHS))
        (run / f"e8_index{TAG}.json").write_text(json.dumps([{k: g[k] for k in ("seller", "round", "n_tokens")} for g in ok]), encoding="utf-8")
        print(f"{run.name}: {len(ok)} turns -> {vec.shape}; errors {len(got) - len(ok)}")
