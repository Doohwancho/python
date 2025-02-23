class Var:
    """
    Variable class for automatic differentiation
    Implements forward-mode automatic differentiation
    """
    def __init__(self, value: float, derivative: float = 0.0):
        self.value = value
        self.derivative = derivative

    def __add__(self, other: Union['Var', float]) -> 'Var':
        if isinstance(other, (int, float)):
            return Var(self.value + other, self.derivative)
        return Var(self.value + other.value, 
                  self.derivative + other.derivative)

    def __mul__(self, other: Union['Var', float]) -> 'Var':
        if isinstance(other, (int, float)):
            return Var(self.value * other, self.derivative * other)
        return Var(self.value * other.value,
                  self.derivative * other.value + self.value * other.derivative)

    def __pow__(self, power: float) -> 'Var':
        return Var(self.value ** power,
                  power * self.value ** (power - 1) * self.derivative)

    def __truediv__(self, other: Union['Var', float]) -> 'Var':
        if isinstance(other, (int, float)):
            return Var(self.value / other, self.derivative / other)
        return Var(self.value / other.value,
                  (self.derivative * other.value - self.value * other.derivative) / 
                  (other.value * other.value))
