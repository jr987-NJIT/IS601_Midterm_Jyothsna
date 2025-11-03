"""Unit tests for configuration management."""

import pytest
import os
import tempfile
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


class TestCalculatorConfig:
    """Tests for CalculatorConfig class."""
    
    @pytest.fixture
    def temp_env_file(self):
        """Create a temporary .env file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("""CALCULATOR_LOG_DIR=test_logs
CALCULATOR_HISTORY_DIR=test_history
CALCULATOR_MAX_HISTORY_SIZE=50
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=3
CALCULATOR_MAX_INPUT_VALUE=5000
CALCULATOR_DEFAULT_ENCODING=utf-8""")
            temp_file = f.name
        
        yield temp_file
        
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    def test_config_load_from_env(self, temp_env_file):
        """Test loading configuration from .env file."""
        config = CalculatorConfig(temp_env_file)
        
        assert config.log_dir == 'test_logs'
        assert config.history_dir == 'test_history'
        assert config.max_history_size == 50
        assert config.auto_save is True
        assert config.precision == 3
        assert config.max_input_value == 5000
        assert config.default_encoding == 'utf-8'
    
    def test_config_defaults(self):
        """Test configuration uses defaults when env file missing."""
        # Clear environment vars
        env_backup = {}
        for key in ['CALCULATOR_LOG_DIR', 'CALCULATOR_HISTORY_DIR', 'CALCULATOR_MAX_HISTORY_SIZE',
                    'CALCULATOR_AUTO_SAVE', 'CALCULATOR_PRECISION', 'CALCULATOR_MAX_INPUT_VALUE',
                    'CALCULATOR_DEFAULT_ENCODING']:
            if key in os.environ:
                env_backup[key] = os.environ[key]
                del os.environ[key]
        
        try:
            config = CalculatorConfig('nonexistent.env')
            
            assert config.log_dir == 'logs'
            assert config.history_dir == 'history'
            assert config.max_history_size == 100
            assert config.auto_save is True
            assert config.precision == 2
            assert config.max_input_value == 1e10
            assert config.default_encoding == 'utf-8'
        finally:
            # Restore environment
            for key, value in env_backup.items():
                os.environ[key] = value
    
    def test_config_get_method(self, temp_env_file):
        """Test get method."""
        config = CalculatorConfig(temp_env_file)
        
        assert config.get('CALCULATOR_LOG_DIR') == 'test_logs'
        assert config.get('NONEXISTENT_KEY', 'default') == 'default'
    
    def test_config_invalid_history_size(self):
        """Test invalid history size raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("CALCULATOR_MAX_HISTORY_SIZE=0\n")
            temp_file = f.name
        
        try:
            with pytest.raises(ConfigurationError, match="must be at least 1"):
                CalculatorConfig(temp_file)
        finally:
            os.remove(temp_file)
    
    def test_config_invalid_precision(self):
        """Test invalid precision raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("""CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=-1
CALCULATOR_MAX_INPUT_VALUE=10000000000
CALCULATOR_DEFAULT_ENCODING=utf-8""")
            temp_file = f.name
        
        try:
            with pytest.raises(ConfigurationError, match="must be non-negative"):
                CalculatorConfig(temp_file)
        finally:
            os.remove(temp_file)
    
    def test_config_invalid_max_input_value(self):
        """Test invalid max input value raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("""CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=-100
CALCULATOR_DEFAULT_ENCODING=utf-8""")
            temp_file = f.name
        
        try:
            with pytest.raises(ConfigurationError, match="must be positive"):
                CalculatorConfig(temp_file)
        finally:
            os.remove(temp_file)
    
    def test_config_auto_save_false(self):
        """Test auto_save set to false."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("""CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=false
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=10000000000
CALCULATOR_DEFAULT_ENCODING=utf-8""")
            temp_file = f.name
        
        try:
            config = CalculatorConfig(temp_file)
            assert config.auto_save is False
        finally:
            os.remove(temp_file)
    
    def test_config_invalid_type(self):
        """Test invalid type in config raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("""CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=abc
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=10000000000
CALCULATOR_DEFAULT_ENCODING=utf-8""")
            temp_file = f.name
        
        try:
            with pytest.raises(ConfigurationError, match="Invalid configuration value"):
                CalculatorConfig(temp_file)
        finally:
            os.remove(temp_file)
