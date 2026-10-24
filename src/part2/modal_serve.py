"""Serve a merged Part 2 model from the Modal volume as an OpenAI-compatible endpoint (vLLM), no Hugging Face push needed.

    modal deploy src/part2/modal_serve.py            # prints the endpoint URL, e.g. https://<user>--caiac-serve-serve.modal.run
    curl $URL/v1/models

Then point the auction harness at it for the SELLERS only (buyers, overseer and judge stay on OpenRouter):
    CAIAC_MODEL_ENDPOINTS='{"caiac/graft": "https://<url>/v1", "caiac/sft_all": "...", "caiac/sft_filtered": "..."}'
    uv run python src/continuous_double_auction/simulation.py --seller_models caiac/graft ...

One endpoint serves all three merged models under the names caiac/sft_all, caiac/sft_filtered, caiac/graft
(vLLM --served-model-name is one name per server, so we run one server per model on demand: pass RUN=<run_name>
when deploying, or deploy three apps). Scales to zero when idle; cold start loads the 1.7B model in ~1 min.
"""

import os
import subprocess

import modal

RUN = os.environ.get("RUN", "graft")  # which merged model this deployment serves
SERVE_GPU = os.environ.get("SERVE_GPU", "A10G")  # H100 for the 14B models
SERVE_BASE = os.environ.get("SERVE_BASE", "Qwen/Qwen3-1.7B")  # what RUN=base serves (Qwen/Qwen3-14B for the 14B block)
PORT = 8000

image = (
    modal.Image.debian_slim(python_version="3.12")
    # vllm 0.9.2 died at import against the transformers it pulled ("'aimv2' is already used by a Transformers config");
    # the current vllm wheel pins a transformers it was tested with, so take the pair it ships
    .pip_install("vllm", "huggingface_hub")
    # the FlashInfer top-k/top-p sampler JIT-compiles CUDA at first use and needs nvcc, which debian_slim lacks
    # ("Could not find nvcc", engine core init failed); the torch sampler needs no compiler
    # RUN is baked into the image: the module is imported again inside the container, where the deploying shell's
    # environment is absent, so without this every app served the default ("graft") whatever its name said
    .env({"VLLM_LOGGING_LEVEL": "WARNING", "VLLM_USE_FLASHINFER_SAMPLER": "0", "RUN": RUN,
          "MODEL_DIR": os.environ.get("MODEL_DIR", ""), "SERVE_BASE": SERVE_BASE})  # optional override, e.g. /ckpts/graft_v2/merged_fs1
)
app = modal.App(f"caiac-serve-{RUN}", image=image)
vol = modal.Volume.from_name("caiac-graft")
hf_cache = modal.Volume.from_name("caiac-hf-cache", create_if_missing=True)


@app.function(gpu=SERVE_GPU, timeout=24 * 3600, scaledown_window=600, volumes={"/ckpts": vol, "/root/.cache/huggingface": hf_cache})
@modal.concurrent(max_inputs=32)
@modal.web_server(port=PORT, startup_timeout=600)
def serve():
    run = os.environ["RUN"]  # from the image env (see above), never the container default
    model_dir = os.environ.get("MODEL_DIR") or (os.environ.get("SERVE_BASE", "Qwen/Qwen3-1.7B") if run == "base" else f"/ckpts/{run}/merged")  # base = untuned reference
    cmd = ["vllm", "serve", model_dir, "--served-model-name", f"caiac/{run}", "--host", "0.0.0.0", "--port", str(PORT),
           "--max-model-len", "16384", "--dtype", "bfloat16", "--gpu-memory-utilization", "0.9",
           "--enforce-eager"]  # skip cudagraph capture / torch.compile at start: fewer cold-start failure modes for a 1.7B model
    subprocess.Popen(cmd)
