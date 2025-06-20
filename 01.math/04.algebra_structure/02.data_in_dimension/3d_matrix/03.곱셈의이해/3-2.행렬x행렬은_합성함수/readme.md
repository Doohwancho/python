### **2. 행렬과 행렬의 곱: 변환(함수)의 '합성'**

행렬과 행렬의 곱셈 $AB$는 **두 개의 선형 변환(함수)을 순서대로 적용하는 것을 하나의 새로운 변환(함수)으로 합치는 과정**입니다. 이는 수학의 **함수 합성(Function Composition)** 개념과 정확히 일치합니다.

> **$g(f(x))$ 와 같이 함수 $f$를 먼저 적용하고, 그 결과를 다시 함수 $g$에 적용하는 것과 같습니다.**

1.  **두 개의 변환**: 공간을 변환하는 두 행렬(함수) $A$와 $B$가 있다고 합시다.
    -   $B$: 1차 변환 (함수 $f$)
    -   $A$: 2차 변환 (함수 $g$)

2.  **순차적 적용**: 어떤 벡터 $\vec{x}$를 먼저 $B$로 변환하고, 그 결과를 다시 $A$로 변환해 봅시다.
    -   1단계: $B$ 변환 적용 $\rightarrow B\vec{x}$
    -   2단계: 위 결과에 $A$ 변환 적용 $\rightarrow A(B\vec{x})$

3.  **하나의 변환으로 합치기**: 이 두 단계를 한 번에 처리하는 새로운 행렬 $C$를 만들 수 있는데, 이것이 바로 행렬 곱 $AB$ 입니다.
    $$ C\vec{x} = A(B\vec{x}) \implies C = AB $$

    **주의할 점**은 연산 순서입니다. 벡터에 가까운 **오른쪽 행렬 $B$가 먼저 적용**됩니다. 따라서 $AB \neq BA$ 입니다.

#### **$C = AB$의 의미**

새로운 변환 행렬 $C$의 각 열은 무엇을 의미할까요?

-   **$C$의 첫 번째 열**: 원래의 x축 기저 벡터($\hat{i}$)가 **$B$로 변환된 후, 다시 $A$로 변환된 최종 목적지**입니다.
    -   $B$로 변환: $B\hat{i}$ (이는 $B$의 첫 번째 열입니다.)
    -   다시 $A$로 변환: $A(B\hat{i})$ (이는 $A$와 '$B$의 첫 번째 열'을 곱한 것입니다.)

이것이 행렬 곱셈을 우리가 아는 방식으로 계산하는 이유입니다. $AB$의 첫 번째 열은 $A$와 $B$의 첫 번째 열을 곱해서 구하고, $AB$의 두 번째 열은 $A$와 $B$의 두 번째 열을 곱해서 구하는 식입니다.

결론적으로, 행렬 곱셈 $AB$는 **"B 변환을 하고, 연이어 A 변환을 하라"** 는 두 가지 연속된 명령을, **단 한 번에 처리하는 새로운 변환 행렬을 만드는 과정**입니다.