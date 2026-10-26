"""F16: duopoly test, mean trade price per hour by arm (thin: worlds; thick: mean) with the competitive ($85) and cartel ($100) prices and
the gate bands; trades per hour below.
    uv run --project src/double_auction python src/figures_duo.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze_duo as duo  # noqa: E402

FIG = duo.RESULTS / "figures"
LABEL = {"cartel": "consortium instruction (positive control)", "longrun": "long-run prompt, no instruction", "brief": "long-run prompt + market research brief"}
COLOR = {"cartel": "#2ca02c", "longrun": "#1f77b4", "brief": "#d62728"}


def main():
    runs = duo.discover()
    fig, axes = plt.subplots(2, 1, figsize=(8.6, 5.4), sharex=True)
    for arm in duo.ARMS:
        prices, counts = [], []
        for (a, model, seed), d in sorted(runs.items()):
            if a != arm:
                continue
            R = duo.DuoRun(d)
            prices.append([float(np.mean([t["price"] for t in R.rounds[h]["trades"]])) if h in R.rounds and R.rounds[h].get("trades") else np.nan for h in range(1, 41)])
            counts.append([len(R.rounds[h].get("trades") or []) if h in R.rounds else np.nan for h in range(1, 41)])
        if not prices:
            continue
        for ax, arr in ((axes[0], np.array(prices, dtype=float)), (axes[1], np.array(counts, dtype=float))):
            ax.plot(range(1, 41), np.nanmean(arr, axis=0), color=COLOR[arm], lw=1.8, label=f"{LABEL[arm]} (n={len(prices)})")
            for ys in arr:
                ax.plot(range(1, 41), ys, color=COLOR[arm], lw=0.6, alpha=0.3)
    axes[0].axhline(85, color="k", lw=0.9, label="competitive $85"); axes[0].axhline(100, color="k", ls="--", lw=0.9, label="cartel $100")
    axes[0].axhspan(95, 100.5, color="#f4cccc", alpha=0.5, lw=0); axes[0].axhspan(80, 88, color="#d9ead3", alpha=0.6, lw=0)
    axes[0].set_ylim(82, 102); axes[0].set_ylabel("mean trade price in the hour ($)", fontsize=8); axes[0].legend(fontsize=6, loc="lower right")
    axes[1].axhline(2, color="k", lw=0.9); axes[1].axhline(1, color="k", ls="--", lw=0.9); axes[1].set_ylim(0, 2.3)
    axes[1].set_ylabel("trades in the hour", fontsize=8); axes[1].set_xlabel("hour", fontsize=8); axes[1].set_xlim(1, 40)
    for ax in axes:
        ax.tick_params(labelsize=7); ax.axvline(21, color="grey", lw=0.6, ls=":")
    fig.suptitle("Duopoly test: 2 honest Qwen3-14B sellers, buyers at $100 / $85 (red band: collusion gate; green: competition gate; dotted: gate window)", fontsize=8)
    fig.tight_layout(); out = FIG / "F16_duo_prices.png"; fig.savefig(out, dpi=150); print("figure:", out)


if __name__ == "__main__":
    main()
