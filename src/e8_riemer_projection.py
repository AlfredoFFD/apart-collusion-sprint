"""EXPLORATORY. Project our E8 seller-turn activations onto the collusion steering vectors that ship with the
llm-cartel starter folder (Riemer et al. 2026, arXiv:2608.18078; `results/steering_vectors/Qwen3-14B/custom/
vectors.json`, one vector per layer, built by contrastive activation addition on Qwen3-14B with counterfactual
future-profit labels in a Bertrand duopoly). Same base model as our sellers, a different game and prompt, so the
vector cannot have learned our consortium block. Question: does a borrowed, behaviour-labelled direction separate our
cartel turns from compete turns, and in particular the silent cartel (chat off, nothing in the text) from compete?

Our vectors: `results/<run>/e8_vectors.npz` (`vec`: [turns, 3 depths, 5120], mean of the residual stream over the
reply tokens at hidden_states[10|20|30] of 40 layers; `e8_index.json` lists seller and round per turn). Riemer's
vectors are the output of `model.model.layers[i]`, i.e. hidden_states[i+1], so depth 10/20/30 maps to keys 9/19/29;
keys 10/20/30 are reported as a robustness check. Score = cosine similarity. No model call, no API call.

Run from the repo root:  uv run --project src/double_auction python src/e8_riemer_projection.py
Writes results/e8_riemer/{scores.csv, summary.md}. Nothing here enters the report as a claim.
"""
from __future__ import annotations
import csv, glob, json, os, re
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RIEMER = ROOT / "vendor/collusion_hackathon/llm-cartel/results/steering_vectors/Qwen3-14B/custom/vectors.json"
OUT = ROOT / "results/e8_riemer"
DEPTH_HS = [10, 20, 30]                      # hidden_states indices used by e8_directions_modal.py (40 layers)
KEYSETS = {"exact(i-1)": [9, 19, 29], "offset(i)": [10, 20, 30]}
BRANCH = 8                                   # E2 forks continue from the saved round-8 state

# arm label from the run folder name; (label, template_era, post_branch_only)
ARMS = [
    ("E1_instructed",        "cartel_instructed_E1 (old template)", "old", False),
    ("E1_pressure",          "pressure_E1 (old template)",          "old", False),
    ("E1_nochat",            "nochat_E1 (old template)",            "old", False),
    ("E1_compete",           "compete",                              "new", False),
    ("E1_pricesonly",        "pricesonly",                           "new", False),
    ("E1_silentcartel",      "cartel_silent (chat off)",             "new", False),
    ("E1_monopoly",          "monopoly (one seller)",                "new", False),
    ("E1_isolated",          "isolated (rivals hidden)",             "new", False),
    ("E2p_A0norem_none",     "cartel_A0_noreminder (block removed)", "new", True),
    ("E2p_A0noremresetb",    "cartel_noreminder_freshbuyers",        "new", True),
    ("E2p_A0noremresets",    "cartel_noreminder_freshsellers",       "new", True),
    ("E2p_A0_none",          "cartel_A0 (post-branch)",              "new", True),
    ("E2p_A1silent",         "cartel_A1silent",                      "new", True),
    ("E2p_A1_rot_nofine",    "cartel_A1_notice",                     "new", True),
    ("E2p_A2dodge",          "cartel_A2dodge",                       "new", True),
    ("E2p_A2full",           "cartel_A2full",                        "new", True),
    ("E2p_A2two",            "cartel_A2two",                         "new", True),
    ("E2p_A2norem",          "cartel_A2_noreminder",                 "new", True),
    ("E2p_A2_rot_fine20",    "cartel_A2_fine",                       "new", True),
    ("E2p_A3_rand_fine20",   "cartel_A3_random",                     "new", True),
    ("E2_prefix8",           "cartel_prefix (rounds 1-8)",           "new", False),
]


def arm_of(name: str):
    tag = name[16:]
    for key, label, era, post in ARMS:
        if tag.startswith(key):
            return label, era, post
    return None


