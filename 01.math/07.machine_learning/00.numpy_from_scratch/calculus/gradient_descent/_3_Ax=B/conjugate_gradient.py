"""
It's an optimization method designed specifically for solving linear systems Ax = b
Instead of going in the direction of steepest descent (like regular gradient descent), it uses directions that are A-conjugate
Two vectors d₁ and d₂ are A-conjugate if d₁ᵀAd₂ = 0
Main advantage: It's particularly efficient for large, sparse systems because:

Doesn't need to store the full Hessian matrix
Can find the exact solution in n iterations (where n is dimension)
Each step produces the optimal solution in a growing subspace
"""
class ConjugateGradient(IterativeSolver):
    """
    Conjugate Gradient method for solving Ax = b
    where A is symmetric positive definite
    """
    def solve(self, A: Matrix, b: List[float], x0: List[float] = None) -> Tuple[List[float], List[float]]:
        """
        Solve Ax = b starting from x0
        Returns: (solution, residual_history)
        """
        n = len(b)
        x = x0 if x0 is not None else [0.0] * n
        
        # Initial residual r = b - Ax
        r = [bi - sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
        p = r.copy()
        
        residual_history = [self._norm(r)]
        
        for k in range(self.max_iterations):
            # Compute Ap
            Ap = [sum(A[i][j] * p[j] for j in range(n)) for i in range(n)]
            
            # Compute step size
            r_norm_sq = self._dot(r, r)
            alpha = r_norm_sq / self._dot(p, Ap)
            
            # Update solution and residual
            for i in range(n):
                x[i] += alpha * p[i]
                r[i] -= alpha * Ap[i]
            
            # Check convergence
            r_norm = self._norm(r)
            residual_history.append(r_norm)
            if r_norm < self.tolerance:
                break
                
            # Update search direction
            beta = self._dot(r, r) / r_norm_sq
            for i in range(n):
                p[i] = r[i] + beta * p[i]
                
        return x, residual_history
