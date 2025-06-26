import os
from dotenv import load_dotenv
from app.exceptions import ConfigError

load_dotenv()


class CalculatorConfig:

    LOG_DIR = os.getenv("CALCULATOR_LOG_DIR", "./logs")
    HISTORY_DIR = os.getenv("CALCULATOR_HISTORY_DIR", "./history")
    MAX_HISTORY_SIZE = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", 50))
    AUTO_SAVE = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
    PRECISION = int(os.getenv("CALCULATOR_PRECISION", 2))
    MAX_INPUT_VALUE = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", 1e6))
    DEFAULT_ENCODING = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

    @classmethod
    def validate(cls):
        if cls.PRECISION < 0:
            raise ConfigError("PRECISION must be non-negative.")
        if cls.MAX_HISTORY_SIZE < 1:
            raise ConfigError("MAX_HISTORY_SIZE must be at least 1")
        if cls.MAX_INPUT_VALUE <= 0:
            raise ConfigError("MAX_INPUT_VALUE must be greater than zero")


