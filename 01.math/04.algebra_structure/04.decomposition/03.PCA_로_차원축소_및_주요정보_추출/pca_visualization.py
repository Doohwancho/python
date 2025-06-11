from manim import *
import numpy as np

# manim -pql pca_visualization.py PCAVisualization

class PCAVisualization(Scene):
    """
    PCA(주성분 분석)의 과정을 단계별로 시각화하는 Manim 씬입니다.
    1. 데이터 중심화
    2. 주성분 계산 (고유값 분해)
    3. 주성분 축으로 데이터 투영 (차원 축소)
    """
    def construct(self):
        # -- 0. 초기 설정 및 제목 --
        title = Title("Principal Component Analysis (PCA) Visualization")
        self.add(title)

        # -- 1. 데이터 생성 및 초기 상태 --
        # 일부러 상관관계를 갖는 2D 데이터 생성
        np.random.seed(0)
        mean = [1, 1]
        cov = [[3, 2.5], [2.5, 3]] 
        data_points = np.random.multivariate_normal(mean, cov, 100)

        # Manim의 점(Dot) 객체로 변환
        dots = VGroup(*[Dot(point=np.array([p[0], p[1], 0]), radius=0.06) for p in data_points])
        dots.set_color_by_gradient(BLUE, GREEN)

        # 초기 데이터 플롯
        initial_axes = Axes(x_range=[-5, 5, 1], y_range=[-5, 5, 1], x_length=8, y_length=8)
        initial_data_group = VGroup(initial_axes, dots)
        
        initial_title = Tex("Original 2D Data").to_edge(UP, buff=1.5)
        self.play(Write(initial_title))
        self.play(Create(initial_axes), Create(dots), run_time=2)
        self.wait(2)
        self.play(FadeOut(initial_title))

        # -- 2. 1단계: 데이터 중심 맞추기 (Mean-Centering) --
        step1_title = Tex("Step 1: Mean-Centering").to_edge(UP, buff=1.5)
        self.play(Write(step1_title))
        
        # 데이터의 평균 계산
        mean_vector = np.mean(data_points, axis=0)
        mean_dot = Dot(point=np.array([mean_vector[0], mean_vector[1], 0]), color=RED, radius=0.1)
        mean_label = MathTex(r"\text{Mean}", color=RED).next_to(mean_dot, UR)
        
        self.play(Create(mean_dot), Write(mean_label))
        self.wait(1)
        
        # 모든 점들을 원점으로 이동
        self.play(
            dots.animate.shift(-mean_dot.get_center()),
            FadeOut(mean_dot, mean_label),
            run_time=2
        )
        # 중심화된 데이터 좌표 업데이트
        centered_data = data_points - mean_vector
        self.wait(2)
        self.play(FadeOut(step1_title))

        # -- 3. 2&3단계: 주성분 찾기 (Eigendecomposition) --
        
        # <<< --- 여기가 수정된 부분입니다 --- >>>
        step2_title = Tex("Step 2 \\& 3: Find Principal Components").to_edge(UP, buff=1.5)
        
        self.play(Write(step2_title))
        
        # 공분산 행렬 및 고유값 분해
        covariance_matrix = np.cov(centered_data, rowvar=False)
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
        
        # 고유값 크기 순으로 정렬
        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]
        
        # 주성분(고유벡터) 시각화
        # 길이를 고유값의 제곱근(표준편차)에 비례하게 설정하여 중요도 표현
        pc1_vec = eigenvectors[:, 0] * np.sqrt(eigenvalues[0]) * 1.5
        pc2_vec = eigenvectors[:, 1] * np.sqrt(eigenvalues[1]) * 1.5
        
        pc1 = Vector(pc1_vec, color=YELLOW)
        pc2 = Vector(pc2_vec, color=ORANGE)
        pc1_label = MathTex("PC1", color=YELLOW).next_to(pc1.get_end(), UR)
        pc2_label = MathTex("PC2", color=ORANGE).next_to(pc2.get_end(), UR)

        self.play(
            Create(pc1), Write(pc1_label),
            Create(pc2), Write(pc2_label),
            run_time=2
        )
        self.wait(3)
        self.play(FadeOut(step2_title))

        # -- 4. 4&5단계: 주성분 축으로 변환 및 투영 --
        step3_title = Tex("Step 4 \\& 5: Project Data onto PC1").to_edge(UP, buff=1.5)
        self.play(Write(step3_title))
        
        # PC1 축을 새로운 x축으로 만들기 위한 회전 변환
        angle = -pc1.get_angle()
        
        # 모든 객체들을 회전
        group_to_rotate = VGroup(dots, pc1, pc2, pc1_label, pc2_label, initial_axes)
        self.play(
            group_to_rotate.animate.rotate(angle, about_point=ORIGIN),
            run_time=3
        )
        self.wait(2)
        
        # PC1 축(새로운 x축)으로 점들을 투영
        projection_lines = VGroup()
        projected_dots = VGroup()
        for dot in dots:
            start_point = dot.get_center()
            end_point = np.array([start_point[0], 0, 0])
            projection_lines.add(DashedLine(start_point, end_point, stroke_width=2, stroke_color=WHITE, stroke_opacity=0.5))
            projected_dots.add(Dot(point=end_point, color=RED, radius=0.06))

        self.play(Create(projection_lines), run_time=2)
        self.play(Transform(dots, projected_dots), run_time=2)
        self.wait(2)

        # -- 5. 최종 결과 --
        final_title = Tex("Result: 2D Data reduced to 1D").to_edge(UP, buff=1.5)
        self.play(FadeOut(step3_title), Write(final_title))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])