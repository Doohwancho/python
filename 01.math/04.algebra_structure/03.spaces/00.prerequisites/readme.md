# what 
1. Span (생성)
    - 핵심 질문: "주어진 벡터들을 가지고 어떤 공간을 만들어낼(span) 수 있는가?"
    - 의미: 벡터들의 덧셈과 스칼라 곱을 통해 만들 수 있는 모든 가능한 벡터들의 집합입니다. 
    - 예를 들어, 2차원 공간의 벡터 [1,0]과 [0,1]이 있다면, 이 둘의 조합으로 2차원 평면 전체를 'span'할 수 있습니다.
2. Linear Independence (선형 독립)
    - 핵심 질문: "주어진 벡터들 중에 불필요한, 중복되는 벡터는 없는가?"
    - 의미: 어떤 벡터도 다른 벡터들의 조합으로 만들어질 수 없을 때, 그 벡터들은 '선형 독립'이라고 합니다. 예를 들어, [1,0]과 [0,1]은 서로를 만들 수 없으므로 선형 독립입니다. 하지만 [1,0], [0,1], [2,1] 세 벡터는 [2,1]이 앞의 두 벡터로 만들어지므로 선형 '종속'입니다.
3. Basis (기저)
    - 핵심 질문: "어떤 공간을 표현하는 데 필요한 최소한의 '재료(벡터)'는 무엇인가?"
    - 의미: 특정 공간을 span하는 선형 독립적인 벡터들의 집합입니다. 우리가 흔히 쓰는 x축, y축 벡터 [1,0], [0,1]은 2차원 공간의 수많은 기저 중 하나일 뿐입니다. 기저는 공간의 '좌표계'나 '관점'으로 생각할 수 있습니다.

# Q. what is span?

이거보면 이해감. https://youtu.be/Z9wcO_mFzE8?t=96

**Span**은 주어진 벡터들의 모든 가능한 **선형 조합(linear combination)** 으로 만들 수 있는 공간을 의미합니다. \
즉, 주어진 벡터들을 '재료'로 사용하여 덧셈과 스칼라 곱셈만으로 도달할 수 있는 모든 점들의 집합, 다시 말해 벡터들의 **'영향력의 범위'** 를 나타냅니다.

## a-1. Span의 정의

벡터 집합 $\{ \vec{v}_1, \vec{v}_2, \dots, \vec{v}_k \}$의 **Span**은 스칼라 $c_1, c_2, \dots, c_k$에 대해 다음 형태를 갖는 모든 벡터 $\vec{v}$의 집합으로 정의됩니다.

$$ \vec{v} = c_1\vec{v}_1 + c_2\vec{v}_2 + \dots + c_k\vec{v}_k $$

* **벡터 1개의 Span**: 원점을 지나고 해당 벡터와 평행한 **직선**.
* **선형 독립인 벡터 2개의 Span**: 2차원 공간에서 서로 다른 방향을 가리키는 두 벡터의 Span은 **2차원 평면 전체**($\mathbb{R}^2$).
* **선형 종속인 벡터 2개의 Span**: 두 벡터가 같은 직선 위에 있다면, 이들의 Span은 여전히 **직선**에 머무릅니다.

---

## a-2. Span의 중요성

Span은 추상적으로 보일 수 있지만, 선형대수의 여러 핵심 개념을 이해하는 데 필수적인 **기초**입니다.

### a-2-1. 부분공간 (Subspace) 정의
Span은 부분공간을 정의하는 가장 일반적인 방법입니다. 어떤 벡터들의 집합이 주어졌을 때, 그들의 Span은 항상 원점을 포함하고 덧셈과 스칼라 곱에 닫혀 있는 유효한 벡터 부분공간을 형성합니다.

### a-2-2. 행렬의 열공간 (Column Space) 이해
행렬 $A$의 **열공간(Column Space)** 은 말 그대로 행렬 $A$의 열벡터(column vectors)들의 Span입니다. 이는 $A\vec{x} = \vec{b}$ 라는 방정식에서 **도달 가능한 모든 출력 벡터 $\vec{b}$들의 집합**을 의미합니다.

### a-2-3. 선형 시스템의 해 존재 여부 판단
"$A\vec{x} = \vec{b}$ 라는 방정식의 해가 존재하는가?" 라는 질문은 "**벡터 $\vec{b}$가 행렬 $A$의 열벡터들의 Span 안에 포함되는가?**"라는 질문과 정확히 같습니다. Span의 개념을 통해 특정 문제가 풀릴 수 있는지 없는지를 기하학적으로 판단할 수 있습니다.

결론적으로 Span은 벡터들이 생성할 수 있는 '공간의 범위'를 정의함으로써, 행렬 변환의 결과와 선형 시스템의 해를 이해하는 근본적인 틀을 제공합니다.

