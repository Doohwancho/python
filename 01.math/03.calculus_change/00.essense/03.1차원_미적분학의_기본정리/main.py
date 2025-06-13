import numpy as np
import matplotlib.pyplot as plt

# 1. 함수 정의
# F(x) = 0.1*x^3 - 0.5*x^2 + 2x + 5
# F'(x) = f(x) = 0.3*x^2 - 1.0*x + 2
def F(x):
    return 0.1*x**3 - 0.5*x**2 + 2*x + 5

def f(x):
    return 0.3*x**2 - 1.0*x + 2

# 2. 데이터 생성
x = np.linspace(0, 10, 400)
y_F = F(x)
y_f = f(x)
a, b = 2, 8

# 3. 시각화 (두 개의 플롯을 위아래로 생성, x축 공유)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), sharex=True)
fig.suptitle("The Essence of the Fundamental Theorem of Calculus", fontsize=18)

# --- 상단 플롯: 원함수 F(x) ---
ax1.plot(x, y_F, 'r-', label='Original Function $F(x)$ (Position)')
ax1.set_title("Total Change in Original Function")
ax1.set_ylabel("$F(x)$")
ax1.grid(True)

# F(a)와 F(b) 지점 표시
ax1.plot(a, F(a), 'ro')
ax1.plot(b, F(b), 'ro')
ax1.text(a, F(a) + 1, f'$F(a)={F(a):.1f}$', horizontalalignment='center')
ax1.text(b, F(b) + 1, f'$F(b)={F(b):.1f}$', horizontalalignment='center')

# F(b) - F(a) 변화량 시각화
ax1.plot([a, b], [F(b), F(b)], 'k--')
ax1.plot([a, a], [F(a), F(b)], 'k--')
change_value = F(b) - F(a)
ax1.text(a + 0.2, (F(a)+F(b))/2, f"Total Change\n$F(b) - F(a) \simeq {change_value:.2f}$", 
         color='blue', fontsize=12, verticalalignment='center')
ax1.legend()


# --- 하단 플롯: 도함수 f(x) ---
ax2.plot(x, y_f, 'b-', label="Derivative $f(x) = F'(x)$ (Velocity)")
ax2.set_title("Area under Derivative (Sum of Instantaneous Changes)")
ax2.set_xlabel("x")
ax2.set_ylabel("$f(x)$")
ax2.grid(True)

# 구간 [a, b]의 면적 채우기
ix = np.linspace(a, b)
iy = f(ix)
ax2.fill_between(ix, iy, color='lightgray', label=f"Area = $\int_{a}^{b} f(x)dx$")

# 면적 값 텍스트로 추가
integral_value = change_value # 이론적으로 두 값은 같음
ax2.text((a+b)/2, 0.5, f"Area = $\int_{{{a}}}^{{{b}}} f(x)dx \simeq {integral_value:.2f}$",
         color='blue', fontsize=12, horizontalalignment='center')
ax2.legend()

# 레이아웃 조정
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()