# 행렬 곱셈과 기하학적 사영의 결과는 같은가?

네, 완벽하게 같습니다.

행렬 곱셈이라는 순수한 산술 과정의 **결과**는, '사영(Projection)'이라는 기하학적 변환의 **결과**와 정확히 일치합니다. 아래는 Manim 예제에서 사용된 값으로 직접 증명한 것입니다.

---

### 주어진 값

* 3D 벡터: $\vec{v}_{3D} = \begin{bmatrix} 2 \\ 2 \\ 3 \end{bmatrix}$
* 2x3 행렬: $A = \begin{bmatrix} 1 & 0.5 & 0 \\ 0 & 1 & 0.5 \end{bmatrix}$

---

### 방법 1: 순수한 행렬 곱셈

'사영'이라는 개념 없이, 오직 정해진 산술 규칙에 따라 계산합니다.

$$
\begin{aligned}
A \vec{v}_{3D} &= \begin{bmatrix} 1 & 0.5 & 0 \\ 0 & 1 & 0.5 \end{bmatrix} \begin{bmatrix} 2 \\ 2 \\ 3 \end{bmatrix} \\
&= \begin{bmatrix} (1 \cdot 2) + (0.5 \cdot 2) + (0 \cdot 3) \\ (0 \cdot 2) + (1 \cdot 2) + (0.5 \cdot 3) \end{bmatrix} \\
&= \begin{bmatrix} 2 + 1 + 0 \\ 0 + 2 + 1.5 \end{bmatrix} \\
&= \begin{bmatrix} 3 \\ 3.5 \end{bmatrix}
\end{aligned}
$$

**결과: $\begin{bmatrix} 3 \\ 3.5 \end{bmatrix}$**

---

### 방법 2: 기하학적 사영 해석

행렬 $A$가 "3차원 공간의 기본 축들을 2차원 공간 어디로 보내는가"에 대한 지시서라고 해석합니다.

* $\text{Projection}(\hat{i}) = \text{Projection}\left(\begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}\right) = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ (A의 1열)
* $\text{Projection}(\hat{j}) = \text{Projection}\left(\begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}\right) = \begin{bmatrix} 0.5 \\ 1 \end{bmatrix}$ (A의 2열)
* $\text{Projection}(\hat{k}) = \text{Projection}\left(\begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}\right) = \begin{bmatrix} 0 \\ 0.5 \end{bmatrix}$ (A의 3열)

$\vec{v}_{3D}$는 $2\hat{i} + 2\hat{j} + 3\hat{k}$ 이므로, 전체 벡터의 사영 결과는 각 기저 벡터 사영 결과의 합과 같습니다.

$$
\begin{aligned}
\text{Projection}(\vec{v}_{3D}) &= 2 \cdot \text{Projection}(\hat{i}) + 2 \cdot \text{Projection}(\hat{j}) + 3 \cdot \text{Projection}(\hat{k}) \\
&= 2 \begin{bmatrix} 1 \\ 0 \end{bmatrix} + 2 \begin{bmatrix} 0.5 \\ 1 \end{bmatrix} + 3 \begin{bmatrix} 0 \\ 0.5 \end{bmatrix} \\
&= \begin{bmatrix} 2 \\ 0 \end{bmatrix} + \begin{bmatrix} 1 \\ 2 \end{bmatrix} + \begin{bmatrix} 0 \\ 1.5 \end{bmatrix} \\
&= \begin{bmatrix} 2+1+0 \\ 0+2+1.5 \end{bmatrix} \\
&= \begin{bmatrix} 3 \\ 3.5 \end{bmatrix}
\end{aligned}
$$

**결과: $\begin{bmatrix} 3 \\ 3.5 \end{bmatrix}$**

---

### 결론

두 방법의 결과는 완벽하게 일치합니다. **행렬 곱셈**은 **선형 변환**이라는 기하학적 작용을 대수적으로 표현하기 위해 만들어진 연산이기 때문입니다. '사영'이라는 시각적 해석은 이 연산의 의미를 설명하는 효과적인 스토리텔링이며, 그 스토리는 수학적 진실에 정확히 부합합니다.