import numpy as np
import matplotlib.pyplot as plt

# 1. 시간 데이터 생성
t = np.linspace(0, 10, 500)
a, b = 3, 9  # 적분 및 변화량을 확인할 구간 설정

# 2. 새로운 '등가속도' 시나리오에 따른 함수 정의
def position_func(t):
    # s(t) = t^2 (포물선 운동)
    return t**2

def velocity_func(t):
    # v(t) = 2t (선형 증가)
    return 2 * t

def acceleration_func(t):
    # a(t) = 2 (상수)
    return np.full_like(t, 2) # t와 동일한 크기의 배열을 2로 채움

position = position_func(t)
velocity = velocity_func(t)
acceleration = acceleration_func(t)

# 3. 시각화 (두 개의 플롯을 위아래로 생성, x축 공유)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
fig.suptitle("Constant Acceleration and the Fundamental Theorem of Calculus", fontsize=18)

# --- 상단 플롯: 위치 s(t) (원함수) ---
ax1.plot(t, position, 'b-', linewidth=2.5, label=r'Position $s(t) = t^2$')
ax1.set_title("Original Function: Total Change in Position", fontsize=14)
ax1.set_ylabel("Position (meters)", fontsize=12)
ax1.grid(True)

# s(a)와 s(b) 지점 표시
s_a = position_func(a)
s_b = position_func(b)
ax1.plot([a, b], [s_a, s_b], 'bo', markersize=8)
ax1.text(a, s_a - 10, f's({a})={s_a:.1f}', horizontalalignment='center')
ax1.text(b, s_b + 5, f's({b})={s_b:.1f}', horizontalalignment='center')

# s(b) - s(a) 총 변화량 시각화
ax1.plot([b, b], [s_a, s_b], 'k--', alpha=0.7)
ax1.plot([a, b], [s_a, s_a], 'k--', alpha=0.7)
change_value = s_b - s_a
ax1.text(a + 0.2, s_a + change_value/2, f"Total Change\n$s({b}) - s({a}) = {change_value:.1f}$",
         color='blue', fontsize=12, verticalalignment='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# 함수 수식 텍스트 추가
ax1.text(1, 40, r'$s(t) = t^2$', fontsize=14, color='blue', alpha=0.9)


# --- 하단 플롯: 속도 v(t) (도함수)와 가속도 a(t) ---
ax2.plot(t, velocity, 'r--', linewidth=2, label=r'Velocity $v(t) = 2t$')
ax2.plot(t, acceleration, 'g:', linewidth=3, label=r'Acceleration $a(t) = 2$') # 가속도 선을 더 두껍게
ax2.set_title("Derivative: Area under Velocity Curve", fontsize=14)
ax2.set_xlabel("Time (t)", fontsize=12)
ax2.set_ylabel("Velocity / Acceleration", fontsize=12)
ax2.grid(True)

# 속도 그래프 아래 구간 [a, b]의 면적 채우기 (사다리꼴 넓이)
ix = np.linspace(a, b)
iy = velocity_func(ix)
ax2.fill_between(ix, iy, color='lightgray', label=f'Area under v(t) from t={a} to t={b}')

# 면적(적분값) 텍스트로 추가
integral_value = change_value  # FTC에 의해 두 값은 정확히 같음
ax2.text((a+b)/2, 2, f"Area = $\int_{{{a}}}^{{{b}}} v(t)dt = {integral_value:.1f}$",
         color='red', fontsize=12, horizontalalignment='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# 함수 수식 텍스트 추가
ax2.text(1, 15, r'$v(t) = 2t$', fontsize=14, color='red', alpha=0.9)
ax2.text(1, 3.5, r'$a(t) = 2$', fontsize=14, color='green', alpha=0.9)

# 범례 통합 표시
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=10)

# 레이아웃 조정
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()