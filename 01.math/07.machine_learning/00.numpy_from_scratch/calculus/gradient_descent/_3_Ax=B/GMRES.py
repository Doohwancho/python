class GMRES(IterativeSolver):
    """
    Generalized Minimal Residual method for solving Ax = b
    Works for non-symmetric matrices
    """
    def _arnoldi(self, A: Matrix, v: List[float], k: int) -> Tuple[List[List[float]], List[List[float]]]:
        """
        Arnoldi iteration to build orthonormal basis of Krylov subspace
        Returns: (H, Q) where H is Hessenberg matrix and Q is orthonormal basis
        """
        n = len(v)
        Q = [v]  # Orthonormal basis vectors
        H = [[0.0] * (k+1) for _ in range(k)]  # Hessenberg matrix
        
        for j in range(k):
            # Compute Aq
            q = Q[j]
            Aq = [sum(A[i][l] * q[l] for l in range(n)) for i in range(n)]
            
            # Orthogonalize against previous vectors
            for i in range(j + 1):
                H[j][i] = self._dot(Aq, Q[i])
                for l in range(n):
                    Aq[l] -= H[j][i] * Q[i][l]
            
            # Normalize
            H[j][j+1] = self._norm(Aq)
            if H[j][j+1] > self.tolerance:
                Q.append([x / H[j][j+1] for x in Aq])
            else:
                break
                
        return H, Q

    def _solve_least_squares(self, H: List[List[float]], b: List[float]) -> List[float]:
        """Solve min ||Hy - b|| using QR decomposition"""
        m = len(H)
        n = len(H[0])
        
        # Apply Givens rotations to create upper triangular system
        Q = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
        R = [row[:] for row in H]
        
        for i in range(m-1):
            for j in range(i+1, m):
                if abs(R[j][i]) > self.tolerance:
                    # Compute Givens rotation
                    r = math.sqrt(R[i][i]**2 + R[j][i]**2)
                    c = R[i][i] / r
                    s = -R[j][i] / r
                    
                    # Apply to R and Q
                    for k in range(n):
                        temp = R[i][k]
                        R[i][k] = c * temp - s * R[j][k]
                        R[j][k] = s * temp + c * R[j][k]
                    
                    for k in range(m):
                        temp = Q[i][k]
                        Q[i][k] = c * temp - s * Q[j][k]
                        Q[j][k] = s * temp + c * Q[j][k]
        
        # Back substitution
        y = [0.0] * n
        for i in range(m-1, -1, -1):
            y[i] = b[i]
            for j in range(i+1, n):
                y[i] -= R[i][j] * y[j]
            y[i] /= R[i][i]
            
        return y

    def solve(self, A: Matrix, b: List[float], x0: List[float] = None) -> Tuple[List[float], List[float]]:
        """
        Solve Ax = b using GMRES with restarts
        Returns: (solution, residual_history)
        """
        n = len(b)
        x = x0 if x0 is not None else [0.0] * n
        
        residual_history = []
        restart_size = min(n, 50)  # Maximum Krylov subspace size
        
        for restart in range(self.max_iterations):
            # Compute initial residual
            r = [bi - sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
            beta = self._norm(r)
            
            if beta < self.tolerance:
                break
                
            residual_history.append(beta)
            v = [ri / beta for ri in r]
            
            # Build Krylov subspace
            H, Q = self._arnoldi(A, v, restart_size)
            
            # Solve least squares problem
            y = self._solve_least_squares(H, [beta] + [0.0] * (restart_size - 1))
            
            # Update solution
            for i in range(n):
                for j in range(len(y)):
                    x[i] += y[j] * Q[j][i]
                    
        return x, residual_history
