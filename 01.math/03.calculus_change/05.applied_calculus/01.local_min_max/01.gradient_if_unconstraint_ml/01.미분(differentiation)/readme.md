# what 
미분하는 방식이 원함수가 어떤 특수함수인지에 따라 달라짐 

1. x^n인 함수의 경우 (가장 일반적인 경우)
    - 미분은 그냥 도함수 먹이듯이 찻수-1 하고 앞에 변수로 내리는걸 모든 변수에 반복하면 됨
2. **삼각함수**: $\sin(x) \rightarrow \cos(x)$
3. **지수/로그함수**: $e^x \rightarrow e^x$, $\ln(x) \rightarrow \frac{1}{x}$
4. **곱의 미분법**: $h(x) = f(x)g(x) \rightarrow h'(x) = f'(x)g(x) + f(x)g'(x)$
5. **연쇄 법칙(Chain Rule)**: $h(x) = f(g(x)) \rightarrow h'(x) = f'(g(x))g'(x)$ (딥러닝 역전파의 핵심)
    - 함성함수 (ex. f(g(x)))얘네 미분할 때 사용하는 방법
    - 딥러닝 backpropagation이 중요한 원리가 된다. 

즉 미분이란, 하나의 공식이 아니라, 함수에 형태에 따라 적용되는 여러 공식들의 집합체이다. 

