"""Calculation class representing a single calculation."""

from datetime import datetime
from typing import Any


class Calculation:
    """Represents a single calculation with operation, operands, and result."""
    
    def __init__(self, operation: str, operand1: float, operand2: float, result: float):
        """
        Initialize a calculation.
        
        Args:
            operation: The operation name.
            operand1: The first operand.
            operand2: The second operand.
            result: The result of the calculation.
        """
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result
        self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        """Return string representation of the calculation."""
        return (
            f"{self.operand1} {self.operation} {self.operand2} = {self.result} "
            f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]"
        )
    
    def __repr__(self) -> str:
        """Return detailed representation of the calculation."""
        return (
            f"Calculation(operation={self.operation}, "
            f"operand1={self.operand1}, operand2={self.operand2}, "
            f"result={self.result}, timestamp={self.timestamp})"
        )
    
    def to_dict(self) -> dict:
        """
        Convert calculation to dictionary.
        
        Returns:
            Dictionary representation of the calculation.
        """
        return {
            'operation': self.operation,
            'operand1': self.operand1,
            'operand2': self.operand2,
            'result': self.result,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Calculation':
        """
        Create a Calculation instance from a dictionary.
        
        Args:
            data: Dictionary containing calculation data.
            
        Returns:
            A new Calculation instance.
        """
        calc = cls(
            operation=data['operation'],
            operand1=float(data['operand1']),
            operand2=float(data['operand2']),
            result=float(data['result'])
        )
        
        # Set timestamp if provided
        if 'timestamp' in data:
            calc.timestamp = datetime.fromisoformat(data['timestamp'])
        
        return calc
