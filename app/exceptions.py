class CalculatorError(Exception):
    """ Base class for all calculator-related exceptions."""
    pass


class OperationError(CalculatorError):
    """ Raised for invalid operations or failures in operations execution. """
    pass


class ValidationError(CalculatorError):
    """ Raised when user input is invalid."""
    pass


class ConfigError(CalculatorError):
    """ Raised when Configration loading fails."""
    pass
