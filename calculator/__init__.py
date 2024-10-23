import logging

class Calculator:
    """A simple calculator class for basic arithmetic operations."""

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Calculator initialized.")

    def execute(self, operation, *args):
        """Execute a specific operation based on the command provided."""
        if len(args) != 2:
            logging.error("Please enter 2 arguments.")
            return "Error: Please enter exactly 2 arguments."

        try:
            arg1, arg2 = float(args[0]), float(args[1])  # Convert inputs to numbers
        except ValueError:
            logging.error("Invalid arguments for arithmetic operation. Arguments must be numbers.")
            return "Error: Invalid arguments. Arguments must be numbers."

        if operation == "add":
            return self.add(arg1, arg2)
        elif operation == "subtract":
            return self.subtract(arg1, arg2)
        elif operation == "multiply":
            return self.multiply(arg1, arg2)
        elif operation == "divide":
            return self.divide(arg1, arg2)
        else:
            logging.error(f"Unknown operation: {operation}")
            return f"Error: Unknown operation '{operation}'."

    def add(self, a, b):
        """Return the sum of a and b."""
        result = a + b
        entry = f"Added {a} + {b} = {result}"
        logging.info(entry)
        return result

    def subtract(self, a, b):
        """Return the result of a minus b."""
        result = a - b
        entry = f"Subtracted {a} - {b} = {result}"
        logging.info(entry)
        return result

    def multiply(self, a, b):
        """Return the product of a and b."""
        result = a * b
        entry = f"Multiplied {a} * {b} = {result}"
        logging.info(entry)
        return result

    def divide(self, a, b):
        """Return the result of a divided by b."""
        if b == 0:
            logging.error("Division by zero attempted.")
            return "Error: Cannot divide by zero."
        result = a / b
        entry = f"Divided {a} / {b} = {result}"
        logging.info(entry)
        return result