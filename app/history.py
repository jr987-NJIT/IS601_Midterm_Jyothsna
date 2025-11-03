"""History management with pandas integration for CSV operations."""

import os
from typing import List
import pandas as pd
from app.calculation import Calculation
from app.exceptions import HistoryError


class CalculationHistory:
    """Manages calculation history with file persistence using pandas."""
    
    def __init__(self, max_size: int = 100):
        """
        Initialize calculation history.
        
        Args:
            max_size: Maximum number of calculations to store.
        """
        self._history: List[Calculation] = []
        self._max_size = max_size
    
    def add_calculation(self, calculation: Calculation):
        """
        Add a calculation to history.
        
        Args:
            calculation: The calculation to add.
        """
        self._history.append(calculation)
        
        # Trim history if it exceeds max size
        if len(self._history) > self._max_size:
            self._history = self._history[-self._max_size:]
    
    def get_history(self) -> List[Calculation]:
        """
        Get all calculations in history.
        
        Returns:
            List of calculations.
        """
        return self._history.copy()
    
    def clear_history(self):
        """Clear all history."""
        self._history.clear()
    
    def get_last_calculation(self) -> Calculation:
        """
        Get the most recent calculation.
        
        Returns:
            The last calculation.
            
        Raises:
            HistoryError: If history is empty.
        """
        if not self._history:
            raise HistoryError("History is empty")
        return self._history[-1]
    
    def remove_last_calculation(self):
        """
        Remove the most recent calculation.
        
        Raises:
            HistoryError: If history is empty.
        """
        if not self._history:
            raise HistoryError("History is empty")
        self._history.pop()
    
    def set_history(self, history: List[Calculation]):
        """
        Replace current history with a new list.
        
        Args:
            history: New history list.
        """
        self._history = history.copy()
        
        # Trim if necessary
        if len(self._history) > self._max_size:
            self._history = self._history[-self._max_size:]
    
    def save_to_csv(self, file_path: str, encoding: str = 'utf-8'):
        """
        Save history to a CSV file using pandas.
        
        Args:
            file_path: Path to the CSV file.
            encoding: File encoding.
            
        Raises:
            HistoryError: If saving fails.
        """
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            # Convert calculations to list of dictionaries
            data = [calc.to_dict() for calc in self._history]
            
            # Create DataFrame and save to CSV
            if data:
                df = pd.DataFrame(data)
                df.to_csv(file_path, index=False, encoding=encoding)
            else:
                # Create empty CSV with headers
                df = pd.DataFrame(columns=['operation', 'operand1', 'operand2', 'result', 'timestamp'])
                df.to_csv(file_path, index=False, encoding=encoding)
                
        except Exception as e:  # pragma: no cover
            raise HistoryError(f"Failed to save history to CSV: {e}")  # pragma: no cover
    
    def load_from_csv(self, file_path: str, encoding: str = 'utf-8'):
        """
        Load history from a CSV file using pandas.
        
        Args:
            file_path: Path to the CSV file.
            encoding: File encoding.
            
        Raises:
            HistoryError: If loading fails.
        """
        try:
            if not os.path.exists(file_path):
                raise HistoryError(f"History file not found: {file_path}")
            
            # Read CSV using pandas
            df = pd.read_csv(file_path, encoding=encoding)
            
            # Convert DataFrame to list of Calculation objects
            self._history.clear()
            for _, row in df.iterrows():
                calc = Calculation.from_dict(row.to_dict())
                self._history.append(calc)
            
            # Trim if necessary
            if len(self._history) > self._max_size:
                self._history = self._history[-self._max_size:]
                
        except pd.errors.EmptyDataError:
            # Empty CSV file
            self._history.clear()
        except Exception as e:
            raise HistoryError(f"Failed to load history from CSV: {e}")
    
    def __len__(self) -> int:
        """Get the number of calculations in history."""
        return len(self._history)
    
    def __str__(self) -> str:
        """Return string representation of history."""
        if not self._history:
            return "No calculations in history"
        
        lines = ["Calculation History:"]
        for i, calc in enumerate(self._history, 1):
            lines.append(f"{i}. {calc}")
        
        return "\n".join(lines)
