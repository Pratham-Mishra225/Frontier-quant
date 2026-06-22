"""
conftest.py — pytest configuration for the Frontier test suite.

Registers the custom 'network' marker so tests that make live calls to
Yahoo Finance can be selectively skipped:

    pytest -m "not network"        # offline / fast CI
    pytest                          # full suite including live calls
"""
import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "network: marks tests that require a live internet connection (Yahoo Finance)",
    )
