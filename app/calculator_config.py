"""Configuration management for the calculator application."""

import os
from typing import Any
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages configuration settings for the calculator."""
    
    # Default configuration values
    DEFAULTS = {
        'CALCULATOR_LOG_DIR': 'logs',
        'CALCULATOR_HISTORY_DIR': 'history',
        'CALCULATOR_MAX_HISTORY_SIZE': 100,
        'CALCULATOR_AUTO_SAVE': 'true',
        'CALCULATOR_PRECISION': 2,
        'CALCULATOR_MAX_INPUT_VALUE': 1e10,
        'CALCULATOR_DEFAULT_ENCODING': 'utf-8',
    }
    
    def __init__(self, env_file: str = '.env'):
        """
        Initialize configuration.
        
        Args:
            env_file: Path to the .env file.
        """
        # Load environment variables from .env file
        # Override=True to prioritize the env file over system environment
        load_dotenv(env_file, override=True)
        
        self._config = {}
        self._load_config()
        self._validate_config()
    
    def _load_config(self):
        """Load configuration from environment variables with defaults."""
        for key, default_value in self.DEFAULTS.items():
            value = os.getenv(key, default_value)
            self._config[key] = value
    
    def _validate_config(self):
        """Validate and convert configuration values to appropriate types."""
        try:
            # Convert numeric values
            self._config['CALCULATOR_MAX_HISTORY_SIZE'] = int(
                self._config['CALCULATOR_MAX_HISTORY_SIZE']
            )
            self._config['CALCULATOR_PRECISION'] = int(
                self._config['CALCULATOR_PRECISION']
            )
            self._config['CALCULATOR_MAX_INPUT_VALUE'] = float(
                self._config['CALCULATOR_MAX_INPUT_VALUE']
            )
            
            # Convert boolean value
            self._config['CALCULATOR_AUTO_SAVE'] = (
                self._config['CALCULATOR_AUTO_SAVE'].lower() == 'true'
            )
            
            # Validate ranges
            if self._config['CALCULATOR_MAX_HISTORY_SIZE'] < 1:
                raise ConfigurationError(
                    "CALCULATOR_MAX_HISTORY_SIZE must be at least 1"
                )
            
            if self._config['CALCULATOR_PRECISION'] < 0:
                raise ConfigurationError(
                    "CALCULATOR_PRECISION must be non-negative"
                )
            
            if self._config['CALCULATOR_MAX_INPUT_VALUE'] <= 0:
                raise ConfigurationError(
                    "CALCULATOR_MAX_INPUT_VALUE must be positive"
                )
            
        except (ValueError, AttributeError) as e:
            raise ConfigurationError(f"Invalid configuration value: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key.
            default: Default value if key not found.
            
        Returns:
            The configuration value.
        """
        return self._config.get(key, default)
    
    @property
    def log_dir(self) -> str:
        """Get the log directory path."""
        return self._config['CALCULATOR_LOG_DIR']
    
    @property
    def history_dir(self) -> str:
        """Get the history directory path."""
        return self._config['CALCULATOR_HISTORY_DIR']
    
    @property
    def max_history_size(self) -> int:
        """Get the maximum history size."""
        return self._config['CALCULATOR_MAX_HISTORY_SIZE']
    
    @property
    def auto_save(self) -> bool:
        """Get the auto-save setting."""
        return self._config['CALCULATOR_AUTO_SAVE']
    
    @property
    def precision(self) -> int:
        """Get the calculation precision."""
        return self._config['CALCULATOR_PRECISION']
    
    @property
    def max_input_value(self) -> float:
        """Get the maximum input value."""
        return self._config['CALCULATOR_MAX_INPUT_VALUE']
    
    @property
    def default_encoding(self) -> str:
        """Get the default encoding."""
        return self._config['CALCULATOR_DEFAULT_ENCODING']
