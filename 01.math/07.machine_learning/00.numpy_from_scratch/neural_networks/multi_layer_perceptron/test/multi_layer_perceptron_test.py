import sys
import os

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(project_root)


from neural_networks.multi_layer_perceptron.multi_layer_perceptron import NeuralNetwork
from neural_networks.multi_layer_perceptron.layer.dense import Dense
from neural_networks.multi_layer_perceptron.layer.batch_normalization import BatchNormalization
from neural_networks.multi_layer_perceptron.layer.dropout import Dropout  
from neural_networks.multi_layer_perceptron.activation_function.ReLu import ReLU
from neural_networks.multi_layer_perceptron.activation_function.sigmoid import Sigmoid  
from neural_networks.multi_layer_perceptron.loss.MSE_loss import MSELoss
from linear_algebra.matrix import Matrix

"""
Q. what is XOR problem?

# 입력과 기대 출력
[0,0] -> 0  # 둘 다 0이면 0
[0,1] -> 1  # 하나만 1이면 1
[1,0] -> 1  # 하나만 1이면 1
[1,1] -> 0  # 둘 다 1이면 0

neural network에서 왜 굳이 XOR 문제를 학습시킴?
선형적으로 분리 불가능한 가장 간단한 문제 (하나의 직선으로 구분 불가)
"""

"""
Q. 테스트 결과


case1) 기본 gradient descent를 쓴 경우 (dense.py 참조)
Summary:
Learning rate: 0.01, Minimum epochs needed: 7839
Learning rate: 0.05, Minimum epochs needed: 10000
Learning rate: 0.10, Minimum epochs needed: 1027
Learning rate: 0.50, Minimum epochs needed: 147
Learning rate: 1.00, Minimum epochs needed: 10000


case2) custom gradient descent를 쓴 경우 (dense.py 참조)
Summary:
Learning rate: 0.01, Minimum epochs needed: 10000
Learning rate: 0.05, Minimum epochs needed: 3585
Learning rate: 0.10, Minimum epochs needed: 10000
Learning rate: 0.50, Minimum epochs needed: 10000
Learning rate: 1.00, Minimum epochs needed: 10000
"""


