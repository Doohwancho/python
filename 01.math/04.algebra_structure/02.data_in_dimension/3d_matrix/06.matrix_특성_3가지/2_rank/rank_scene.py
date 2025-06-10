from manim import *

# manim -pql rank_scene.py RankScene

class RankScene(Scene):
    def construct(self):
        # 초기 설정: 격자, 기저 벡터 i, j
        grid = NumberPlane(x_range=(-4, 4, 1), y_range=(-3, 3, 1))
        i_hat = grid.get_vector([1, 0], color=GREEN)
        j_hat = grid.get_vector([0, 1], color=RED)
        i_label = MathTex("\\hat{i}", color=GREEN).next_to(i_hat, RIGHT)
        j_label = MathTex("\\hat{j}", color=RED).next_to(j_hat, UP)

        self.add(grid, i_hat, j_hat, i_label, j_label)
        self.wait(1)

        # 텍스트 라벨 설정
        matrix_label = MathTex("A =").to_edge(UP, buff=0.5).shift(LEFT*2)
        rank_text = MathTex("rank(A) = ").next_to(matrix_label, RIGHT, buff=1)
        output_text = Text("Output is a ").next_to(grid, DOWN)

        # --- 1. Rank = 2 (Full Rank) ---
        matrix_2 = np.array([[1, 1], [0, 1]]) # Shear 행렬
        matrix_tex_2 = MathTex("\\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}").next_to(matrix_label, RIGHT)
        rank_2_text = MathTex("2").next_to(rank_text, RIGHT)
        output_2_text = Text("2D Plane", color=BLUE).next_to(output_text, RIGHT)
        
        self.play(Write(matrix_label), Write(matrix_tex_2), Write(rank_text), Write(rank_2_text))
        self.wait(1)
        
        transform_group = VGroup(grid, i_hat, j_hat, i_label, j_label)
        self.play(ApplyMatrix(matrix_2, transform_group), run_time=2)
        self.play(Write(output_text), Write(output_2_text))
        self.wait(2)

        # --- 2. Rank = 1 ---
        # 원래 상태로 되돌리기
        self.play(ApplyMatrix(np.linalg.inv(matrix_2), transform_group), FadeOut(matrix_tex_2, rank_2_text, output_text, output_2_text))
        self.wait(1)

        matrix_1 = np.array([[2, 1], [-2, -1]]) # Rank가 1인 행렬
        matrix_tex_1 = MathTex("\\begin{bmatrix} 2 & 1 \\\\ -2 & -1 \\end{bmatrix}").next_to(matrix_label, RIGHT)
        rank_1_text = MathTex("1", color=YELLOW).next_to(rank_text, RIGHT)
        output_1_text = Text("1D Line", color=YELLOW).next_to(output_text, RIGHT)

        self.play(Write(matrix_tex_1), Write(rank_1_text))
        self.wait(1)
        
        self.play(ApplyMatrix(matrix_1, transform_group), run_time=2)
        self.play(Write(output_text), Write(output_1_text))
        self.wait(2)

        # --- 3. Rank = 0 ---
        # 이 변환은 역행렬이 없으므로, 객체를 새로 만듬
        self.play(FadeOut(transform_group, matrix_tex_1, rank_1_text, output_text, output_1_text))
        grid = NumberPlane(x_range=(-4, 4, 1), y_range=(-3, 3, 1))
        i_hat = grid.get_vector([1, 0], color=GREEN)
        j_hat = grid.get_vector([0, 1], color=RED)
        i_label = MathTex("\\hat{i}", color=GREEN).next_to(i_hat, RIGHT)
        j_label = MathTex("\\hat{j}", color=RED).next_to(j_hat, UP)
        transform_group = VGroup(grid, i_hat, j_hat, i_label, j_label)
        self.add(transform_group)
        self.wait(1)

        matrix_0 = np.array([[0, 0], [0, 0]]) # Rank가 0인 영행렬
        matrix_tex_0 = MathTex("\\begin{bmatrix} 0 & 0 \\\\ 0 & 0 \\end{bmatrix}").next_to(matrix_label, RIGHT)
        rank_0_text = MathTex("0", color=RED).next_to(rank_text, RIGHT)
        output_0_text = Text("0D Point", color=RED).next_to(output_text, RIGHT)

        self.play(Write(matrix_tex_0), Write(rank_0_text))
        self.wait(1)

        self.play(ApplyMatrix(matrix_0, transform_group), run_time=2)
        self.play(Write(output_text), Write(output_0_text))
        self.wait(3)