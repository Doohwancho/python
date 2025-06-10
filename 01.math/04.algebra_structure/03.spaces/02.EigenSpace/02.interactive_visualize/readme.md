# what 
## 1. eigen vector?
저 주황, 핑크 선이 eigen vector이다.\
이 뜻은, 저 [3,1 \ 0,2] 행렬로 linear transformation 해도,\
저 선 위에 벡터들의 방향은 절대 안바뀜. 크기만 바뀜.

## 2. eigen value?
> Q. 크기는 얼만큼 바뀜?\
> A. eigenvalue 만큼 바뀜.\
> eigen value 계산법은 아래 설명해놓음.


## 3. 그래서 어쩌라고?
> Q. 어떤 행렬에 대해 linear transformation 해도 크기가 바꼈음 바꼈지 방향은 안바뀌는 eigen_vector이 있다 쳐, 그래서 어쩌라고?

> A. 복잡한 행렬 변환(A)도, 그것의 고유벡터(v)에게는 그저 '숫자(λ)를 곱하는' 단순한 문제로 바뀐다. --> 이래서 중요한 것

> 아무리 복잡해 보이는 변환이라도 "아, 이 변환은 결국 A축 방향으로 3배 늘리고, B축 방향으로 0.5배 줄이는 것이 전부였구나!" 하고 그 본질을 간파할 수 있게 됩니다.

> 그리고 행렬 계속 곱하는것도 단순화 시킴.

### 3-1. ex1) 행렬곱 100번하는걸 스칼라곱으로 단순화 시킴 
- ex) 어떤 시스템의 상태가 매년 행렬 A에 따라 변한다고 상상해 봅시다.
    - 1년 후 상태: Ax
    - 2년 후 상태: A(Ax)=A^2x
    - 100년 후 상태: A^100x

행렬을 100번 곱하는 것은 거의 불가능에 가까운 계산입니다. 하지만, 만약 x를 고유벡터들의 조합으로 표현할 수만 있다면 이 문제는 초등학생 수준의 산수가 됩니다.

만약 x가 고유값 3을 갖는 고유벡터 v라면,
- Ax = 3x
- A^2x = A(3x) = 3(Ax) = 3(3x) = 3^2x
- A^100x = 3^100x

복잡한 행렬 곱셈이 간단한 스칼라의 거듭제곱으로 바뀌는 마법이 일어납니다. 시스템의 장기적인 변화(날씨 예측, 인구 변화, 경제 모델)를 분석하는 데 결정적인 역할을 합니다.


### 3-2. ex2) PCA 
수많은 얼굴 사진 데이터에서 '얼굴을 구성하는 핵심적인 특징'들을 어떻게 찾을 수 있을까요? 데이터의 공분산 행렬(covariance matrix)을 만든 뒤, 그것의 고유벡터를 찾습니다. 이 고유벡터들이 바로 '평균적인 얼굴', '눈이 큰 특징', '코가 긴 특징' 등 얼굴을 구성하는 가장 중요한 '주성분'이 됩니다. (이를 Eigenface라고 부릅니다.)

수만 개의 픽셀 정보 대신, 단 몇십 개의 고유벡터 조합(좌표)만으로 얼굴을 인식할 수 있게 되어 계산이 훨씬 빠르고 효율적으로 변합니다.

결론적으로, 고유벡터와 고유값은 복잡한 시스템의 '본질적인 축과 그 힘의 크기'를 알려주는 도구입니다. 이를 통해 우리는 시스템을 더 깊이 이해하고, 미래를 예측하며, 데이터를 효율적으로 처리할 수 있게 됩니다.


### 3-3. ex3) 구글의 검색순위: 페이지 랭크 알고리즘 
구글은 "중요한 페이지로부터 링크를 많이 받은 페이지가 중요하다"는 아이디어로 웹페이지의 순위를 매깁니다. 이 관계를 거대한 행렬로 표현할 수 있습니다. 이때, 이 거대 행렬의 가장 큰 고유값(λ=1)에 해당하는 고유벡터를 찾으면, 각 웹페이지의 최종적인 '중요도 점수'가 계산됩니다. 이 점수가 바로 검색 결과의 순위가 됩니다.




# A. Eigenvalue(고유값) 계산 방법: `det(A - λI) = 0`

고유값($\lambda$)과 고유벡터($\vec{v}$)의 정의는 $A\vec{v} = \lambda\vec{v}$ 입니다. 이 식을 약간 변형하면 고유값을 계산하는 방법을 찾을 수 있습니다.

### 1단계: 특성방정식(Characteristic Equation) 유도

1.  모든 항을 왼쪽으로 옮깁니다.
    $$ A\vec{v} - \lambda\vec{v} = \vec{0} $$

2.  벡터 $\vec{v}$로 묶기 위해, 스칼라 $\lambda$에 단위행렬(Identity Matrix) $I$를 곱해줍니다. ($I\vec{v} = \vec{v}$ 이므로 식은 동일합니다)
    $$ A\vec{v} - \lambda I\vec{v} = \vec{0} $$

3.  $\vec{v}$로 묶어줍니다.
    $$ (A - \lambda I)\vec{v} = \vec{0} $$

이 식의 의미는 "**$(A - \lambda I)$라는 새로운 행렬이, 영벡터가 아닌 벡터 $\vec{v}$를 영벡터로 만드는(Null Space로 보내는) 것**"입니다.

어떤 행렬이 영벡터가 아닌 벡터를 영벡터로 만들려면, 그 행렬은 반드시 공간을 낮은 차원으로 **붕괴**시켜야 합니다. 그리고 공간이 붕괴되는 행렬의 **Determinant는 항상 0**입니다.

