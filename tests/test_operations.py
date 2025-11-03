"""Unit tests for operations module."""

import pytest
from app.operations import (
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    PowerOperation,
    RootOperation,
    ModulusOperation,
    IntegerDivideOperation,
    PercentageOperation,
    AbsoluteDifferenceOperation,
    OperationFactory,
)
from app.exceptions import OperationError


class TestAddOperation:
    """Tests for AddOperation."""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        op = AddOperation()
        assert op.execute(5, 3) == 8
        assert op.get_name() == "add"
    
    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        op = AddOperation()
        assert op.execute(-5, -3) == -8
        assert op.execute(-5, 3) == -2
    
    def test_add_zero(self):
        """Test adding zero."""
        op = AddOperation()
        assert op.execute(5, 0) == 5
        assert op.execute(0, 0) == 0


class TestSubtractOperation:
    """Tests for SubtractOperation."""
    
    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        op = SubtractOperation()
        assert op.execute(10, 3) == 7
        assert op.get_name() == "subtract"
    
    def test_subtract_negative_result(self):
        """Test subtraction resulting in negative."""
        op = SubtractOperation()
        assert op.execute(3, 10) == -7


class TestMultiplyOperation:
    """Tests for MultiplyOperation."""
    
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        op = MultiplyOperation()
        assert op.execute(5, 3) == 15
        assert op.get_name() == "multiply"
    
    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        op = MultiplyOperation()
        assert op.execute(5, 0) == 0
    
    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        op = MultiplyOperation()
        assert op.execute(-5, 3) == -15
        assert op.execute(-5, -3) == 15


class TestDivideOperation:
    """Tests for DivideOperation."""
    
    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        op = DivideOperation()
        assert op.execute(10, 2) == 5
        assert op.get_name() == "divide"
    
    def test_divide_by_zero(self):
        """Test division by zero raises error."""
        op = DivideOperation()
        with pytest.raises(OperationError, match="Division by zero"):
            op.execute(10, 0)
    
    def test_divide_negative_numbers(self):
        """Test dividing negative numbers."""
        op = DivideOperation()
        assert op.execute(-10, 2) == -5
        assert op.execute(10, -2) == -5


class TestPowerOperation:
    """Tests for PowerOperation."""
    
    def test_power_positive_exponent(self):
        """Test power with positive exponent."""
        op = PowerOperation()
        assert op.execute(2, 3) == 8
        assert op.get_name() == "power"
    
    def test_power_zero_exponent(self):
        """Test power with zero exponent."""
        op = PowerOperation()
        assert op.execute(5, 0) == 1
    
    def test_power_negative_exponent(self):
        """Test power with negative exponent."""
        op = PowerOperation()
        assert op.execute(2, -2) == 0.25
    
    def test_power_fractional_exponent(self):
        """Test power with fractional exponent."""
        op = PowerOperation()
        assert op.execute(4, 0.5) == 2


class TestRootOperation:
    """Tests for RootOperation."""
    
    def test_square_root(self):
        """Test square root."""
        op = RootOperation()
        assert op.execute(9, 2) == 3
        assert op.get_name() == "root"
    
    def test_cube_root(self):
        """Test cube root."""
        op = RootOperation()
        result = op.execute(8, 3)
        assert abs(result - 2) < 0.01
    
    def test_root_zero_degree(self):
        """Test root with zero degree raises error."""
        op = RootOperation()
        with pytest.raises(OperationError, match="Root degree cannot be zero"):
            op.execute(9, 0)
    
    def test_even_root_negative_number(self):
        """Test even root of negative number raises error."""
        op = RootOperation()
        with pytest.raises(OperationError, match="Cannot calculate even root"):
            op.execute(-9, 2)
    
    def test_odd_root_negative_number(self):
        """Test odd root of negative number."""
        op = RootOperation()
        result = op.execute(-8, 3)
        assert abs(result - (-2)) < 0.01


