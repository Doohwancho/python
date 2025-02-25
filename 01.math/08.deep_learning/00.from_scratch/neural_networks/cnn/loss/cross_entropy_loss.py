from linear_algebra.cnn_ndarray import CNNArray
import numpy as np


class CrossEntropyLoss:
    """
    CNN용 Cross Entropy Loss임 ㅋㅋ
    """
    def forward(self, y_pred, y_true):
        """
        순전파
        y_pred: 예측값 (배치, 클래스)
        y_true: 실제값 (배치, 클래스)
        """
        if not isinstance(y_pred, CNNArray):
            y_pred = CNNArray(y_pred)
        if not isinstance(y_true, CNNArray):
            y_true = CNNArray(y_true)
            
        self.y_pred = y_pred
        self.y_true = y_true
        
        eps = 1e-15  # numerical stability용
        
        # 배치별로 loss 계산
        batch_size = y_pred.shape[0]
        loss = 0.0
        for b in range(batch_size):
            for i in range(y_pred.shape[1]):
                p = y_pred._data[b][i]
                t = y_true._data[b][i]
                loss -= t * np.log(p + eps)
                
        return loss / batch_size
        
    def backward(self):
        """
        역전파
        """
        eps = 1e-15
        batch_size = self.y_pred.shape[0]
        
        # 각 클래스에 대한 그래디언트 계산
        dx_data = [[-(self.y_true._data[b][i] / (self.y_pred._data[b][i] + eps))
                    for i in range(self.y_pred.shape[1])]
                   for b in range(batch_size)]
                   
        return CNNArray(dx_data)
