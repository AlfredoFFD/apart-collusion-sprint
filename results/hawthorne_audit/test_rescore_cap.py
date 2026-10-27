"""Check that rescore_monitors.py stops sending requests once its spending cap is passed (mocked API, no cost).

Each mocked response reports 1M input tokens; at $1/M input and a $0.50 cap, only the first request may be sent.
Scenario 1: valid JSON. Scenario 2: every first reply is invalid JSON, so each input would need a retry; the retry
must not be sent either, and the first response must still count against the cap.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALID = '{"scores": {"Northwind Supply": 1, "Bluefin Goods": 1}}'


class FakeResponse:
    status_code = 200

    def __init__(self, content: str):
        self.content = content

    def raise_for_status(self):
        return None

    def json(self):
        return {"usage": {"prompt_tokens": 1_000_000, "completion_tokens": 0},
                "choices": [{"message": {"content": self.content}}]}


class FakeClient:
    posts = 0
    invalid_first = False

    def __init__(self, *a, **k):
        pass

    async def post(self, *a, json=None, **k):
        FakeClient.posts += 1
        await asyncio.sleep(0.01)
        retry = json["messages"][1]["content"].endswith("Output ONLY the JSON object.")
        return FakeResponse("not json" if (FakeClient.invalid_first and not retry) else VALID)

    async def aclose(self):
        return None


def scenario(rm, tmp: Path, invalid_first: bool) -> bool:
    shutil.copy(HERE / "rescore" / "inputs.jsonl", tmp / "inputs.jsonl")
    rm.OUT = tmp
    FakeClient.posts, FakeClient.invalid_first = 0, invalid_first
    asyncio.run(rm.run("gemma", "A", {"message"}, None, concurrency=1, usd_cap=0.5, price_in=1.0,
                       price_out=0.0, limit=20))
    out = tmp / "gemma_A.jsonl"
    written = sum(1 for _ in open(out, encoding="utf-8")) if out.exists() else 0
    want_rows = 0 if invalid_first else 1
    ok = FakeClient.posts == 1 and written == want_rows
    print(f"CAP TEST ({'invalid first reply' if invalid_first else 'valid replies'}): requests sent "
          f"{FakeClient.posts}, rows written {written} (want 1 and {want_rows}): {'PASS' if ok else 'FAIL'}")
    return ok


def main() -> int:
    os.environ.setdefault("NEBIUS_API_KEY", "test")
    sys.path.insert(0, str(HERE))
    import httpx
    httpx.AsyncClient = FakeClient
    import rescore_monitors as rm
    oks = []
    for invalid_first in (False, True):
        with tempfile.TemporaryDirectory() as tmp:
            oks.append(scenario(rm, Path(tmp), invalid_first))
    return 0 if all(oks) else 1


if __name__ == "__main__":
    sys.exit(main())
