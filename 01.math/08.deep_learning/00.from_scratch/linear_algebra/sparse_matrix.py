from typing import Dict, Tuple, List, Optional
import itertools

"""
Q. what is sparse matrix?

A sparse matrix is a matrix where most elements are zero. 
Instead of storing all zeros, 
it only stores non-zero values to save memory.


ex)
# Regular Matrix (stores all values)
regular = [
    [1, 0, 0, 0, 2],
    [0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0],
    [4, 0, 0, 5, 0]
]

# Sparse Matrix (stores only non-zero values)
sparse = {
    (0,0): 1,  # row 0, col 0: value 1
    (0,4): 2,  # row 0, col 4: value 2
    (1,2): 3,  # row 1, col 2: value 3
    (3,0): 4,  # row 3, col 0: value 4
    (3,3): 5   # row 3, col 3: value 5
}
"""

class SparseMatrix:
    """
    Compressed Sparse Row (CSR) matrix implementation
    Efficient for large, sparse matrices
    """
    def __init__(self, shape: Tuple[int, int], data: Dict[Tuple[int, int], float] = None):
        self.shape = shape
        self.rows, self.cols = shape
        self._data = {} if data is None else data.copy()
        
        # CSR format components
        self._csr_initialized = False
        self._values: List[float] = []
        self._col_indices: List[int] = []
        self._row_pointers: List[int] = []
        
    def _to_csr(self):
        """Convert dictionary format to CSR format"""
        if self._csr_initialized:
            return
            
        # Sort elements by row, then column
        sorted_elements = sorted(self._data.items(), 
                               key=lambda x: (x[0][0], x[0][1]))
        
        self._values = []
        self._col_indices = []
        self._row_pointers = [0]
        current_row = 0
        
        for (row, col), value in sorted_elements:
            # Fill in empty rows
            while current_row < row:
                self._row_pointers.append(len(self._values))
                current_row += 1
            
            self._values.append(value)
            self._col_indices.append(col)
            
        # Fill in remaining empty rows
        while current_row < self.rows:
            self._row_pointers.append(len(self._values))
            current_row += 1
            
        self._row_pointers.append(len(self._values))
        self._csr_initialized = True
        
    def __getitem__(self, key: Tuple[int, int]) -> float:
        """Get value at specified position"""
        return self._data.get(key, 0.0)
        
    def __setitem__(self, key: Tuple[int, int], value: float):
        """Set value at specified position"""
        if abs(value) < 1e-10:  # Don't store near-zero values
            self._data.pop(key, None)
        else:
            self._data[key] = value
        self._csr_initialized = False
        
    def __matmul__(self, other: 'SparseMatrix') -> 'SparseMatrix':
        """Matrix multiplication optimized for sparse matrices"""
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions don't match")
            
        result = SparseMatrix((self.rows, other.cols))
        
        # Convert both matrices to CSR format
        self._to_csr()
        other._to_csr()
        
        # Multiply
        for i in range(self.rows):
            row_start = self._row_pointers[i]
            row_end = self._row_pointers[i + 1]
            
            for j in range(other.cols):
                # Compute dot product of row i and column j
                value = 0.0
                for k in range(row_start, row_end):
                    col_i = self._col_indices[k]
                    val_i = self._values[k]
                    
                    # Find matching element in other matrix
                    other_row_start = other._row_pointers[col_i]
                    other_row_end = other._row_pointers[col_i + 1]
                    
                    for l in range(other_row_start, other_row_end):
                        if other._col_indices[l] == j:
                            value += val_i * other._values[l]
                            break
                
                if abs(value) >= 1e-10:
                    result[i, j] = value
                    
        return result
