"""Tests for our fixes to the upstream harness. Each fix is marked "CAIAC fix" in the code.

Run from src/double_auction:  uv run --with pytest pytest -q tests/test_caiac_fixes.py
No network calls and no real keys: the provider tests use fake keys and stub the catalog lookups.
"""

import pytest

from src.continuous_double_auction.evaluation.evaluate import compute_collusion_metrics
from src.continuous_double_auction.evaluation.metrics import gini
from src.resources import model_wrappers as mw


def test_gini_divides_by_the_total():
    assert gini([10, 20, 30]) == pytest.approx(2 / 9)  # upstream returned 800
    assert gini([5, 5, 5]) == pytest.approx(0.0)
    assert gini([0, 0, 1]) == pytest.approx(2 / 3)
    assert gini([]) is None
    assert gini([0, 0]) == 0.0


def _metadata(buyer_values, seller_costs):
    return {
        "auction_config": {"buyer_valuations": buyer_values, "seller_valuations": seller_costs},
        "buyer_ids": [f"Buyer {i}" for i in range(len(buyer_values))],
        "seller_ids": [f"Seller {i}" for i in range(len(seller_costs))],
    }


def test_round_with_no_bids_does_not_crash(tmp_path):
    meta = _metadata([100.0, 100.0, 100.0], [80.0, 80.0, 80.0])
    rounds = [
        {"buyer_bids": {"Buyer 0": 90.0, "Buyer 1": 88.0}, "seller_asks": {"Seller 0": 95.0}, "trades": []},
        {"buyer_bids": {}, "seller_asks": {"Seller 0": 96.0}, "trades": []},  # every buyer withdrew
    ]
    out = compute_collusion_metrics(meta, rounds, log_file=None, exp_dir=tmp_path, run_llm_judge=False)
    assert out, "metrics should be computed"
    assert out["collusion_auc"] == out["collusion_auc"]  # not NaN: the empty round is skipped


def test_equal_benchmark_prices_do_not_crash(tmp_path):
    meta = _metadata([100.0, 100.0], [80.0, 100.0])  # competitive and cartel prices coincide
    rounds = [{"buyer_bids": {"Buyer 0": 99.0}, "seller_asks": {"Seller 0": 99.5}, "trades": []}]
    out = compute_collusion_metrics(meta, rounds, log_file=None, exp_dir=tmp_path, run_llm_judge=False)
    assert out, "metrics should be computed (upstream raised UnboundLocalError)"


