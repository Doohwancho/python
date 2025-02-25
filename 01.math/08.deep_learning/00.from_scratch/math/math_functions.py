import math
from typing import Union, Optional #Union = tuple = dictionary 


class MathFunctions:
    """
    Basic mathematical functions implementation
    """
    @staticmethod
    def sqrt(x: Union[float, int]) -> float:
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        
        # Newton's method for square root
        # TODO: Q. 이게 효률적인 sqrt() 계산 방법인가?
        guess = x / 2
        while True:
            new_guess = (guess + x / guess) / 2
            if abs(new_guess - guess) < 1e-10:  # Convergence threshold
                return new_guess
            guess = new_guess

    @staticmethod
    def exp(x: Union[float, int], iterations: int = 100) -> float:
        """
        Calculate e^x using Taylor series
        """
        result = 1.0
        term = 1.0
        for i in range(1, iterations):
            term *= x / i
            result += term
            if abs(term) < 1e-10:  # Convergence check
                break
        return result

    @staticmethod
    def ln(x: Union[float, int]) -> float:
        """
        Natural logarithm using Newton's method
        """
        if x <= 0:
            raise ValueError("Cannot calculate logarithm of non-positive number")
        
        # Initial guess
        guess = x - 1
        while True:
            new_guess = guess + (x - MathFunctions.exp(guess)) / MathFunctions.exp(guess)
            if abs(new_guess - guess) < 1e-10:
                return new_guess
            guess = new_guess
