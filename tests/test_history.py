"""Unit tests for history management."""

import pytest
import os
import tempfile
import pandas as pd
from app.history import CalculationHistory
from app.calculation import Calculation
from app.exceptions import HistoryError


class TestCalculationHistory:
    """Tests for CalculationHistory class."""
    
    def test_history_initialization(self):
        """Test history initializes correctly."""
        history = CalculationHistory(max_size=10)
        assert len(history) == 0
    
    def test_add_calculation(self):
        """Test adding calculation to history."""
        history = CalculationHistory()
        calc = Calculation("add", 5, 3, 8)
        history.add_calculation(calc)
        
        assert len(history) == 1
        assert history.get_history()[0] == calc
    
    def test_add_multiple_calculations(self):
        """Test adding multiple calculations."""
        history = CalculationHistory()
        calc1 = Calculation("add", 5, 3, 8)
        calc2 = Calculation("subtract", 10, 2, 8)
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        
        assert len(history) == 2
    
    def test_max_size_limit(self):
        """Test history respects max size limit."""
        history = CalculationHistory(max_size=3)
        
        for i in range(5):
            calc = Calculation("add", i, i, i*2)
            history.add_calculation(calc)
        
        assert len(history) == 3
        # Should keep the most recent 3
        assert history.get_history()[0].operand1 == 2
    
    def test_get_history(self):
        """Test getting history returns a copy."""
        history = CalculationHistory()
        calc = Calculation("add", 5, 3, 8)
        history.add_calculation(calc)
        
        history_list = history.get_history()
        assert len(history_list) == 1
        
        # Modifying the returned list shouldn't affect original
        history_list.clear()
        assert len(history) == 1
    
    def test_clear_history(self):
        """Test clearing history."""
        history = CalculationHistory()
        history.add_calculation(Calculation("add", 5, 3, 8))
        history.add_calculation(Calculation("subtract", 10, 2, 8))
        
        history.clear_history()
        assert len(history) == 0
    
    def test_get_last_calculation(self):
        """Test getting last calculation."""
        history = CalculationHistory()
        calc1 = Calculation("add", 5, 3, 8)
        calc2 = Calculation("subtract", 10, 2, 8)
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        
        last = history.get_last_calculation()
        assert last == calc2
    
    def test_get_last_calculation_empty_history(self):
        """Test getting last calculation from empty history raises error."""
        history = CalculationHistory()
        
        with pytest.raises(HistoryError, match="History is empty"):
            history.get_last_calculation()
    
    def test_remove_last_calculation(self):
        """Test removing last calculation."""
        history = CalculationHistory()
        calc1 = Calculation("add", 5, 3, 8)
        calc2 = Calculation("subtract", 10, 2, 8)
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        
        history.remove_last_calculation()
        assert len(history) == 1
        assert history.get_last_calculation() == calc1
    
    def test_remove_last_calculation_empty_history(self):
        """Test removing from empty history raises error."""
        history = CalculationHistory()
        
        with pytest.raises(HistoryError, match="History is empty"):
            history.remove_last_calculation()
    
    def test_set_history(self):
        """Test setting entire history."""
        history = CalculationHistory()
        calc1 = Calculation("add", 5, 3, 8)
        calc2 = Calculation("subtract", 10, 2, 8)
        
        new_history = [calc1, calc2]
        history.set_history(new_history)
        
        assert len(history) == 2
    
    def test_set_history_with_trim(self):
        """Test setting history that exceeds max size."""
        history = CalculationHistory(max_size=2)
        calcs = [
            Calculation("add", i, i, i*2)
            for i in range(5)
        ]
        
        history.set_history(calcs)
        assert len(history) == 2
    
    def test_save_to_csv(self):
        """Test saving history to CSV."""
        history = CalculationHistory()
        calc1 = Calculation("add", 5, 3, 8)
        calc2 = Calculation("subtract", 10, 2, 8)
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'history.csv')
            history.save_to_csv(file_path)
            
            assert os.path.exists(file_path)
            
            # Verify CSV contents
            df = pd.read_csv(file_path)
            assert len(df) == 2
            assert 'operation' in df.columns
            assert 'operand1' in df.columns
            assert 'result' in df.columns
    
    def test_save_empty_history_to_csv(self):
        """Test saving empty history to CSV."""
        history = CalculationHistory()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'history.csv')
            history.save_to_csv(file_path)
            
            assert os.path.exists(file_path)
            df = pd.read_csv(file_path)
            assert len(df) == 0
    
    def test_load_from_csv(self):
        """Test loading history from CSV."""
        history = CalculationHistory()
        calc1 = Calculation("add", 5, 3, 8)
        calc2 = Calculation("multiply", 4, 2, 8)
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'history.csv')
            history.save_to_csv(file_path)
            
            # Load into new history
            new_history = CalculationHistory()
            new_history.load_from_csv(file_path)
            
            assert len(new_history) == 2
            loaded = new_history.get_history()
            assert loaded[0].operation == "add"
            assert loaded[1].operation == "multiply"
    
    def test_load_from_nonexistent_file(self):
        """Test loading from non-existent file raises error."""
        history = CalculationHistory()
        
        with pytest.raises(HistoryError, match="History file not found"):
            history.load_from_csv("nonexistent.csv")
    
    def test_load_from_empty_csv(self):
        """Test loading from empty CSV file."""
        history = CalculationHistory()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'empty.csv')
            # Create empty CSV
            with open(file_path, 'w') as f:
                f.write('')
            
            history.load_from_csv(file_path)
            assert len(history) == 0
    
    def test_str_representation_empty(self):
        """Test string representation of empty history."""
        history = CalculationHistory()
        assert "No calculations" in str(history)
    
    def test_str_representation_with_calculations(self):
        """Test string representation with calculations."""
        history = CalculationHistory()
        history.add_calculation(Calculation("add", 5, 3, 8))
        
        string_repr = str(history)
        assert "Calculation History" in string_repr
        assert "1." in string_repr
