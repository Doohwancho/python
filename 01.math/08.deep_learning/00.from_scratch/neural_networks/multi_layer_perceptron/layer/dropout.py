from neural_networks.multi_layer_perceptron.layer.layer import Layer
from linear_algebra.matrix import Matrix
import random

"""
Q. why use dropout?
A. prevent overfitting

how?

훈련 중:
nodes = [0.2, 0.5, 0.8, 0.3]
dropout_mask = [1, 0, 1, 0]  # '랜덤'하게 일부 노드를 0으로 (20% 확률)
result = [0.2, 0, 0.8, 0]    # 일부 노드의 출력을 '무시'


1. 매 훈련 단계마다 랜덤하게 일부 노드를 비활성화
2. 네트워크가 특정 노드에 너무 의존하는 것을 방지
3. 여러 feature의 조합을 학습하도록 강제


"""


class Dropout(Layer):
    """
    Dropout Layer
    Randomly sets a fraction of inputs to zero during training
    """
    def __init__(self, dropout_rate: float = 0.5):
        self.dropout_rate = dropout_rate
        self.mask = None
        self.training = True

    def forward(self, inputs: Matrix) -> Matrix:
        if not self.training:
            return inputs
            
        # Generate dropout mask
        self.mask = Matrix([[1 if random.random() > self.dropout_rate else 0 
                            for _ in range(inputs.cols)] 
                            for _ in range(inputs.rows)])
        
        # Scale the outputs
        scale = 1/(1 - self.dropout_rate)
        return inputs * self.mask * scale

    def backward(self, grad: Matrix) -> Matrix:
        return grad * self.mask * (1/(1 - self.dropout_rate))

    def update(self, learning_rate: float):
        """Dropout layer has no parameters to update"""
        pass
