# Advanced Calculator Application

A robust command-line calculator application with advanced features including history management, undo/redo functionality, automatic saving, and comprehensive error handling.

## Features

### Core Functionality
- **Arithmetic Operations**: Addition, Subtraction, Multiplication, Division
- **Advanced Operations**: 
  - Power (exponentiation)
  - Root (nth root calculation)
  - Modulus (remainder)
  - Integer Division
  - Percentage Calculation
  - Absolute Difference

### Design Patterns
- **Factory Pattern**: Dynamic operation creation and management
- **Memento Pattern**: Undo/redo functionality for calculations
- **Observer Pattern**: Event-driven logging and auto-save features
- **Singleton Pattern**: Centralized logger instance

### Key Features
- **Interactive REPL**: User-friendly command-line interface
- **History Management**: Track all calculations with timestamps
- **Undo/Redo**: Revert or replay calculations
- **Data Persistence**: Save/load history to CSV files using pandas
- **Configuration Management**: Flexible settings via `.env` file
- **Comprehensive Logging**: Detailed logging of all operations
- **Auto-Save**: Automatic history backup on each calculation
- **Input Validation**: Robust validation with meaningful error messages
- **Color-Coded Output**: Enhanced readability with colorama
- **90%+ Test Coverage**: Comprehensive unit tests with pytest

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd IS601_Midterm_Jyothsna
   ```

2. **Create Virtual Environment**
   
   On Windows (PowerShell):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   
   On Linux/Mac:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application uses a `.env` file for configuration. Default values are provided, but you can customize them:

### Configuration Parameters

Create or edit the `.env` file in the root directory:

```env
# Directory Settings
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history

# History Settings
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true

# Calculation Settings
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=10000000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

### Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `CALCULATOR_LOG_DIR` | Directory for log files | `logs` |
| `CALCULATOR_HISTORY_DIR` | Directory for history files | `history` |
| `CALCULATOR_MAX_HISTORY_SIZE` | Maximum number of history entries | `100` |
| `CALCULATOR_AUTO_SAVE` | Enable auto-save (true/false) | `true` |
| `CALCULATOR_PRECISION` | Decimal places for results | `2` |
| `CALCULATOR_MAX_INPUT_VALUE` | Maximum allowed input value | `10000000000` |
| `CALCULATOR_DEFAULT_ENCODING` | File encoding | `utf-8` |

## Usage

### Starting the Calculator

Run the calculator application:

```bash
python -m app.calculator
```

### Available Commands

#### Arithmetic Operations
Enter the operation name, then provide two numbers when prompted:

- `add` - Addition
- `subtract` - Subtraction
- `multiply` - Multiplication
- `divide` - Division
- `power` - Raise first number to the power of second
- `root` - Calculate nth root (first number is value, second is root degree)
- `modulus` - Calculate remainder
- `int_divide` - Integer division
- `percent` - Calculate percentage (first / second * 100)
- `abs_diff` - Absolute difference between numbers

#### History Management
- `history` - Display all calculations in history
- `clear` - Clear calculation history
- `undo` - Undo the last calculation
- `redo` - Redo the last undone calculation

#### File Operations
- `save` - Manually save history to CSV file
- `load` - Load history from CSV file

#### Other Commands
- `help` - Display help information
- `exit` - Exit the calculator

### Example Session

```
calculator> add
Enter first number: 10
Enter second number: 5
Result: 15

calculator> power
Enter first number: 2
Enter second number: 8
Result: 256

calculator> history
Calculation History:
1. 10.0 add 5.0 = 15.0 [2025-11-02 10:30:45]
2. 2.0 power 8.0 = 256.0 [2025-11-02 10:31:12]

calculator> undo
Undo successful

calculator> exit
Goodbye!
```

