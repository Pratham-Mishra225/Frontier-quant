"""
Unit tests for frontier.exceptions — exception hierarchy.

Tests verify:
  - Class hierarchy (issubclass relationships)
  - ConvergenceError can be raised and caught
  - Catching at parent class levels works correctly
"""
import pytest
from frontier.exceptions import (
    FrontierError,
    OptimizationError,
    ConvergenceError,
    DataAlignmentError,
)


# ---------------------------------------------------------------------------
# Hierarchy tests
# ---------------------------------------------------------------------------

def test_frontier_error_is_exception():
    assert issubclass(FrontierError, Exception)


def test_optimization_error_is_frontier_error():
    assert issubclass(OptimizationError, FrontierError)


def test_convergence_error_is_optimization_error():
    assert issubclass(ConvergenceError, OptimizationError)


def test_convergence_error_is_frontier_error():
    assert issubclass(ConvergenceError, FrontierError)


def test_data_alignment_error_is_frontier_error():
    assert issubclass(DataAlignmentError, FrontierError)


# ---------------------------------------------------------------------------
# Raise / catch behaviour
# ---------------------------------------------------------------------------

def test_convergence_error_can_be_raised_and_caught():
    """ConvergenceError must be raiseable and caught by its own type."""
    with pytest.raises(ConvergenceError, match="did not converge"):
        raise ConvergenceError("Optimizer did not converge.")


def test_convergence_error_caught_as_optimization_error():
    """ConvergenceError must be catchable as OptimizationError."""
    with pytest.raises(OptimizationError):
        raise ConvergenceError("Optimizer did not converge.")


def test_convergence_error_caught_as_frontier_error():
    """ConvergenceError must be catchable as FrontierError."""
    with pytest.raises(FrontierError):
        raise ConvergenceError("Optimizer did not converge.")


def test_convergence_error_caught_as_base_exception():
    """ConvergenceError must be catchable as the base Exception type."""
    with pytest.raises(Exception):
        raise ConvergenceError("Optimizer did not converge.")


def test_convergence_error_message_preserved():
    """The error message must be accessible via str()."""
    msg = "SLSQP iteration limit exceeded"
    exc = ConvergenceError(msg)
    assert str(exc) == msg


def test_data_alignment_error_can_be_raised_and_caught():
    """DataAlignmentError must be raiseable and caught by its own type."""
    with pytest.raises(DataAlignmentError):
        raise DataAlignmentError("Return series lengths do not match.")


# ---------------------------------------------------------------------------
# Optimizer convergence integration (mocked scipy)
# ---------------------------------------------------------------------------

def test_optimizer_raises_convergence_error_on_failed_solve(fake_returns):
    """
    If scipy.optimize.minimize reports failure (success=False),
    optimize_portfolio must raise ConvergenceError — never return silently.
    """
    from unittest.mock import patch, MagicMock
    from frontier.core.optimizer import optimize_portfolio

    failed_result = MagicMock()
    failed_result.success = False
    failed_result.message = "Iteration limit exceeded"

    with patch("frontier.core.optimizer.sco.minimize", return_value=failed_result):
        with pytest.raises(ConvergenceError, match="Iteration limit exceeded"):
            optimize_portfolio(fake_returns)


def test_optimizer_convergence_error_is_optimization_error(fake_returns):
    """ConvergenceError raised by optimizer must be catchable as OptimizationError."""
    from unittest.mock import patch, MagicMock
    from frontier.core.optimizer import optimize_portfolio

    failed_result = MagicMock()
    failed_result.success = False
    failed_result.message = "Iteration limit exceeded"

    with patch("frontier.core.optimizer.sco.minimize", return_value=failed_result):
        with pytest.raises(OptimizationError):
            optimize_portfolio(fake_returns)


def test_optimizer_successful_convergence_does_not_raise(fake_returns):
    """Normal valid input must not raise any convergence error."""
    from frontier.core.optimizer import optimize_portfolio

    # Should complete without raising — any exception here is a test failure.
    result = optimize_portfolio(fake_returns)
    assert "optimal_portfolio" in result
