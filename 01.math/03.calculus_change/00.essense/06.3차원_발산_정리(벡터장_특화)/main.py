import numpy as np
import matplotlib.pyplot as plt

# 1. 3D 시각화 설정
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection='3d')

# 2. 닫힌 곡면(구) 정의
phi = np.linspace(0, np.pi, 20)
theta = np.linspace(0, 2 * np.pi, 20)
PHI, THETA = np.meshgrid(phi, theta)
r = 1.0
X_s = r * np.sin(PHI) * np.cos(THETA)
Y_s = r * np.sin(PHI) * np.sin(THETA)
Z_s = r * np.cos(PHI)

# 구 그리기
ax.plot_surface(X_s, Y_s, Z_s, alpha=0.2, color='orange', rstride=1, cstride=1)

# 3. 벡터 필드 정의 F = <x, y, z>
x_q = np.arange(-1.2, 1.3, 0.6)
y_q = np.arange(-1.2, 1.3, 0.6)
z_q = np.arange(-1.2, 1.3, 0.6)
X_q, Y_q, Z_q = np.meshgrid(x_q, y_q, z_q)

# 벡터 필드 그리기
ax.quiver(X_q, Y_q, Z_q, X_q, Y_q, Z_q, length=0.2, normalize=True, color='gray')

# 4. 그래프 설정
ax.set_title("Divergence (Gauss's) Theorem", fontsize=16)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_box_aspect([1,1,1]) # 정육면체 비율
plt.show()