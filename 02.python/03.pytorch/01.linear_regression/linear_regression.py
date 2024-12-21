import torch
import torch.nn as nn
import torch.optim as optim

print(torch.__version__)
print(optim.SGD)

# Data (inputs and corresponding outputs)
x_train = torch.tensor([[1.0], [2.0], [3.0], [4.0]], dtype=torch.float32)
y_train = torch.tensor([[2.0], [4.0], [6.0], [8.0]], dtype=torch.float32)

# Model definition
class LinearRegressionModel(nn.Module):
    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        self.linear = nn.Linear(1, 1)  # input and output are 1D

    def forward(self, x):
        return self.linear(x)

# Create the model
model = LinearRegressionModel()

# Loss and optimizer
criterion = nn.MSELoss()  # Mean Squared Error
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Training loop
epochs = 1000
for epoch in range(epochs):
    model.train()

    # Forward pass: compute predictions
    y_pred = model(x_train)

    # Compute loss
    loss = criterion(y_pred, y_train)

    # Backward pass: compute gradients and update weights
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Print progress
    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

# Testing the model
model.eval()
with torch.no_grad():
    predicted = model(x_train)
    print(f"Predicted values: \n{predicted}")

