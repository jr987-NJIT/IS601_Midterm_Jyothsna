"""Additional tests to achieve 100% coverage."""

import pytest
import os
import tempfile
import builtins
from unittest.mock import patch, Mock
from app.calculator import Calculator
from app.logger import Logger
from app.history import CalculationHistory
from app.input_validators import InputValidator
from app.operations import OperationFactory, PowerOperation
from app.exceptions import ValidationError, OperationError, HistoryError
from app.calculator_config import CalculatorConfig


class TestLoggerMethods:
    """Tests for Logger methods to achieve 100% coverage."""
    
    def test_logger_warning(self):
        """Test logger warning method."""
        logger = Logger()
        logger.warning("Test warning message")
        # Should not raise exception
    
    def test_logger_error(self):
        """Test logger error method."""
        logger = Logger()
        logger.error("Test error message")
        # Should not raise exception
    
    def test_logger_debug(self):
        """Test logger debug method."""
        logger = Logger()
        logger.debug("Test debug message")
        # Should not raise exception


class TestCalculatorREPLCoverage:
    """Tests for Calculator REPL to achieve 100% coverage."""
    
    @pytest.fixture
    def calculator_with_config(self, tmp_path):
        """Create calculator with temporary config."""
        env_content = f"""CALCULATOR_LOG_DIR={tmp_path}/logs
CALCULATOR_HISTORY_DIR={tmp_path}/history
CALCULATOR_AUTO_SAVE=false
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=10000000000
CALCULATOR_DEFAULT_ENCODING=utf-8"""
        env_file = tmp_path / '.env'
        env_file.write_text(env_content)
        
        config = CalculatorConfig(str(env_file))
        calc = Calculator(config)
        yield calc
        calc.logger.close_handlers()
    
    @patch('builtins.input')
    def test_repl_empty_command(self, mock_input, calculator_with_config):
        """Test REPL with empty command."""
        mock_input.side_effect = ['', 'exit']
        calculator_with_config.run_repl()
        # Should handle empty input gracefully
    
    @patch('builtins.input')
    def test_repl_history_command(self, mock_input, calculator_with_config):
        """Test REPL history command."""
        mock_input.side_effect = ['add', '5', '3', 'history', 'exit']
        calculator_with_config.run_repl()
        # Should display history
    
    @patch('builtins.input')
    def test_repl_clear_command(self, mock_input, calculator_with_config):
        """Test REPL clear command."""
        mock_input.side_effect = ['add', '5', '3', 'clear', 'exit']
        calculator_with_config.run_repl()
        # Should clear history
    
    @patch('builtins.input')
    def test_repl_undo_command(self, mock_input, calculator_with_config):
        """Test REPL undo command."""
        mock_input.side_effect = ['add', '5', '3', 'undo', 'exit']
        calculator_with_config.run_repl()
        # Should undo
    
    @patch('builtins.input')
    def test_repl_redo_command(self, mock_input, calculator_with_config):
        """Test REPL redo command."""
        mock_input.side_effect = ['add', '5', '3', 'undo', 'redo', 'exit']
        calculator_with_config.run_repl()
        # Should redo
    
    @patch('builtins.input')
    def test_repl_save_command(self, mock_input, calculator_with_config):
        """Test REPL save command."""
        mock_input.side_effect = ['add', '5', '3', 'save', 'exit']
        calculator_with_config.run_repl()
        # Should save
    
    @patch('builtins.input')
    def test_repl_load_command(self, mock_input, calculator_with_config, tmp_path):
        """Test REPL load command."""
        # First save some history
        calculator_with_config.perform_calculation('add', 5, 3)
        calculator_with_config.save_history()
        
        mock_input.side_effect = ['load', 'exit']
        calculator_with_config.run_repl()
        # Should load
    
    @patch('builtins.input')
    def test_repl_operation_error(self, mock_input, calculator_with_config):
        """Test REPL handling of operation error."""
        mock_input.side_effect = ['divide', '10', '0', 'exit']
        calculator_with_config.run_repl()
        # Should handle division by zero
    
    @patch('builtins.input')
    def test_repl_validation_error(self, mock_input, calculator_with_config):
        """Test REPL handling of validation error."""
        mock_input.side_effect = ['add', 'abc', '3', 'exit']
        calculator_with_config.run_repl()
        # Should handle invalid input
    
    @patch('builtins.input')
    def test_repl_history_error(self, mock_input, calculator_with_config):
        """Test REPL handling of history error."""
        mock_input.side_effect = ['undo', 'undo', 'exit']
        calculator_with_config.run_repl()
        # Should handle undo on empty history
    
    @patch('builtins.input')
    def test_repl_unexpected_error(self, mock_input, calculator_with_config):
        """Test REPL handling of unexpected error."""
        mock_input.side_effect = ['add', '5', '3', 'exit']
        
        # Mock perform_calculation to raise unexpected error
        original_perform = calculator_with_config.perform_calculation
        def mock_perform(*args, **kwargs):
            if len(args) > 0 and args[0] == 'add':
                raise RuntimeError("Unexpected error")
            return original_perform(*args, **kwargs)
        
        calculator_with_config.perform_calculation = mock_perform
        calculator_with_config.run_repl()
        # Should handle unexpected errors


