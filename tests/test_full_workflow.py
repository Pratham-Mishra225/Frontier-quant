"""
End-to-end integration tests: adapter → optimizer pipeline — pytest-compatible.

All tests here make live network calls to Yahoo Finance.
Skip in CI with: pytest -m "not network"
Run with: pytest tests/test_full_workflow.py -v
"""
import pytest
from frontier.adapters.yfinance_client import fetch_historical_returns
from frontier.core.optimizer import optimize_portfolio

TICKERS = ["AAPL", "MSFT", "GOOG"]
LOOKBACK = 1  # 1 year — fast enough for CI, representative enough to validate


@pytest.fixture(scope="module")
def pipeline_result():
    """
    Shared module-scoped fixture: runs the full adapter → optimizer pipeline once
    and reuses the result across all tests in this module.
    """
    returns_dict = fetch_historical_returns(TICKERS, lookback_years=LOOKBACK)
    result = optimize_portfolio(returns_dict, risk_free_rate=0.04)
    return result


# ---------------------------------------------------------------------------
# Pipeline integration tests
# ---------------------------------------------------------------------------

@pytest.mark.network
def test_pipeline_returns_result_dict(pipeline_result):
    """Full pipeline must return a dict."""
    assert isinstance(pipeline_result, dict)


@pytest.mark.network
def test_pipeline_optimal_portfolio_key(pipeline_result):
    """Result must contain 'optimal_portfolio'."""
    assert "optimal_portfolio" in pipeline_result


@pytest.mark.network
def test_pipeline_frontier_curve_key(pipeline_result):
    """Result must contain 'frontier_curve'."""
    assert "frontier_curve" in pipeline_result


@pytest.mark.network
def test_pipeline_weights_sum_to_one(pipeline_result):
    """End-to-end weights must still sum to 1.0."""
    weights = pipeline_result["optimal_portfolio"]["weights"]
    assert round(sum(weights.values()), 2) == 1.0


@pytest.mark.network
def test_pipeline_weights_are_non_negative(pipeline_result):
    """All weights from live data must be >= 0 (long-only)."""
    weights = pipeline_result["optimal_portfolio"]["weights"]
    for ticker, w in weights.items():
        assert w >= 0.0, f"Negative weight for {ticker}: {w}"


@pytest.mark.network
def test_pipeline_covers_all_tickers(pipeline_result):
    """Weights must be returned for every input ticker."""
    weights = pipeline_result["optimal_portfolio"]["weights"]
    assert set(weights.keys()) == set(TICKERS)


@pytest.mark.network
def test_pipeline_frontier_is_non_empty(pipeline_result):
    """Live pipeline must produce at least one frontier point."""
    assert len(pipeline_result["frontier_curve"]) > 0


@pytest.mark.network
def test_pipeline_frontier_point_structure(pipeline_result):
    """Every frontier point must have 'volatility' and 'return_rate'."""
    for point in pipeline_result["frontier_curve"]:
        assert "volatility" in point
        assert "return_rate" in point


@pytest.mark.network
def test_pipeline_sharpe_is_positive(pipeline_result):
    """Max-Sharpe portfolio should yield a positive Sharpe ratio for typical blue-chips."""
    sharpe = pipeline_result["optimal_portfolio"]["sharpe_ratio"]
    assert sharpe > 0, f"Expected positive Sharpe ratio, got {sharpe}"