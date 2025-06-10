import numpy as np
import matplotlib.pyplot as plt

# 1. 데이터 준비 (완벽한 직선 위에 있지 않은 점들)
x_data = np.array([0, 1, 2, 3])
y_data = np.array([1, 2.5, 2.9, 4.2])

# 2. 행렬 A와 벡터 b 구성
# A의 첫 번째 열은 y절편 c를 위해 모두 1, 두 번째 열은 기울기 m을 위해 x 데이터
A = np.vstack([np.ones(len(x_data)), x_data]).T
b = y_data

print("Matrix A:\n", A)
print("\nVector b:\n", b)

# 3. 최적의 근사해 x̂ 구하기 (정규방정식 사용)
# A^T * A * x_hat = A^T * b  ==>  x_hat = (A^T * A)^-1 * A^T * b
A_T = A.T
ATA = A_T @ A
ATb = A_T @ b

x_hat = np.linalg.inv(ATA) @ ATb

# Numpy의 내장 함수를 사용하면 더 간단합니다.
# x_hat, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

c_hat, m_hat = x_hat
print(f"\n최적의 근사해 (x̂):")
print(f"y-intercept (c) = {c_hat:.4f}")
print(f"slope (m) = {m_hat:.4f}")
print(f"결과 직선: y = {c_hat:.4f} + {m_hat:.4f}x")

# 4. 결과 시각화
plt.figure(figsize=(8, 6))
# 원본 데이터 점들
plt.scatter(x_data, y_data, color='blue', label='Original Data Points')
# 최적의 근사 직선
plt.plot(x_data, c_hat + m_hat * x_data, color='red', label='Best-Fit Line (Least Squares)')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Least Squares Linear Regression')
plt.legend()
plt.grid(True)
plt.show()