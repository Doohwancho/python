# manim -pql manim_scene.py DerivativeScene
from manim import *

class DerivativeScene(Scene):
    def construct(self):
        # --- 수정 1: f(x) 함수를 명시적으로 정의 ---
        # lambda를 사용하여 f라는 이름의 함수를 정의합니다.
        f = lambda x: x**2

        # 1. 축과 함수 그래프 설정
        axes = Axes(
            x_range=[-1, 4, 1], y_range=[-1, 10, 2],
            x_length=8, y_length=6, axis_config={"color": BLUE},
        )
        # 이제 이름이 있는 함수 'f'를 사용하여 그래프를 그립니다.
        func = axes.plot(f, color=WHITE)
        
        # 함수 라벨 위치 조정 시에도 'f'를 사용합니다.
        func_label = MathTex(r'f(x) = x^2').next_to(
            axes.c2p(3, f(3)), UR, buff=0.2 # 이제 f(3)이 정상적으로 작동합니다.
        )

        self.play(Create(axes), Create(func), Write(func_label))
        self.wait(1)

        # 2. h 값을 추적하는 ValueTracker 생성
        h = ValueTracker(2)
        x_val = 1

        # 3. 점, 할선, '기울기 삼각형' 등 모든 요소 설정
        p1 = Dot(axes.c2p(x_val, f(x_val)), color=YELLOW)
        p2 = Dot(color=YELLOW)
        
        delta_x_line = Line(color=ORANGE, stroke_width=3)
        delta_y_line = Line(color=ORANGE, stroke_width=3)
        delta_x_label = MathTex(r"\Delta x = h", color=ORANGE, font_size=30)
        delta_y_label = MathTex(r"\Delta y", color=ORANGE, font_size=30)

        secant_line = Line(p1.get_center(), p2.get_center(), color=RED)
        
        # h값에 따라 모든 요소가 계속 업데이트되도록 설정
        def update_all_elements(m):
            current_h = h.get_value()
            p2.move_to(axes.c2p(x_val + current_h, f(x_val + current_h)))
            secant_line.become(Line(p1.get_center(), p2.get_center(), color=RED))
            p3_coords = axes.c2p(x_val + current_h, f(x_val))
            delta_x_line.become(Line(p1.get_center(), p3_coords))
            delta_y_line.become(Line(p3_coords, p2.get_center()))
            delta_x_label.next_to(delta_x_line, DOWN, buff=0.1)
            delta_y_label.next_to(delta_y_line, RIGHT, buff=0.1)
        
        # 애니메이션 시작 전 초기 위치 설정
        update_all_elements(None)
        
        # 'm'의 의미를 명확히 하는 텍스트
        slope_text = MathTex(r"\text{Secant Slope } m = \frac{\Delta y}{\Delta x}", color=RED).to_corner(UR)
        slope_value_text = MathTex(color=YELLOW).next_to(slope_text, DOWN)
        
        def update_slope_value(m):
            current_h = h.get_value()
            if abs(current_h) < 1e-6:
                slope = 2 * x_val
            else:
                slope = (f(x_val + current_h) - f(x_val)) / current_h
            m.become(MathTex(f"m \\approx {slope:.2f}"))
            m.next_to(slope_text, DOWN)
        
        # 모든 객체에 업데이트 함수 한번에 적용
        # Group을 사용하여 updater를 한번에 관리하면 더 안정적입니다.
        group = VGroup(p2, secant_line, delta_x_line, delta_y_line, delta_x_label, delta_y_label, slope_value_text)
        group.add_updater(update_all_elements)
        slope_value_text.add_updater(update_slope_value)


        self.play(Create(p1), Create(group), Write(slope_text))
        self.wait(1)

        # 4. 애니메이션 실행: h 값을 0.01로 줄임
        self.play(h.animate.set_value(0.01), run_time=5)
        self.wait(1)
        
        # 5. 최종 결과 표시
        final_slope_text = MathTex(r"f'(1) = \lim_{h \to 0} m = 2", color=GREEN).next_to(slope_text, DOWN)
        
        # updater들을 모두 제거하여 더 이상 움직이지 않게 함
        group.clear_updaters()
        slope_value_text.clear_updaters()
        
        self.play(
            FadeOut(slope_value_text, delta_x_label, delta_y_label, delta_x_line, delta_y_line),
            FadeIn(final_slope_text),
            secant_line.animate.set_color(GREEN)
        )
        self.wait(2)