from manim import *

class EigenspaceScene(Scene):
    def construct(self):
        # --- 0. 설정 ---
        plane = NumberPlane(x_range=(-5, 5, 1), y_range=(-5, 5, 1), background_line_style={"stroke_opacity": 0.4})
        title = Text("Eigenspace: The 'Axes' of a Transformation").to_edge(UP)
        matrix = np.array([[3, 1], [0, 2]])
        matrix_tex = MathTex(r"A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}").to_corner(UL)

        self.play(Create(plane), Write(title), Write(matrix_tex))
        self.wait(1)

        # --- 1. 일반적인 벡터의 변환 ---
        v_general = Vector([1, 2], color=WHITE)
        v_general_label = MathTex(r"\vec{v}").next_to(v_general, UR)
        self.play(GrowArrow(v_general), Write(v_general_label))
        
        # 변환 후 벡터
        v_general_transformed = Vector(matrix @ v_general.get_end()[:2], color=YELLOW)
        
        explanation1 = Text("Most vectors change their direction.", font_size=24).to_edge(DOWN)
        self.play(Transform(v_general, v_general_transformed), FadeOut(v_general_label), Write(explanation1))
        self.wait(2)
        self.play(FadeOut(v_general, explanation1))
        
        # --- 2. Eigenspace 1 (고유값 λ=3) ---
        # λ=3에 대한 고유벡터는 [1, 0]이며, 고유공간은 x축이다.
        eigenvalue1_text = MathTex(r"\lambda_1 = 3", color=PURPLE).next_to(matrix_tex, DOWN, aligned_edge=LEFT)
        eigenspace1_line = Line([-5, 0, 0], [5, 0, 0], color=PURPLE, stroke_width=6)
        eigenspace1_label = Text("Eigenspace for λ=3", color=PURPLE, font_size=24).next_to(eigenspace1_line, UP)

        self.play(Write(eigenvalue1_text))
        self.play(Create(eigenspace1_line), Write(eigenspace1_label))

        eig_vec1 = Vector([2, 0], color=PURPLE)
        eig_vec1_label = MathTex(r"\vec{v}_1", color=PURPLE).next_to(eig_vec1, UR)
        self.play(GrowArrow(eig_vec1), Write(eig_vec1_label))
        
        # 변환 후에는 3배 늘어남
        eig_vec1_transformed = Vector(matrix @ eig_vec1.get_end()[:2], color=PURPLE)
        
        self.play(Transform(eig_vec1, eig_vec1_transformed), run_time=2)
        self.wait(2)
        self.play(FadeOut(eig_vec1, eig_vec1_label))

        # --- 3. Eigenspace 2 (고유값 λ=2) ---
        # λ=2에 대한 고유벡터는 [1, -1]이며, 고유공간은 y=-x 직선이다.
        eigenvalue2_text = MathTex(r"\lambda_2 = 2", color=ORANGE).next_to(eigenvalue1_text, DOWN, aligned_edge=LEFT)
        eigenspace2_line = Line([-3.5, 3.5, 0], [3.5, -3.5, 0], color=ORANGE, stroke_width=6)
        eigenspace2_label = Text("Eigenspace for λ=2", color=ORANGE, font_size=24).next_to(eigenspace2_line, UR)
        
        self.play(Write(eigenvalue2_text))
        self.play(ReplacementTransform(eigenspace1_line, eigenspace2_line), ReplacementTransform(eigenspace1_label, eigenspace2_label))

        eig_vec2 = Vector([2, -2], color=ORANGE)
        eig_vec2_label = MathTex(r"\vec{v}_2", color=ORANGE).next_to(eig_vec2, UR)
        self.play(GrowArrow(eig_vec2), Write(eig_vec2_label))
        
        # 변환 후에는 2배 늘어남
        eig_vec2_transformed = Vector(matrix @ eig_vec2.get_end()[:2], color=ORANGE)
        
        self.play(Transform(eig_vec2, eig_vec2_transformed), run_time=2)
        self.wait(3)