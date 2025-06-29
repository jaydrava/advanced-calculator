# tests/test_calculator_memento.py
import pytest
from app.calculator_memento import Memento, Caretaker

def make_history(entries):
    """Helper to create history-like list of dicts."""
    return [entry.copy() for entry in entries]

def test_memento_state_copies():
    history = [{"operation": "add", "a": 1, "b": 2, "result": 3}]
    memento = Memento(history)
    state = memento.get_state()

    # Should be equal but not the same object (deep copy)
    assert state == history
    assert state is not history
    assert state[0] is not history[0]

def test_caretaker_save_and_get_state():
    history1 = [{"operation": "add", "a": 1, "b": 2, "result": 3}]
    history2 = [{"operation": "subtract", "a": 5, "b": 3, "result": 2}]

    caretaker = Caretaker()
    memento1 = Memento(history1)
    memento2 = Memento(history2)

    caretaker.save_state(memento1)
    caretaker.save_state(memento2)

    # Current state should be the last saved
    current_state = caretaker.undo_stack[-1].get_state()
    assert current_state == history2

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

    # Redo once: should return history3 (NOT history2)
    redo_state = caretaker.redo()
    assert redo_state == history2

def test_undo_clears_redo_stack():
    history1 = [{"operation": "add", "a": 1, "b": 2, "result": 3}]
    history2 = [{"operation": "subtract", "a": 5, "b": 3, "result": 2}]
    history3 = [{"operation": "multiply", "a": 3, "b": 4, "result": 12}]

    caretaker = Caretaker()
    caretaker.save_state(Memento(history1))
    caretaker.save_state(Memento(history2))
    caretaker.save_state(Memento(history3))

    # Undo twice
    caretaker.undo()
    caretaker.undo()

    # Now save new state; redo stack should be cleared
    new_history = [{"operation": "divide", "a": 10, "b": 2, "result": 5}]
    caretaker.save_state(Memento(new_history))

    # Redo should be empty
    assert caretaker.redo() is None

def test_get_current_state_empty_stack():
    caretaker = Caretaker()
    assert caretaker.get_current_state() is None

def test_get_current_state_returns_latest():
    history = [{"operation": "add", "a": 1, "b": 2, "result": 3}]
    caretaker = Caretaker()
    caretaker.save_state(Memento(history))
    assert caretaker.get_current_state() == history
