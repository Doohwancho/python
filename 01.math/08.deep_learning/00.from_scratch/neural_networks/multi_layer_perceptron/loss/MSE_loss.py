from neural_networks.multi_layer_perceptron.loss.loss import Loss
from linear_algebra.matrix import Matrix

class MSELoss(Loss):
    @staticmethod
    def forward(y_pred: Matrix, y_true: Matrix) -> float:
        """
        Calculate Mean Squared Error
        y_pred and y_true are matrices of shape (batch_size, output_size)
        """
        error_sum = 0.0
        for i in range(y_pred.rows):
            for j in range(y_pred.cols):
                error = y_pred[i][j] - y_true[i][j]
                error_sum += error * error
        return error_sum / (y_pred.rows * y_pred.cols)

    @staticmethod
    def backward(y_pred: Matrix, y_true: Matrix) -> Matrix:
        """
        Calculate gradient of MSE loss
        Returns matrix of same shape as input
        """
        # Derivative of MSE is 2(y_pred - y_true)/n
        n = y_pred.rows * y_pred.cols
        return Matrix([[2 * (y_pred[i][j] - y_true[i][j]) / n
                       for j in range(y_pred.cols)]
                      for i in range(y_pred.rows)])
