"""Appendix B figure (Hawthorne duopoly intervention test), in the visual language of the teammate's paper figures
(xxozzi/hawthorne scripts/paper_figs.py: palette, type sizes, rounded bars, left titles). Drawn only from committed
result files; no new runs, no randomness.

    python results/paper_figures/make_paper_figures.py

Data: results/hawthorne_negotiation/summary.json (price_delta_r16_30 for every game of the four arms).
Typeface: PP Neue Montreal when its .otf files are in results/paper_figures/fonts/ (the files are not committed;
they come with the teammate's paper sources); otherwise Arial. Writes PDF and PNG next to this script.
Section 4.3 uses the teammate's own market2 figure (report/paper/figs/market2.pdf in xxozzi/hawthorne), which shows
the same double-auction numbers in this style.
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
for f in (OUT / "fonts").glob("ppneuemontreal-*.otf"):
    fm.fontManager.addfont(str(f))
FAMILY = "PP Neue Montreal" if any("Neue Montreal" in f.name for f in fm.fontManager.ttflist) else "Arial"

# palette and type, as in the teammate's scripts/paper_figs.py
INK, INK2, MUTED, GRID, BASE = "#0b0b0b", "#4a4a4a", "#8a8a8a", "#e8e8e5", "#c3c2b7"
RED, BLUE, GREEN, AMBER = "#d42a2a", "#1c2df7", "#139a74", "#e39b00"
plt.rcParams.update({
    "font.family": FAMILY, "font.size": 8, "axes.titlesize": 8.6, "axes.titleweight": "medium",
    "axes.titlelocation": "left", "axes.titlepad": 10, "axes.labelsize": 7.6, "axes.labelcolor": INK2,
    "axes.edgecolor": BASE, "axes.linewidth": 0.7, "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelsize": 7.2,
    "ytick.labelsize": 7.2, "xtick.major.size": 0, "ytick.major.size": 0, "xtick.major.pad": 5,
    "ytick.major.pad": 4, "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.axisbelow": True, "legend.frameon": False, "legend.fontsize": 7.4, "figure.dpi": 200,
    "pdf.fonttype": 42, "savefig.bbox": "tight", "savefig.pad_inches": 0.03, "text.color": INK,
    "lines.solid_capstyle": "round",
})
W = 5.5  # the teammate's figure width, inches


def rbar(ax, x, h, w, color, base=0.0, r_pt=2.2):
    """Column square at the baseline with a rounded data end (radius in points); as in paper_figs.py."""
    fig = ax.figure
    fig.canvas.draw_idle()
    bb = ax.get_window_extent()
    rx = r_pt * np.diff(ax.get_xlim())[0] / bb.width * fig.dpi / 72
    ry = r_pt * np.diff(ax.get_ylim())[0] / bb.height * fig.dpi / 72
    if abs(h) < 1e-9:
        return
    ext = ry * 1.2
    box = FancyBboxPatch((x - w / 2, base - ext), w, h + ext, boxstyle=f"round,pad=0,rounding_size={rx}",
                         mutation_aspect=ry / rx, fc=color, ec="none", zorder=2)
    ax.add_patch(box)
    box.set_clip_path(Rectangle((x - w, base), 2 * w, h + ext, transform=ax.transData))


def figure_b():
    s = json.loads((ROOT / "results/hawthorne_negotiation/summary.json").read_text(encoding="utf-8"))
    arms = [("ON", "Full setup", RED), ("OFF", "No same-round\nnegotiation", BLUE),
            ("C", "No payoff\nbrief", GREEN), ("D", "Brief without\nits $20 row", AMBER)]
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.set_xlim(-0.6, 3.6)
    ax.set_ylim(0, 1.32)
    offsets = [-0.16, -0.08, 0.0, 0.08, 0.16]
    for x, (key, name, color) in enumerate(arms):
        eps = sorted(s[key]["episodes"], key=lambda e: e["seed"])
        assert [e["seed"] for e in eps] == [0, 1, 2, 3, 4], key
        vals = [e["price_delta_r16_30"] for e in eps]
        mean = sum(vals) / len(vals)
        rbar(ax, x, mean, 0.58, color)
        ax.scatter([x + o for o in offsets], vals, s=9, color=INK, edgecolors="white", linewidths=0.6, zorder=4)
        ax.text(x + 0.33, mean, f"{mean:.2f}", ha="left", va="center", fontsize=7, fontweight="medium", color=INK)
    ax.axhline(0.5, color=MUTED, lw=0.7, ls=(0, (3, 2.5)), zorder=1)
    ax.text(3.62, 0.5, "cartel\nthreshold", ha="left", va="center", fontsize=6.6, color=MUTED, linespacing=1.0)
    ax.text(3.62, 1.0, "monopoly\nprice", ha="left", va="center", fontsize=6.6, color=MUTED, linespacing=1.0)
    ax.axhline(0, color=BASE, lw=0.7)
    ax.set_xticks(range(len(arms)))
    ax.set_xticklabels([a[1] for a in arms], fontsize=6.8, color=INK, linespacing=1.05)
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(["0", "0.5", "1"])
    ax.set_title("Price index over rounds 16-30, by arm")
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig_hawthorne_intervention.{ext}", dpi=220 if ext == "png" else None)
    plt.close(fig)


if __name__ == "__main__":
    figure_b()
    print("font:", FAMILY, "| wrote", sorted(p.name for p in OUT.glob("fig_hawthorne_intervention.*")))
