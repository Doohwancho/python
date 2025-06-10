- 선형대수의 기본정리 (Fundamental Theorem of Linear Algebra)
    - 의미: 4대 기본 부분공간들의 차원과 관계를 명확하게 설명하는 정리입니다.
    - 행렬 변환 A는 Row Space를 Column Space로 일대일 대응시키고, Null Space를 원점으로 보내버린다는 것이 핵심 내용입니다.


# manim 설명 
가장 기본이 되는 **기저 벡터(i, j, k)** 에 간단한 3x3행렬을 곱했을 때, 어떻게 변하는지에 집중하여 4대 부분공간의 역할을 보여드리겠습니다.

- step1. before linear transformation
    - 파란색 평면: Row Space (실질적인 입력 공간) 
    - 회색 직선: Null Space (변환 시 0으로 붕괴되는 입력 공간)
        - row space와 null space는 서로 직교한다.
- step2. after linear transformation
    - 빨간색 평면: Column Space (변환 후 결과물이 도착하는 공간)
    - 보라색 직선: Left Null Space (결과물이 절대 도달할 수 없는, Column Space에 수직인 공간)
        - column space와 left null space는 서로 직교한다.
 


## 1. 행공간(Row Space)의 재료는 무엇인가?

우리는 종종 3차원 공간을 이야기할 때 당연하게 기저벡터 $\hat{i}, \hat{j}, \hat{k}$를 떠올립니다.

* $\hat{i} = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}$ (x축 방향)
* $\hat{j} = \begin{bmatrix} 0 & 1 & 0 \end{bmatrix}$ (y축 방향)
* $\hat{k} = \begin{bmatrix} 0 & 0 & 1 \end{bmatrix}$ (z축 방향)

**하지만 이 벡터들은 '공간'의 기본 구성요소일 뿐, '변환'을 정의하는 행렬 $A$의 행벡터와는 다릅니다.**

### 1-1. Manim 예제의 행렬 A 다시 보기

Manim 예제에서 사용한 행렬 $A$는 다음과 같았습니다.

$$ A = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix} $$

이 행렬 $A$의 **행벡터**들을 가로줄 그대로 꺼내보면 다음과 같습니다.

* **1행**: $\vec{r}_1 = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}$
* **2행**: $\vec{r}_2 = \begin{bmatrix} 0 & 1 & 0 \end{bmatrix}$
* **3행**: $\vec{r}_3 = \begin{bmatrix} 0 & 0 & 0 \end{bmatrix}$ (영벡터)

### 1-2. 행공간(Row Space)의 계산

행공간의 정의는 **"행벡터들이 Span하는 공간"** 입니다. 이제 위에서 꺼낸 행벡터들($\vec{r}_1, \vec{r}_2, \vec{r}_3$)로 만들 수 있는 공간을 생각해 봅시다.

1.  $\vec{r}_1 = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}$ 이 있으므로, 우리는 **x축 방향**으로 자유롭게 움직일 수 있습니다.
2.  $\vec{r}_2 = \begin{bmatrix} 0 & 1 & 0 \end{bmatrix}$ 이 있으므로, 우리는 **y축 방향**으로도 자유롭게 움직일 수 있습니다.
3.  $\vec{r}_3 = \begin{bmatrix} 0 & 0 & 0 \end{bmatrix}$ 은 영벡터이므로, Span에 아무런 새로운 방향을 추가해주지 않습니다.

결론적으로 $\text{span}(\vec{r}_1, \vec{r}_2, \vec{r}_3)$은 x축 방향과 y축 방향으로 만들어낼 수 있는 모든 벡터들의 집합, 즉 **xy-평면 전체**가 됩니다.

바로 이 때문에, 이 특정 행렬 $A$의 행공간(Row Space)이 정확히 **xy-평면**(Manim 영상의 파란색 평면)이 되는 것입니다.

