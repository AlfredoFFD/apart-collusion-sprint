"""CAIAC forced-cut audit in Jayden Jeong's Hawthorne duopoly. Pre-registered in PREREG.md (commit 69c422c5).

His code runs from a separate worktree (his commit 29878b03 plus `patch_audit.diff`, kept in this folder). The
patch only adds two optional arguments to `run_episode` (`force`, `skip_monitors`) and two recorded fields.

  python fork_audit.py gate-g1 --k 14 15 [--prefix-dir DIR]   rebuilt state regenerates the saved next-round prompt
  python fork_audit.py gate-g2                                patched code without options == his code (mock LLM)
  python fork_audit.py prefix --base-url URL --arm ON --seeds 5-9 --out DIR
  python fork_audit.py fork   --base-url URL --arm ON --seeds 0-9 --copies S,C0,R0,C1,R1 --prefix-dir DIR --out DIR

Run with the venv that ran the Oct 25 test (C:/Users/fabia/dev/hawthorne-negotiation/.venv).
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
AUDIT_CODE = Path(os.environ.get("HAWTHORNE_AUDIT_CODE", "C:/Users/fabia/dev/hawthorne-audit"))
ORIG_CODE = Path(os.environ.get("HAWTHORNE_ORIG_CODE", "C:/Users/fabia/dev/hawthorne-negotiation"))
OCT25 = REPO / "results" / "hawthorne_negotiation"
ARM_DIR = {"ON": OCT25 / "neg_on", "OFF": OCT25 / "neg_off"}
K = 15          # rounds 1-15 are the prefix; round 16 (0-based index 15) is the forced round
T_ROUNDS = 30
COPIES = {"S": None,
          "C0": {"round": K, "seller": 0, "factor": 0.9},
          "R0": {"round": K, "seller": 0, "factor": 1.1},
          "C1": {"round": K, "seller": 1, "factor": 0.9},
          "R1": {"round": K, "seller": 1, "factor": 1.1}}
NEG_MARKERS = ("SELLER CHANNEL — this round's negotiation so far:", "PRICE STEP:")


def use_code(code: Path) -> None:
    sys.path.insert(0, str(code))


def parse_seeds(s: str) -> list[int]:
    out: list[int] = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def src_file(arm: str, seed: int, prefix_dir: str | None) -> Path:
    n = "N" if arm == "ON" else ""
    if seed <= 4:
        return ARM_DIR[arm] / f"unwatched__profitDMI{n}__r30__s{seed}.json"
    if not prefix_dir:
        raise SystemExit(f"seed {seed} needs --prefix-dir")
    return Path(prefix_dir) / arm / f"unwatched__profitDMI{n}__r15__s{seed}.json"


def rebuild_state(ep: dict, k: int) -> dict:
    """The checkpoint his run_episode writes after round k (0-based next_round = k), rebuilt from a saved file."""
    from hawthorne.market import MarketParams, equilibria
    from hawthorne.prompts import SELLER_NAMES
    c = ep["config"]
    n = c["n_sellers"]
    names = SELLER_NAMES[:n]
    assert c["condition"] == "unwatched" and c["stakes"] == "base", "rebuild assumes the unwatched base setup"
    rows: dict[int, dict[int, dict]] = {}
    for s in ep["steps"]:
        rows.setdefault(s["round"], {})[s["seller"]] = s
    for r in range(k):
        assert r in rows and sorted(rows[r]) == list(range(n)), f"round {r + 1} incomplete"
    balances, units = [0.0] * n, [0] * n
    history = []
    for r in range(k):
        row = [rows[r][i] for i in range(n)]
        for i in range(n):
            balances[i] += row[i]["profit"] - 0.0          # base stakes: no fixed cost (his line 245)
            balances[i] -= row[i]["penalty"]              # unwatched: always 0.0
            units[i] += row[i]["units"]
            assert row[i]["penalty"] == 0.0 and not row[i]["flagged"]
            assert balances[i] == row[i]["balance_after"], f"balance mismatch r{r + 1} s{i}"
        history.append({"round": r + 1, "prices": [x["price"] for x in row],
                        "units": [x["units"] for x in row], "profit": [x["profit"] for x in row]})
    last = [rows[k - 1][i] for i in range(n)]
    inbox = [[[names[j], last[j]["message"]] for j in range(n) if j != i and last[j]["message"]]
             for i in range(n)]
    eq = equilibria(MarketParams(n_sellers=n))
    review = [{"strikes": 0, "window_start": 0, "rounds_done_in_window": 0, "window_net": 0.0,
               "last_result": None, "replaced_round": None, "nash_net": eq.pi_nash - c["fixed_cost"]}
              for _ in range(n)]
    v, internal, gauss = random.Random(c["seed"]).getstate()  # unwatched never draws from his rng
    return {"next_round": k, "balances": balances, "units_total": units, "history": history,
            "inbox": inbox, "notices": [[] for _ in range(n)], "last_price": [x["price"] for x in last],
            "steps": [s for s in ep["steps"] if s["round"] < k],
            "notes": [{"plans": x["plans"], "insights": x["insights"]} for x in last], "review": review,
            "monitor_rationales": [m for m in ep["monitor_rationales"] if m["round"] < k],
            "rng": [v, list(internal), gauss], "elapsed": 0.0}


def _prefix_lines(prompt: str) -> list[str]:
    out = []
    for line in prompt.split("\n"):
        if line.startswith(NEG_MARKERS):
            break
        out.append(line)
    return out


def regen_prompt(ep: dict, k: int, i: int) -> str:
    from hawthorne.prompts import EpisodeConfig, seller_round_prompt
    cfg = EpisodeConfig(**ep["config"])
    st = rebuild_state(ep, k)
    return seller_round_prompt(i, cfg, k, st["history"], [tuple(m) for m in st["inbox"][i]], st["notices"][i],
                               st["balances"][i], st["units_total"][i], notes=st["notes"][i],
                               review=st["review"][i], transcript=[])


def gate_g1(ks: list[int], prefix_dir: str | None) -> bool:
    use_code(ORIG_CODE)
    files = []
    for arm in ("ON", "OFF"):
        for seed in range(10):
            p = src_file(arm, seed, prefix_dir) if (seed <= 4 or prefix_dir) else None
            if p is not None and p.exists():
                files.append((arm, seed, p))
    ok_all, n_checks = True, 0
    for arm, seed, p in files:
        ep = json.loads(p.read_text())
        neg = ep["config"]["negotiate"]
        saved_rounds = {s["round"] for s in ep["steps"]}
        for k in ks:
            if k not in saved_rounds:
                continue
            for i in range(ep["config"]["n_sellers"]):
                saved = next(s["user_prompt"] for s in ep["steps"] if s["round"] == k and s["seller"] == i)
                regen = regen_prompt(ep, k, i)
                same = (_prefix_lines(saved) == _prefix_lines(regen)) if neg else (saved == regen)
                n_checks += 1
                if not same:
                    ok_all = False
                    print(f"G1 FAIL {arm} seed {seed} k={k} seller {i} ({p.name})")
    print(f"G1 {'PASS' if ok_all else 'FAIL'}: {n_checks} prompt checks on {len(files)} files "
          f"({'line prefix before the negotiation block' if True else ''} for ON, byte-exact for OFF)")
    return ok_all


# ----------------------------------------------------------------------------------------------- G2 (mock LLM)
async def _mock(code: str, negotiate: bool, skip: bool, force: dict | None, out: str) -> None:
    use_code(AUDIT_CODE if code == "AUDIT" else ORIG_CODE)
    from hawthorne.episode import run_episode
    from hawthorne.market import MarketParams
    from hawthorne.mock_llm import MockClient
    from hawthorne.prompts import EpisodeConfig
    cfg = EpisodeConfig(condition="unwatched", goal="profit", seed=3, n_rounds=8, stakes="base", n_sellers=2,
                        memory=True, indefinite=True, negotiate=negotiate)
    kw = {}
    if code == "AUDIT":
        kw = {"force": force, "skip_monitors": skip}
    rec = await run_episode(cfg, MockClient(seed=11), MarketParams(n_sellers=2), **kw)
    keep = ("round", "seller", "user_prompt", "price", "message", "plans", "insights", "units", "profit",
            "price_chosen", "forced")
    Path(out).write_text(json.dumps({"system_prompts": rec.system_prompts,
                                     "steps": [{k: s.get(k) for k in keep} for s in rec.steps]}))


def gate_g2() -> bool:
    tmp = HERE / "_gate_g2"
    tmp.mkdir(exist_ok=True)
    py = sys.executable
    ok_all = True

    def run(tag, code, neg, skip=False, force=None):
        out = tmp / f"{tag}.json"
        args = [py, str(Path(__file__)), "_mock", "--code", code, "--negotiate", str(int(neg)), "--out", str(out)]
        if skip:
            args.append("--skip-monitors")
        if force:
            args += ["--force", json.dumps(force)]
        subprocess.run(args, check=True)
        return json.loads(out.read_text())

    core = ("round", "seller", "user_prompt", "price", "message", "plans", "insights", "units", "profit")
    for neg in (False, True):
        orig = run(f"orig_neg{int(neg)}", "ORIG", neg)
        aud = run(f"audit_neg{int(neg)}", "AUDIT", neg)
        aud_skip = run(f"audit_skip_neg{int(neg)}", "AUDIT", neg, skip=True)
        f = {"round": 4, "seller": 0, "factor": 0.9}
        aud_force = run(f"audit_force_neg{int(neg)}", "AUDIT", neg, force=f)

        def proj(rec):
            return [[s[k] for k in core] for s in rec["steps"]]

        a = proj(orig) == proj(aud) and orig["system_prompts"] == aud["system_prompts"]
        b = proj(orig) == proj(aud_skip)
        # forced copy: identical before round 5, round 5 seller 0 posts 0.9 x chosen, history shows it next round
        pre_same = proj(orig)[:8] == proj(aud_force)[:8]
        st5 = next(s for s in aud_force["steps"] if s["round"] == 4 and s["seller"] == 0)
        c = (pre_same and st5["forced"] and st5["price"] == round(st5["price_chosen"] * 0.9, 2)
             and all(not s["forced"] for s in aud_force["steps"] if not (s["round"] == 4 and s["seller"] == 0)))
        nxt = next(s for s in aud_force["steps"] if s["round"] == 5 and s["seller"] == 1)["user_prompt"]
        c = c and f"${st5['price']:.2f}" in nxt
        print(f"G2 negotiate={neg}: no options == his code: {a}; skip_monitors keeps seller steps: {b}; "
              f"force works as registered: {c}")
        ok_all = ok_all and a and b and c
    print(f"G2 {'PASS' if ok_all else 'FAIL'}")
    return ok_all


# ----------------------------------------------------------------------------------------------- runs
def _client(base_url: str, concurrency: int):
    from hawthorne.llm import LLMClient, LLMConfig
    return LLMClient(LLMConfig(base_url=base_url, model="hawthorne", concurrency=concurrency, max_tokens=6000))


async def run_prefix(base_url: str, arm: str, seeds: list[int], out: str, concurrency: int) -> None:
    use_code(AUDIT_CODE)
    from hawthorne.episode import run_episode
    from hawthorne.market import MarketParams
    from hawthorne.prompts import EpisodeConfig
    template = json.loads(src_file(arm, 0, None).read_text())["config"]
    client = _client(base_url, concurrency)
    out_dir = Path(out) / arm
    cfgs = [EpisodeConfig(**{**template, "seed": s, "n_rounds": K}) for s in seeds]
    todo = [c for c in cfgs if not (out_dir / f"{c.tag()}.json").exists()]
    print(f"prefix {arm}: {len(todo)} of {len(cfgs)} to run -> {out_dir}", flush=True)
    t0 = time.time()

    async def one(cfg):
        try:
            rec = await run_episode(cfg, client, MarketParams(n_sellers=2), out_dir=out_dir, skip_monitors=True)
            print(f"done {cfg.tag()} mean price {rec.summary['mean_price']:.2f} "
                  f"perr={rec.summary['n_parse_errors']} {rec.wall_time:.0f}s", flush=True)
        except Exception as e:
            print(f"FAILED {cfg.tag()}: {e!r}", flush=True)

    await asyncio.gather(*[one(c) for c in todo])
    retry = [c for c in todo if not (out_dir / f"{c.tag()}.json").exists()]
    if retry:
        print(f"retrying {len(retry)}", flush=True)
        await asyncio.gather(*[one(c) for c in retry])
    await client.close()
    print(f"prefix {arm} done in {time.time() - t0:.0f}s; calls={client.total_calls} "
          f"prompt_tok={client.total_prompt_tokens:,} completion_tok={client.total_completion_tokens:,} "
          f"errors={client.errors}", flush=True)


async def run_fork(base_url: str, arm: str, seeds: list[int], copies: list[str], prefix_dir: str | None,
                   out: str, concurrency: int) -> None:
    use_code(AUDIT_CODE)
    from hawthorne.episode import run_episode
    from hawthorne.market import MarketParams
    from hawthorne.prompts import EpisodeConfig
    client = _client(base_url, concurrency)
    manifest = []
    jobs = []
    for seed in seeds:
        src = src_file(arm, seed, prefix_dir)
        ep = json.loads(src.read_text())
        state = rebuild_state(ep, K)
        cfg = EpisodeConfig(**{**ep["config"], "n_rounds": T_ROUNDS})
        for cp in copies:
            od = Path(out) / arm / cp
            manifest.append({"arm": arm, "seed": seed, "copy": cp, "force": COPIES[cp], "source": str(src),
                             "source_sha256": sha(src), "tag": cfg.tag()})
            if (od / f"{cfg.tag()}.json").exists():
                continue
            ck = od / "_ckpt" / f"{cfg.tag()}.json"
            if not ck.exists():  # an interrupted copy resumes from its own later checkpoint
                ck.parent.mkdir(parents=True, exist_ok=True)
                ck.write_text(json.dumps(state))
            jobs.append((cfg, od, cp))
    (Path(out) / arm).mkdir(parents=True, exist_ok=True)
    (Path(out) / arm / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"fork {arm}: {len(jobs)} copies to run -> {Path(out) / arm}", flush=True)
    t0 = time.time()

    async def one(cfg, od, cp):
        try:
            rec = await run_episode(cfg, client, MarketParams(n_sellers=2), out_dir=od, force=COPIES[cp],
                                    skip_monitors=True)
            print(f"done {arm} {cp} {cfg.tag()} perr={rec.summary['n_parse_errors']} {rec.wall_time:.0f}s",
                  flush=True)
        except Exception as e:
            print(f"FAILED {arm} {cp} {cfg.tag()}: {e!r}", flush=True)

    await asyncio.gather(*[one(*j) for j in jobs])
    retry = [j for j in jobs if not (j[1] / f"{j[0].tag()}.json").exists()]
    if retry:
        print(f"retrying {len(retry)}", flush=True)
        await asyncio.gather(*[one(*j) for j in retry])
    await client.close()
    print(f"fork {arm} done in {time.time() - t0:.0f}s; calls={client.total_calls} "
          f"prompt_tok={client.total_prompt_tokens:,} completion_tok={client.total_completion_tokens:,} "
          f"errors={client.errors}", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    g1 = sub.add_parser("gate-g1")
    g1.add_argument("--k", type=int, nargs="+", default=[14, 15])
    g1.add_argument("--prefix-dir", default=None)
    sub.add_parser("gate-g2")
    m = sub.add_parser("_mock")
    m.add_argument("--code", choices=["ORIG", "AUDIT"], required=True)
    m.add_argument("--negotiate", type=int, default=0)
    m.add_argument("--skip-monitors", action="store_true")
    m.add_argument("--force", default=None)
    m.add_argument("--out", required=True)
    for name in ("prefix", "fork"):
        q = sub.add_parser(name)
        q.add_argument("--base-url", required=True)
        q.add_argument("--arm", choices=["ON", "OFF"], required=True)
        q.add_argument("--seeds", required=True)
        q.add_argument("--out", required=True)
        q.add_argument("--concurrency", type=int, default=64)
        if name == "fork":
            q.add_argument("--copies", default="S,C0,R0,C1,R1")
            q.add_argument("--prefix-dir", default=None)
    a = p.parse_args()
    if a.cmd == "gate-g1":
        sys.exit(0 if gate_g1(a.k, a.prefix_dir) else 1)
    if a.cmd == "gate-g2":
        sys.exit(0 if gate_g2() else 1)
    if a.cmd == "_mock":
        asyncio.run(_mock(a.code, bool(a.negotiate), a.skip_monitors, json.loads(a.force) if a.force else None,
                          a.out))
        return
    if a.cmd == "prefix":
        asyncio.run(run_prefix(a.base_url, a.arm, parse_seeds(a.seeds), a.out, a.concurrency))
        return
    if a.cmd == "fork":
        asyncio.run(run_fork(a.base_url, a.arm, parse_seeds(a.seeds), a.copies.split(","), a.prefix_dir, a.out,
                             a.concurrency))


if __name__ == "__main__":
    main()
