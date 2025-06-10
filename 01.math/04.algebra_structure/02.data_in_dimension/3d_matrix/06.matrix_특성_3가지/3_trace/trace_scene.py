from manim import *

# manim -pql trace_scene.py TraceScene

class TraceScene(Scene):
    def construct(self):
        # 초기 설정
        grid = NumberPlane(x_range=(-4, 4, 1), y_range=(-3, 3, 1))
        self.add(grid)

        # 타이틀
        title = Text("What is the Trace?").to_edge(UP)
        trace_formula = MathTex(r"A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \implies \text{tr}(A) = a+d").next_to(title, DOWN)
        self.play(Write(title), Write(trace_formula))
        self.wait(2)

        # --- 1. Positive Trace (팽창) ---
        matrix_pos = np.array([[2, 1], [-1, 1.5]])
        
        # 기저벡터와 설명 텍스트
        i_hat = Arrow(ORIGIN, RIGHT, buff=0, color=GREEN)
        j_hat = Arrow(ORIGIN, UP, buff=0, color=RED)
        i_label = MathTex("\\hat{i}", color=GREEN).next_to(i_hat, RIGHT)
        j_label = MathTex("\\hat{j}", color=RED).next_to(j_hat, UP)
        self.play(Create(i_hat), Create(j_hat), Write(i_label), Write(j_label))

        # 변환 후의 기저벡터
        new_i_hat = Arrow(ORIGIN, np.array([matrix_pos[0][0], matrix_pos[1][0], 0]), buff=0, color=GREEN)
        new_j_hat = Arrow(ORIGIN, np.array([matrix_pos[0][1], matrix_pos[1][1], 0]), buff=0, color=RED)

        # a와 d 성분을 시각화할 보조선
        a_line = Line(ORIGIN, [matrix_pos[0][0], 0, 0], color=GREEN, stroke_width=7)
        d_line = Line([matrix_pos[0][1], 0, 0], [matrix_pos[0][1], matrix_pos[1][1], 0], color=RED, stroke_width=7)

        a_brace = Brace(a_line, direction=DOWN)
        d_brace = Brace(d_line, direction=RIGHT)
        a_label = a_brace.get_tex("a = 2")
        d_label = d_brace.get_tex("d = 1.5")
        
        trace_calc_pos = MathTex(r"\text{tr}(A) = a+d = 2+1.5 = 3.5 > 0", r"\\ \implies \text{Overall Expansion}").to_edge(DOWN)
        
        # 애니메이션 실행
        self.play(
            Transform(i_hat, new_i_hat),
            Transform(j_hat, new_j_hat),
            FadeOut(i_label, j_label)
        )
        self.play(Create(a_line), Create(d_line))
        self.play(FadeIn(a_brace, a_label, d_brace, d_label))
        self.play(Write(trace_calc_pos))
        self.wait(3)

        # --- 2. Negative Trace (수축) ---
        # 이전 객체들 숨기기
        self.play(FadeOut(i_hat, j_hat, a_line, d_line, a_brace, a_label, d_brace, d_label, trace_calc_pos))

        matrix_neg = np.array([[-0.5, 1], [1, -1]])
        new_i_hat_neg = Arrow(ORIGIN, np.array([matrix_neg[0][0], matrix_neg[1][0], 0]), buff=0, color=GREEN)
        new_j_hat_neg = Arrow(ORIGIN, np.array([matrix_neg[0][1], matrix_neg[1][1], 0]), buff=0, color=RED)
        
        a_line_neg = Line(ORIGIN, [matrix_neg[0][0], 0, 0], color=GREEN, stroke_width=7)
        d_line_neg = Line([matrix_neg[0][1], 0, 0], [matrix_neg[0][1], matrix_neg[1][1], 0], color=RED, stroke_width=7)

        a_brace_neg = Brace(a_line_neg, direction=DOWN)
        d_brace_neg = Brace(d_line_neg, direction=RIGHT)
        a_label_neg = a_brace_neg.get_tex("a = -0.5")
        d_label_neg = d_brace_neg.get_tex("d = -1")
        
        trace_calc_neg = MathTex(r"\text{tr}(A) = a+d = -0.5 - 1 = -1.5 < 0", r"\\ \implies \text{Overall Contraction}").to_edge(DOWN)

        # 애니메이션 실행
        self.play(Create(i_hat), Create(j_hat))
        self.play(Transform(i_hat, new_i_hat_neg), Transform(j_hat, new_j_hat_neg))
        self.play(Create(a_line_neg), Create(d_line_neg))
        self.play(FadeIn(a_brace_neg, a_label_neg, d_brace_neg, d_label_neg))
        self.play(Write(trace_calc_neg))
        self.wait(3)