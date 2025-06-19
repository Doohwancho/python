### 4. 기댓값 (Expected Value, $E(X)$)

기댓값은 확률변수의 모든 가능한 값들을 확률(또는 확률밀도)로 가중평균한 값입니다. 해당 확률분포의 "무게중심" 또는 "장기적인 평균"을 의미합니다. 말씀하신 "integral of probability distribution of random variable"은 정확히 연속확률변수의 기댓값 정의입니다.

* **이산확률변수**:
    $$E(X) = \mu_X = \sum_x x \cdot p(x)$$

* **연속확률변수**:
    $$E(X) = \mu_X = \int_{-\infty}^{\infty} x \cdot f(x) dx$$
