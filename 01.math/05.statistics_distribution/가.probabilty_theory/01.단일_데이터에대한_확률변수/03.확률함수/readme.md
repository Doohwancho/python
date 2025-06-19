### 3. 확률 함수 (Probability Functions): $f(x)$와 $F(x)$

확률변수가 특정 값을 가질 확률을 어떻게 표현할지를 나타내는 함수입니다.

#### 3.1. 확률질량/밀도함수 ($f(x)$)

* **확률질량함수 (Probability Mass Function, PMF)**: **이산확률변수**에 사용됩니다. 확률변수 $X$가 정확히 특정 값 $x$를 가질 확률을 나타냅니다.
    * 표기: $p(x) = P(X=x)$
    * 특징:
        1.  모든 $x$에 대해 $0 \le p(x) \le 1$
        2.  모든 가능한 $x$에 대한 확률의 총합은 1입니다: $\sum_x p(x) = 1$

* **확률밀도함수 (Probability Density Function, PDF)**: **연속확률변수**에 사용됩니다. PDF의 값 자체가 확률은 아니며, 특정 구간의 **넓이**가 해당 구간에 변수가 포함될 확률을 나타냅니다. (연속변수는 한 점에서의 확률이 0이므로).
    * 표기: $f(x)$
    * 특징:
        1.  모든 $x$에 대해 $f(x) \ge 0$
        2.  $f(x)$ 곡선 아래의 전체 면적은 1입니다: $\int_{-\infty}^{\infty} f(x) dx = 1$
        3.  $P(a \le X \le b) = \int_a^b f(x) dx$

#### 3.2. 누적분포함수 (Cumulative Distribution Function, CDF)

누적분포함수 $F(x)$는 확률변수 $X$가 특정 값 $x$보다 작거나 같을 확률을 나타냅니다. 이산형과 연속형 모두에 사용되는 통합적인 개념입니다.

* 표기: $F(x) = P(X \le x)$
* **이산형**의 경우: $F(x) = \sum_{t \le x} p(t)$
* **연속형**의 경우: $F(x) = \int_{-\infty}^{x} f(t) dt$
* CDF와 PDF의 관계 (연속형): $f(x) = \frac{dF(x)}{dx}$ (CDF를 미분하면 PDF가 됩니다)
