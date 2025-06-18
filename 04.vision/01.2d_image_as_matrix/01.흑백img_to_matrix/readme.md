# Goal 

2d image -> matrix로 변환 -> matrix transformation -> image로 visualize 

# Index 

1. 10 x 10 pixels (small)
2. black color
3. matrix로 추출 
4. 행렬 곱셈을 이용하여 이미지 회전(rotate)
5. 행렬 곱셈을 이용하여 이미지 뒤집기(reflection)
6. 행렬 곱셈을 이용하여 이미지 스케일링(scaling)
7. 외곽선 인지(edge detection)
    - Convolution (컨볼루션): 이미지 처리에서 필터(커널)를 사용하여 픽셀 값을 변환하는 작업입니다. 이는 사실상 행렬 곱셈의 한 형태입니다. 필터 행렬이 이미지 행렬 위를 슬라이딩하면서 각 위치에서 원소별 곱셈 및 합산을 수행합니다.
    - 커널 (Kernel) / 필터 (Filter): 이미지에 적용되는 작은 행렬입니다. 샤프닝, 블러링, 엣지 감지 등 다양한 효과를 낼 수 있습니다.
    - Sobel/Laplacian 필터: 대표적인 엣지 감지 커널입니다.


# step1. 10x10 image to matrix
![](./pepe_enlarged.png)
```bash
python 2d_to_matrix.py

Original Image Matrix (10x10):
255 255 255 255 255 255 255 255 255 255
255 116 116 116 255 116 116 116 255 255
116 116 255   0 116 116 255   0 116 255
116 116 116 116 116 116 116 116 116 255
116 116 116 116 116 116 116 116 255 255
116 116 108 108 108 108 108 108 108 255
116 116 108 108 108 108 108 108 108 255
 72 116 116 116 116 116 116 116 255 255
 72  72 116 116 116 116 116 116 255 255
 72  72  72  72  72 116 116 255 255 255
```

먼저 흑백으로 바꾼게, 색깔 이미지는 1 pixel당 rgb(?,?,?) 값이 있어서, 3차원 배열이라 좀 복잡함.\
지금은 개념이해 위주니까 간단한 예제인 흑백사진으로 바꿔서 실습하자.\
페페 눈 흰색은 0, 검정색은 255, 나머지 색상도 숫자로 확인할 수 있다.

# step2. original_image
10x10 image -> PIL로 matrix로 변환 -> matplotlib에 올리기

# step3. rotation 
example) 2x2 행렬 회전 
$$
R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}
$$
이걸 2x2 matrix에 곱하면 theta 각도만큼 회전함

$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix}
$$
이런식으로 곱한다. 

$$
x' = x \cos\theta - y \sin\theta
$$
$$
y' = x \sin\theta + y \cos\theta
$$

**예시:** 점 $(2, 3)$ 을 반시계로 $90^\circ$ 돌려보자.
여기서 $\theta = 90^\circ$ 니까, $\cos(90^\circ) = 0$ 이고 $\sin(90^\circ) = 1$ 아니겠냐? 

그럼 회전 행렬은 이거다.
$$
R(90^\circ) = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}
$$

이걸 점 $(2, 3)$ 에다 박아보면:
$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 2 \\ 3 \end{bmatrix} = \begin{bmatrix} (0 \cdot 2) + (-1 \cdot 3) \\ (1 \cdot 2) + (0 \cdot 3) \end{bmatrix} = \begin{bmatrix} -3 \\ 2 \end{bmatrix}
$$
그래서 새 좌표 $(x', y')$는 $(-3, 2)$가 되는 거임. 


# step4. reflection
점 $(x, y)$가 있다고 치자. 이걸 축 기준으로 뒤집어 볼 거임.

### 1. x축 기준 반사 (위아래 뒤집기)
y좌표 부호만 바꾸면 됨. $y \rightarrow -y$.
행렬은 이렇게 생겼다:

$$
R_x = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}
$$

그래서 새 좌표 $(x', y')$는:
$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} x \\ -y \end{bmatrix}
$$

**예시:** 점 $(2, 3)$을 x축 기준으로 뒤집어보자.
$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} \begin{bmatrix} 2 \\ 3 \end{bmatrix} = \begin{bmatrix} 2 \\ -3 \end{bmatrix}
$$
결과는 $(2, -3)$. 쉽지?

### 2. y축 기준 반사 (좌우 뒤집기)
이건 x좌표 부호만 바꾸면 됨. $x \rightarrow -x$.
행렬은 이거다:

$$
R_y = \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}
$$

