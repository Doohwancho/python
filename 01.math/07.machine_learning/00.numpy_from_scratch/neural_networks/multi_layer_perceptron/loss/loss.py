from linear_algebra.ndarray import NDArray

class Loss:
    """Base class for loss functions"""
    @staticmethod
    def forward(y_pred: NDArray, y_true: NDArray) -> float:
        raise NotImplementedError

    @staticmethod
    def backward(y_pred: NDArray, y_true: NDArray) -> NDArray:
        raise NotImplementedError
