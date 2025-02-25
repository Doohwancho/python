class Number:
    """
    Base class for numeric types (Real numbers for now)
    We'll implement rational and complex numbers later
    """
    def __init__(self, value: float):
        self.value = float(value)  # Convert to float for consistency

    def __add__(self, other):
        return Number(self.value + other.value)

    def __sub__(self, other):
        return Number(self.value - other.value)

    def __mul__(self, other):
        return Number(self.value * other.value)

    def __truediv__(self, other):
        if other.value == 0:
            raise ZeroDivisionError("Division by zero")
        return Number(self.value / other.value)

    def __str__(self):
        return str(self.value)
