from manim import *

# manim -pql linear_independence_scene.py LinearIndependenceScene

class LinearIndependenceScene(Scene):
    def construct(self):
        # --- 초기 설정 ---
        title = Text("What is Linear Independence?").to_edge(UP)
        plane = NumberPlane(x_range=(-7, 7, 1), y_range=(-5, 5, 1), background_line_style={"stroke_opacity": 0.5})
        self.play(Write(title), Create(plane))
        self.wait(1)

        # --- 기준 벡터 v1 ---
        v1 = np.array([2, 1, 0])
        v1_arrow = Vector(v1, color=GREEN)
        v1_label = MathTex(r"\vec{v}_1", color=GREEN).next_to(v1_arrow, UR)
        v1_span_line = Line(v1 * -4, v1 * 4, color=GREEN, stroke_opacity=0.3)
        self.play(GrowArrow(v1_arrow), Write(v1_label), Create(v1_span_line))
        self.wait(1)

        # --- 1. 선형 독립 (Linearly INDEPENDENT) ---
        part1_text = Text("Case 1: Linearly Independent", font_size=36).next_to(title, DOWN)
        self.play(Write(part1_text))

        # v1의 span 위에 있지 않은 새로운 벡터 v2
        v2 = np.array([-1, 2, 0])
        v2_arrow = Vector(v2, color=RED)
        v2_label = MathTex(r"\vec{v}_2", color=RED).next_to(v2_arrow, UL)
        
        explanation1 = Text("v2 adds a new direction. v1 cannot make v2.", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(GrowArrow(v2_arrow), Write(v2_label))
        self.play(Write(explanation1))
        
        # 선형 독립의 정의: c1*v1 + c2*v2 = 0 이려면 c1=0, c2=0 이어야만 함
        def_text1 = MathTex(r"c_1\vec{v}_1 + c_2\vec{v}_2 = \vec{0} \iff c_1=0, c_2=0").next_to(explanation1, UP)
        self.play(FadeOut(explanation1), Write(def_text1))
        self.wait(3)
        self.play(FadeOut(part1_text, v2_arrow, v2_label, def_text1))


        # --- 2. 선형 종속 (Linearly DEPENDENT) ---
        part2_text = Text("Case 2: Linearly Dependent", font_size=36).next_to(title, DOWN)
        self.play(Write(part2_text))

        # v1의 span 위에 있는 새로운 벡터 v3
        v3 = np.array([-3, -1.5, 0]) # v3 = -1.5 * v1
        v3_arrow = Vector(v3, color=ORANGE)
        v3_label = MathTex(r"\vec{v}_3", color=ORANGE).next_to(v3_arrow, DL)
        
        explanation2 = Text("v3 is on the same line. v3 is redundant.", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(GrowArrow(v3_arrow), Write(v3_label))
        self.play(Write(explanation2))

        # 선형 종속의 정의: 0이 아닌 c1, c2로 c1*v1 + c2*v3 = 0 을 만들 수 있음
        def_text2 = MathTex(r"\text{We can find non-zero } c_1, c_2 \text{ for } c_1\vec{v}_1 + c_2\vec{v}_3 = \vec{0}").next_to(explanation2, UP)
        
        # 1.5*v1 + 1*v3 = 0 을 시각적으로 보여줌
        c1, c2 = 1.5, 1
        c1_v1 = Vector(c1 * v1, color=GREEN)
        c2_v3 = Vector(c2 * v3, color=ORANGE).shift(c1 * v1)
        
        sum_path = VGroup(c1_v1, c2_v3)
        
        self.play(FadeOut(explanation2), Write(def_text2))
        self.wait(1)
        
        # v1, v3 숨기고 계산과정 보여주기
        self.play(FadeOut(v1_arrow, v3_arrow, v1_label, v3_label))
        
        c1_v1_label = MathTex(f"{c1}"+r"\vec{v}_1").next_to(c1_v1.get_center(), UP, buff=0.2)
        c2_v3_label = MathTex(f"{c2}"+r"\vec{v}_3").next_to(c2_v3.get_center(), UP, buff=0.2)
        
        self.play(GrowArrow(c1_v1), Write(c1_v1_label))
        self.play(GrowArrow(c2_v3), Write(c2_v3_label))
        
        # 두 벡터의 합이 원점으로 돌아오는 것을 보여줌
        origin_dot = Dot(ORIGIN, color=YELLOW, radius=0.1)
        self.play(Create(origin_dot))
        self.wait(3)