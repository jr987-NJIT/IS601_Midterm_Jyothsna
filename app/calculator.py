"""Main calculator module with Observer pattern and REPL interface."""

import os
from abc import ABC, abstractmethod
from typing import List
from colorama import init, Fore, Style

from app.calculation import Calculation
from app.operations import OperationFactory
from app.history import CalculationHistory
from app.calculator_memento import CalculatorMemento, CalculatorCaretaker
from app.calculator_config import CalculatorConfig
from app.logger import Logger
from app.input_validators import InputValidator
from app.exceptions import OperationError, ValidationError, HistoryError

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)


class CalculatorObserver(ABC):
    """Abstract observer for calculator events."""
    
    @abstractmethod
    def on_calculation_performed(self, calculation: Calculation):
        """
        Called when a calculation is performed.
        
        Args:
            calculation: The calculation that was performed.
        """
        pass  # pragma: no cover


class LoggingObserver(CalculatorObserver):
    """Observer that logs calculations."""
    
    def __init__(self, logger: Logger):
        """
        Initialize logging observer.
        
        Args:
            logger: Logger instance.
        """
        self.logger = logger
    
    def on_calculation_performed(self, calculation: Calculation):
        """Log the calculation."""
        message = (
            f"Calculation performed: {calculation.operation} "
            f"({calculation.operand1}, {calculation.operand2}) = {calculation.result}"
        )
        self.logger.info(message)


class AutoSaveObserver(CalculatorObserver):
    """Observer that automatically saves history to CSV."""
    
    def __init__(self, history: CalculationHistory, file_path: str, encoding: str = 'utf-8'):
        """
        Initialize auto-save observer.
        
        Args:
            history: Calculation history instance.
            file_path: Path to save the CSV file.
            encoding: File encoding.
        """
        self.history = history
        self.file_path = file_path
        self.encoding = encoding
    
    def on_calculation_performed(self, calculation: Calculation):
        """Auto-save history to CSV."""
        try:
            self.history.save_to_csv(self.file_path, self.encoding)
        except Exception as e:
            print(f"{Fore.RED}Failed to auto-save history: {e}")


