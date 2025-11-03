"""Memento pattern implementation for calculator state management."""

from typing import List
from app.calculation import Calculation


class CalculatorMemento:
    """Stores the state of the calculator for undo/redo functionality."""
    
    def __init__(self, history: List[Calculation]):
        """
        Initialize memento with calculator history.
        
        Args:
            history: List of calculations to save.
        """
        # Create a deep copy of the history
        self._history = [calc for calc in history]
    
    def get_history(self) -> List[Calculation]:
        """
        Get the saved history.
        
        Returns:
            List of calculations.
        """
        return [calc for calc in self._history]


class CalculatorCaretaker:
    """Manages mementos for undo/redo operations."""
    
    def __init__(self):
        """Initialize the caretaker with empty undo and redo stacks."""
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []
    
    def save_state(self, memento: CalculatorMemento):
        """
        Save a memento to the undo stack.
        
        Args:
            memento: The memento to save.
        """
        self._undo_stack.append(memento)
        # Clear redo stack when a new state is saved
        self._redo_stack.clear()
    
    def undo(self) -> CalculatorMemento:
        """
        Get the previous state for undo operation.
        
        Returns:
            The previous memento.
            
        Raises:
            IndexError: If there's nothing to undo.
        """
        if not self._undo_stack:
            raise IndexError("Nothing to undo")
        
        # Pop the current state and move it to redo stack
        memento = self._undo_stack.pop()
        self._redo_stack.append(memento)
        
        # Return the previous state if it exists
        if self._undo_stack:
            return self._undo_stack[-1]
        else:
            # Return an empty state if no more undo history
            return CalculatorMemento([])
    
    def redo(self) -> CalculatorMemento:
        """
        Get the next state for redo operation.
        
        Returns:
            The next memento.
            
        Raises:
            IndexError: If there's nothing to redo.
        """
        if not self._redo_stack:
            raise IndexError("Nothing to redo")
        
        # Pop from redo stack and restore it to undo stack
        memento = self._redo_stack.pop()
        self._undo_stack.append(memento)
        
        return memento
    
    def can_undo(self) -> bool:
        """
        Check if undo is possible.
        
        Returns:
            True if undo is possible, False otherwise.
        """
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        """
        Check if redo is possible.
        
        Returns:
            True if redo is possible, False otherwise.
        """
        return len(self._redo_stack) > 0
    
    def clear(self):
        """Clear all undo and redo stacks."""
        self._undo_stack.clear()
        self._redo_stack.clear()
