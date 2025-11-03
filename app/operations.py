"""Operations module with Factory pattern for calculator operations."""

from abc import ABC, abstractmethod
from typing import Dict, Type
from app.exceptions import OperationError


class Operation(ABC):
    """Abstract base class for all operations."""
    
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """
        Execute the operation.
        
        Args:
            a: First operand.
            b: Second operand.
            
        Returns:
            Result of the operation.
        """
        pass  # pragma: no cover
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the operation name."""
        pass  # pragma: no cover


class AddOperation(Operation):
    """Addition operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    def get_name(self) -> str:
        """Get operation name."""
        return "add"


class SubtractOperation(Operation):
    """Subtraction operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Subtract b from a."""
        return a - b
    
    def get_name(self) -> str:
        """Get operation name."""
        return "subtract"


class MultiplyOperation(Operation):
    """Multiplication operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    def get_name(self) -> str:
        """Get operation name."""
        return "multiply"


class DivideOperation(Operation):
    """Division operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Divide a by b."""
        if b == 0:
            raise OperationError("Division by zero is not allowed")
        return a / b
    
    def get_name(self) -> str:
        """Get operation name."""
        return "divide"


class PowerOperation(Operation):
    """Power operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Raise a to the power of b."""
        try:
            result = a ** b
            if not isinstance(result, (int, float)) or result != result:  # Check for NaN
                raise OperationError("Invalid result from power operation")
            return result
        except (ValueError, OverflowError) as e:
            raise OperationError(f"Power operation failed: {e}")
    
    def get_name(self) -> str:
        """Get operation name."""
        return "power"


class RootOperation(Operation):
    """Root operation - calculates the nth root of a number."""
    
    def execute(self, a: float, b: float) -> float:
        """
        Calculate the bth root of a.
        
        Args:
            a: The number to find the root of.
            b: The root degree (e.g., 2 for square root, 3 for cube root).
        """
        if b == 0:
            raise OperationError("Root degree cannot be zero")
        
        if a < 0 and b % 2 == 0:
            raise OperationError("Cannot calculate even root of negative number")
        
        try:
            # For negative numbers with odd roots, handle the sign separately
            if a < 0:
                result = -(abs(a) ** (1 / b))
            else:
                result = a ** (1 / b)
            
            if not isinstance(result, (int, float)) or result != result:  # Check for NaN  # pragma: no cover
                raise OperationError("Invalid result from root operation")  # pragma: no cover
            
            return result
        except (ValueError, OverflowError, ZeroDivisionError) as e:  # pragma: no cover
            raise OperationError(f"Root operation failed: {e}")  # pragma: no cover
    
    def get_name(self) -> str:
        """Get operation name."""
        return "root"


class ModulusOperation(Operation):
    """Modulus operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Calculate a modulo b."""
        if b == 0:
            raise OperationError("Modulus by zero is not allowed")
        return a % b
    
    def get_name(self) -> str:
        """Get operation name."""
        return "modulus"


class IntegerDivideOperation(Operation):
    """Integer division operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Perform integer division of a by b."""
        if b == 0:
            raise OperationError("Division by zero is not allowed")
        return a // b
    
    def get_name(self) -> str:
        """Get operation name."""
        return "int_divide"


class PercentageOperation(Operation):
    """Percentage operation - calculates what percentage a is of b."""
    
    def execute(self, a: float, b: float) -> float:
        """
        Calculate what percentage a is of b.
        
        Args:
            a: The part.
            b: The whole.
            
        Returns:
            (a / b) * 100
        """
        if b == 0:
            raise OperationError("Cannot calculate percentage with zero denominator")
        return (a / b) * 100
    
    def get_name(self) -> str:
        """Get operation name."""
        return "percent"


class AbsoluteDifferenceOperation(Operation):
    """Absolute difference operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Calculate the absolute difference between a and b."""
        return abs(a - b)
    
    def get_name(self) -> str:
        """Get operation name."""
        return "abs_diff"


class OperationFactory:
    """Factory class for creating operation instances."""
    
    _operations: Dict[str, Type[Operation]] = {
        'add': AddOperation,
        'subtract': SubtractOperation,
        'multiply': MultiplyOperation,
        'divide': DivideOperation,
        'power': PowerOperation,
        'root': RootOperation,
        'modulus': ModulusOperation,
        'int_divide': IntegerDivideOperation,
        'percent': PercentageOperation,
        'abs_diff': AbsoluteDifferenceOperation,
    }
    
    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        """
        Create an operation instance by name.
        
        Args:
            operation_name: Name of the operation.
            
        Returns:
            An instance of the requested operation.
            
        Raises:
            OperationError: If the operation is not supported.
        """
        operation_class = cls._operations.get(operation_name)
        if operation_class is None:
            raise OperationError(
                f"Unknown operation: {operation_name}. "
                f"Available operations: {', '.join(cls.get_available_operations())}"
            )
        return operation_class()
    
    @classmethod
    def get_available_operations(cls) -> list:
        """
        Get a list of available operation names.
        
        Returns:
            List of operation names.
        """
        return list(cls._operations.keys())
    
    @classmethod
    def register_operation(cls, name: str, operation_class: Type[Operation]):
        """
        Register a new operation.
        
        Args:
            name: Name of the operation.
            operation_class: Operation class to register.
        """
        cls._operations[name] = operation_class
