import numpy as np
from keras.datasets import mnist

def to_one_hot(y, num_classes=10):
    one_hot = np.zeros((len(y), num_classes))
    one_hot[np.arange(len(y)), y] = 1
    return one_hot

# 데이터 전처리 코드 (숫자 그림을 받는다. )
def load_mnist(sample_size=5000):
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    
    print(f"Original data shape - X_train: {X_train.shape}, y_train: {y_train.shape}")

    indices = np.random.choice(len(X_train), sample_size, replace=False)
    X_train = X_train[indices]
    y_train = y_train[indices]
    
    test_size = sample_size // 5
    test_indices = np.random.choice(len(X_test), test_size, replace=False)
    X_test = X_test[test_indices]
    y_test = y_test[test_indices]
    
    print(f"Sampled data size - train: {sample_size}, test: {test_size}")
    
    # 데이터 정규화 개선: 평균 0, 표준편차 1로 정규화
    # 모델 입력 형태(N, C, H, W)로 변환해줌
    # 정규화 안하면 학습 개느려짐 
    X_train = X_train.reshape(-1, 1, 28, 28) / 255.0
    X_test = X_test.reshape(-1, 1, 28, 28) / 255.0
    
    # 원핫 인코딩
    y_train_one_hot = to_one_hot(y_train)
    y_test_one_hot = to_one_hot(y_test)
    
    return (X_train, y_train_one_hot), (X_test, y_test_one_hot), (y_train, y_test)

# feature map 생성 
# 이 함수가 바로 특성 추출의 핵심 
# 이미지를 작은 조각으로 쪼개서 필터와 연산하기 쉽게 만드는 것 
def im2col(input_data, filter_h, filter_w, stride=1, pad=0):
    # 입력 MNIST 이미지
    N, C, H, W = input_data.shape # (128, 1, 28, 28)
    # N = 배치 크기 (한번에 처리하는 이미지 개수, 보통 128개)
    # C = 채널 수 (흑백이라 1, 컬러면 3)
    # H = 높이 (MNIST는 28픽셀)
    # W = 너비 (MNIST는 28픽셀)

    out_h = (H + 2*pad - filter_h)//stride + 1
    out_w = (W + 2*pad - filter_w)//stride + 1

    img = np.pad(input_data, [(0,0), (0,0), (pad, pad), (pad, pad)], mode='constant')

    # 이거 ㄹㅇ 핵심 부분인데, 이미지를 패치 형태로 재구성하는 것. 
    # 1. 처음에 (128, 1, 30, 30) 매트릭스를 as_strided로 (128, 1, 28, 28, 3, 3) 형태로 변환 (3x3 패치들)
    # 2. transpose로 축 순서 바꿔서 (128, 28, 28, 1, 3, 3)으로 변환
    # 3. reshape으로 (1282828, 133) = (100352, 9) 형태의 2D 매트릭스로 펼침

    # 각 행은 3x3 필터가 보는 이미지 패치 하나를 나타냄. 100352개의 패치가 있고, 각 패치는 9개 픽셀로 구성됨ㅇㅇ

    # Q. stride_tricks.as_strided란?
    # 원본 이미지를 복사하지 않고 메모리 뷰만 조작해서 이미지 패치들을 2D 매트릭스로 변환함. 
    # 필터가 이미지 위를 슥삭 슥삭 움직이면서 생기는 모든 패치를 한방에 구함
    col = np.lib.stride_tricks.as_strided(
        img,
        shape=(N, C, out_h, out_w, filter_h, filter_w),
        strides=(img.strides[0], img.strides[1], img.strides[2]*stride, img.strides[3]*stride, img.strides[2], img.strides[3])
    )
    col = col.transpose(0, 2, 3, 1, 4, 5).reshape(N*out_h*out_w, -1)
    return col

