from app.exceptions import ValidationError

def validate_operands(operands):
    if len(operands) != 2:
        raise ValidationError("Please provide exactly two numeric operands. Example: add 5 2")
    try:
        a, b = float(operands[0]), float(operands[1])
    except ValueError:
        raise ValidationError("Operands must be numeric.")
    return a, b
