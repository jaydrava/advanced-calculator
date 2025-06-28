import pytest
from unittest.mock import patch
from app.calculator import CalculatorREPL
from app.exceptions import OperationError

def test_help_command(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['help', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Available Commands:" in captured.out

def test_unknown_command(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['foo', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Unknown command: foo" in captured.out

def test_add_command(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['add 2 3', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out

def test_add_command_invalid_operands(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['add a b', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Error: Operands must be numbers." in captured.out

def test_division_by_zero(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['division 5 0', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Error: Division by zero is not allowed." in captured.out