## Testing

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=app --cov-report=html
```

Run tests with coverage enforcement (90% threshold):
```bash
pytest --cov=app --cov-fail-under=90
```

View detailed coverage report:
```bash
pytest --cov=app --cov-report=term-missing
```

### Test Structure

The test suite includes comprehensive tests for:
- All arithmetic operations
- Input validation
- Error handling
- History management
- Undo/redo functionality
- Configuration loading
- File persistence (CSV operations)
- Observer pattern
- Memento pattern

## CI/CD Pipeline

### GitHub Actions

The project uses GitHub Actions for continuous integration:

- **Triggers**: Runs on push/pull request to main branch
- **Environment**: Ubuntu latest with Python 3.x
- **Steps**:
  1. Check out code
  2. Set up Python environment
  3. Install dependencies
  4. Run tests with 90% coverage enforcement

### Workflow File

Located at `.github/workflows/python-app.yml`

## Project Structure

```
IS601_Midterm_Jyothsna/
├── app/
│   ├── __init__.py
│   ├── calculator.py          # Main calculator with REPL
│   ├── calculation.py          # Calculation class
│   ├── calculator_config.py    # Configuration management
│   ├── calculator_memento.py   # Memento pattern for undo/redo
│   ├── exceptions.py           # Custom exceptions
│   ├── history.py              # History management with pandas
│   ├── input_validators.py     # Input validation utilities
│   ├── logger.py               # Logging configuration
│   └── operations.py           # Operations with Factory pattern
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_calculation.py
│   ├── test_calculator_config.py
│   ├── test_calculator_memento.py
│   ├── test_history.py
│   ├── test_input_validators.py
│   └── test_operations.py
├── .github/
│   └── workflows/
│       └── python-app.yml      # CI/CD workflow
├── .env                        # Configuration file
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Architecture

### Design Patterns

#### Factory Pattern
The `OperationFactory` class manages creation of operation instances, making it easy to add new operations without modifying existing code.

#### Memento Pattern
The `CalculatorMemento` and `CalculatorCaretaker` classes implement undo/redo functionality by saving and restoring calculator state.

#### Observer Pattern
The calculator uses observers to respond to calculation events:
- `LoggingObserver`: Logs calculations to file
- `AutoSaveObserver`: Automatically saves history to CSV

#### Singleton Pattern
The `Logger` class uses singleton pattern to ensure a single logging instance across the application.

## Error Handling

The application includes robust error handling:

- **OperationError**: Raised for operation failures (e.g., division by zero)
- **ValidationError**: Raised for invalid inputs
- **ConfigurationError**: Raised for configuration issues
- **HistoryError**: Raised for history management errors

All errors provide meaningful messages to help users correct their input.

## Logging

Logs are automatically created in the configured log directory with:
- Timestamp
- Log level (INFO, WARNING, ERROR)
- Detailed messages

Log files are named: `calculator_YYYYMMDD.log`

## Data Persistence

History is stored in CSV format using pandas:

### CSV Format
```csv
operation,operand1,operand2,result,timestamp
add,5.0,3.0,8.0,2025-11-02T10:30:45.123456
subtract,10.0,2.0,8.0,2025-11-02T10:31:12.789012
```

Files are saved to the configured history directory with UTF-8 encoding.

## Optional Features Implemented

### Color-Coded Output (using Colorama)
- Cyan: Informational messages and history
- Green: Success messages and results
- Yellow: Input prompts
- Red: Error messages
- Enhanced readability and user experience

## Development

### Adding New Operations

1. Create a new operation class inheriting from `Operation`:

```python
class NewOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        # Implementation
        return result
    
    def get_name(self) -> str:
        return "new_op"
```

2. Register it with the factory:

```python
OperationFactory.register_operation("new_op", NewOperation)
```

### Code Quality

The project follows best practices:
- **DRY Principle**: No code duplication
- **SOLID Principles**: Proper OOP design
- **PEP 8**: Python style guide compliance
- **Type Hints**: Enhanced code clarity
- **Docstrings**: Comprehensive documentation
- **Modular Design**: Separation of concerns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with clear commit messages
4. Ensure tests pass and coverage remains above 90%
5. Submit a pull request

## License

This project is created for educational purposes as part of IS601 coursework.

## Author

Jyothsna Reddy

## Acknowledgments

- Course: IS601 - Web Systems Development
- Institution: NJIT
- Instructor: Professor Keith Williams
