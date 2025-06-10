from manim import *

# manim -pql basis_scene.py BasisScene

class BasisScene(Scene):
    def construct(self):
        # --- 초기 설정 ---
        title = Text("What is a Basis?").to_edge(UP)
        plane = NumberPlane(x_range=(-6, 6, 1), y_range=(-4, 4, 1), background_line_style={"stroke_opacity": 0.5})
        self.play(Write(title))
        self.play(Create(plane))
        self.wait(1)

        # --- 1. 표준 기저 (Standard Basis) ---
        part1_text = Text("Part 1: The Standard Basis (our default view)").to_edge(DOWN)
        self.play(Write(part1_text))

        i_hat = plane.get_vector([1, 0], color=GREEN)
        j_hat = plane.get_vector([0, 1], color=RED)
        i_label = MathTex(r"\hat{i}", color=GREEN).next_to(i_hat, RIGHT)
        j_label = MathTex(r"\hat{j}", color=RED).next_to(j_hat, UP)
        self.play(Create(i_hat), Create(j_hat), Write(i_label), Write(j_label))

        target_point = np.array([3, 2, 0])
        target_dot = Dot(target_point, color=YELLOW)
        
        # (3,2)를 표준 기저로 표현하는 과정
        path_x = Line(ORIGIN, i_hat.get_end() * 3, color=GREEN, stroke_width=6)
        path_y = Line(path_x.get_end(), target_point, color=RED, stroke_width=6)
        coord_label_std = MathTex(r"\text{Coordinates: } (3, 2) \implies 3\hat{i} + 2\hat{j}").to_corner(UL)

        self.play(Create(target_dot))
        self.play(Create(path_x), run_time=1.5)
        self.play(Create(path_y), run_time=1.5)
        self.play(Write(coord_label_std))
        self.wait(2)
        self.play(FadeOut(part1_text, path_x, path_y))

        # --- 2. 새로운 기저 (A New Basis) ---
        part2_text = Text("Part 2: A New Basis (a different point of view)").to_edge(DOWN)
        self.play(Write(part2_text))

        # 새로운 기저 벡터 b1, b2
        b1 = np.array([2, 1, 0])
        b2 = np.array([-1, 1, 0])
        b1_arrow = Vector(b1, color=ORANGE)
        b2_arrow = Vector(b2, color=PURPLE)
        b1_label = MathTex(r"\vec{b}_1", color=ORANGE).next_to(b1_arrow, direction=np.array([1, -1, 0]))
        b2_label = MathTex(r"\vec{b}_2", color=PURPLE).next_to(b2_arrow, UL)

        self.play(Transform(i_hat, b1_arrow), Transform(j_hat, b2_arrow),
                  Transform(i_label, b1_label), Transform(j_label, b2_label),
                  FadeOut(coord_label_std))
        
        # 새로운 기저에 맞춰 그리드 변환
        matrix = np.array([[b1[0], b2[0], 0], [b1[1], b2[1], 0], [0, 0, 1]])
        self.play(ApplyMatrix(matrix.T, plane), run_time=2)
        
        # 같은 점 (3,2)를 새로운 기저로 표현
        # c1*b1 + c2*b2 = [3,2]  ==> c1=5/3, c2=-1/3 (계산 결과)
        c1, c2 = 5/3, -1/3
        path_b1 = Line(ORIGIN, b1 * c1, color=ORANGE, stroke_width=6)
        path_b2 = Line(path_b1.get_end(), target_point, color=PURPLE, stroke_width=6)
        coord_label_new = MathTex(r"\text{New Coordinates: } (\frac{5}{3}, -\frac{1}{3}) \implies \frac{5}{3}\vec{b}_1 - \frac{1}{3}\vec{b}_2").to_corner(UL)

        self.play(Create(path_b1), run_time=1.5)
        self.play(Create(path_b2), run_time=1.5)
        self.play(Write(coord_label_new))
        self.wait(3)
        self.play(FadeOut(*self.mobjects)) # 모두 지우기

        # --- 3. 기저가 아닌 경우 ---
        final_title = Text("What is NOT a Basis?").to_edge(UP)
        self.play(Write(final_title))
        
        # Case A: 선형 종속
        dep_v1 = Vector([2, 1, 0], color=GREEN)
        dep_v2 = Vector([-2, -1, 0], color=ORANGE)
        dep_text = Text("Linearly Dependent: Cannot span the 2D plane.", font_size=32).shift(UP*2)
        span_line = Line(dep_v1.get_end()*-2, dep_v1.get_end()*2, color=GRAY)
        self.play(Write(dep_text), Create(span_line), Create(dep_v1), Create(dep_v2))
        self.wait(2)
        self.play(FadeOut(dep_v1, dep_v2, span_line, dep_text))

        # Case B: Span 부족
        one_v = Vector([2, 1, 0], color=GREEN)
        one_v_text = Text("Not Enough Vectors: Cannot span the 2D plane.", font_size=32).shift(UP*2)
        span_line_2 = Line(one_v.get_end()*-2, one_v.get_end()*2, color=GRAY)
        self.play(Write(one_v_text), Create(span_line_2), Create(one_v))
        self.wait(3)