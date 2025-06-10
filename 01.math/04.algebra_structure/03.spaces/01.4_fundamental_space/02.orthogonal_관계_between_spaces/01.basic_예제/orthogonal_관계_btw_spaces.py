from manim import *

# manim -pql orthogonal_관계_btw_spaces.py FundamentalTheoremDeepDive

class FundamentalTheoremDeepDive(ThreeDScene):
    def construct(self):
        # --- 0. 설정 ---
        axes = ThreeDAxes(x_range=[-5, 5, 1], y_range=[-5, 5, 1], z_range=[-5, 5, 1])
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, zoom=0.9)
        self.add(axes)

        A_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
        matrix_tex = MathTex(r"A = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}").to_corner(UR)
        self.add_fixed_in_frame_mobjects(matrix_tex)

        # --- 1막: 변환 전 (Input Space) ---

        title_before = Text("Before Transformation: Input Space (ℝ³)", font_size=32).to_corner(UL)
        legend_before = VGroup(
            Text("Row Space: The 'Effective' Inputs", color=BLUE, font_size=24),
            Text("Null Space: The 'Ignored' Inputs", color=GRAY, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(title_before, DOWN, aligned_edge=LEFT)

        self.add_fixed_in_frame_mobjects(title_before, legend_before)

        row_space_plane = NumberPlane(x_range=[-5, 5], y_range=[-5, 5], color=BLUE, background_line_style={"stroke_opacity": 0.4}).set_opacity(0.5)
        null_space_line = Line3D(start=DOWN*5, end=UP*5, color=GRAY, thickness=0.02)

        self.play(Create(row_space_plane), Create(null_space_line))

        ortho_symbol_1 = VGroup(
            Line(ORIGIN, [0.5, 0, 0]), Line(ORIGIN, [0, 0, 0.5])
        ).set_color(YELLOW)
        self.play(Create(ortho_symbol_1))

        hud_text_1 = Text("Row Space ⟂ Null Space", font_size=24).to_corner(DL)
        self.add_fixed_in_frame_mobjects(hud_text_1)
        self.play(Write(hud_text_1))
        self.wait(2)

        null_vec = Vector([0, 0, 2.5], color=GRAY)
        self.play(GrowArrow(null_vec))

        hud_text_2 = Text("Any vector in the Null Space will be crushed to zero.", font_size=24).next_to(hud_text_1, UP, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(hud_text_2)
        self.play(Write(hud_text_2))
        self.play(Transform(null_vec, Vector(ORIGIN, color=GRAY)))
        self.wait(2)

        self.play(FadeOut(null_vec, hud_text_1, hud_text_2, ortho_symbol_1))

        # --- 2막: 변환 후 (Output Space) ---

        title_after = Text("After Transformation: Output Space", font_size=32).to_corner(UL)
        legend_after = VGroup(
            Text("Column Space: Possible Outputs", color=RED, font_size=24),
            Text("Left Null Space: Unreachable Outputs", color=PURPLE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(title_after, DOWN, aligned_edge=LEFT)

        self.play(
            ReplacementTransform(title_before, title_after),
            ReplacementTransform(legend_before, legend_after)
        )
        self.add_fixed_in_frame_mobjects(title_after, legend_after)

        col_space_plane = NumberPlane(x_range=[-5, 5], y_range=[-5, 5], background_line_style={"stroke_opacity": 0.4}).set_fill(RED, opacity=0.5).set_stroke(RED)
        left_null_space_line = Line3D(start=DOWN*5, end=UP*5, color=PURPLE, thickness=0.02)

        self.play(
            ReplacementTransform(row_space_plane, col_space_plane),
            ReplacementTransform(null_space_line, left_null_space_line),
            run_time=2
        )

        ortho_symbol_2 = VGroup(
            Line(ORIGIN, [0.5, 0, 0]), Line(ORIGIN, [0, 0.5, 0]), Line(ORIGIN, [0, 0, 0.5])
        ).set_color(YELLOW)
        self.play(Create(ortho_symbol_2))

        hud_text_3 = Text("Column Space ⟂ Left Null Space", font_size=24).to_corner(DL)
        self.add_fixed_in_frame_mobjects(hud_text_3)
        self.play(Write(hud_text_3))
        self.wait(3)

# --- 아래 부분이 클래스 밖으로 나와서 수정되었습니다 ---

def main():
    scene = FundamentalTheoremDeepDive()
    scene.render()

# 'name'이 아니라 '__name__' 으로 수정되었습니다.
if __name__ == "__main__":
    main()