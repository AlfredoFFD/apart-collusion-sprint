import json, os, re
RES = r"C:\Users\fabia\dev\apart-collusion-sprint\results"
RX = re.compile(r"Auction round (\d+) completed with result: (.*)$")
def find(tag):
    rx = re.compile(r"^\d{8}_\d{6}_" + re.escape(tag) + r"$")
    return [os.path.join(RES, h) for h in sorted(d for d in os.listdir(RES) if rx.match(d))][-1]
def load(d):
    last = {}
    for line in open(os.path.join(d, "unified.log"), encoding="utf-8"):
        if "completed with result:" in line:
            m = RX.search(line.rstrip("\n")); last[int(m.group(1))] = json.loads(m.group(2))
    meta = json.load(open(os.path.join(d, "experiment_metadata.json"), encoding="utf-8"))
    return last, meta
for kind, models in [("compete", ["base14b","sftall14bfs1","graft14b","graft14bfs1"]), ("floor", ["base14b"])]:
    for m in models:
        row = []
        for s in range(3):
            last, meta = load(find(f"RCB_{kind}_{m}_s{s}"))
            sc = dict(zip(meta["seller_ids"], meta["auction_config"]["seller_valuations"]))
            bc = [(h, t) for h in range(1, 41) for t in last[h]["trades"] if t["price"] < sc[t["seller_id"]]]
            n140 = len(bc); l140 = sum(sc[t["seller_id"]] - t["price"] for h, t in bc)
            b3 = [(h, t) for h, t in bc if h >= 31]
            n3 = len(b3); l3 = sum(sc[t["seller_id"]] - t["price"] for h, t in b3)
            costs = sorted(set(sc[t["seller_id"]] for h, t in bc))
            row.append(f"s{s}: 1-40 {n140} (${l140:.2f}) | 31-40 {n3} (${l3:.2f}) | sellers' cost {costs}")
        print(f"{kind} {m:13s} " + " || ".join(row))
