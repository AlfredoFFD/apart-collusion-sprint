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
