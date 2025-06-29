import pytest
from app import calculator_config
from app.exceptions import ConfigError

def test_load_config(monkeypatch):
    # Set some environment variables
    monkeypatch.setenv("CALCULATOR_PRECISION", "3")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "10")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "1000")

    config = calculator_config.load_config()
    assert config.PRECISION == 3
    assert config.MAX_HISTORY_SIZE == 10
    assert config.MAX_INPUT_VALUE == 1000.0

def test_invalid_precision(monkeypatch):
    monkeypatch.setenv("CALCULATOR_PRECISION", "-1")
    with pytest.raises(ConfigError, match="PRECISION must be non-negative."):
        calculator_config.load_config()

def test_invalid_max_history_size(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "0")
    with pytest.raises(ConfigError, match="MAX_HISTORY_SIZE must be at least 1"):
        calculator_config.load_config()

def test_invalid_max_input_value(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "0")
    with pytest.raises(ConfigError, match="MAX_INPUT_VALUE must be greater than zero"):
        calculator_config.load_config()
