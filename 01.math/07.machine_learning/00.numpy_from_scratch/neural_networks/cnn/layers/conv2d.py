from linear_algebra.cnn_ndarray import CNNArray
import numpy as np


class Conv2D:
    def __init__(self, filters, kernel_size, stride=1, padding='same'):
        self.filters = filters
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.W = None
        self.b = None

    def _init_params(self, input_channels):
        """
        가중치랑 편향 초기화하는거임 ㅋㅋ
        """
        print(f"가중치 초기화 - 입력 채널: {input_channels}, 필터: {self.filters}")   

        # 가중치 초기화 (filters, channels, kernel_size, kernel_size)
        w_shape = (self.filters, input_channels, self.kernel_size, self.kernel_size)
        total_elements = self.filters * input_channels * self.kernel_size * self.kernel_size
        
        # Xavier/Glorot 초기화
        scale = np.sqrt(2.0 / (input_channels * self.kernel_size ** 2))
        w_data = [[[[scale * np.random.randn() for _ in range(self.kernel_size)]
                   for _ in range(self.kernel_size)]
                  for _ in range(input_channels)]
                 for _ in range(self.filters)]
        
        b_data = [0.0] * self.filters
        
        self.W = CNNArray(w_data)
        self.b = CNNArray(b_data)
        
        print(f"가중치 shape: {self.W.shape}")  
        print(f"편향 shape: {self.b.shape}")  

    def _pad_data(self, x_data, pad):
        """
        패딩 추가하는 함수임 ㅋㅋ
        x_data: 4차원 리스트 (batch, channel, height, width)
        """
        if pad == 0:
            return x_data
            
        # 리스트의 크기로 shape 계산
        batch_size = len(x_data)
        channels = len(x_data[0])
        height = len(x_data[0][0])
        width = len(x_data[0][0][0])
        
        print(f"패딩 전 크기: ({batch_size}, {channels}, {height}, {width})")  
        
        new_height = height + 2 * pad
        new_width = width + 2 * pad
        
        # 패딩된 데이터 초기화 (0으로)
        padded_data = [[[[0.0 for _ in range(new_width)] 
                        for _ in range(new_height)]
                       for _ in range(channels)]
                      for _ in range(batch_size)]
        
        # 원본 데이터 복사
        for b in range(batch_size):
            for c in range(channels):
                for h in range(height):
                    for w in range(width):
                        padded_data[b][c][h+pad][w+pad] = x_data[b][c][h][w]
                        
        print(f"패딩 후 크기: ({batch_size}, {channels}, {new_height}, {new_width})") 
        return padded_data

    def forward(self, x):
        """
        앞으로 전파하는거임 ㅋㅋ
        x 모양: (배치, 채널, 높이, 너비)
        """
        if not isinstance(x, CNNArray):
            x = CNNArray(x)
            
        print(f"Conv2D forward 입력 shape: {x.shape}")   

        batch_size, channels, height, width = x.shape
        
        # 처음이면 가중치 초기화
        if self.W is None:
            self._init_params(channels)
            
        # 패딩 계산
        if self.padding == 'same':
            pad = (self.kernel_size - 1) // 2
            x_padded = self._pad_data(x._data, pad)
            x_padded = CNNArray(x_padded)
        else:
            x_padded = x
            pad = 0
            
        padded_height = height + 2 * pad
        padded_width = width + 2 * pad
        
        # 출력 크기 계산
        out_height = (padded_height - self.kernel_size) // self.stride + 1
        out_width = (padded_width - self.kernel_size) // self.stride + 1
        
        print(f"Conv2D 출력 크기: ({batch_size}, {self.filters}, {out_height}, {out_width})")  
        
        # 출력 데이터 초기화
        out_data = [[[[0.0 for _ in range(out_width)]
                     for _ in range(out_height)]
                    for _ in range(self.filters)]
                   for _ in range(batch_size)]
        
        # 컨볼루션 연산
        for b in range(batch_size):
            for f in range(self.filters):
                for i in range(out_height):
                    for j in range(out_width):
                        window_sum = 0
                        for c in range(channels):
                            for ki in range(self.kernel_size):
                                for kj in range(self.kernel_size):
                                    in_i = i * self.stride + ki
                                    in_j = j * self.stride + kj
                                    in_val = x_padded._data[b][c][in_i][in_j]
                                    w_val = self.W._data[f][c][ki][kj]
                                    window_sum += in_val * w_val
                        out_data[b][f][i][j] = window_sum + self.b._data[f]
        
        self.x_padded = x_padded  # 역전파용으로 저장
        output_shape = (batch_size, self.filters, out_height, out_width)
        return CNNArray(out_data, output_shape)

    def backward(self, dout):
        """
        역전파임 ㅋㅋ
        """
        if not isinstance(dout, CNNArray):
            dout = CNNArray(dout)
            
        batch_size, _, out_height, out_width = dout.shape
        _, channels, padded_height, padded_width = self.x_padded.shape
        
        # 입력에 대한 그래디언트 초기화
        dx_padded_data = [[[[0.0 for _ in range(padded_width)]
                           for _ in range(padded_height)]
                          for _ in range(channels)]
                         for _ in range(batch_size)]
                         
        # 가중치에 대한 그래디언트 초기화
        dw_data = [[[[0.0 for _ in range(self.kernel_size)]
                     for _ in range(self.kernel_size)]
                    for _ in range(channels)]
                   for _ in range(self.filters)]
                   
        # 편향에 대한 그래디언트 초기화
        db_data = [0.0] * self.filters
        
        # 그래디언트 계산
        for b in range(batch_size):
            for f in range(self.filters):
                for i in range(out_height):
                    for j in range(out_width):
                        dout_val = dout._data[b][f][i][j]
                        db_data[f] += dout_val
                        
                        for c in range(channels):
                            for ki in range(self.kernel_size):
                                for kj in range(self.kernel_size):
                                    in_i = i * self.stride + ki
                                    in_j = j * self.stride + kj
                                    x_val = self.x_padded._data[b][c][in_i][in_j]
                                    
                                    # 가중치 그래디언트
                                    dw_data[f][c][ki][kj] += x_val * dout_val
                                    
                                    # 입력 그래디언트
                                    w_val = self.W._data[f][c][ki][kj]
                                    dx_padded_data[b][c][in_i][in_j] += w_val * dout_val
        
        # 패딩 제거
        if self.padding == 'same':
            pad = (self.kernel_size - 1) // 2
            dx_height = padded_height - 2 * pad
            dx_width = padded_width - 2 * pad
            
            dx_data = [[[[dx_padded_data[b][c][h+pad][w+pad] 
                         for w in range(dx_width)]
                        for h in range(dx_height)]
                       for c in range(channels)]
                      for b in range(batch_size)]
        else:
            dx_data = dx_padded_data
            
        # 그래디언트 저장
        self.dW = CNNArray(dw_data)
        self.db = CNNArray(db_data)
        
        return CNNArray(dx_data)