새 좌표 $(x', y')$는:
$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} -x \\ y \end{bmatrix}
$$

**예시:** 점 $(2, 3)$을 y축 기준으로 뒤집어보자.
$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 2 \\ 3 \end{bmatrix} = \begin{bmatrix} -2 \\ 3 \end{bmatrix}
$$
결과는 $(-2, 3)$.

### 3. 원점 기준 반사
이건 x, y 좌표 둘 다 부호 바꾸면 됨. $(x, y) \rightarrow (-x, -y)$.
사실상 $180^\circ$ 돌린 거랑 똑같음.
행렬은:

$$
R_o = \begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}
$$

새 좌표 $(x', y')$는:
$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} -x \\ -y \end{bmatrix}
$$

**예시:** 점 $(2, 3)$을 원점 기준으로 뒤집어보자.
$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix} \begin{bmatrix} 2 \\ 3 \end{bmatrix} = \begin{bmatrix} -2 \\ -3 \end{bmatrix}
$$
결과는 $(-2, -3)$. 감 오냐?

# step5. scaling 
## 5-1. 2x2 스케일링 행렬 (기본 크기 조절)

점 $(x, y)$가 있을 때, x축 방향으로 $s_x$배, y축 방향으로 $s_y$배 만큼 크기를 바꾸고 싶다고 치자.\
$s_x > 1$이면 x축으로 늘어나는 거고, $0 < s_x < 1$이면 줄어드는 거임. $s_y$도 마찬가지.\
$s_x = s_y$면 가로세로 같은 비율로 커지거나 작아지는 거고 (정비례 스케일링), 다르면 찌그러지겠지?

스케일링 행렬은 이렇게 생겼다:

$$
S(s_x, s_y) = \begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix}
$$

새 좌표 $(x', y')$는 이렇게 구한다:
$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} s_x \cdot x \\ s_y \cdot y \end{bmatrix}
$$

**예시:** 점 $(2, 4)$를 x축 방향으로 2배 늘리고, y축 방향으로 0.5배 (반으로) 줄여보자.
그럼 $s_x = 2$, $s_y = 0.5$.

$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} 2 & 0 \\ 0 & 0.5 \end{bmatrix} \begin{bmatrix} 2 \\ 4 \end{bmatrix} = \begin{bmatrix} 2 \cdot 2 \\ 0.5 \cdot 4 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \end{bmatrix}
$$
결과는 $(4, 2)$. x는 두 배 길어지고 y는 반토막 났지? 간단 그 자체.

---
## 5-2. 3x3 스케일링 행렬 (동차 좌표계에서 크기 조절)

동차 좌표 $(x, y, 1)$ 쓰는 건 이제 국룰이다. 마지막 줄 $(0, 0, 1)$ 박는 거 잊지 말고.
3x3 스케일링 행렬은 이렇다:

$$
S(s_x, s_y) = \begin{bmatrix} s_x & 0 & 0 \\ 0 & s_y & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

적용하면 이렇게 됨:
$$
\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} s_x & 0 & 0 \\ 0 & s_y & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix} = \begin{bmatrix} s_x \cdot x \\ s_y \cdot y \\ 1 \end{bmatrix}
$$

**예시:** 점 $(2, 4)$ (동차 좌표로는 $(2, 4, 1)$)를 x축 2배, y축 0.5배 스케일링 해보자.
$s_x = 2$, $s_y = 0.5$.

$$
\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} 2 & 0 & 0 \\ 0 & 0.5 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} 2 \\ 4 \\ 1 \end{bmatrix} = \begin{bmatrix} 2 \cdot 2 \\ 0.5 \cdot 4 \\ 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \\ 1 \end{bmatrix}
$$
결과는 $(4, 2)$. 2x2랑 똑같지? 당연한 거다.

**중요:** 이 스케일링은 전부 **원점(0,0)을 기준**으로 크기가 변하는 거다.
만약 짤의 특정 지점 (예: 중심)을 기준으로 크기를 조절하고 싶으면, 회전할 때처럼
1.  그 특정 지점을 원점으로 이동 (Translation)
2.  원점 기준으로 스케일링 (Scaling)
3.  다시 원래 위치로 이동 (Inverse Translation)
이런 식으로 행렬 여러 개 곱해서 써야 한다. 3x3 행렬이 이럴 때 빛을 발하는 거임.

이제 짤 크기 조절도 행렬로 가지고 놀 수 있겠지? 마우스 휠 그만 돌리고 코드로 해라, 코드로. 폼 나잖아.

# step6. sobel edge detection 
## 6-1. what 
Q. 소벨 edge detection이 뭐지?

