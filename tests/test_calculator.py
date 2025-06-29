import pytest
from unittest.mock import patch, MagicMock
from app.calculator import CalculatorREPL
from app.exceptions import OperationError
from app.calculator_memento import Memento, Caretaker

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

def test_history_empty_and_nonempty(capsys):
    repl = CalculatorREPL()
    # Initially empty history
    with patch('builtins.input', side_effect=['history', 'add 1 1', 'history', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "History is empty." in captured.out
    assert "add(1.0, 1.0) = 2.0" in captured.out

def test_undo_redo_behavior():
    history1 = [{"operation": "add", "a": 1, "b": 2, "result": 3}]
    history2 = [{"operation": "subtract", "a": 5, "b": 3, "result": 2}]
    history3 = [{"operation": "multiply", "a": 3, "b": 4, "result": 12}]

    caretaker = Caretaker()
    memento1 = Memento(history1)
    memento2 = Memento(history2)
    memento3 = Memento(history3)

    caretaker.save_state(memento1)
    caretaker.save_state(memento2)
    caretaker.save_state(memento3)

    # Undo once: should return history2
    undo_state = caretaker.undo()
    assert undo_state == history2

    # Undo again: should return history1
    undo_state = caretaker.undo()
    assert undo_state == history1

    # Undo again: should return None, can't undo further
    undo_state = caretaker.undo()
    assert undo_state is None

def test_undo_nothing_to_undo(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['undo', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Nothing to undo." in captured.out

def test_redo_nothing_to_redo(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['redo', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Nothing to redo." in captured.out

def test_save_success_and_failure(capsys, monkeypatch):
    repl = CalculatorREPL()

    # Patch save_to_csv to succeed
    monkeypatch.setattr(repl.history_manager, 'save_to_csv', lambda: None)
    with patch('builtins.input', side_effect=['save', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "History saved successfully." in captured.out

    # Patch save_to_csv to raise Exception
    def fail_save():
        raise Exception("disk full")
    monkeypatch.setattr(repl.history_manager, 'save_to_csv', fail_save)
    with patch('builtins.input', side_effect=['save', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Error saving history: disk full" in captured.out

def test_load_success_and_failure(capsys, monkeypatch):
    repl = CalculatorREPL()

    # Patch load_from_csv to succeed
    monkeypatch.setattr(repl.history_manager, 'load_from_csv', lambda: None)
    with patch('builtins.input', side_effect=['load', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "History loaded successfully." in captured.out

    # Patch load_from_csv to raise Exception
    def fail_load():
        raise Exception("file corrupted")
    monkeypatch.setattr(repl.history_manager, 'load_from_csv', fail_load)
    with patch('builtins.input', side_effect=['load', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Error loading history: file corrupted" in captured.out

def test_invalid_operand_count(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['add 1', 'add 1 2 3', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Please provide exactly two numeric operands." in captured.out

def test_observer_updates(monkeypatch):
    repl = CalculatorREPL()

    calls = []

    # Define fake update method to record calls
    def fake_update(command, a, b, result):
        calls.append((command, a, b, result))

    # Patch the update method of logger and auto_saver observers
    monkeypatch.setattr(repl.logger, 'update', fake_update)
    monkeypatch.setattr(repl.auto_saver, 'update', fake_update)

    from unittest.mock import patch

    with patch('builtins.input', side_effect=['add 3 4', 'exit']):
        repl.run()

    # Assert both observers received the update once
    assert calls.count(('add', 3.0, 4.0, 7.0)) == 2

def test_empty_input_skips(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['   ', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Goodbye!" in captured.out

def test_undo_shows_last_entry(capsys):
    repl = CalculatorREPL()
    repl.caretaker.save_state(Memento([]))  # Simulate initial state
    with patch('builtins.input', side_effect=['add 1 2', 'undo', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "History is now empty after undo." in captured.out

def test_redo_shows_last_entry(capsys):
    repl = CalculatorREPL()

    # Save initial empty state manually before operation
    repl.caretaker.save_state(Memento([]))  # So undo can go back

    with patch('builtins.input', side_effect=['add 1 2', 'undo', 'redo', 'exit']):
        repl.run()

    captured = capsys.readouterr()
    assert "Redo -> add(1.0, 2.0) = 3.0" in captured.out

def test_operation_error_handling(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['invalid_op', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Unknown command: invalid_op" in captured.out

def test_redo_restores_empty_history(capsys):
    repl = CalculatorREPL()
    # Simulate empty -> saved -> undo -> redo (which will restore empty)
    repl.caretaker.save_state(Memento([]))
    with patch('builtins.input', side_effect=['undo', 'redo', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Nothing to redo." in captured.out or "Redo restored empty history." in captured.out

def test_invalid_operands_handled(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['add five six', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Operands must be numbers." in captured.out

def test_undo_results_in_empty_history(capsys):
    repl = CalculatorREPL()
    # Save empty history first
    repl.caretaker.save_state(Memento([]))  # <- ADD THIS LINE
    repl.history_manager.add_entry("add", 2, 3, 5)
    repl.caretaker.save_state(Memento(repl.history_manager.history.copy()))

    with patch('builtins.input', side_effect=['undo', 'exit']):
        repl.run()

    captured = capsys.readouterr()
    assert "History is now empty after undo." in captured.out

def test_zero_division_handled(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['division 5 0', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Division by zero is not allowed." in captured.out


def test_unknown_operation_handled(capsys):
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['unknownop 1 2', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out

def test_undo_shows_last_entry_non_empty(capsys):
    repl = CalculatorREPL()
    repl.history_manager.add_entry("add", 1, 2, 3)
    repl.history_manager.add_entry("subtract", 5, 3, 2)
    repl.caretaker.save_state(Memento(repl.history_manager.history.copy()))
    repl.caretaker.save_state(Memento(repl.history_manager.history.copy()))
    with patch('builtins.input', side_effect=['undo', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Undo -> subtract(5, 3) = 2" in captured.out

def test_redo_restores_empty_history_exact_message(capsys):
    repl = CalculatorREPL()

    # Save initial empty state
    repl.caretaker.save_state(Memento([]))

    # Save non-empty state (with one entry)
    repl.history_manager.add_entry("add", 1, 2, 3)
    repl.caretaker.save_state(Memento(repl.history_manager.history.copy()))

    # Undo once (removes last entry, back to empty)
    _ = repl.caretaker.undo()

    repl.caretaker.redo_stack.clear()
    repl.caretaker.redo_stack.append(Memento([]))  # Wrap in Memento

    with patch('builtins.input', side_effect=['redo', 'exit']):
        repl.run()

    captured = capsys.readouterr()
    assert "Redo restored empty history." in captured.out

def test_operation_error_handling_print(capsys, monkeypatch):
    repl = CalculatorREPL()
    def raise_operation_error(command):
        raise OperationError("Test operation error")
    monkeypatch.setattr("app.operations.OperationFactory.get_operation", raise_operation_error)
    with patch('builtins.input', side_effect=['add 1 2', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Operation Error: Test operation error" in captured.out

def test_generic_exception_handling_print(capsys, monkeypatch):
    repl = CalculatorREPL()
    def raise_generic_exception(command):
        raise Exception("Test generic error")
    monkeypatch.setattr("app.operations.OperationFactory.get_operation", raise_generic_exception)
    with patch('builtins.input', side_effect=['add 1 2', 'exit']):
        repl.run()
    captured = capsys.readouterr()
    assert "Error: Test generic error" in captured.out