def col2im(col, x_shape, filter_h, filter_w, stride=1, pad=0):
    N, C, H, W = x_shape
    out_h = (H + 2*pad - filter_h) // stride + 1
    out_w = (W + 2*pad - filter_w) // stride + 1
    col = col.reshape(N, out_h, out_w, C, filter_h, filter_w)
    
    img = np.zeros((N, C, H + 2*pad, W + 2*pad))
    for y in range(filter_h):
        y_max = y + stride * out_h
        for x in range(filter_w):
            x_max = x + stride * out_w
            col_slice = col[:, :, :, :, y, x].transpose(0, 3, 1, 2)
            img[:, :, y:y_max:stride, x:x_max:stride] += col_slice
    
    if pad > 0:
        img = img[:, :, pad:-pad, pad:-pad]
    return img

class Conv2D:
    def __init__(self, filters, kernel_size, stride=1, padding='same'):
        self.filters = filters
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.W = None
        self.b = None
        self.x = None
        self.dW = None
        self.db = None

    def _init_params(self, input_channels):
        # He 초기화 방식으로 변경 (ReLU 활성화 함수에 더 적합)
        scale = np.sqrt(2.0 / (input_channels * self.kernel_size**2))
        self.W = np.random.randn(self.filters, input_channels, self.kernel_size, self.kernel_size) * scale
        self.b = np.zeros(self.filters)

    # 여기서 실제 특성 추출이 일어남ㅇㅇ
    # 1. 필터를 2D로 평탄화(W_flat)한 이후,
    # 2. 행렬곱으로 합성곱 연산을 한방에 계산 (W_flat @ col.T)
    #    진짜 핵심은 W_flat @ col.T + self.b[:, np.newaxis] 이 한 줄임. 이게 특성 추출 코드 
    # 3. 바이어스 더함
    # 4. 결과를 다시 원하는 형태(N, C, H, W)로 변환
    def forward(self, x):
        N, C, H, W = x.shape # 입력 이미지 개수, 채널 수, 높이, 너비
        filter_h, filter_w = self.kernel_size, self.kernel_size # 필터 크기 (3x3 같은거)

        pad = self.kernel_size // 2 if self.padding == 'same' else 0 # padding='same'이면 입출력 크기 동일하게
        # padding='same'이면 매트릭스 주변에 0을 채움. 3x3 필터면 pad=1이니까:
        # 입력: (128, 1, 28, 28)
        # 패딩 후: (128, 1, 30, 30) 
        # 이렇게 하는 이유는 이미지 가장자리 정보를 안 잃으려고 하는거임ㅇㅇ 안하면 모서리 부분이 연산 과정에서 씹힘

        out_h = (H + 2*pad - filter_h)//self.stride + 1 # 출력 높이 계산
        out_w = (W + 2*pad - filter_w)//self.stride + 1 # 출력 너비 계산

        # 초기화가 안 된 경우 초기화
        if self.W is None:
            self._init_params(C) # 가중치 초기화 안됐으면 초기화

        self.x = x # 역전파할 때 쓰려고 입력 저장

        # 여기서 im2col 함수가 입력 이미지를 필터가 보는 패치(조각)들로 쫙 펼쳐버림. 
        # 예를 들면:
        # 1. 원래 이미지가 (1, 1, 28, 28)이고 3x3 필터면
        # 2. im2col은 3x3 패치를 쭉 늘어놓은 행렬로 만듦
        # 3. 결과 형태는 (26*26, 9) = (676, 9)가 됨 (28x28에서 3x3 윈도우 이동하면 26x26개 패치 생김)
        # 이게 바로 합성곱 연산을 행렬곱으로 개꿀로 바꾸는 핵심임ㅋㅋ 이러면 GPU에서 쌉가능함
        col = im2col(x, filter_h, filter_w, self.stride, pad) 

        # 필터도 평평하게 만들자
        # 원래 필터는 (필터 개수, 채널, 높이, 너비) = (32, 1, 3, 3) 같은 형태인데, 이걸 (32, 9)로 납작하게 쪼개버림ㅋㅋ
        W_flat = self.W.reshape(self.filters, -1) # (32, 1, 3, 3) -> (32, 9)
                                                  # 원래 필터: (32, 1, 3, 3) = 32개의 3x3 필터
                                                  # 변환 후: (32, 9) = 각 필터를 9개 원소의 벡터로 변환

        # 설명1)
        # W_flat @ col.T: 여기서 행렬곱이 일어남. W_flat은 (32, 9), col.T는 (9, 676)이니까 결과는 (32, 676)이 됨.
        # 이 말은 32개의 필터를 사용해서 676개의 위치에서 특성을 추출했다는 의미임
        # 각 필터는 선, 점, 코너 같은 간단한 특성을 찾아내는 역할을 함. 세로선, 가로선, 45도 기울어진 선 등 다양한 패턴을 인식 가능
        # + self.b[:, np.newaxis]는 각 필터마다 바이어스(치우침) 더해줌. 이건 필터가 특정 값에 과민반응 안하게 조절하는 역할임.
        # (32,) 형태의 바이어스를 (32, 1) 형태로 확장해서 브로드캐스팅(자동 확장)을 통해 (32, 676)에 더함

        # 설명2)
        # 1. W_flat(32, 9)와 col.T(9, 100352)의 행렬곱 = (32, 100352)
        # 2. 각 필터(32개)가 모든 패치(100352개)와 내적(dot product)
        # 3. 바이어스 더하기: (32,) -> (32, 1) -> (32, 100352)로 브로드캐스팅
        # 이거 뜻은 32개의 각 필터가 이미지의 모든 위치에서 특정 패턴(가로선, 세로선, 대각선 등)을 얼마나 찾았는지를 수치화한 것임ㅋㅋ
        conv_output = W_flat @ col.T + self.b[:, np.newaxis] # 특성 추출 코드. # (32, 9) @ (9, 100352) -> (32, 100352)

        # 마지막으로 이거는 뽑은 특성을 예쁘게 정리하는 부분임:
        # 설명1)
        # 1. conv_output.T: (32, 676)을 (676, 32)로 뒤집음
        # 2. reshape(N, out_h, out_w, self.filters): (676, 32)를 (1, 26, 26, 32)로 변형 (배치, 높이, 너비, 필터)
        # 3. transpose(0, 3, 1, 2): (1, 26, 26, 32)를 (1, 32, 26, 26)으로 축 순서 바꿈 (배치, 필터, 높이, 너비)
        # 이렇게 하는 이유는 PyTorch/TensorFlow 관례상 채널(필터)이 두 번째 차원에 오는게 일반적이라서임

        # 설명2)
        # 1. transpose: (32, 100352) -> (100352, 32)
        # 2. reshape: (100352, 32) -> (128, 28, 28, 32)
        # 3. 다시 transpose: (128, 28, 28, 32) -> (128, 32, 28, 28)
        # 최종 출력은 (128, 32, 28, 28) 형태의 텐서가 됨ㅋㅋㅋ 
        # 즉, 128개 이미지 각각에 대해 32개의 28x28 특성 맵을 얻음ㅇㅇ 
        # 각 특성 맵은 특정 패턴(엣지, 선 등)의 위치 정보를 나타냄
        return conv_output.T.reshape(N, out_h, out_w, self.filters).transpose(0, 3, 1, 2) # (32, 100352).T -> (100352, 32) -> (128, 28, 28, 32) -> (128, 32, 28, 28)

    def backward(self, dout):
        N, F, out_h, out_w = dout.shape
        C, H, W = self.x.shape[1], self.x.shape[2], self.x.shape[3]
        filter_h, filter_w = self.kernel_size, self.kernel_size
        pad = self.kernel_size // 2 if self.padding == 'same' else 0

        # dL/dB 계산
        self.db = np.sum(dout, axis=(0, 2, 3))

        # dL/dW 계산
        col = im2col(self.x, filter_h, filter_w, self.stride, pad)
        dout_flat = dout.transpose(0, 2, 3, 1).reshape(-1, F)
        self.dW = np.dot(dout_flat.T, col).reshape(self.W.shape)

        # dL/dX 계산
        W_flat = self.W.reshape(F, -1)
        dcol = np.dot(dout_flat, W_flat)
        dx = col2im(dcol, self.x.shape, filter_h, filter_w, self.stride, pad)
        return dx

