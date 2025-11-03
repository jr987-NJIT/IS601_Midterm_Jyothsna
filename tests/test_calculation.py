"""Unit tests for Calculation class."""

import pytest
from datetime import datetime
from app.calculation import Calculation


class TestCalculation:
    """Tests for Calculation class."""
    
    def test_calculation_initialization(self):
        """Test creating a calculation."""
        calc = Calculation("add", 5, 3, 8)
        assert calc.operation == "add"
        assert calc.operand1 == 5
        assert calc.operand2 == 3
        assert calc.result == 8
        assert isinstance(calc.timestamp, datetime)
    
    def test_calculation_str(self):
        """Test string representation of calculation."""
        calc = Calculation("add", 5, 3, 8)
        string_repr = str(calc)
        assert "5" in string_repr
        assert "3" in string_repr
        assert "8" in string_repr
        assert "add" in string_repr
    
    def test_calculation_repr(self):
        """Test repr of calculation."""
        calc = Calculation("multiply", 2, 4, 8)
        repr_str = repr(calc)
        assert "Calculation" in repr_str
        assert "multiply" in repr_str
        assert "2" in repr_str
        assert "4" in repr_str
        assert "8" in repr_str
    
    def test_calculation_to_dict(self):
        """Test converting calculation to dictionary."""
        calc = Calculation("subtract", 10, 3, 7)
        calc_dict = calc.to_dict()
        
        assert calc_dict['operation'] == "subtract"
        assert calc_dict['operand1'] == 10
        assert calc_dict['operand2'] == 3
        assert calc_dict['result'] == 7
        assert 'timestamp' in calc_dict
    
    def test_calculation_from_dict(self):
        """Test creating calculation from dictionary."""
        data = {
            'operation': 'divide',
            'operand1': 20,
            'operand2': 4,
            'result': 5,
            'timestamp': datetime.now().isoformat()
        }
        
        calc = Calculation.from_dict(data)
        assert calc.operation == "divide"
        assert calc.operand1 == 20
        assert calc.operand2 == 4
        assert calc.result == 5
        assert isinstance(calc.timestamp, datetime)
    
    def test_calculation_from_dict_without_timestamp(self):
        """Test creating calculation from dict without timestamp."""
        data = {
            'operation': 'power',
            'operand1': 2,
            'operand2': 3,
            'result': 8
        }
        
        calc = Calculation.from_dict(data)
        assert calc.operation == "power"
        assert isinstance(calc.timestamp, datetime)
    
    def test_calculation_with_negative_numbers(self):
        """Test calculation with negative numbers."""
        calc = Calculation("subtract", 5, 10, -5)
        assert calc.operand1 == 5
        assert calc.operand2 == 10
        assert calc.result == -5
    
    def test_calculation_with_floats(self):
        """Test calculation with float numbers."""
        calc = Calculation("divide", 10.5, 2.5, 4.2)
        assert calc.operand1 == 10.5
        assert calc.operand2 == 2.5
        assert calc.result == 4.2
