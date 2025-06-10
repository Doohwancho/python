from manim import *

# manim -pql ax_b_final.py Ax_b_Super_Explained

class Ax_b_Super_Explained(Scene):
    def construct(self):
        # --- 공통 설정 ---
        A_matrix = np.array([[1, 1], [0, 1]])  # Shear 행렬
        x_coord = np.array([2, 1])
        b_coord = np.dot(A_matrix, x_coord)

        # =====================================================================
        # 1단계: Ax = b 의 의미 시각화 (정방향)
        # =====================================================================
        
        part1_title = Text("Part 1: Visualizing Ax = b").to_edge(UP)
        self.play(Write(part1_title))

        # 초기 공간, 기저 벡터 i, j 와 벡터 x 설정
        plane = NumberPlane().add_coordinates()
        i_hat = plane.get_vector([1, 0], color=GREEN)
        j_hat = plane.get_vector([0, 1], color=RED)
        i_label = MathTex("\\hat{i}", color=GREEN).next_to(i_hat, RIGHT)
        j_label = MathTex("\\hat{j}", color=RED).next_to(j_hat, UP)
        
        x_vector = plane.get_vector(x_coord, color=BLUE)
        # --- 개선점 1: 벡터 x의 좌표를 명시적으로 표시 ---
        x_coord_label = MathTex(r"\vec{x} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}", color=BLUE).next_to(plane.c2p(2, 1), UR)

        self.play(Create(plane), Create(i_hat), Create(j_hat), Write(i_label), Write(j_label))
        self.play(Create(x_vector), Write(x_coord_label))
        self.wait(1)
        
        # --- 개선점 2: 변환 전 원본 축(잔상)을 복사 ---
        ghost_axes = VGroup(i_hat.copy().set_color(GRAY), j_hat.copy().set_color(GRAY))
        self.add(ghost_axes)

        # 변환 A를 적용
        matrix_A_tex = MathTex("A = \\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}").to_edge(UL)
        self.play(Write(matrix_A_tex))

        transform_group = VGroup(plane, i_hat, j_hat, i_label, j_label, x_vector, x_coord_label)
        self.play(ApplyMatrix(A_matrix, transform_group), run_time=3)
        self.wait(1)

        # 변환된 결과가 b임을 표시
        b_label = MathTex(r"\vec{b} = A\vec{x}", color=RED).next_to(plane.c2p(*b_coord), UP)
        self.play(Write(b_label))
        self.wait(3)

        # =====================================================================
        # 2단계: Ax = b 의 해법 시각화 (역방향)
        # =====================================================================

        self.play(FadeOut(*self.mobjects)) # 모든 객체 지우기
        self.wait(1)

        part2_title = Text("Part 2: Finding x from Ax = b").to_edge(UP)
        self.play(Write(part2_title))
        
        # 변환된 공간에서 b를 보여주며 시작
        plane2 = NumberPlane().add_coordinates()
        i_hat2 = plane2.get_vector([1, 0], color=GREEN)
        j_hat2 = plane2.get_vector([0, 1], color=RED)
        # 먼저 변환된 상태로 만듬
        plane2.apply_matrix(A_matrix)
        i_hat2.apply_matrix(A_matrix)
        j_hat2.apply_matrix(A_matrix)

        b_vector_2 = plane2.get_vector(b_coord, color=RED)
        b_label_2 = MathTex("\\vec{b}", color=RED).next_to(b_vector_2, UP)
        
        self.play(Create(plane2), Create(i_hat2), Create(j_hat2), Create(b_vector_2), Write(b_label_2))
        self.wait(1)

        # --- 개선점 2: 변환 전(휘어진) 축의 잔상을 복사 ---
        warped_ghost_axes = VGroup(i_hat2.copy().set_color(GRAY), j_hat2.copy().set_color(GRAY))
        self.add(warped_ghost_axes)

        # 역행렬을 적용하여 공간을 되돌림
        A_inv_matrix = np.linalg.inv(A_matrix)
        matrix_A_inv_tex = MathTex("A^{-1} = \\begin{bmatrix} 1 & -1 \\\\ 0 & 1 \\end{bmatrix}", color=YELLOW).to_edge(UR)
        self.play(Write(matrix_A_inv_tex))
        self.wait(1)

        conclusion2 = MathTex(r"\vec{x} = A^{-1}\vec{b}").next_to(part2_title, DOWN)
        self.play(Write(conclusion2))

        # 역변환 그룹
        inv_transform_group = VGroup(plane2, i_hat2, j_hat2, b_vector_2)
        self.play(ApplyMatrix(A_inv_matrix, inv_transform_group), run_time=3)
        
        # 라벨을 b에서 x로 변경
        self.play(Transform(b_label_2, MathTex(r"\vec{x}", color=BLUE).next_to(b_vector_2, DOWN)))
        self.wait(3)