# Q. what is linear independence?

**선형 독립**은 Span과 함께 벡터 공간을 이해하는 데 가장 중요한 기본 개념 중 하나입니다. \
직관적으로, 주어진 벡터 집합에 **'쓸모없거나 중복되는 벡터가 없는'** 상태를 의미합니다.

## b-1. 선형 독립이란 무엇인가요? 

어떤 벡터들의 집합이 주어졌을 때, 그 집합 안의 어떤 벡터도 **다른 벡터들의 조합으로 만들어질 수 없다면** 그 벡터들은 **선형 독립(Linearly Independent)** 이라고 합니다. 각 벡터가 공간에 '고유한 방향' 또는 '새로운 정보'를 추가하는 셈입니다.


### b-1-1. example 
1. vector a,b,c가 있을 때,
2. c = 2a+b 이면, 
3. c는 a,b를 조합해서 만든거니까, a,b로부터 dependent하기 때문에
4. 선형독립하지 않다. 불필요하다.


### b-1-2. 공식적인 정의

벡터 집합 $\{\vec{v}_1, \vec{v}_2, \dots, \vec{v}_k\}$가 선형 독립이라는 것은, 아래의 벡터 방정식을 만족하는 유일한 해가 **오직 모든 스칼라가 0인 경우**뿐이라는 의미입니다.

$$ c_1\vec{v}_1 + c_2\vec{v}_2 + \dots + c_k\vec{v}_k = \vec{0} \iff c_1 = c_2 = \dots = c_k = 0 $$

이를 **자명해(trivial solution)** 라고 합니다.

반대로, $c_k$ 값들 중 하나라도 0이 아닌 해가 존재한다면 그 벡터 집합은 **선형 종속(Linearly Dependent)** 이라고 합니다. 이는 적어도 하나의 벡터가 다른 벡터들의 조합으로 표현될 수 있어 '중복'된다는 뜻입니다.

---

## b-2. 왜 중요한가요?

선형 독립은 여러 핵심적인 선형대수 개념의 기초가 되는 '자격 요건'과 같습니다.

1.  **기저(Basis)와 차원(Dimension)의 정의**
    * 벡터 공간의 **기저(Basis)** 는 그 공간 전체를 Span(생성)하는 **선형 독립적인** 벡터들의 집합입니다.
    * **차원(Dimension)** 은 그 기저를 구성하는 벡터의 개수입니다.
    * 선형 독립 조건이 없다면, 우리는 공간을 표현하는 데 불필요하게 많은 벡터를 사용하게 될 것입니다. 선형 독립은 공간을 표현하는 **가장 효율적이고 최소한의 '뼈대'** 를 찾도록 보장합니다.

2.  **표현의 유일성 (Uniqueness)**
    * 어떤 벡터를 기저 벡터들의 조합으로 표현할 때, 그 조합(좌표)은 **오직 한 가지 방법**으로만 존재합니다. 이는 기저 벡터들이 선형 독립이기 때문에 가능합니다. 만약 종속이라면, 같은 벡터를 표현하는 방법이 무한히 많아져 좌표계로서의 의미를 잃게 됩니다.

3.  **행렬의 가역성(Invertibility) 판단**
    * 정사각형 행렬 $A$의 역행렬($A^{-1}$)이 존재하는지 여부는 **행렬 $A$의 열벡터들이 선형 독립인지**와 동치입니다.
    * 열벡터들이 선형 종속이라면, 변환 시 공간이 붕괴(차원 축소)된다는 의미이며, 이는 $det(A) = 0$ 이고 역행렬이 존재하지 않음을 뜻합니다.

4.  **Rank의 정의**
    * 행렬의 **Rank**는 그 행렬의 열벡터들 중 선형 독립인 벡터의 최대 개수입니다. Rank는 곧 선형 독립인 벡터가 몇 개인지를 알려주는 직접적인 척도입니다.

---

## b-3. 어디에 쓰이나요? 

선형 독립은 이론을 넘어 다양한 실제 분야에서 데이터의 중복을 제거하고 핵심을 파악하는 데 사용됩니다.

* **머신러닝 및 데이터 과학**: 데이터셋의 각 특성(feature)을 벡터로 볼 수 있습니다. 만약 두 특성이 서로 매우 높은 상관관계를 보인다면, 이들은 거의 선형 종속에 가깝습니다. 이런 경우 한 특성을 제거하여 모델을 단순화하고 과적합(overfitting)을 방지하며 성능을 높일 수 있습니다.

