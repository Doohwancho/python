# manim -pql green_theorem_scene.py GreenTheoremScene
from manim import *

# green_theorem_scene.py
from manim import *

class GreenTheoremScene(Scene):
    def construct(self):
        # 1. 축, 벡터 필드, 경로 설정
        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.5}
        )
        
        # --- 수정된 부분 1: 벡터 필드 함수 내부에서 크기 조절 ---
        def vector_field_func(p):
            x, y, z = p
            # 벡터를 계산하고, 그 크기를 0.2배로 줄여서 반환
            # 이렇게 하면 화살표가 너무 커지지 않음
            return np.array([-y, x, 0]) * 0.2

        # --- 수정된 부분 2: VectorField 생성 시 불필요한 인자 모두 제거 ---
        field = VectorField(vector_field_func)
        
        # 닫힌 경로 C (원)
        curve = Circle(radius=2, color=YELLOW)
        
        # 경로 내부 영역 D
        area = Polygon(*curve.get_points(), fill_color=BLUE, fill_opacity=0.3, stroke_width=0)


        # --- 애니메이션 시작 ---
        self.play(Create(plane))
        self.play(Create(field))
        self.wait()

        # --- 좌변: 선적분(순환) 시각화 ---
        title_lhs = Title("Left Hand Side: Line Integral (Circulation)")
        equation_lhs = MathTex(r"\oint_C \mathbf{F} \cdot d\mathbf{r}", font_size=48).to_corner(UL)
        
        self.play(Write(title_lhs), Create(curve))
        self.play(FadeIn(equation_lhs))

        dot = Dot(color=RED).move_to(curve.get_start())
        self.play(Create(dot))
        self.play(
            MoveAlongPath(dot, curve, rate_func=linear, run_time=4)
        )
        self.play(FadeOut(dot))
        self.wait(1)
        self.play(FadeOut(title_lhs))

        # --- 우변: 중적분(컬의 합) 시각화 ---
        title_rhs = Title("Right Hand Side: Double Integral (Sum of Curl)")
        equation_rhs = MathTex(r"\iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dA", font_size=48).to_corner(UL)
        
        self.play(ReplacementTransform(equation_lhs, equation_rhs))
        self.play(FadeIn(title_rhs))

        # 영역 내부의 작은 회전(Curl)들을 표현하는 스피너 생성
        spinners = VGroup()
        for x in np.arange(-1.5, 2, 1):
            for y in np.arange(-1.5, 2, 1):
                if x**2 + y**2 < 2**2: # 원 내부에만 생성
                    spinner = VGroup(
                        Dot(point=[x, y, 0], radius=0.05, color=WHITE),
                        Arrow(start=[x, y, 0], end=[x, y+0.3, 0], buff=0)
                    )
                    spinners.add(spinner)

        self.play(FadeIn(area))
        self.play(Create(spinners))
        self.play(
            Rotate(spinners, angle=2*PI, about_point=ORIGIN, rate_func=linear, run_time=3)
        )
        self.wait(1)
        
        # --- 최종 결론 ---
        self.play(FadeOut(title_rhs, spinners, area, curve, field))
        
        final_equation = MathTex(
            r"\oint_C \mathbf{F} \cdot d\mathbf{r}", "=", 
            r"\iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dA"
        )
        final_equation.scale(1.2)
        
        self.play(ReplacementTransform(equation_rhs, final_equation))
        
        conclusion_text = Text("Boundary Circulation = Total Inner Spin", font_size=36).next_to(final_equation, DOWN, buff=0.5)
        self.play(Write(conclusion_text))
        self.wait(3)