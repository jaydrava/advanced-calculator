from app.operations import OperationFactory
from app.exceptions import OperationError, ValidationError

class Calculation:
    def __init__(self, operation_name, a, b):
        self.operation_name = operation_name
        self.a = a
        self.b = b
        self.result = None

    def validate_inputs(self):
        if not isinstance(self.a, (int, float)) or not isinstance(self.b, (int, float)):
            raise ValidationError("Input must be numeric.")

    def execute(self):
        try:
            self.validate_inputs()
            operation_class = OperationFactory.get_operation(self.operation_name)
            self.result = operation_class.execute(self.a, self.b)
            return self.result
        except (OperationError, ZeroDivisionError, ValueError) as e:
            raise OperationError(f"Calculation failed: {str(e)}")




