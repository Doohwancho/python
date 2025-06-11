# matrix는 정규직교 기저가 어떻게 변하는지 표현해 놓은것일 뿐이다.

### **1. 모든 공간은 '기저(Basis)'로 이루어져 있다**

우리가 흔히 사용하는 2차원 데카르트 좌표계($xy$ 평면)를 생각해 봅시다. 이 공간은 사실 두 개의 서로 수직이고 길이가 1인 **기저 벡터(Basis Vector)** 로 이루어져 있습니다.

-   $\hat{i} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ (x축 방향의 단위벡터)
-   $\hat{j} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ (y축 방향의 단위벡터)

이 둘은 서로 수직(orthogonal)이고 길이가 1(normal)이므로 **정규직교 기저(Orthonormal Basis)** 가 됩니다.

공간상의 모든 벡터 $\vec{v} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}$는 이 기저 벡터들의 선형 결합으로 표현됩니다.

$$ \vec{v} = 3\begin{bmatrix} 1 \\ 0 \end{bmatrix} + 2\begin{bmatrix} 0 \\ 1 \end{bmatrix} = 3\hat{i} + 2\hat{j} $$

---

### **2. 행렬의 열 = 변환된 기저 벡터의 '목적지'**

**행렬의 가장 중요한 역할은 이 기저 벡터들이 선형 변환 후 어디로 가는지를 알려주는 것입니다.**

예를 들어, 행렬 $A = \begin{bmatrix} 2 & -1 \\ 1 & 3 \end{bmatrix}$ 가 있다고 합시다.

-   행렬 $A$의 **첫 번째 열** $\begin{bmatrix} 2 \\ 1 \end{bmatrix}$은, 원래 x축 방향 기저 벡터였던 $\hat{i} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$가 변환 후 도착하는 **새로운 위치**입니다.
    $$ A\hat{i} = \begin{bmatrix} 2 & -1 \\ 1 & 3 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 2 \\ 1 \end{bmatrix} $$

-   행렬 $A$의 **두 번째 열** $\begin{bmatrix} -1 \\ 3 \end{bmatrix}$은, 원래 y축 방향 기저 벡터였던 $\hat{j} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$가 변환 후 도착하는 **새로운 위치**입니다.
    $$ A\hat{j} = \begin{bmatrix} 2 & -1 \\ 1 & 3 \end{bmatrix} \begin{bmatrix} 0 \\ 1 \end{bmatrix} = \begin{bmatrix} -1 \\ 3 \end{bmatrix} $$

즉, 행렬 $A$는 **"기존의 표준 기저 $\hat{i}, \hat{j}$가 각각 $\begin{bmatrix} 2 \\ 1 \end{bmatrix}$와 $\begin{bmatrix} -1 \\ 3 \end{bmatrix}$으로 바뀐다"** 라는 변환 정보를 압축해 놓은 설명서와 같습니다.

---

### **3. 결론: 행렬 곱셈의 의미**

이 원리를 알면 행렬과 벡터의 곱셈 $A\vec{v}$가 왜 그렇게 계산되는지 직관적으로 이해할 수 있습니다.

앞서 본 벡터 $\vec{v} = 3\hat{i} + 2\hat{j}$를 행렬 $A$로 변환하는 것은, **변환된 새로운 기저 벡터**들을 동일한 비율로 조합하는 것과 같습니다.

$$
\begin{align*}
A\vec{v} &= A(3\hat{i} + 2\hat{j}) \\
&= 3(A\hat{i}) + 2(A\hat{j}) \\
&= 3\begin{bmatrix} 2 \\ 1 \end{bmatrix} + 2\begin{bmatrix} -1 \\ 3 \end{bmatrix} \\
&= \begin{bmatrix} 6 \\ 3 \end{bmatrix} + \begin{bmatrix} -2 \\ 6 \end{bmatrix} = \begin{bmatrix} 4 \\ 9 \end{bmatrix}
\end{align*}
$$

결국 행렬은 **좌표계의 축(기저)들이 어떻게 변형되는지에 대한 정보를 담고 있는 컨테이너**이며, 이 정보만 알면 공간상의 모든 벡터가 어떻게 변환될지 예측할 수 있습니다. 

따라서 `matrix는 정규직교 기저가 어떻게 변하는지 표현해 놓은 것일 뿐이다`라는 말은 선형대수의 핵심을 꿰뚫는 완벽한 설명입니다.


### 4. 다시 내 언어로 
1. 2x2행렬은 (x축 기저, y축 기저)가 어떻게 변환되는지 알려주는거고
2. 3x3행렬은 (x축 기저, y축 기저, z축 기저)가 어떻게 변환되는지 알려주는거고,
3. 4x4행렬은 (x축 기저, y축 기저, z축 기저, k축 기저)가 어떻게 변환되는지 알려주는거다.

`Ax=b`에서 vector_x를 linear transform하는게 행렬 A라 했는데,\
linear transform할 때, manim에서 보면, x,y,z축 자체가 변하는게 보이는데,\
그게 다 정규직교 기저가 변하는 만큼, 저 x,y,z축이 변하는 것이다.

왜냐면 정규직교 기저 [1, 0 \ 0, 1]은 x,y축에 1씩 증가되는 눈금과 같기 떄문.


### 5. example 

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
