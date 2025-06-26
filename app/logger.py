import os
import datetime
from app.calculator_config import CalculatorConfig
from app.exceptions import LoggingError

class LoggingObserver:
    def __init__(self):
        os.makedirs(CalculatorConfig.LOG_DIR, exist_ok=True)
        self.log_file = os.path.join(CalculatorConfig.LOG_DIR, "calculator.log")

    def update(self, operation_name, a, b, result):
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] {operation_name.upper()} | {a}, {b} => {result}\n"
        try:
            with open(self.log_file, "a", encoding=CalculatorConfig.DEFAULT_ENCODING) as f:
                f.write(log_entry)
        except Exception as e:
            raise LoggingError(f"Failed to write log: {str(e)}")

class AutoSaveObserver:
    def __init__(self, history_manager):
        self.history_manager = history_manager

    def update(self, *args, **kwargs):
        try:
            self.history_manager.save_to_csv()
        except Exception as e:
            raise LoggingError(f"Auto-save failed: {str(e)}")