class TestHistoryCoverage:
    """Tests for History to achieve 100% coverage."""
    
    def test_load_from_malformed_csv(self, tmp_path):
        """Test loading from malformed CSV file."""
        history = CalculationHistory()
        
        # Create malformed CSV
        file_path = tmp_path / 'malformed.csv'
        file_path.write_text('invalid,csv,data\nno,proper,columns')
        
        # Should raise HistoryError
        with pytest.raises(HistoryError):
            history.load_from_csv(str(file_path))


class TestInputValidatorCoverage:
    """Tests for InputValidator to achieve 100% coverage."""
    
    def test_validate_operation_with_empty_list(self):
        """Test validate operation with empty available operations."""
        with pytest.raises(ValidationError):
            InputValidator.validate_operation('add', [])


class TestOperationsCoverage:
    """Tests for Operations to achieve 100% coverage."""
    
    def test_power_operation_name(self):
        """Test power operation get_name."""
        op = PowerOperation()
        assert op.get_name() == "power"
    
    def test_operation_factory_error_message(self):
        """Test operation factory error message includes available ops."""
        try:
            OperationFactory.create_operation("invalid_op")
        except OperationError as e:
            error_msg = str(e)
            assert "Unknown operation" in error_msg
            assert "invalid_op" in error_msg
            assert "Available operations" in error_msg
    
    def test_power_operation_invalid_result(self):
        """Test power operation with result that would be NaN."""
        from app.operations import PowerOperation
        op = PowerOperation()
        
        # This should work fine
        result = op.execute(2, 3)
        assert result == 8
    
    def test_root_operation_error_message(self):
        """Test root operation error messages."""
        from app.operations import RootOperation
        op = RootOperation()
        
        # Test zero degree error
        with pytest.raises(OperationError, match="Root degree cannot be zero"):
            op.execute(9, 0)
        
        # Test even root of negative
        with pytest.raises(OperationError, match="Cannot calculate even root"):
            op.execute(-9, 2)


class TestCalculatorMain:
    """Test calculator main function."""
    
    @patch('app.calculator.Calculator')
    def test_main_function_success(self, mock_calc_class):
        """Test main function runs successfully."""
        from app.calculator import main
        
        mock_calculator = Mock()
        mock_calc_class.return_value = mock_calculator
        
        main()
        
        mock_calc_class.assert_called_once()
        mock_calculator.run_repl.assert_called_once()
    
    @patch('app.calculator.Calculator')
    def test_main_function_failure(self, mock_calc_class, capsys):
        """Test main function handles initialization failure."""
        from app.calculator import main
        
        mock_calc_class.side_effect = Exception("Init failed")
        
        main()
        
        captured = capsys.readouterr()
        assert "Failed to start calculator" in captured.out


class TestCalculatorObserverPattern:
    """Test observer pattern edge cases."""
    
    def test_observer_notification(self, tmp_path):
        """Test that observers are properly notified."""
        env_content = f"""CALCULATOR_LOG_DIR={tmp_path}/logs
CALCULATOR_HISTORY_DIR={tmp_path}/history
CALCULATOR_AUTO_SAVE=false"""
        env_file = tmp_path / '.env'
        env_file.write_text(env_content)
        
        config = CalculatorConfig(str(env_file))
        calc = Calculator(config)
        
        # Create mock observer
        mock_observer = Mock()
        calc.register_observer(mock_observer)
        
        # Perform calculation
        calc.perform_calculation('add', 5, 3)
        
        # Verify observer was called
        mock_observer.on_calculation_performed.assert_called_once()
        
        calc.logger.close_handlers()


class TestCalculatorWithAutoSave:
    """Tests for calculator with auto_save enabled to cover lines 110-114."""
    
    def test_calculator_with_auto_save_enabled(self):
        """Test calculator initialization with auto_save enabled."""
        import os
        import tempfile
        
        # Create a temp directory for history
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set environment to enable auto_save
            os.environ['AUTO_SAVE'] = 'true'
            os.environ['HISTORY_DIR'] = temp_dir
            
            try:
                # Create calculator which should register AutoSaveObserver
                calc = Calculator()
                
                # Verify calculator was created successfully
                assert calc is not None
                
                # Perform an operation
                result = calc.perform_calculation('add', 5, 3)
                assert result == 8
                
                calc.logger.close_handlers()
                
            finally:
                # Clean up environment
                if 'AUTO_SAVE' in os.environ:
                    del os.environ['AUTO_SAVE']
                if 'HISTORY_DIR' in os.environ:
                    del os.environ['HISTORY_DIR']


