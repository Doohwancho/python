from typing import Union

class Rational:
    """
    Represents rational numbers as fractions (numerator/denominator)
    """
    def __init__(self, numerator: int, denominator: int = 1):
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        
        # Ensure denominator is positive
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
            
        # Simplify the fraction
        gcd = self._gcd(abs(numerator), abs(denominator))
        self.numerator = numerator // gcd
        self.denominator = denominator // gcd

    def _gcd(self, a: int, b: int) -> int:
        """Calculate Greatest Common Divisor using Euclidean algorithm"""
        while b:
            a, b = b, a % b
        return a

    def __add__(self, other: 'Rational') -> 'Rational':
        new_num = (self.numerator * other.denominator + 
                  other.numerator * self.denominator)
        new_den = self.denominator * other.denominator
        return Rational(new_num, new_den)

    def __mul__(self, other: 'Rational') -> 'Rational':
        return Rational(self.numerator * other.numerator,
                       self.denominator * other.denominator)

    def __truediv__(self, other: 'Rational') -> 'Rational':
        if other.numerator == 0:
            raise ZeroDivisionError("Division by zero")
        return Rational(self.numerator * other.denominator,
                       self.denominator * other.numerator)

    def to_float(self) -> float:
        return self.numerator / self.denominator

    def __str__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"
