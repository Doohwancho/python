from neural_networks.multi_layer_perceptron.loss.loss import Loss
from linear_algebra.matrix import NDArray

class CrossEntropyLoss(Loss):
    """Cross Entropy Loss for classification"""
    @staticmethod
    def forward(y_pred: NDArray, y_true: NDArray) -> float:
        eps = 1e-15  # prevent log(0)
        return -sum(t * math.log(p + eps) for p, t in zip(y_pred, y_true))

    @staticmethod
    def backward(y_pred: NDArray, y_true: NDArray) -> NDArray:
        eps = 1e-15
        return NDArray([-t / (p + eps) for p, t in zip(y_pred, y_true)])
