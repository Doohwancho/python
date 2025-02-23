class IterativeSolver:
    """Base class for iterative solvers"""
    def __init__(self, max_iterations: int = 1000, tolerance: float = 1e-10):
        self.max_iterations = max_iterations
        self.tolerance = tolerance

    def _norm(self, x: List[float]) -> float:
        """Compute vector norm"""
        return math.sqrt(sum(xi * xi for xi in x))

    def _dot(self, x: List[float], y: List[float]) -> float:
        """Compute dot product"""
        return sum(xi * yi for xi, yi in zip(x, y))
