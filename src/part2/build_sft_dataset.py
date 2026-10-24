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
    for run in run_dirs:
        m = COND_RE.search(run.name)
        cond = m.group(2) if m else run.name
        fv = run / "fullview_scores.json"
        scores = json.loads(fv.read_text(encoding="utf-8")) if fv.exists() else {}
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
        for seller, rn, prompt, resp in turns(run):
            counts["anchor"] += 1
            files["anchor"].write(json.dumps({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": resp}],
                                              "label": "anchor", "run": run.name, "seller": seller, "round": rn}, ensure_ascii=False) + "\n")
    for f in files.values():
        f.close()
    (OUT / "counts.json").write_text(json.dumps(counts, indent=1), encoding="utf-8")
    print(counts, "->", OUT)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", action="append", default=[], help="run folders for the training mix (repeatable)")
    ap.add_argument("--anchor-glob", action="append", default=[], help="run folders for the clean anchor set (compete runs)")
    a = ap.parse_args()
    runs = sorted({Path(p) for g in a.glob for p in glob.glob(g) if Path(p).is_dir()})
    anchors = sorted({Path(p) for g in a.anchor_glob for p in glob.glob(g) if Path(p).is_dir()})
    build(runs, anchors)
