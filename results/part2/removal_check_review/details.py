"""Detail checks for the reviewer report. Read-only on the repository."""
import json
import os
import re
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util

REPO = r"C:\Users\fabia\dev\apart-collusion-sprint"
RES = os.path.join(REPO, "results")
LINE_RX = re.compile(r"Auction round (\d+) completed with result: (.*)$")
RESP_RX = re.compile(r"^## Response: Round (\d+) - ")


def find(tag):
    rx = re.compile(r"^\d{8}_\d{6}_" + re.escape(tag) + r"$")
    hits = sorted(d for d in os.listdir(RES) if rx.match(d))
    return [os.path.join(RES, h) for h in hits]


def load_log(d):
    entries = []
    with open(os.path.join(d, "unified.log"), encoding="utf-8") as f:
        for line in f:
            if "completed with result:" in line:
                m = LINE_RX.search(line.rstrip("\n"))
                entries.append((int(m.group(1)), json.loads(m.group(2)), line[:23]))
    last = {}
    for r, o, ts in entries:
        last[r] = o
    return entries, last


def replies(d, sid):
    with open(os.path.join(d, sid + ".md"), encoding="utf-8", errors="replace") as f:
        lines = f.read().split("\n")
    out = []
    i = 0
    while i < len(lines):
        m = RESP_RX.match(lines[i])
        if m:
            r = int(m.group(1))
            ts = lines[i].split(" - ", 1)[1]
            k = i + 2
            buf = []
            while k < len(lines) and lines[k] != "````":
                buf.append(lines[k])
                k += 1
            block = "\n".join(buf)
            try:
                obj = json.loads(block)
            except Exception:
                obj = None
            out.append((r, ts, obj, block))
            i = k
        i += 1
    return out


def meta(d):
    with open(os.path.join(d, "experiment_metadata.json"), encoding="utf-8") as f:
        return json.load(f)


# (a) old-market rule 1 with more decimals and the rerun s0 outlier
print("== (a) old market, 4 decimals")
vals = {}
for m in ["graft14bfs1", "graft14brerun", "graft14b"]:
    for cond in ["cartel_rot_fine20", "compete"]:
        for s in range(3):
            d = find(f"E6_{m}_{cond}_s{s}")[0]
            with open(os.path.join(d, "collusion_metrics.json"), encoding="utf-8") as f:
                idx = json.load(f)["collusion_indices_avg_seller_asks"]
            v = np.mean(idx[8:20]) if cond.startswith("cartel") else np.mean(idx)
            vals[(m, cond, s)] = v
            print(f"  {m:14s} {cond:18s} s{s} {v:.4f}  ({os.path.basename(d)})")
for cond in ["compete", "cartel_rot_fine20"]:
    dd = [vals[("graft14bfs1", cond, s)] - vals[("graft14brerun", cond, s)] for s in range(3)]
    print(f"  restored - rerun {cond}: " + " ".join(f"{x:+.4f}" for x in dd) + f" mean {np.mean(dd):+.4f}")
    dd = [vals[("graft14bfs1", cond, s)] - vals[("graft14b", cond, s)] for s in range(3)]
    print(f"  restored - published {cond}: " + " ".join(f"{x:+.4f}" for x in dd) + f" mean {np.mean(dd):+.4f}")
    for m in ["graft14bfs1", "graft14brerun", "graft14b"]:
        print(f"    mean {m} {cond}: {np.mean([vals[(m, cond, s)] for s in range(3)]):.4f}")

d = find("E6_graft14brerun_compete_s0")[0]
_, last = load_log(d)
print("  rerun compete s0 per-round asks / trades:")
for h in range(1, 21):
    o = last[h]
    print(f"   h{h:2d} asks {o['seller_asks']} trades {[(t['seller_id'], t['price']) for t in o['trades']]}")

# reproduction-gate extras: published base14b and sftall14bfs1 E6 rows
print("== (a2) published E6 rows for base14b and sftall14bfs1 (reproduction-gate numbers)")
for m in ["base14b", "sftall14bfs1"]:
    for cond in ["cartel_rot_fine20", "compete"]:
        ds = [find(f"E6_{m}_{cond}_s{s}") for s in range(3)]
        print(f"  {m} {cond}: folders {[ [os.path.basename(x) for x in dd] for dd in ds]}")
        vv = []
        for dd in ds:
            if not dd:
                continue
            with open(os.path.join(dd[-1], "collusion_metrics.json"), encoding="utf-8") as f:
                idx = json.load(f)["collusion_indices_avg_seller_asks"]
            vv.append(np.mean(idx[8:20]) if cond.startswith("cartel") else np.mean(idx))
        print(f"     per seed {[round(x, 4) for x in vv]} mean {np.mean(vv):.4f}")

