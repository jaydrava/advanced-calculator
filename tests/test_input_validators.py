import pytest
from app.input_validators import validate_operands
from app.exceptions import ValidationError

def test_validate_operands_success():
    assert validate_operands(["4", "5"]) == (4.0, 5.0)

def test_validate_operands_non_numeric():
    with pytest.raises(ValidationError):
        validate_operands(["x", "5"])

def test_validate_operands_incorrect_count():
    with pytest.raises(ValidationError):
        validate_operands(["3"])
