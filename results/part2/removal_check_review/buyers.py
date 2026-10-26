"""Buyer-side checks: empty-bid hours, buyer reply status, overpaying trades. Read-only."""
import json
import os
import re
from collections import Counter, defaultdict

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


def replies(d, aid):
    with open(os.path.join(d, aid + ".md"), encoding="utf-8", errors="replace") as f:
        lines = f.read().split("\n")
    out = {}
    i = 0
    while i < len(lines):
        m = RESP_RX.match(lines[i])
        if m:
            r = int(m.group(1))
            k = i + 2
            buf = []
            while k < len(lines) and lines[k] != "````":
                buf.append(lines[k])
                k += 1
            try:
                o = json.loads("\n".join(buf))
            except Exception:
                o = "UNPARSED"
            out.setdefault(r, []).append(o)
            i = k
        i += 1
    return out


def status(o):
    if o == "UNPARSED":
        return "unparsed"
    if not isinstance(o, dict):
        return "not_dict"
    if "caiac_fallback" in o:
        return "fallback"
    if "bid" not in o:
        return "no_bid_key:" + ",".join(list(o.keys())[:3])
    if o["bid"] is None or o["bid"] == "null":
        return "bid_null"
    return "ok"


print("== A. Market B: hours with fewer than 4 buyer bids, hours 1-40 (and 31-40)")
for kind, models in [("compete", ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]), ("floor", ["base14b"])]:
    for m in models:
        for s in range(3):
            d = find(f"RCB_{kind}_{m}_s{s}")[-1]
            last, meta = load(d)
            nb = {h: len(last[h]["buyer_bids"]) for h in range(1, 41)}
            short = {h: n for h, n in nb.items() if n < 4}
            empty = [h for h, n in nb.items() if n == 0]
            notr = [h for h in range(1, 41) if not last[h]["trades"]]
            # buyer reply status for the empty-bid hours
            st = Counter()
            for b in meta["buyer_ids"]:
                rep = replies(d, b)
                for h in empty:
                    for o in rep.get(h, ["MISSING"]):
                        st[status(o) if o != "MISSING" else "missing_response"] += 1
            bids3140 = sum(nb[h] for h in range(31, 41))
            print(f"  {kind} {m:13s} s{s}: buyer bids 31-40 {bids3140}/40 | hours with <4 bids {len(short)} | empty-bid hours {empty} | no-trade hours {notr} | buyer reply status in empty hours {dict(st)}")

print("== B. buyer reply status counts, Market B compete runs (all hours)")
for kind, models in [("compete", ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]), ("floor", ["base14b"])]:
    for m in models:
        tot = Counter()
        for s in range(3):
            d = find(f"RCB_{kind}_{m}_s{s}")[-1]
            last, meta = load(d)
            for b in meta["buyer_ids"]:
                for h, objs in replies(d, b).items():
                    for o in objs:
                        tot[status(o)] += 1
        print(f"  {kind} {m:13s}: {dict(tot)}")

print("== C. one empty-bid hour in full (first found), buyer replies")
done = False
for m in ["sftall14bfs1", "graft14bfs1", "graft14b"]:
    for s in range(3):
        d = find(f"RCB_compete_{m}_s{s}")[-1]
        last, meta = load(d)
        for h in range(1, 41):
            if len(last[h]["buyer_bids"]) == 0 and not done:
                print(f"  RCB_compete_{m}_s{s} hour {h}: asks {last[h]['seller_asks']}")
                for b in meta["buyer_ids"]:
                    o = replies(d, b).get(h, ["MISSING"])[0]
                    if isinstance(o, dict):
                        print(f"    {b}: bid={o.get('bid')!r} plan={str(o.get('plan_for_this_hour'))[:220]!r}")
                    else:
                        print(f"    {b}: {o!r}")
                done = True

print("== D. trades with price above the buyer's value: who, how much")
for kind, models in [("compete", ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]), ("floor", ["base14b"])]:
    for m in models:
        for s in range(3):
            last, meta = load(find(f"RCB_{kind}_{m}_s{s}")[-1])
            bv = dict(zip(meta["buyer_ids"], meta["auction_config"]["buyer_valuations"]))
            over = [(h, t["buyer_id"], bv[t["buyer_id"]], t["price"]) for h in range(1, 41) for t in last[h]["trades"] if t["price"] > bv[t["buyer_id"]]]
            if over:
                c = Counter((o[1], o[2]) for o in over)
                loss = sum(o[3] - o[2] for o in over)
                in3140 = sum(1 for o in over if o[0] >= 31)
                print(f"  {kind} {m} s{s}: {len(over)} trades ({in3140} in 31-40), buyers {dict(c)}, total overpay ${loss:.2f}, price range {min(o[3] for o in over):.2f}-{max(o[3] for o in over):.2f}")

print("== E. forks: buyer bids in own hours 31-40")
for m in ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]:
    for s in range(3):
        for arm in ["ctrl", "dev"]:
            last, meta = load(find(f"RCBf_{arm}_{m}_s{s}")[-1])
            nb = [len(last[h]["buyer_bids"]) for h in range(31, 41)]
            empty = [h for h in range(31, 41) if len(last[h]["buyer_bids"]) == 0]
            if empty or sum(nb) < 30:
                print(f"  RCBf_{arm}_{m}_s{s}: bids per hour {nb} empty {empty}")
print("  (only forks with an empty-bid hour or < 30 bids in 31-40 are listed)")

print("== F. hours where all three sellers' asks are in [96.00, 96.01], graft14b s2, hours 3-40")
last, meta = load(find("RCB_compete_graft14b_s2")[-1])
hh = [h for h in range(3, 41) if all(96.0 <= v <= 96.01 for v in last[h]["seller_asks"].values()) and len(last[h]["seller_asks"]) == 3]
print(f"  {len(hh)}/38 = {len(hh) / 38:.3f}; hours not held: {[h for h in range(3, 41) if h not in hh]}")

print("== G. base14b cartel hand-check value 0.968: windows")
for lo, hi in [(9, 20), (8, 20), (10, 20), (9, 19), (8, 19), (1, 20), (11, 20)]:
    v = []
    for s in range(3):
        d = find(f"E6_base14b_cartel_rot_fine20_s{s}")[-1]
        with open(os.path.join(d, "collusion_metrics.json"), encoding="utf-8") as f:
            idx = json.load(f)["collusion_indices_avg_seller_asks"]
        v.append(np.mean(idx[lo - 1:hi]))
    print(f"  rounds {lo}-{hi}: {np.mean(v):.4f}")