def test_xor():
    """Test XOR problem with a simple neural network"""
    # Q. 얼만큼 train할거야? 얼만큼 learn_rate로 할거야?
    # case1) 기본 gradient descent 인 경우, 
    # 성공 케이스 epoch 7000, learn_rate 0.05 
    # 성공 케이스 epoch 5000, learn_rate 0.1
    # 성공 케이스 epoch 2600, learn_rate 1.0 

    # case2) custom gradient descent를 사용한 경우 
    # epoch = 5000
    # learning_rate = 1.0

    # Create network
    def create_network(learning_rate):
        network = NeuralNetwork(
            layers=[
                # 입력층 -> 첫 번째 은닉층
                # input(2) -> hidden(4) (문제가 복잡할 수록 여러 레이어와 노드가 필요하겠지? ex. XOR문제는 선형적으로 분리 불가능한 문제)
                # 입력은 4x2 matrix (x_train)
                # 출력은 4x4 matrix 
                # Q. 왜 input size가 2임?
                # A. x_train에 column이 2니까, 2개씩 입력되기 때문 
                Dense(input_size=2, output_size=4, activation=ReLU(), learning_rate=learning_rate),  
                BatchNormalization(input_size=4), # 학습 안정화. Q. 어떻게 학습 안정화 함? A. Batch normalization 파일에 적어둠                 

                # 두 번째 은닉층
                # hidden(4) -> hidden(3) 
                Dense(input_size=4, output_size=3, activation=ReLU(), learning_rate=learning_rate),           
                Dropout(dropout_rate=0.2), # 과적합 방지. Q. 어떻게 과적합 방지함?  A. dropout 파일에 적어둠  

                # 출력층
                # hidden(3) -> output(1) (3->1은 최종 결정하는 단계)
                Dense(input_size=3, output_size=1, activation=Sigmoid(), learning_rate=learning_rate)         
                # Q. 1,2 layer에서는 ReLU() 쓰고 마지막 출력층은 Sigmoid() 쓰는 이유는? 
                # A. ReLU()는 0 or 양수로 단순화 한거임 -> 계산이 빠르고 gradient vanishing 문제가 적음 
                #    sigmoid()는 출력을 0~1 사이로 제한 (이진 분류에 적합). 마지막 결과값을 0~1 사이에 확률로 해석 가능 
            ],
            # Q. layer의 층을 지금은 3개인데 100개로 늘리면 성능이 더 좋아지려나?
            # A. ㄴㄴ. xor문제 같이 간단한 문제는 레이어 3개면 떡을 치는데, 쉬운 문제에 100layer 쓰면 오히려 성능 안좋음.
            # Q. 왜 간단한 문제에 복잡한 레이어 쓰면 안좋음?
            # A. back() 함수에서 gradient descent값을 구해서 넘길 때, 0.25 씩 10번 계속 layer 넘어가면서 곱하다 보면 = 0.25¹⁰ ≈ 0.0000095 gradient가 너무 작아져서 사실상 학습이 안됨
            #    그렇다고 미분값이 1보다 큰 경우, 1.5 * 1.5 * 1.5 * ... # 10번 곱하기 
            #      = 1.5¹⁰ ≈ 57.665
            #    gradient가 너무 커져서 학습이 불안정해짐
            loss=MSELoss()
        )
        return network

    """
    # 입력 데이터
    x = Matrix([
        [0, 0],     # (4×2) 행렬
        [0, 1],
        [1, 0],
        [1, 1]
    ])

    # 첫 번째 Dense Layer 통과 후
    output1 = Matrix([
        [0.03, 0.0, 0.08, 0.0],    # (4×4) 행렬로 변환
        [0.08, 0.0, 0.11, 0.04],
        [0.05, 0.02, 0.15, 0.0],
        [0.10, 0.0, 0.18, 0.06]
    ])

    # 두 번째 Dense Layer 통과 후
    output2 = Matrix([
        [0.12, 0.05, 0.09],        # (4×3) 행렬로 변환
        [0.15, 0.08, 0.11],
        [0.18, 0.07, 0.13],
        [0.20, 0.09, 0.15]
    ])

    # 마지막 Dense Layer 통과 후
    final_output = Matrix([
        [0.02],                     # (4×1) 행렬로 변환
        [0.98],
        [0.95],
        [0.03]
    ])
    """

    # XOR data
    x_train = Matrix([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    y_train = Matrix([
        [0],
        [1],
        [1],
        [0]
    ])

    # Test different learning rates
    learning_rates = [0.01, 0.05, 0.1, 0.5, 1.0]
    results = []

    for lr in learning_rates:
        network = create_network(lr)
        losses = network.train(
            x_train=x_train,
            y_train=y_train,
            target_loss=0.1,
            epochs=10000,  # Max epochs as safety
            batch_size=4,
            learning_rate=lr
        )
        results.append((lr, len(losses)))
        print(f"Learning rate: {lr}, Required epochs: {len(losses)}")

    # Print summary
    print("\nSummary:")
    for lr, epochs in results:
        print(f"Learning rate: {lr:.2f}, Minimum epochs needed: {epochs}")


    # Train
    # 성공 케이스 epoch 7000, learn_rate 0.05 
    # losses = network.train(
    #     x_train=x_train,  # input이 이럴 때, (goal)
    #     y_train=y_train,  # output이 이렇게 나와야 한다. (goal)
    #     epochs=7000,      # if you want to optimize, change epochs(iterations)
    #     batch_size=4,     # Use all data in each batch
    #     learning_rate=0.05 # if you want to optimize, change learning rate
    # ) 

    # 성공 케이스. (epoch 5000, learn_rate 0.1)
    # losses = network.train(
    #     x_train=x_train,  # input이 이럴 때, (goal)
    #     y_train=y_train,  # output이 이렇게 나와야 한다. (goal)
    #     epochs=epoch,      # if you want to optimize, change epochs(iterations)
    #     batch_size=4,     # Use all data in each batch
    #     learning_rate=learning_rate # if you want to optimize, change learning rate
    # ) 

    # 성공 케이스. (epoch 2600, learn_rate 1.0)
    # losses = network.train(
    #     x_train=x_train,  # input이 이럴 때, (goal)
    #     y_train=y_train,  # output이 이렇게 나와야 한다. (goal)
    #     epochs=2600,      # if you want to optimize, change epochs(iterations)
    #     batch_size=4,     # Use all data in each batch
    #     learning_rate=1 # if you want to optimize, change learning rate
    # ) 

    # 초기 실패 케이스
    # losses = network.train(
    #     x_train=x_train,  # input이 이럴 때, (goal)
    #     y_train=y_train,  # output이 이렇게 나와야 한다. (goal)
    #     epochs=1000,      # if you want to optimize, change epochs(iterations)
    #     batch_size=4,     # Use all data in each batch
    #     learning_rate=0.01 # if you want to optimize, change learning rate
    # ) 

    
    # # Test predictions
    # predictions = network.predict(x_train)
    # print("Predictions:", predictions)
    # print("Final loss:", losses[-1])

    # # Add some assertions for automated testing
    # assert len(predictions) == 4, "Should have 4 predictions"
    # assert losses[-1] < 0.1, "Final loss should be less than 0.1"

    # # Test predictions are close to expected values
    # expected = [[0], [1], [1], [0]]
    # for pred, exp in zip(predictions, expected):
    #     assert abs(pred[0] - exp[0]) < 0.2, f"Prediction {pred[0]} should be closer to {exp[0]}"


if __name__ == "__main__":
    test_xor()