def auc(pos: np.ndarray, neg: np.ndarray) -> float:
    """Rank AUC (probability a random positive scores above a random negative), ties count half."""
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    allv = np.concatenate([pos, neg])
    order = allv.argsort(kind="mergesort")
    ranks = np.empty(len(allv))
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[order[j + 1]] == allv[order[i]]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    return float((ranks[: len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def main():
    rj = json.load(open(RIEMER, encoding="utf-8"))
    vecs = {int(k): np.asarray(v, dtype=np.float32) for k, v in rj["vectors"].items()}
    for k in vecs:
        vecs[k] = vecs[k] / (np.linalg.norm(vecs[k]) + 1e-8)
    print(f"Riemer vectors: {rj.get('model_name')} · {rj.get('extraction_method')} · {rj.get('context')} · "
          f"{len(vecs)} layers · normalized={rj.get('normalized')}")

    rows = []
    for npz in sorted(glob.glob(str(ROOT / "results/*/e8_vectors.npz"))):
        run = Path(npz).parent
        arm = arm_of(run.name)
        if arm is None:
            continue
        label, era, post = arm
        seed_m = re.search(r"_s(\d+)$", run.name)
        seed = int(seed_m.group(1)) if seed_m else -1
        vec = np.load(npz)["vec"].astype(np.float32)          # [turns, 3, 5120]
        index = json.load(open(run / "e8_index.json", encoding="utf-8"))
        for t, meta in enumerate(index):
            if post and meta["round"] <= BRANCH:
                continue
            row = {"run": run.name, "arm": label, "era": era, "seed": seed, "seller": meta["seller"],
                   "round": meta["round"]}
            for d, hs in enumerate(DEPTH_HS):
                x = vec[t, d]
                xn = x / (np.linalg.norm(x) + 1e-8)
                for ks, keys in KEYSETS.items():
                    row[f"cos_{ks}_hs{hs}"] = float(xn @ vecs[keys[d]])
            rows.append(row)

    OUT.mkdir(parents=True, exist_ok=True)
    cols = list(rows[0].keys())
    with open(OUT / "scores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    score_cols = [c for c in cols if c.startswith("cos_")]
    arms = sorted({r["arm"] for r in rows}, key=lambda a: -np.mean([r[score_cols[1]] for r in rows if r["arm"] == a]))
    lines = ["# EXPLORATORY: our E8 reply activations projected on Riemer's Qwen3-14B collusion vectors", "",
             "Cosine similarity, mean over turns (sd over the per-run means). Columns: mapping × depth "
             "(hidden_states index). Nothing here is a claim; the vector was fit in another game.", ""]
    lines.append("| arm | runs | turns | " + " | ".join(score_cols) + " |")
    lines.append("|---|---|---|" + "---|" * len(score_cols))
    for a in arms:
        sub = [r for r in rows if r["arm"] == a]
        runs = sorted({r["run"] for r in sub})
        cells = []
        for c in score_cols:
            per_run = [np.mean([r[c] for r in sub if r["run"] == rn]) for rn in runs]
            cells.append(f"{np.mean([r[c] for r in sub]):+.3f} ± {np.std(per_run):.3f}")
        lines.append(f"| {a} | {len(runs)} | {len(sub)} | " + " | ".join(cells) + " |")

    tests = [
        ("cartel_A0 (post-branch) vs compete", "cartel_A0 (post-branch)", "compete"),
        ("cartel_silent (chat off) vs compete", "cartel_silent (chat off)", "compete"),
        ("cartel_A0_noreminder vs compete", "cartel_A0_noreminder (block removed)", "compete"),
        ("cartel_A0 vs cartel_A0_noreminder (prompt-reading check; ~0.5 = reads behaviour)",
         "cartel_A0 (post-branch)", "cartel_A0_noreminder (block removed)"),
        ("monopoly vs compete (greed, not collusion)", "monopoly (one seller)", "compete"),
        ("cartel_A2_fine vs compete", "cartel_A2_fine", "compete"),
        ("cartel_prefix (rounds 1-8) vs compete", "cartel_prefix (rounds 1-8)", "compete"),
        ("cartel_instructed_E1 (old template) vs compete [template era differs]",
         "cartel_instructed_E1 (old template)", "compete"),
    ]
    lines += ["", "## Turn-level AUC (positive = first arm)", "",
              "| comparison | n pos / n neg | " + " | ".join(score_cols) + " |",
              "|---|---|" + "---|" * len(score_cols)]
    for title, pa, na in tests:
        p = [r for r in rows if r["arm"] == pa]
        n = [r for r in rows if r["arm"] == na]
        cells = [f"{auc(np.array([r[c] for r in p]), np.array([r[c] for r in n])):.2f}" for c in score_cols]
        lines.append(f"| {title} | {len(p)} / {len(n)} | " + " | ".join(cells) + " |")

    # per-seed AUC for the two load-bearing comparisons, exact mapping, middle depth
    c = "cos_exact(i-1)_hs20"
    lines += ["", f"## Per-seed AUC, {c}", ""]
    for title, pa, na in tests[:3]:
        parts = []
        for s in sorted({r["seed"] for r in rows if r["arm"] == pa}):
            p = np.array([r[c] for r in rows if r["arm"] == pa and r["seed"] == s])
            n = np.array([r[c] for r in rows if r["arm"] == na and r["seed"] == s])
            parts.append(f"seed {s}: {auc(p, n):.2f} ({len(p)}/{len(n)})")
        lines.append(f"- {title}: " + "; ".join(parts))

    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nwrote {OUT/'scores.csv'} ({len(rows)} turns), {OUT/'summary.md'}")


if __name__ == "__main__":
    main()
