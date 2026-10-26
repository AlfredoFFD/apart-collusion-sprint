"""Two paper figures, drawn only from committed result files (no new runs, no randomness).

    python results/paper_figures/make_paper_figures.py

Figure A (Section 4.3, double auction): for each monitor condition, the change in price and in the share of
coordinating messages against the same seed's no-monitor run, mean and 95% bootstrap interval over seeds, as
printed in the "Paired differences" table of results/E5_conditions.md (columns d ask_idx_post, d coord_share_post).
Figure B (Appendix B, Hawthorne duopoly): price-Delta over rounds 16-30 for every game of the four arms, from
results/hawthorne_negotiation/summary.json.
Writes PDF (vector) and PNG (300 dpi) next to this script.
"""
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BLUE, ORANGE = "#2a78d6", "#eb6834"          # categorical slots 1 and 2 (validated, light surface)
INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.linewidth": 0.8, "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.facecolor": "white",
})
CELL = re.compile(r"([+-]?\d+\.\d+) \[([+-]?\d+\.\d+), ([+-]?\d+\.\d+)\] \(n=(\d+)\)")


def paired_rows():
    """Rows of the paired-differences table: {(exp, condition): {column: (mean, lo, hi, n)}}."""
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
                row[h] = tuple(float(x) for x in m.groups()[:3]) + (int(m.group(4)),)
        out[(cells[0], cells[1])] = row
    return out


def figure_a():
    rows = paired_rows()
    conds = [  # label, Qwen condition (E2p), GPT-4.1 condition (E11p)
        ("Silent monitor", "A1silent_rot_nofine", None),
        ("Announced monitor", "A1_rot_nofine", "A1_rot_nofine_gpt41"),
        ("Fined, one seller read", "A2_rot_fine20", "A2_rot_fine20_gpt41"),
        ("Fined, two sellers read", "A2two_rot_fine20", None),
        ("Fined, every seller read", "A2full_rot_fine20", "Afull_rot_fine20_gpt41"),
        ("Fined, told to evade", "A2dodge_rot_fine20", "dodge_rot_fine20_gpt41"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.9), sharey=True, gridspec_kw={"wspace": 0.16})
    panels = [("d ask_idx_post", "Change in price (ask index)", 1.0, (-1.05, 0.15), [-1.0, -0.5, 0.0]),
              ("d coord_share_post", "Change in coordinating messages (points)", 100.0, (-105, 22),
               [-100, -50, 0])]
    ys = list(range(len(conds)))[::-1]
    for ax, (col, xlabel, scale, xlim, xticks) in zip(axes, panels):
        ax.axvline(0, color=AXIS, lw=1.0, zorder=1)
        ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
        for (label, q, g), y in zip(conds, ys):
            for cond, exp, color, dy in ((q, "E2p", BLUE, 0.13), (g, "E11p", ORANGE, -0.13)):
                if cond is None:
                    continue
                m, lo, hi, n = rows[(exp, cond)][col]
                ax.plot([lo * scale, hi * scale], [y + dy, y + dy], color=color, lw=2, solid_capstyle="round",
                        zorder=2)
                ax.plot(m * scale, y + dy, "o", ms=6.5, color=color, mec="white", mew=1.2, zorder=3)
        ax.set_xlim(*xlim)
        ax.set_xticks(xticks)
        ax.set_xlabel(xlabel, fontsize=8.5)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(length=0)
    axes[0].set_yticks(ys)
    axes[0].set_yticklabels([c[0] for c in conds])
    axes[0].set_ylim(-0.6, len(conds) - 0.4)
    axes[0].text(0.02, 1.04, "Price barely moves", transform=axes[0].transAxes, fontsize=9, color=INK,
                 fontweight="bold")
    axes[1].text(0.02, 1.04, "Coordinating messages fall", transform=axes[1].transAxes, fontsize=9, color=INK,
                 fontweight="bold")
    h = [plt.Line2D([], [], marker="o", color=c, lw=2, ms=6, mec="white") for c in (BLUE, ORANGE)]
    fig.legend(h, ["Qwen3-14B", "GPT-4.1"], loc="upper right", bbox_to_anchor=(0.91, 1.10), ncol=2,
               frameon=False, fontsize=8.5, numpoints=1, handlelength=1.6,
               title="dot = mean, line = 95% interval over seeds", title_fontsize=7.5)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig_monitor_words_vs_price.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def figure_b():
    s = json.loads((ROOT / "results/hawthorne_negotiation/summary.json").read_text(encoding="utf-8"))
    arms = [("ON", "Full setup"), ("OFF", "No same-round\nnegotiation"), ("C", "No payoff\nbrief"),
            ("D", "Brief without\nits $20 row")]
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    for yv, txt, style in ((0.0, "competitive price ($14.73)", "-"), (0.5, "cartel threshold", "--"),
                           (1.0, "monopoly price ($19.25)", "-")):
        ax.axhline(yv, color=AXIS if style == "-" else MUTED, lw=0.9, ls=style, zorder=1)
        ax.text(3.62, yv, txt, va="center", ha="left", fontsize=7.5, color=MUTED)
    offsets = [-0.16, -0.08, 0.0, 0.08, 0.16]
    for x, (key, _) in enumerate(arms):
        eps = sorted(s[key]["episodes"], key=lambda e: e["seed"])
        vals = [e["price_delta_r16_30"] for e in eps]
        assert [e["seed"] for e in eps] == [0, 1, 2, 3, 4], key
        ax.plot([x + o for o in offsets], vals, "o", ms=7, color=BLUE, mec="white", mew=1.2, zorder=3)
        mean = sum(vals) / len(vals)
        ax.plot([x - 0.26, x + 0.26], [mean, mean], color=INK, lw=1.6, zorder=2)
        ax.text(x - 0.3, mean, f"mean {mean:.2f}", va="center", ha="right", fontsize=7.5, color=INK)
    ax.text(0.22, 1.166, "3 pairs at $20", va="center", ha="left", fontsize=7.5, color=MUTED)
    ax.set_xticks(range(len(arms)))
    ax.set_xticklabels([a[1] for a in arms], fontsize=8.5)
    ax.set_xlim(-0.95, 3.55)
    ax.set_ylim(-0.12, 1.3)
    ax.set_ylabel("Price index, rounds 16-30\n(0 = competitive, 1 = monopoly)", fontsize=8.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(length=0)
    ax.grid(axis="y", color=GRID, lw=0.6, zorder=0)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig_hawthorne_intervention.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    figure_a()
    figure_b()
    print("wrote", sorted(p.name for p in OUT.glob("fig_*")))
