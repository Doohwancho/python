from linear_algebra.cnn_ndarray import CNNArray


class ReLU:
    """
    CNN용 ReLU 활성화 함수임 ㅋㅋ
    """
    def forward(self, x):
        """
        순전파 - max(0,x) 계산
        """
        if not isinstance(x, CNNArray):
            x = CNNArray(x)
        
        print(f"ReLU 입력 shape: {x.shape}")  # 디버깅
        
        # 입력 데이터 가져오기
        input_data = x._data
        
        # 원본 shape 저장
        self.input_shape = x.shape
        
        # 결과 데이터 초기화
        if len(x.shape) == 4:  # Conv 레이어 다음의 경우
            batch_size, channels, height, width = x.shape
            out_data = [[[[max(0, input_data[b][c][h][w]) 
                         for w in range(width)]
                        for h in range(height)]
                       for c in range(channels)]
                      for b in range(batch_size)]
        else:  # Dense 레이어 다음의 경우
            batch_size, features = x.shape
            out_data = [[max(0, input_data[b][f]) 
                        for f in range(features)]
                       for b in range(batch_size)]
        
        # 입력 저장 (역전파용)
        self.x = x
        
        return CNNArray(out_data)
        
    def backward(self, dout):
        """
        역전파 - x > 0이면 그대로, 아니면 0
        """
        if not isinstance(dout, CNNArray):
            dout = CNNArray(dout)
            
        # 입력 데이터
        x_data = self.x._data
        # 역전파 데이터
        dout_data = dout._data
        
        # 결과 데이터 초기화
        if len(self.input_shape) == 4:  # Conv 레이어의 경우
            batch_size, channels, height, width = self.input_shape
            dx_data = [[[[dout_data[b][c][h][w] if x_data[b][c][h][w] > 0 else 0
                         for w in range(width)]
                        for h in range(height)]
                       for c in range(channels)]
                      for b in range(batch_size)]
        else:  # Dense 레이어의 경우
            batch_size, features = self.input_shape
            dx_data = [[dout_data[b][f] if x_data[b][f] > 0 else 0
                       for f in range(features)]
                      for b in range(batch_size)]
            
        return CNNArray(dx_data)
