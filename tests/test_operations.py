import pytest
from app.operations import OperationFactory
from app.exceptions import OperationError

@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 8),
    (-1, -2, -3),
    (0, 0, 0)
])
def test_add(a, b, expected):
    op = OperationFactory.get_operation("add")
    assert op.execute(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 2),
    (0, 5, -5),
])
def test_subtract(a, b, expected):
    op = OperationFactory.get_operation("subtract")
    assert op.execute(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (2, 4, 8),
    (-1, 3, -3),
])
def test_multiply(a, b, expected):
    op = OperationFactory.get_operation("multiply")
    assert op.execute(a, b) == expected

def test_division():
    op = OperationFactory.get_operation("division")
    assert op.execute(6, 3) == 2

def test_division_by_zero():
    op = OperationFactory.get_operation("division")
    with pytest.raises(ZeroDivisionError):
        op.execute(5, 0)

def test_modulus():
    op = OperationFactory.get_operation("modulus")
    assert op.execute(10, 3) == 1

def test_power():
    op = OperationFactory.get_operation("power")
    assert op.execute(2, 3) == 8

def test_root():
    op = OperationFactory.get_operation("root")
    assert round(op.execute(27, 3), 5) == 3

def test_int_divide():
    op = OperationFactory.get_operation("int_divide")
    assert op.execute(7, 2) == 3

def test_abs_diff():
    op = OperationFactory.get_operation("abs_diff")
    assert op.execute(5, 10) == 5

def test_invalid_operation():
    with pytest.raises(OperationError):
        OperationFactory.get_operation("invalid")

def test_root_with_zero_exponent():
    op = OperationFactory.get_operation("root")
    with pytest.raises(ZeroDivisionError, match="Cannot take root with exponent 0."):
        op.execute(27, 0)

def test_int_divide_by_zero():
    op = OperationFactory.get_operation("int_divide")
    with pytest.raises(ZeroDivisionError, match="Cannot perform interger division by 0."):
        op.execute(10, 0)
