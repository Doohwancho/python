from typing import List
from linear_algebra.matrix import Matrix
from neural_networks.multi_layer_perceptron.layer.layer import Layer
from neural_networks.multi_layer_perceptron.layer.dense import Dense
from neural_networks.multi_layer_perceptron.layer.batch_normalization import BatchNormalization
from neural_networks.multi_layer_perceptron.layer.dropout import Dropout
from neural_networks.multi_layer_perceptron.activation_function.ReLu import ReLU
from neural_networks.multi_layer_perceptron.activation_function.sigmoid import Sigmoid
from neural_networks.multi_layer_perceptron.loss.MSE_loss import MSELoss
from neural_networks.multi_layer_perceptron.loss.loss import Loss


class NeuralNetwork:
    """
    Neural Network implementation that combines layers
    """
    def __init__(self, layers: List[Layer], loss: Loss):
        self.layers = layers
        self.loss = loss

    def forward(self, x: Matrix) -> Matrix:
        """Forward pass through all layers"""
        output = x
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def backward(self, grad: Matrix) -> None:
        """Backward pass through all layers"""
        for layer in reversed(self.layers):
            grad = layer.backward(grad)

    def train_step(self, x: Matrix, y: Matrix, learning_rate: float) -> float:
        """Single training step"""
        # Forward pass
        predictions = self.forward(x)
        
        # Compute loss
        loss = self.loss.forward(predictions, y) # goal y로 부터 prediction이 얼마나 차이나는지 mean square error로 loss값 검출 
        
        # Backward pass (this is gradient descent! 경사하강법) 
        grad = self.loss.backward(predictions, y) # goal - 예측치의 미분값을 구한게 grad
        self.backward(grad) #구한 미분값 grad를 적용 
        
        # Update parameters
        # 여기에서 경사하강법으로 변화시켜줄 수치를 weight & bias에 더해준다. 
        for layer in self.layers:
            layer.update(learning_rate) 
            
        return loss

    def train(self, 
              x_train: Matrix, 
              y_train: Matrix, 
              target_loss: float = 0.1,  # Add target loss parameter
              epochs: int = 100, 
              batch_size: int = 32, 
              learning_rate: float = 0.01) -> List[float]:
        """
        Train the network
        Returns list of losses for monitoring
        """
        n_samples = x_train.rows
        losses = []
        
        for epoch in range(epochs):
            epoch_loss = 0
            # Create batches

            # Q. what is batch?
            # example
            # 전체 학습 데이터
            # x_train = Matrix([
            #     [0, 0],  # sample 1
            #     [0, 1],  # sample 2
            #     [1, 0],  # sample 3
            #     [1, 1]   # sample 4
            # ])  # shape: (4 × 2)

            # # batch_size = 2라면:
            # batch1 = Matrix([
            #     [0, 0],  # sample 1
            #     [0, 1]   # sample 2
            # ])  # shape: (2 × 2)

            # batch2 = Matrix([
            #     [1, 0],  # sample 3
            #     [1, 1]   # sample 4
            # ])  # shape: (2 × 2)

            for i in range(0, n_samples, batch_size):
                batch_x = Matrix(x_train._data[i:i + batch_size])
                batch_y = Matrix(y_train._data[i:i + batch_size])
                
                loss = self.train_step(batch_x, batch_y, learning_rate)
                epoch_loss += loss
                
            avg_loss = epoch_loss / (n_samples // batch_size)
            losses.append(avg_loss)

            # Stop if loss is good enough
            if avg_loss < target_loss:
                # print(f"Reached target loss at epoch {epoch}")
                # break
                predictions = self.predict(x_train)  # Get predictions

                # 각 예측값이 target과 0.2 차이 이내인지 확인
                all_good = all(abs(pred[0] - exp[0]) < 0.2 
                            for pred, exp in zip(predictions._data, y_train._data))
                if all_good:
                    print(f"Reached target loss at epoch {epoch}")
                    print(f"Final loss: {avg_loss}")
                    print(f"Predictions at convergence:")
                    print(predictions)
                    print(f"Expected: [[0], [1], [1], [0]]")
                    break
            
        return losses

    def predict(self, x: Matrix) -> Matrix:
        """Make predictions for input x"""
        return self.forward(x)
