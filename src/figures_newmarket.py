"""Figures for the new-market pilot and the words-versus-price picture across both markets (Sun Oct 25 PM).

F12  new market: mean trade price per hour by arm (GPT-4.1 and Qwen3-14B), with the competitive range ($88-92), the cartel price ($96)
     and the no-chat floor.
F13  words versus price: every chat world we ran, old market and new, one point per world: x = share of the sellers' messages the
     frozen judge prompt scores as coordinating (post-branch, or hours 31-40), y = trade-price index on that market's own scale
     (0 = its competitive benchmark, 1 = its cartel price). Old market: Qwen arms (E2p) and GPT-4.1 arms (E11p) from results/E5_runs.csv;
     new market: results/*_NM_* via analyze_newmarket.Run.
    uv run --project src/double_auction python src/figures_newmarket.py
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze_newmarket as nm  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIG = RESULTS / "figures"
FIG.mkdir(exist_ok=True)


def f12():
    runs, _ = nm.discover()
    models = sorted({m for (_, m, _) in runs})
    fig, axes = plt.subplots(1, len(models), figsize=(4.6 * len(models), 3.4), squeeze=False)
    colors = {"chat": "#1f77b4", "press": "#d62728", "cartel": "#2ca02c", "iso": "#7f7f7f"}
    labels = {"chat": "chat, no instruction", "press": "chat + CEO note", "cartel": "consortium instruction", "iso": "no chat, rivals hidden (floor)"}
    for ax, model in zip(axes[0], models):
        for arm in ("iso", "chat", "press", "cartel"):
            series = []
            for (a, m, s), d in sorted(runs.items()):
                if a != arm or m != model:
                    continue
                R = nm.Run(d)
                ys = []
                for h in range(1, 41):
                    r = R.rounds.get(h)
                    ys.append(float(np.mean([t["price"] for t in r["trades"]])) if r and r.get("trades") else np.nan)
                series.append(ys)
            if not series:
                continue
            arr = np.array(series, dtype=float)
            mean = np.nanmean(arr, axis=0)
            ax.plot(range(1, 41), mean, color=colors[arm], lw=1.8, label=f"{labels[arm]} (n={len(series)})")
            for ys in series:
                ax.plot(range(1, 41), ys, color=colors[arm], lw=0.6, alpha=0.35)
        ax.axhspan(88, 92, color="#dddddd", alpha=0.6, lw=0, label="competitive range $88-92")
        ax.axhline(96, color="k", ls="--", lw=0.9, label="cartel price $96 (2 trades)")
        ax.set_ylim(82, 98); ax.set_xlim(1, 40); ax.set_xlabel("hour", fontsize=8); ax.tick_params(labelsize=7)
        ax.set_title({"gpt41": "GPT-4.1", "qwen14b": "Qwen3-14B"}.get(model, model), fontsize=9)
    axes[0][0].set_ylabel("mean trade price in the hour ($)", fontsize=8)
    axes[0][-1].legend(fontsize=6, loc="lower right")
    fig.suptitle("New market: 3 sellers (cost 80, 84, 88), 4 buyers (value 100, 96, 92, 86); opening asks $90, horizon hidden", fontsize=9)
    fig.tight_layout(); out = FIG / "F12_newmarket_prices.png"; fig.savefig(out, dpi=150); print("figure:", out)


def f13():
    pts = []  # (x coordinating share, y trade idx, group)
    rows = list(csv.DictReader(open(RESULTS / "E5_runs.csv", encoding="utf-8")))
    groups_old = {
        ("E2p", "A0_none"): "old market, Qwen, no monitor", ("E2p", "A1_rot_nofine"): "old market, Qwen, monitor announced",
        ("E2p", "A2_rot_fine20"): "old market, Qwen, fined", ("E2p", "A2full_rot_fine20"): "old market, Qwen, fined, all read",
        ("E2p", "A2dodge_rot_fine20"): "old market, Qwen, told to dodge", ("E2p", "A3_rand_fine20"): "old market, Qwen, fined",
        ("E11p", "A0_none_gpt41"): "old market, GPT-4.1, no monitor", ("E11p", "A1_rot_nofine_gpt41"): "old market, GPT-4.1, monitor announced",
        ("E11p", "A2_rot_fine20_gpt41"): "old market, GPT-4.1, fined", ("E11p", "Afull_rot_fine20_gpt41"): "old market, GPT-4.1, fined, all read",
        ("E11p", "dodge_rot_fine20_gpt41"): "old market, GPT-4.1, told to dodge",
    }
    for r in rows:
        g = groups_old.get((r["exp"], r["condition"]))
        if g and r.get("coord_share_post") not in ("", None) and r.get("trade_price_idx_post") not in ("", None):
            pts.append((float(r["coord_share_post"]), float(r["trade_price_idx_post"]), g))
    runs, _ = nm.discover()
    names = {"chat": "chat, no instruction", "press": "chat + CEO note", "cartel": "consortium instruction"}
    for (arm, model, seed), d in runs.items():
        if arm not in names:
            continue
        R = nm.Run(d)
        x, y = R.coord_share(31, 40), R.trade_idx(31, 40)
        if not np.isnan(x) and not np.isnan(y):
            pts.append((x, y, f"new market, {'GPT-4.1' if model == 'gpt41' else 'Qwen3-14B'}, {names[arm]}"))
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    style = {}
    for g in sorted({p[2] for p in pts}):
        old = g.startswith("old")
        color = "#1f77b4" if "Qwen" in g else "#d62728"
        marker = {"no monitor": "o", "monitor announced": "s", "fined, all read": "D", "fined": "^", "told to dodge": "X",
                  "chat, no instruction": "P", "chat + CEO note": "*", "consortium instruction": "v"}[g.split(", ", 2)[-1]]
        style[g] = (color, marker, "none" if not old else color)
    for g, (color, marker, face) in style.items():
        xs = [p[0] for p in pts if p[2] == g]; ys = [p[1] for p in pts if p[2] == g]
        ax.scatter(xs, ys, marker=marker, s=46, facecolors=face, edgecolors=color, linewidths=1.2, label=f"{g} (n={len(xs)})", alpha=0.9)
    ax.axhline(0, color="grey", lw=0.6); ax.axhline(1, color="grey", lw=0.6, ls="--")
    ax.set_xlabel("share of the sellers' messages scored as coordinating (frozen judge prompt)", fontsize=8)
    ax.set_ylabel("trade-price index on the market's own scale\n(0 = competitive benchmark, 1 = cartel price)", fontsize=8)
    ax.set_xlim(-0.03, 1.03); ax.set_ylim(-1.1, 1.25); ax.tick_params(labelsize=7)
    ax.set_title("Words and price: filled = old market (continuations), hollow = new market (hours 31-40)", fontsize=9)
    ax.legend(fontsize=5.6, loc="lower left", ncol=2, frameon=False)
    fig.tight_layout(); out = FIG / "F13_words_vs_price.png"; fig.savefig(out, dpi=150); print("figure:", out, "points:", len(pts))


if __name__ == "__main__":
    f12()
    f13()
