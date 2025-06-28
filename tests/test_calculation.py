import pytest
from app.operations import OperationFactory
from app.exceptions import OperationError

def test_addition():
    op = OperationFactory.get_operation("add")
    assert op.execute(2, 3) == 5

def test_subtraction():
    op = OperationFactory.get_operation("subtract")
    assert op.execute(5, 2) == 3

def test_multiplication():
    op = OperationFactory.get_operation("multiply")
    assert op.execute(3, 4) == 12

def test_division():
    op = OperationFactory.get_operation("division")
    assert op.execute(10, 2) == 5

def test_division_by_zero():
    op = OperationFactory.get_operation("division")
    with pytest.raises(ZeroDivisionError):
        op.execute(5, 0)
