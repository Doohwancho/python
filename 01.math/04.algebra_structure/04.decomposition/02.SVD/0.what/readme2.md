# what 

SVD도 eigen decomposition처럼,
1. 일단 어떤 행렬 곱해서 linear transformation해서 다른 축? 공간?으로 간 다음 
2. 특정 값을 곱하고 
3. 다시 돌아오는 식

> "복잡한 문제를 풀기 쉬운 '특별한 관점(좌표계)'으로 이동해서, 그 쉬운 관점에서 문제를 해결하고, 결과를 다시 원래의 관점으로 가져온다."

다만, eigen decomposition은 eigen space로 가서 eigen vector들에게 eigen value값만큼 곱하는 것이고,\
SVD는 V^t로 갔다가 다시 V^t에 transpose를 곱해서 돌아오는게 아니라, U를 곱해서 돌아옴

---

### **1. SVD, 왜 필요할까요? (고유값 분해의 한계)**

이전 설명에서 고유값 분해($A=PDP^{-1}$)는 **정사각형 행렬**에만 쓸 수 있는 '특수 기술'이라고 했습니다. 하지만 세상에는 키와 몸무게 데이터처럼 행과 열의 개수가 다른 **직사각형 행렬**이 훨씬 많습니다.

SVD(특이값 분해)는 바로 이 **모든 직사각형 행렬에 사용할 수 있는 일반 기술**, 즉 '끝판왕' 분해 방법입니다.

---

### **2. SVD의 핵심 아이디어: 모든 변환은 세 가지 행동의 조합이다 🤹**

SVD의 핵심은 아무리 복잡해 보이는 행렬 변환이라도, 결국 아래 세 가지 단순한 행동의 조합이라는 것입니다.

> **모든 행렬 변환은 "회전 → 신축 → 또 다른 회전" 이다.**

SVD는 이 세 가지 행동에 해당하는 세 개의 행렬($U, \Sigma, V^T$)을 찾아주는 과정입니다.

$$ A = U \Sigma V^T $$

---

### **3. SVD의 3단계 여행: A = UΣV^T**

어떤 벡터 $\vec{x}$가 행렬 $A$를 만나 $A\vec{x}$로 변환되는 과정을 3단계 우회 경로로 따라가 보겠습니다.

#### **1단계: $V^T$ - 출발 공간의 '특별한 축' 찾기 (첫 번째 회전)**

-   **역할**: 공간을 회전시켜서, 변환하기에 **가장 편한 축**을 찾습니다.
-   **의미**: 행렬 $A$로 변환을 했을 때, 서로 수직이었던 벡터들이 변환 후에도 여전히 **수직 관계를 유지하는 특별한 축들**이 존재합니다. 행렬 $V$의 열벡터들($\vec{v_1}, \vec{v_2}, \dots$)이 바로 이 특별한 축(방향)들입니다. $V^T$는 이 축들을 기준으로 공간을 바라보도록 **회전**시키는 역할을 합니다.
-   **결과**: 입력 벡터 $\vec{x}$가 이 '특별한 축' 기준으로 표현됩니다.


#### **2단계: $\Sigma$ - 각 축 방향으로 늘리기/줄이기 (신축)**

-   **역할**: '특별한 축' 방향으로 벡터를 늘리거나 줄입니다.
-   **의미**: 이 특별한 축 위에서는 복잡한 변환이 아닌, **단순한 '신축'** 만 일어납니다. 대각행렬 $\Sigma$의 대각 원소인 **특이값(Singular Value, $\sigma$)** 들이 바로 각 축의 **신축률**입니다. $\sigma_1$은 첫 번째 특별 축($\vec{v_1}$) 방향의 신축률, $\sigma_2$는 두 번째 특별 축($\vec{v_2}$) 방향의 신축률입니다.
-   **결과**: 회전된 벡터가 각 축 방향으로 $\sigma_1, \sigma_2, \dots$ 배만큼 크기가 변합니다.


#### **3단계: $U$ - 도착 공간의 '결과 축' 정렬 (두 번째 회전)**

-   **역할**: 신축된 결과를 최종 목적지에 맞게 회전시킵니다.
-   **의미**: 2단계에서 신축된 벡터들(원래 $\vec{v_1}, \vec{v_2}$가 변환된 결과)이 도착 공간에서 새로운 수직축들을 이룹니다. 이 **결과 축의 방향**을 알려주는 것이 바로 행렬 $U$입니다. 행렬 $U$는 이 결과물을 최종 방향에 맞게 **회전**시켜 변환을 마무리합니다.
-   **결과**: 최종 변환된 벡터 $A\vec{x}$가 얻어집니다.


---

### **4. 그래서 V, U, Σ는 어떻게 찾나요? (고유값 분해와의 연결고리)**

이제야 처음 봤던 어려운 내용이 등장합니다. "회전-신축-회전"이라는 아이디어는 알겠는데, 그 회전 각도($V, U$)와 신축률($\Sigma$)은 어떻게 계산할까요?

> **SVD는 $A$와 관련된 특수한 정사각형 행렬($A^TA$와 $AA^T$)을 '고유값 분해'해서 찾습니다.**

-   **$V$ (출발 공간의 특별한 축)**: $A^TA$를 고유값 분해해서 찾습니다.
-   **$U$ (도착 공간의 결과 축)**: $AA^T$를 고유값 분해해서 찾습니다.
-   **$\Sigma$ (신축률)**: 위에서 구한 고유값($\lambda$)들에 루트를 씌워서 찾습니다 ($\sigma = \sqrt{\lambda}$).

지금 당장 $A^TA$의 의미를 깊게 파고들기보다, **"아, SVD의 재료들을 구하기 위해 고유값 분해라는 도구를 쓰는구나!"** 라고 이해하는 것이 정신 건강에 좋습니다.

---

### **5. 최종 요약: SVD는 '변환의 뼈대'를 보여준다**

-   SVD는 모든 행렬 변환 $A$를 **[회전($V^T$)] → [신축($\Sigma$)] → [회전($U$)]** 으로 분해합니다.
-   **신축률($\sigma$)이 큰 축**이 그 변환에서 **가장 중요한 방향(뼈대)**입니다.
-   신축률이 작은 축은 상대적으로 덜 중요하므로, 이 부분을 생략해서 데이터를 압축(PCA)하거나 노이즈를 제거할 수 있습니다.