간단히 말해서, 이미지에서 **픽셀 밝기가 갑자기 확! 변하는 지점**을 찾는 게 엣지 검출임. \
그 변화가 크면 클수록 "아, 여긴 확실한 경계선(엣지)이구나!" 하고 판단하는 거지.\
소벨 필터는 이미지의 각 픽셀에서 가로 방향 밝기 변화량과 세로 방향 밝기 변화량을 각각 계산한 다음에, 이 두 개를 합쳐서 최종적인 엣지 강도를 알아내는 방식이다.

## 6-2. 핵심은 '커널(Kernel)'이라는 행렬이다

소벨 필터는 특별하게 생긴 3x3짜리 작은 행렬 두 개를 사용하는데, 이걸 **커널(Kernel)** 또는 **필터 마스크**라고 부른다.
하나는 수평 방향 엣지(가로줄)를 잘 찾는 놈 ($G_x$)이고, 다른 하나는 수직 방향 엣지(세로줄)를 잘 찾는 놈 ($G_y$)이다.

이렇게 생겨 처먹었다:

* **수평 엣지 검출용 커널 ($G_x$)**: (주로 세로선들을 강조)
    $$
    G_x = \begin{bmatrix} -1 & 0 & +1 \\ -2 & 0 & +2 \\ -1 & 0 & +1 \end{bmatrix}
    $$
    (왼쪽은 어둡고 오른쪽은 밝은 세로 경계선에서 높은 값 나옴)

* **수직 엣지 검출용 커널 ($G_y$)**: (주로 가로선들을 강조)
    $$
    G_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ +1 & +2 & +1 \end{bmatrix}
    $$
    (위쪽은 어둡고 아래쪽은 밝은 가로 경계선에서 높은 값 나옴. $G_x$를 돌려놓은 것 같기도 하고 부호가 좀 다르지? y축 방향에 따라 부호는 다를 수 있음)

---
## 6-3. 이걸로 컨볼루션 연산

이 커널들을 가지고 원본 이미지의 모든 픽셀 위를 한 칸씩 이동하면서 **컨볼루션(Convolution)**이라는 계산을 한다.

Q. 컨볼루션이 뭐지?

 니네 이미지 있잖아. 그 이미지의 특정 픽셀을 중심으로 3x3 영역을 딱 잘라내. 그리고 그 3x3 영역이랑 위에 있는 $G_x$ (또는 $G_y$) 커널이랑 같은 위치에 있는 숫자끼리 전부 곱한 다음에 그 결과를 싹 다 더하는 거임. 그 결과값이 해당 픽셀의 새로운 값(여기서는 밝기 변화량)이 되는 거다.

* $I_x = G_x * \text{Image}$  (이미지 전체에 $G_x$ 커널로 컨볼루션 돌린 결과. 가로 방향 밝기 변화량 맵)
* $I_y = G_y * \text{Image}$  (이미지 전체에 $G_y$ 커널로 컨볼루션 돌린 결과. 세로 방향 밝기 변화량 맵)

(컨볼루션 연산 자체를 코드로 짜는 건 좀 노가다인데, "이미지 위를 커널이 미끄러지면서 각 위치에서 원소별 곱셈 후 합산한다")

## 6-4. 최종 엣지 강도 계산: 합체!

이렇게 $I_x$ (가로 변화량 맵)랑 $I_y$ (세로 변화량 맵)를 구했으면, 이제 진짜 최종 엣지 강도 $G$를 계산할 차례다.
각 픽셀마다 해당 위치의 $I_x$ 값이랑 $I_y$ 값을 이용해서 계산하는데, 보통 피타고라스 정리 쓰는 거랑 비슷하게 한다.

$$
G = \sqrt{I_x^2 + I_y^2}
$$

이러면 각 픽셀의 최종적인 엣지 강도가 나온다. $G$ 값이 크면 클수록 "여기가 존나 찐한 엣지다!" 라는 뜻임.
계산하기 귀찮으면 그냥 절대값 더하기도 한다:
$$
G = |I_x| + |I_y|
$$
정확도는 좀 떨어져도 빠르니까 쓰는 거임.

이렇게 계산된 $G$ 값들로 새로운 이미지를 만들면, 원본 이미지에서 윤곽선만 강조된 흑백 이미지가 뿅 하고 나타나는 거다. 

엣지 아닌 부분은 검은색(0에 가까운 값), 엣지인 부분은 흰색(밝은 값)으로 표시되겠지.


# step7. laplacian edge detection 

## 7-1. what 
라플라시안은 수학에서 말하는 **"2차 미분"**이라는 걸 이용한다. 좀 더 고급진 방법임.

