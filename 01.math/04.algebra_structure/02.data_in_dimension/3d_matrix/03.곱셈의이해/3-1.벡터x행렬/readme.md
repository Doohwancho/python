### **1. 벡터와 행렬의 곱: 변환된 기저들의 '선형 결합'**

벡터와 행렬의 곱은 단순히 숫자를 곱하는 것이 아니라, **벡터의 각 성분을 '가중치'로 사용하여 행렬의 각 열(변환된 기저 벡터)들을 조합하는 과정**입니다.

"x축 기저끼리 곱하고 y축 기저끼리 곱한다"는 개념을 조금 더 정확히 표현하면, **"벡터의 x 성분만큼 새로운 x축 기저를 가져오고, y 성분만큼 새로운 y축 기저를 가져온다"** 가 됩니다.

1.  **벡터의 의미**: 벡터 $\vec{v} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}$는 "x축 방향으로 3만큼, y축 방향으로 2만큼 가라"는 명령어입니다.
    $$ \vec{v} = 3 \begin{pmatrix} 1 \\ 0 \end{pmatrix} + 2 \begin{pmatrix} 0 \\ 1 \end{pmatrix} = 3\hat{i} + 2\hat{j} $$

2.  **행렬의 의미**: 행렬 $A = \begin{bmatrix} \color{red}2 & \color{blue}{-1} \\ \color{red}1 & \color{blue}3 \end{bmatrix}$는 "원래 x축($\hat{i}$)은 $\begin{pmatrix} \color{red}2 \\ \color{red}1 \end{pmatrix}$로, 원래 y축($\hat{j}$)은 $\begin{pmatrix} \color{blue}{-1} \\ \color{blue}3 \end{pmatrix}$으로 바꿔라"는 변환 설명서입니다.

3.  **벡터와 행렬의 곱 ($A\vec{v}$)**: 이 곱셈은 **변환된 새로운 공간**에서 "x축 방향으로 3만큼, y축 방향으로 2만큼 가라"는 명령어를 수행하는 것과 같습니다.

    즉, **벡터의 성분($3, 2$)을 가중치**로 삼아 **행렬의 열(새로운 기저 벡터)들을 선형 결합(Linear Combination)**하는 것입니다.

    $$
    \begin{align*}
    A\vec{v} &= 3 \cdot (\text{새로운 x축}) + 2 \cdot (\text{새로운 y축}) \\
    &= 3 \begin{pmatrix} \color{red}2 \\ \color{red}1 \end{pmatrix} + 2 \begin{pmatrix} \color{blue}{-1} \\ \color{blue}3 \end{pmatrix} \\
    &= \begin{pmatrix} 6 \\ 3 \end{pmatrix} + \begin{pmatrix} -2 \\ 6 \end{pmatrix} = \begin{pmatrix} 4 \\ 9 \end{pmatrix}
    \end{align*}
    $$

결론적으로 $A\vec{v}$는 **벡터 $\vec{v}$의 각 성분을 분리하여, 그 성분 값만큼 변환된 기저 벡터들을 스케일링한 후 모두 더하는 과정**입니다.

