from calculus.gradient_descent._1_numerical_differentiation.optimizer import Optimizer
from linear_algebra.ndarray import NDArray
from typing import Callable, Tuple, List


class GradientDescent(Optimizer):
    """Gradient Descent optimization"""
    def minimize(self, f: Callable, initial_x: NDArray) -> Tuple[NDArray, List[float]]:
        """
        Minimize function f starting from initial_x
        Returns: (optimal_x, history_of_f_values)
        """
        x = initial_x.copy() # 시작점
        history = [f(x)]     # 함숫값 기록용 
        
        for i in range(self.max_iterations):         # 반복 
            gradient = self._compute_gradient(f, x)  # 현재 위치에서 미분값(기울기) 구함 (Optimizer.py -> _compute_gradient())
            x = x - gradient * self.learning_rate    # 기울기의 반대방향으로 이동. 
                                                     # (미분값이 양수면 그래프가 우상향이라는 말이니, 왼쪽으로 이동)
                                                     # (미분값이 음수면 그래프가 우사향이라는 말이니, 오른쪽으로 이동)
                                                     # 결국 미분값이 0이되는 방향으로 수렴함 
            
            current_value = f(x)
            history.append(current_value)
            
            # 지금이랑 이전이랑 차이가 엄청 작으면 끝냄 
            if abs(history[-1] - history[-2]) < self.tolerance: # 거의 변화가 없으면 멈춤 
                break                                           # 이때가 미분값이 거의 0이 된 시점
                
        return x, history
