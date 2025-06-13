## 그래디언트(Gradient): 모든 방향의 경사 정보를 담은 '나침반'

> **그래디언트($\nabla L$)** 는 흩어져 있던 모든 편미분 값(쪽지 정보)들을 모아 하나의 **벡터(화살표)** 로 만든 것입니다.

$$
\nabla L = \begin{pmatrix} \frac{\partial L}{\partial w_1} \\ \frac{\partial L}{\partial w_2} \\ \vdots \\ \frac{\partial L}{\partial w_n} \end{pmatrix} = \begin{pmatrix} +3 \\ -5 \\ \vdots \\ +1 \end{pmatrix}
$$

이 그래디언트 벡터는 아주 특별하고 마법 같은 속성을 가지고 있습니다.

> **그래디언트 벡터($\nabla L$)는 현재 위치에서 손실(Loss)이 가장 가파르게 증가하는 방향(the direction of steepest ascent)을 가리킨다.**

즉, 이 벡터는 "이쪽 방향으로 가야 가장 가파른 오르막길이야!" 라고 알려주는 **완벽한 나침반**인 셈입니다.
