"""Relabel the Part 2 training pools with the FULL-VIEW overseer (every message scored), i.e. a monitor with perfect
coverage of the chat: forget = the turn's message scored >= 3, retain = everything else. Compared with the budgeted
monitor's label (results/part2/graft, flagged = seen and scored >= 3), this isolates the label's coverage as the
variable: same data, same recipe (GRAFT 'filtered' mode = SFT on the retain pool), only the label changes.
    uv run --project src/double_auction python src/part2/build_fullview_pools.py
Writes results/part2/graft_fullview/gr_train_{forget,retain}.jsonl (+ the eval files copied) and prints the counts.
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
SRC = RESULTS / "part2" / "graft"
OUT = RESULTS / "part2" / "graft_fullview"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fv_cache = {}

    def fv_score(run, seller, rn):
        if run not in fv_cache:
            p = RESULTS / run / "fullview_scores.json"
            fv_cache[run] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        return fv_cache[run].get(seller, {}).get(str(rn), {}).get("score")

    forget, retain = [], []
    counts = {"forget": 0, "retain_clean_message": 0, "retain_no_message": 0, "retain_no_fullview_file": 0, "was_forget": 0, "was_retain": 0}
    for fname, was in (("gr_train_forget.jsonl", "forget"), ("gr_train_retain.jsonl", "retain")):
        for line in (SRC / fname).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line); meta = rec["meta"]
            s = fv_score(meta["run"], meta["seller"], meta["round"])
            meta["fullview_score"] = s; meta["label_source"] = "fullview_overseer"
            counts["was_" + was] += 1
            if s is not None and s >= 3:
                forget.append(rec); counts["forget"] += 1
            else:
                retain.append(rec)
                if s is None:
                    has_file = (RESULTS / meta["run"] / "fullview_scores.json").exists()
                    counts["retain_no_message" if has_file else "retain_no_fullview_file"] += 1
                else:
                    counts["retain_clean_message"] += 1
    with open(OUT / "gr_train_forget.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in forget)
    with open(OUT / "gr_train_retain.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in retain)
    for fname in ("gr_eval_forget.jsonl", "gr_eval_retain.jsonl"):
        if (SRC / fname).exists():
            shutil.copy(SRC / fname, OUT / fname)
    (OUT / "counts.json").write_text(json.dumps(counts, indent=1), encoding="utf-8")
    print(counts)


if __name__ == "__main__":
    main()