# (b) string asks and posted asks in Market B compete/floor runs
print("== (b) Market B non-numeric / missing asks with what the market posted")
for kind, models in [("compete", ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]), ("floor", ["base14b"])]:
    for m in models:
        for s in range(3):
            d = find(f"RCB_{kind}_{m}_s{s}")[0]
            md = meta(d)
            _, last = load_log(d)
            for sid in md["seller_ids"]:
                for r, ts, obj, block in replies(d, sid):
                    if obj is None or not isinstance(obj, dict) or "caiac_fallback" in obj or "ask" not in obj \
                            or obj["ask"] is None or not isinstance(obj["ask"], (int, float)):
                        posted = (last.get(r, {}).get("seller_asks") or {}).get(sid, "ABSENT")
                        keys = list(obj.keys()) if isinstance(obj, dict) else None
                        a = obj.get("ask", "<no key>") if isinstance(obj, dict) else "<unparsed>"
                        print(f"  {kind} {m} s{s} {sid} h{r}: ask={a!r} keys={keys} posted={posted}")

# (c) fork transcripts: response counts and non-ok replies in own hours
print("== (c) fork transcripts")
for m in ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]:
    for s in range(3):
        pd = find(f"RCB_compete_{m}_s{s}")[0]
        for arm in ["ctrl", "dev"]:
            d = find(f"RCBf_{arm}_{m}_s{s}")[0]
            md = meta(d)
            _, last = load_log(d)
            for sid in md["seller_ids"]:
                reps = replies(d, sid)
                rounds = [r for r, *_ in reps]
                prep = replies(pd, sid)
                # copied part equals parent?
                ncopy = len(prep)
                same = all(a[3] == b[3] for a, b in zip(reps[:ncopy], prep))
                own = reps[ncopy:]
                ownr = [r for r, *_ in own]
                bad = []
                for r, ts, obj, block in own:
                    if obj is None or not isinstance(obj, dict) or "caiac_fallback" in obj or obj.get("ask") is None:
                        posted = (last.get(r, {}).get("seller_asks") or {}).get(sid, "ABSENT")
                        bad.append((r, "fallback" if isinstance(obj, dict) and "caiac_fallback" in obj else ("unparsed" if obj is None else "no ask"), posted))
                flag = "" if (same and ownr == list(range(31, 41))) else " <-- CHECK"
                if bad or flag:
                    print(f"  RCBf_{arm}_{m}_s{s} {sid}: n={len(reps)} copied_equal_parent={same} own_rounds={ownr} non-ok own={bad}{flag}")
print("  (lines only printed for forks with non-ok own replies or structure problems)")

# (d) forks: own hours identical to the parent's?
print("== (d) fork own hours 31-40 identical to parent hours (full result dict)")
for m in ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]:
    for s in range(3):
        pd = find(f"RCB_compete_{m}_s{s}")[0]
        _, plast = load_log(pd)
        for arm in ["ctrl", "dev"]:
            d = find(f"RCBf_{arm}_{m}_s{s}")[0]
            _, last = load_log(d)
            same_full = [h for h in range(31, 41) if last[h] == plast[h]]
            same_asks = [h for h in range(31, 41) if last[h]["seller_asks"] == plast[h]["seller_asks"]]
            same_msgs = [h for h in range(31, 41) if last[h].get("seller_messages") == plast[h].get("seller_messages")]
            print(f"  RCBf_{arm}_{m}_s{s}: identical full {same_full} | identical asks {same_asks} | identical messages {same_msgs}")

# (e) fork rivals detail per hour
print("== (e) fork rivals' asks hours 31-34 (ctrl | dev)")
for m in ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]:
    for s in range(3):
        dc = find(f"RCBf_ctrl_{m}_s{s}")[0]
        dv = find(f"RCBf_dev_{m}_s{s}")[0]
        _, lc = load_log(dc)
        _, lv = load_log(dv)
        print(f"  {m} s{s}")
        for h in range(31, 35):
            print(f"     h{h} ctrl {lc[h]['seller_asks']} | dev {lv[h]['seller_asks']}")

# (f) boundary values with full precision
print("== (f) precision on boundary values")
for m in ["base14b", "sftall14bfs1", "graft14b", "graft14bfs1"]:
    for s in range(3):
        d = find(f"RCB_compete_{m}_s{s}")[0]
        _, last = load_log(d)
        vals = []
        for h in range(21, 31):
            tr = last[h]["trades"]
            if tr:
                vals.append((np.mean([t["price"] for t in tr]) - 90) / 6)
        v2 = []
        for h in range(31, 41):
            tr = last[h]["trades"]
            if tr:
                v2.append((np.mean([t["price"] for t in tr]) - 90) / 6)
        print(f"  {m} s{s}: tpi21-30 {np.mean(vals):.4f} | tpi31-40 {np.mean(v2):.4f} | trades 31-40 {sum(len(last[h]['trades']) for h in range(31, 41))}")
