"""Logging configuration and utilities for the calculator application."""

import logging
import os
from datetime import datetime


class Logger:
    """Manages logging for the calculator application."""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Implement singleton pattern for Logger."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logger if not already initialized."""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """Set up the logger with file and console handlers."""
        self._logger = logging.getLogger('calculator')
        self._logger.setLevel(logging.INFO)
        
        # Avoid adding handlers multiple times
        if not self._logger.handlers:
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)
    
    def configure_file_handler(self, log_dir: str, log_file: str = None):
        """
        Configure file handler for logging.
        
        Args:
            log_dir: Directory for log files.
            log_file: Name of the log file (optional).
        """
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Generate log filename if not provided
        if log_file is None:
            timestamp = datetime.now().strftime('%Y%m%d')
            log_file = f'calculator_{timestamp}.log'
        
        log_path = os.path.join(log_dir, log_file)
        
        # Remove existing file handlers and close them
        for handler in self._logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()
                self._logger.removeHandler(handler)
        
        # Add file handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
    
    def info(self, message: str):
        """Log an info message."""
        self._logger.info(message)
    
    def warning(self, message: str):
        """Log a warning message."""
        self._logger.warning(message)
    
    def error(self, message: str):
        """Log an error message."""
        self._logger.error(message)
    
    def debug(self, message: str):
        """Log a debug message."""
        self._logger.debug(message)
    
    def close_handlers(self):
        """Close all file handlers."""
        for handler in self._logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()
                self._logger.removeHandler(handler)
