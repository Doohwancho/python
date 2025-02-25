from linear_algebra.cnn_ndarray import CNNArray

class Flatten:
    """
    걍 다 펴는거임 ㅋㅋ CNN -> Dense 레이어로 넘어갈때 씀
    """
    def forward(self, x):
        """
        (배치, 채널, 높이, 너비) -> (배치, 채널*높이*너비)
        """
        if not isinstance(x, CNNArray):
            x = CNNArray(x)
            
        print(f"Flatten 입력 shape: {x.shape}")  # 디버깅
        
        # 입력 shape 저장 (역전파용)
        self.input_shape = x.shape
        
        # 배치 크기
        batch_size = x.shape[0]
        
        # flatten할 특징 수 계산 (채널 * 높이 * 너비)
        flattened_size = 1
        for s in x.shape[1:]:  # 배치 크기 제외하고 곱하기
            flattened_size *= s
            
        print(f"Flatten - batch_size: {batch_size}, flattened_size: {flattened_size}")  # 디버깅
            
        # 데이터 flatten
        flattened = [[0.0 for _ in range(flattened_size)] 
                    for _ in range(batch_size)]
        
        # 4D -> 2D로 변환
        for b in range(batch_size):
            idx = 0
            for c in range(x.shape[1]):  # 채널
                for h in range(x.shape[2]):  # 높이
                    for w in range(x.shape[3]):  # 너비
                        flattened[b][idx] = x._data[b][c][h][w]
                        idx += 1
        
        out = CNNArray(flattened, (batch_size, flattened_size))
        print(f"Flatten 출력 shape: {out.shape}")  # 디버깅
        return out
        
    def backward(self, dout):
        """
        역전파
        2D (배치, 채널*높이*너비) -> 4D (배치, 채널, 높이, 너비)
        """
        if not isinstance(dout, CNNArray):
            dout = CNNArray(dout)
            
        batch_size = self.input_shape[0]
        channels = self.input_shape[1]
        height = self.input_shape[2]
        width = self.input_shape[3]
        
        # 4D 데이터 초기화
        dx_data = [[[[0.0 for _ in range(width)]
                    for _ in range(height)]
                   for _ in range(channels)]
                  for _ in range(batch_size)]
                  
        # 2D -> 4D로 복원
        for b in range(batch_size):
            idx = 0
            for c in range(channels):
                for h in range(height):
                    for w in range(width):
                        dx_data[b][c][h][w] = dout._data[b][idx]
                        idx += 1
                        
        return CNNArray(dx_data, self.input_shape)
