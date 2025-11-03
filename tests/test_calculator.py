"""Unit tests for calculator module."""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from app.calculator import Calculator, LoggingObserver, AutoSaveObserver
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.history import CalculationHistory
from app.logger import Logger
from app.exceptions import OperationError, ValidationError, HistoryError


class TestCalculator:
    """Tests for Calculator class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def test_config(self, temp_dir):
        """Create a test configuration."""
        env_content = f"""
CALCULATOR_LOG_DIR={temp_dir}/logs
CALCULATOR_HISTORY_DIR={temp_dir}/history
CALCULATOR_MAX_HISTORY_SIZE=10
CALCULATOR_AUTO_SAVE=false
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
"""
        env_file = os.path.join(temp_dir, '.env')
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        return CalculatorConfig(env_file)
    
    @pytest.fixture
    def calculator(self, test_config):
        """Create a calculator instance for testing."""
        calc = Calculator(test_config)
        yield calc
        # Cleanup: close logger file handlers to avoid Windows file locking issues
        calc.logger.close_handlers()
    
    def test_calculator_initialization(self, calculator):
        """Test calculator initializes correctly."""
        assert calculator.config is not None
        assert calculator.logger is not None
        assert calculator.history is not None
        assert calculator.caretaker is not None
        assert len(calculator.observers) > 0
    
    @pytest.mark.parametrize("operation,a,b,expected", [
        ("add", 5, 3, 8),
        ("subtract", 10, 4, 6),
        ("multiply", 3, 4, 12),
        ("divide", 10, 2, 5),
        ("power", 2, 3, 8),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 50, 200, 25),
        ("abs_diff", 3, 10, 7),
    ])
    def test_perform_calculation(self, calculator, operation, a, b, expected):
        """Test performing various calculations."""
        result = calculator.perform_calculation(operation, a, b)
        assert result == expected
        assert len(calculator.history) == 1
    
    def test_perform_calculation_with_strings(self, calculator):
        """Test calculation with string inputs."""
        result = calculator.perform_calculation("add", "5", "3")
        assert result == 8
    
    def test_perform_calculation_invalid_operation(self, calculator):
        """Test calculation with invalid operation."""
        with pytest.raises(OperationError):
            calculator.perform_calculation("invalid", 5, 3)
    
    def test_perform_calculation_invalid_input(self, calculator):
        """Test calculation with invalid input."""
        with pytest.raises(ValidationError):
            calculator.perform_calculation("add", "abc", 3)
    
    def test_perform_calculation_exceeds_max_value(self, calculator):
        """Test calculation with value exceeding maximum."""
        with pytest.raises(ValidationError):
            calculator.perform_calculation("add", 10000000, 5)
    
    def test_division_by_zero(self, calculator):
        """Test division by zero raises error."""
        with pytest.raises(OperationError):
            calculator.perform_calculation("divide", 10, 0)
    
    def test_undo_operation(self, calculator):
        """Test undo functionality."""
        calculator.perform_calculation("add", 5, 3)
        calculator.perform_calculation("subtract", 10, 2)
        assert len(calculator.history) == 2
        
        calculator.undo()
        assert len(calculator.history) == 1
    
    def test_undo_empty_history(self, calculator):
        """Test undo with empty history succeeds (goes back to initial state)."""
        # Initial state has one saved state (empty)
        # Undo should work and return to empty
        calculator.undo()
        assert len(calculator.history) == 0
        
        # Now try to undo again - should raise error since there's nothing left
        with pytest.raises(HistoryError):
            calculator.undo()
    
    def test_redo_operation(self, calculator):
        """Test redo functionality."""
        calculator.perform_calculation("add", 5, 3)
        calculator.undo()
        assert len(calculator.history) == 0
        
        calculator.redo()
        assert len(calculator.history) == 1
    
    def test_redo_without_undo(self, calculator):
        """Test redo without undo raises error."""
        with pytest.raises(HistoryError):
            calculator.redo()
    
    def test_clear_history(self, calculator):
        """Test clearing history."""
        calculator.perform_calculation("add", 5, 3)
        calculator.perform_calculation("subtract", 10, 2)
        calculator.clear_history()
        assert len(calculator.history) == 0
    
    def test_save_history(self, calculator, temp_dir):
        """Test saving history to file."""
        calculator.perform_calculation("add", 5, 3)
        file_path = os.path.join(temp_dir, 'test_history.csv')
        calculator.save_history(file_path)
        assert os.path.exists(file_path)
    
    def test_load_history(self, calculator, temp_dir):
        """Test loading history from file."""
        calculator.perform_calculation("add", 5, 3)
        file_path = os.path.join(temp_dir, 'test_history.csv')
        calculator.save_history(file_path)
        
        calculator.clear_history()
        assert len(calculator.history) == 0
        
        calculator.load_history(file_path)
        assert len(calculator.history) == 1
    
    def test_display_history_empty(self, calculator, capsys):
        """Test displaying empty history."""
        calculator.display_history()
        captured = capsys.readouterr()
        assert "No calculations" in captured.out
    
    def test_display_history_with_calculations(self, calculator, capsys):
        """Test displaying history with calculations."""
        calculator.perform_calculation("add", 5, 3)
        calculator.display_history()
        captured = capsys.readouterr()
        assert "Calculation History" in captured.out
    
    def test_display_help(self, calculator, capsys):
        """Test displaying help message."""
        calculator.display_help()
        captured = capsys.readouterr()
        assert "Calculator Commands" in captured.out
        assert "add" in captured.out
        assert "exit" in captured.out
    
    def test_register_observer(self, calculator):
        """Test registering an observer."""
        mock_observer = Mock()
        initial_count = len(calculator.observers)
        calculator.register_observer(mock_observer)
        assert len(calculator.observers) == initial_count + 1
    
    def test_notify_observers(self, calculator):
        """Test notifying observers."""
        mock_observer = Mock()
        calculator.register_observer(mock_observer)
        
        calculator.perform_calculation("add", 5, 3)
        assert mock_observer.on_calculation_performed.called
    
    def test_precision_rounding(self, calculator):
        """Test result is rounded to configured precision."""
        result = calculator.perform_calculation("divide", 10, 3)
        # With precision=2, should be 3.33
        assert result == 3.33
    
    def test_root_operation(self, calculator):
        """Test root operation."""
        result = calculator.perform_calculation("root", 9, 2)
        assert result == 3.0


class TestLoggingObserver:
    """Tests for LoggingObserver."""
    
    def test_logging_observer(self):
        """Test logging observer logs calculations."""
        mock_logger = Mock(spec=Logger)
        observer = LoggingObserver(mock_logger)
        
        calc = Calculation("add", 5, 3, 8)
        observer.on_calculation_performed(calc)
        
        assert mock_logger.info.called
        call_args = mock_logger.info.call_args[0][0]
        assert "add" in call_args
        assert "5" in call_args
        assert "3" in call_args
        assert "8" in call_args


class TestAutoSaveObserver:
    """Tests for AutoSaveObserver."""
    
    def test_auto_save_observer(self, tmp_path):
        """Test auto-save observer saves history."""
        history = CalculationHistory()
        file_path = tmp_path / "auto_save.csv"
        
        observer = AutoSaveObserver(history, str(file_path))
        
        calc = Calculation("add", 5, 3, 8)
        history.add_calculation(calc)
        observer.on_calculation_performed(calc)
        
        assert file_path.exists()
    
    def test_auto_save_observer_error_handling(self, capsys):
        """Test auto-save observer handles errors gracefully."""
        from unittest.mock import patch
        
        history = CalculationHistory()
        observer = AutoSaveObserver(history, "/tmp/test.csv")
        
        # Mock save_to_csv to raise an exception
        with patch.object(history, 'save_to_csv', side_effect=Exception("Test error")):
            calc = Calculation("add", 5, 3, 8)
            # Should not raise exception - errors should be caught
            observer.on_calculation_performed(calc)
        
        captured = capsys.readouterr()
        # The error message should be printed to stdout
        assert "Failed to auto-save" in captured.out


class TestCalculatorREPL:
    """Tests for Calculator REPL."""
    
    @pytest.fixture
    def calculator_with_config(self, tmp_path):
        """Create calculator with temporary config."""
        env_content = f"""
