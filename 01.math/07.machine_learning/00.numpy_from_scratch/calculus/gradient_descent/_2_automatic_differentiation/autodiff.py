class AutoDiff:
    """
    Automatic differentiation system for scalar functions
    """
    @staticmethod
    def gradient(f: Callable, x: List[float]) -> List[float]:
        """
        Compute gradient of f at point x
        """
        n = len(x)
        grad = []
        
        for i in range(n):
            # Create variable with derivative 1 for current coordinate
            vars = [Var(x[j], 1.0 if j == i else 0.0) for j in range(n)]
            result = f(vars)
            grad.append(result.derivative)
            
        return grad

    @staticmethod
    def hessian(f: Callable, x: List[float]) -> Matrix:
        """
        Compute Hessian matrix of f at point x
        """
        n = len(x)
        H = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i, n):
                # Compute second partial derivative
                def partial_ij(t):
                    vars = [Var(x[k]) for k in range(n)]
                    vars[i] = Var(x[i], 1.0)
                    vars[j] = Var(x[j], 1.0)
                    return f(vars).derivative
                
                H[i][j] = H[j][i] = partial_ij(x)
                
        return Matrix(H)
