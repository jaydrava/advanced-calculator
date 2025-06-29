# Command-Line Calculator

## Overview

This project is a modular, extensible command-line calculator implemented in Python. It supports a variety of arithmetic operations, command history management, undo/redo functionality, persistent saving/loading of history, and logging. The design utilizes multiple software design patterns such as Factory, Memento, and Observer to ensure maintainability and scalability.


## Features

- **Arithmetic Operations:**
  Addition, Subtraction, Multiplication, Division, Modulus, Power, Root, Interger Division, Absolute Difference.

- **Command History:**
  Maintains a history of all operations with support for saving to and loading from CSV files.

- **Undo/Redo:**
  Undo and redo the last operations using the Memento design pattern.

- **Logging:**
  Logs every operation with timestamps to a log file using Observer pattern.

- **Autosave:**
  Automatically saves history after each operation.

- **Robust Error Handling:**
  Handles invalid input, division by zero and other exceptions gracefully.

- **Comprehensive Unit Tests:**
  100% test coverage with pytest, including tests for operations, history, memento, and the REPL interface.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (python package manager)

### Installtion

1. Clone the repository:

   ```bash

   git clone https://github.com/jaydrava/advanced-calculator.git

   ```
2. Create and activate a virtual enironment:
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Usage
    Run the calculator REPL interface:
    ```bash
    python -m app.calculator
    ```
5. Commands
   - add a b — Adds two numbers
   - subtract a b — Subtracts b from a
   - multiply a b — Multiplies two numbers
   - division a b — Divides a by b (b ≠ 0)
   - modulus a b — Computes a modulo b
   - power a b — Computes a raised to the power of b
   - root a b — Computes the b-th root of a
   - int_divide a b — Integer division of a by b
   - abs_diff a b — Absolute difference between a and b
   - history — Show operation history
   - undo — Undo last operation
   - redo — Redo last undone operation
   - save — Save history to CSV
   - load — Load history from CSV
   - help — Show available commands
   - exit — Exit the calculator

6. Project Structure

```
project_root/
│
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── logger.py
│   ├── operations.py
│
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_calculation.py
│   ├── test_history.py
│   ├── test_memento.py
│   ├── test_operations.py
│
├── history/                  # Generated runtime history (CSV)
│   └── calculator_history.csv
│
├── logs/                     # Runtime logs
│   └── calculator.log
│
├── .gitignore
├── README.md
├── requirements.txt
└── venv/                     # Virtual environment (ignored by git)
```

7. Testing

    pytest --cov=app tests/

    Test Cover:

    - Operation classes and Factory

    - HistoryManager

    - Memento and Caretaker (undo/redo)

    - REPL interface and command parsing

8. Design Patterns

    - Factory: Creates arithmetic operation objects based on command names.

    - Memento: Captures and restores calculator state for undo/redo.

    - Observer: Used for logging and autosave functionality triggered on operations.




















