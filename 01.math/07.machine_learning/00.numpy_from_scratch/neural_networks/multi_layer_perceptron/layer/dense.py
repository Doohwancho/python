
from neural_networks.multi_layer_perceptron.layer.layer import Layer  
from neural_networks.multi_layer_perceptron.activation_function.activation import Activation
from linear_algebra.matrix import Matrix
from linear_algebra.ndarray import NDArray
from calculus.gradient_descent._1_numerical_differentiation.gradient_descent import GradientDescent
from calculus.gradient_descent._1_numerical_differentiation.optimizer import Optimizer
import random


class Dense(Layer):
    
    # case1) simple version 
    # def __init__(self, input_size: int, output_size: int, activation: Activation):
    #     # Initialize weights with shape (output_size, input_size)
    #     self.weights = Matrix([[random.uniform(-0.1, 0.1) 
    #                           for _ in range(input_size)] 
    #                           for _ in range(output_size)])
        
    #     # Initialize biases with shape (1, output_size)
    #     self.biases = Matrix([[random.uniform(-0.1, 0.1) 
    #                          for _ in range(output_size)]])
    #     self.activation = activation
        
    #     # Store for backprop
    #     self.inputs = None
    #     self.output_before_activation = None
    #     self.output = None
        
    #     # Store gradients
    #     self.weight_gradients = None
    #     self.bias_gradients = None

    #     # config for custom_gradient_descent function 
    #     self.optimizer = GradientDescent(learning_rate=0.01)

    # case2) custom gradient descent 
    def __init__(self, input_size: int, output_size: int, activation: Activation, learning_rate: float = 0.01):
        # Existing initialization
        self.weights = Matrix([[random.uniform(-0.1, 0.1) 
                              for _ in range(input_size)] 
                              for _ in range(output_size)])

        # step1
        # 예시 값:
        # First Dense Layer: input_size=2, output_size=4
        # weights = Matrix([
        #     [-0.08, 0.05],  # 첫 번째 출력 노드: input1에 -0.08, input2에 0.05 가중치
        #     [0.02, -0.09],  # 두 번째 출력 노드: input1에 0.02, input2에 -0.09 가중치
        #     [0.07, 0.03],   # 세 번째 출력 노드: input1에 0.07, input2에 0.03 가중치
        #     [-0.04, 0.06]   # 네 번째 출력 노드: input1에 -0.04, input2에 0.06 가중치
        # ])
        
        self.biases = Matrix([[random.uniform(-0.1, 0.1) 
                             for _ in range(output_size)]])

        # step2
        # biases는 (1 × output_size) Matrix가 됨:
        # biases = Matrix([[
        #     random.uniform(-0.1, 0.1),  # 첫 번째 출력 노드의 bias
        #     random.uniform(-0.1, 0.1),  # 두 번째 출력 노드의 bias
        #     random.uniform(-0.1, 0.1),  # 세 번째 출력 노드의 bias
        #     random.uniform(-0.1, 0.1)   # 네 번째 출력 노드의 bias
        # ]])

        # step3
        # 이렇게 만들어진 weights와 biases로:

        # 입력 데이터
        # inputs = Matrix([
        #     [0, 0],  # 첫 번째 샘플
        #     [0, 1],  # 두 번째 샘플
        #     [1, 0],  # 세 번째 샘플
        #     [1, 1]   # 네 번째 샘플
        # ])

        # 입력 [0,0]이 들어오면:

        # 첫 번째 노드: 0*(-0.08) + 0*(0.05) + 0.03 = 0.03
        # 두 번째 노드: 0*(0.02) + 0*(-0.09) - 0.05 = -0.05
        # 등으로 계산됨


        # 입력 [0,1]이 들어오면:

        # 첫 번째 노드: 0*(-0.08) + 1*(0.05) + 0.03 = 0.08
        # 두 번째 노드: 0*(0.02) + 1*(-0.09) - 0.05 = -0.14
        # 등으로 계산됨

        # 이런 식으로 각 input에 대해 4개의 출력값이 계산된다. (노드가 4개라)

        # ex) 각 샘플에 대해 계산된 결과
        # output = Matrix([
        #     # 샘플[0,0]의 4개 출력값
        #     [0*(-0.08) + 0*(0.05) + 0.03,    # = 0.03
        #     0*(0.02) + 0*(-0.09) - 0.05,    # = -0.05
        #     0*(0.07) + 0*(0.03) + 0.08,     # = 0.08
        #     0*(-0.04) + 0*(0.06) - 0.02],   # = -0.02

        #     # 샘플[0,1]의 4개 출력값
        #     [0*(-0.08) + 1*(0.05) + 0.03,    # = 0.08
        #     0*(0.02) + 1*(-0.09) - 0.05,    # = -0.14
        #     0*(0.07) + 1*(0.03) + 0.08,     # = 0.11
        #     0*(-0.04) + 1*(0.06) - 0.02],   # = 0.04

        #     # 이런식으로 [1,0], [1,1]도 계산
        #     [...],
        #     [...]
        # ])

        # step4
        # 이 값들이 ReLU 활성화 함수를 거쳐 다음 layer로 전달됩니다.
        # ReLU 활성화 함수 적용 후 (max(0,x)): 
        # final_output = Matrix([
        #     [0.03,  0.0,   0.08,  0.0],   # [0,0]에 대한 출력, 이래서 첫번째 레이어에서 input_size가 2인데, output_size가 4인가?
        #     [0.08,  0.0,   0.11,  0.04],  # [0,1]에 대한 출력
        #     [0.05,  0.02,  0.15,  0.0],   # [1,0]에 대한 출력
        #     [0.10,  0.0,   0.18,  0.06]   # [1,1]에 대한 출력
        # ])
        self.activation = activation
        
        # Add optimizer
        self.optimizer = GradientDescent(learning_rate=learning_rate, tolerance=1e-6)


        
    def forward(self, inputs: Matrix) -> Matrix:
        """
        Forward pass
        inputs: batch_size × input_size
        returns: batch_size × output_size
        """
        self.inputs = inputs
        
        # For debugging, print shapes
        # print(f"Input shape: {inputs.shape}")
        # print(f"Weights shape: {self.weights.shape}")
        # print(f"Biases shape: {self.biases.shape}")
        
        # Matrix multiplication: (batch_size × input_size) @ (input_size × output_size)
        matmul_result = inputs @ self.weights.transpose()
        # print(f"Matmul result shape: {matmul_result.shape}")
        
        # Broadcasting biases to match batch size
        batch_size = inputs.rows
        broadcasted_biases = Matrix([self.biases._data[0] for _ in range(batch_size)])
        
        # Add biases
        self.output_before_activation = matmul_result + broadcasted_biases
        
        # Apply activation function
        # ReLu던 Sigmoid건, 인풋값을 먹이면 각 layer마다 다른 그래프가 나오고,
        # 맨 끝에 레이어에서 이 여러 들쭉날쭉한 그래프들을 합쳐서 하나의 output graph를 만들면,
        # 여기에 x 입력하면 y 구하고 하는 식 
        self.output = self.activation.forward(self.output_before_activation)
        return self.output

    def backward(self, grad: Matrix) -> Matrix:
        """
        Backward pass
        grad: gradient from next layer
        returns: gradient for previous layer
        """
        # Gradient through activation function
        grad = grad * self.activation.backward(self.output_before_activation)
        
        # Compute gradients for weights and biases
        self.weight_gradients = grad.transpose() @ self.inputs 
        self.bias_gradients = grad.sum(axis=0)
        
        # Compute gradient for previous layer
        return grad @ self.weights
        
    # case1) 완전 기본 gradient descent 적용
    def update(self, learning_rate: float):
        """Update weights and biases using gradients"""
        # Just simple subtraction with learning rate
        self.weights = self.weights - self.weight_gradients * learning_rate
        self.biases = self.biases - self.bias_gradients * learning_rate
    
    # # case2) custom gradient descent 적용한 것 
    # def update(self, learning_rate: float):
    #     # 2D -> 1D로 변환 (Optimizer.py가 1d만 받음)
    #     flat_weights = [item for sublist in self.weights._data for item in sublist]
    #     flat_gradients = [item for sublist in self.weight_gradients._data for item in sublist]
        
    #     # 목적 함수 정의 (얼마나 틀렸는지 계산하는 함수)
    #     def weight_objective(w):
    #         return sum(g * w_i for g, w_i in zip(flat_gradients, w))
        
    #     # 최적화 알고리즘으로 최적값 찾기
    #     # - Tolerance checking
    #     # - Max iterations
    #     # - Convergence checking
    #     new_weights, _ = self.optimizer.minimize(
    #         f=weight_objective,
    #         initial_x=NDArray(flat_weights)
    #     )
        
    #     # 1D를 다시 2D로 변환
    #     rows = self.weights.rows
    #     cols = self.weights.cols
    #     reshaped_weights = [new_weights[i:i+cols] for i in range(0, len(new_weights), cols)]
    #     self.weights = Matrix(reshaped_weights)

    #     # weight 말고 이번엔 biases한테 한다 
    #     flat_biases = self.biases._data[0]
    #     flat_bias_gradients = self.bias_gradients._data[0]
        
    #     def bias_objective(b):
    #         return sum(g * b_i for g, b_i in zip(flat_bias_gradients, b))
        
    #     new_biases, _ = self.optimizer.minimize(
    #         f=bias_objective,
    #         initial_x=NDArray(flat_biases)
    #     )
        
    #     self.biases = Matrix([list(new_biases)])
