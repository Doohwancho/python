
class SigmoidLayer(Layer):
    """Sigmoid Layer: 1/(1 + e^-x)"""
    def __init__(self):
        self.outputs = None

    def forward(self, inputs: Matrix) -> Matrix:
        def sigmoid(x):
            if x < -700: return 0
            if x > 700: return 1
            return 1/(1 + math.exp(-x))
            
        self.outputs = Matrix([[sigmoid(x) for x in row] for row in inputs._data])
        return self.outputs

    def backward(self, grad: Matrix) -> Matrix:
        return Matrix([[g * out * (1 - out) 
                       for g, out in zip(grad_row, output_row)]
                       for grad_row, output_row in zip(grad._data, self.outputs._data)])
