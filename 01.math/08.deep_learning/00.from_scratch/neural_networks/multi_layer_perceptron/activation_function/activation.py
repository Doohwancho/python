from linear_algebra.matrix import Matrix

class Activation:
    """Base class for activation functions"""
    @staticmethod
    def forward(x: Matrix) -> Matrix:
        raise NotImplementedError
    
    @staticmethod
    def backward(x: Matrix) -> Matrix:
        raise NotImplementedError
