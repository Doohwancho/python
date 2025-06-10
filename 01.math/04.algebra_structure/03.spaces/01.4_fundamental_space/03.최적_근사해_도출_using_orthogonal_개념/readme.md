# 최소제곱법 (Least Squares)을 이용한 최적의 근사해

종종 현실 세계의 데이터는 완벽한 선형 관계를 보이지 않습니다. 이럴 때, 우리는 모든 점을 통과하는 '완벽한 해' 대신, 전체적인 오차를 최소화하는 **'최적의 근사해(Best Approximate Solution)'** 를 찾아야 합니다. 최소제곱법은 4대 부분공간과 직교성의 개념을 이용하여 이 문제를 해결하는 가장 대표적인 방법입니다.

---

## 1. 문제 설정: 선형 시스템 $A\vec{x} = \vec{b}$

아래와 같이 4개의 데이터 점 $(x, y)$가 있고, 이 점들을 가장 잘 나타내는 직선 $y = c + mx$ 를 찾는다고 가정해 봅시다.

* `(0, 1)`, `(1, 2.5)`, `(2, 2.9)`, `(3, 4.2)`

이 점들을 모두 통과하는 단 하나의 직선은 존재하지 않으므로, 아래 선형 시스템의 정확한 해 $\vec{x} = \begin{bmatrix} c \\ m \end{bmatrix}$ 은 없습니다.

$$
\underbrace{
\begin{bmatrix}
1 & 0 \\
1 & 1 \\
1 & 2 \\
1 & 3
\end{bmatrix}
}_{A}
\underbrace{
\begin{bmatrix}
c \\
m
\end{bmatrix}
}_{\vec{x}}
=
\underbrace{
\begin{bmatrix}
1 \\
2.5 \\
2.9 \\
4.2
\end{bmatrix}
}_{\vec{b}}
$$

이는 기하학적으로 "벡터 $\vec{b}$가 행렬 $A$의 **열공간(Column Space)** 안에 존재하지 않음"을 의미합니다.

---

## 2. 해결책: 정규방정식 (Normal Equation)

해가 존재하지 않을 때, 우리는 도달 가능한 영역(Column Space) 안에서 원래의 목표 $\vec{b}$와 **가장 가까운 벡터 $\vec{p}$** 를 찾습니다. 이 $\vec{p}$는 $\vec{b}$를 $A$의 Column Space에 **정사영(orthogonal projection)** 시킨 결과입니다.

그리고 우리는 이 새로운 목표 $\vec{p}$를 만족하는 방정식 $A\hat{x} = \vec{p}$를 풉니다. 이 방정식의 해인 $\hat{x}$가 바로 우리가 찾던 최적의 근사해입니다.

이 과정은 오차 벡터($\vec{b} - A\hat{x}$)가 Column Space에 직교해야 한다는 조건으로부터 다음과 같은 **정규방정식(Normal Equation)** 을 유도합니다.

$$ A^T A \hat{x} = A^T \vec{b} $$

우리는 이 방정식을 풀어 $\hat{x}$를 구합니다.