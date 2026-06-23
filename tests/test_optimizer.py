"""
Unit tests for frontier.core.optimizer — pytest-compatible.
Run with: pytest tests/test_optimizer.py -v
"""
import pytest
from frontier.core.optimizer import optimize_portfolio

# ---------------------------------------------------------------------------
# Correctness tests  (fake_returns fixture is defined in conftest.py)
# ---------------------------------------------------------------------------

def test_output_has_required_keys(fake_returns):
    """Result must contain 'optimal_portfolio' and 'frontier_curve'."""
    result = optimize_portfolio(fake_returns, risk_free_rate=0.04)
    assert "optimal_portfolio" in result
    assert "frontier_curve" in result


def test_optimal_portfolio_keys(fake_returns):
    """optimal_portfolio must expose all four metric keys."""
    optimal = optimize_portfolio(fake_returns)["optimal_portfolio"]
    assert "sharpe_ratio" in optimal
    assert "expected_annual_return" in optimal
    assert "annual_volatility" in optimal
    assert "weights" in optimal


def test_weights_sum_to_one(fake_returns):
    """Portfolio weights must sum to exactly 1.0 (no-leverage, no-short constraint)."""
    weights = optimize_portfolio(fake_returns)["optimal_portfolio"]["weights"]
    total = sum(weights.values())
    assert round(total, 2) == 1.0, f"Weights sum to {total}, expected 1.0"


def test_weights_are_non_negative(fake_returns):
    """All weights must be >= 0 (long-only constraint)."""
    weights = optimize_portfolio(fake_returns)["optimal_portfolio"]["weights"]
    for ticker, w in weights.items():
        assert w >= 0.0, f"Negative weight found for {ticker}: {w}"


def test_weights_cover_all_assets(fake_returns):
    """Weights dict must contain an entry for every input asset."""
    weights = optimize_portfolio(fake_returns)["optimal_portfolio"]["weights"]
    assert set(weights.keys()) == set(fake_returns.keys())


def test_frontier_curve_is_non_empty(fake_returns):
    """At least one Efficient Frontier point must be returned."""
    frontier = optimize_portfolio(fake_returns)["frontier_curve"]
    assert len(frontier) > 0


def test_frontier_points_have_correct_keys(fake_returns):
    """Each frontier point must have 'volatility' and 'return_rate'."""
    frontier = optimize_portfolio(fake_returns)["frontier_curve"]
    for point in frontier:
        assert "volatility" in point
        assert "return_rate" in point


def test_frontier_volatilities_are_positive(fake_returns):
    """Volatility (standard deviation) must always be a positive number."""
    frontier = optimize_portfolio(fake_returns)["frontier_curve"]
    for point in frontier:
        assert point["volatility"] > 0


def test_sharpe_ratio_is_finite(fake_returns):
    """Sharpe ratio must be a real, finite number."""
    import math
    sharpe = optimize_portfolio(fake_returns)["optimal_portfolio"]["sharpe_ratio"]
    assert math.isfinite(sharpe)


# ---------------------------------------------------------------------------
# Input guard tests
# ---------------------------------------------------------------------------

def test_raises_on_single_asset():
    """Optimizer must reject a single-asset input with a clear ValueError."""
    with pytest.raises(ValueError, match="At least 2 assets"):
        optimize_portfolio({"AAPL": [0.01, 0.02, 0.03]})


def test_raises_on_mismatched_lengths():
    """Optimizer must reject series with different observation counts."""
    with pytest.raises(ValueError, match="same length"):
        optimize_portfolio({
            "AAPL": [0.01, 0.02, 0.03],
            "MSFT": [0.01, 0.02],
        })


def test_raises_on_insufficient_observations():
    """Optimizer must reject series with fewer than 2 data points."""
    with pytest.raises(ValueError, match="at least 2 return observations"):
        optimize_portfolio({
            "AAPL": [0.01],
            "MSFT": [0.02],
        })


def test_raises_on_empty_dict():
    """An empty returns dict must also raise ValueError (< 2 assets)."""
    with pytest.raises(ValueError, match="At least 2 assets"):
        optimize_portfolio({})