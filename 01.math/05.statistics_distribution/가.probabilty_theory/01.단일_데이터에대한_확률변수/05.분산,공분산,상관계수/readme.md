### 5. 분산, 공분산, 상관계수

#### 5.1. 분산 (Variance, $\text{Var}(X)$)

분산은 확률변수가 기댓값으로부터 얼마나 퍼져있는지를 나타내는 척도입니다. 편차 제곱의 기댓값으로 계산합니다.

* 정의:
    $$\text{Var}(X) = \sigma^2_X = E[(X - E(X))^2] = E[(X - \mu_X)^2]$$
* 계산에 유용한 공식:
    $$\text{Var}(X) = E(X^2) - [E(X)]^2$$
* **표준편차 (Standard Deviation)**: 분산에 제곱근을 취한 값으로, 원래 데이터와 단위가 같아 해석이 용이합니다. $\sigma_X = \sqrt{\text{Var}(X)}$

#### 5.2. 공분산 (Covariance, $\text{Cov}(X,Y)$)

**두 확률변수** $X$와 $Y$가 함께 어떻게 변하는지를 측정하는 척도입니다. 여기서부터 두 변수 간의 관계를 다루기 시작합니다.

* 정의:
    $$\text{Cov}(X, Y) = E[(X - E(X))(Y - E(Y))]$$
* 계산에 유용한 공식:
    $$\text{Cov}(X, Y) = E(XY) - E(X)E(Y)$$
* 해석:
    * $\text{Cov}(X,Y) > 0$: $X$가 증가할 때 $Y$도 증가하는 경향 (양의 관계)
    * $\text{Cov}(X,Y) < 0$: $X$가 증가할 때 $Y$는 감소하는 경향 (음의 관계)
    * $\text{Cov}(X,Y) \approx 0$: 선형 관계가 거의 없음

#### 5.3. 상관계수 (Correlation, $\text{Corr}(X,Y)$)

공분산은 변수의 단위에 따라 값이 크게 달라지므로, 관계의 '강도'를 직접적으로 비교하기 어렵습니다. 상관계수는 공분산을 각 변수의 표준편차로 나누어 정규화(standardize)한 값입니다.

* 정의:
    $$\rho_{XY} = \text{Corr}(X,Y) = \frac{\text{Cov}(X,Y)}{\sqrt{\text{Var}(X)}\sqrt{\text{Var}(Y)}} = \frac{\text{Cov}(X,Y)}{\sigma_X \sigma_Y}$$
* 특징:
    * 항상 $-1 \le \rho_{XY} \le 1$ 사이의 값을 가집니다.
    * $\rho_{XY} = 1$: 완벽한 양의 선형 관계
    * $\rho_{XY} = -1$: 완벽한 음의 선형 관계
    * $\rho_{XY} = 0$: 선형 관계 없음
