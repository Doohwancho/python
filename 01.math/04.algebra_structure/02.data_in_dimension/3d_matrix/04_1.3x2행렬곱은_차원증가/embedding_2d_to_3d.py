from manim import *

# manim -pql embedding_2d_to_3d.py Embedding2Dto3D

class Embedding2Dto3D(ThreeDScene):
    def construct(self):
        # 1. 설정: 2D 공간, 2D 벡터, 3x2 행렬 정의
        plane = NumberPlane(x_range=[-2, 5], y_range=[-2, 5])
        axes_3d = ThreeDAxes()
        axes_3d.move_to(plane.get_origin())

        v_2d_coord = np.array([3, 2])
        matrix_3x2 = np.array([[1, 0], [0, 1], [1, 0.5]]) # 3x2 행렬

        # 2D 벡터를 3D 벡터로 변환
        v_3d_coord = matrix_3x2 @ v_2d_coord

        # 2. 2D 공간에서 시작
        title = Text("3x2 Matrix: 2D vector to 3D vector (Embedding)").to_edge(UP)
        vector_2d = plane.get_vector(v_2d_coord, color=BLUE)
        v_2d_label = MathTex(r"\vec{v}_{2D} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}", color=BLUE).next_to(vector_2d.get_end(), UR)

        self.play(Write(title))
        self.play(Create(plane), Create(vector_2d), Write(v_2d_label))
        self.wait(1)

        # 3. 3D 공간으로의 변환 애니메이션
        explanation = Text("Embeds the 2D vector into 3D space", font_size=24).next_to(title, DOWN)
        self.play(Write(explanation))

        # 2D 평면을 3D 축으로 교체하면서 카메라 각도 변경 (먼저 카메라 설정)
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, run_time=2)
        self.play(ReplacementTransform(plane, axes_3d))
        self.wait(1)

        # 4. 2D 벡터가 3D 벡터로 '상승'
        vector_3d = Arrow3D(start=ORIGIN, end=v_3d_coord, color=RED)
        v_3d_hud_label = MathTex(r"\vec{v}_{3D} = \begin{bmatrix} 3 \\ 2 \\ 4 \end{bmatrix}", color=RED).to_corner(UR)

        self.play(
            Transform(vector_2d, vector_3d),
            Transform(v_2d_label, v_3d_hud_label)
        )
        self.wait(3)
        