class Calculator:
    """Advanced calculator with REPL interface."""
    
    def __init__(self, config: CalculatorConfig = None):
        """
        Initialize calculator.
        
        Args:
            config: Configuration instance (optional).
        """
        # Load configuration
        self.config = config or CalculatorConfig()
        
        # Initialize components
        self.logger = Logger()
        self.logger.configure_file_handler(self.config.log_dir)
        
        self.history = CalculationHistory(self.config.max_history_size)
        self.caretaker = CalculatorCaretaker()
        
        # Initialize with empty state for undo/redo
        self.caretaker.save_state(CalculatorMemento(self.history.get_history()))
        
        # Initialize observers
        self.observers: List[CalculatorObserver] = []
        
        # Register default observers
        self.register_observer(LoggingObserver(self.logger))
        
        if self.config.auto_save:
            history_file = os.path.join(
                self.config.history_dir,
                'calculator_history.csv'
            )
            self.register_observer(
                AutoSaveObserver(self.history, history_file, self.config.default_encoding)
            )
        
        self.logger.info("Calculator initialized")
    
    def register_observer(self, observer: CalculatorObserver):
        """
        Register an observer.
        
        Args:
            observer: Observer to register.
        """
        self.observers.append(observer)
    
    def notify_observers(self, calculation: Calculation):
        """
        Notify all observers of a calculation.
        
        Args:
            calculation: The calculation to notify about.
        """
        for observer in self.observers:
            observer.on_calculation_performed(calculation)
    
    def perform_calculation(self, operation: str, operand1: float, operand2: float) -> float:
        """
        Perform a calculation.
        
        Args:
            operation: Operation name.
            operand1: First operand.
            operand2: Second operand.
            
        Returns:
            The result of the calculation.
            
        Raises:
            OperationError: If the operation fails.
            ValidationError: If inputs are invalid.
        """
        # Validate inputs
        operand1 = InputValidator.validate_number(operand1, self.config.max_input_value)
        operand2 = InputValidator.validate_number(operand2, self.config.max_input_value)
        
        # Get operation and execute
        op = OperationFactory.create_operation(operation)
        result = op.execute(operand1, operand2)
        
        # Round result to configured precision
        result = round(result, self.config.precision)
        
        # Create calculation record
        calculation = Calculation(operation, operand1, operand2, result)
        
        # Add to history
        self.history.add_calculation(calculation)
        
        # Save state AFTER adding calculation
        self.caretaker.save_state(CalculatorMemento(self.history.get_history()))
        
        # Notify observers
        self.notify_observers(calculation)
        
        return result
    
    def undo(self):
        """
        Undo the last calculation.
        
        Raises:
            HistoryError: If there's nothing to undo.
        """
        if not self.caretaker.can_undo():
            raise HistoryError("Nothing to undo")
        
        try:
            memento = self.caretaker.undo()
            self.history.set_history(memento.get_history())
            self.logger.info("Undo performed")
            print(f"{Fore.GREEN}Undo successful")
        except IndexError:
            raise HistoryError("Nothing to undo")
    
    def redo(self):
        """
        Redo the last undone calculation.
        
        Raises:
            HistoryError: If there's nothing to redo.
        """
        if not self.caretaker.can_redo():
            raise HistoryError("Nothing to redo")
        
        try:
            memento = self.caretaker.redo()
            self.history.set_history(memento.get_history())
            self.logger.info("Redo performed")
            print(f"{Fore.GREEN}Redo successful")
        except IndexError:
            raise HistoryError("Nothing to redo")
    
    def clear_history(self):
        """Clear calculation history."""
        self.history.clear_history()
        self.caretaker.clear()
        self.logger.info("History cleared")
        print(f"{Fore.GREEN}History cleared")
    
    def save_history(self, file_path: str = None):
        """
        Save history to CSV file.
        
        Args:
            file_path: Path to save file (optional).
        """
        if file_path is None:
            file_path = os.path.join(
                self.config.history_dir,
                'calculator_history.csv'
            )
        
        self.history.save_to_csv(file_path, self.config.default_encoding)
        self.logger.info(f"History saved to {file_path}")
        print(f"{Fore.GREEN}History saved to {file_path}")
    
    def load_history(self, file_path: str = None):
        """
        Load history from CSV file.
        
        Args:
            file_path: Path to load file (optional).
        """
        if file_path is None:
            file_path = os.path.join(
                self.config.history_dir,
                'calculator_history.csv'
            )
        
        self.history.load_from_csv(file_path, self.config.default_encoding)
        self.logger.info(f"History loaded from {file_path}")
        print(f"{Fore.GREEN}History loaded from {file_path}")
    
    def display_history(self):
        """Display calculation history."""
        if len(self.history) == 0:
            print(f"{Fore.YELLOW}No calculations in history")
        else:
            print(f"{Fore.CYAN}{Style.BRIGHT}Calculation History:")
            for i, calc in enumerate(self.history.get_history(), 1):
                print(f"{Fore.CYAN}{i}. {calc}")
    
    def display_help(self):
        """Display help information."""
        operations = OperationFactory.get_available_operations()
        
        help_text = f"""
{Fore.CYAN}{Style.BRIGHT}Calculator Commands:
{Fore.GREEN}Arithmetic Operations:
"""
        for op in operations:
            help_text += f"  {op:<15} - Perform {op} operation\n"
        
        help_text += f"""
{Fore.GREEN}History Management:
  {"history":<15} - Display calculation history
  {"clear":<15} - Clear calculation history
  {"undo":<15} - Undo the last calculation
  {"redo":<15} - Redo the last undone calculation

{Fore.GREEN}File Operations:
  {"save":<15} - Save history to CSV file
  {"load":<15} - Load history from CSV file

{Fore.GREEN}Other Commands:
  {"help":<15} - Display this help message
  {"exit":<15} - Exit the calculator
"""
        print(help_text)
    
    def run_repl(self):
        """Run the REPL (Read-Eval-Print Loop) interface."""
        print(f"{Fore.CYAN}{Style.BRIGHT}Welcome to the Advanced Calculator!")
        print(f"{Fore.CYAN}Type 'help' for available commands or 'exit' to quit.\n")
        
        while True:
            try:
                # Read command
                command = input(f"{Fore.YELLOW}calculator> {Style.RESET_ALL}").strip().lower()
                
                if not command:
                    continue
                
                # Handle exit
                if command == 'exit':
                    print(f"{Fore.CYAN}Goodbye!")
                    self.logger.info("Calculator exited")
                    break
                
                # Handle help
                if command == 'help':
                    self.display_help()
                    continue
                
                # Handle history
                if command == 'history':
                    self.display_history()
                    continue
                
                # Handle clear
                if command == 'clear':
                    self.clear_history()
                    continue
                
                # Handle undo
                if command == 'undo':
                    self.undo()
                    continue
                
                # Handle redo
                if command == 'redo':
                    self.redo()
                    continue
                
                # Handle save
                if command == 'save':
                    self.save_history()
                    continue
                
                # Handle load
                if command == 'load':
                    self.load_history()
                    continue
                
                # Handle operations
                available_operations = OperationFactory.get_available_operations()
                if command in available_operations:
                    # Get operands
                    operand1_str = input(f"{Fore.YELLOW}Enter first number: {Style.RESET_ALL}").strip()
                    operand2_str = input(f"{Fore.YELLOW}Enter second number: {Style.RESET_ALL}").strip()
                    
                    # Perform calculation
                    result = self.perform_calculation(command, operand1_str, operand2_str)
                    print(f"{Fore.GREEN}{Style.BRIGHT}Result: {result}")
                else:
                    print(f"{Fore.RED}Unknown command: {command}. Type 'help' for available commands.")
                
            except (OperationError, ValidationError, HistoryError) as e:
                print(f"{Fore.RED}Error: {e}")
                self.logger.error(str(e))
            except KeyboardInterrupt:
                print(f"\n{Fore.CYAN}Use 'exit' command to quit.")
            except Exception as e:
                print(f"{Fore.RED}Unexpected error: {e}")
                self.logger.error(f"Unexpected error: {e}")


def main():
    """Main entry point for the calculator application."""
    try:
        calculator = Calculator()
        calculator.run_repl()
    except Exception as e:
        print(f"{Fore.RED}Failed to start calculator: {e}")


if __name__ == "__main__":  # pragma: no cover
    main()
