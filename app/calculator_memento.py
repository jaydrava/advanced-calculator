# app/ calculator_memento.py

class CalculatorState:
    def __init__(self, operation_name, a, b, result):
        self.operation_name = operation_name
        self.a = a
        self.b = b
        self.result = result

class CalculatorMemento:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def save_state(self, state):
        self.undo_stack.append(state)
        self.redo_stack.clear() # Clear redo stack after new operation

    def undo(self):
        if len(self.undo_stack) <= 1:
            return None
        state = self.undo_stack.pop()
        self.redo_stack.append(state)
        return self.undo_stack[-1]

    def redo(self):
        if not self.redo_stack:
            return None
        state = self.redo_stack.pop()
        self.undo_stack.append(state)
        return state

    def get_current_state(self):
        if not self.undo_stack:
            return None
        return self.undo_stack[-1]
