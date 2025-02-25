import sys
import os
import numpy as np

# 프로젝트 루트 경로를 파이썬 path에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(project_root)


import numpy as np
from linear_algebra.cnn_ndarray import CNNArray
from neural_networks.cnn.cnn import CNN
from neural_networks.cnn.layers.conv2d import Conv2D
from neural_networks.cnn.layers.maxpool2d import MaxPool2D
from neural_networks.cnn.layers.flatten import Flatten
from neural_networks.cnn.layers.dense import Dense
from neural_networks.cnn.activation_functions.ReLU import ReLU


def load_mnist(sample_size=5000):
    """
    MNIST 데이터 로드하는 함수임 ㅋㅋ
    """
    from keras.datasets import mnist
    
    # 데이터 로드
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    
    print(f"원본 데이터 shape - X_train: {X_train.shape}, y_train: {y_train.shape}")

    # 데이터 샘플링
    indices = np.random.choice(len(X_train), sample_size, replace=False)
    X_train = X_train[indices]
    y_train = y_train[indices]
    
    test_size = sample_size // 5  # 테스트셋은 train의 1/5
    test_indices = np.random.choice(len(X_test), test_size, replace=False)
    X_test = X_test[test_indices]
    y_test = y_test[test_indices]
    
    print(f"샘플링된 데이터 크기 - 학습: {sample_size}, 테스트: {test_size}")
    
    
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
        return one_hot.tolist()  # list로 변환
        
    y_train_onehot = to_one_hot(y_train)
    y_test_onehot = to_one_hot(y_test)
    
    # NDArray로 변환하면서 shape 지정
    X_train_shape = (len(X_train), 1, 28, 28)
    y_train_shape = (len(y_train), 10)
    X_test_shape = (len(X_test), 1, 28, 28)
    y_test_shape = (len(y_test), 10)
    
    X_train_nd = CNNArray(X_train_list, X_train_shape)
    y_train_nd = CNNArray(y_train_onehot, y_train_shape)
    X_test_nd = CNNArray(X_test_list, X_test_shape)
    y_test_nd = CNNArray(y_test_onehot, y_test_shape)
    
    print(f"CNNArray 변환 후:")
    print(f"X_train shape: {X_train_nd.shape}")
    print(f"y_train shape: {y_train_nd.shape}")
    
    return (X_train_nd, y_train_nd), (X_test_nd, y_test_nd)