* **주성분 분석 (PCA)**: 고차원 데이터의 차원을 축소하는 대표적인 기법입니다. 데이터가 가장 넓게 분포하는 '축'들을 찾는데, 이 축들은 서로 직교하며 **선형 독립**입니다. PCA는 데이터의 본질적인 구조를 설명하는 새로운 기저를 찾는 과정입니다.

* **공학 및 신호 처리**: 복잡한 신호나 힘을 분석할 때, 이를 다루기 쉬운 **선형 독립적인** 기본 요소(예: 사인파와 코사인파)들의 합으로 분해합니다. 푸리에 변환(Fourier Transform)이 대표적인 예입니다.


# Q. what is basis?

**기저(Basis)** 란 어떤 벡터 공간을 생성(span)하는 **선형 독립(linearly independent)** 적인 벡터들의 집합입니다. \
직관적으로, 기저는 해당 공간을 설명하는 데 필요한 **최소한의 '뼈대' 또는 '좌표계'** 역할을 합니다.

## c-1. 기저의 정의

어떤 벡터 공간 $V$에 속한 벡터들의 집합 $B = \{\vec{v}_1, \vec{v}_2, \dots, \vec{v}_n\}$가 다음 두 가지 조건을 모두 만족할 때, $B$를 $V$의 기저라고 합니다.

1.  **선형 독립 (Linearly Independent)**: 집합 $B$의 어떤 벡터도 다른 벡터들의 선형 조합으로 표현될 수 없습니다. 즉, 불필요하거나 중복되는 벡터가 없어야 합니다.

2.  **생성 (Span)**: 집합 $B$에 속한 벡터들의 선형 조합으로 공간 $V$의 모든 벡터를 만들어낼 수 있어야 합니다. 즉, $\text{span}(\vec{v}_1, \vec{v}_2, \dots, \vec{v}_n) = V$ 여야 합니다.

---

## c-2. 기저는 왜 중요한가?

기저는 벡터 공간의 구조를 이해하는 데 가장 근본적인 개념입니다.

### c-2-1. 좌표계의 역할을 합니다.
기저는 공간의 모든 벡터에 대해 **유일한 주소(좌표)를 부여**합니다. 예를 들어, $\mathbb{R}^2$의 표준 기저 $B = \{\hat{i}, \hat{j}\}$가 있을 때, 벡터 $\vec{v} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}$는 $3\hat{i} + 2\hat{j}$로 유일하게 표현됩니다. 만약 기저가 선형 종속이거나 공간 전체를 생성하지 못한다면, 좌표가 없거나 무한히 많아져 시스템이 붕괴됩니다.

### c-2-2. 공간의 차원(Dimension)을 결정합니다.
어떤 벡터 공간에 대해, 기저를 구성하는 **벡터의 개수는 항상 동일**합니다. 이 개수를 바로 그 공간의 **차원(Dimension)**이라고 정의합니다.
* $\mathbb{R}^2$ (2차원 평면)의 기저는 항상 2개의 벡터로 이루어집니다.
* $\mathbb{R}^3$ (3차원 공간)의 기저는 항상 3개의 벡터로 이루어집니다.

### c-2-3. 선형 변환(Linear Transformation)을 단순화합니다.
복잡한 행렬 변환이 기저 벡터들에게 어떤 영향을 미치는지만 알면, 그 공간의 다른 모든 벡터들이 어떻게 변환될지 예측할 수 있습니다. 즉, 몇 개의 기저 벡터 변환만으로 전체 공간의 변환을 설명할 수 있게 됩니다.

---

### c-2-4. 예시

* **표준 기저 (Standard Basis)**: 우리가 가장 흔하게 사용하는 기저입니다.
    * $\mathbb{R}^2$의 표준 기저: $\left\{ \hat{i} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \hat{j} = \begin{bmatrix} 0 \\ 1 \end{bmatrix} \right\}$

* **새로운 기저 (A New Basis)**: 하나의 공간에는 무수히 많은 기저가 존재할 수 있습니다.
    * $\left\{ \begin{bmatrix} 2 \\ 1 \end{bmatrix}, \begin{bmatrix} -1 \\ 1 \end{bmatrix} \right\}$ 또한 $\mathbb{R}^2$를 정의하는 유효한 기저입니다.

* **기저가 아닌 경우**:
    * $\left\{ \begin{bmatrix} 1 \\ 1 \end{bmatrix}, \begin{bmatrix} 2 \\ 2 \end{bmatrix} \right\}$: 선형 종속이므로 기저가 아닙니다.
    * $\left\{ \begin{bmatrix} 1 \\ 1 \end{bmatrix} \right\}$: $\mathbb{R}^2$ 전체를 span할 수 없으므로 $\mathbb{R}^2$의 기저가 아닙니다. (직선에 대한 기저는 될 수 있습니다.)


