def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    pass


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return a divided by b, or an error string if b is 0."""
    if b == 0:
        return "Error: division by zero"
    return a / b
