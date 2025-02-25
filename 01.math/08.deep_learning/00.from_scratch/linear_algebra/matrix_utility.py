class MatrixUtilities:
    @staticmethod
    def condition_number(A: Matrix) -> float:
        """
        Estimate condition number using power iteration
        """
        # Estimate largest singular value
        sigma_max, _ = A.power_iteration()
        
        # Estimate smallest singular value
        AtA = A.transpose() @ A
        lambda_min = 1.0
        v = [random.random() for _ in range(A.cols)]
        
        for _ in range(100):
            w = [sum(AtA[i][j] * v[j] for j in range(A.cols)) 
                 for i in range(A.cols)]
            lambda_min = sum(v[i] * w[i] for i in range(A.cols))
            norm = math.sqrt(sum(w[i] * w[i] for i in range(A.cols)))
            v = [w[i] / norm for i in range(A.cols)]
            
        sigma_min = math.sqrt(lambda_min)
        return sigma_max / sigma_min

    @staticmethod
    def balance_matrix(A: Matrix) -> Tuple[Matrix, List[float]]:
        """
        Balance matrix to improve condition number
        Returns: (balanced_matrix, scaling_factors)
        """
        n = A.rows
        done = [False] * n
        scaling = [1.0] * n
        
        while not all(done):
            done = [True] * n
            for i in range(n):
                # Compute row and column norms
                row_norm = sum(abs(A[i][j]) for j in range(n))
                col_norm = sum(abs(A[j][i]) for j in range(n))
                
                if row_norm > 0 and col_norm > 0:
                    # Compute scaling factor
                    f = math.sqrt(row_norm / col_norm)
                    if abs(f - 1.0) > 0.1:
                        done[i] = False
                        scaling[i] *= f
                        
                        # Apply scaling
                        for j in range(n):
                            A[i][j] /= f
                            A[j][i] *= f
                            
        return A, scaling