사용자께서 지적하신 `[0,0,1]` 벡터($\hat{k}$)는 행렬 $A$의 행벡터가 아니므로, 이 행공간을 만드는 계산에 포함되지 않습니다.

### 1-3. 비유: 배우와 대본

이 관계를 연극에 비유할 수 있습니다.

* **무대**: 3차원 공간($\mathbb{R}^3$)
* **기본 배우들**: 기저 벡터 $\hat{i}, \hat{j}, \hat{k}$. 이들은 어떤 역할이든 맡을 수 있는 기본 배우입니다.
* **대본**: 행렬 $A$. 변환이라는 연극을 어떻게 진행할지 적혀있는 지시사항입니다.
* **행벡터**: '대사'나 '지문'에 해당합니다. 행렬 $A$라는 대본에는 "x방향으로 움직여라", "y방향으로 움직여라" 라는 대사만 있고, "z방향으로 움직여라" 라는 대사는 없습니다 (세 번째 행이 영벡터이므로).

따라서 행공간은 **대본(행렬 A)에 실제로 적혀있는 방향들(행벡터)로만** 만들어지는 공간입니다.


## 2. Column Space (열공간)에 대한 확인

> column space도 아마 계산해보면 x,y 축을 가진 평면이겠네?

네, 정확합니다! 사용한 행렬 $A = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}$ 의 열벡터들은 다음과 같습니다.

* **1열**: $\begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}$ (x축 방향)
* **2열**: $\begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}$ (y축 방향)
* **3열**: $\begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$ (영벡터)

이 세 벡터가 생성(Span)하는 공간은 영벡터를 제외한 두 벡터, 즉 x축과 y축 방향 벡터가 만드는 **xy-평면**이 맞습니다.

### 3. Null Space (영공간)에 대한 설명

> null space는 변환시 0으로 붕괴되는 지점이니까... 흠 이거 잘 이해 안되네.

Null Space를 '점'이 아닌 **'벡터들의 집합'** 또는 **'공간'**으로 이해하는 것이 중요합니다.

* **정의**: $A\vec{x} = \vec{0}$ 을 만족하는 **모든 입력 벡터 $\vec{x}$ 들의 집합**
* **의미**: 이 공간에 속한 벡터들은 행렬 $A$에 의해 변환될 때, 모두 똑같이 **원점($\vec{0}$)이라는 하나의 점으로 뭉개져 버립니다.** 즉, 변환 과정에서 정보가 완전히 소멸되는 '블랙홀' 같은 영역입니다.

우리의 예시 행렬 $A$로 계산해보면:
$$ A\vec{x} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} x \\ y \\ 0 \end{bmatrix} $$
이 결과가 영벡터 $\begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$ 가 되려면, $x=0$ 그리고 $y=0$ 이어야 합니다. $z$는 어떤 값이든 상관없습니다.
따라서 해가 되는 벡터 $\vec{x}$는 $\begin{bmatrix} 0 \\ 0 \\ z \end{bmatrix}$ 형태를 가집니다. 이것이 바로 **z축 전체**를 의미합니다. 즉, 이 행렬의 Null Space는 z축입니다.

### 4. Left Null Space 와 직교성(Orthogonality)

> left null space도 이해 안가. 그리고 아까 어떤 두 space가 perpendicular 하다고 하지 않았나?

* **Left Null Space**: 출력 공간($\mathbb{R}^m$)에서, **Column Space에 도달하지 못하는 '허공'** 을 의미합니다. 이 공간은 Column Space와 항상 **직교(perpendicular)** 합니다.
* **직교성**: Manim 예제에서 **Column Space는 xy-평면**이었습니다. 이 평면에 수직인 공간은 무엇일까요? 바로 **z축**입니다. 따라서 이 예제에서 **Left Null Space는 z축**이 됩니다.

마찬가지로, **Row Space (xy-평면)** 와 **Null Space (z-축)** 역시 서로 직교합니다.