def create_mnist_cnn():
    """
    MNIST용 CNN 모델 만드는 함수임

    [28x28 이미지]
        ↓ (Conv2D 32개)
    [32개 특징맵]
        ↓ (MaxPool)
    [크기 1/2로]
        ↓ (Conv2D 64개)
    [64개 특징맵]
        ↓ (MaxPool)
    [크기 1/2로]
        ↓ (Flatten)
    [일렬로 펴기]
        ↓ (Dense)
    [10개 클래스]
    """
    model = CNN()
    
    print("CNN 모델 구조:") 
    
    # 첫번째 컨볼루션 블록
    model.add(Conv2D(filters=32, kernel_size=3, padding='same'))  # 3x3 필터 32개로 특징 추출 / padding='same'이라 크기 유지됨 
                                                                  # 입력: (32, 1, 28, 28)
                                                                  # 출력: (32, 32, 28, 28)  # ㄹㅇ 채널수만 1->32로 늘어남 ㅋㅋ
    print("Conv2D(32, 3x3) 추가됨")
    
    model.add(ReLU())  
    print("ReLU 추가됨")
    
    model.add(MaxPool2D(pool_size=2)) # 2x2 영역에서 최대값만 뽑음
                                      # 크기가 반으로 줄어듦 (특징은 살리고 크기는 줄이는거임 ㅇㅇ)
                                      # 입력: (32, 32, 28, 28)
                                      # 출력: (32, 32, 14, 14)
    print("MaxPool2D(2x2) 추가됨")
    
    # 두번째 컨볼루션 블록 (첫번째꺼 반복)
    # Conv2D(64): (32, 32, 14, 14) -> (32, 64, 14, 14)
    # MaxPool2D: (32, 64, 14, 14) -> (32, 64, 7, 7)
    # 필터 수를 64개로 늘려서 더 많은 특징 잡아냄 ㄹㅇ 
    model.add(Conv2D(filters=64, kernel_size=3, padding='same'))  # (B, 64, 14, 14)
    print("Conv2D(64, 3x3) 추가됨")
    
    model.add(ReLU())  # 기존 ReLU 대신 ReLUCNN 사용
    print("ReLU 추가됨")
    
    model.add(MaxPool2D(pool_size=2))  # (B, 64, 7, 7), pool_size = 2라는건 2x2로 압축한다는 것
    print("MaxPool2D(2x2) 추가됨")
    
    # Dense 레이어로 변환
    # 4차원 -> 2차원으로 펴줌 
    # 입력: (32, 64, 7, 7)
    # 출력: (32, 6477) = (32, 3136)
    # 이제 이걸로 일반 Dense 레이어 돌림 ㅋㅋ
    model.add(Flatten())  # (B, 64*7*7)
    print("Flatten 추가됨")
    
    # Fully Connected 레이어
    # 첫번째 Dense: (32, 3136) -> (32, 128)
    model.add(Dense(input_size=64*7*7, output_size=128))  # (B, 128)
    print("Dense(128) 추가됨")
    
    model.add(ReLU())  # Dense 후에도 ReLUCNN 사용
    print("ReLU 추가됨")
    
    # 마지막에 10개 클래스로 분류함 ㅇㅇ
    model.add(Dense(input_size=128, output_size=10))   # (B, 10)
    print("Dense(10) 추가됨")
    
    print("모델 생성 완료!")
    return model


def train_model(model, train_data, test_data, epochs=5, batch_size=128):
    """
    모델 학습하는 함수임 ㅋㅋ
    """
    X_train, y_train = train_data
    X_test, y_test = test_data
    
    # len() -> size() 로 수정
    print(f"학습 데이터 크기 - X_train: {X_train.size()}, y_train: {y_train.size()}")
    
    n_samples = X_train.shape[0]  # shape[0]로 배치 크기 계산
    n_batches = max(n_samples // batch_size, 1)  # 최소 1개 배치 보장
    
    print(f"배치 계산 - n_samples: {n_samples}, batch_size: {batch_size}, n_batches: {n_batches}")
    
    for epoch in range(epochs):
        total_loss = 0
        
        # 배치 단위로 학습
        for i in range(n_batches):
            start_idx = i * batch_size
            end_idx = min(start_idx + batch_size, n_samples)
            
            # 배치 데이터 가져오기
            X_batch = X_train[start_idx:end_idx]
            y_batch = y_train[start_idx:end_idx]
            
            print(f"배치 {i+1} shape - X: {X_batch.shape}, y: {y_batch.shape}")  # 디버깅 출력 추가
            
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
    n_samples = X_test.shape[0]  # shape[0]로 샘플 수 계산
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
        pred_classes = np.argmax(predictions._data, axis=1)
        true_classes = np.argmax(y_batch._data, axis=1)
        correct += np.sum(pred_classes == true_classes)
        total += end_idx - start_idx
    
    accuracy = correct / total
    print(f"테스트 정확도: {accuracy*100:.2f}%")
    return accuracy

if __name__ == "__main__":
    print("MNIST 데이터 로딩중...")
    train_data, test_data = load_mnist(sample_size=5000) # 5000개만 사용 
    
    print("CNN 모델 생성중...")
    model = create_mnist_cnn()
    
    print("학습 시작!")
    train_model(model, train_data, test_data, epochs=5, batch_size=128) # batch_size was previously 32 , epoch는 5회로 제한. 
