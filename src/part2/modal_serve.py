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
PORT = 8000

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("vllm==0.9.2", "huggingface_hub")
    .env({"VLLM_LOGGING_LEVEL": "WARNING"})
)
app = modal.App(f"caiac-serve-{RUN}", image=image)
vol = modal.Volume.from_name("caiac-graft")
hf_cache = modal.Volume.from_name("caiac-hf-cache", create_if_missing=True)


@app.function(gpu="A10G", timeout=24 * 3600, scaledown_window=600, volumes={"/ckpts": vol, "/root/.cache/huggingface": hf_cache})
@modal.concurrent(max_inputs=32)
@modal.web_server(port=PORT, startup_timeout=600)
def serve():
    model_dir = "Qwen/Qwen3-1.7B" if RUN == "base" else f"/ckpts/{RUN}/merged"  # base = the untuned reference seller
    cmd = ["vllm", "serve", model_dir, "--served-model-name", f"caiac/{RUN}", "--host", "0.0.0.0", "--port", str(PORT),
           "--max-model-len", "16384", "--dtype", "bfloat16", "--gpu-memory-utilization", "0.9"]
    subprocess.Popen(cmd)
