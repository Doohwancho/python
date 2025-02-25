import sys
import os
import numpy as np

# 프로젝트 루트 경로를 파이썬 path에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(project_root)


from neural_networks.cnn.utils.cnn_ndarray import CNNArray
from neural_networks.cnn.cnn import CNN
from neural_networks.cnn.layers.conv2d import Conv2D
from neural_networks.cnn.layers.maxpool2d import MaxPool2D
from neural_networks.cnn.layers.flatten import Flatten
from neural_networks.cnn.layers.dense import Dense
from neural_networks.cnn.activation_functions.ReLu import ReLU
import numpy as np


def load_mnist():
    """
    MNIST 데이터 로드하는 함수임 ㅋㅋ
    """
    from keras.datasets import mnist
    
    # 데이터 로드
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    
    print(f"원본 데이터 shape - X_train: {X_train.shape}, y_train: {y_train.shape}")
    
    # 전처리 - numpy array를 list로 변환
    def np_to_list(arr):
        return arr.tolist()
    
    # (60000, 28, 28) -> (60000, 1, 28, 28)로 변환하고 정규화
    X_train_reshaped = (X_train.reshape(-1, 1, 28, 28) / 255.0)
    X_test_reshaped = (X_test.reshape(-1, 1, 28, 28) / 255.0)
    
    # numpy array를 list로 변환
    X_train_list = np_to_list(X_train_reshaped)
    X_test_list = np_to_list(X_test_reshaped)
    
    # One-hot 인코딩
    def to_one_hot(y, num_classes=10):
        one_hot = np.zeros((len(y), num_classes))
        one_hot[np.arange(len(y)), y] = 1
        return one_hot.tolist()
        
    y_train_onehot = to_one_hot(y_train)
    y_test_onehot = to_one_hot(y_test)
    
    # CNNArray로 변환하면서 shape 지정
    X_train_shape = (len(X_train), 1, 28, 28)
    y_train_shape = (len(y_train), 10)
    X_test_shape = (len(X_test), 1, 28, 28)
    y_test_shape = (len(y_test), 10)
    
    X_train_cnn = CNNArray(X_train_list, X_train_shape)
    y_train_cnn = CNNArray(y_train_onehot, y_train_shape)
    X_test_cnn = CNNArray(X_test_list, X_test_shape)
    y_test_cnn = CNNArray(y_test_onehot, y_test_shape)
    
    print(f"CNNArray 변환 후:")
    print(f"X_train shape: {X_train_cnn.shape}")
    print(f"y_train shape: {y_train_cnn.shape}")
    
    return (X_train_cnn, y_train_cnn), (X_test_cnn, y_test_cnn)

def create_mnist_cnn():
    """
    MNIST용 CNN 모델 만드는 함수임
    """
    model = CNN()
    relu = ReLU()  # activation 인스턴스 생성
    
    # 첫번째 컨볼루션 블록
    model.add(Conv2D(filters=32, kernel_size=3, padding='same'))  # (B, 32, 28, 28)
    model.add(ReLU())
    model.add(MaxPool2D(pool_size=2))  # (B, 32, 14, 14)
    
    # 두번째 컨볼루션 블록
    model.add(Conv2D(filters=64, kernel_size=3, padding='same'))  # (B, 64, 14, 14)
    model.add(ReLU())
    model.add(MaxPool2D(pool_size=2))  # (B, 64, 7, 7)
    
    # Dense 레이어로 변환
    model.add(Flatten())  # (B, 64*7*7)
    
    # Fully Connected 레이어
    model.add(Dense(input_size=64*7*7, output_size=128, activation=relu))  # (B, 128)
    model.add(Dense(input_size=128, output_size=10, activation=None))   # (B, 10)
    
    return model

def train_model(model, train_data, test_data, epochs=5, batch_size=32):
    """
    모델 학습하는 함수임 ㅋㅋ
    """
    X_train, y_train = train_data
    X_test, y_test = test_data
    
    print(f"학습 데이터 크기 - X_train: {X_train.size()}, y_train: {y_train.size()}")  # len -> size
    
    n_samples = X_train.shape[0]  # len -> shape[0]
    n_batches = max(n_samples // batch_size, 1)  # 최소 1개 배치 보장
    
    print(f"배치 계산 - n_samples: {n_samples}, batch_size: {batch_size}, n_batches: {n_batches}")
    
    for epoch in range(epochs):
        total_loss = 0
        
        # 배치 단위로 학습
        for i in range(n_batches):
            start_idx = i * batch_size
            end_idx = min(start_idx + batch_size, n_samples)
            
            # 배치 데이터
            # CNNArray의 슬라이싱은 이미 shape 정보를 유지하므로 따로 shape을 지정할 필요 없음
            X_batch = X_train[start_idx:end_idx]
            y_batch = y_train[start_idx:end_idx]
            
            # 학습
            loss = model.train_step(X_batch, y_batch)
            total_loss += loss
            
            # 진행상황 출력
            if i % 10 == 0:
                print(f"에포크 {epoch+1}, 배치 {i+1}/{n_batches}, 로스: {loss:.4f}")
        
        avg_loss = total_loss / n_batches
        print(f"에포크 {epoch+1} 완료! 평균 로스: {avg_loss:.4f}")
        
        # 테스트 세트로 평가
        if epoch % 1 == 0:
            evaluate_model(model, test_data, batch_size)

def evaluate_model(model, test_data, batch_size=32):
    """
    모델 평가하는 함수임
    """
    X_test, y_test = test_data
    n_samples = X_test.shape[0]  # len -> shape[0]
    n_batches = n_samples // batch_size
    
    correct = 0
    total = 0
    
    for i in range(n_batches):
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, n_samples)
        
        X_batch = X_test[start_idx:end_idx]
        y_batch = y_test[start_idx:end_idx]
        
        # 예측
        predictions = model.forward(X_batch)
        
        # 정확도 계산
        pred_classes = np.argmax(predictions._data, axis=1)  # CNNArray._data로 접근
        true_classes = np.argmax(y_batch._data, axis=1)
        correct += np.sum(pred_classes == true_classes)
        total += end_idx - start_idx
    
    accuracy = correct / total
    print(f"테스트 정확도: {accuracy*100:.2f}%")
    return accuracy

if __name__ == "__main__":
    print("MNIST 데이터 로딩중...")
    train_data, test_data = load_mnist()
    
    print("CNN 모델 생성중...")
    model = create_mnist_cnn()
    
    print("학습 시작!")
    train_model(model, train_data, test_data, epochs=5, batch_size=32)
