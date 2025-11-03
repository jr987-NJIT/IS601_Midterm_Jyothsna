"""Unit tests for calculator memento pattern."""

import pytest
from app.calculator_memento import CalculatorMemento, CalculatorCaretaker
from app.calculation import Calculation


class TestCalculatorMemento:
    """Tests for CalculatorMemento class."""
    
    def test_memento_creation(self):
        """Test creating a memento."""
        calc1 = Calculation("add", 5, 3, 8)
        calc2 = Calculation("subtract", 10, 2, 8)
        history = [calc1, calc2]
        
        memento = CalculatorMemento(history)
        saved_history = memento.get_history()
        
        assert len(saved_history) == 2
        assert saved_history[0] == calc1
        assert saved_history[1] == calc2
    
    def test_memento_creates_copy(self):
        """Test memento creates a copy of history."""
        calc = Calculation("add", 5, 3, 8)
        history = [calc]
        
        memento = CalculatorMemento(history)
        
        # Modify original history
        history.clear()
        
        # Memento should still have the calculation
        saved_history = memento.get_history()
        assert len(saved_history) == 1
    
    def test_memento_empty_history(self):
        """Test memento with empty history."""
        memento = CalculatorMemento([])
        assert len(memento.get_history()) == 0


class TestCalculatorCaretaker:
    """Tests for CalculatorCaretaker class."""
    
    def test_caretaker_initialization(self):
        """Test caretaker initializes correctly."""
        caretaker = CalculatorCaretaker()
        assert caretaker.can_undo() is False
        assert caretaker.can_redo() is False
    
    def test_save_state(self):
        """Test saving state."""
        caretaker = CalculatorCaretaker()
        calc = Calculation("add", 5, 3, 8)
        memento = CalculatorMemento([calc])
        
        caretaker.save_state(memento)
        assert caretaker.can_undo() is True
    
    def test_undo(self):
        """Test undo operation."""
        caretaker = CalculatorCaretaker()
        
        # Save first state
        calc1 = Calculation("add", 5, 3, 8)
        memento1 = CalculatorMemento([calc1])
        caretaker.save_state(memento1)
        
        # Save second state
        calc2 = Calculation("subtract", 10, 2, 8)
        memento2 = CalculatorMemento([calc1, calc2])
        caretaker.save_state(memento2)
        
        # Undo should return first state
        previous = caretaker.undo()
        assert len(previous.get_history()) == 1
        assert caretaker.can_redo() is True
    
    def test_undo_empty_stack(self):
        """Test undo with empty stack raises error."""
        caretaker = CalculatorCaretaker()
        
        with pytest.raises(IndexError, match="Nothing to undo"):
            caretaker.undo()
    
    def test_undo_to_empty_state(self):
        """Test undo to empty initial state."""
        caretaker = CalculatorCaretaker()
        
        calc = Calculation("add", 5, 3, 8)
        memento = CalculatorMemento([calc])
        caretaker.save_state(memento)
        
        # Undo when only one state exists
        previous = caretaker.undo()
        assert len(previous.get_history()) == 0
    
    def test_redo(self):
        """Test redo operation."""
        caretaker = CalculatorCaretaker()
        
        calc1 = Calculation("add", 5, 3, 8)
        memento1 = CalculatorMemento([calc1])
        caretaker.save_state(memento1)
        
        calc2 = Calculation("subtract", 10, 2, 8)
        memento2 = CalculatorMemento([calc1, calc2])
        caretaker.save_state(memento2)
        
        # Undo then redo
        caretaker.undo()
        restored = caretaker.redo()
        
        assert len(restored.get_history()) == 2
    
    def test_redo_empty_stack(self):
        """Test redo with empty stack raises error."""
        caretaker = CalculatorCaretaker()
        
        with pytest.raises(IndexError, match="Nothing to redo"):
            caretaker.redo()
    
    def test_save_clears_redo_stack(self):
        """Test saving new state clears redo stack."""
        caretaker = CalculatorCaretaker()
        
        calc1 = Calculation("add", 5, 3, 8)
        memento1 = CalculatorMemento([calc1])
        caretaker.save_state(memento1)
        
        calc2 = Calculation("subtract", 10, 2, 8)
        memento2 = CalculatorMemento([calc1, calc2])
        caretaker.save_state(memento2)
        
        # Undo to populate redo stack
        caretaker.undo()
        assert caretaker.can_redo() is True
        
        # Save new state should clear redo
        calc3 = Calculation("multiply", 3, 4, 12)
        memento3 = CalculatorMemento([calc1, calc3])
        caretaker.save_state(memento3)
        
        assert caretaker.can_redo() is False
    
    def test_can_undo(self):
        """Test can_undo method."""
        caretaker = CalculatorCaretaker()
        assert caretaker.can_undo() is False
        
        memento = CalculatorMemento([Calculation("add", 5, 3, 8)])
        caretaker.save_state(memento)
        assert caretaker.can_undo() is True
    
    def test_can_redo(self):
        """Test can_redo method."""
        caretaker = CalculatorCaretaker()
        assert caretaker.can_redo() is False
        
        memento = CalculatorMemento([Calculation("add", 5, 3, 8)])
        caretaker.save_state(memento)
        caretaker.undo()
        
        assert caretaker.can_redo() is True
    
    def test_clear(self):
        """Test clearing undo/redo stacks."""
        caretaker = CalculatorCaretaker()
        
        memento1 = CalculatorMemento([Calculation("add", 5, 3, 8)])
        caretaker.save_state(memento1)
        caretaker.undo()
        
        assert caretaker.can_undo() is False
        assert caretaker.can_redo() is True
        
        caretaker.clear()
        
        assert caretaker.can_undo() is False
        assert caretaker.can_redo() is False
    
    def test_multiple_undo_redo(self):
        """Test multiple undo and redo operations."""
        caretaker = CalculatorCaretaker()
        
        # Save multiple states
        for i in range(5):
            calcs = [Calculation("add", i, i, i*2) for _ in range(i+1)]
            memento = CalculatorMemento(calcs)
            caretaker.save_state(memento)
        
        # Undo multiple times
        caretaker.undo()
        caretaker.undo()
        state = caretaker.undo()
        assert len(state.get_history()) == 2
        
        # Redo
        state = caretaker.redo()
        assert len(state.get_history()) == 3
