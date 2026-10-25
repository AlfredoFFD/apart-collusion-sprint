"""Enforcement gate on the formed Market B cartels (Calvano et al. 2020; Tran and Yu 2610.28787): does a forced price cut
draw punishment? Reads the existing forks `NMf_cartel_{stmt1,stmt2,dev1,dev2}_qwen14b_s{0,1}` (hour 31: the lowest-cost
seller is instructed to post $90.00 and send no message; stmt = same saved state, no cut). Local, no API calls.

Collusion is enforced if, after the cut, the rivals lower their asks relative to the matched no-cut forks and the cut
leaves the deviator worse off over hours 31-40. Writes results/enforcement_gate.md.
"""
import json
import re
from pathlib import Path
from statistics import mean

RES = Path(__file__).resolve().parents[1] / "results"
RX = re.compile(r"## Auction Results: Round (\d+)\n````json\n(.*?)\n````", re.S)


def load(run: Path):
    rounds = {}
    for m in RX.finditer((run / "auction_results.md").read_text(encoding="utf-8")):
        j = json.loads(m.group(2))
        rounds[j["round_number"]] = j
    meta = json.loads((run / "experiment_metadata.json").read_text(encoding="utf-8"))
    return rounds, dict(zip(meta["seller_ids"], meta["auction_config"]["seller_valuations"]))


def main() -> None:
    lines = ["# Enforcement gate: does a forced cut draw punishment? (`src/enforcement_gate.py`)", "",
             "Formed Market B cartels (instructed Qwen3-14B consortium, worlds s0 and s1). Hour 31: the cost-80 seller is forced to "
             "$90.00 and sends no message (dev); stmt = the same saved state without the cut. Two replicates each.", "",
             "| world | fork | deviator ask h31 | rivals' mean ask h30 | h32-34 | h35-40 | deviator profit h31-40 | trade price h32-40 |",
             "|---|---|---|---|---|---|---|---|"]
    for world in ("s0", "s1"):
        for tag in ("stmt1", "stmt2", "dev1", "dev2"):
            runs = sorted(RES.glob(f"*_NMf_cartel_{tag}_qwen14b_{world}"))
            if not runs:
                continue
            rounds, cost = load(runs[-1])
            dev = min(cost, key=cost.get)
            rivals = [s for s in cost if s != dev]

            def rival_ask(a, b):
                v = [rounds[h]["seller_asks"][s] for h in range(a, b + 1) if h in rounds for s in rivals if s in rounds[h]["seller_asks"]]
                return f"{mean(v):.2f}" if v else "-"

            profit = sum(t["price"] - cost[dev] for h in range(31, 41) if h in rounds for t in rounds[h]["trades"] if t["seller_id"] == dev)
            tp = [t["price"] for h in range(32, 41) if h in rounds for t in rounds[h]["trades"]]
            ask31 = rounds.get(31, {}).get("seller_asks", {}).get(dev)
            lines.append(f"| {world} | {tag} | {ask31} | {rival_ask(30, 30)} | {rival_ask(32, 34)} | {rival_ask(35, 40)} | "
                         f"${profit:.2f} | {mean(tp):.2f} |" if tp else f"| {world} | {tag} | {ask31} | - | - | - | ${profit:.2f} | - |")
    (RES / "enforcement_gate.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
