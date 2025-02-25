from typing import List, Union, Tuple, Sequence, Optional
from linear_algebra.ndarray import NDArray
import math
import itertools

# Q. what functions there are, and for what?

######################################
# Ch.1 basic matrix operations
######################################

# 1. Basic Properties and Access:

# __init__: Creates matrix, ensures it's 2D
# rows, cols: Get number of rows/columns
# __len__: Returns number of rows
# __str__: Converts matrix to string format
# __getitem__: Allows accessing elements with [] notation


# 2. Basic Arithmetic:

# __add__: Matrix addition (A + B)
# __sub__: Matrix subtraction (A - B)
# __mul__: Element-wise multiplication and scalar multiplication (A * B or A * 2)
# __truediv__: Element-wise division (A / B or A / 2)
# __matmul__: Matrix multiplication (A @ B)


# 3. Shape Manipulation:

# transpose: Flips matrix over diagonal
# reshape: Changes matrix dimensions
# broadcast_to: Expands matrix to larger shape



######################################
# Ch.2 Statistics and analysis 
######################################

# mean: Calculates average along axis
# sum: Sums elements along axis
# covariance: Computes covariance matrix
# correlation: Computes correlation matrix


######################################
# Ch.3 Matrix Decomposition
######################################

# 1. Common Decompositions:

# svd, svd2: Singular Value Decomposition
# lu_decomposition: LU decomposition
# qr_decomposition: QR decomposition
# cholesky_decomposition: Cholesky decomposition


# 2. Eigenvalue Methods:

# power_iteration: Finds largest eigenvalue/vector
# eigenvalues_qr: Finds all eigenvalues


######################################
# Ch.4 Utility Functions
######################################

# Matrix Properties:
# determinant: Calculates matrix determinant
# inverse: Finds matrix inverse

# Linear System Solving:
# solve_lu: Solves Ax = b using LU decomposition



