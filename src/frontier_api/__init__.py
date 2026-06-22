"""
frontier_api — Stateless Vectorized Portfolio Optimization Engine.

Public API surface. Import the core engine and data adapter directly:

    from frontier_api import optimize_portfolio, fetch_historical_returns

For the FastAPI web server install the [server] extra:

    pip install frontier-api[server]

then run:

    uvicorn frontier_api.api.main:app --reload
"""

from frontier_api.core.optimizer import (
    optimize_portfolio,
    portfolio_performance,
)
from frontier_api.adapters.yfinance_client import fetch_historical_returns

__version__ = "0.1.0"
__author__ = "Pratham Mishra"
__license__ = "MIT"

__all__ = [
    # Core math engine
    "optimize_portfolio",
    "portfolio_performance",
    # Market data adapter
    "fetch_historical_returns",
    # Package metadata
    "__version__",
    "__author__",
    "__license__",
]
