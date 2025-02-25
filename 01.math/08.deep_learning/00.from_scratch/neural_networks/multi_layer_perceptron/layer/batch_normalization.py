from neural_networks.multi_layer_perceptron.layer.layer import Layer
from linear_algebra.matrix import Matrix
import math

"""
Q. why batch normalize?

A. 학습 안정화를 위해.

어케?

ex.
예를 들어 이런 값들이 레이어에 입력된다고 가정
inputs = [100, 200, 300, 400]

BatchNormalization은:
# 1. 평균을 0으로
normalized = [value - mean(inputs) for value in inputs]
결과: [-150, -50, 50, 150]

2. 표준편차를 1로
normalized = normalized / std(normalized)
결과: [-1.34, -0.45, 0.45, 1.34]

이렇게 하면 *모든 값이 비슷한 범위*에 있게 됨

pros
1. Gradient vanishing/exploding 문제 감소
2. 학습 속도 향상

"""

class BatchNormalization(Layer):
    """
    Batch Normalization Layer
    Normalizes the input to have zero mean and unit variance
    """
    def __init__(self, input_size: int, epsilon: float = 1e-8):
        self.epsilon = epsilon
        # Learnable parameters
        self.gamma = Matrix([[1.0] * input_size])  # scale
        self.beta = Matrix([[0.0] * input_size])   # shift
        
        # Cache for backward pass
        self.input_mean = None
        self.input_var = None
        self.normalized = None
        self.inputs = None
        
        # Gradients
        self.gamma_grad = None
        self.beta_grad = None

    def forward(self, inputs: Matrix) -> Matrix:
        self.inputs = inputs
        batch_size = inputs.rows
        
        # Compute mean and variance for each feature
        self.input_mean = inputs.mean(axis=0)
        self.input_var = Matrix([[
            sum((inputs[i][j] - self.input_mean[0][j])**2 
                for i in range(batch_size)) / batch_size
            for j in range(inputs.cols)
        ]])
        
        # Normalize
        self.normalized = (inputs - Matrix([self.input_mean._data[0]] * batch_size)) / \
                         Matrix([[(math.sqrt(self.input_var[0][j] + self.epsilon))
                                for j in range(inputs.cols)]] * batch_size)
        
        # Scale and shift
        return self.normalized * Matrix([self.gamma._data[0]] * batch_size) + \
               Matrix([self.beta._data[0]] * batch_size)

    def backward(self, grad: Matrix) -> Matrix:
        batch_size = self.inputs.rows
        
        # Compute gradients for gamma and beta
        self.gamma_grad = (grad * self.normalized).sum(axis=0)
        self.beta_grad = grad.sum(axis=0)
        
        # Compute gradient for normalized inputs
        normalized_grad = grad * Matrix([self.gamma._data[0]] * batch_size)
        
        # Compute gradient for variance
        var_grad = normalized_grad * (self.inputs - Matrix([self.input_mean._data[0]] * batch_size)) * \
                  -0.5 * Matrix([[1/(math.sqrt(v + self.epsilon)**3) for v in self.input_var._data[0]]] * batch_size)
        
        # Compute gradient for mean
        mean_grad = normalized_grad * -1/Matrix([[math.sqrt(v + self.epsilon) 
                                                for v in self.input_var._data[0]]] * batch_size)
        
        # Compute input gradients
        return normalized_grad * 1/Matrix([[math.sqrt(v + self.epsilon) 
                                          for v in self.input_var._data[0]]] * batch_size) + \
               var_grad * 2 * (self.inputs - Matrix([self.input_mean._data[0]] * batch_size))/batch_size + \
               mean_grad/batch_size

    def update(self, learning_rate: float):
        """Update gamma and beta parameters"""
        self.gamma = self.gamma - Matrix([[learning_rate * g for g in self.gamma_grad._data[0]]])
        self.beta = self.beta - Matrix([[learning_rate * g for g in self.beta_grad._data[0]]])
