from neural_networks.multi_layer_perceptron.activation_function.activation import Activation
from linear_algebra.matrix import Matrix

class ReLU(Activation):
    """
    Q. matrix를 ReLu로 처리한다? 어케?

    A. 
    1. 입력 행렬이 이렇다고 가정,
    input_matrix = Matrix([
        [ 1.2, -0.5,  0.8],
        [-2.0,  3.1, -0.7],
        [ 0.0,  1.5, -1.0]
    ])

    2. ReLU forward 적용 후
    output_matrix = Matrix([
        [1.2, 0.0, 0.8],  # -0.5 -> 0
        [0.0, 3.1, 0.0],  # -2.0, -0.7 -> 0
        [0.0, 1.5, 0.0]   # -1.0 -> 0
    ])

    3. ReLU backward (미분) 적용 후
    gradient_matrix = Matrix([
        [1, 0, 1],  # 양수였던 곳 -> 1
        [0, 1, 0],  # 음수였던 곳 -> 0
        [0, 1, 0]
    ])
    """
    @staticmethod
    def forward(x: Matrix) -> Matrix:
        """Apply ReLU activation to each element"""
        return Matrix([[max(0, x[i][j]) 
                       for j in range(x.cols)]
                       for i in range(x.rows)])


    """
    Q. 이게 어딜봐서 matrix의 gradient 값임?
    A. ReLU 함수는: f(x) = max(0, x)
        이 함수의 미분은:

        x > 0일 때: 1
        x ≤ 0일 때: 0
    """
    @staticmethod
    def backward(x: Matrix) -> Matrix:
        """Compute ReLU derivative for each element"""
        return Matrix([[1 if x[i][j] > 0 else 0 
                       for j in range(x.cols)]
                       for i in range(x.rows)])