따라서, 우리는 고유값을 찾기 위한 다음과 같은 **특성방정식(Characteristic Equation)**을 얻게 됩니다.

$$ \det(A - \lambda I) = 0 $$

### 2단계: 행렬 $A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}$ 에 대한 계산

1.  **먼저 $(A - \lambda I)$ 행렬을 만듭니다.**
    $$
    \begin{aligned}
    A - \lambda I &= \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix} - \lambda \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \\
    &= \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix} - \begin{bmatrix} \lambda & 0 \\ 0 & \lambda \end{bmatrix} \\
    &= \begin{bmatrix} 3-\lambda & 1 \\ 0 & 2-\lambda \end{bmatrix}
    \end{aligned}
    $$

2.  **이 새로운 행렬의 Determinant를 계산합니다.** ($det\begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc$)
    $$
    \begin{aligned}
    \det(A - \lambda I) &= (3-\lambda)(2-\lambda) - (1)(0) \\
    &= 6 - 3\lambda - 2\lambda + \lambda^2 - 0 \\
    &= \lambda^2 - 5\lambda + 6
    \end{aligned}
    $$

### 3단계: 특성방정식 풀기

이제 우리가 찾은 Determinant가 0이 되는 $\lambda$ 값을 찾으면 됩니다.

$$ \lambda^2 - 5\lambda + 6 = 0 $$

이 이차방정식을 인수분해하면,
$$ (\lambda - 2)(\lambda - 3) = 0 $$

따라서, 이 방정식을 만족하는 해는 다음과 같습니다.

$$ \lambda_1 = 2, \quad \lambda_2 = 3 $$

이것이 바로 행렬 $A$의 고유값(Eigenvalues)입니다. 이 계산 과정은 시각화에서 봤던 '방향이 변하지 않는 축의 배율'이 왜 `2`와 `3`이었는지를 수학적으로 완벽하게 증명합니다.


# B. Eigenvector(고유벡터) 계산 방법: `(A - λI)v = 0`

**주어진 행렬:** $A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}$
**알고 있는 고유값:** $\lambda_1 = 3$, $\lambda_2 = 2$

---

### Case 1: 고유값 $\lambda_1 = 3$ 에 대한 고유벡터 찾기

1.  **$(A - \lambda I)$ 행렬 계산**: 식에 $\lambda = 3$을 대입합니다.
    $$
    A - 3I = \begin{bmatrix} 3-3 & 1 \\ 0 & 2-3 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & -1 \end{bmatrix}
    $$

2.  **$(A - \lambda I)\vec{v} = \vec{0}$ 방정식 세우기**: $\vec{v} = \begin{bmatrix} x \\ y \end{bmatrix}$ 라고 하고 방정식을 풉니다.
    $$
    \begin{bmatrix} 0 & 1 \\ 0 & -1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
    $$

3.  **연립방정식 풀기**:
    * 첫 번째 행: $(0 \cdot x) + (1 \cdot y) = 0 \implies y = 0$
    * 두 번째 행: $(0 \cdot x) + (-1 \cdot y) = 0 \implies y = 0$

    두 방정식 모두 우리에게 **$y=0$** 이라는 정보를 줍니다. $x$에 대한 조건은 없습니다. 즉, $x$는 어떤 값이든 될 수 있습니다.

4.  **고유벡터 찾기**:
    위 조건을 만족하는 벡터 $\vec{v}$는 $\begin{bmatrix} x \\ 0 \end{bmatrix}$ 형태를 가집니다. $x=1$로 가장 간단하게 표현하면,
    $$ \vec{v}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix} $$
    따라서, 고유값 3에 대한 고유공간(Eigenspace)은 **x축 전체**이며, 그 방향을 나타내는 가장 간단한 고유벡터(Eigenvector)는 $\vec{v}_1$ 입니다. (이것이 바로 시각화의 **보라색 선**이었습니다)

---

### Case 2: 고유값 $\lambda_2 = 2$ 에 대한 고유벡터 찾기

1.  **$(A - \lambda I)$ 행렬 계산**: 식에 $\lambda = 2$를 대입합니다.
    $$
    A - 2I = \begin{bmatrix} 3-2 & 1 \\ 0 & 2-2 \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 0 & 0 \end{bmatrix}
    $$

2.  **$(A - \lambda I)\vec{v} = \vec{0}$ 방정식 세우기**:
    $$
    \begin{bmatrix} 1 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
    $$

3.  **연립방정식 풀기**:
    * 첫 번째 행: $(1 \cdot x) + (1 \cdot y) = 0 \implies x + y = 0 \implies y = -x$
    * 두 번째 행: $(0 \cdot x) + (0 \cdot y) = 0 \implies 0 = 0$ (이 식은 아무 정보도 주지 않습니다)

    우리가 얻은 유일한 조건은 **$y = -x$** 입니다.

4.  **고유벡터 찾기**:
    위 조건을 만족하는 벡터 $\vec{v}$는 $\begin{bmatrix} x \\ -x \end{bmatrix}$ 형태를 가집니다. $x=1$로 가장 간단하게 표현하면,
    $$ \vec{v}_2 = \begin{bmatrix} 1 \\ -1 \end{bmatrix} $$
    따라서, 고유값 2에 대한 고유공간(Eigenspace)은 **$y = -x$ 직선**이며, 그 방향을 나타내는 가장 간단한 고유벡터(Eigenvector)는 $\vec{v}_2$ 입니다. (이것이 바로 시각화의 **주황색 선**이었습니다)

이처럼, 행렬과 고유값을 알면 `(A - λI)v = 0` 방정식을 풀어 그 행렬 변환의 '축'이 되는 고유벡터와 고유공간을 정확히 찾아낼 수 있습니다.