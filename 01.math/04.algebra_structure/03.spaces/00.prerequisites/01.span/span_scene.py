from manim import *

# manim -pql span_scene.py SpanScene

class SpanScene(Scene):
    def construct(self):
        # --- 초기 설정 ---
        title = Text("What is Span?").to_edge(UP)
        plane = NumberPlane(x_range=(-7, 7, 1), y_range=(-5, 5, 1), background_line_style={"stroke_opacity": 0.5})
        self.play(Write(title), Create(plane))
        self.wait(1)

        # --- 1. 벡터 1개의 Span ---
        v1 = np.array([2, 1, 0])
        v1_arrow = Vector(v1, color=GREEN)
        v1_label = MathTex(r"\vec{v}_1", color=GREEN).next_to(v1_arrow, UR)
        
        part1_text = Text("The Span of a single vector...", font_size=36).next_to(title, DOWN)
        self.play(Write(part1_text))
        self.play(GrowArrow(v1_arrow), Write(v1_label))

        # Span은 모든 스칼라 곱의 집합
        span_line = Line(v1 * -4, v1 * 4, color=GREEN, stroke_opacity=0.7)
        span_text = MathTex(r"\text{span}(\vec{v}_1) = \{c \cdot \vec{v}_1 \mid c \in \mathbb{R}\}").next_to(span_line.get_end(), DOWN)
        
        # c*v1 벡터를 보여주며 선을 그림
        c = ValueTracker(1)
        scaled_arrow = always_redraw(lambda: Vector(v1 * c.get_value(), color=YELLOW))
        self.play(Create(span_line), Create(scaled_arrow))
        self.play(c.animate.set_value(-2), run_time=2)
        self.play(c.animate.set_value(2), run_time=2)
        self.play(Write(span_text))
        self.wait(2)
        self.play(FadeOut(part1_text, span_text, scaled_arrow))

        # --- 2. 선형 독립인 벡터 2개의 Span ---
        v2 = np.array([-1, 2, 0])
        v2_arrow = Vector(v2, color=RED)
        v2_label = MathTex(r"\vec{v}_2", color=RED).next_to(v2_arrow, UL)

        part2_text = Text("...add a second, linearly independent vector...", font_size=36).next_to(title, DOWN)
        self.play(Write(part2_text))
        self.play(GrowArrow(v2_arrow), Write(v2_label))
        self.wait(1)

        # c1*v1 + c2*v2 조합으로 평면 전체를 채울 수 있음을 보여줌
        surface = Surface(
            lambda u, v: plane.c2p(u, v),
            u_range=[-7, 7], v_range=[-5, 5],
            fill_opacity=0.3, checkerboard_colors=[BLUE_D, BLUE_E]
        )
        # 기저벡터 변환을 통해 그리드 변형
        new_grid = plane.copy()
        matrix = np.array([[v1[0], v2[0], 0], [v1[1], v2[1], 0], [0, 0, 1]])
        
        span_2d_text = MathTex(r"\text{span}(\vec{v}_1, \vec{v}_2) = \mathbb{R}^2").to_edge(DOWN)
        
        self.play(FadeOut(span_line), FadeIn(surface, target_shape=plane), ApplyMatrix(matrix.T, new_grid), run_time=3)
        self.play(Write(span_2d_text))
        self.wait(2)
        self.play(FadeOut(part2_text, span_2d_text, surface, new_grid))


        # --- 3. 선형 종속인 벡터 2개의 Span ---
        v3 = np.array([-2, -1, 0]) # v3 = -1 * v1
        v3_arrow = Vector(v3, color=ORANGE)
        v3_label = MathTex(r"\vec{v}_3 = -1 \cdot \vec{v}_1", color=ORANGE).next_to(v3_arrow, DL)
        
        part3_text = Text("...but if the second vector is linearly dependent...", font_size=36).next_to(title, DOWN)
        self.play(Write(part3_text), FadeOut(v2_arrow, v2_label))
        self.play(Create(span_line))
        self.play(GrowArrow(v3_arrow), Write(v3_label))
        self.wait(1)
        
        span_1d_text = Text("The Span is still just a line!", color=YELLOW).to_edge(DOWN)
        self.play(Write(span_1d_text))
        self.wait(3)