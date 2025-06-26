from app.exceptions import OperationError
class Add:
    @staticmethod
    def execute(a, b):
        return a + b

class Subtract:
    @staticmethod
    def execute(a, b):
        return a - b

class Multiply:
    @staticmethod
    def execute(a, b):
        return a * b

class Division:
    @staticmethod
    def execute(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b

class Modulus:
    @staticmethod
    def execute(a, b):
        return a % b

class Power:
    @staticmethod
    def execute(a, b):
        return a ** b

class Root:
    @staticmethod
    def execute(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot take root with exponent 0.")
        return a ** (1/b)

class IntDivide:
    @staticmethod
    def execute(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot perform interger division by 0.")
        return a // b

class AbsDiff:
    @staticmethod
    def execute(a, b):
        return abs(a - b)

class OperationFactory:
    operations = {

        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "division": Division,
        "modulus": Modulus,
        "power": Power,
        "root": Root,
        "int_divide": IntDivide,
        "abs_diff": AbsDiff
    }

    @classmethod
    def get_operation(cls, name):
        op = cls.operations.get(name.lower())
        if not op:
            raise OperationError(f"Unsupported operation: '{name}'")
        return op
