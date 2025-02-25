import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(project_root)

from optimizer import Optimizer
from gradient_descent import GradientDescent
from linear_algebra.ndarray import NDArray


def test_gradient_descent():
    # 테스트할 함수: f(x) = x² + 2x + 1
    # 최소값은 x = -1에서 발생
    def quadratic(x: NDArray) -> float:
        return x[0]**2 + 2*x[0] + 1 # f'(x) = 2x + 2 -> x값이 -1일 때 derivative 값이 0 -> 이 함수의 최솟값은 -1

    # GradientDescent 객체 생성
    optimizer = GradientDescent(
        learning_rate=0.1,
        tolerance=1e-6, # gradient_descent로 조금씩 이동하는데, 이전이랑 이동한거의 차이가 엄~청 미세하면 중단하기.  
        max_iterations=1000
    )

    # 시작점
    initial_x = NDArray([2.0])  # x = 2에서 시작

    # 최적화 실행
    optimal_x, history = optimizer.minimize(quadratic, initial_x)

    # 결과 출력
    print(f"시작점: x = {initial_x[0]}")
    print(f"찾은 최소점: x = {optimal_x[0]}")
    print(f"실제 최소점: x = -1")
    print(f"반복 횟수: {len(history) - 1}")
    print(f"최종 함수값: {history[-1]}")
    print("\n최적화 과정:")
    for i, value in enumerate(history):
        print(f"Iteration {i}: f(x) = {value}") # 점점 값이 1.몇 * e-06으로 가는데, 이건 10^(-6)으로 매우 작은 값이라는 뜻. 
                                                # 결국 

    # 검증
    assert abs(optimal_x[0] + 1) < 0.01, "최소점이 -1에 충분히 가깝지 않습니다"
    assert history[-1] < 1.0, "최소값이 1보다 작아야 합니다"

def test_gradient_descent_concave_up():
    # 위로 볼록 테스트 (maximum 찾기)
    def concave_up(x: NDArray) -> float:
        return -(x[0]**2) + 2*x[0] + 1  # 최대값: x = 1, f'(x) = -2x+2, x=1일 때, derivative가 0
    
    optimizer = GradientDescent(learning_rate=0.1)

    # 위로 볼록 테스트
    print("\n위로 볼록 함수 테스트 (최대값 찾기):")
    # 최대값 찾기는 함수에 -1 곱해서 최소값 찾기로 변환
    x, history = optimizer.minimize(lambda x: -concave_up(x), NDArray([0.0]))
    print(f"Found x = {x[0]}, f'(x) = {concave_up(x)}")
    print(f"Expected x = 1, where f'(x) = 0")

def test_multiple_starting_points():
    """여러 시작점에서 테스트"""
    def quadratic(x: NDArray) -> float:
        return x[0]**2 + 2*x[0] + 1

    starting_points = [-5.0, -2.0, 0.0, 2.0, 5.0]
    optimizer = GradientDescent(learning_rate=0.1)

    print("\n여러 시작점에서의 테스트:")
    for start in starting_points:
        optimal_x, history = optimizer.minimize(quadratic, NDArray([start]))
        print(f"시작점: {start:.1f}, 최종점: {optimal_x[0]:.6f}, 반복 횟수: {len(history)-1}")

def test_learning_rates():
    """다양한 learning rate 테스트"""
    def quadratic(x: NDArray) -> float:
        return x[0]**2 + 2*x[0] + 1

    learning_rates = [0.01, 0.1, 0.5, 1.0]
    initial_x = NDArray([2.0])

    print("\n다양한 learning rate 테스트:")
    for lr in learning_rates:
        optimizer = GradientDescent(learning_rate=lr)
        optimal_x, history = optimizer.minimize(quadratic, initial_x)
        print(f"Learning rate: {lr}, 반복 횟수: {len(history)-1}, 최종점: {optimal_x[0]:.6f}")

if __name__ == "__main__":
    test_gradient_descent()
    test_gradient_descent_concave_up()
    test_multiple_starting_points()
    test_learning_rates()
