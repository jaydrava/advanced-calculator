# app/calculator_memento.py

class Memento:
    def __init__(self, state):
        # Save a deep copy of the current full history
        self._state = [entry.copy() for entry in state]

    def get_state(self):
        return [entry.copy() for entry in self._state]


class Caretaker:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def save_state(self, memento):
        self.undo_stack.append(memento)
        self.redo_stack.clear()  # Clear redo stack on new action

    def undo(self):
        if len(self.undo_stack) <= 1:
            return None
        memento = self.undo_stack.pop()
        self.redo_stack.append(memento)
        return self.undo_stack[-1].get_state()

    def redo(self):
        if not self.redo_stack:
            return None
        memento = self.redo_stack.pop()
        self.undo_stack.append(memento)
        return memento.get_state()
