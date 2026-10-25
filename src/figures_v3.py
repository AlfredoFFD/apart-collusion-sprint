"""Plan v3 figures: F10 (GPT-4.1 coalitions under our monitors, ask index by round, forks share the prefix) and
F11 (what carries the price: the carrier 2x2 from the no-reminder forks). Reads results/ only.
    uv run --project src/double_auction python src/figures_v3.py
"""
import csv
import glob
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS, FIG = ROOT / "results", ROOT / "results" / "figures"
ARMS = [("A0_none", "no monitor"), ("A1_rot_nofine", "announced, no fine"), ("A2_rot_fine20", "fined, 1 of 5 read"),
        ("Afull_rot_fine20", "fined, all 5 read"), ("dodge_rot_fine20", "told to dodge (control)")]


def ask_idx_by_round(run_dir):
    m = json.loads((Path(run_dir) / "collusion_metrics.json").read_text(encoding="utf-8"))
    return [x if isinstance(x, (int, float)) else np.nan for x in m.get("collusion_indices_avg_seller_asks") or []]


def f10(model="gpt41", k=15):
    FIG.mkdir(parents=True, exist_ok=True)
    seeds = sorted({int(Path(d).name.rsplit("_s", 1)[1]) for d in glob.glob(str(RESULTS / f"*E11p_A0_none_{model}_s*"))})
    if not seeds:
        print("F10: no E11p runs for", model); return
    fig, axes = plt.subplots(1, len(seeds), figsize=(3.6 * len(seeds), 3.3), sharey=True, squeeze=False)
    for ax, s in zip(axes[0], seeds):
        for arm, label in ARMS:
            ds = glob.glob(str(RESULTS / f"*E11p_{arm}_{model}_s{s}"))
            if not ds:
                continue
            y = ask_idx_by_round(ds[-1])
            ax.plot(range(1, len(y) + 1), y, lw=1.2, label=label)
        ax.axvline(k + 0.5, color="grey", ls=":", lw=0.8); ax.axhline(0, color="grey", lw=0.5); ax.axhline(1, color="grey", lw=0.5)
        ax.set_title(f"seed {s}", fontsize=9); ax.set_xlabel("round", fontsize=8); ax.tick_params(labelsize=7)
    axes[0][0].set_ylabel("ask index (0 = $90, 1 = $100)", fontsize=8); axes[0][0].legend(fontsize=6)
    fig.suptitle("GPT-4.1 coalitions (5 sellers / 5 buyers, CEO pressure, no instruction): monitors from round 16", fontsize=9)
    fig.tight_layout(); out = FIG / f"F10_{model}_forks.png"; fig.savefig(out, dpi=150); print("figure:", out)


def f11():
    rows = list(csv.DictReader(open(RESULTS / "E5_runs.csv", encoding="utf-8")))
    def mean_post(cond, exp="E2p"):
        v = [float(r["ask_idx_post"]) for r in rows if r["exp"] == exp and r["condition"] == cond and r.get("ask_idx_post") not in ("", None)]
        return (np.mean(v), np.std(v) / np.sqrt(len(v)) if len(v) > 1 else 0.0, len(v)) if v else (np.nan, 0.0, 0)
    cells = [("agents kept\nmarket kept\n(instruction removed)", mean_post("A0norem_none")),
             ("agents fresh\nmarket kept", mean_post("A0noremresetboth_none")),
             ("agents kept\nmarket fresh", mean_post("A0noremmreset_none")),
             ("agents fresh\nmarket fresh\nlast 3 messages kept", mean_post("A0noremresetbothmreset_none")),
             ("agents fresh\nmarket fresh\nmessages gone", mean_post("A0noremresetall_none")),
             ]
    # neither: fresh base-prompt markets (E1 rows, whole run) as the floor
    floor = [float(r["ask_idx_post"]) for r in rows if r["exp"] == "E1" and r["condition"] in ("nochat", "pressure", "isolated", "compete") and r.get("ask_idx_post") not in ("", None)]
    cells.append(("neither\n(fresh base-prompt\nmarket, E1)", (np.mean(floor), np.std(floor) / np.sqrt(len(floor)) if len(floor) > 1 else 0.0, len(floor))))
    fig, ax = plt.subplots(figsize=(7.8, 3.5))
    xs = np.arange(len(cells)); ys = [c[1][0] for c in cells]; es = [c[1][1] for c in cells]
    ax.bar(xs, ys, yerr=es, color=["#444", "#777", "#777", "#999", "#1f77b4", "#bbb"], capsize=3)
    for x, (label, (m, _, n)) in zip(xs, cells):
        ax.text(x, (m if m == m else 0) + 0.03, f"{m:.2f}\nn={n}", ha="center", fontsize=7)
    ax.set_xticks(xs); ax.set_xticklabels([c[0] for c in cells], fontsize=7); ax.set_ylabel("ask index after the branch (rounds 9-20)", fontsize=8)
    ax.axhline(0, color="grey", lw=0.5); ax.axhline(1, color="grey", lw=0.5); ax.set_ylim(-0.3, 1.15)
    ax.set_title("What carries the cartel price: notes, book or chat alone is enough; none of them, and it falls", fontsize=9)
    fig.tight_layout(); out = FIG / "F11_carriers_2x2.png"; fig.savefig(out, dpi=150); print("figure:", out)


if __name__ == "__main__":
    f10("gpt41")
    f10("qwen14b")
    f11()
