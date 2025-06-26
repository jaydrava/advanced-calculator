import os
import pandas as pd
from app.calculator_config import CalculatorConfig
from app.exceptions import HistoryError

class HistoryManager:
    def __init__(self):
        self.history = [] # internal list to hold records
        self.history_file = os.path.join(
            CalculatorConfig.HISTORY_DIR, "calculator_history.csv"
        )
        os.makedirs(CalculatorConfig.HISTORY_DIR, exist_ok=True)

    def add_entry(self, operation_name, a, b, result):
        self.history.append({
            "operation": operation_name,
            "a": a,
            "b": b,
            "result": result
        })

    def save_to_csv(self):
        try:
            df = pd.DataFrame(self.history)
            df.to_csv(self.history_file, index=False, encoding=CalculatorConfig.DEFAULT_ENCODING)
        except Exception as e:
            raise HistoryError(f"Failed to save history: {str(e)}")

    def load_from_csv(self):
        if not os.path.exists(self.history_file):
            return  # No history file yet, so nothing to load

        try:
            df = pd.read_csv(self.history_file, encoding=CalculatorConfig.DEFAULT_ENCODING)
            self.history = df.to_dict(orient="records")
        except Exception as e:
            raise HistoryError(f"Failed to load history: {str(e)}")

    def get_all(self):
        return self.history
