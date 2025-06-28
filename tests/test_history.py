import os
import pytest
from app.history import HistoryManager
from app.exceptions import HistoryError
from app.calculator_config import CalculatorConfig

@pytest.fixture
def history_manager():
    # Clean up before test
    hm = HistoryManager()
    if os.path.exists(hm.history_file):
        os.remove(hm.history_file)
    return hm

def test_add_entry(history_manager):
    history_manager.add_entry("add", 1, 2, 3)
    assert len(history_manager.history) == 1
    assert history_manager.history[0]["operation"] == "add"

def test_save_and_load(history_manager):
    history_manager.add_entry("add", 1, 2, 3)
    history_manager.save_to_csv()
    assert os.path.exists(history_manager.history_file)

    # Create new instance and load
    new_manager = HistoryManager()
    new_manager.load_from_csv()
    assert len(new_manager.history) == 1
    assert new_manager.history[0]["result"] == 3

def test_load_no_file(history_manager):
    # Remove file if exists
    if os.path.exists(history_manager.history_file):
        os.remove(history_manager.history_file)
    # Should not raise error
    history_manager.load_from_csv()
    assert history_manager.history == []

def test_save_raises(monkeypatch, history_manager):
    # Monkeypatch pandas to raise error on to_csv
    def fail_to_csv(*args, **kwargs):
        raise Exception("Fake write error")
    monkeypatch.setattr("pandas.DataFrame.to_csv", fail_to_csv)
    history_manager.add_entry("add", 1, 2, 3)
    with pytest.raises(HistoryError):
        history_manager.save_to_csv()

def test_load_raises(monkeypatch, history_manager):
    # Create a bad CSV to raise error on read
    with open(history_manager.history_file, "w") as f:
        f.write("bad,data\n1")
    monkeypatch.setattr("pandas.read_csv", lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Fake read error")))
    with pytest.raises(HistoryError):
        history_manager.load_from_csv()