class BatchNorm:
    def __init__(self, size, momentum=0.9, eps=1e-5):
        self.gamma = np.ones(size)
        self.beta = np.zeros(size)
        self.momentum = momentum
        self.eps = eps
        self.running_mean = np.zeros(size)
        self.running_var = np.ones(size)
        
        self.x = None
        self.x_norm = None
        self.x_centered = None
        self.std = None
        self.dgamma = None
        self.dbeta = None
        self.train_mode = True

    def forward(self, x):
        # 합성곱 레이어 출력인 경우 (N, C, H, W) 형태를 (N, H, W, C) 형태로 변환
        if x.ndim == 4:
            N, C, H, W = x.shape
            x_reshaped = x.transpose(0, 2, 3, 1).reshape(-1, C)
            out_reshaped = self._forward(x_reshaped)
            out = out_reshaped.reshape(N, H, W, C).transpose(0, 3, 1, 2)
            return out
        else:
            return self._forward(x)

    def _forward(self, x):
        self.x = x
        
        if self.train_mode:
            batch_mean = np.mean(x, axis=0)
            batch_var = np.var(x, axis=0)
            
            # 이동 평균 및 분산 업데이트
            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * batch_mean
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * batch_var
            
            self.x_centered = x - batch_mean
            self.std = np.sqrt(batch_var + self.eps)
            self.x_norm = self.x_centered / self.std
        else:
            self.x_norm = (x - self.running_mean) / np.sqrt(self.running_var + self.eps)
            
        out = self.gamma * self.x_norm + self.beta
        return out

    def backward(self, dout):
        # 합성곱 레이어 출력인 경우
        if dout.ndim == 4:
            N, C, H, W = dout.shape
            dout_reshaped = dout.transpose(0, 2, 3, 1).reshape(-1, C)
            dx_reshaped = self._backward(dout_reshaped)
            dx = dx_reshaped.reshape(N, H, W, C).transpose(0, 3, 1, 2)
            return dx
        else:
            return self._backward(dout)

    def _backward(self, dout):
        batch_size = self.x.shape[0]
        
        # gamma와 beta에 대한 그래디언트
        self.dgamma = np.sum(dout * self.x_norm, axis=0)
        self.dbeta = np.sum(dout, axis=0)
        
        # 정규화된 x에 대한 그래디언트
        dx_norm = dout * self.gamma
        
        # 분산에 대한 그래디언트
        dvar = np.sum(dx_norm * self.x_centered * -0.5 * self.std**(-3), axis=0)
        
        # 평균에 대한 그래디언트
        dmean = np.sum(dx_norm * -1 / self.std, axis=0) + dvar * np.sum(-2 * self.x_centered, axis=0) / batch_size
        
        # 입력에 대한 그래디언트
        dx = dx_norm / self.std + dvar * 2 * self.x_centered / batch_size + dmean / batch_size
        
        return dx

