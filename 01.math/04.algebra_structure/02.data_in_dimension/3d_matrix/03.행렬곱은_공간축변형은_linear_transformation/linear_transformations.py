from manim import *

# Q. how to run?
# A. pip install manim 
#    manim -pql linear_transformations.py VectorAndSpaceTransformation

class VectorAndSpaceTransformation(Scene):
    def construct(self):
        # 1. 초기 설정
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        ).add_coordinates()

        # 기저 벡터 i_hat, j_hat
        i_hat = plane.get_vector([1, 0], color=GREEN)
        j_hat = plane.get_vector([0, 1], color=RED)
        i_label = MathTex("\\hat{i}").next_to(i_hat, RIGHT)
        j_label = MathTex("\\hat{j}").next_to(j_hat, UP)

        # 변환시킬 벡터 v
        v_vector = plane.get_vector([2, 2], color=ORANGE)
        v_label = MathTex("\\vec{v}").next_to(v_vector, UP, buff=0.2)

        self.play(Create(plane), Create(i_hat), Create(j_hat), Create(v_vector))
        self.play(Write(i_label), Write(j_label), Write(v_label))
        self.wait(1)

        # 그룹화: 공간, 벡터, 레이블을 함께 변환하기 위함
        transform_group = VGroup(plane, i_hat, j_hat, v_vector, i_label, j_label, v_label)

        # 2. Shear (밀림) 변환
        shear_matrix = [[1, 1], [0, 1]]
        shear_text = MathTex("Shear: \\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}").to_edge(UP)
        
        self.play(Write(shear_text))
        self.play(ApplyMatrix(shear_matrix, transform_group), run_time=3)
        self.wait(2)

        # 3. Rotate (회전) 변환
        # 원래 상태로 되돌리기 위해 역변환 적용
        inv_shear_matrix = [[1, -1], [0, 1]]
        rotation_matrix = [[0, -1], [1, 0]] # 90도 회전
        rotation_text = MathTex("Rotate: \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}").to_edge(UP)

        self.play(ApplyMatrix(inv_shear_matrix, transform_group), FadeOut(shear_text), run_time=2)
        self.play(Write(rotation_text))
        self.play(ApplyMatrix(rotation_matrix, transform_group), run_time=3)
        self.wait(2)
        
        # 4. Reflection (반사) 변환
        inv_rotation_matrix = [[0, 1], [-1, 0]]
        reflection_matrix = [[-1, 0], [0, 1]] # y축 기준 반사
        reflection_text = MathTex("Reflection: \\begin{bmatrix} -1 & 0 \\\\ 0 & 1 \\end{bmatrix}").to_edge(UP)
        
        self.play(ApplyMatrix(inv_rotation_matrix, transform_group), FadeOut(rotation_text), run_time=2)
        self.play(Write(reflection_text))
        self.play(ApplyMatrix(reflection_matrix, transform_group), run_time=3)
        self.wait(2)