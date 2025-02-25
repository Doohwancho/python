from linear_algebra.cnn_ndarray import CNNArray
import numpy as np

class MaxPool2D:
    """
    맥스풀링이다 ㅋㅋ 걍 최대값 뽑는거임
    """
    def __init__(self, pool_size=2, stride=None):
        self.pool_size = pool_size
        self.stride = stride if stride is not None else pool_size
        
    def forward(self, x):
        """
        앞으로 가즈아ㅏㅏ
        x 모양: (배치, 채널, 높이, 너비)
        """
        if not isinstance(x, CNNArray):
            x = CNNArray(x)
            
        N, C, H, W = x.shape
        H_out = (H - self.pool_size) // self.stride + 1
        W_out = (W - self.pool_size) // self.stride + 1
        
        out = [[[[0.0 for _ in range(W_out)] 
                 for _ in range(H_out)]
                for _ in range(C)]
               for _ in range(N)]
               
        self.max_indices = [[[[0 for _ in range(W_out)]
                             for _ in range(H_out)]
                            for _ in range(C)]
                           for _ in range(N)]
        
        # 각 풀링 윈도우에서 최대값과 그 위치 찾기
        for n in range(N):
            for c in range(C):
                for i in range(H_out):
                    for j in range(W_out):
                        h_start = i * self.stride
                        w_start = j * self.stride
                        
                        # 현재 윈도우에서 최대값 찾기
                        max_val = float('-inf')
                        max_idx = 0
                        for h_offset in range(self.pool_size):
                            for w_offset in range(self.pool_size):
                                h_idx = h_start + h_offset
                                w_idx = w_start + w_offset
                                val = x[n][c][h_idx][w_idx]
                                
                                if val > max_val:
                                    max_val = val
                                    max_idx = h_offset * self.pool_size + w_offset
                                    
                        out[n][c][i][j] = max_val
                        self.max_indices[n][c][i][j] = max_idx
        
        out_shape = (N, C, H_out, W_out)
        return CNNArray(out, out_shape)
        
    def backward(self, dout):
        """
        역전파임
        """
        if not isinstance(dout, CNNArray):
            dout = CNNArray(dout)
            
        N, C, H_out, W_out = dout.shape
        H = (H_out - 1) * self.stride + self.pool_size
        W = (W_out - 1) * self.stride + self.pool_size
        
        dx = [[[[0.0 for _ in range(W)]
                for _ in range(H)]
               for _ in range(C)]
              for _ in range(N)]
        
        for n in range(N):
            for c in range(C):
                for i in range(H_out):
                    for j in range(W_out):
                        h_start = i * self.stride
                        w_start = j * self.stride
                        max_idx = self.max_indices[n][c][i][j]
                        
                        h_idx = h_start + (max_idx // self.pool_size)
                        w_idx = w_start + (max_idx % self.pool_size)
                        dx[n][c][h_idx][w_idx] = dout[n][c][i][j]
                        
        return CNNArray(dx, (N, C, H, W))
