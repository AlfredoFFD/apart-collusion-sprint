"""CAIAC: save a market after round k and fork it into several arms (PRD section 3, step 2).

A prefix run is played for exactly k rounds with ``--save_state_round k``; it writes ``state_round_k.json`` into its
results folder. Each arm then starts with ``--resume_from <that folder>``: the prefix's logs are carried into the new
run folder, the market and every agent's private state (memory, scratchpad, ZIP margins) are restored, and play
continues from round k+1 under the arm's own flags. So every arm shares the identical cartel history.
"""

import json
import random
import shutil
from pathlib import Path
from typing import Any

import numpy as np

from src.continuous_double_auction.cda_types import MarketRound, Trade

STATE_FILE = "state_round_{k}.json"


def _rng_state(rng) -> Any:
    if rng is None:
        return None
    v, internal, gauss = rng.getstate()
    return [v, list(internal), gauss]


def _set_rng_state(rng, state) -> None:
    if rng is not None and state is not None:
        rng.setstate((state[0], tuple(state[1]), state[2]))


def save_state(market, path: Path) -> None:
    agents = {}
    for a in list(market.sellers) + list(market.buyers):
        d: dict[str, Any] = {}
        mm = getattr(a, "memory_manager", None)
        if mm is not None:
            d["memories"] = {str(h): m for h, m in mm.memories.items()}
        if hasattr(a, "scratch_pad"):
            d["scratch_pad"] = a.scratch_pad
        for f in ("profit_margin", "last_adjustment"):  # ZIP buyers
            if hasattr(a, f):
                d[f] = getattr(a, f)
        agents[a.id] = d
    np_state = np.random.get_state()
    state = {
        "rounds_completed": len(market.rounds),
        "rounds": [r.model_dump() for r in market.rounds],
        "seller_ask_queue": market.seller_ask_queue,
        "buyer_bid_queue": market.buyer_bid_queue,
        "past_trades": [t.model_dump() for t in market.past_trades],
        "is_gag_order_active": market.is_gag_order_active,
        "fines": market.fines,
        "agents": agents,
        "random_state": _rng_state(random),
        "numpy_state": [np_state[0], np_state[1].tolist(), int(np_state[2]), int(np_state[3]), float(np_state[4])],
        "overseer_rng": _rng_state(market.overseer_rng),
        "monitor_rng": _rng_state(market.monitor_rng),
    }
    path.write_text(json.dumps(state), encoding="utf-8")


def load_state(market, path: Path) -> int:
    """Restore the market and agents; return the number of rounds already played."""
    state = json.loads(path.read_text(encoding="utf-8"))
    market.rounds = [MarketRound(**r) for r in state["rounds"]]
    market.seller_ask_queue = [tuple(x) for x in state["seller_ask_queue"]]
    market.buyer_bid_queue = [tuple(x) for x in state["buyer_bid_queue"]]
    market.past_trades = [Trade(**t) for t in state["past_trades"]]
    market.is_gag_order_active = state["is_gag_order_active"]
    market.fines = dict(state.get("fines", {}))
    market.current_round = MarketRound(round_number=state["rounds_completed"] + 1)
    by_id = {a.id: a for a in list(market.sellers) + list(market.buyers)}
    for aid, d in state["agents"].items():
        a = by_id.get(aid)
        if a is None:
            raise ValueError(f"resumed state has agent {aid!r}, which this run does not have (same seed and roster?)")
        if "memories" in d and getattr(a, "memory_manager", None) is not None:
            a.memory_manager.memories = {int(h): m for h, m in d["memories"].items()}
        if "scratch_pad" in d:
            a.scratch_pad = d["scratch_pad"]
        for f in ("profit_margin", "last_adjustment"):
            if f in d:
                setattr(a, f, d[f])
    _set_rng_state(random, state["random_state"])
    ns = state["numpy_state"]
    np.random.set_state((ns[0], np.array(ns[1], dtype=np.uint32), ns[2], ns[3], ns[4]))
    _set_rng_state(market.overseer_rng, state.get("overseer_rng"))
    _set_rng_state(market.monitor_rng, state.get("monitor_rng"))
    return state["rounds_completed"]


def carry_prefix_logs(prefix_dir: Path, logger) -> None:
    """Copy the prefix run's agent logs into the new run folder and replay its round-result lines into unified.log,
    so the evaluator sees rounds 1..k and k+1..N as one run."""
    for md in prefix_dir.glob("*.md"):
        shutil.copyfile(md, logger.log_dir / md.name)
    src = prefix_dir / "unified.log"
    if src.exists():
        for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
            if "Auction round " in line and " completed with result: " in line:
                logger.logger.info(line.split(" - ", 2)[-1] if " - " in line else line)
    mon = prefix_dir / "monitor_log.jsonl"
    if mon.exists():
        shutil.copyfile(mon, logger.log_dir / "monitor_log.jsonl")
