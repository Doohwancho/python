from manim import *
import numpy as np

# manim -pql prediction_scene.py LeastSquaresPrediction

class LeastSquaresPrediction(Scene):
    def construct(self):
        # --- 0. 설정 및 계산 ---
        title = Text("Predicting the Future with Least Squares").to_edge(UP)
        self.play(Write(title))

        x_data = np.array([1, 2, 3, 4, 5])
        y_data = np.array([15, 22, 28, 35, 43])

        A = np.vstack([np.ones(len(x_data)), x_data]).T
        b = y_data

        x_hat = np.linalg.inv(A.T @ A) @ A.T @ b
        c_hat, m_hat = x_hat
        
        future_x = 7
        predicted_y = c_hat + m_hat * future_x

        # 2. 시각화 객체 생성
        axes = Axes(
            x_range=[0, 8.5, 1],
            y_range=[0, 70, 10],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN, buff=1)
        labels = axes.get_axis_labels(x_label="Day", y_label="Visitors")

        data_points = VGroup(*[Dot(axes.c2p(x, y), color=BLUE) for x, y in zip(x_data, y_data)])
        
        fit_line = axes.plot(lambda x: c_hat + m_hat * x, x_range=[0, 5], color=RED)
        fit_label = MathTex(f"y = {c_hat:.2f} + {m_hat:.2f}x", color=RED).next_to(fit_line, UR, buff=0.2)

        # --- 3. 애니메이션 실행 ---
        
        self.play(Create(axes), Create(labels))
        self.play(Write(Text("Past Data (Day 1-5)").next_to(axes, UP, buff=0.2)))
        self.play(Create(data_points))
        self.wait(2)

        self.play(Write(fit_label))
        self.play(Create(fit_line))
        self.wait(2)

        prediction_text = Text("Predicting for Day 7...").move_to(fit_label.get_center())
        self.play(ReplacementTransform(fit_label, prediction_text))

        # --- 이 부분이 수정되었습니다 ---
        # 1. 먼저 일반 실선 그래프를 생성합니다.
        future_line_solid = axes.plot(lambda x: c_hat + m_hat * x, x_range=[5, future_x], color=RED)
        # 2. 생성된 실선 그래프를 DashedVMobject로 감싸 점선으로 만듭니다.
        future_line_dashed = DashedVMobject(future_line_solid, num_dashes=20)
        
        self.play(Create(future_line_dashed))
        
        # 7일차 지점에서 예측값 찾기
        x_line = axes.get_vertical_line(axes.c2p(future_x, predicted_y), color=YELLOW, line_func=DashedLine)
        y_line = axes.get_horizontal_line(axes.c2p(future_x, predicted_y), color=YELLOW, line_func=DashedLine)
        predicted_dot = Dot(axes.c2p(future_x, predicted_y), color=YELLOW)
        predicted_label = MathTex(f"{predicted_y:.1f}", color=YELLOW).next_to(predicted_dot, RIGHT)

        self.play(Create(x_line))
        self.play(Create(y_line))
        self.play(FadeIn(predicted_dot, scale=1.5), Write(predicted_label))
        self.wait(3)