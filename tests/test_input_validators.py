"""Unit tests for input validators."""

import pytest
from app.input_validators import InputValidator
from app.exceptions import ValidationError


class TestInputValidator:
    """Tests for InputValidator class."""
    
    def test_validate_number_with_int(self):
        """Test validating integer."""
        result = InputValidator.validate_number(5)
        assert result == 5.0
    
    def test_validate_number_with_float(self):
        """Test validating float."""
        result = InputValidator.validate_number(5.5)
        assert result == 5.5
    
    def test_validate_number_with_string(self):
        """Test validating numeric string."""
        result = InputValidator.validate_number("10")
        assert result == 10.0
    
    def test_validate_number_with_invalid_string(self):
        """Test validating invalid string raises error."""
        with pytest.raises(ValidationError, match="Invalid number"):
            InputValidator.validate_number("abc")
    
    def test_validate_number_with_none(self):
        """Test validating None raises error."""
        with pytest.raises(ValidationError):
            InputValidator.validate_number(None)
    
    def test_validate_number_exceeds_max(self):
        """Test validating number exceeding maximum."""
        with pytest.raises(ValidationError, match="exceeds maximum"):
            InputValidator.validate_number(1000, max_value=100)
    
    def test_validate_number_with_negative_max(self):
        """Test validating negative number with max value."""
        with pytest.raises(ValidationError, match="exceeds maximum"):
            InputValidator.validate_number(-1000, max_value=100)
    
    def test_validate_operation_valid(self):
        """Test validating valid operation."""
        available = ['add', 'subtract', 'multiply']
        result = InputValidator.validate_operation('add', available)
        assert result == 'add'
    
    def test_validate_operation_invalid(self):
        """Test validating invalid operation raises error."""
        available = ['add', 'subtract', 'multiply']
        with pytest.raises(ValidationError, match="Unknown operation"):
            InputValidator.validate_operation('divide', available)
    
    def test_validate_positive_number(self):
        """Test validating positive number."""
        result = InputValidator.validate_positive_number(5)
        assert result == 5.0
    
    def test_validate_positive_number_with_zero(self):
        """Test validating zero raises error."""
        with pytest.raises(ValidationError, match="must be positive"):
            InputValidator.validate_positive_number(0)
    
    def test_validate_positive_number_with_negative(self):
        """Test validating negative number raises error."""
        with pytest.raises(ValidationError, match="must be positive"):
            InputValidator.validate_positive_number(-5)
    
    def test_validate_non_zero(self):
        """Test validating non-zero number."""
        result = InputValidator.validate_non_zero(5)
        assert result == 5.0
        
        result = InputValidator.validate_non_zero(-5)
        assert result == -5.0
    
    def test_validate_non_zero_with_zero(self):
        """Test validating zero raises error."""
        with pytest.raises(ValidationError, match="cannot be zero"):
            InputValidator.validate_non_zero(0)
    
    def test_validate_number_with_float_string(self):
        """Test validating float string."""
        result = InputValidator.validate_number("3.14")
        assert result == 3.14
    
    def test_validate_number_with_negative_string(self):
        """Test validating negative string."""
        result = InputValidator.validate_number("-10")
        assert result == -10.0
