from app.operations import OperationFactory
from app.history import HistoryManager
from app.calculator_memento import Caretaker, Memento

class CalculatorREPL:
    def __init__(self):
        self.history_manager = HistoryManager()
        self.caretaker = Caretaker()
        print("Welcome to the Modular Command-Line Calculator!")
        print("Type 'help' to see available commands.\n")

    def run(self):
        while True:
            user_input = input(">>> ").strip()
            if not user_input:
                continue

            command_parts = user_input.split()
            command = command_parts[0].lower()

            try:
                if command == "exit":
                    print("Goodbye!")
                    break

                elif command == "help":
                    self.print_help()

                elif command in [
                    "add", "subtract", "multiply", "division",
                    "modulus", "power", "root", "int_divide", "abs_diff"
                ]:
                    a = float(command_parts[1])
                    b = float(command_parts[2])
                    operation = OperationFactory.get_operation(command)
                    result = operation.execute(a, b)
                    print(f"Result: {result}")

                    self.history_manager.add_entry(command, a, b, result)
                    memento = Memento(command, a, b, result)
                    self.caretaker.save_state(memento)

                elif command == "history":
                    entries = self.history_manager.get_all()
                    if not entries:
                        print("History is empty.")
                    else:
                        for i, entry in enumerate(entries, start=1):
                            print(f"{i}. {entry['operation']}({entry['a']}, {entry['b']}) = {entry['result']}")

                elif command == "undo":
                    state = self.caretaker.undo()
                    if state:
                        print(f"Undo -> {state.operation_name}({state.a}, {state.b}) = {state.result}")
                    else:
                        print("Nothing to undo.")

                elif command == "redo":
                    state = self.caretaker.redo()
                    if state:
                        print(f"Redo -> {state.operation_name}({state.a}, {state.b}) = {state.result}")
                    else:
                        print("Nothing to redo.")

                elif command in ["save", "load"]:
                    print(f"(Stub) Command '{command}' recognized but not implemented yet.")

                else:
                    print(f"Unknown command: {command}. Type 'help' for a list of commands.")

            except Exception as e:
                print(f"Error: {e}")

    def print_help(self):
        print("\nAvailable Commands:")
        print("add, subtract, multiply, division, modulus, power, root, int_divide, abs_diff")
        print("undo, redo, save, load, history, help, exit\n")

if __name__ == "__main__":
    repl = CalculatorREPL()
    repl.run()