class Matrix(NDArray):
    """
    Matrix class extending NDArray with specific matrix operations
    """
    def __init__(self, data: Sequence):
        super().__init__(data)
        if self.ndim != 2:
            raise ValueError("Matrix must be 2-dimensional")
            
    @property
    def rows(self) -> int:
        """Number of rows in the array"""
        return self.shape[0]
        
    @property
    def cols(self) -> int:
        """Number of columns in the array"""
        return self.shape[1]

    def __len__(self) -> int:
        """Return number of rows in matrix"""
        return self.rows

    def __str__(self) -> str:
        """String representation of matrix"""
        return '\n'.join([str(row) for row in self._data])

    def transpose(self) -> 'NDArray':
        """
        Transpose array (currently supports 2D only)
        """
        if self.ndim != 2:
            raise ValueError("Transpose currently only supported for 2D arrays")
            
        rows, cols = self.shape
        transposed = [[self._data[i][j] for i in range(rows)] 
                      for j in range(cols)]
        return type(self)(transposed)  # Returns same type as self (Matrix or NDArray)

    def __add__(self, other: 'Matrix') -> 'Matrix':
        """Matrix addition"""
        if self.shape != other.shape:
            # Try broadcasting
            if other.rows == 1:
                other = Matrix([other._data[0] for _ in range(self.rows)])
            else:
                raise ValueError(f"Cannot broadcast shapes {self.shape} and {other.shape}")
        
        # Add matrices element-wise
        result = [[self[i][j] + other[i][j] 
                  for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def __mul__(self, other: Union['Matrix', float, int]) -> 'Matrix':
        """Element-wise multiplication (Hadamard product) or scalar multiplication"""
        if isinstance(other, (int, float)):
            # Scalar multiplication
            result = [[self[i][j] * other 
                      for j in range(self.cols)]
                      for i in range(self.rows)]
            return Matrix(result)
        
        # Matrix multiplication (element-wise)
        if self.shape != other.shape:
            # Try broadcasting
            # Q. what is broadcasting?
            # A. __truediv__()에 적은 주석을 보라!
            if other.rows == 1:
                other = Matrix([other._data[0] for _ in range(self.rows)])
            else:
                raise ValueError(f"Cannot broadcast shapes {self.shape} and {other.shape}")
        
        result = [[self[i][j] * other[i][j] 
                  for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def __rmul__(self, other: Union[float, int]) -> 'Matrix':
        """Right scalar multiplication (scalar * matrix)"""
        return self.__mul__(other)

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        """Matrix subtraction"""
        if self.shape != other.shape:
            # Try broadcasting
            if other.rows == 1:
                other = Matrix([other._data[0] for _ in range(self.rows)])
            else:
                raise ValueError(f"Cannot broadcast shapes {self.shape} and {other.shape}")
        
        result = [[self[i][j] - other[i][j] 
                  for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def __truediv__(self, other: Union['Matrix', float, int]) -> 'Matrix':
        """Matrix division (element-wise)"""
        if isinstance(other, (int, float)):
            result = [[self[i][j] / other 
                      for j in range(self.cols)]
                      for i in range(self.rows)]
            return Matrix(result)
        
        # Q. what is broadcasting?
        # matrix_a / matrix_b 할 때, shape이 다르면?
        
        # A = Matrix([[1, 2, 3],    # shape: (2, 3)
        #    [4, 5, 6]])

        # B = Matrix([[10, 20, 30]])  # shape: (1, 3)

        # 나누기가 안됨. 따라서 B의 shape을 바꿔주는게 broadcasting.
        # B is broadcasted to:
        # B_broadcasted = Matrix([[10, 20, 30],   # shape: (2, 3)
        #                     [10, 20, 30]])   # Row is repeated

        # Then division happens element-wise:
        # Result = [[1/10, 2/20, 3/30],
        #         [4/10, 5/20, 6/30]]

        if self.shape != other.shape:
            # Try broadcasting
            if other.rows == 1:
                other = Matrix([other._data[0] for _ in range(self.rows)]) #broad casting 한다. smaller shaped matrix to match larger matrix 
            else:
                raise ValueError(f"Cannot broadcast shapes {self.shape} and {other.shape}")
        
        result = [[self[i][j] / other[i][j] 
                  for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def sum(self, axis: Optional[int] = None) -> Union['Matrix', float]:
        """
        Sum elements along specified axis
        axis=None: sum all elements
        axis=0: sum along rows (columns remain)
        axis=1: sum along columns (rows remain)
        """
        if axis is None:
            # Sum all elements
            return sum(sum(row) for row in self._data)
        
        elif axis == 0:
            # Sum along rows (result has shape (1, cols))
            col_sums = [sum(self[i][j] for i in range(self.rows))
                       for j in range(self.cols)]
            return Matrix([col_sums])
            
        elif axis == 1:
            # Sum along columns (result has shape (rows, 1))
            row_sums = [[sum(row)] for row in self._data]
            return Matrix(row_sums)
            
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def broadcast_to(self, shape: Tuple[int, int]) -> 'Matrix':
        """Broadcast matrix to new shape"""
        if shape == self.shape:
            return self
            
        if self.rows == 1:
            return Matrix([self._data[0] for _ in range(shape[0])])
        elif self.cols == 1:
            return Matrix([[row[0] for _ in range(shape[1])] for row in self._data])
        else:
            raise ValueError(f"Cannot broadcast shape {self.shape} to {shape}")

        
    def __matmul__(self, other: 'Matrix') -> 'Matrix':
        """Matrix multiplication using @ operator"""
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions do not match for multiplication")
            
        result = [[sum(self[i][k] * other[k][j] 
                      for k in range(self.cols))
                  for j in range(other.cols)]
                  for i in range(self.rows)]
        return Matrix(result)
    
    def determinant(self) -> float:
        """
        Calculate matrix determinant using recursive definition
        Note: This is not efficient for large matrices
        """
        if self.rows != self.cols:
            raise ValueError("Determinant only defined for square matrices")
            
        if self.rows == 1:
            return self[0][0]
        if self.rows == 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]
            
        det = 0
        for j in range(self.cols):
            det += ((-1) ** j) * self[0][j] * self._minor(0, j).determinant()
        return det
    
    def _minor(self, i: int, j: int) -> 'Matrix':
        """Return matrix minor (matrix with row i and column j removed)"""
        return Matrix([[self[r][c] for c in range(self.cols) if c != j]
                      for r in range(self.rows) if r != i])

    def inverse(self) -> 'Matrix':
        """
        Calculate matrix inverse using Gauss-Jordan elimination
        """
        if self.rows != self.cols:
            raise ValueError("Only square matrices are invertible")
            
        n = self.rows
        # Augment matrix with identity matrix
        aug = [[self[i][j] for j in range(n)] + [1 if i == j else 0 for j in range(n)]
               for i in range(n)]
        
        # Gaussian elimination
        for i in range(n):
            # Find pivot
            pivot = aug[i][i]
            if abs(pivot) < 1e-10:
                raise ValueError("Matrix is singular")
                
            # Divide row by pivot
            for j in range(2*n):
                aug[i][j] /= pivot
                
            # Eliminate column
            for k in range(n):
                if k != i:
                    factor = aug[k][i]
                    for j in range(2*n):
                        aug[k][j] -= factor * aug[i][j]
        
        # Extract inverse matrix
        inverse = [[aug[i][j+n] for j in range(n)] for i in range(n)]
        return Matrix(inverse)

    def power_iteration(self, num_iterations: int = 100, tolerance: float = 1e-10) -> Tuple[float, List[float]]:
        """
        Find the dominant eigenvalue and eigenvector using power iteration method
        Returns: (eigenvalue, eigenvector)
        """
        if self.rows != self.cols:
            raise ValueError("Only square matrices support eigendecomposition")
            
        n = self.rows
        # Start with random vector
        vector = [1/math.sqrt(n)] * n
        
        for _ in range(num_iterations):
            # Multiply matrix by vector
            new_vector = [sum(self[i][j] * vector[j] for j in range(n))
                         for i in range(n)]
            
            # Calculate magnitude
            magnitude = math.sqrt(sum(x*x for x in new_vector))
            
            # Normalize
            new_vector = [x/magnitude for x in new_vector]
            
            # Check convergence
            if all(abs(new_vector[i] - vector[i]) < tolerance for i in range(n)):
                break
                
            vector = new_vector
            
        # Calculate eigenvalue using Rayleigh quotient
        eigenvalue = sum(sum(self[i][j] * vector[j] * vector[i] 
                           for j in range(n)) for i in range(n))
        
        return eigenvalue, vector

    def qr_decomposition(self) -> Tuple['Matrix', 'Matrix']:
        """
        Compute QR decomposition using Gram-Schmidt process
        Returns: (Q, R) where Q is orthogonal and R is upper triangular
        """
        n = self.rows
        m = self.cols
        
        Q = [[0.0] * m for _ in range(n)]
        R = [[0.0] * m for _ in range(m)]
        
        # Gram-Schmidt process
        for j in range(m):
            # Copy column j
            v = [self[i][j] for i in range(n)]
            
            for k in range(j):
                # Calculate dot product
                dot = sum(Q[i][k] * self[i][j] for i in range(n))
                R[k][j] = dot
                
                # Subtract projection
                for i in range(n):
                    v[i] -= dot * Q[i][k]
            
            # Normalize
            norm = math.sqrt(sum(x*x for x in v))
            if norm < 1e-10:
                raise ValueError("Matrix columns are linearly dependent")
                
            R[j][j] = norm
            for i in range(n):
                Q[i][j] = v[i] / norm
        
        return Matrix(Q), Matrix(R)
    

    def eigenvalues_qr(self, num_iterations: int = 100, tolerance: float = 1e-10) -> List[float]:
        """
        Find all eigenvalues using QR iteration method
        """
        if self.rows != self.cols:
            raise ValueError("Only square matrices support eigendecomposition")
            
        A = Matrix(self._data)  # Make a copy
        n = self.rows
        
        for _ in range(num_iterations):
            Q, R = A.qr_decomposition()
            new_A = R @ Q  # Matrix multiplication
            
            # Check convergence
            if all(abs(new_A[i][j]) < tolerance 
                   for i in range(n) for j in range(i)):
                break
                
            A = new_A
        
        # Return diagonal elements (eigenvalues)
        return [A[i][i] for i in range(n)]

    def mean(self, axis: int = None) -> Union['Matrix', float]:
        """Calculate mean along specified axis"""
        if axis is None:
            return sum(sum(row) for row in self._data) / (self.rows * self.cols)
        
        if axis == 0:  # Along columns
            col_sums = [sum(self[i][j] for i in range(self.rows))
                       for j in range(self.cols)]
            return Matrix([col_sums]) * (1.0 / self.rows)
        
        if axis == 1:  # Along rows
            row_sums = [sum(row) for row in self._data]
            return Matrix([[x] for x in row_sums]) * (1.0 / self.cols)
        
        raise ValueError("Axis must be 0, 1, or None")


    def lu_decomposition(self) -> Tuple['Matrix', 'Matrix', List[int]]:
        """
        Compute LU decomposition with partial pivoting
        Returns: (L, U, P) where P*A = L*U
        L is lower triangular with unit diagonal
        U is upper triangular
        P is permutation list
        """
        if self.rows != self.cols:
            raise ValueError("LU decomposition requires square matrix")
            
        n = self.rows
        L = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        U = [[self[i][j] for j in range(n)] for i in range(n)]
        P = list(range(n))  # Permutation vector
        
        for k in range(n-1):
            # Find pivot
            pivot_value = abs(U[k][k])
            pivot_row = k
            for i in range(k+1, n):
                if abs(U[i][k]) > pivot_value:
                    pivot_value = abs(U[i][k])
                    pivot_row = i
            
            if pivot_value < 1e-10:
                raise ValueError("Matrix is singular")
                
            # Swap rows if necessary
            if pivot_row != k:
                U[k], U[pivot_row] = U[pivot_row], U[k]
                L[k], L[pivot_row] = L[pivot_row], L[k]
                P[k], P[pivot_row] = P[pivot_row], P[k]
                
            # Eliminate below pivot
            for i in range(k+1, n):
                factor = U[i][k] / U[k][k]
                L[i][k] = factor
                for j in range(k, n):
                    U[i][j] -= factor * U[k][j]
                    
        return Matrix(L), Matrix(U), P

    def solve_lu(self, b: List[float]) -> List[float]:
        """
        Solve system Ax = b using LU decomposition
        """
        L, U, P = self.lu_decomposition()
        n = self.rows
        
        # Apply permutation to b
        b_perm = [b[P[i]] for i in range(n)]
        
        # Forward substitution (Ly = b)
        y = [0] * n
        for i in range(n):
            y[i] = b_perm[i]
            for j in range(i):
                y[i] -= L[i][j] * y[j]
                
        # Back substitution (Ux = y)
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = y[i]
            for j in range(i+1, n):
                x[i] -= U[i][j] * x[j]
            x[i] /= U[i][i]
            
        return x

    def cholesky_decomposition(self) -> 'Matrix':
        """
        Compute Cholesky decomposition for positive definite matrix
        Returns lower triangular matrix L where A = L * L^T
        """
        if self.rows != self.cols:
            raise ValueError("Cholesky decomposition requires square matrix")
            
        n = self.rows
        L = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i+1):
                sum_k = sum(L[i][k] * L[j][k] for k in range(j))
                
                if i == j:
                    # Diagonal elements
                    value = self[i][i] - sum_k
                    if value <= 0:
                        raise ValueError("Matrix is not positive definite")
                    L[i][j] = math.sqrt(value)
                else:
                    # Off-diagonal elements
                    L[i][j] = (self[i][j] - sum_k) / L[j][j]
                    
        return Matrix(L)
    
    # 통계

    def covariance(self) -> 'Matrix':
        """
        Calculate covariance matrix
        Assumes features are in columns, samples in rows
        """
        n = self.rows
        # Center the data
        means = self.mean(axis=0)
        centered = self - Matrix([means._data[0]] * n)
        
        # Calculate covariance
        # Q. whats that @ sign in python?
        # A. @ is matrix multiplication in python
        # A = Matrix([[1, 2],
        #     [3, 4]])

        # B = Matrix([[5, 6],
        #             [7, 8]])

        # # Element-wise multiplication (*)
        # A * B = Matrix([[1*5, 2*6],
        #                 [3*7, 4*8]])
        #     = Matrix([[5, 12],
        #                 [21, 32]])

        # # Matrix multiplication (@)
        # A @ B = Matrix([[1*5 + 2*7, 1*6 + 2*8],
        #                 [3*5 + 4*7, 3*6 + 4*8]])
        #     = Matrix([[19, 22],
        #                 [43, 50]])
        return (centered.transpose() @ centered) * (1.0 / (n - 1))

    def correlation(self) -> 'Matrix':
        """Calculate correlation matrix"""
        # 1. Get standard deviations (sqrt of diagonal elements in covariance matrix)
        cov = self.covariance()

        # Calculate standard deviations
        std = Matrix([[math.sqrt(cov[i][i]) for i in range(cov.rows)]])
        std_matrix = std.transpose() @ std
        
        return Matrix([[cov[i][j] / std_matrix[i][j]
                       for j in range(cov.cols)]
                      for i in range(cov.rows)])



    def svd(self, num_iterations: int = 100, tolerance: float = 1e-10) -> Tuple['Matrix', 'Matrix', 'Matrix']:
        """
        Compute Singular Value Decomposition using power iteration method
        Returns: (U, Σ, V^T) where A = U * Σ * V^T
        """
        A = self
        m, n = A.shape
        
        # Compute V and singular values using eigendecomposition of A^T * A
        ATA = A.transpose() @ A
        eigenvalues, V = [], []
        
        for i in range(min(m, n)):
            # Find largest remaining eigenvalue/vector
            lambda_i, v_i = ATA.power_iteration(num_iterations, tolerance)
            if lambda_i < tolerance:
                break
                
            eigenvalues.append(math.sqrt(lambda_i))  # singular values
            V.append(v_i)
            
            # Deflate matrix
            v_matrix = Matrix([v_i]).transpose()
            ATA = ATA - Matrix([v_i]).transpose() @ Matrix([v_i]) * lambda_i
        
        # Construct Σ (diagonal matrix of singular values)
        k = len(eigenvalues)
        Sigma = [[eigenvalues[i] if i == j else 0 for j in range(n)] for i in range(m)]
        
        # Compute U using A * v / σ
        U = []
        for i in range(k):
            u_i = (A @ Matrix([V[i]]).transpose())._data
            u_i = [x[0] / eigenvalues[i] for x in u_i]
            U.append(u_i)
        
        # Pad U with orthogonal vectors if necessary
        while len(U) < m:
            # Generate random vector and orthogonalize
            u_new = [random.random() for _ in range(m)]
            for u_i in U:
                dot_product = sum(a * b for a, b in zip(u_new, u_i))
                u_new = [u_new[j] - dot_product * u_i[j] for j in range(m)]
            
            # Normalize
            norm = math.sqrt(sum(x*x for x in u_new))
            if norm > tolerance:
                U.append([x/norm for x in u_new])
        
        return Matrix(U), Matrix(Sigma), Matrix(V)


    def svd2(self, max_iterations: int = 100, tolerance: float = 1e-10) -> Tuple['Matrix', 'Matrix', 'Matrix']:
        """
        Compute Singular Value Decomposition using two-sided Jacobi iteration method
        Returns (U, Σ, V^T) where A = U * Σ * V^T
        U and V are orthogonal matrices
        Σ is diagonal matrix with singular values
        """
        m, n = self.shape
        A = Matrix(self._data)  # Make a copy
        
        # Initialize U and V as identity matrices
        U = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
        V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        
        for iteration in range(max_iterations):
            max_change = 0.0
            
            # Sweep through all pairs of columns
            for i, j in itertools.combinations(range(n), 2):
                # Compute 2x2 SVD for columns i and j
                # Get relevant vectors
                x = [A[k][i] for k in range(m)]
                y = [A[k][j] for k in range(m)]
                
                # Compute elements of normal equations
                a = sum(xk * xk for xk in x)
                b = sum(xk * yk for xk, yk in zip(x, y))
                c = sum(yk * yk for yk in y)
                
                # Compute rotation angles
                if abs(b) < tolerance * math.sqrt(a * c):
                    continue
                    
                tau = (c - a) / (2.0 * b)
                t = math.copysign(1.0, tau) / (abs(tau) + math.sqrt(1.0 + tau * tau))
                cs = 1.0 / math.sqrt(1.0 + t * t)
                sn = cs * t
                
                # Update columns
                for k in range(m):
                    temp = A[k][i]
                    A[k][i] = cs * temp - sn * A[k][j]
                    A[k][j] = sn * temp + cs * A[k][j]
                    
                    # Update U
                    temp = U[k][i]
                    U[k][i] = cs * temp - sn * U[k][j]
                    U[k][j] = sn * temp + cs * U[k][j]
                    
                # Update V
                for k in range(n):
                    temp = V[k][i]
                    V[k][i] = cs * temp - sn * V[k][j]
                    V[k][j] = sn * temp + cs * V[k][j]
                    
                max_change = max(max_change, abs(b))
            
            # Check convergence
            if max_change < tolerance:
                break
        
        # Construct Σ (diagonal matrix with singular values)
        Sigma = [[0.0] * n for _ in range(m)]
        for i in range(min(m, n)):
            Sigma[i][i] = math.sqrt(sum(A[k][i] * A[k][i] for k in range(m)))
            
            # Ensure U and V have correct orientation
            if Sigma[i][i] != 0:
                for k in range(m):
                    U[k][i] *= math.copysign(1.0, A[0][i])
                for k in range(n):
                    V[k][i] *= math.copysign(1.0, A[0][i])
        
        return Matrix(U), Matrix(Sigma), Matrix(V).transpose()

    def gram_schmidt(self) -> Tuple['Matrix', 'Matrix']:
        """
        Compute QR decomposition using modified Gram-Schmidt
        Returns (Q, R) where Q is orthogonal and R is upper triangular
        """
        m, n = self.shape
        Q = [[0.0] * n for _ in range(m)]
        R = [[0.0] * n for _ in range(n)]
        
        for j in range(n):
            # Copy column j
            v = [self[i][j] for i in range(m)]
            
            for k in range(j):
                # Compute dot product
                R[k][j] = sum(Q[i][k] * self[i][j] for i in range(m))
                
                # Subtract projection
                for i in range(m):
                    v[i] -= R[k][j] * Q[i][k]
            
            # Compute norm
            R[j][j] = math.sqrt(sum(x * x for x in v))
            
            if R[j][j] > self.tolerance:
                # Normalize column
                for i in range(m):
                    Q[i][j] = v[i] / R[j][j]
            else:
                # Handle linear dependence
                R[j][j] = 0.0
                Q[i][j] = 0.0
                
        return Matrix(Q), Matrix(R)
