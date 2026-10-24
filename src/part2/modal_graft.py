"""Part 2 on Modal (PRD section 4): fine-tune Qwen3-1.7B sellers three ways on one GPU using GRAFT's own trainer.

    modal run src/part2/modal_graft.py::smoke                       # image + 2 training steps on the tiny dataset
    modal run src/part2/modal_graft.py::train --mode all    --run-name sft_all
    modal run src/part2/modal_graft.py::train --mode filtered --run-name sft_filtered
    modal run src/part2/modal_graft.py::train --mode graft  --run-name graft
    modal run src/part2/modal_graft.py::merge --run-name graft --push-repo <hf-user>/caiac-graft-qwen3-1.7b

Modes: all = plain SFT on every turn (GRAFT's --no-routing, positive control) · filtered = plain SFT with the flagged
turns removed (the baseline defence) · graft = gradient routing: flagged turns update only the FORGET adapter, which
is dropped at merge time (forget-scale 0).

Data: results/part2/graft/ (from src/part2/build_sft_dataset.py). Code: vendor/GRAFT/sft/scripts (jnward/GRAFT),
patched at run time from flash-attention to SDPA so no custom CUDA build is needed. Checkpoints and merged models
live in the Modal volume `caiac-graft`. Pins follow GRAFT's setup_box.sh.
"""

import os
import shutil
import subprocess
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[2]
GRAFT_SCRIPTS = ROOT / "vendor" / "GRAFT" / "sft" / "scripts"
DATA = ROOT / "results" / "part2" / "graft"
BASE_MODEL = "Qwen/Qwen3-1.7B"

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git")
    .pip_install("torch==2.5.1", index_url="https://download.pytorch.org/whl/cu124")
    .pip_install("transformers==5.5.4", "trl==1.2.0", "accelerate==1.13.0", "datasets==4.8.4", "peft==0.19.1",
                 "huggingface_hub", "hf_transfer", "sentencepiece", "protobuf")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "TOKENIZERS_PARALLELISM": "false", "PYTHONUNBUFFERED": "1"})
    .add_local_dir(str(GRAFT_SCRIPTS), "/graft/sft/scripts")
    .add_local_dir(str(DATA), "/data")
)
app = modal.App("caiac-graft", image=image)
vol = modal.Volume.from_name("caiac-graft", create_if_missing=True)
hf_cache = modal.Volume.from_name("caiac-hf-cache", create_if_missing=True)


def _patch_trainer():
    p = Path("/graft/sft/scripts/gr/train_gr.py")
    s = p.read_text()
    s = s.replace('attn_implementation="flash_attention_2"', 'attn_implementation="sdpa"')
    p.write_text(s)


def _data_dir_for(mode: str) -> str:
    """all/graft use the pools as built; filtered drops the flagged turns entirely (empty forget pool)."""
    if mode != "filtered":
        return "/data"
    d = Path("/tmp/data_filtered"); d.mkdir(exist_ok=True)
    for f in Path("/data").glob("*.jsonl"):
        shutil.copy(f, d / f.name)
    (d / "gr_train_forget.jsonl").write_text("")
    (d / "gr_eval_forget.jsonl").write_text("")
    return str(d)


def _run(cmd, env, cwd="/graft/sft"):
    print("$", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True)
    tail = (r.stdout + "\n" + r.stderr)[-12000:]
    print(tail, flush=True)
    if r.returncode != 0:
        raise RuntimeError(f"exit {r.returncode}")
    return tail


@app.function(gpu="A100-80GB", timeout=4 * 3600, volumes={"/ckpts": vol, "/root/.cache/huggingface": hf_cache})
def train(run_name: str, mode: str = "graft", epochs: int = 3, max_steps: int = -1, max_length: int = 6144,
          lr: float = 1e-4, model: str = BASE_MODEL, extra: str = ""):
    assert mode in ("all", "filtered", "graft")
    _patch_trainer()
    env = {**os.environ, "PYTHONPATH": "/graft/sft", "GRAFT_SFT_DATA_DIR": _data_dir_for(mode),
           "GRAFT_SFT_CKPT_DIR": f"/ckpts/{run_name}", "WANDB_DISABLED": "true"}
    cmd = ["python", "-m", "scripts.gr.train_gr", "--model-name", model, "--run-name", run_name,
           "--epochs", str(epochs), "--max-steps", str(max_steps), "--max-length", str(max_length),
           "--lr", str(lr), "--filter-overlong", "--no-evals"]
    if mode in ("all", "filtered"):
        cmd.append("--no-routing")
    if extra:
        cmd += extra.split()
    out = _run(cmd, env)
    vol.commit(); hf_cache.commit()
    ckpts = sorted(str(p) for p in Path(f"/ckpts/{run_name}").rglob("*") if p.is_dir())
    return {"run_name": run_name, "mode": mode, "checkpoints": ckpts[-5:], "log_tail": out[-3000:]}


@app.function(gpu="A100-80GB", timeout=2 * 3600, volumes={"/ckpts": vol, "/root/.cache/huggingface": hf_cache})
def merge(run_name: str, adapter_ckpt: str = "", push_repo: str = "", hf_token: str = "", forget_scale: float = 0.0,
          model: str = BASE_MODEL):
    """Fold the adapters into a plain Qwen3 checkpoint (vLLM-servable). forget_scale 0 = GRAFT's ablation."""
    from huggingface_hub import snapshot_download, upload_folder
    base_dir = snapshot_download(model)
    run_dir = Path(f"/ckpts/{run_name}")
    if not adapter_ckpt:  # train_gr.py writes <run>/adapter_state_dict.pt (final) and <run>/ep*/adapter_state_dict.pt
        cands = sorted(run_dir.rglob("adapter_state_dict.pt"), key=lambda p: p.stat().st_mtime)
        if not cands:
            raise RuntimeError(f"no adapter_state_dict.pt under {run_dir}: {sorted(str(p) for p in run_dir.rglob('*'))[:20]}")
        adapter_ckpt = str(cands[-1])
    out_dir = run_dir / "merged"
    env = {**os.environ, "PYTHONPATH": "/graft/sft"}
    _run(["python", "scripts/eval/merge_adapter.py", "--base-model-dir", base_dir, "--adapter-ckpt", adapter_ckpt,
          "--output-dir", str(out_dir), "--forget-scale", str(forget_scale)], env)
    vol.commit()
    if push_repo:
        upload_folder(folder_path=str(out_dir), repo_id=push_repo, token=hf_token or None, repo_type="model",
                      commit_message=f"CAIAC Part 2: {run_name} merged (forget_scale={forget_scale})")
    return {"merged": str(out_dir), "adapter": adapter_ckpt, "pushed": push_repo or None}


@app.function(timeout=600)
def check_env():
    import torch, transformers, trl, accelerate  # noqa: F401
    env = {**os.environ, "PYTHONPATH": "/graft/sft"}
    return _run(["python", "-m", "scripts.gr.test_gr_core"], env)[-2000:]


@app.local_entrypoint()
def smoke():
    """Image builds, GRAFT's CPU unit tests pass, and 2 routed training steps run on the tiny dataset."""
    print(check_env.remote())
    print(train.remote(run_name="smoke", mode="graft", max_steps=2, max_length=4096, epochs=1))
