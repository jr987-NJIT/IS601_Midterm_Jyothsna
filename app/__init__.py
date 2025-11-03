"""Calculator application package."""

from app.calculator import Calculator
from app.calculation import Calculation
from app.operations import OperationFactory
from app.exceptions import (
    CalculatorError,
    OperationError,
    ValidationError,
    ConfigurationError,
    HistoryError,
)

__version__ = "1.0.0"
__all__ = [
    "Calculator",
    "Calculation",
    "OperationFactory",
    "CalculatorError",
    "OperationError",
    "ValidationError",
    "ConfigurationError",
    "HistoryError",
]
