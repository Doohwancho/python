### **1. 벡터의 성분 (x, y, z축 요소)**

벡터에서 x, y, z축 요소는 해당 벡터가 각 축 방향으로 얼마나 나아가는지를 나타내는 **스칼라(scalar) 값**입니다.

#### **세로 벡터 (열벡터, Column Vector)**

3차원 공간의 한 점을 나타내는 벡터 $\vec{v}$가 있다면, 다음과 같이 표현합니다.

$$ \vec{v} = \begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} 3 \\ 4 \\ 5 \end{bmatrix} $$

-   **x축 요소 (x-component)**: 3 (x축 방향으로 3만큼의 크기를 가짐)
-   **y축 요소 (y-component)**: 4 (y축 방향으로 4만큼의 크기를 가짐)
-   **z축 요소 (z-component)**: 5 (z축 방향으로 5만큼의 크기를 가짐)

이 벡터는 원점에서 시작하여 x축으로 3, y축으로 4, z축으로 5만큼 이동한 지점을 가리키는 화살표라고 생각할 수 있습니다.

#### **가로 벡터 (행벡터, Row Vector)**

벡터를 가로로 나열하는 방식도 있으며, 이를 **행벡터(Row Vector)** 라고 합니다. 행벡터는 열벡터를 눕혀놓은 것, 즉 **전치(Transpose)** 시킨 것과 같습니다.

$$ \vec{v}^T = \begin{bmatrix} x & y & z \end{bmatrix} = \begin{bmatrix} 3 & 4 & 5 \end{bmatrix} $$

-   **표준**: 대부분의 교재와 논문에서는 벡터를 열벡터로 간주합니다. 이는 행렬 곱셈 $A\vec{x}$의 연산 규칙과 자연스럽게 맞아떨어지기 때문입니다.
-   **용도**: 행벡터는 특정 계산이나 다른 관점(예: 데이터를 표현할 때)에서 사용되기도 합니다.

---

### **2. 행렬과 x, y, z축의 관계**

이제 가장 흥미로운 질문입니다: **"x, y, z축 요소가 벡터가 아니라 행렬인 경우"**

이것은 매우 중요한 개념적 전환입니다.

> **결론부터 말하면, 행렬은 x, y, z '요소'를 갖는 것이 아니라, 행렬의 '열(column)' 자체가 변환된 새로운 x, y, z축 '벡터'가 됩니다.**

이전 질문에서 "matrix는 정규직교 기저가 어떻게 변하는지 표현해 놓은 것"이라고 이해하신 것과 정확히 같은 맥락입니다.

3x3 행렬 $A$가 있다고 가정해 봅시다.

$$ A = \begin{bmatrix} \color{red}2 & \color{blue}0 & \color{green}0 \\ \color{red}0 & \color{blue}3 & \color{green}0 \\ \color{red}0 & \color{blue}0 & \color{green}4 \end{bmatrix} $$

이 행렬 $A$를 공간에 대한 변환(transformation)으로 해석하면 다음과 같습니다.

-   **첫 번째 열 $\begin{bmatrix} \color{red}2 \\ \color{red}0 \\ \color{red}0 \end{bmatrix}$**: 원래 **x축 기저 벡터** $\begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix}$가 변환된 **새로운 x축의 모습**입니다. 즉, x축 방향으로 2배 늘어났습니다.

-   **두 번째 열 $\begin{bmatrix} \color{blue}0 \\ \color{blue}3 \\ \color{blue}0 \end{bmatrix}$**: 원래 **y축 기저 벡터** $\begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}$가 변환된 **새로운 y축의 모습**입니다. 즉, y축 방향으로 3배 늘어났습니다.

-   **세 번째 열 $\begin{bmatrix} \color{green}0 \\ \color{green}0 \\ \color{green}4 \end{bmatrix}$**: 원래 **z축 기저 벡터** $\begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}$가 변환된 **새로운 z축의 모습**입니다. 즉, z축 방향으로 4배 늘어났습니다.

만약 행렬이 더 복잡하다면, 축들이 회전하고 늘어나는 변환을 동시에 표현합니다.

$$ B = \begin{bmatrix} \color{red}{0.8} & \color{blue}{-0.6} & \color{green}0 \\ \color{red}{0.6} & \color{blue}{0.8} & \color{green}0 \\ \color{red}0 & \color{blue}0 & \color{green}1 \end{bmatrix} $$

-   **첫 번째 열**: 새로운 x축은 $\begin{pmatrix} 0.8 \\ 0.6 \\ 0 \end{pmatrix}$ 벡터 방향이 됩니다.
-   **두 번째 열**: 새로운 y축은 $\begin{pmatrix} -0.6 \\ 0.8 \\ 0 \end{pmatrix}$ 벡터 방향이 됩니다.
-   (이 경우 z축은 변하지 않았습니다.)
-   이 행렬 $B$는 z축을 기준으로 공간을 약 36.87도 회전시키는 변환을 나타냅니다.

---

### **핵심 요약**

| 구분 | 의미 | 구성 요소 |
| :--- | :--- | :--- |
| **벡터 (Vector)** | 공간 속의 **한 점 또는 방향** | **스칼라** 값들 (x, y, z 좌표) |
| **행렬 (Matrix)**| 공간 자체의 **변환(Transformation)** | **벡터**들 (변환된 새로운 축들의 좌표) |

따라서 "행렬의 x, y, z축 요소"를 생각할 때는, 행렬의 각 **열(column)**이 **변환 후의 새로운 x축, y축, z축 벡터**라고 이해하는 것이 가장 정확합니다.
