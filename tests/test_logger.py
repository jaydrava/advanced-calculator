import pytest
from unittest.mock import patch, MagicMock
from app.logger import LoggingObserver, AutoSaveObserver
from app.exceptions import LoggingError

def test_logging_observer_update():
    logger = LoggingObserver()
    # Normal call: should not raise
    logger.update('add', 1, 2, 3)

def test_logging_observer_update_raises(monkeypatch):
    logger = LoggingObserver()
    # Patch open to raise IOError to simulate file write failure
    def fake_open(*args, **kwargs):
        raise IOError("disk full")
    monkeypatch.setattr("builtins.open", fake_open)

    with pytest.raises(LoggingError) as excinfo:
        logger.update('add', 1, 2, 3)
    assert "Failed to write log" in str(excinfo.value)

def test_auto_save_observer_update():
    class DummyHistoryManager:
        def __init__(self):
            self.saved = False
        def save_to_csv(self):
            self.saved = True

    history_manager = DummyHistoryManager()
    auto_saver = AutoSaveObserver(history_manager)
    auto_saver.update('add', 1, 2, 3)
    assert history_manager.saved is True

def test_auto_save_observer_update_raises():
    class FailingHistoryManager:
        def save_to_csv(self):
            raise Exception("disk full")

    history_manager = FailingHistoryManager()
    auto_saver = AutoSaveObserver(history_manager)

    with pytest.raises(LoggingError) as excinfo:
        auto_saver.update()
    assert "Auto-save failed" in str(excinfo.value)