class MaxPool2D:
    def __init__(self, pool_size=2, stride=None):
        self.pool_size = pool_size
        self.stride = stride if stride is not None else pool_size
        self.x = None
        self.max_indices = None

    # 풀링은 다운샘플링하는거임:
    # 1. 2x2 윈도우로 이미지를 쪼갬 (128, 32, 14, 14, 2, 2)
    # 2. 각 윈도우에서 최대값만 선택해서 (128, 32, 14, 14) 형태로 줄임
    # 3. 즉 공간 크기는 절반으로 줄고 (28x28 -> 14x14) 채널 수는 그대로 (32)
    # 이렇게 하면 중요한 특성은 살리고 계산량은 확 줄임ㅋㅋ
    def forward(self, x):
        N, C, H, W = x.shape
        out_h = (H - self.pool_size) // self.stride + 1
        out_w = (W - self.pool_size) // self.stride + 1

        self.x = x
        # Reshape using stride_tricks
        col = np.lib.stride_tricks.as_strided(
            x,
            shape=(N, C, out_h, out_w, self.pool_size, self.pool_size),
            strides=(x.strides[0], x.strides[1], 
                     x.strides[2] * self.stride, x.strides[3] * self.stride,
                     x.strides[2], x.strides[3])
        )
        x_reshaped = col.reshape(N, C, out_h, out_w, self.pool_size * self.pool_size)
        self.max_indices = np.argmax(x_reshaped, axis=4)
        out = x_reshaped.max(axis=4)
        return out

    def backward(self, dout):
        N, C, out_h, out_w = dout.shape
        dx = np.zeros_like(self.x)
        for n in range(N):
            for c in range(C):
                for i in range(out_h):
                    for j in range(out_w):
                        h_start = i * self.stride
                        w_start = j * self.stride
                        idx = self.max_indices[n, c, i, j]
                        h_idx = h_start + (idx // self.pool_size)
                        w_idx = w_start + (idx % self.pool_size)
                        dx[n, c, h_idx, w_idx] = dout[n, c, i, j]
        return dx

class Flatten:
    def __init__(self):
        self.input_shape = None

    # 이제 2D 이미지 구조를 1D 벡터로 펼침ㅇㅇ

    # 입력: (128, 32, 14, 14)
    # 출력: (128, 6272)

    # 각 이미지가 6272개의 특징을 가진 벡터로 변환됨ㅋㅋ
    def forward(self, x):
        # 입력: (128, 32, 14, 14)
        self.input_shape = x.shape

        return x.reshape(x.shape[0], -1) # (128, 32*14*14) = (128, 6272)

    def backward(self, dout):
        return dout.reshape(self.input_shape)

class Dense:
    def __init__(self, input_size, output_size):
        # He 초기화
        scale = np.sqrt(2.0 / input_size)
        self.W = np.random.randn(output_size, input_size) * scale
        self.b = np.zeros(output_size)
        self.x = None
        self.dW = None
        self.db = None

    # 1. 가중치 행렬 W는 (128, 6272) 형태
    # 2. 입력 x(128, 6272)와 W.T(6272, 128)의 행렬곱 = (128, 128)
    # 3. 바이어스 b(128,) 더해서 최종 출력 (128, 128)

    # 이 과정에서 각 뉴런은 이전 레이어의 모든 뉴런과 연결됨ㅇㅇ
    # Q. 만약 마지막 레이어라면?
    # 입력: (128, 128)
    # (128, 128) @ (10, 128).T -> (128, 10) = 각 이미지에 대해 10개 숫자의 점수
    def forward(self, x):
        self.x = x # 입력: (128, 6272)
        return np.dot(x, self.W.T) + self.b # (128, 6272) @ (128, 6272) -> (128, 128)

    def backward(self, dout):
        # 수정된 그래디언트 계산
        self.dW = np.dot(dout.T, self.x)
        self.db = np.sum(dout, axis=0)
        dx = np.dot(dout, self.W)
        return dx

class ReLU:
    def __init__(self):
        self.x = None

    def forward(self, x):
        self.x = x
        return np.maximum(x, 0)

    def backward(self, dout):
        return np.where(self.x > 0, 1, 0) * dout

class Dropout:
    def __init__(self, dropout_ratio=0.5):
        self.dropout_ratio = dropout_ratio
        self.mask = None
        self.train_mode = True

    def forward(self, x):
        if self.train_mode:
            self.mask = np.random.rand(*x.shape) > self.dropout_ratio
            return x * self.mask / (1.0 - self.dropout_ratio)
        else:
            return x

    def backward(self, dout):
        if self.train_mode:
            return dout * self.mask / (1.0 - self.dropout_ratio)
        else:
            return dout

class CrossEntropyLoss:
    def __init__(self):
        self.y_pred = None
        self.y_true = None
        self.y_pred_prob = None

    # 소프트맥스로 점수를 확률로 변환:

    # 1. 수치 안정성을 위해 최대값 빼기
    # 2. 지수 함수 적용
    # 3. 합이 1이 되도록 정규화
    # 4. 결과는 (128, 10) 형태의 확률 분포 (각 숫자일 확률)

    # 결론: MNIST CNN 전체 과정은 (128, 1, 28, 28) -> (128, 10)으로 매트릭스가 변환되는 과정임
    def forward(self, y_pred, y_true):
        self.y_pred = y_pred
        self.y_true = y_true

        # 수치 안정성을 위해 최대값 빼기
        exp_y_pred = np.exp(y_pred - np.max(y_pred, axis=1, keepdims=True))
        y_pred_prob = exp_y_pred / np.sum(exp_y_pred, axis=1, keepdims=True) # (128, 10)
        self.y_pred_prob = y_pred_prob

        # 수치 안정성 개선을 위한 epsilon 값 추가
        loss = -np.sum(self.y_true * np.log(y_pred_prob + 1e-15)) / y_pred_prob.shape[0]
        return loss

    def backward(self):
        # 그래디언트 계산 (소프트맥스 출력 - 원핫 인코딩된 레이블)
        batch_size = self.y_true.shape[0]
        return (self.y_pred_prob - self.y_true) / batch_size

class SGDMomentum:
    def __init__(self, learning_rate=0.01, momentum=0.9):
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.v = {}

    def update(self, params, grads, param_name):
        if param_name not in self.v:
            self.v[param_name] = np.zeros_like(params)
            
        self.v[param_name] = self.momentum * self.v[param_name] - self.learning_rate * grads
        return params + self.v[param_name]

class CNN:
    def __init__(self, learning_rate=0.001, momentum=0.9):
        self.layers = []
        self.loss_fn = CrossEntropyLoss()
        self.optimizer = SGDMomentum(learning_rate, momentum)
        self.train_mode = True

    def add(self, layer):
        self.layers.append(layer)

    def forward(self, x):
        for layer in self.layers:
            # 배치 정규화와 드롭아웃 레이어의 모드 설정
            if hasattr(layer, 'train_mode'):
                layer.train_mode = self.train_mode
            x = layer.forward(x)
        return x

    def backward(self, dout):
        for layer in reversed(self.layers):
            dout = layer.backward(dout)

    def train(self):
        self.train_mode = True

    def eval(self):
        self.train_mode = False

    def train_step(self, x, y):
        # 학습 모드 설정
        self.train()
        
        # 순전파
        out = self.forward(x)
        loss = self.loss_fn.forward(out, y)
        
        # 역전파
        dout = self.loss_fn.backward()
        self.backward(dout)

        # 가중치 업데이트
        for i, layer in enumerate(self.layers):
            if hasattr(layer, 'W'):
                layer.W = self.optimizer.update(layer.W, layer.dW, f"W_{i}")
                layer.b = self.optimizer.update(layer.b, layer.db, f"b_{i}")
            
            # 배치 정규화 매개변수 업데이트
            if hasattr(layer, 'gamma'):
                layer.gamma = self.optimizer.update(layer.gamma, layer.dgamma, f"gamma_{i}")
                layer.beta = self.optimizer.update(layer.beta, layer.dbeta, f"beta_{i}")

        return loss

def train_model(model, train_data, test_data, epochs=20, batch_size=128):
    X_train, y_train = train_data
    X_test, y_test = test_data
    
    n_samples = X_train.shape[0]
    n_batches = max(n_samples // batch_size, 1)
    
    print(f"Training data size - X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"Batch calculation - n_samples: {n_samples}, batch_size: {batch_size}, n_batches: {n_batches}")
    
    # 학습 곡선을 기록하기 위한 리스트
    train_losses = []
    test_accuracies = []
    
    for epoch in range(epochs):
        # 데이터 섞기
        indices = np.random.permutation(n_samples)
        X_train_shuffled = X_train[indices]
        y_train_shuffled = y_train[indices]
        
        total_loss = 0
        for i in range(n_batches):
            start_idx = i * batch_size
            end_idx = min(start_idx + batch_size, n_samples)
            X_batch = X_train_shuffled[start_idx:end_idx]
            y_batch = y_train_shuffled[start_idx:end_idx]
            
            loss = model.train_step(X_batch, y_batch)
            total_loss += loss
            
            if i % 10 == 0:
                print(f"Epoch {epoch+1}, Batch {i+1}/{n_batches}, Loss: {loss:.4f}")
        
        avg_loss = total_loss / n_batches
        train_losses.append(avg_loss)
        print(f"Epoch {epoch+1} completed! Average Loss: {avg_loss:.4f}")
        
        # 매 에폭마다 테스트 세트에서 평가
        accuracy = evaluate_model(model, test_data, batch_size)
        test_accuracies.append(accuracy)
        
        # 조기 종료 (선택 사항)
        if accuracy > 0.98:
            print(f"Early stopping at epoch {epoch+1} with accuracy {accuracy*100:.2f}%")
            break

    return train_losses, test_accuracies

def evaluate_model(model, test_data, batch_size=32):
    # 평가 모드 설정
    model.eval()
    
    X_test, y_test = test_data
    n_samples = X_test.shape[0]
    n_batches = n_samples // batch_size + (1 if n_samples % batch_size != 0 else 0)
    
    correct = 0
    total = 0
    
    for i in range(n_batches):
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, n_samples)
        X_batch = X_test[start_idx:end_idx]
        y_batch = y_test[start_idx:end_idx]
        
        predictions = model.forward(X_batch)
        pred_classes = np.argmax(predictions, axis=1)
        true_classes = np.argmax(y_batch, axis=1)
        correct += np.sum(pred_classes == true_classes)
        total += end_idx - start_idx
    
    accuracy = correct / total
    print(f"Test Accuracy: {accuracy*100:.2f}%")
    return accuracy

# 학습 완료 후 특정 이미지에 대한 예측 테스트
def predict_single_image(model, image, true_label=None):
    # 이미지 형태 확인 및 변환
    if image.ndim == 2:  # (28, 28) 형태인 경우
        image = image.reshape(1, 1, 28, 28)
    elif image.ndim == 3 and image.shape[0] == 1:  # (1, 28, 28) 형태인 경우
        image = image.reshape(1, 1, 28, 28)
    
    # 순전파 실행
    output = model.forward(image)
    
    # 결과 처리
    predicted_class = np.argmax(output)
    exp_output = np.exp(output - np.max(output))
    probabilities = exp_output / np.sum(exp_output)
    
    # 결과 출력
    print(f"\n예측 결과:")
    if true_label is not None:
        if isinstance(true_label, np.ndarray) and true_label.ndim > 0:
            true_label = np.argmax(true_label)
        print(f"실제 숫자: {true_label}")
    print(f"예측 숫자: {predicted_class}")
    print(f"예측 확률: {probabilities[0][predicted_class]:.4f}")
    
    return predicted_class, probabilities[0]

def visualize_filters(model, layer_idx=0):
    # 첫 번째 컨볼루션 레이어의 필터 시각화
    layer = model.layers[layer_idx]
    if not hasattr(layer, 'W') or len(layer.W.shape) != 4:
        print("선택한 레이어가 컨볼루션 레이어가 아닙니다.")
        return
    
    filters = layer.W
    n_filters, n_channels, height, width = filters.shape
    
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 10))
    
    # 필터의 일부만 시각화
    n_display = min(n_filters, 16)
    for i in range(n_display):
        filter_img = filters[i, 0]  # 첫 번째 채널만 시각화
        plt.subplot(4, 4, i+1)
        plt.imshow(filter_img, cmap='viridis')
        plt.axis('off')
        plt.title(f'Filter {i+1}')
    
    plt.tight_layout()
    plt.savefig("conv_filters.png")
    print("필터가 conv_filters.png 파일로 저장되었습니다.")

