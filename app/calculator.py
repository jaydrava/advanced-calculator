from app.operations import OperationFactory
from app.history import HistoryManager
from app.calculator_memento import Caretaker, Memento
from app.exceptions import OperationError
from app.logger import LoggingObserver, AutoSaveObserver

class CalculatorREPL:
    def __init__(self):
        self.history_manager = HistoryManager()
        self.caretaker = Caretaker()
        self.logger = LoggingObserver()
        self.auto_saver = AutoSaveObserver(self.history_manager)
        self.observers = [self.logger, self.auto_saver]
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
                    if len(command_parts) != 3:
                        print("Error: Please provide exactly two numeric operands. Example: add 5 2")
                        continue
                    try:
                        a = float(command_parts[1])
                        b = float(command_parts[2])
                    except ValueError:
                        print("Error: Operands must be numbers.")
                        continue
                    operation = OperationFactory.get_operation(command)
                    result = operation.execute(a, b)
                    print(f"Result: {result}")

                    self.history_manager.add_entry(command, a, b, result)
                    memento = Memento(self.history_manager.history)
                    self.caretaker.save_state(memento)

                    for observer in self.observers:
                        observer.update(command, a, b, result)


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
                        self.history_manager.history = state  # Restore full history
                        last_entry = state[-1] if state else None
                        if last_entry:
                            print(f"Undo -> {last_entry['operation']}({last_entry['a']}, {last_entry['b']}) = {last_entry['result']}")
                        else:
                            print("History is now empty after undo.")
                    else:
                        print("Nothing to undo.")

                elif command == "redo":
                    state = self.caretaker.redo()
                    if state:
                        self.history_manager.history = state
                        last_entry = state[-1] if state else None
                        if last_entry:
                            print(f"Redo -> {last_entry['operation']}({last_entry['a']}, {last_entry['b']}) = {last_entry['result']}")
                        else:
                            print("Redo restored empty history.")
                    else:
                        print("Nothing to redo.")

                elif command == "save":
                    try:
                        self.history_manager.save_to_csv()
                        print("History saved successfully.")
                    except Exception as e:
                        print(f"Error saving history: {e}")

                elif command == "load":
                    try:
                        self.history_manager.load_from_csv()
                        print("History loaded successfully.")
                    except Exception as e:
                        print(f"Error loading history: {e}")

                else:
                    print(f"Unknown command: {command}. Type 'help' for a list of commands.")

            except ZeroDivisionError:
                print("Error: Division by zero is not allowed.")
            except OperationError as e:
                print(f"Operation Error: {e}")
            except Exception as e:
                print(f"Error: {e}")

    def print_help(self):
        print("\nAvailable Commands:")
        print("add, subtract, multiply, division, modulus, power, root, int_divide, abs_diff")
        print("undo, redo, save, load, history, help, exit\n")

if __name__ == "__main__":
    repl = CalculatorREPL()
    repl.run()
