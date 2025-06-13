import numpy as np
import matplotlib.pyplot as plt

# 1. 벡터 필드 정의 F = <P, Q> = <-y, x>
x, y = np.meshgrid(np.linspace(-2, 2, 20), np.linspace(-2, 2, 20))
P = -y
Q = x

# 2. 닫힌 경로(원) 정의
theta = np.linspace(0, 2 * np.pi, 100)
r = 1.5 # 반지름
path_x = r * np.cos(theta)
path_y = r * np.sin(theta)

# 3. 시각화
plt.figure(figsize=(8, 8))
# 벡터 필드 그리기
plt.quiver(x, y, P, Q, color='gray', alpha=0.7, label='Vector Field F = <-y, x>')
# 닫힌 경로 그리기
plt.plot(path_x, path_y, 'r-', linewidth=2, label='Closed Path C')

# 4. 그래프 설정
plt.title("Green's Theorem", fontsize=16)
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc='upper right')
plt.axis('equal')
plt.grid(True)
plt.show()