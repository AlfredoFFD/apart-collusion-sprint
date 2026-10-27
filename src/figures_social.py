"""Social-media figure: fines emptied the chat, the price stayed (GPT-4.1 forks).

Reads the two rows it needs from results/E5_conditions.md (no numbers are typed into
this file) and writes results/figures/S1_gpt41_talk_vs_price.png at 1600 x 900 px.

Rows: E11p / A0_none_gpt41 (no monitor) and E11p / Afull_rot_fine20_gpt41 (every
seller read, $20 fine). Columns: coord_share_post (share of post-branch messages
the judge calls coordinating) and ask_idx_post (mean seller ask on the 0 = $90
competitive, 1 = $100 cartel index). Cells are "mean [lo, hi]" over 3 seeds, the
bracket being the 95% bootstrap interval that src/analyze.py writes.

Run:  uv run python src/figures_social.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "results" / "E5_conditions.md"
OUT = ROOT / "results" / "figures" / "S1_gpt41_talk_vs_price.png"

ROWS = {
    "no_monitor": ("E11p", "A0_none_gpt41"),
    "fined_all": ("E11p", "Afull_rot_fine20_gpt41"),
}
COLS = ("coord_share_post", "ask_idx_post")

# dataviz reference palette, light mode (references/palette.md)
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
BLUE = "#2a78d6"

CELL = re.compile(r"^\s*(-?\d+\.\d+)\s*\[\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)\s*\]\s*$")


def load_rows() -> dict[str, dict[str, tuple[float, float, float]]]:
    lines = TABLE.read_text(encoding="utf-8").splitlines()
    header = next(l for l in lines if l.startswith("| exp | condition |"))
    names = [c.strip() for c in header.strip().strip("|").split("|")]
    idx = {n: i for i, n in enumerate(names)}
    out: dict[str, dict[str, tuple[float, float, float]]] = {}
    for key, (exp, cond) in ROWS.items():
        row = next(
            l for l in lines if l.startswith(f"| {exp} | {cond} |")
        )
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        out[key] = {}
        for col in COLS:
            m = CELL.match(cells[idx[col]])
            if not m:
                sys.exit(f"cannot parse {exp}/{cond}/{col}: {cells[idx[col]]!r}")
            out[key][col] = tuple(float(g) for g in m.groups())  # type: ignore[assignment]
    return out


def pick_font() -> str:
    for name in ("Segoe UI", "Inter", "Helvetica", "Arial", "DejaVu Sans"):
        if any(f.name == name for f in font_manager.fontManager.ttflist):
            return name
    return "DejaVu Sans"


def panel(ax, title, caption, vals, fmt, ymax, yticks, ytick_labels):
    labels = ["No monitor", "Every seller read,\n\\$20 fine per message"]
    xs = [0, 1]
    means = [v[0] for v in vals]
    los = [v[1] for v in vals]
    his = [v[2] for v in vals]
    ax.bar(xs, means, width=0.36, color=BLUE, linewidth=0, zorder=3)
    # 95% bootstrap interval as a thin muted whisker
    for x, lo, hi in zip(xs, los, his):
        ax.plot([x, x], [lo, hi], color=INK2, linewidth=1.4, solid_capstyle="butt", zorder=4)
        ax.plot([x - 0.05, x + 0.05], [lo, lo], color=INK2, linewidth=1.4, zorder=4)
        ax.plot([x - 0.05, x + 0.05], [hi, hi], color=INK2, linewidth=1.4, zorder=4)
    # direct value labels above the whisker
    for x, m, hi in zip(xs, means, his):
        ax.text(x, hi + ymax * 0.035, fmt(m), ha="center", va="bottom",
                fontsize=19, color=INK, fontweight="semibold", zorder=5)
    ax.set_title(title, fontsize=17, color=INK, loc="left", pad=30)
    ax.text(0.0, 1.03, caption, transform=ax.transAxes, fontsize=11.5, color=INK2,
            ha="left", va="bottom")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=13, color=INK2)
    ax.set_ylim(0, ymax)
    ax.set_xlim(-0.6, 1.6)
    ax.set_yticks(yticks)
    ax.set_yticklabels(ytick_labels, fontsize=12, color=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=1, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    ax.spines["bottom"].set_linewidth(1)
    ax.tick_params(axis="both", length=0)
    ax.set_facecolor(SURFACE)


def main() -> None:
    rows = load_rows()
    plt.rcParams["font.family"] = pick_font()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.64, bottom=0.23, wspace=0.35)

    coord = [rows["no_monitor"]["coord_share_post"], rows["fined_all"]["coord_share_post"]]
    ask = [rows["no_monitor"]["ask_idx_post"], rows["fined_all"]["ask_idx_post"]]

    panel(ax1, "Messages that coordinate on price",
          "share of all seller messages",
          coord, lambda m: f"{round(m * 100):.0f}%", 1.32,
          [0, 0.25, 0.5, 0.75, 1.0], ["0", "25%", "50%", "75%", "100%"])
    panel(ax2, "Price index",
          "0 = competitive (\\$90), 1 = cartel (\\$100)",
          ask, lambda m: f"{m:.2f}", 1.32,
          [0, 0.25, 0.5, 0.75, 1.0], ["0", "0.25", "0.50", "0.75", "1"])

    fig.text(0.07, 0.95, "Fines emptied the chat. The price stayed.",
             fontsize=24, color=INK, fontweight="bold", ha="left", va="top")
    fig.text(0.07, 0.865,
             "GPT-4.1 sellers in a simulated market, rounds 16 to 30 after the monitor starts.",
             fontsize=11.5, color=INK2, ha="left", va="top")
    fig.text(0.07, 0.825,
             "Bars: mean of 3 seeds. Whiskers: 95% bootstrap interval.",
             fontsize=11.5, color=INK2, ha="left", va="top")
    fig.text(0.07, 0.075,
             "Source: results/E5_conditions.md at tag results-freeze, "
             "github.com/AlfredoFFD/graftpp-collusion-monitoring",
             fontsize=9, color=MUTED, ha="left", va="bottom")
    fig.text(0.07, 0.04,
             "Apart AI Collusion Research Sprint, October 2026.",
             fontsize=9, color=MUTED, ha="left", va="bottom")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, facecolor=SURFACE)
    print(f"wrote {OUT.relative_to(ROOT)}")
    for key in rows:
        print(key, {c: rows[key][c] for c in COLS})


if __name__ == "__main__":
    main()
