"""
frontier.exceptions — Typed exception hierarchy.

All exceptions are importable from this module:

    from frontier.exceptions import ConvergenceError, DataAlignmentError
"""


class FrontierError(Exception):
    """Base class for all Frontier library errors."""


class OptimizationError(FrontierError):
    """Raised when the optimization engine encounters an unrecoverable error."""


class ConvergenceError(OptimizationError):
    """
    Raised when the numerical solver (SLSQP) fails to converge.

    This signals that the optimizer ran but did not find a satisfactory solution.
    Callers should inspect the error message for the solver's own diagnostic.
    """


class DataAlignmentError(FrontierError):
    """
    Raised when input return series have incompatible dimensions.

    For example: different numbers of observations across assets.
    """
