"""Custom exceptions for the calculator application."""


class CalculatorError(Exception):
    """Base exception for calculator-related errors."""
    pass


class OperationError(CalculatorError):
    """Exception raised when an operation fails."""
    pass


class ValidationError(CalculatorError):
    """Exception raised when input validation fails."""
    pass


class ConfigurationError(CalculatorError):
    """Exception raised when there's a configuration issue."""
    pass


class HistoryError(CalculatorError):
    """Exception raised when there's an issue with history management."""
    pass
