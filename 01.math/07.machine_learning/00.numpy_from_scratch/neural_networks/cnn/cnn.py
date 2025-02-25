from neural_networks.cnn.layers.dense import Dense
from neural_networks.cnn.activation_functions.ReLU import ReLU
from neural_networks.cnn.layers.conv2d import Conv2D
from neural_networks.cnn.layers.maxpool2d import MaxPool2D
from neural_networks.cnn.layers.flatten import Flatten
from neural_networks.cnn.loss.cross_entropy_loss import CrossEntropyLoss

class CNN:
    """
    ㅇㅋ CNN 모델임
    컨볼루션 -> 풀링 -> 플래튼 -> Dense 이런식으로 구성됨 ㅋㅋ
    """
    def __init__(self):
        self.layers = []
        self.loss_fn = CrossEntropyLoss()
        
    def add(self, layer):
        """
        레이어 추가하는거임 ㅋㅋ
        """
        self.layers.append(layer)
        
    def forward(self, x):
        """
        순전파 ㄱㄱ
        """
        for layer in self.layers:
            x = layer.forward(x)
        return x
        
    def backward(self, dout):
        """
        역전파 ㄱㄱ
        """
        for layer in reversed(self.layers):
            dout = layer.backward(dout)
            
    def train_step(self, x, y):
        """
        학습 1스텝 하는거임
        """
        # 순전파
        out = self.forward(x)
        
        # 로스 계산
        loss = self.loss_fn.forward(out, y)
        
        # 역전파
        dout = self.loss_fn.backward()
        self.backward(dout)
        
        return loss

# 사용 예시:
"""
# MNIST 데이터셋으로 CNN 학습하는 예시임 

model = CNN()

# 레이어 추가
model.add(Conv2D(filters=32, kernel_size=3, padding='same'))  # 첫번째 컨볼루션
model.add(ReLu())
model.add(MaxPool2D(pool_size=2))

model.add(Conv2D(filters=64, kernel_size=3, padding='same'))  # 두번째 컨볼루션
model.add(ReLu())
model.add(MaxPool2D(pool_size=2))

model.add(Flatten())  # CNN -> Dense 변환
model.add(Dense(128))  # 완전연결층
model.add(ReLu())
model.add(Dense(10))  # 출력층 (MNIST니까 10개 클래스)

# 학습 루프
for epoch in range(epochs):
    for x_batch, y_batch in data_loader:
        loss = model.train_step(x_batch, y_batch)
        print(f'에포크 {epoch} 로스: {loss}')
"""
