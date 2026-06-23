"""
Unit / integration tests for frontier.adapters.yfinance_client — pytest-compatible.

Tests marked with @pytest.mark.network make live calls to Yahoo Finance.
Skip them in CI with: pytest -m "not network"
Run with: pytest tests/test_adapters.py -v
"""
import pytest
from frontier.adapters.yfinance_client import fetch_historical_returns


# ---------------------------------------------------------------------------
# Input guard tests  (no network required)
# ---------------------------------------------------------------------------

def test_raises_on_empty_ticker_list():
    """Adapter must reject an empty ticker list immediately."""
    with pytest.raises(ValueError, match="cannot be empty"):
        fetch_historical_returns([])


# ---------------------------------------------------------------------------
# Live network tests
# ---------------------------------------------------------------------------

@pytest.mark.network
def test_returns_correct_type():
    """Output must be a dict mapping ticker strings to lists of floats."""
    result = fetch_historical_returns(["AAPL", "MSFT"], lookback_years=1)
    assert isinstance(result, dict)
    for ticker, series in result.items():
        assert isinstance(ticker, str)
        assert isinstance(series, list)
        assert all(isinstance(v, float) for v in series)


@pytest.mark.network
def test_returns_expected_tickers():
    """All requested tickers must appear as keys in the output."""
    tickers = ["AAPL", "MSFT"]
    result = fetch_historical_returns(tickers, lookback_years=1)
    assert set(result.keys()) == set(t.upper() for t in tickers)


@pytest.mark.network
def test_data_alignment():
    """All return series must have identical length (matrix alignment requirement)."""
    result = fetch_historical_returns(["AAPL", "MSFT"], lookback_years=1)
    lengths = [len(v) for v in result.values()]
    assert len(set(lengths)) == 1, f"Misaligned series lengths: {lengths}"


@pytest.mark.network
def test_series_are_non_empty():
    """Each return series must contain at least one observation."""
    result = fetch_historical_returns(["AAPL", "MSFT"], lookback_years=1)
    for ticker, series in result.items():
        assert len(series) > 0, f"Empty series returned for {ticker}"


@pytest.mark.network
def test_tickers_are_sorted_deterministically():
    """Adapter must return tickers in sorted order regardless of input order."""
    result = fetch_historical_returns(["MSFT", "AAPL"], lookback_years=1)
    assert list(result.keys()) == sorted(result.keys())


@pytest.mark.network
def test_uppercase_normalisation():
    """Lowercase tickers must be normalised to uppercase in the output."""
    result = fetch_historical_returns(["aapl", "msft"], lookback_years=1)
    for key in result.keys():
        assert key == key.upper()


@pytest.mark.network
def test_duplicate_tickers_deduplicated():
    """Passing duplicate tickers must not double entries in the output."""
    result = fetch_historical_returns(["AAPL", "AAPL", "MSFT"], lookback_years=1)
    assert len(result) == 2