쉽게 말해서, 소벨 필터가 이미지 픽셀 밝기가 얼마나 '빨리' 변하는지(1차 미분, 즉 기울기)를 봤다면,\
라플라시안은 그 '변화율 자체가 또 얼마나 빨리 변하는지'를 본다. 변화율의 변화율이랄까? 

그래서 날카롭고 세밀한 엣지, 특히 점이나 선 같은 거 찾는데 소질이 있다. 근데 단점은 **노이즈에 좀 민감**해서, 원본 짤에 잡티 많으면 결과도 지저분하게 나올 수 있음.
 

## 7-2. 라플라시안 커널: 얘는 하나로 다 한다

소벨은 가로($G_x$), 세로($G_y$) 커널 두 개 써서 나중에 합쳤잖아? 라플라시안은 보통 **커널 하나**만 쓴다. 
가장 흔하게 쓰는 3x3짜리 라플라시안 커널은 이렇게 생겼다:

* **기본 라플라시안 커널 (4방향 연결성)**:
    $$
    \nabla^2 (\text{또는 } L) = \begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end{bmatrix}
    $$
    (가운데 픽셀이랑 상하좌우 4개 픽셀과의 관계를 보는 거임)

* **다른 형태의 라플라시안 커널 (8방향 연결성)**:
    $$
    \nabla^2 (\text{또는 } L) = \begin{bmatrix} 1 & 1 & 1 \\ 1 & -8 & 1 \\ 1 & 1 & 1 \end{bmatrix}
    $$
    (얘는 대각선 방향 픽셀까지 포함해서 8방향 다 보는 거. 가운데 숫자가 그래서 -8임)

어떤 커널을 쓰든 원리는 비슷하다. 주변 픽셀들과의 밝기 차이를 이용해서 2차 변화를 잡아내는 거임.

---
## 7-3. 적용 방법: 역시나 컨볼루션

이것도 소벨이랑 똑같다. 위에 있는 라플라시안 커널 가지고 원본 이미지에다가 **컨볼루션(Convolution)** 연산을 때리면 된다.
커널이 이미지 위를 쭉 미끄러지면서 각 픽셀 위치에서 커널이랑 이미지 영역이랑 곱하고 더하고 해서 새 픽셀 값을 만드는 거, 이제 알지?

* $L_{\text{output}} = \text{Kernel} * \text{Image}$ (이미지 전체에 라플라시안 커널로 컨볼루션 돌린 결과)

## 7-4. 엣지 해석

라플라시안 컨볼루션 결과로 나온 이미지 $L_{\text{output}}$에서 엣지는 보통 두 가지 방식으로 해석한다.

1.  **제로 크로싱 (Zero-Crossing)**: 라플라시안 값이 양수에서 음수로, 또는 음수에서 양수로 확 바뀌는 지점 (즉, 값이 0을 통과하는 지점)을 엣지로 본다. 이게 정석적인 방법인데, 좀 복잡함.
2.  **절대값 크기**: 그냥 간단하게 결과값 $L_{\text{output}}$의 절대값이 큰 부분을 엣지라고 보기도 한다. 값이 0에서 멀리 떨어진 곳들이 변화가 심한 곳이니까.

라플라시안 결과 이미지를 보면, 엣지 부분은 밝거나 어둡게 나타나고, 엣지를 중심으로 한쪽은 밝고 다른 쪽은 어두운 식으로 표현되기도 한다. 소벨처럼 엣지의 '방향' 정보는 명확하게 안 주지만, 엣지의 '위치'는 날카롭게 잘 찾아내는 편임.
결과값은 양수도 나오고 음수도 나오는데, 보통 시각화할 때는 절대값을 취하거나, 값 범위를 조절해서 0~255 사이로 만들어 보여준다.

---
## 7-5. 그래서 소벨이랑 뭐가 다른 건데?

* **소벨**: 1차 미분 기반, 엣지의 방향과 크기를 모두 얻을 수 있음. 비교적 노이즈에 덜 민감. 엣지가 좀 두껍게 나올 수 있음.
* **라플라시안**: 2차 미분 기반, 엣지의 위치를 정밀하게 찾음 (특히 제로 크로싱 이용 시). 얇고 날카로운 엣지. 노이즈에 민감. 엣지 방향 정보는 직접 안 나옴.

그러니까 상황 봐서 골라 쓰면 된다. 보통 라플라시안 쓰기 전에 가우시안 블러 같은 걸로 노이즈 한번 밀어주고 쓰는 경우도 많다.