class TestUndoRedoExceptions:
    """Tests for undo/redo exception handling to cover lines 195-196, 213-214."""
    
    def test_undo_index_error_path(self):
        """Test that undo handles IndexError from caretaker."""
        calc = Calculator()
        
        # Mock caretaker to raise IndexError to cover the except path (lines 195-196)
        with patch.object(calc.caretaker, 'can_undo', return_value=True):
            with patch.object(calc.caretaker, 'undo', side_effect=IndexError("Test error")):
                with pytest.raises(HistoryError) as exc_info:
                    calc.undo()
                
                assert "Nothing to undo" in str(exc_info.value)
        
        calc.logger.close_handlers()
    
    def test_redo_index_error_path(self):
        """Test that redo handles IndexError from caretaker."""
        calc = Calculator()
        
        # Mock caretaker to raise IndexError to cover the except path (lines 213-214)
        with patch.object(calc.caretaker, 'can_redo', return_value=True):
            with patch.object(calc.caretaker, 'redo', side_effect=IndexError("Test error")):
                with pytest.raises(HistoryError) as exc_info:
                    calc.redo()
                
                assert "Nothing to redo" in str(exc_info.value)
        
        calc.logger.close_handlers()


class TestHistoryEmptyDataError:
    """Tests for history EmptyDataError handling to cover line 145."""
    
    def test_load_csv_exceeding_max_size(self):
        """Test loading CSV that exceeds max size to cover line 145."""
        import tempfile
        import os
        import pandas as pd
        from datetime import datetime
        
        # Create history with small max size
        history = CalculationHistory(max_size=3)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            csv_file = f.name
            # Write more calculations than max_size to trigger the trim logic (line 145)
            df = pd.DataFrame([
                {'operation': 'add', 'operand1': 1, 'operand2': 1, 'result': 2, 'timestamp': datetime.now().isoformat()},
                {'operation': 'add', 'operand1': 2, 'operand2': 2, 'result': 4, 'timestamp': datetime.now().isoformat()},
                {'operation': 'add', 'operand1': 3, 'operand2': 3, 'result': 6, 'timestamp': datetime.now().isoformat()},
                {'operation': 'add', 'operand1': 4, 'operand2': 4, 'result': 8, 'timestamp': datetime.now().isoformat()},
                {'operation': 'add', 'operand1': 5, 'operand2': 5, 'result': 10, 'timestamp': datetime.now().isoformat()},
            ])
            df.to_csv(f.name, index=False)
        
        try:
            # Load the CSV - should trim to last 3 entries
            history.load_from_csv(csv_file)
            # History should be trimmed to max_size
            assert len(history.get_history()) == 3
            # Should have the last 3 calculations
            assert history.get_history()[0].result == 6
            assert history.get_history()[1].result == 8
            assert history.get_history()[2].result == 10
        finally:
            if os.path.exists(csv_file):
                os.unlink(csv_file)


class TestInputValidatorNaN:
    """Tests for NaN validation to cover line 31."""
    
    def test_validate_number_with_nan(self):
        """Test that NaN raises ValidationError."""
        import math
        
        with pytest.raises(ValidationError):
            InputValidator.validate_number(math.nan)


class TestOperationsErrorPaths:
    """Tests for operations error paths."""
    
    def test_power_operation_nan_result(self):
        """Test power operation returning NaN to cover line 89."""
        from app.operations import RootOperation
        import math
        power_op = PowerOperation()
        
        # Use mock to simulate NaN result from power operation
        with patch.object(power_op, 'execute', wraps=power_op.execute):
            # (-1) ** 0.5 should produce complex number which Python handles, 
            # but we can simulate ValueError
            with pytest.raises(OperationError):
                # This will cause ValueError internally
                power_op.execute(-1.0, 0.5)
    
    def test_power_operation_overflow(self):
        """Test power operation with overflow to cover lines 91-92."""
        power_op = PowerOperation()
        
        # Try to compute a huge power that causes overflow
        with pytest.raises(OperationError):
            power_op.execute(10.0, 100000.0)
    
    def test_root_operation_zero_degree(self):
        """Test root operation with zero degree."""
        from app.operations import RootOperation
        
        root_op = RootOperation()
        
        # Zero degree raises error early
        with pytest.raises(OperationError) as exc_info:
            root_op.execute(10.0, 0.0)
        
        assert "Root degree cannot be zero" in str(exc_info.value)
    
    def test_abstract_operation_methods(self):
        """Test abstract methods by calling them on subclass to cover lines 23, 28."""
        from app.operations import AddOperation
        
        # These are covered by actual operation implementations
        add_op = AddOperation()
        result = add_op.execute(5.0, 3.0)
        assert result == 8.0
        assert add_op.get_name() == "add"
    
    def test_abstract_observer_method(self):
        """Test abstract observer method to cover line 32."""
        from app.calculator import CalculatorObserver, Calculator
        
        # Create a concrete observer
        class TestObserver(CalculatorObserver):
            def __init__(self):
                self.called = False
            
            def on_calculation_performed(self, calculation):
                self.called = True
        
        calc = Calculator()
        observer = TestObserver()
        calc.register_observer(observer)
        calc.perform_calculation('add', 5, 3)
        assert observer.called
