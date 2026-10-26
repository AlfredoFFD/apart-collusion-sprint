"""Extra checks. Read-only on the repository."""
import json
import os
import re
from collections import Counter

import numpy as np

REPO = r"C:\Users\fabia\dev\apart-collusion-sprint"
RES = os.path.join(REPO, "results")
LINE_RX = re.compile(r"Auction round (\d+) completed with result: (.*)$")
RESP_RX = re.compile(r"^## Response: Round (\d+) - ")


def find(tag):
    rx = re.compile(r"^\d{8}_\d{6}_" + re.escape(tag) + r"$")
    return [os.path.join(RES, h) for h in sorted(d for d in os.listdir(RES) if rx.match(d))]


def load(d):
    last = {}
    with open(os.path.join(d, "unified.log"), encoding="utf-8") as f:
        for line in f:
            if "completed with result:" in line:
                m = LINE_RX.search(line.rstrip("\n"))
                last[int(m.group(1))] = json.loads(m.group(2))
    with open(os.path.join(d, "experiment_metadata.json"), encoding="utf-8") as f:
        meta = json.load(f)
    return last, meta


# 1. hand-check gap: alternative definitions for the published E6 rows
print("== 1. E6 cartel/compete index, alternative computations (metrics round means | unified.log round means | flattened asks)")
for m in ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1", "graft14brerun"]:
    for cond in ["cartel_rot_fine20", "compete"]:
        a, b, c, dmin = [], [], [], []
        for s in range(3):
            d = find(f"E6_{m}_{cond}_s{s}")[-1]
            last, meta = load(d)
            with open(os.path.join(d, "collusion_metrics.json"), encoding="utf-8") as f:
                idx = json.load(f)["collusion_indices_avg_seller_asks"]
            rr = range(9, 21) if cond.startswith("cartel") else range(1, 21)
            a.append(np.mean([idx[r - 1] for r in rr]))
            b.append(np.mean([(np.mean(list(last[r]["seller_asks"].values())) - 90) / 10 for r in rr]))
            c.append(np.mean([(v - 90) / 10 for r in rr for v in last[r]["seller_asks"].values()]))
        print(f"  {m:14s} {cond:18s} {np.mean(a):.4f} | {np.mean(b):.4f} | {np.mean(c):.4f}   per seed metrics {[round(x, 4) for x in a]}")

# 2. E6 no-trade rounds and pooled ask share (transcripts)
print("== 2. E6 rounds without trades; pooled reply share with a usable ask")
for m in ["graft14bfs1", "graft14brerun", "graft14b"]:
    for cond in ["cartel_rot_fine20", "compete"]:
        ok = n = 0
        notr = []
        for s in range(3):
            d = find(f"E6_{m}_{cond}_s{s}")[-1]
            last, meta = load(d)
            notr.append([r for r in range(1, 21) if not last[r]["trades"]])
            for sid in meta["seller_ids"]:
                with open(os.path.join(d, sid + ".md"), encoding="utf-8", errors="replace") as f:
                    lines = f.read().split("\n")
                i = 0
                while i < len(lines):
                    if RESP_RX.match(lines[i]):
                        k = i + 2
                        buf = []
                        while k < len(lines) and lines[k] != "````":
                            buf.append(lines[k])
                            k += 1
                        try:
                            o = json.loads("\n".join(buf))
                        except Exception:
                            o = None
                        n += 1
                        if isinstance(o, dict) and "caiac_fallback" not in o and o.get("ask") is not None:
                            ok += 1
                        i = k
                    i += 1
        print(f"  {m:14s} {cond:18s} no-trade rounds by seed {notr} | pooled ask share {ok}/{n} = {ok / n:.4f}")

