"""
dense 클래스의 abstract class가 layer 
"""

class Layer:
    """Base class for neural network layers"""
    def forward(self, inputs):
        raise NotImplementedError
        
    def backward(self, grad):
        raise NotImplementedError
        
    def update(self, learning_rate):
        raise NotImplementedError
