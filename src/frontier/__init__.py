"""
frontier — Stateless Vectorized Portfolio Optimization Engine.

Minimalist public API. Import directly from the top-level package:

    from frontier import optimize, fetch_data

For the FastAPI web server install the [server] extra:

    pip install frontier-api[server]

then run:

    uvicorn frontier.api.main:app --reload
"""

from .core.optimizer import (
    optimize_portfolio as optimize,
    portfolio_performance,
)
from .adapters.yfinance_client import fetch_historical_returns as fetch_data

__version__ = "0.1.0"
__author__ = "Pratham Mishra"
__license__ = "MIT"

__all__ = [
    # Clean public aliases
    "optimize",
    "fetch_data",
    # Full names (still importable for power users)
    "optimize_portfolio",
    "portfolio_performance",
    "fetch_historical_returns",
    # Package metadata
    "__version__",
    "__author__",
    "__license__",
]

# Also expose the full names so `from frontier import optimize_portfolio` still works
optimize_portfolio = optimize
fetch_historical_returns = fetch_data
