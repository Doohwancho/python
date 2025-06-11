from manim import *

# manim -pql projection_3d_to_2d.py Projection3Dto2D

class Projection3Dto2D(ThreeDScene):
    def construct(self):
        # 1. 설정
        A_matrix = np.array([
            [1, 0.5, 0],
            [0, 1, 0.5]
        ])
        v_3d_coord = np.array([2, 2, 3])
        v_2d_coord = A_matrix @ v_3d_coord

        # 2. HUD 텍스트 (화면에 고정된 2D 텍스트)
        title = Text("2x3 Matrix: 3D -> 2D (Projection)").to_edge(UP)
        matrix_tex = MathTex(r"A = \begin{bmatrix} 1 & 0.5 & 0 \\ 0 & 1 & 0.5 \end{bmatrix}").to_corner(UL)
        v_3d_tex = MathTex(r"\vec{v}_{3D} = \begin{bmatrix} 2 \\ 2 \\ 3 \end{bmatrix}", color=BLUE).next_to(matrix_tex, DOWN, aligned_edge=LEFT)
        v_2d_tex = MathTex(r"\vec{v}_{2D} = \begin{bmatrix} 3 \\ 3.5 \end{bmatrix}", color=RED).next_to(matrix_tex, DOWN, aligned_edge=LEFT)

        self.play(Write(title))
        self.play(Write(matrix_tex), Write(v_3d_tex))

        # 3. 3D 공간 설정 및 시각화
        axes = ThreeDAxes(x_range=[-1, 5, 1], y_range=[-1, 5, 1], z_range=[-1, 5, 1])
        vector_3d = Arrow3D(start=ORIGIN, end=axes.c2p(*v_3d_coord), color=BLUE, resolution=8)

        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, run_time=1.5)
        self.add(axes)
        self.play(Create(vector_3d))
        self.wait(1)

        # 4. 사영(Projection) 과정 시각화
        explanation = Text("Projecting onto the xy-plane (z=0)", font_size=24).next_to(title, DOWN)
        self.play(Write(explanation))

        start_point = axes.c2p(*v_3d_coord)
        end_point = axes.c2p(v_2d_coord[0], v_2d_coord[1], 0)
        projection_line = DashedLine(start_point, end_point, color=GRAY)
        
        self.play(Create(projection_line), run_time=2)
        self.play(FadeOut(explanation, shift=UP))
        self.wait(0.5)

        # --- 애니메이션 로직을 단순하고 명확하게 재구성 ---

        # 5.1. 사영 결과인 2D 벡터를 생성
        vector_2d_as_3d = Arrow3D(start=ORIGIN, end=end_point, color=RED, resolution=8)
        
        self.play(
            ReplacementTransform(v_3d_tex, v_2d_tex), # 라벨을 2D 벡터 정보로 교체
            Create(vector_2d_as_3d) # 새로운 결과 벡터를 그림
        )
        self.wait(1)

        # 5.2. 이해를 도왔던 원본 3D 벡터와 보조선을 숨김
        self.play(
            FadeOut(vector_3d),         # 원래 3D 벡터 숨기기
            FadeOut(projection_line),   # 사영선 숨기기
        )
        self.wait(3)