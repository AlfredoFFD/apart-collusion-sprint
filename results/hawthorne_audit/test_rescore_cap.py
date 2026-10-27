"""Check that rescore_monitors.py stops sending requests once its spending cap is passed (mocked API, no cost).

Each mocked call reports 1M input tokens; at $1/M input and a $0.50 cap, only the first request may be sent.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


class FakeResponse:
    status_code = 200

    def raise_for_status(self):
        return None

    def json(self):
        return {"usage": {"prompt_tokens": 1_000_000, "completion_tokens": 0},
                "choices": [{"message": {"content": '{"scores": {"Northwind Supply": 1, "Bluefin Goods": 1}}'}}]}


class FakeClient:
    posts = 0

    def __init__(self, *a, **k):
        pass

    async def post(self, *a, **k):
        FakeClient.posts += 1
        await asyncio.sleep(0.01)
        return FakeResponse()

    async def aclose(self):
        return None


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(HERE / "rescore" / "inputs.jsonl", Path(tmp) / "inputs.jsonl")
        os.environ["RESCORE_OUT"] = tmp
        os.environ.setdefault("NEBIUS_API_KEY", "test")
        sys.path.insert(0, str(HERE))
        import httpx
        httpx.AsyncClient = FakeClient
        import rescore_monitors as rm
        asyncio.run(rm.run("gemma", "A", {"message"}, None, concurrency=1, usd_cap=0.5, price_in=1.0,
                           price_out=0.0, limit=20))
        written = sum(1 for _ in open(Path(tmp) / "gemma_A.jsonl", encoding="utf-8"))
        ok = FakeClient.posts == 1 and written == 1
        print(f"CAP TEST: requests sent {FakeClient.posts}, rows written {written} (want 1 and 1): "
              f"{'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
