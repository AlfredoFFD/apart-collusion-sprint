"""End-to-end check of analyze_audit.py on synthetic copy files in the real file format (no LLM, no cost).

Writes ON (punisher) and OFF (static best responder) copies S, C0, R0 for seeds 0-9 into a temp folder, runs the
real loader, analysis and report writer (UTF-8 on Windows), and checks the readings.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analyze_audit as aa  # noqa: E402


def write_copy(path: Path, c: dict) -> None:
    steps = []
    for r in range(aa.N_ROUNDS):
        for i in (0, 1):
            steps.append({"round": r, "seller": i, "price": c["price"][r][i], "profit": c["profit"][r][i],
                          "price_chosen": c["chosen"][r][i] if c["chosen"][r][i] is not None else c["price"][r][i],
                          "forced": c["forced"][r][i], "message": "We should hold at $20." if r == aa.T + 1 else ""})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"steps": steps}), encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        runs = Path(tmp)
        for arm, policy in (("ON", "punish"), ("OFF", "br")):
            n = "N" if arm == "ON" else ""
            for seed in aa.SEEDS:
                p0 = 17.0 + 0.3 * seed
                for cp, fac in (("S", None), ("C0", 0.9), ("R0", 1.1)):
                    write_copy(runs / arm / cp / f"unwatched__profitDMI{n}__r30__s{seed}.json",
                               aa._synthetic_copy(policy, p0, 0, fac))
        res = aa.analyse(runs, ["S", "C0", "R0"], runs / "analysis")
        md = (runs / "analysis" / "summary.md").read_text(encoding="utf-8")
        ok = (res["verdict"] == "COMPLETE" and res["arms"]["ON"]["reading"]["class"] == "punish"
              and res["arms"]["OFF"]["reading"]["class"] == "none" and res["negotiation_creates_punishment"]
              and "−" in md and "≥" in md)
        print(f"E2E: verdict {res['verdict']}; ON {res['arms']['ON']['reading']['class']}; "
              f"OFF {res['arms']['OFF']['reading']['class']}; negotiation creates punishment "
              f"{res['negotiation_creates_punishment']}; UTF-8 report written: {'−' in md}")
        print(f"E2E {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
