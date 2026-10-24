"""Part 2 data (PRD section 4.1): seller turns from the auction logs -> SFT datasets with monitor labels.

For every run folder given, each seller turn (prompt -> JSON response) becomes one chat example. Labels come from
fullview_scores.json (run src/fullview_overseer.py first):
  flagged = the in-run monitor saw it and scored it >= threshold      -> what a real monitor would catch
  missed  = coordinating (>= threshold) but the monitor did not see it -> what GRAFT must remove without being told
  clean   = everything else
Prices-only cartel runs have no coordinating *messages*, so their turns are labelled clean by the message monitor even
though the behaviour is collusive: that is the structurally-missed collusion (PRD 4.1b).

Outputs (JSONL, one example per line: {"messages": [...], "label", "run", "condition", "seller", "round"}):
  results/part2/sft_all.jsonl        every turn
  results/part2/sft_filtered.jsonl   every turn except flagged
  results/part2/sft_graft.jsonl      every turn, with "forget": true on flagged turns (GRAFT routes those to FORGET)
  results/part2/anchor.jsonl         turns from compete runs only (GRAFT's clean RETAIN/anchor data)

    uv run --project src/double_auction python src/part2/build_sft_dataset.py --glob "results/*E1_instructed*" \
        --glob "results/*E1_prices_only*" --anchor-glob "results/*E1_compete*"
"""

import argparse
import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "part2"
COND_RE = re.compile(r"_(E\d+p?)_([A-Za-z0-9]+(?:_[a-z0-9]+)*?)_(?:qwen3-14b_)?s(\d+)$")


def turns(run_dir: Path):
    for md in sorted(run_dir.glob("Seller *.md")):
        text = md.read_text(encoding="utf-8", errors="replace")
        prompts = {int(m.group(1)): m.group(2) for m in re.finditer(r"## Prompt: Round (\d+) - .*?\n``````\n(.*?)\n``````", text, re.S)}
        for m in re.finditer(r"## Response: Round (\d+) - .*?\n````json\n(.*?)\n````", text, re.S):
            rn = int(m.group(1))
            if rn not in prompts:
                continue
            try:
                resp = json.loads(m.group(2))
            except json.JSONDecodeError:
                continue
            resp = {k: v for k, v in resp.items() if not k.startswith("_") and k != "caiac_fallback"}  # private thinking stays out of training data
            yield md.stem, rn, prompts[rn], json.dumps(resp, ensure_ascii=False)


def label_for(scores, seller, rn):
    e = scores.get(seller, {}).get(str(rn)) or scores.get(seller, {}).get(rn)
    if not e:
        return "clean"
    if e.get("flagged"):
        return "flagged"
    if e.get("missed"):
        return "missed"
    return "clean"


def build(run_dirs, anchor_dirs):
    OUT.mkdir(parents=True, exist_ok=True)
    files = {k: open(OUT / f"{k}.jsonl", "w", encoding="utf-8") for k in ("sft_all", "sft_filtered", "sft_graft", "anchor")}
    counts = {"flagged": 0, "missed": 0, "clean": 0, "anchor": 0}
    skipped = []
    for run in run_dirs:
        m = COND_RE.search(run.name)
        cond = m.group(2) if m else run.name
        fv = run / "fullview_scores.json"
        if not fv.exists():  # unscored runs would be mislabelled "clean"; refuse them
            skipped.append(run.name)
            continue
        scores = json.loads(fv.read_text(encoding="utf-8"))
        for seller, rn, prompt, resp in turns(run):
            lab = label_for(scores, seller, rn)
            counts[lab] += 1
            ex = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": resp}],
                  "label": lab, "run": run.name, "condition": cond, "seller": seller, "round": rn}
            files["sft_all"].write(json.dumps(ex, ensure_ascii=False) + "\n")
            if lab != "flagged":
                files["sft_filtered"].write(json.dumps(ex, ensure_ascii=False) + "\n")
            files["sft_graft"].write(json.dumps({**ex, "forget": lab == "flagged"}, ensure_ascii=False) + "\n")
    for run in anchor_dirs:
        fv = run / "fullview_scores.json"
        scores = json.loads(fv.read_text(encoding="utf-8")) if fv.exists() else {}
        for seller, rn, prompt, resp in turns(run):
            e = scores.get(seller, {}).get(str(rn)) or {}
            if e.get("score") is not None and e["score"] >= 3:  # anchor = clean turns only
                counts["anchor_dropped_coordinating"] = counts.get("anchor_dropped_coordinating", 0) + 1
                continue
            counts["anchor"] += 1
            files["anchor"].write(json.dumps({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": resp}],
                                              "label": "anchor", "run": run.name, "seller": seller, "round": rn}, ensure_ascii=False) + "\n")
    for f in files.values():
        f.close()
    # GRAFT's own layout (vendor/GRAFT/sft/scripts/gr/loader.py reads these from GRAFT_SFT_DATA_DIR):
    #   gr_train_forget.jsonl = flagged turns (CLASS_FORGET)
    #   gr_train_retain.jsonl = everything else; meta.classification "baseline" = clean/anchor (eligible for RETAIN),
    #                           "missed" = coordinating but unseen by the monitor (stays UNCLASSIFIED, as a false negative)
    #   gr_eval_*.jsonl       = small held-out copies so the trainer's eval hooks have something to read
    gdir = OUT / "graft"; gdir.mkdir(exist_ok=True)
    forget, retain = [], []
    for line in open(OUT / "sft_all.jsonl", encoding="utf-8"):
        ex = json.loads(line)
        rec = {"messages": ex["messages"], "meta": {"classification": "hack" if ex["label"] == "flagged" else ("missed" if ex["label"] == "missed" else "baseline"),
                                                    "run": ex["run"], "seller": ex["seller"], "round": ex["round"]}}
        (forget if ex["label"] == "flagged" else retain).append(rec)
    for line in open(OUT / "anchor.jsonl", encoding="utf-8"):
        ex = json.loads(line)
        retain.append({"messages": ex["messages"], "meta": {"classification": "baseline", "run": ex["run"], "seller": ex["seller"], "round": ex["round"], "anchor": True}})
    def dump(name, recs):
        with open(gdir / name, "w", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + chr(10))
    dump("gr_train_forget.jsonl", forget); dump("gr_train_retain.jsonl", retain)
    dump("gr_eval_forget.jsonl", forget[: max(1, len(forget) // 10)]); dump("gr_eval_retain.jsonl", retain[: max(1, len(retain) // 10)])
    counts["graft_forget"], counts["graft_retain"] = len(forget), len(retain)
    (OUT / "counts.json").write_text(json.dumps(counts, indent=1), encoding="utf-8")
    print(counts, "->", OUT, "and", gdir)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", action="append", default=[], help="run folders for the training mix (repeatable)")
    ap.add_argument("--anchor-glob", action="append", default=[], help="run folders for the clean anchor set (compete runs)")
    a = ap.parse_args()
    runs = sorted({Path(p) for g in a.glob for p in glob.glob(g) if Path(p).is_dir()})
    anchors = sorted({Path(p) for g in a.anchor_glob for p in glob.glob(g) if Path(p).is_dir()})
    build(runs, anchors)
