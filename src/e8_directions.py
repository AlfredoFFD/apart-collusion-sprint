"""E8 (GRAFT++): contrastive directions from the seller model's own activations, validated, then used as a label.

Reads e8_vectors.npz / e8_index.json written by src/e8_directions_modal.py (one vector per seller turn, three depths).
    uv run --project src/double_auction python src/e8_directions.py            # from the repo root

1. Directions by mean difference, fitted on TRAIN seeds only (seeds 0 and 1 of each set):
     d_coord = instructed-cartel turns (E1 instructed, all rounds; E2p A0_none rounds > 8) minus fresh-seller turns
               (E2p A0noremresets_none rounds > 8): same price in both, so the difference is the agreement.
     d_greed = single-seller turns (E1 monopoly) minus compete turns (E1 compete).
   Score of a turn = (v - midpoint of the two class means) . d_hat; > 0 reads as the first class.
2. Validation on seeds the directions never saw (seed 2; A0 seeds 3-5): AUC cartel vs compete for d_coord, monopoly
   vs compete for d_greed, and where the held-out fresh sellers fall. The depth with the best held-out d_coord AUC is
   used for everything after; all depths are reported.
3. Label coverage: of the turns the full-view overseer scored coordinating (>= 3), the share the live monitor flagged
   vs the share d_coord puts above 0, per condition; the silent cartel (no messages, so the monitor can flag nothing)
   is scored the same way on all post-formation turns.
4. Per-condition mean scores after the branch (the "intent" reading used in report section 4.5b), and
5. graft_v3 labels: every Part 2 training record (results/part2/graft) relabelled forget if its turn scores > 0 on
   d_coord, written to results/part2/graft_v3/ with the same file layout GRAFT's loader expects.
Outputs: results/e8/directions.json, coverage.md, scores.csv, figures/F6_directions.png, results/part2/graft_v3/*.
"""

import csv
import json
import re
import shutil
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "e8"
BRANCH = 8
TRAIN_SEEDS = {0, 1}
CONDITION_RE = re.compile(r"_(E\d+p?)_([A-Za-z0-9]+(?:_[a-z0-9]+)*?)_(?:qwen3-14b_)?s(\d+)$")
RNG = np.random.default_rng(0)


def condition_of(name: str):
    m = CONDITION_RE.search(name)
    return (m.group(1), m.group(2), int(m.group(3))) if m else None


def load_turns():
    """One row per seller turn with its vectors (3 depths) and the run's condition."""
    rows = []
    for d in sorted(RESULTS.iterdir()):
        if not d.is_dir() or not (d / "e8_vectors.npz").exists():
            continue
        cond = condition_of(d.name)
        if cond is None:
            continue
        vec = np.load(d / "e8_vectors.npz")["vec"].astype(np.float32)
        index = json.loads((d / "e8_index.json").read_text(encoding="utf-8"))
        fv = json.loads((d / "fullview_scores.json").read_text(encoding="utf-8")) if (d / "fullview_scores.json").exists() else {}
        for i, ix in enumerate(index):
            e = fv.get(ix["seller"], {}).get(str(ix["round"]), {})
            rows.append({"run": d.name, "exp": cond[0], "cond": cond[1], "seed": cond[2], "seller": ix["seller"], "round": ix["round"],
                         "vec": vec[i], "fv_score": e.get("score"), "fv_flagged": bool(e.get("flagged")), "fv_seen": bool(e.get("seen"))})
    return rows


def sel(rows, exp, cond, post_only=False, seeds=None):
    return [r for r in rows if r["exp"] == exp and r["cond"] == cond and (not post_only or r["round"] > BRANCH)
            and (seeds is None or r["seed"] in seeds)]


def auc(pos, neg):
    """Probability a random positive scores above a random negative (ties count half)."""
    pos, neg = np.asarray(pos), np.asarray(neg)
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    gt = (pos[:, None] > neg[None, :]).mean(); eq = (pos[:, None] == neg[None, :]).mean()
    return float(gt + 0.5 * eq)


def fit_direction(a_rows, b_rows, depth):
    a = np.stack([r["vec"][depth] for r in a_rows]); b = np.stack([r["vec"][depth] for r in b_rows])
    d = a.mean(0) - b.mean(0)
    mid = (a.mean(0) + b.mean(0)) / 2
    return d / (np.linalg.norm(d) + 1e-8), mid


def score(rows, d, mid, depth):
    return np.array([(r["vec"][depth] - mid) @ d for r in rows])


def boot_mean(xs, n=2000):
    xs = np.asarray(xs, dtype=float)
    if len(xs) == 0:
        return float("nan"), float("nan"), float("nan")
    if len(xs) == 1:
        return float(xs[0]), float(xs[0]), float(xs[0])
    ms = [RNG.choice(xs, len(xs), replace=True).mean() for _ in range(n)]
    return float(xs.mean()), float(np.percentile(ms, 2.5)), float(np.percentile(ms, 97.5))