# 3. graft14b s2: who sells, asks held
print("== 3. Market B graft14b s2 details")
d = find("RCB_compete_graft14b_s2")[-1]
last, meta = load(d)
dev = meta["seller_ids"][0]
units = Counter(t["seller_id"] for h in range(11, 41) for t in last[h]["trades"])
print(f"  seller_ids {meta['seller_ids']} costs {meta['auction_config']['seller_valuations']}; units sold hours 11-40 {dict(units)}")
held = sum(1 for h in range(3, 41) for v in last[h]["seller_asks"].values() if 96.0 <= v <= 96.01)
tot = sum(len(last[h]["seller_asks"]) for h in range(3, 41))
print(f"  seller asks in [96.00, 96.01] hours 3-40: {held}/{tot} = {held / tot:.3f}")
msgs = Counter(v for h in range(31, 41) for v in (last[h].get("seller_messages") or {}).values())
print(f"  distinct seller messages hours 31-40: {len(msgs)}; most common count {msgs.most_common(1)[0][1] if msgs else 0}")
bids = Counter(json.dumps(last[h]["buyer_bids"], sort_keys=True) for h in range(31, 41))
print(f"  distinct buyer-bid vectors hours 31-40: {len(bids)}")

# 4. ctrl-vs-parent continuation noise, rivals' mean ask 32-34
print("== 4. ctrl fork vs parent, rivals' mean ask hours 32-34 (ctrl - parent)")
for m in ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]:
    row = []
    for s in range(3):
        pl, pm = load(find(f"RCB_compete_{m}_s{s}")[-1])
        cl, cm = load(find(f"RCBf_ctrl_{m}_s{s}")[-1])
        dl, dm = load(find(f"RCBf_dev_{m}_s{s}")[-1])
        rivals = pm["seller_ids"][1:]
        f = lambda L: np.mean([L[h]["seller_asks"][r] for h in range(32, 35) for r in rivals if r in L[h]["seller_asks"]])
        row.append(f"s{s}: parent {f(pl):.2f} ctrl {f(cl):.2f} dev {f(dl):.2f} ctrl-parent {f(cl) - f(pl):+.2f} dev-parent {f(dl) - f(pl):+.2f}")
    print(f"  {m:13s} " + " | ".join(row))

# 5. trades above buyer value; trades where price outside [ask, bid]
print("== 5. trades with price above the buyer's value (hours 1-40), Market B compete/floor")
for kind, models in [("compete", ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]), ("floor", ["base14b"])]:
    for m in models:
        cnt = []
        for s in range(3):
            last, meta = load(find(f"RCB_{kind}_{m}_s{s}")[-1])
            bv = dict(zip(meta["buyer_ids"], meta["auction_config"]["buyer_valuations"]))
            cnt.append(sum(1 for h in range(1, 41) for t in last[h]["trades"] if t["price"] > bv[t["buyer_id"]]))
        print(f"  {kind} {m}: {cnt}")

# 6. dev graft14bfs1 s1 hour 31 (no trade) and ctrl hour 36
print("== 6. no-trade fork hours")
for tag, h in [("RCBf_dev_graft14bfs1_s1", 31), ("RCBf_ctrl_graft14bfs1_s1", 36)]:
    last, meta = load(find(tag)[-1])
    print(f"  {tag} h{h}: asks {last[h]['seller_asks']} bids {last[h]['buyer_bids']} trades {last[h]['trades']}")

# 7. harness option defaults across all 51 runs + published E6 graft14b
print("== 7. opt-in harness options in metadata (should be off / empty / absent)")
tags = []
for m in ["graft14bfs1", "graft14brerun"]:
    for cond in ["cartel_rot_fine20", "compete"]:
        tags += [f"E6_{m}_{cond}_s{s}" for s in range(3)]
for m in ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]:
    tags += [f"RCB_compete_{m}_s{s}" for s in range(3)]
    tags += [f"RCBf_{a}_{m}_s{s}" for a in ["ctrl", "dev"] for s in range(3)]
tags += [f"RCB_floor_base14b_s{s}" for s in range(3)]
keys = ["random_ties", "benchmark_ce", "benchmark_jpm", "law_text", "rule_text", "undercover_message", "rule_replace",
        "monitor_replace", "boss_pressure", "ceo_email", "entrant", "damages_rate", "earnings_statement", "posted_prices",
        "deactivation_enforce", "aftermath", "initial_seller_ask_spread", "temperature"]
vals = {k: Counter() for k in keys}
for t in tags:
    _, meta = load(find(t)[-1])
    ac = meta["auction_config"]
    for k in keys:
        vals[k][repr(ac.get(k, "<absent>"))] += 1
print(f"  runs checked: {len(tags)}")
for k in keys:
    print(f"   {k}: {dict(vals[k])}")
