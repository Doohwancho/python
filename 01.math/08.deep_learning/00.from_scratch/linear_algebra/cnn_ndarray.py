from typing import List, Union, Tuple, Sequence
import copy

class CNNArray:
    """
    CNN 전용 N차원 배열 클래스임 ㅋㅋ
    기존 NDArray랑 헷갈리지 않게 이름 바꿈
    """
    def __init__(self, data: Sequence, shape: Tuple[int, ...] = None):
        self._data = self._validate_and_copy_data(data, shape)
        self._shape = shape if shape is not None else self._calculate_shape(self._data)
        
    def _validate_and_copy_data(self, data: Sequence, shape: Tuple[int, ...] = None) -> List:
        """데이터 검증하고 복사하는거임"""
        if shape is not None:
            # 데이터 크기가 shape이랑 맞는지 확인
            flat_len = 1
            for dim in shape:
                flat_len *= dim
            if flat_len != self._count_elements(data):
                raise ValueError("데이터 크기가 shape이랑 안맞음 ㅋㅋ")
            
        return copy.deepcopy(data)

    def _count_elements(self, data: Sequence) -> int:
        """전체 원소 개수 세는거임"""
        if not isinstance(data, Sequence) or isinstance(data, str):
            return 1
        return sum(self._count_elements(item) for item in data)
    
    def _calculate_shape(self, data: Sequence) -> Tuple[int, ...]:
        """shape 계산하는거임"""
        shape = []
        current = data
        
        while isinstance(current, Sequence) and not isinstance(current, str):
            shape.append(len(current))
            if len(current) > 0:
                current = current[0]
            else:
                break
                
        return tuple(shape)

    @property
    def shape(self) -> Tuple[int, ...]:
        """shape 속성"""
        return self._shape
    
    def size(self) -> int:
        """첫번째 차원의 크기 반환 (기존 len과 구분)"""
        if self._shape:
            return self._shape[0]
        return 0
    
    def __getitem__(self, idx) -> Union['CNNArray', float]:
        """인덱싱/슬라이싱 구현"""
        if isinstance(idx, tuple):
            # 다차원 인덱싱
            current = self._data
            for i in idx:
                if isinstance(i, slice):
                    # 슬라이스 처리
                    current = current[i]
                    if isinstance(current, list):
                        new_shape = list(self._shape[1:])
                        start = i.start if i.start is not None else 0
                        stop = i.stop if i.stop is not None else self._shape[0]
                        step = i.step if i.step is not None else 1
                        length = len(range(start, stop, step))
                        new_shape.insert(0, length)
                        return CNNArray(current, tuple(new_shape))
                else:
                    current = current[i]
            return current
        else:
            # 단일 차원 인덱싱/슬라이싱
            if isinstance(idx, slice):
                sliced_data = self._data[idx]
                if isinstance(sliced_data, list):
                    start = idx.start if idx.start is not None else 0
                    stop = idx.stop if idx.stop is not None else self._shape[0]
                    step = idx.step if idx.step is not None else 1
                    length = len(range(start, stop, step))
                    new_shape = (length,) + self._shape[1:]
                    return CNNArray(sliced_data, new_shape)
            return self._data[idx]
            
    def __setitem__(self, idx, value):
        """아이템 설정"""
        if isinstance(value, CNNArray):
            value = value._data
        
        if isinstance(idx, tuple):
            current = self._data
            for i in idx[:-1]:
                current = current[i]
            current[idx[-1]] = value
        else:
            self._data[idx] = value
    
    def __add__(self, other: Union['CNNArray', float, int]) -> 'CNNArray':
        """덧셈 연산"""
        if isinstance(other, (float, int)):
            # 스칼라 덧셈
            return self._apply_scalar_op(other, lambda x, y: x + y)
        elif isinstance(other, CNNArray):
            # CNNArray 덧셈
            if self.shape != other.shape:
                raise ValueError("shape이 달라서 더할 수 없음 ㅋㅋ")
            return self._apply_binary_op(other, lambda x, y: x + y)
        else:
            raise TypeError("CNNArray랑 더할 수 없는 타입임 ㅋㅋ")

    def __mul__(self, other: Union['CNNArray', float, int]) -> 'CNNArray':
        """곱셈 연산"""
        if isinstance(other, (float, int)):
            # 스칼라 곱셈
            return self._apply_scalar_op(other, lambda x, y: x * y)
        elif isinstance(other, CNNArray):
            # CNNArray 곱셈
            if self.shape != other.shape:
                raise ValueError("shape이 달라서 곱할 수 없음 ㅋㅋ")
            return self._apply_binary_op(other, lambda x, y: x * y)
        else:
            raise TypeError("CNNArray랑 곱할 수 없는 타입임 ㅋㅋ")
            
    def _apply_scalar_op(self, scalar: Union[float, int], op) -> 'CNNArray':
        """스칼라 연산 적용"""
        def apply_recursive(data):
            if isinstance(data, list):
                return [apply_recursive(x) for x in data]
            return op(data, scalar)
            
        return CNNArray(apply_recursive(self._data), self._shape)
        
    def _apply_binary_op(self, other: 'CNNArray', op) -> 'CNNArray':
        """두 CNNArray 간 연산 적용"""
        def apply_recursive(data1, data2):
            if isinstance(data1, list):
                return [apply_recursive(x, y) for x, y in zip(data1, data2)]
            return op(data1, data2)
            
        return CNNArray(apply_recursive(self._data, other._data), self._shape)