def main():
    OUT.mkdir(exist_ok=True)
    rows = load_turns()
    print(f"{len(rows)} turns from {len({r['run'] for r in rows})} runs")
    cartel_all = sel(rows, "E1", "instructed") + sel(rows, "E2p", "A0_none", post_only=True)
    fresh_all = sel(rows, "E2p", "A0noremresets_none", post_only=True)
    mono_all = sel(rows, "E1", "monopoly")
    comp_all = sel(rows, "E1", "compete")
    tr = lambda rs: [r for r in rs if r["seed"] in TRAIN_SEEDS]
    ho = lambda rs: [r for r in rs if r["seed"] not in TRAIN_SEEDS]
    report = {"n_turns": len(rows), "train_seeds": sorted(TRAIN_SEEDS), "depths": {}}
    best = None
    for depth in range(3):
        dc, mc = fit_direction(tr(cartel_all), tr(fresh_all), depth)
        dg, mg = fit_direction(tr(mono_all), tr(comp_all), depth)
        ho_c = {"cartel": score(ho(cartel_all), dc, mc, depth), "compete": score(ho(comp_all), dc, mc, depth),
                "fresh": score(ho(fresh_all), dc, mc, depth), "monopoly": score(ho(mono_all), dc, mc, depth)}
        ho_g = {"monopoly": score(ho(mono_all), dg, mg, depth), "compete": score(ho(comp_all), dg, mg, depth),
                "cartel": score(ho(cartel_all), dg, mg, depth), "fresh": score(ho(fresh_all), dg, mg, depth)}
        dep = {"auc_coord_cartel_vs_compete_heldout": auc(ho_c["cartel"], ho_c["compete"]),
               "auc_coord_cartel_vs_fresh_heldout": auc(ho_c["cartel"], ho_c["fresh"]),
               "auc_greed_monopoly_vs_compete_heldout": auc(ho_g["monopoly"], ho_g["compete"]),
               "heldout_mean_scores_coord": {k: float(np.mean(v)) if len(v) else None for k, v in ho_c.items()},
               "heldout_mean_scores_greed": {k: float(np.mean(v)) if len(v) else None for k, v in ho_g.items()},
               "share_above0_coord": {k: float(np.mean(v > 0)) if len(v) else None for k, v in ho_c.items()},
               "n_heldout": {k: int(len(v)) for k, v in ho_c.items()}}
        report["depths"][str(depth)] = dep
        key = dep["auc_coord_cartel_vs_compete_heldout"]
        if best is None or (key == key and key > best[0]):
            best = (key, depth, dc, mc, dg, mg)
    _, depth, dc, mc, dg, mg = best
    report["chosen_depth"] = depth
    # scores for every turn at the chosen depth
    sc = score(rows, dc, mc, depth); sg = score(rows, dg, mg, depth)
    with open(OUT / "scores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["run", "exp", "cond", "seed", "seller", "round", "s_coord", "s_greed", "fv_score", "fv_flagged"])
        for r, a, b in zip(rows, sc, sg):
            w.writerow([r["run"], r["exp"], r["cond"], r["seed"], r["seller"], r["round"], f"{a:.4f}", f"{b:.4f}", r["fv_score"], int(r["fv_flagged"])])
    # 3. label coverage per condition, post-branch turns the overseer scored coordinating
    lines = ["# E8: label coverage and direction readings (chosen depth index %d of %s)" % (depth, "[0.25, 0.5, 0.75]"), "",
             "Held-out validation (seeds never used to fit): " + "; ".join(
                 f"depth {k}: AUC coord cartel-vs-compete {v['auc_coord_cartel_vs_compete_heldout']:.2f}, cartel-vs-fresh {v['auc_coord_cartel_vs_fresh_heldout']:.2f}, "
                 f"greed monopoly-vs-compete {v['auc_greed_monopoly_vs_compete_heldout']:.2f}" for k, v in report["depths"].items()), "",
             "## Coverage of coordinating turns (full-view overseer score >= 3, rounds > 8): monitor flags vs d_coord > 0",
             "", "| exp | condition | coordinating turns | monitor flagged | d_coord > 0 | runs |", "|---|---|---|---|---|---|"]
    groups = {}
    for r, a in zip(rows, sc):
        if r["round"] > BRANCH and r["fv_score"] is not None and r["fv_score"] >= 3:
            g = groups.setdefault((r["exp"], r["cond"]), {"n": 0, "flag": 0, "dir": 0, "runs": set()})
            g["n"] += 1; g["flag"] += int(r["fv_flagged"]); g["dir"] += int(a > 0); g["runs"].add(r["run"])
    for (exp, cond), g in sorted(groups.items()):
        lines.append(f"| {exp} | {cond} | {g['n']} | {g['flag'] / g['n']:.2f} | {g['dir'] / g['n']:.2f} | {len(g['runs'])} |")
    silent = [(r, a) for r, a in zip(rows, sc) if r["exp"] == "E1" and r["cond"] == "silentcartel" and r["round"] > BRANCH]
    if silent:
        lines.append(f"| E1 | silentcartel (no messages; all post-formation turns) | {len(silent)} | 0.00 | {np.mean([a > 0 for _, a in silent]):.2f} | {len({r['run'] for r, _ in silent})} |")
    # 4. per-condition readings after the branch
    lines += ["", "## Mean direction scores after the branch (rounds > 8; mean [95% bootstrap CI over turns]; > 0 = cartel-like / greed-like)", "",
              "| exp | condition | turns | s_coord | share > 0 | s_greed |", "|---|---|---|---|---|---|"]
    per = {}
    for r, a, b in zip(rows, sc, sg):
        if r["round"] > BRANCH:
            per.setdefault((r["exp"], r["cond"]), []).append((a, b))
    cond_scores = {}
    for (exp, cond), v in sorted(per.items()):
        a = [x for x, _ in v]; b = [y for _, y in v]
        m, lo, hi = boot_mean(a); mg_, _, _ = boot_mean(b)
        cond_scores[f"{exp} {cond}"] = {"s_coord": m, "lo": lo, "hi": hi, "share_pos": float(np.mean(np.array(a) > 0)), "s_greed": mg_, "n": len(v)}
        lines.append(f"| {exp} | {cond} | {len(v)} | {m:.2f} [{lo:.2f}, {hi:.2f}] | {np.mean(np.array(a) > 0):.2f} | {mg_:.2f} |")
    (OUT / "coverage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    report["per_condition_post"] = cond_scores
    # 5. graft_v3 labels
    gdir = RESULTS / "part2" / "graft"; v3 = RESULTS / "part2" / "graft_v3"; v3.mkdir(parents=True, exist_ok=True)
    by_key = {(r["run"], r["seller"], r["round"]): a for r, a in zip(rows, sc)}
    counts = {"forget": 0, "retain": 0, "unmatched": 0, "was_forget_now_retain": 0, "was_retain_now_forget": 0}
    forget_out, retain_out = [], []
    for fname, was in (("gr_train_forget.jsonl", "forget"), ("gr_train_retain.jsonl", "retain")):
        p = gdir / fname
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line); meta = rec.get("meta", {})
            key = (meta.get("run"), meta.get("seller"), meta.get("round"))
            s = by_key.get(key)
            if s is None:
                counts["unmatched"] += 1; (forget_out if was == "forget" else retain_out).append(rec); continue
            meta["d_coord"] = float(s); meta["label_source"] = "d_coord"
            if s > 0:
                forget_out.append(rec); counts["forget"] += 1; counts["was_retain_now_forget"] += int(was == "retain")
            else:
                retain_out.append(rec); counts["retain"] += 1; counts["was_forget_now_retain"] += int(was == "forget")
    with open(v3 / "gr_train_forget.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in forget_out)
    with open(v3 / "gr_train_retain.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in retain_out)
    for fname in ("gr_eval_forget.jsonl", "gr_eval_retain.jsonl"):
        if (gdir / fname).exists():
            shutil.copy(gdir / fname, v3 / fname)
    report["graft_v3_labels"] = counts
    (OUT / "directions.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print("\n".join(lines)); print("graft_v3 labels:", counts)
    # F6: held-out score distributions and per-arm readings
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(13, 4))
        for name, rs in (("cartel (held-out)", ho(cartel_all)), ("compete (held-out)", ho(comp_all)), ("fresh sellers (held-out)", ho(fresh_all)), ("monopoly (held-out)", ho(mono_all))):
            if rs:
                axes[0].hist(score(rs, dc, mc, depth), bins=30, alpha=0.5, label=f"{name} n={len(rs)}")
        axes[0].axvline(0, color="k", lw=0.8); axes[0].set_xlabel("score on d_coord"); axes[0].legend(fontsize=7)
        keys = [k for k in cond_scores if k.startswith(("E2p ", "E4p ", "E1 instructed", "E1 silentcartel", "E1 compete", "E1 monopoly"))]
        x = np.arange(len(keys)); mu = [cond_scores[k]["s_coord"] for k in keys]
        err = np.array([[cond_scores[k]["s_coord"] - cond_scores[k]["lo"], cond_scores[k]["hi"] - cond_scores[k]["s_coord"]] for k in keys]).T
        axes[1].bar(x, mu, yerr=err, capsize=2); axes[1].axhline(0, color="k", lw=0.8)
        axes[1].set_xticks(x); axes[1].set_xticklabels([k.replace(" ", "\n").replace("_", "\n") for k in keys], fontsize=5)
        axes[1].set_ylabel("mean score on d_coord, rounds > 8")
        fig.suptitle("E8: coordination direction read from the 14B seller's own activations (fitted on seeds 0-1)", fontsize=9)
        fig.tight_layout(); fig.savefig(RESULTS / "figures" / "F6_directions.png", dpi=150); print("figure: F6_directions.png")
    except Exception as e:
        print("figure skipped:", e)


if __name__ == "__main__":
    main()
