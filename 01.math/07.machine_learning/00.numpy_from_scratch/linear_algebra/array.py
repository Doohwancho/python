from typing import List, Union, Callable
import copy
from math.math_functions import MathFunctions


class Array:
    """
    Base array class with basic numerical operations
    """
    def __init__(self, data: List[Union[int, float]]):
        self._data = copy.deepcopy(data)
        self._size = len(data)

    @property
    def size(self) -> int:
        return self._size

    def __getitem__(self, index: int) -> Union[int, float]:
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        return self._data[index]

    def __setitem__(self, index: int, value: Union[int, float]):
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        self._data[index] = value

    def __len__(self) -> int:
        return self._size

    def map(self, func: Callable) -> 'Array':
        """Apply function to each element"""
        return Array([func(x) for x in self._data])

    def reduce(self, func: Callable, initial=None) -> Union[int, float]:
        """Reduce array to single value using function"""
        if initial is None:
            result = self._data[0]
            start_idx = 1
        else:
            result = initial
            start_idx = 0

        for i in range(start_idx, self._size):
            result = func(result, self._data[i])
        return result

    def __add__(self, other: 'Array') -> 'Array':
        if self._size != len(other):
            raise ValueError("Arrays must be of same size")
        return Array([a + b for a, b in zip(self._data, other._data)])

    def __mul__(self, scalar: Union[int, float]) -> 'Array':
        return Array([x * scalar for x in self._data])

    def sum(self) -> Union[int, float]:
        """Sum of all elements"""
        return sum(self._data)

    def mean(self) -> float:
        """Average of all elements"""
        return self.sum() / self._size

    def variance(self) -> float:
        """Calculate variance"""
        mean = self.mean()
        return sum((x - mean) ** 2 for x in self._data) / self._size

    def std(self) -> float:
        """Calculate standard deviation"""
        return MathFunctions.sqrt(self.variance())

    def __str__(self) -> str:
        return str(self._data)