CALCULATOR_LOG_DIR={tmp_path}/logs
CALCULATOR_HISTORY_DIR={tmp_path}/history
CALCULATOR_AUTO_SAVE=false
"""
        env_file = tmp_path / '.env'
        env_file.write_text(env_content)
        
        config = CalculatorConfig(str(env_file))
        return Calculator(config)
    
    @patch('builtins.input')
    def test_repl_exit_command(self, mock_input, calculator_with_config, capsys):
        """Test REPL exit command."""
        mock_input.side_effect = ['exit']
        
        calculator_with_config.run_repl()
        captured = capsys.readouterr()
        assert "Goodbye" in captured.out
    
    @patch('builtins.input')
    def test_repl_help_command(self, mock_input, calculator_with_config, capsys):
        """Test REPL help command."""
        mock_input.side_effect = ['help', 'exit']
        
        calculator_with_config.run_repl()
        captured = capsys.readouterr()
        assert "Calculator Commands" in captured.out
    
    @patch('builtins.input')
    def test_repl_calculation(self, mock_input, calculator_with_config, capsys):
        """Test REPL calculation."""
        mock_input.side_effect = ['add', '5', '3', 'exit']
        
        calculator_with_config.run_repl()
        captured = capsys.readouterr()
        assert "Result: 8" in captured.out
    
    @patch('builtins.input')
    def test_repl_invalid_command(self, mock_input, calculator_with_config, capsys):
        """Test REPL with invalid command."""
        mock_input.side_effect = ['invalid', 'exit']
        
        calculator_with_config.run_repl()
        captured = capsys.readouterr()
        assert "Unknown command" in captured.out
    
    @patch('builtins.input')
    def test_repl_keyboard_interrupt(self, mock_input, calculator_with_config, capsys):
        """Test REPL handles keyboard interrupt."""
        mock_input.side_effect = [KeyboardInterrupt(), 'exit']
        
        calculator_with_config.run_repl()
        captured = capsys.readouterr()
        assert "exit" in captured.out.lower()