def visualize_activations(model, image):
    # 각 레이어의 활성화 맵 시각화
    model.eval()
    
    if image.ndim == 2:
        image = image.reshape(1, 1, 28, 28)
    
    activations = []
    x = image
    
    # 각 레이어의 활성화 수집
    for layer in model.layers:
        x = layer.forward(x)
        if isinstance(layer, Conv2D) or isinstance(layer, MaxPool2D):
            activations.append(x.copy())
    
    # 활성화 맵 시각화
    import matplotlib.pyplot as plt
    plt.figure(figsize=(15, 10))
    
    for i, activation in enumerate(activations):
        n_features = activation.shape[1]
        n_display = min(n_features, 16)
        
        for j in range(n_display):
            plt.subplot(len(activations), n_display, i*n_display + j + 1)
            plt.imshow(activation[0, j], cmap='viridis')
            plt.axis('off')
            if j == 0:
                layer_type = "Conv" if i % 2 == 0 else "Pool"
                plt.title(f'{layer_type} {i//2+1}')
    
    plt.tight_layout()
    plt.savefig("activations.png")
    print("활성화 맵이 activations.png 파일로 저장되었습니다.")

if __name__ == "__main__":
    print("Loading MNIST data...")
    train_data, test_data, (y_train_raw, y_test_raw) = load_mnist(sample_size=10000)  # 샘플 크기 증가
    
    print("Creating CNN model...")
    model = CNN(learning_rate=0.001, momentum=0.9)  # 학습률 감소 및 모멘텀 추가
    
    """
    convolutional layer란?

    1. 첫 레이어에서는 선, 엣지, 간단한 모양 같은 저수준 특성 추출
    2. 깊은 레이어로 갈수록 텍스처, 패턴, 물체 부분 같은 고수준 특성 추출
    3. 마지막엔 이 특성들 조합해서 "이건 7이다" 같은 판단을 내림
    """

    # 1st convolutional layer
    # 32개의 필터로 기본적인 특성(엣지, 선, 간단한 패턴)을 추출
    model.add(Conv2D(filters=32, kernel_size=3, padding='same'))
    model.add(BatchNorm(32)) # 배치 정규화로 학습 안정화
    model.add(ReLU()) # ReLU로 비선형성 추가 (이거 없으면 그냥 선형 변환이라 개망함). 
                      # ReLU는 단순히 음수값을 0으로 만듦ㅇㅇ 매트릭스 크기는 변하지 않고 (128, 32, 28, 28) 그대로지만, 음수값은 다 0이 됨. 
                      # 이렇게 비선형성 추가함ㅋㅋ
    model.add(MaxPool2D(pool_size=2)) # MaxPool로 공간 크기는 줄이고 중요 특성은 보존
    
    # 2nd convolutional layer
    # 64개, 128개로 필터 수 증가 (더 복잡한 특성 추출)
    # 각 층을 지날 때마다 점점 더 추상적인 특성을 학습함
    model.add(Conv2D(filters=64, kernel_size=3, padding='same'))
    model.add(BatchNorm(64))
    model.add(ReLU())
    model.add(MaxPool2D(pool_size=2))
    
    # 3rd convolutional layer
    # 첫 층: 엣지, 선 → 중간 층: 간단한 모양 → 마지막 층: 복잡한 패턴
    model.add(Conv2D(filters=128, kernel_size=3, padding='same'))
    model.add(BatchNorm(128))
    model.add(ReLU())
    model.add(MaxPool2D(pool_size=2))
    
    model.add(Flatten())
    model.add(Dense(input_size=128*3*3, output_size=256))
    model.add(BatchNorm(256))
    model.add(ReLU())
    model.add(Dropout(0.3))  # 드롭아웃 추가로 과적합 방지
    
    model.add(Dense(input_size=256, output_size=10))
    
    print("Starting training!")
    train_losses, test_accuracies = train_model(model, train_data, test_data, epochs=3, batch_size=128) # 원래 epoch 15였는데 너무 오래걸려서 3으로 낮춤 
    
    # 학습 곡선 시각화
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(train_losses)
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    
    plt.subplot(1, 2, 2)
    plt.plot(test_accuracies)
    plt.title('Test Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    
    plt.tight_layout()
    plt.savefig('learning_curves.png')
    print("학습 곡선이 learning_curves.png 파일로 저장되었습니다.")
    
    # 테스트 데이터에서 몇 개의 이미지 선택하여 테스트
    num_test_images = 5
    for i in range(num_test_images):
        try:
            # 테스트 세트에서 무작위로 이미지 선택
            idx = np.random.randint(0, len(test_data[0]))
            test_image = test_data[0][idx]
            true_label = np.argmax(test_data[1][idx])
            
            # 예측 수행
            predicted, probs = predict_single_image(model, test_image, true_label)
            
            # 이미지 저장
            plt.figure(figsize=(5, 5))
            plt.imshow(test_image.reshape(28, 28), cmap='gray')
            plt.title(f"실제: {true_label}, 예측: {predicted}")
            plt.axis('off')
            plt.savefig(f"test_image_{i+1}.png")
            print(f"테스트 이미지 {i+1}이 test_image_{i+1}.png 파일로 저장되었습니다.")
        except Exception as e:
            print(f"테스트 이미지 {i+1} 처리 중 오류 발생: {e}")
