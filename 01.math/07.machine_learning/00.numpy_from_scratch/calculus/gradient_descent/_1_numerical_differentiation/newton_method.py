"""
Q. what is Newton's Method?

It's an optimization method that uses both first AND second derivatives (unlike gradient descent which only uses first derivatives)
Think of it like this: while gradient descent only looks at the slope, Newton's method also looks at the curvature
The update rule is: x_new = x - f'(x)/f''(x) for 1D case
For multiple dimensions: x_new = x - H⁻¹∇f where H is the Hessian matrix (matrix of second derivatives) and ∇f is the gradient
Advantages: Converges much faster than gradient descent (quadratic vs linear convergence)
Disadvantages: More expensive per iteration (needs Hessian computation and matrix inversion)
"""
class NewtonMethod(Optimizer):
    """Newton's Method optimization"""
    def _compute_hessian(self, f: Callable, x: NDArray) -> Matrix:
        """Compute Hessian matrix using finite differences"""
        eps = 1e-6
        n = len(x)
        hessian = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                x_pp = x.copy()
                x_pp[i] += eps
                x_pp[j] += eps
                
                x_pm = x.copy()
                x_pm[i] += eps
                x_pm[j] -= eps
                
                x_mp = x.copy()
                x_mp[i] -= eps
                x_mp[j] += eps
                
                x_mm = x.copy()
                x_mm[i] -= eps
                x_mm[j] -= eps
                
                hessian[i][j] = (f(x_pp) - f(x_pm) - f(x_mp) + f(x_mm)) / (4 * eps * eps)
                
        return Matrix(hessian)

    def minimize(self, f: Callable, initial_x: NDArray) -> Tuple[NDArray, List[float]]:
        x = initial_x.copy()
        history = [f(x)]
        
        for i in range(self.max_iterations):
            gradient = self._compute_gradient(f, x)
            hessian = self._compute_hessian(f, x)
            
            try:
                # Solve H * delta = -gradient
                delta = hessian.inverse() @ Matrix([[-g] for g in gradient])
                x = x + NDArray([d[0] for d in delta._data])
            except ValueError:
                # If Hessian is singular, fall back to gradient descent
                x = x - gradient * self.learning_rate
            
            current_value = f(x)
            history.append(current_value)
            
            if abs(history[-1] - history[-2]) < self.tolerance:
                break
                
        return x, history
