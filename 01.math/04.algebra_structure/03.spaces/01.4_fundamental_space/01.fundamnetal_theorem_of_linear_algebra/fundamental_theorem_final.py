from manim import *

class FundamentalTheoremFinalScene(ThreeDScene):
    def construct(self):
        # --- 0. 설정: 축, 변환 행렬 및 범례(Legend) ---
        axes = ThreeDAxes(x_range=[-5, 5], y_range=[-5, 5], z_range=[-5, 5])
        # 3D 공간을 xy평면으로 사영(projection)시키는 행렬
        A_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
        
        # 화면 우측 상단에 고정될 범례 생성
        legend = VGroup(
            Text("Color Legend", font_size=24, weight=BOLD),
            Text("Row Space", color=BLUE, font_size=20),
            Text("Null Space", color=GRAY, font_size=20),
            Text("Column Space", color=RED, font_size=20),
            Text("Left Null Space", color=PURPLE, font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR)
        
        self.add_fixed_in_frame_mobjects(legend) # 범례를 2D HUD로 추가

        # 카메라 각도 설정
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES, zoom=0.75)
        self.add(axes)

        # --- 1막: 입력 공간(Domain) 시각화 ---
        title1 = Text("Input Space (ℝ³)", font_size=32).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title1)
        
        # Row Space는 xy-평면
        row_space_plane = NumberPlane(x_range=[-5, 5], y_range=[-5, 5], background_line_style={"stroke_opacity": 0.5}).set_color(BLUE).set_opacity(0.5)
        # Null Space는 z-축
        null_space_line = Line3D(start=DOWN*5, end=UP*5, color=GRAY, thickness=0.03)

        self.play(Write(title1))
        self.play(Create(row_space_plane))
        self.play(Create(null_space_line))
        self.wait(2)

        # --- 2막: 변환의 적용 ---
        matrix_tex = MathTex(r"A = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}").scale(0.8).next_to(legend, DOWN, buff=0.2, aligned_edge=RIGHT)
        self.add_fixed_in_frame_mobjects(matrix_tex)
        
        # 기저 벡터 i, j, k 생성
        i_hat = Vector([1,0,0], color=GREEN)
        j_hat = Vector([0,1,0], color=GREEN)
        k_hat = Vector([0,0,1], color=GRAY)
        
        self.play(FadeOut(title1), Write(matrix_tex))
        self.play(GrowArrow(i_hat), GrowArrow(j_hat), GrowArrow(k_hat))
        
        # 변환 설명 텍스트
        transform_text = Text("Applying Transformation A...", font_size=24).next_to(legend, LEFT, buff=0.5)
        self.add_fixed_in_frame_mobjects(transform_text)
        self.play(Write(transform_text))

        # Null Space에 있는 k벡터가 원점으로 붕괴하는 애니메이션
        self.play(Transform(k_hat, Vector(ORIGIN, color=GRAY)), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(i_hat, j_hat, k_hat, transform_text))

        # --- 3막: 출력 공간(Codomain) 시각화 ---
        title2 = Text("Output Space (ℝ³)", font_size=32).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title2)
        
        # Column Space는 변환된 i,j가 span하는 공간 (xy-평면)
        col_space_plane = NumberPlane(x_range=[-5, 5], y_range=[-5, 5], background_line_style={"stroke_opacity": 0.5}).set_color(RED).set_opacity(0.5)
        # Left Null Space는 Column Space에 직교하는 공간 (z-축)
        left_null_space_line = Line3D(start=DOWN*5, end=UP*5, color=PURPLE, thickness=0.03)
        
        self.play(Write(title2))
        self.play(ReplacementTransform(row_space_plane, col_space_plane)) # Row Space가 Column Space로 매핑됨
        self.play(ReplacementTransform(null_space_line, left_null_space_line)) # Null Space와 Left Null Space의 관계
        self.wait(3)