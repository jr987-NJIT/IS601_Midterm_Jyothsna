"""Input validation utilities for the calculator application."""

from typing import Any
from app.exceptions import ValidationError


class InputValidator:
    """Validates user inputs for the calculator."""
    
    @staticmethod
    def validate_number(value: Any, max_value: float = None) -> float:
        """
        Validate and convert input to a number.
        
        Args:
            value: The value to validate.
            max_value: Maximum allowed value (optional).
            
        Returns:
            The validated number as a float.
            
        Raises:
            ValidationError: If validation fails.
        """
        try:
            num = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid number: {value}")
        
        if not isinstance(num, (int, float)) or num != num:  # Check for NaN
            raise ValidationError(f"Invalid number: {value}")
        
        if max_value is not None and abs(num) > max_value:
            raise ValidationError(
                f"Number {num} exceeds maximum allowed value of {max_value}"
            )
        
        return num
    
    @staticmethod
    def validate_operation(operation: str, available_operations: list) -> str:
        """
        Validate that the operation is supported.
        
        Args:
            operation: The operation name.
            available_operations: List of supported operations.
            
        Returns:
            The validated operation name.
            
        Raises:
            ValidationError: If the operation is not supported.
        """
        if operation not in available_operations:
            raise ValidationError(
                f"Unknown operation: {operation}. "
                f"Available operations: {', '.join(available_operations)}"
            )
        return operation
    
    @staticmethod
    def validate_positive_number(value: Any) -> float:
        """
        Validate that the input is a positive number.
        
        Args:
            value: The value to validate.
            
        Returns:
            The validated positive number.
            
        Raises:
            ValidationError: If the value is not positive.
        """
        num = InputValidator.validate_number(value)
        if num <= 0:
            raise ValidationError(f"Value must be positive: {value}")
        return num
    
    @staticmethod
    def validate_non_zero(value: Any) -> float:
        """
        Validate that the input is not zero.
        
        Args:
            value: The value to validate.
            
        Returns:
            The validated non-zero number.
            
        Raises:
            ValidationError: If the value is zero.
        """
        num = InputValidator.validate_number(value)
        if num == 0:
            raise ValidationError("Value cannot be zero")
        return num
