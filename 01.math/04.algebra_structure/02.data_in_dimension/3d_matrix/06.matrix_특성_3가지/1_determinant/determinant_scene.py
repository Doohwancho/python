from manim import *

# manim -pql determinant_scene.py DeterminantScene

class DeterminantScene(Scene):
    def construct(self):
        # 초기 설정: 격자, 기저 벡터, 단위 정사각형
        grid = NumberPlane(x_range=(-4, 4, 1), y_range=(-3, 3, 1))
        
        i_hat = grid.get_vector([1, 0], color=GREEN)
        j_hat = grid.get_vector([0, 1], color=RED)
        
        unit_square = Polygon(
            grid.c2p(0, 0), grid.c2p(1, 0), grid.c2p(1, 1), grid.c2p(0, 1),
            fill_color=BLUE, fill_opacity=0.5, stroke_color=BLUE
        )
        
        area_text = MathTex("Area = 1").next_to(unit_square, UP)
        
        self.add(grid, unit_square, i_hat, j_hat, area_text)
        self.wait(1)

        # --- 1. 양수 Determinant: 넓이의 확장 ---
        matrix_pos = np.array([[2, 1], [1, 2]])
        det_pos = np.linalg.det(matrix_pos)
        
        matrix_label_pos = MathTex(
            "A = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix}",
            "\\implies det(A) = 3"
        ).to_edge(UP)
        
        self.play(Write(matrix_label_pos))
        self.wait(1)

        # 변환 그룹
        transform_group = VGroup(grid, unit_square, i_hat, j_hat)
        self.play(ApplyMatrix(matrix_pos, transform_group), run_time=3)

        # 변환 후 넓이 텍스트 업데이트
        new_area_text_pos = MathTex("Area = 3").move_to(area_text.get_center() + UP*0.5)
        self.play(Transform(area_text, new_area_text_pos))
        self.wait(2)

        # --- 2. 음수 Determinant: 공간의 반전 ---
        # 원래 상태로 되돌리기
        self.play(ApplyMatrix(np.linalg.inv(matrix_pos), transform_group), FadeOut(matrix_label_pos, area_text))
        self.add(area_text.move_to(new_area_text_pos.get_center() - UP*0.5)) # 원위치
        self.wait(1)

        matrix_neg = np.array([[-1, 1], [0, 1]])
        det_neg = np.linalg.det(matrix_neg)
        
        matrix_label_neg = MathTex(
            "B = \\begin{bmatrix} -1 & 1 \\\\ 0 & 1 \\end{bmatrix}",
            "\\implies det(B) = -1"
        ).to_edge(UP)

        self.play(Write(matrix_label_neg))
        self.wait(1)

        # 변환 적용
        self.play(ApplyMatrix(matrix_neg, transform_group), run_time=3)
        
        # 방향이 반전되었음을 설명
        orientation_text = Text("Orientation Flipped!", color=YELLOW, font_size=36).next_to(unit_square, DOWN)
        new_area_text_neg = MathTex("Area = |-1| = 1").move_to(area_text.get_center())
        self.play(Write(orientation_text), Transform(area_text, new_area_text_neg))
        self.wait(2)

        # --- 3. 0인 Determinant: 공간의 붕괴 ---
        # 원래 상태로 되돌리기
        self.play(ApplyMatrix(np.linalg.inv(matrix_neg), transform_group), FadeOut(matrix_label_neg, area_text, orientation_text))
        self.add(area_text.move_to(new_area_text_neg.get_center())) # 원위치
        self.wait(1)

        matrix_zero = np.array([[2, 1], [4, 2]])
        det_zero = np.linalg.det(matrix_zero)

        matrix_label_zero = MathTex(
            "C = \\begin{bmatrix} 2 & 1 \\\\ 4 & 2 \\end{bmatrix}",
            "\\implies det(C) = 0"
        ).to_edge(UP)

        self.play(Write(matrix_label_zero))
        self.wait(1)

        # 변환 적용
        self.play(ApplyMatrix(matrix_zero, transform_group), run_time=3)
        
        # 공간이 붕괴되었음을 설명
        collapse_text = Text("Space collapsed into a line!", color=RED, font_size=36).next_to(grid, DOWN)
        new_area_text_zero = MathTex("Area = 0").move_to(area_text.get_center() + LEFT)
        self.play(Write(collapse_text), Transform(area_text, new_area_text_zero))
        self.wait(3)