class TestModulusOperation:
    """Tests for ModulusOperation."""
    
    def test_modulus_positive_numbers(self):
        """Test modulus with positive numbers."""
        op = ModulusOperation()
        assert op.execute(10, 3) == 1
        assert op.get_name() == "modulus"
    
    def test_modulus_by_zero(self):
        """Test modulus by zero raises error."""
        op = ModulusOperation()
        with pytest.raises(OperationError, match="Modulus by zero"):
            op.execute(10, 0)
    
    def test_modulus_negative_numbers(self):
        """Test modulus with negative numbers."""
        op = ModulusOperation()
        assert op.execute(-10, 3) == 2


class TestIntegerDivideOperation:
    """Tests for IntegerDivideOperation."""
    
    def test_integer_divide_positive_numbers(self):
        """Test integer division with positive numbers."""
        op = IntegerDivideOperation()
        assert op.execute(10, 3) == 3
        assert op.get_name() == "int_divide"
    
    def test_integer_divide_by_zero(self):
        """Test integer division by zero raises error."""
        op = IntegerDivideOperation()
        with pytest.raises(OperationError, match="Division by zero"):
            op.execute(10, 0)
    
    def test_integer_divide_negative_numbers(self):
        """Test integer division with negative numbers."""
        op = IntegerDivideOperation()
        assert op.execute(-10, 3) == -4


class TestPercentageOperation:
    """Tests for PercentageOperation."""
    
    def test_percentage_calculation(self):
        """Test percentage calculation."""
        op = PercentageOperation()
        assert op.execute(50, 200) == 25
        assert op.get_name() == "percent"
    
    def test_percentage_zero_denominator(self):
        """Test percentage with zero denominator raises error."""
        op = PercentageOperation()
        with pytest.raises(OperationError, match="Cannot calculate percentage"):
            op.execute(50, 0)
    
    def test_percentage_over_100(self):
        """Test percentage over 100."""
        op = PercentageOperation()
        assert op.execute(300, 200) == 150


class TestAbsoluteDifferenceOperation:
    """Tests for AbsoluteDifferenceOperation."""
    
    def test_absolute_difference_positive_result(self):
        """Test absolute difference with positive result."""
        op = AbsoluteDifferenceOperation()
        assert op.execute(10, 3) == 7
        assert op.get_name() == "abs_diff"
    
    def test_absolute_difference_negative_inputs(self):
        """Test absolute difference always returns positive."""
        op = AbsoluteDifferenceOperation()
        assert op.execute(3, 10) == 7
        assert op.execute(-5, -3) == 2


class TestOperationFactory:
    """Tests for OperationFactory."""
    
    @pytest.mark.parametrize("operation_name,expected_class", [
        ("add", AddOperation),
        ("subtract", SubtractOperation),
        ("multiply", MultiplyOperation),
        ("divide", DivideOperation),
        ("power", PowerOperation),
        ("root", RootOperation),
        ("modulus", ModulusOperation),
        ("int_divide", IntegerDivideOperation),
        ("percent", PercentageOperation),
        ("abs_diff", AbsoluteDifferenceOperation),
    ])
    def test_create_operation(self, operation_name, expected_class):
        """Test creating operations using factory."""
        op = OperationFactory.create_operation(operation_name)
        assert isinstance(op, expected_class)
    
    def test_create_unknown_operation(self):
        """Test creating unknown operation raises error."""
        with pytest.raises(OperationError, match="Unknown operation"):
            OperationFactory.create_operation("unknown")
    
    def test_get_available_operations(self):
        """Test getting list of available operations."""
        operations = OperationFactory.get_available_operations()
        assert len(operations) == 10
        assert "add" in operations
        assert "subtract" in operations
        assert "multiply" in operations
    
    def test_register_operation(self):
        """Test registering a new operation."""
        class CustomOperation(AddOperation):
            def get_name(self):
                return "custom"
        
        OperationFactory.register_operation("custom", CustomOperation)
        op = OperationFactory.create_operation("custom")
        assert isinstance(op, CustomOperation)
        
        # Clean up
        OperationFactory._operations.pop("custom", None)
