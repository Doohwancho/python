from typing import Callable
from linear_algebra.ndarray import NDArray


class Optimizer:
    """Base class for optimization algorithms"""
    def __init__(self, learning_rate: float = 0.01, tolerance: float = 1e-6, max_iterations: int = 1000):
        self.learning_rate = learning_rate
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def _compute_gradient(self, f: Callable, x: NDArray) -> NDArray:
        """
        Compute numerical gradient using central difference
        f: objective function
        x: current point
        """
        eps = 1e-8 # 엄~청 작은 값 
        gradient = []

        # 미분 값 구하는 것
        # 앞뒤로 eps만큼 이동해서 기울기를 구함
        for i in range(len(x)):
            x_plus = x.copy()
            x_plus[i] += eps #앞으로 약간 이동하고 
            x_minus = x.copy()
            x_minus[i] -= eps #뒤로 약간 이동해서 
            # 기울기 = (앞에값 - 뒤에값) / (앞뒤거리)
            gradient.append((f(x_plus) - f(x_minus)) / (2 * eps))  # 각 포인트에서 계산한 미분값을 기록 
        return NDArray(gradient) # 기울기들을 반환함 
