from manim import *
import numpy as np

# manim -pql svd_visualization.py SVDVisualization

class SVDVisualization(Scene):
    """
    SVD(특이값 분해)의 과정을 시각적으로 보여주는 Manim 씬입니다.
    A = U * Sigma * V^T
    1. V^T에 의한 회전
    2. Sigma에 의한 신축
    3. U에 의한 회전
    """
    def construct(self):
        # -- 1. 초기 설정 --
        # 변환할 행렬 A (가로 방향으로 찌그러뜨리는 전단 행렬)
        A = np.array([
            [1, 0.5],
            [0, 1]
        ])

        # SVD 계산
        U, s, Vt = np.linalg.svd(A)
        Sigma = np.diag(s)
        V = Vt.T
        
        # Manim에서 사용할 행렬들
        MAT_A = A
        MAT_U = U
        MAT_S = Sigma
        MAT_V = V
        MAT_VT = Vt

        # 기본 그리드와 벡터 생성
        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        ).add_coordinates()
        
        vector = Vector([1, 1], color=YELLOW)
        vector_label = MathTex(r"\vec{v}", color=YELLOW).next_to(vector.get_end(), UR, buff=0.2)

        # 제목과 설명 텍스트
        title = Title("SVD Visualization: $A = U \\Sigma V^T$")
        self.add(title)

        # -- 2. 직접 변환 보여주기 (비교용) --
        direct_transform_title = Tex("Direct Transformation: $A\\vec{v}$").to_edge(UP, buff=1.5)
        
        # 변환 전 상태 복사
        direct_group = VGroup(grid.copy(), vector.copy(), vector_label.copy())

        self.play(Write(direct_transform_title))
        self.play(Create(direct_group))
        self.wait(1)
        
        # 직접 변환 애니메이션
        self.play(
            ApplyMatrix(MAT_A, direct_group),
            run_time=3
        )
        self.wait(2)
        
        # 원래대로 되돌리기
        self.play(FadeOut(direct_group), FadeOut(direct_transform_title))
        self.wait(1)

        # -- 3. SVD 3단계 분해 시각화 --
        # 원본 그리드와 벡터 다시 생성
        svd_group = VGroup(grid, vector, vector_label)
        self.play(Create(svd_group))

        # 단계별 제목
        step_title = Tex("").to_edge(UP, buff=1.5)

        # --- 3.1. 1단계: V^T 적용 (첫 번째 회전) ---
        step1_text = Tex("Step 1: Rotate by $V^T$")
        self.play(Transform(step_title, step1_text))
        
        # V의 기저 벡터(특별한 축) 시각화
        v1 = Vector(MAT_V[:, 0], color=RED)
        v2 = Vector(MAT_V[:, 1], color=BLUE)
        v_labels = VGroup(
            MathTex(r"\vec{v}_1", color=RED).next_to(v1.get_end(), UR, buff=0.1),
            MathTex(r"\vec{v}_2", color=BLUE).next_to(v2.get_end(), DR, buff=0.1)
        )
        self.play(Create(v1), Create(v2), Write(v_labels))
        self.wait(2)
        
        # V^T 변환 (회전)
        self.play(
            ApplyMatrix(MAT_VT, svd_group),
            FadeOut(v1, v2, v_labels),
            run_time=3
        )
        self.wait(2)

        # --- 3.2. 2단계: Sigma 적용 (신축) ---
        step2_text = Tex("Step 2: Scale by $\\Sigma$")
        self.play(Transform(step_title, step2_text))
        
        # 신축 애니메이션
        # Manim의 stretch는 기저벡터 방향으로만 작동하므로,
        # 여기서는 apply_matrix를 사용해 Sigma 변환을 적용합니다.
        # 이 변환은 현재의 x, y축(회전된 축) 방향으로 신축을 일으킵니다.
        self.play(
            ApplyMatrix(MAT_S, svd_group),
            run_time=3
        )
        self.wait(2)

        # --- 3.3. 3단계: U 적용 (두 번째 회전) ---
        step3_text = Tex("Step 3: Rotate by $U$")
        self.play(Transform(step_title, step3_text))

        # U 변환 (회전)
        self.play(
            ApplyMatrix(MAT_U, svd_group),
            run_time=3
        )
        self.wait(2)

        # -- 4. 결과 확인 --
        final_text = Tex("Final Result: $A\\vec{v} = U\\Sigma V^T \\vec{v}$")
        self.play(Transform(step_title, final_text))
        
        # 최종 위치에 원을 그려 강조
        final_pos_circle = Circle(radius=0.2, color=ORANGE, stroke_width=6).move_to(vector.get_end())
        self.play(Create(final_pos_circle))
        self.wait(3)
        
        self.play(
            FadeOut(svd_group),
            FadeOut(step_title),
            FadeOut(title),
            FadeOut(final_pos_circle)
        )
        self.wait(1)