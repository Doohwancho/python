from typing import List, Union, Tuple, Sequence
import copy

class NDArray:
    """
    N-dimensional array implementation
    """
    def __init__(self, data):
        """
        numpy array를 래핑하는 클래스임 ㅋㅋ
        """
        if isinstance(data, NDArray):
            self.data = data.data
        else:
            self.data = np.array(data)

    def __init__(self, data: Sequence, shape: Tuple[int, ...] = None):
        self._data = self._validate_and_copy_data(data, shape)
        self._shape = self._calculate_shape(self._data)
        self._flatten_data = self._flatten(self._data)
        
    def _validate_and_copy_data(self, data: Sequence, shape: Tuple[int, ...] = None) -> List:
        """Validate input data and ensure consistent shape"""
        if shape is not None:
            # Verify data matches given shape
            flat_len = 1
            for dim in shape:
                flat_len *= dim
            if flat_len != self._count_elements(data):
                raise ValueError("Data size does not match specified shape")
            
        return copy.deepcopy(data)

    def copy(self) -> 'NDArray':
        """Return a deep copy of this array"""
        return NDArray(copy.deepcopy(self._data))

    def __len__(self) -> int:
        """Return total number of elements in array"""
        return len(self._flatten_data)
    
    def _count_elements(self, data: Sequence) -> int:
        """Count total number of elements in nested sequence"""
        if not isinstance(data, Sequence) or isinstance(data, str):
            return 1
        return sum(self._count_elements(item) for item in data)
    
    def _calculate_shape(self, data: Sequence) -> Tuple[int, ...]:
        """Calculate shape of nested sequence"""

        # assuming input 2d array is [[0,1],[1,0]],
        shape = []
        current = data
        
        while isinstance(current, Sequence) and not isinstance(current, str):
            shape.append(len(current)) # 4
            if len(current) > 0:
                current = current[0]   # Takes [0, 0]
                # Next iteration gets 2 (inner list length) 
            else:
                break
                
        return tuple(shape)  # Returns (4, 2) - 4 rows, 2 columns
    
    def _flatten(self, data: Sequence) -> List:
        """Convert nested sequence to flat list"""
        # ex. Converts [[0,0], [0,1], [1,0], [1,1]] 
        # to [0,0,0,1,1,0,1,1]
        if not isinstance(data, Sequence) or isinstance(data, str):
            return [data]
        
        flat_data = []
        for item in data:
            flat_data.extend(self._flatten(item))
        return flat_data

    def _unflatten(self, flat_data: List[float], shape: Tuple[int, ...]) -> List:
        """Convert flat list back to nested structure"""
        if len(shape) == 1:
            return flat_data
        
        result = []
        size = shape[-1]
        for i in range(0, len(flat_data), size):
            result.append(flat_data[i:i + size])
        return result
    
    @property
    def shape(self) -> Tuple[int, ...]:
        return self._shape
    
    @property
    def ndim(self) -> int:
        return len(self._shape)
    
    # Example: reshape (4,2) to (2,4)
    # Checks if total elements match
    # [0,0,0,1,1,0,1,1] -> [[0,0,0,1], [1,0,1,1]]
    def reshape(self, new_shape: Tuple[int, ...]) -> 'NDArray':
        """Reshape array to new dimensions"""
        new_size = 1
        for dim in new_shape:
            new_size *= dim
            
        if new_size != len(self._flatten_data):
            raise ValueError("New shape must have same number of elements")
            
        # Create new nested structure
        new_data = self._flatten_data
        for dim in reversed(new_shape[1:]):
            new_data = [new_data[i:i + dim] for i in range(0, len(new_data), dim)]
            
        return NDArray(new_data, new_shape)
    
    def __getitem__(self, index):
        """Support for multi-dimensional indexing"""
        if isinstance(index, tuple):
            current = self._data
            for idx in index:
                current = current[idx]
            return current
        return self._data[index]

    def __setitem__(self, index: int, value: float):
        """Set value at specified index"""
        self._flatten_data[index] = value
        # Rebuild data structure
        self._data = self._unflatten(self._flatten_data, self._shape)

    
    def __add__(self, other: 'NDArray') -> 'NDArray':
        if self.shape != other.shape:
            raise ValueError("Arrays must have same shape")
            
        result = [a + b for a, b in zip(self._flatten_data, other._flatten_data)]
        return NDArray(result).reshape(self.shape)
    
    def __sub__(self, other: 'NDArray') -> 'NDArray':
        """Subtraction"""
        if not isinstance(other, NDArray):
            return NDArray([x - other for x in self._flatten_data])
        result = [a - b for a, b in zip(self._flatten_data, other._flatten_data)]
        return NDArray(result).reshape(self._shape)

    def __mul__(self, scalar: Union[int, float]) -> 'NDArray':
        result = [x * scalar for x in self._flatten_data]
        return NDArray(result).reshape(self.shape)
    
    def transpose(self) -> 'NDArray':
        """
        Transpose array (currently supports 2D only)
        """
        if self.ndim != 2:
            raise ValueError("Transpose currently only supported for 2D arrays")
            
        rows, cols = self.shape
        transposed = [[self._data[i][j] for i in range(rows)] for j in range(cols)]
        return NDArray(transposed)
