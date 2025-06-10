from manim import *

# manim -pql fundamental_theorem_general.py FundamentalTheoremGeneralCase

class FundamentalTheoremGeneralCase(ThreeDScene):
    def construct(self):
        # --- 0. 설정: 일반적인 행렬 및 각 공간의 기저벡터 정의 ---
        A_matrix = np.array([[1, 0, 1], [1, 1, 2], [0, 1, 1]])
        
        # 각 공간의 기저벡터 정의
        row_space_basis = [np.array([1, 0, 1]), np.array([0, 1, 1])]
        null_space_basis = np.array([1, 1, -1])
        col_space_basis = [np.array([1, 1, 0]), np.array([0, 1, 1])]
        left_null_space_basis = np.array([1, -1, 1])

        # 입력 벡터 x와 그 성분들
        x_coord = np.array([2, 3, 1])
        # x = x_row + x_null, Ax = Ax_row
        x_row_coord = np.array([1, 2, 2]) # x를 Row Space에 정사영
        x_null_coord = np.array([1, 1, -1]) # x - x_row
        b_coord = A_matrix @ x_coord

        # --- HUD 설정 ---
        legend = VGroup(
            Text("Legend", font_size=28, weight=BOLD), Text("Row Space", color=BLUE), Text("Null Space", color=GRAY),
            Text("Column Space", color=RED), Text("Left Null Space", color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR)
        self.add_fixed_in_frame_mobjects(legend)
        
        # --- 1막: 입력 공간 ---
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=65 * DEGREES, theta=-120 * DEGREES, zoom=0.9)
        self.add(axes)

        title1 = Text("Input Space (ℝ³)", font_size=32).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title1)

        # 기울어진 Row Space와 Null Space 생성
        row_space_plane = Surface(
            lambda u, v: u * row_space_basis[0] + v * row_space_basis[1],
            u_range=[-2, 2], v_range=[-2, 2], checkerboard_colors=[BLUE_D, BLUE_E]
        ).set_opacity(0.5)
        null_space_line = Line3D(start=null_space_basis * -4, end=null_space_basis * 4, color=GRAY, thickness=0.02)
        
        self.play(Create(row_space_plane), Create(null_space_line))
        self.wait(2)

        # 입력 벡터 x와 그 성분들 시각화
        x_vec = Vector(x_coord, color=YELLOW)
        x_row_vec = Vector(x_row_coord, color=BLUE)
        x_null_vec = Arrow(start=x_row_coord, end=x_coord, color=GRAY, buff=0)
        self.play(GrowArrow(x_vec))
        self.play(Transform(x_vec.copy(), x_row_vec))
        self.play(Create(x_null_vec))
        self.wait(2)

        # --- 2막: 변환 ---
        matrix_tex = MathTex(r"A = \begin{bmatrix} 1 & 0 & 1 \\ 1 & 1 & 2 \\ 0 & 1 & 1 \end{bmatrix}").scale(0.8).next_to(legend, DOWN, aligned_edge=RIGHT)
        self.add_fixed_in_frame_mobjects(matrix_tex)
        self.play(Write(matrix_tex))
        
        # 변환이 시작되면서 축도 함께 변함 (ApplyMatrix)
        # x_null은 원점으로, x_row는 b로 변환
        b_vec = Vector(b_coord, color=RED)
        self.play(
            ApplyMatrix(A_matrix, axes),
            FadeOut(x_vec, row_space_plane, null_space_line), # 기존 공간은 숨김
            Transform(x_null_vec, Vector(ORIGIN, color=GRAY)),
            Transform(x_row_vec, b_vec),
            run_time=3
        )
        self.wait(2)
        
        # --- 3막: 출력 공간 ---
        self.play(FadeOut(title1), FadeOut(matrix_tex), FadeOut(x_null_vec))
        title2 = Text("Output Space (ℝ³)", font_size=32).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title2)
        
        # Column Space와 Left Null Space 시각화
        col_space_plane = Surface(
            lambda u, v: u * col_space_basis[0] + v * col_space_basis[1],
            u_range=[-2, 2], v_range=[-2, 2], checkerboard_colors=[RED_D, RED_E]
        ).set_opacity(0.5)
        left_null_space_line = Line3D(start=left_null_space_basis * -4, end=left_null_space_basis * 4, color=PURPLE, thickness=0.02)
        
        self.play(Create(col_space_plane))
        self.play(Create(left_null_space_line))
        
        # 최종 b가 Column Space 위에 있음을 보여줌
        b_on_plane_dot = Dot3D(b_coord, color=YELLOW)
        self.play(FadeIn(b_on_plane_dot, scale=2), FadeOut(x_row_vec))
        self.wait(3)