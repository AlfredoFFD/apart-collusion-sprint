"""Two paper figures, drawn only from committed result files (no new runs, no randomness).

    python results/paper_figures/make_paper_figures.py

Figure A (Section 4.3, double auction): for each monitor condition, the change in price and in the share of
coordinating messages against the same seed's no-monitor run, mean and 95% bootstrap interval over seeds, as
printed in the "Paired differences" table of results/E5_conditions.md (columns d ask_idx_post, d coord_share_post).
Figure B (Appendix B, Hawthorne duopoly): price-Delta over rounds 16-30 for every game of the four arms, from
results/hawthorne_negotiation/summary.json.
Journal style: serif type to match the paper, small text, panel labels; the takeaway goes in the LaTeX caption.
Writes PDF (vector, embedded TrueType) and PNG (300 dpi) next to this script.
"""
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BLUE, ORANGE = "#2a78d6", "#eb6834"          # categorical slots 1 and 2 (validated on a light surface)
INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#3a3936", "#7d7b75", "#e6e5df", "#9c9a93"
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "STIXGeneral", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 8.5, "axes.labelsize": 8.5, "axes.titlesize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
    "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.5, "ytick.major.size": 0, "pdf.fonttype": 42, "ps.fonttype": 42,
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
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


def clean(ax):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)


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
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.45), sharey=True, gridspec_kw={"wspace": 0.12})
    panels = [("d ask_idx_post", "(a) Price", "change in ask index", 1.0, (-1.05, 0.2), [-1.0, -0.5, 0.0]),
              ("d coord_share_post", "(b) Coordinating messages", "change in share of messages (points)", 100.0,
               (-105, 22), [-100, -50, 0])]
    ys = list(range(len(conds)))[::-1]
    for ax, (col, title, xlabel, scale, xlim, xticks) in zip(axes, panels):
        ax.axvline(0, color=AXIS, lw=0.8, zorder=1)
        for y in ys:
            ax.axhline(y, color=GRID, lw=0.5, zorder=0)
        for (label, q, g), y in zip(conds, ys):
            for cond, exp, color, dy in ((q, "E2p", BLUE, 0.14), (g, "E11p", ORANGE, -0.14)):
                if cond is None:
                    continue
                m, lo, hi, n = rows[(exp, cond)][col]
                ax.plot([lo * scale, hi * scale], [y + dy, y + dy], color=color, lw=1.3, solid_capstyle="butt",
                        zorder=2)
                ax.plot(m * scale, y + dy, "o", ms=4.2, color=color, mec="white", mew=0.7, zorder=3)
        ax.set_xlim(*xlim)
        ax.set_xticks(xticks)
        ax.set_xlabel(xlabel)
        ax.set_title(title, loc="left", fontsize=9, color=INK, pad=4)
        clean(ax)
    axes[0].set_yticks(ys)
    axes[0].set_yticklabels([c[0] for c in conds])
    axes[0].set_ylim(-0.6, len(conds) - 0.45)
    h = [plt.Line2D([], [], marker="o", color=c, lw=1.3, ms=4.2, mec="white", mew=0.7) for c in (BLUE, ORANGE)]
    fig.legend(h, ["Qwen3-14B", "GPT-4.1"], loc="upper center", bbox_to_anchor=(0.56, -0.02), ncol=2,
               frameon=False, numpoints=1, handlelength=1.4, columnspacing=1.6)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig_monitor_words_vs_price.{ext}", dpi=300, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def figure_b():
    s = json.loads((ROOT / "results/hawthorne_negotiation/summary.json").read_text(encoding="utf-8"))
    arms = [("ON", "Full setup"), ("OFF", "No same-round\nnegotiation"), ("C", "No payoff\nbrief"),
            ("D", "Brief without\nits \\$20 row")]
    fig, ax = plt.subplots(figsize=(4.6, 2.5))
    for yv, txt, style, col in ((0.0, "competitive price", "-", AXIS), (0.5, "cartel threshold", (0, (3, 2)), MUTED),
                                (1.0, "monopoly price", "-", AXIS)):
        ax.axhline(yv, color=col, lw=0.7, ls=style, zorder=1)
        ax.text(3.52, yv, txt, va="center", ha="left", fontsize=7.5, color=MUTED)
    offsets = [-0.14, -0.07, 0.0, 0.07, 0.14]
    labels = []
    for x, (key, name) in enumerate(arms):
        eps = sorted(s[key]["episodes"], key=lambda e: e["seed"])
        assert [e["seed"] for e in eps] == [0, 1, 2, 3, 4], key
        vals = [e["price_delta_r16_30"] for e in eps]
        mean = sum(vals) / len(vals)
        ax.plot([x - 0.24, x + 0.24], [mean, mean], color=INK, lw=1.1, zorder=2)
        ax.plot([x + o for o in offsets], vals, "o", ms=4.6, color=BLUE, mec="white", mew=0.7, zorder=3)
        labels.append(f"{name}\nmean {mean:.2f}")
    ax.set_xticks(range(len(arms)))
    ax.set_xticklabels(labels)
    ax.tick_params(axis="x", length=0, pad=4)
    ax.set_xlim(-0.45, 3.45)
    ax.set_ylim(-0.1, 1.27)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0, 1.25])
    ax.set_ylabel("price index, rounds 16-30")
    clean(ax)
    ax.spines["left"].set_visible(True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig_hawthorne_intervention.{ext}", dpi=300, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


if __name__ == "__main__":
    figure_a()
    figure_b()
    print("wrote", sorted(p.name for p in OUT.glob("fig_*")))
