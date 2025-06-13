import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**2

x_val = 1
h_values = [2, 1, 0.5, 0.1] # h값을 점점 줄여나감

# 2x2 서브플롯 생성
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("The Secant Line Approaching the Tangent Line", fontsize=16)
axes = axes.flatten() # 2x2 배열을 1차원 배열로 만듦

# 메인 함수 그래프 데이터
x_range = np.linspace(-1, 4, 400)
y_range = f(x_range)

for i, h in enumerate(h_values):
    ax = axes[i]
    
    # 1. 함수 그래프 그리기
    # 올바른 LaTeX 문법으로 수정
    ax.plot(x_range, y_range, 'b-', label=r'$f(x)=x^2$')
    
    # 2. 두 점 p1, p2 정의
    p1 = (x_val, f(x_val))
    p2 = (x_val + h, f(x_val + h))
    
    # 3. 할선(secant line) 그리기
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r--')
    ax.plot(p1[0], p1[1], 'yo', markersize=8)
    ax.plot(p2[0], p2[1], 'yo', markersize=8)
    
    # 4. 기울기 계산 및 텍스트 추가
    slope = (p2[1] - p1[1]) / h
    ax.set_title(f'h = {h}, Slope ≈ {slope:.2f}', fontsize=12)
    
    # 5. 그래프 설정
    ax.grid(True)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()

# 최종 접선(h->0)을 마지막 그래프에 추가
ax = axes[-1]
tangent_slope = 2 * x_val # f'(x)=2x 이므로 f'(1)=2
x_tangent = np.array([x_val - 1, x_val + 1])
y_tangent = tangent_slope * (x_tangent - x_val) + f(x_val)
# 올바른 LaTeX 문법으로 수정
ax.plot(x_tangent, y_tangent, 'g-', linewidth=2, label=f"Tangent Line (m={tangent_slope})")
ax.legend()
    
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()