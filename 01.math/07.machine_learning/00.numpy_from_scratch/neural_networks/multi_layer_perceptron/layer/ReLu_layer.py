class ReLULayer(Layer):
    """ReLU Layer: max(0, x)"""
    def __init__(self):
        self.inputs = None

    def forward(self, inputs: Matrix) -> Matrix:
        self.inputs = inputs
        return Matrix([[max(0, x) for x in row] for row in inputs._data])

    def backward(self, grad: Matrix) -> Matrix:
        return Matrix([[g if x > 0 else 0 
                       for g, x in zip(grad_row, input_row)]
                       for grad_row, input_row in zip(grad._data, self.inputs._data)])
