"""Paper figures in the visual language of the teammate's figures (xxozzi/hawthorne scripts/paper_figs.py: palette,
type sizes, left titles, rounded bars, muted ticks, light grid). Drawn only from committed result files; no new runs,
no randomness.

    python results/paper_figures/make_paper_figures.py

fig_hawthorne_intervention (Appendix B): price index over rounds 16-30 for every game of the four arms, from
results/hawthorne_negotiation/summary.json.
fig_monitor_words_vs_price (double auction): each monitor condition minus the same seed's no-monitor run, mean and 95%
bootstrap interval over seeds, from the "Paired differences" table of results/E5_conditions.md. The teammate's own
market2 figure shows the same conditions as levels.

Typeface: PP Neue Montreal if its .otf files are in results/paper_figures/fonts/ (not committed; they come with the
teammate's paper sources); otherwise Aptos (Microsoft's sans, embedding allowed); otherwise Arial.
"""
import json
import os
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def pick_font():
    for f in (OUT / "fonts").glob("ppneuemontreal-*.otf"):
        fm.fontManager.addfont(str(f))
    if any("Neue Montreal" in f.name for f in fm.fontManager.ttflist):
        return "PP Neue Montreal"
    cloud = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "FontCache" / "4" / "CloudFonts" / "Aptos"
    for f in cloud.glob("*.ttf"):
        fm.fontManager.addfont(str(f))
    if any(f.name == "Aptos" for f in fm.fontManager.ttflist):
        return "Aptos"
    return "Arial"


