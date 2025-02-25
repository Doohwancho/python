from linear_algebra.cnn_ndarray import CNNArray
import numpy as np

class Dense:
    """
    CNN용 Dense 레이어임 ㅋㅋ
    기존 Dense 레이어랑 구분하려고 이름 바꿈
    """
    def __init__(self, input_size: int, output_size: int):
        self.input_size = input_size
        self.output_size = output_size
        
        # Xavier/Glorot 초기화
        scale = np.sqrt(2.0 / (input_size + output_size))
        weights_data = [[scale * np.random.randn() for _ in range(input_size)] 
                       for _ in range(output_size)]
        bias_data = [0.0] * output_size
        
        self.weights = CNNArray(weights_data)  # (output_size, input_size)
        self.bias = CNNArray(bias_data)      # (output_size,)
        
        print(f"Dense 레이어 생성 - 입력: {input_size}, 출력: {output_size}")
        print(f"가중치 shape: {self.weights.shape}")
        print(f"편향 shape: {self.bias.shape}")

    def forward(self, x):
        """
        순전파임
        입력 x: (batch_size, input_size)
        출력: (batch_size, output_size)
        """
        if not isinstance(x, CNNArray):
            x = CNNArray(x)
            
        print(f"Dense forward 입력 shape: {x.shape}")  # 디버깅
        
        batch_size = x.shape[0]
        
        # 행렬곱 구현 (x @ W^T)
        out_data = [[sum(x._data[b][i] * self.weights._data[j][i] 
                        for i in range(self.input_size)) + self.bias._data[j]
                    for j in range(self.output_size)]
                   for b in range(batch_size)]
        
        # 입력 저장 (역전파용)
        self.x = x
        
        return CNNArray(out_data)
        
    def backward(self, dout):
        """
        역전파임
        입력 dout: (batch_size, output_size)
        출력: (batch_size, input_size)
        """
        if not isinstance(dout, CNNArray):
            dout = CNNArray(dout)
            
        batch_size = dout.shape[0]
        
        # 입력에 대한 그래디언트 (dout @ W)
        dx_data = [[sum(dout._data[b][j] * self.weights._data[j][i]
                       for j in range(self.output_size))
                   for i in range(self.input_size)]
                  for b in range(batch_size)]
                  
        # 가중치에 대한 그래디언트 (x^T @ dout)
        dw_data = [[sum(self.x._data[b][i] * dout._data[b][j]
                       for b in range(batch_size))
                   for i in range(self.input_size)]
                  for j in range(self.output_size)]
                  
        # 편향에 대한 그래디언트
        db_data = [sum(dout._data[b][j] for b in range(batch_size))
                  for j in range(self.output_size)]
                  
        # 그래디언트 저장
        self.dW = CNNArray(dw_data)
        self.db = CNNArray(db_data)
        
        return CNNArray(dx_data)