@pytest.fixture
def both_keys(monkeypatch):
    for var in ("LLM_BASE_URL", "LLM_MODEL", "LLM_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("NEBIUS_API_KEY", "test-nebius-key")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
    monkeypatch.setattr(mw._llm_config, "openrouter_serves", lambda model: model)
    return monkeypatch


def test_model_nebius_lacks_goes_to_openrouter(both_keys):
    both_keys.setattr(mw._llm_config, "nebius_serves", lambda model: model == "qwen/qwen3-14b")
    client, model = mw._client_for("openai/gpt-4.1-mini")
    assert "openrouter.ai" in str(client.base_url) and model == "openai/gpt-4.1-mini"
    client, model = mw._client_for("qwen/qwen3-14b")
    assert "nebius" in str(client.base_url) and model == "qwen/qwen3-14b"


def test_closed_model_goes_to_openrouter_when_catalog_unreadable(both_keys):
    both_keys.setattr(mw._llm_config, "nebius_serves", lambda model: None)
    client, _ = mw._client_for("openai/gpt-4.1-mini")
    assert "openrouter.ai" in str(client.base_url)
    client, _ = mw._client_for("qwen/qwen3-14b")
    assert "nebius" in str(client.base_url)


def test_single_key_behaviour_unchanged(both_keys):
    both_keys.setenv("OPENROUTER_API_KEY", "")
    both_keys.setattr(mw._llm_config, "nebius_serves", lambda model: False)
    client, _ = mw._client_for("openai/gpt-4.1-mini")
    assert "nebius" in str(client.base_url)  # upstream behaviour with only a Nebius key


def test_keys_only_in_compute_env_still_route(monkeypatch):
    """Keys that exist only in compute.env must count before the routing check (first client of a run)."""
    for var in ("LLM_BASE_URL", "LLM_MODEL", "LLM_API_KEY", "NEBIUS_API_KEY", "OPENROUTER_API_KEY"):
        monkeypatch.delenv(var, raising=False)

    def fake_load():  # stands in for reading compute.env
        monkeypatch.setenv("NEBIUS_API_KEY", "test-nebius-key")
        monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
        return "compute.env"

    monkeypatch.setattr(mw._llm_config, "_load", fake_load)
    monkeypatch.setattr(mw._llm_config, "nebius_serves", lambda model: False)
    monkeypatch.setattr(mw._llm_config, "openrouter_serves", lambda model: model)
    client, _ = mw._client_for("openai/gpt-4.1-mini")
    assert "openrouter.ai" in str(client.base_url)


def test_plot_aggregate_with_no_runs_returns_nothing():
    from src.continuous_double_auction.util.plotting_util import aggregate_metric_data
    assert aggregate_metric_data([], "empty", lambda d: None, "value") == (None, 0, 0)


def test_custom_endpoint_routes_only_that_model(monkeypatch):
    monkeypatch.setenv("CAIAC_MODEL_ENDPOINTS", '{"caiac/graft": "https://example.modal.run/v1"}')
    monkeypatch.setenv("NEBIUS_API_KEY", "test-nebius-key")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    client, model = mw._client_for("caiac/graft")
    assert "example.modal.run" in str(client.base_url) and model == "caiac/graft"
    client, _ = mw._client_for("qwen/qwen3-14b")
    assert "example.modal.run" not in str(client.base_url)


def test_to_price_accepts_text_numbers():
    """CAIAC: small fine-tuned sellers send asks as text; the market keeps the number and drops the rest."""
    from src.continuous_double_auction.market.market import Market
    assert Market._to_price("98.00") == 98.0 and Market._to_price("$98") == 98.0 and Market._to_price(97) == 97.0
    assert Market._to_price(" 1,000.5 ") == 1000.5
    assert Market._to_price("null") is None and Market._to_price(True) is None and Market._to_price("high") is None


def test_market_side_reset_keeps_memory_and_wipes_the_book(tmp_path):
    """--reset_market_state: agents keep memory and scratchpad; queues, trades and the past-hours table are wiped;
    round numbering and the last hour's messages stay (plan v2, Phase 2)."""
    import json
    from types import SimpleNamespace
    from src.continuous_double_auction.market import branching
    state = {"rounds_completed": 2,
             "rounds": [{"round_number": 1, "seller_asks": {"S": 98.0}, "buyer_bids": {"B": 90.0}, "trades": [], "seller_messages": {"S": "hi"}, "buyer_messages": {}},
                        {"round_number": 2, "seller_asks": {"S": 99.0}, "buyer_bids": {"B": 91.0}, "trades": [], "seller_messages": {"S": "hold"}, "buyer_messages": {}}],
             "seller_ask_queue": [["S", 99.0]], "buyer_bid_queue": [["B", 91.0]],
             "past_trades": [{"round_number": 2, "buyer_id": "B", "seller_id": "S", "price": 95.0}],
             "is_gag_order_active": False, "fines": {"S": 20.0},
             "agents": {"S": {"memories": {"1": "m1"}, "scratch_pad": "notes"}, "B": {"memories": {"1": "b1"}}},
             "random_state": None, "numpy_state": list(map(lambda x: x, [0, [0] * 624, 624, 0, 0.0])), "overseer_rng": None, "monitor_rng": None}
    state["numpy_state"][0] = "MT19937"
    p = tmp_path / "state_round_2.json"; p.write_text(json.dumps(state), encoding="utf-8")
    S = SimpleNamespace(id="S", memory_manager=SimpleNamespace(memories={}), scratch_pad="")
    Bn = SimpleNamespace(id="B", memory_manager=SimpleNamespace(memories={}))
    market = SimpleNamespace(sellers=[S], buyers=[Bn], rounds=[], seller_ask_queue=[], buyer_bid_queue=[], past_trades=[],
                             is_gag_order_active=False, fines={}, current_round=None, overseer_rng=None, monitor_rng=None)
    assert branching.load_state(market, p, reset_market=True) == 2
    assert S.memory_manager.memories == {1: "m1"} and S.scratch_pad == "notes"      # memory kept
    assert market.seller_ask_queue == [] and market.buyer_bid_queue == [] and market.past_trades == []  # book wiped
    assert [r.round_number for r in market.rounds] == [1, 2] and market.current_round.round_number == 3  # numbering kept
    assert all(r.seller_asks == {} and r.buyer_bids == {} for r in market.rounds)      # past-hours table blank
    assert market.rounds[-1].seller_messages == {"S": "hold"} and market.rounds[0].seller_messages == {}
    assert market.fines == {"S": 20.0}
    # the default path still restores everything
    market2 = SimpleNamespace(sellers=[S], buyers=[Bn], rounds=[], seller_ask_queue=[], buyer_bid_queue=[], past_trades=[],
                              is_gag_order_active=False, fines={}, current_round=None, overseer_rng=None, monitor_rng=None)
    branching.load_state(market2, p)
    assert market2.seller_ask_queue == [("S", 99.0)] and len(market2.past_trades) == 1 and market2.rounds[1].seller_asks == {"S": 99.0}


def test_deactivation_rule_forfeits_strikes_and_removes(tmp_path):
    """T5: below the threshold a seller forfeits the hour's profit and takes a strike; at the strike limit it is
    decommissioned (ask withdrawn, no longer consulted); above the threshold nothing happens; words-only never enforces."""
    import json
    from src.continuous_double_auction.cda_types import Agent, ExperimentParams, MarketRound, Trade
    from src.continuous_double_auction.market.market import Market
    params = ExperimentParams(seller_valuations=[80.0, 80.0], buyer_valuations=[100.0], seller_models=["m", "m"],
                              buyer_models=[None], rounds=5, deactivation_threshold=95.0, deactivation_strikes=2, deactivation_enforce=True)
    low = Agent(id="Seller Low", company="L", valuation=80.0, expt_params=params)
    high = Agent(id="Seller High", company="H", valuation=80.0, expt_params=params)
    buyer = Agent(id="Buyer B", company="B", valuation=100.0, expt_params=params)
    log = tmp_path / "deactivation_log.jsonl"
    m = Market(sellers=[low, high], buyers=[buyer], deactivation_threshold=95.0, deactivation_strikes=2, deactivation_enforce=True,
               deactivation_log_path=str(log))
    # round 1: Low sold at 90 (below 95), High sold at 97
    m.current_round = MarketRound(round_number=1, seller_asks={"Seller Low": 90.0, "Seller High": 97.0})
    m.current_round.trades = [Trade(round_number=1, buyer_id="Buyer B", seller_id="Seller Low", price=90.0),
                              Trade(round_number=1, buyer_id="Buyer B", seller_id="Seller High", price=97.0)]
    m.past_trades = list(m.current_round.trades)
    m.apply_deactivation_rule()
    assert m.strikes == {"Seller Low": 1} and m.fines["Seller Low"] == 10.0 and m.forfeit_last_round == {"Seller Low": 10.0}
    assert m.deactivated == [] and "Seller High" not in m.fines
    # round 2: Low made no sale; its current ask (92) stands in -> second strike -> decommissioned, ask withdrawn
    m.current_round = MarketRound(round_number=2, seller_asks={"Seller Low": 92.0, "Seller High": 97.0})
    m.seller_ask_queue = [(97.0, "Seller High"), (92.0, "Seller Low")]
    m.apply_deactivation_rule()
    assert m.strikes["Seller Low"] == 2 and m.deactivated == ["Seller Low"]
    assert m.seller_ask_queue == [(97.0, "Seller High")] and "Seller Low" not in m.current_round.seller_asks
    entries = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines()]
    assert sum(e["strike"] for e in entries) == 2 and sum(e["deactivated"] for e in entries) == 1
    # words-only twin: same threshold, enforce False -> run_round never calls the rule; the rule itself is inert when unenforced
    m2 = Market(sellers=[low, high], buyers=[buyer], deactivation_threshold=95.0, deactivation_enforce=False)
    assert m2.deactivation_threshold > 0 and not m2.deactivation_enforce and m2.strikes == {}