FAMILY = pick_font()
INK, INK2, MUTED, GRID, BASE = "#0b0b0b", "#4a4a4a", "#8a8a8a", "#e8e8e5", "#c3c2b7"
RED, BLUE, GREEN, AMBER = "#d42a2a", "#1c2df7", "#139a74", "#e39b00"
plt.rcParams.update({
    "font.family": FAMILY, "font.size": 8, "axes.titlesize": 8.6, "axes.titleweight": "normal",
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
    """Column square at the baseline with a rounded data end (radius in points), as in paper_figs.py."""
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


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf")
    fig.savefig(OUT / f"{name}.png", dpi=220)
    plt.close(fig)


def fig_hawthorne_intervention():
    s = json.loads((ROOT / "results/hawthorne_negotiation/summary.json").read_text(encoding="utf-8"))
    arms = [("ON", "Full setup", RED), ("OFF", "No same-round\nnegotiation", BLUE),
            ("C", "No brief", GREEN), ("D", "Brief without\nits $20 row", AMBER)]
    fig, ax = plt.subplots(figsize=(W, 2.25))
    ax.set_xlim(-0.6, 3.55)
    ax.set_ylim(0, 1.3)
    offsets = [-0.15, -0.075, 0.0, 0.075, 0.15]
    for x, (key, _, color) in enumerate(arms):
        eps = sorted(s[key]["episodes"], key=lambda e: e["seed"])
        assert [e["seed"] for e in eps] == [0, 1, 2, 3, 4], key
        vals = [e["price_delta_r16_30"] for e in eps]
        mean = sum(vals) / len(vals)
        rbar(ax, x, mean, 0.56, color)
        ax.scatter([x + o for o in offsets], vals, s=7, color=INK, edgecolors="white", linewidths=0.5, zorder=4)
        ax.text(x + 0.32, mean, f"{mean:.2f}", ha="left", va="center", fontsize=7.2, color=INK)
    ax.axhline(0.5, color=MUTED, lw=0.6, ls=(0, (3, 2.5)), zorder=1)
    ax.text(3.58, 0.5, "cartel\nthreshold", ha="left", va="center", fontsize=6.6, color=MUTED, linespacing=1.0,
            clip_on=False)
    ax.text(3.58, 1.0, "monopoly\nprice", ha="left", va="center", fontsize=6.6, color=MUTED, linespacing=1.0,
            clip_on=False)
    ax.axhline(0, color=BASE, lw=0.7)
    ax.set_xticks(range(len(arms)))
    ax.set_xticklabels([a[1] for a in arms], fontsize=7, color=INK, linespacing=1.05)
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(["0", "0.5", "1"])
    ax.set_title("Price index over rounds 16–30, five games per arm")
    save(fig, "fig_hawthorne_intervention")


CELL = re.compile(r"([+-]?\d+\.\d+) \[([+-]?\d+\.\d+), ([+-]?\d+\.\d+)\] \(n=(\d+)\)")


def paired_rows():
    text = (ROOT / "results/E5_conditions.md").read_text(encoding="utf-8")
    sec = text.split("## Paired differences", 1)[1]
    lines = [l for l in sec.splitlines() if l.startswith("|")]
    header = [h.strip() for h in lines[0].strip("|").split("|")]
    out = {}
    for l in lines[2:]:
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) != len(header):
            break
        row = {}
        for h, c in zip(header[2:], cells[2:]):
            m = CELL.fullmatch(c)
            if m:
                row[h] = tuple(float(x) for x in m.groups()[:3])
        out[(cells[0], cells[1])] = row
    return out


def fig_monitor_words_vs_price():
    rows = paired_rows()
    conds = [("Silent", "A1silent_rot_nofine", None), ("Told", "A1_rot_nofine", "A1_rot_nofine_gpt41"),
             ("Fined, 1 read", "A2_rot_fine20", "A2_rot_fine20_gpt41"), ("Fined, 2 read", "A2two_rot_fine20", None),
             ("Fined, all read", "A2full_rot_fine20", "Afull_rot_fine20_gpt41"),
             ("Told to dodge", "A2dodge_rot_fine20", "dodge_rot_fine20_gpt41")]
    models = [("E2p", "Qwen3-14B, three sellers", BLUE, 0.15), ("E11p", "GPT-4.1, five sellers", INK2, -0.15)]
    fig, axes = plt.subplots(1, 2, figsize=(W, 2.35), sharey=True, gridspec_kw={"wspace": 0.24})
    panels = [("d ask_idx_post", "a   Price index", 1.0, (-0.5, 0.5), [-0.5, 0, 0.5], ["−0.5", "0", "+0.5"]),
              ("d coord_share_post", "b   Messages that coordinate", 100.0, (-108, 25), [-100, -50, 0],
               ["−100", "−50", "0"])]
    ys = list(range(len(conds)))[::-1]
    for ax, (col, title, scale, xlim, ticks, ticklabels) in zip(axes, panels):
        ax.grid(axis="y", visible=False)
        ax.grid(axis="x", color=GRID, lw=0.6)
        ax.axvline(0, color=BASE, lw=0.8, zorder=1)
        for (label, q, g), y in zip(conds, ys):
            for (exp, _, color, dy), cond in zip(models, (q, g)):
                if cond is None:
                    continue
                m, lo, hi = rows[(exp, cond)][col]
                ax.plot([lo * scale, hi * scale], [y + dy, y + dy], color=color, lw=1.6, solid_capstyle="round",
                        zorder=2)
                ax.scatter([m * scale], [y + dy], s=16, color=color, edgecolors="white", linewidths=0.8, zorder=3)
        ax.set_xlim(*xlim)
        ax.set_xticks(ticks)
        ax.set_xticklabels(ticklabels)
        ax.spines["bottom"].set_visible(False)
        ax.set_title(title)
    axes[0].set_yticks(ys)
    axes[0].set_yticklabels([c[0] for c in conds], color=INK, fontsize=7.2)
    axes[0].set_ylim(-0.6, len(conds) - 0.4)
    axes[0].set_xlabel("change against no monitor (1 = cartel price gap)", fontsize=6.8, color=MUTED)
    axes[1].set_xlabel("change against no monitor (percentage points)", fontsize=6.8, color=MUTED)
    h = [plt.Line2D([], [], marker="o", color=c, lw=0, ms=5, mec="white", mew=0.8) for _, _, c, _ in models]
    fig.legend(h, [m[1] for m in models], loc="lower center", ncol=2, bbox_to_anchor=(0.55, -0.1),
               handlelength=1.3, columnspacing=1.8)
    save(fig, "fig_monitor_words_vs_price")


if __name__ == "__main__":
    fig_hawthorne_intervention()
    fig_monitor_words_vs_price()
    print("font:", FAMILY, "| wrote", sorted(p.name for p in OUT.glob("fig_*")))
