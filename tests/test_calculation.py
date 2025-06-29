import pytest
from app.calculation import Calculation
from app.exceptions import OperationError, ValidationError


def test_valid_addition():
    calc = Calculation("add", 5, 3)
    result = calc.execute()
    assert result == 8
    assert calc.result == 8


def test_valid_division():
    calc = Calculation("division", 10, 2)
    result = calc.execute()
    assert result == 5.0


def test_non_numeric_inputs():
    calc = Calculation("add", "a", 2)
    with pytest.raises(ValidationError):
        calc.execute()


def test_invalid_operation_name():
    calc = Calculation("foobar", 5, 2)
    with pytest.raises(OperationError) as exc_info:
        calc.execute()
    assert "Calculation failed" in str(exc_info.value)


def test_division_by_zero():
    calc = Calculation("division", 5, 0)
    with pytest.raises(OperationError) as exc_info:
        calc.execute()
    assert "Calculation failed" in str(exc_info.value)
