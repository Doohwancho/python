class Tanh(Activation):
    """Hyperbolic tangent activation"""
    @staticmethod
    def forward(x: NDArray) -> NDArray:
        def tanh(x):
            if x < -700:
                return -1
            elif x > 700:
                return 1
            ex = math.exp(x)
            enx = math.exp(-x)
            return (ex - enx) / (ex + enx)
        return NDArray([tanh(xi) for xi in x])

    @staticmethod
    def backward(x: NDArray) -> NDArray:
        # derivative of tanh is 1 - tanh²(x)
        fx = Tanh.forward(x)
        return NDArray([1 - fi * fi for fi in fx])
