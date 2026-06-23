"""
conftest.py — pytest configuration for the Frontier test suite.

Registers the custom 'network' marker so tests that make live calls to
Yahoo Finance can be selectively skipped:

    pytest -m "not network"        # offline / fast CI
    pytest                          # full suite including live calls

Shared fixtures available to all test modules are defined here.
"""
import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "network: marks tests that require a live internet connection (Yahoo Finance)",
    )


# ---------------------------------------------------------------------------
# Shared fixture — reusable across test_optimizer, test_exceptions, test_api
# ---------------------------------------------------------------------------

@pytest.fixture
def fake_returns():
    """Minimal valid returns dict: 3 assets, 5 observations each."""
    return {
        "AAPL": [0.010,  0.005, -0.002,  0.015,  0.008],
        "MSFT": [0.008,  0.010,  0.000, -0.005,  0.012],
        "GOOG": [-0.010, 0.020,  0.010, -0.015,  0.005],
    }
