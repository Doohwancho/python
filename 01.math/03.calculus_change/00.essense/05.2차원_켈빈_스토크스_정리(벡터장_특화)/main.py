import numpy as np
import matplotlib.pyplot as plt

# 1. 3D 시각화 설정
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection='3d')

# 2. 열린 곡면(포물면) 정의: z = x^2 + y^2
u = np.linspace(0, 1, 30)
v = np.linspace(0, 2 * np.pi, 30)
U, V = np.meshgrid(u, v)
X = U * np.cos(V)
Y = U * np.sin(V)
Z = U**2

# 곡면 그리기
ax.plot_surface(X, Y, Z, alpha=0.3, color='cyan', rstride=1, cstride=1)

# 3. 경계선(원) 정의: z=1 평면 위의 반지름 1인 원
ax.plot(np.cos(v), np.sin(v), 1, 'r-', linewidth=3, label='Boundary Path C')

# 4. 벡터 필드 정의 F = <-y, x, 0>
x_q = np.arange(-1, 1.1, 0.5)
y_q = np.arange(-1, 1.1, 0.5)
z_q = np.arange(0, 1.1, 0.5)
X_q, Y_q, Z_q = np.meshgrid(x_q, y_q, z_q)
P_q = -Y_q
Q_q = X_q
R_q = np.zeros_like(Z_q)

# 벡터 필드 그리기
ax.quiver(X_q, Y_q, Z_q, P_q, Q_q, R_q, length=0.2, normalize=True, color='gray', alpha=0.7)

# 5. 그래프 설정
ax.set_title("Stokes' Theorem", fontsize=16)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.view_init(elev=30, azim=-45)
ax.legend()
plt.show()