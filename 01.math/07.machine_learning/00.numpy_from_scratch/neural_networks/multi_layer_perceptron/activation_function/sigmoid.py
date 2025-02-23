# neural_network/activation_function/sigmoid.py
from neural_networks.multi_layer_perceptron.activation_function.activation import Activation
from linear_algebra.matrix import Matrix
import math

class Sigmoid(Activation):
    @staticmethod
    def forward(x: Matrix) -> Matrix:
        def sigmoid(x):
            if x < -700:  # prevent overflow
                return 0
            elif x > 700:
                return 1
            return 1 / (1 + math.exp(-x))
            
        return Matrix([[sigmoid(x[i][j]) 
                       for j in range(x.cols)]
                       for i in range(x.rows)])

    @staticmethod
    def backward(x: Matrix) -> Matrix:
        # Sigmoid derivative is s(x) * (1 - s(x))
        s = Sigmoid.forward(x)
        return Matrix([[s[i][j] * (1 - s[i][j]) 
                       for j in range(s.cols)]
                       for i in range(s.rows)])
