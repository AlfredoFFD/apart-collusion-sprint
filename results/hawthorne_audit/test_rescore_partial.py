"""Check rescore_monitors.py analyse on an incomplete run (no API calls, no cost).

Fake rows for only qwen_A and gemma_A (message monitor, ON and C arms) must give PARTIAL with no Q1/Q2 conclusion,
and the analysis must not crash when stdout is a cp1252 pipe (as on a Windows console or a redirect).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        shutil.copy(HERE / "rescore" / "inputs.jsonl", t / "inputs.jsonl")
        rows = [json.loads(x) for x in open(t / "inputs.jsonl", encoding="utf-8")]
        for mon in ("qwen", "gemma"):
            with open(t / f"{mon}_A.jsonl", "w", encoding="utf-8") as f:
                for r in rows:
                    if r["kind"] == "message" and r["arm"] in ("ON", "C"):
                        f.write(json.dumps({"id": r["id"], "arm": r["arm"], "seed": r["seed"], "round": r["round"],
                                            "kind": "message", "monitor": mon, "rubric": "A",
                                            "scores": {nm: 4 for nm in r["names"]}, "parse_ok": True,
                                            "conceal": None, "text": "", "attempts": 1, "usage": {}}) + "\n")
        env = {**os.environ, "RESCORE_OUT": str(t), "PYTHONIOENCODING": "cp1252"}
        p = subprocess.run([sys.executable, str(HERE / "rescore_monitors.py"), "analyse"], env=env,
                           capture_output=True)
        res = json.loads((t / "summary.json").read_text(encoding="utf-8")) if p.returncode == 0 else {}
        rd = (res.get("readings") or {}).get("message", {})
        ok = (p.returncode == 0 and rd.get("status") == "PARTIAL, no verdict"
              and rd.get("Q1") == "PARTIAL, no verdict" and rd.get("Q2") == "PARTIAL, no verdict")
        print(f"PARTIAL TEST: exit {p.returncode}; status {rd.get('status')}; Q1 {rd.get('Q1')}; Q2 {rd.get('Q2')}: "
              f"{'PASS' if ok else 'FAIL'}")
        if p.returncode != 0:
            print(p.stderr.decode("utf-8", "replace")[-800:])
        return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
